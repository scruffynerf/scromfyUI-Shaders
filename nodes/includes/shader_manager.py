import moderngl
import numpy as np
import torch
import platform
import os
import re
from PIL import Image

class ShaderContext:
    def __init__(self):
        self.ctx = None
        self.uniforms = {}
        self.textures = {}
        self.buffers = {} # Persistent buffers for feedback
        self.processed_includes = set()
        self._init_context()

    def _init_context(self):
        try:
            # Create standalone context - ModernGL will attempt to find the best backend
            self.ctx = moderngl.create_standalone_context()
        except Exception as e:
            print(f"Failed to create standalone ModernGL context: {e}")
            try:
                # Fallback to default standalone
                self.ctx = moderngl.create_context(standalone=True)
            except Exception as e2:
                raise RuntimeError(f"Could not initialize ModernGL context: {e2}")

    def set_uniform(self, name, value):
        self.uniforms[name] = value

    def resolve_includes(self, source, base_path=None):
        """Recursively resolve #include directives"""
        def replace_include(match):
            include_path = match.group(1).strip()
            
            # Search order:
            # 1. Relative to base_path (if provided)
            # 2. Relative to web/lygia/ (for library files)
            
            search_dirs = []
            if base_path:
                search_dirs.append(base_path)
            
            # Library root (consolidated in web/lygia)
            lib_root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "web")
            search_dirs.append(lib_root)
            
            full_path = None
            for d in search_dirs:
                # Handle lygia/ prefix
                if include_path.startswith("lygia/"):
                    candidate = os.path.join(lib_root, "lygia", include_path[6:])
                else:
                    # For local includes like .lib/ or others
                    candidate = os.path.join(d, include_path)
                
                if os.path.exists(candidate):
                    full_path = candidate
                    break
            
            if full_path:
                if full_path in self.processed_includes:
                    return f"// {include_path} already included"
                
                self.processed_includes.add(full_path)
                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                    # Prepend a marker for debugging
                    return f"// BEGIN {include_path}\n" + self.resolve_includes(content, os.path.dirname(full_path)) + f"\n// END {include_path}"
                except Exception as e:
                    return f"// ERROR: Failed to read {include_path}: {str(e)}"
            return f"// ERROR: Could not find {include_path}"

        # Support both #include "file" and #include file
        return re.sub(r'#include\s+["<]?([^"\s>]+)[">]?', replace_include, source)

    def set_texture(self, name, tensor):
        """Convert torch tensor (B, H, W, C) to ModernGL texture"""
        if tensor is None:
            return
        
        # If it's already a texture object (e.g. from another pass), just store it
        if isinstance(tensor, moderngl.Texture):
            self.textures[name] = tensor
            return

        # Assume batch size 1 for now or take the first frame
        if len(tensor.shape) == 4:
            img_data = tensor[0].cpu().numpy()
        else:
            img_data = tensor.cpu().numpy()

        # ModernGL expects H, W, C
        h, w, c = img_data.shape
        texture = self.ctx.texture((w, h), c, data=img_data.astype('f4').tobytes(), dtype='f4')
        self.textures[name] = texture

    def _get_buffer_definitions(self, source):
        """Find BUFFER_N and DOUBLE_BUFFER_N in source"""
        buffers = re.findall(r'BUFFER_(\d+)', source)
        double_buffers = re.findall(r'DOUBLE_BUFFER_(\d+)', source)
        return sorted(list(set(buffers))), sorted(list(set(double_buffers)))

    def render(self, fragment_source, width, height, vertex_source=None, base_path=None):
        # 0. Resolve includes first to see what's really in there
        fragment_source = self.resolve_includes(fragment_source, base_path)

        # 1. Strip existing #version if present to re-inject properly
        version_line = "#version 330"
        precision_line = "precision highp float;"
        
        # Check if version exists
        v_match = re.search(r'#version\s+\d+\b.*', fragment_source)
        if v_match:
            version_line = v_match.group(0)
            fragment_source = fragment_source[:v_match.start()] + fragment_source[v_match.end():]
            
        # Check if precision exists
        p_match = re.search(r'precision\s+\w+\s+float;', fragment_source)
        if p_match:
            precision_line = p_match.group(0)
            fragment_source = fragment_source[:p_match.start()] + fragment_source[p_match.end():]

        preamble = """
            uniform float iTime;
            uniform float u_time;
            uniform vec3 iResolution;
            uniform vec3 u_resolution;
            uniform vec4 iMouse;
        """

        # Shadertoy wrapper if main() is missing but mainImage is present
        wrapper_top = ""
        wrapper_bottom = ""
        if "void main()" not in fragment_source and "void mainImage" in fragment_source:
            wrapper_top = "out vec4 fragColor;\n"
            wrapper_bottom = "\nvoid main() { mainImage(fragColor, gl_FragCoord.xy); }\n"

        def assemble_shader(defines=""):
            return f"{version_line}\n{precision_line}\n{defines}\n{preamble}\n{wrapper_top}\n{fragment_source}\n{wrapper_bottom}"

        if vertex_source is None:
            vertex_source = """
                #version 330
                in vec2 in_vert;
                out vec2 uv;
                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                    uv = in_vert * 0.5 + 0.5;
                }
            """

        # 1. Scan for buffers
        buffers_n, _ = self._get_buffer_definitions(fragment_source)
        
        # Internal textures for passes
        pass_textures = {}

        # 2. Full screen quad setup
        vbo = self.ctx.buffer(np.array([
            -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0,
        ], dtype='f4'))

        def run_pass(src, out_fbo=None):
            prog = self.ctx.program(vertex_shader=vertex_source, fragment_shader=src)
            vao = self.ctx.simple_vertex_array(prog, vbo, 'in_vert')
            
            # Use standard uniforms
            for name, value in self.uniforms.items():
                if name in prog:
                    try: prog[name].value = value
                    except: pass

            # Use input textures
            tex_idx = 0
            for name, tex in self.textures.items():
                if name in prog:
                    tex.use(tex_idx)
                    prog[name].value = tex_idx
                    tex_idx += 1
            
            # Use previous pass textures
            for name, tex in pass_textures.items():
                if name in prog:
                    tex.use(tex_idx)
                    prog[name].value = tex_idx
                    tex_idx += 1

            if out_fbo:
                out_fbo.use()
            else:
                self.ctx.screen.use()
            
            self.ctx.clear(0, 0, 0, 0)
            vao.render(moderngl.TRIANGLE_STRIP)
            
            # Cleanup pass-specific objects
            vao.release()
            prog.release()

        # 3. Render each BUFFER_N
        for b_idx in buffers_n:
            defines = f"#define BUFFER_{b_idx}"
            pass_src = assemble_shader(defines)
            tex = self.ctx.texture((width, height), 4, dtype='f4')
            fbo = self.ctx.framebuffer(color_attachments=[tex])
            run_pass(pass_src, fbo)
            pass_textures[f"u_buffer{b_idx}"] = tex
            fbo.release()

        # 4. Main pass
        main_src = assemble_shader()
        main_tex = self.ctx.texture((width, height), 4, dtype='f4')
        main_fbo = self.ctx.framebuffer(color_attachments=[main_tex])
        run_pass(main_src, main_fbo)

        # 5. Read back
        data = main_fbo.read(components=4, dtype='f4')
        img = np.frombuffer(data, dtype='f4').reshape((height, width, 4))
        
        # 6. Cleanup
        main_fbo.release()
        main_tex.release()
        for tex in pass_textures.values():
            tex.release()
        vbo.release()
        
        # Clear transient textures
        for tex in self.textures.values():
            tex.release()
        self.textures.clear()
        
        return torch.from_numpy(img).unsqueeze(0)

class GLSLContext:
    """Wrapper for ComfyUI connection type"""
    def __init__(self):
        self.uniforms = {}
        self.textures = {}

    def update(self, other):
        if isinstance(other, GLSLContext):
            self.uniforms.update(other.uniforms)
            self.textures.update(other.textures)
        return self
