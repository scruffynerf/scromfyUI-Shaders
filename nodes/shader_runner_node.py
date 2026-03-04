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

    def render(self, **kwargs):
        fragment_code = kwargs.get("fragment_code")
        width = kwargs.get("width")
        height = kwargs.get("height")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()

        ctx = ShaderContext()
        
        # Apply context uniforms/textures to the renderer
        for name, val in context.uniforms.items():
            ctx.set_uniform(name, val)
        for name, tex in context.textures.items():
            ctx.set_texture(name, tex)

        # Dynamic uniforms from context declarations
        dynamic_declarations = ""
        for name, val in context.uniforms.items():
            if isinstance(val, (float, int)):
                if name.startswith("b_") or name in ["vertical", "reverse"]: # Heuristic for bools
                    dynamic_declarations += f"uniform bool {name};\n"
                else:
                    dynamic_declarations += f"uniform float {name};\n"
            elif isinstance(val, (tuple, list)):
                if len(val) == 2:
                    dynamic_declarations += f"uniform vec2 {name};\n"
                elif len(val) == 3:
                    dynamic_declarations += f"uniform vec3 {name};\n"
                elif len(val) == 4:
                    dynamic_declarations += f"uniform vec4 {name};\n"
        
        for name in context.textures.keys():
            dynamic_declarations += f"uniform sampler2D {name};\n"

        full_source = dynamic_declarations + "\n" + fragment_code
        
        result = ctx.render(full_source, width, height)
        # result is (1, H, W, 4)
        
        image = result[:, :, :, :3]
        mask = result[:, :, :, 3]
        
        return {"ui": {"resolution": [width, height]}, "result": (context, image, mask)}

NODE_CLASS_MAPPINGS = {
    "ShaderRunner": ShaderRunner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderRunner": "Shader: Runner",
}
