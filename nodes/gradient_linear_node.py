import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderGradientLinear:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "start_color": ("VEC4", {"default": [0.0, 0.0, 0.0, 1.0]}),
                "end_color": ("VEC4", {"default": [1.0, 1.0, 1.0, 1.0]}),
                "vertical": ("BOOLEAN", {"default": False}),
                "reverse": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("IMAGE", "GLSL_CONTEXT")
    RETURN_NAMES = ("image", "context")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Create"

    def render(self, width, height, start_color, end_color, vertical, reverse, context=None):
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", "gradient_linear.frag")
        with open(shader_path, 'r') as f:
            shader_code = f.read()
            
        ctx = ShaderContext()
        # Transfer uniforms
        for k, v in context.uniforms.items():
            ctx.uniforms[k] = v
        # Transfer textures
        for k, v in context.textures.items():
            ctx.set_texture(k, v)
        
        # Shader specific uniforms
        ctx.uniforms["start"] = tuple(start_color)
        ctx.uniforms["end"] = tuple(end_color)
        ctx.uniforms["vertical"] = vertical
        ctx.uniforms["reverse"] = reverse
            
        result = ctx.render(shader_code, width, height, base_path=os.path.dirname(shader_path))
        
        # Update context
        context.uniforms["start"] = tuple(start_color)
        context.uniforms["end"] = tuple(end_color)
        context.uniforms["vertical"] = vertical
        context.uniforms["reverse"] = reverse
        
        return (result, context)

NODE_CLASS_MAPPINGS = {
    "ShaderGradientLinear": ShaderGradientLinear,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderGradientLinear": "Shader: Linear Gradient",
}
