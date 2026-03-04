import torch
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderRunner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "fragment_code": ("STRING", {"default": "void mainImage(out vec4 fragColor, in vec2 fragCoord) { fragColor = vec4(1.0, 0.0, 0.0, 1.0); }", "multiline": True}),
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "IMAGE", "MASK")
    RETURN_NAMES = ("context", "image", "mask")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders"

    def render(self, fragment_code, width, height, context=None):
        if context is None:
            context = GLSLContext()

        ctx = ShaderContext()
        
        # Apply context uniforms/textures to the renderer
        for name, val in context.uniforms.items():
            ctx.set_uniform(name, val)
        for name, tex in context.textures.items():
            ctx.set_texture(name, tex)

        # Standard uniforms
        ctx.set_uniform("iResolution", (float(width), float(height), 0.0))
        ctx.set_uniform("iTime", 0.0)
        ctx.set_uniform("iFrame", 0)

        # Basic Shadertoy wrapper logic
        full_source = f"""
        #version 330
        precision highp float;
        uniform vec3 iResolution;
        uniform float iTime;
        uniform int iFrame;
        
        // Dynamic uniforms from context
        """
        
        # Add uniform declarations from context
        for name, val in context.uniforms.items():
            if isinstance(val, (float, int)):
                if name.startswith("b_") or name in ["vertical", "reverse"]: # Heuristic for bools
                    full_source += f"uniform bool {name};\n"
                else:
                    full_source += f"uniform float {name};\n"
            elif isinstance(val, (tuple, list)):
                if len(val) == 2:
                    full_source += f"uniform vec2 {name};\n"
                elif len(val) == 3:
                    full_source += f"uniform vec3 {name};\n"
                elif len(val) == 4:
                    full_source += f"uniform vec4 {name};\n"
        
        for name in context.textures.keys():
            full_source += f"uniform sampler2D {name};\n"

        full_source += "\n" + fragment_code + "\n"
        
        # Add main() if only mainImage is provided
        if "void main()" not in full_source:
            full_source += """
            out vec4 finalColor;
            void main() {
                mainImage(finalColor, gl_FragCoord.xy);
            }
            """

        # Resolve includes (lygia, etc.)
        full_source = ctx.resolve_includes(full_source)

        result = ctx.render(full_source, width, height)
        # result is (1, H, W, 4)
        
        image = result[:, :, :, :3]
        mask = result[:, :, :, 3]
        
        return {"ui": {"resolution": [width, height]}, "result": (context, image, mask)}

NODE_CLASS_MAPPINGS = {
    "ShaderRunner": ShaderRunner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderRunner": "Shader Runner",
}
