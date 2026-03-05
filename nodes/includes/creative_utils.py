import hashlib
import json
import os
import threading
from collections import OrderedDict
from typing import List, Optional

import numpy as np
import torch
import moderngl
from PIL import Image, ImageOps

from .shader_manager import ShaderContext

# Constants / Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Graphic code (Shaders, P5) will be stored in 'graphic_code' at the project root
GRAPHIC_CODE_DIR = os.path.join(os.path.dirname(BASE_DIR), "graphic_code")
P5_CACHE_DIR = os.path.join(BASE_DIR, "p5_cache")

os.makedirs(GRAPHIC_CODE_DIR, exist_ok=True)
os.makedirs(P5_CACHE_DIR, exist_ok=True)

def get_available_shaders():
    shaders = ["None"]
    if not os.path.exists(GRAPHIC_CODE_DIR):
        return shaders
    
    # Recursively find .glsl, .frag and .js files
    for root, _, files in os.walk(GRAPHIC_CODE_DIR):
        for f in files:
            if f.endswith(".glsl") or f.endswith(".frag") or f.endswith(".js"):
                rel_path = os.path.relpath(os.path.join(root, f), GRAPHIC_CODE_DIR)
                shaders.append(rel_path.replace("\\", "/"))
                
    return sorted(shaders)

def get_available_frag_shaders():
    shaders = ["None"]
    frag_dir = os.path.join(GRAPHIC_CODE_DIR, "frag")
    if not os.path.exists(frag_dir):
        return shaders
    
    for f in os.listdir(frag_dir):
        if f.endswith((".glsl", ".frag")):
            shaders.append(os.path.join("frag", f).replace("\\", "/"))
                
    return sorted(shaders)

def get_available_p5_sketches():
    sketches = ["None"]
    p5_dir = os.path.join(GRAPHIC_CODE_DIR, "p5")
    if not os.path.exists(p5_dir):
        return sketches
    
    for f in os.listdir(p5_dir):
        if f.endswith(".js"):
            sketches.append(os.path.join("p5", f).replace("\\", "/"))
                
    return sorted(sketches)

DEFAULT_SHADER = """void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec3 col = 0.5 + 0.5 * cos(iTime + uv.xyx + vec3(0, 2, 4));
    fragColor = vec4(col, 1.0);
}"""

class ScromfyCreativeGPU:
    def __init__(self):
        self.shader_ctx = ShaderContext()
        self.ctx = self.shader_ctx.ctx
        self.program_cache = OrderedDict()
        self.max_cache_size = 50
        self.vbo = self.ctx.buffer(np.array([
            -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0,
        ], dtype='f4'))
        self.current_size = (0, 0)
        self.fbo = None
        self.color_tex = None
        self.lock = threading.Lock()

    def _ensure_fbo(self, width, height):
        if self.current_size != (width, height):
            if self.fbo: self.fbo.release()
            if self.color_tex: self.color_tex.release()
            self.color_tex = self.ctx.texture((width, height), 4, dtype='f4')
            self.fbo = self.ctx.framebuffer(color_attachments=[self.color_tex])
            self.current_size = (width, height)

    def _get_program(self, code):
        # Resolve includes using Scromfy's system
        resolved_code = self.shader_ctx.resolve_includes(code)
        
        # Hash for caching
        code_hash = hashlib.sha1(resolved_code.encode()).hexdigest()
        if code_hash in self.program_cache:
            self.program_cache.move_to_end(code_hash)
            return self.program_cache[code_hash]

        # Wrap in Shadertoy if needed
        header = """#version 330
        precision highp float;
        uniform vec3 iResolution;
        uniform float iTime;
        uniform float iTimeDelta;
        uniform int iFrame;
        uniform float iFrameRate;
        uniform vec4 iMouse;
        uniform sampler2D iChannel0;
        uniform sampler2D iChannel1;
        uniform sampler2D iChannel2;
        uniform sampler2D iChannel3;
        out vec4 fragColor;
        """
        
        body = resolved_code
        if "void mainImage" in body and "void main()" not in body:
            body += "\nvoid main() { mainImage(fragColor, gl_FragCoord.xy); }"
        
        full_source = f"{header}\n{body}"
        
        vertex_source = """#version 330
        in vec2 in_pos;
        void main() {
            gl_Position = vec4(in_pos, 0.0, 1.0);
        }
        """
        
        try:
            program = self.ctx.program(vertex_shader=vertex_source, fragment_shader=full_source)
        except Exception as e:
            raise ValueError(f"GLSL Compile Error: {str(e)}")

        if len(self.program_cache) >= self.max_cache_size:
            self.program_cache.popitem(last=False)
        self.program_cache[code_hash] = program
        return program

    def render(self, code, width, height, frame_count, fps, time_start, custom_uniforms, channels, texture_wrap, texture_filter):
        with self.lock:
            self._ensure_fbo(width, height)
            program = self._get_program(code)
            vao = self.ctx.simple_vertex_array(program, self.vbo, 'in_pos')
            
            # Setup textures
            channel_textures = []
            for i in range(4):
                if f"iChannel{i}" in program:
                    program[f"iChannel{i}"].value = i
                    img_tensor = channels.get(f"iChannel{i}")
                    if img_tensor is not None:
                        tex = self.ctx.texture((8,8), 4, dtype='f4') 
                        tex.use(location=i)
                        channel_textures.append(tex)
            
            output_frames = torch.empty((frame_count, height, width, 3), dtype=torch.float32)
            dt = 1.0 / max(fps, 0.001)

            try:
                for i in range(frame_count):
                    t = float(time_start) + (i * dt)
                    
                    if "iResolution" in program: program["iResolution"].value = (float(width), float(height), 1.0)
                    if "iTime" in program: program["iTime"].value = t
                    if "iTimeDelta" in program: program["iTimeDelta"].value = dt
                    if "iFrame" in program: program["iFrame"].value = i
                    if "iFrameRate" in program: program["iFrameRate"].value = float(fps)
                    if "iMouse" in program: program["iMouse"].value = (0.0, 0.0, 0.0, 0.0)

                    for ch_idx in range(4):
                        img_tensor = channels.get(f"iChannel{ch_idx}")
                        if img_tensor is not None:
                            b_idx = i % img_tensor.shape[0]
                            frame = img_tensor[b_idx].flip(0)
                            fh, fw, fc = frame.shape
                            data = frame.cpu().numpy().astype('f4').tobytes()
                            tex = self.ctx.texture((fw, fh), fc, data=data, dtype='f4')
                            
                            if texture_filter == "nearest":
                                tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
                            else:
                                tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
                            
                            if texture_wrap == "clamp":
                                tex.repeat_x = tex.repeat_y = False
                            elif texture_wrap == "mirror":
                                try:
                                    tex.wrap_x = tex.wrap_y = moderngl.MIRRORED_REPEAT
                                except:
                                    tex.repeat_x = tex.repeat_y = True
                            else:
                                tex.repeat_x = tex.repeat_y = True
                                
                            tex.use(location=ch_idx)
                            channel_textures.append(tex)

                    for name, val in custom_uniforms.items():
                        if name in program:
                            try:
                                uniform = program[name]
                                if isinstance(val, (list, tuple)):
                                    val = [float(v) for v in val]
                                    if len(val) == 1: uniform.value = val[0]
                                    else: uniform.value = tuple(val)
                                elif isinstance(val, bool):
                                    uniform.value = 1.0 if val else 0.0
                                else:
                                    uniform.value = float(val)
                            except: continue

                    self.fbo.use()
                    self.ctx.clear(0, 0, 0, 1)
                    vao.render(moderngl.TRIANGLE_STRIP)
                    
                    data = self.fbo.read(components=3, alignment=1, dtype='f4')
                    frame_np = np.frombuffer(data, dtype='f4').reshape((height, width, 3))
                    output_frames[i] = torch.from_numpy(np.flipud(frame_np).copy())

            finally:
                vao.release()
                for tex in channel_textures: 
                    try: tex.release()
                    except: pass
            
            return output_frames

_creative_gpu = None
def get_creative_gpu():
    global _creative_gpu
    if _creative_gpu is None:
        _creative_gpu = ScromfyCreativeGPU()
    return _creative_gpu
