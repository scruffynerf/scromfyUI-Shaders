import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderGradientLinear:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "start_color (vec4)": ("VEC4", {"default": [0.0, 0.0, 0.0, 1.0]}),
                "end_color (vec4)": ("VEC4", {"default": [1.0, 1.0, 1.0, 1.0]}),
                "offset (vec2)": ("VEC2", {"default": [0.0, 0.0]}),
                "angle": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 360.0, "step": 0.01}),
                "vertical": ("BOOLEAN", {"default": False}),
                "reverse": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "IMAGE")
    RETURN_NAMES = ("context", "image")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Create"

    def render(self, **kwargs):
        width = kwargs.get("width")
        height = kwargs.get("height")
        start_color = kwargs.get("start_color (vec4)")
        end_color = kwargs.get("end_color (vec4)")
        offset = kwargs.get("offset (vec2)")
        angle = kwargs.get("angle")
        vertical = kwargs.get("vertical")
        reverse = kwargs.get("reverse")
        context = kwargs.get("context")
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
        ctx.uniforms["offset"] = tuple(offset)
        ctx.uniforms["angle"] = float(angle)
        ctx.uniforms["vertical"] = vertical
        ctx.uniforms["reverse"] = reverse
            
        result = ctx.render(shader_code, width, height, base_path=os.path.dirname(shader_path))
        
        # Update context
        context.uniforms["start"] = tuple(start_color)
        context.uniforms["end"] = tuple(end_color)
        context.uniforms["offset"] = tuple(offset)
        context.uniforms["angle"] = float(angle)
        context.uniforms["vertical"] = vertical
        context.uniforms["reverse"] = reverse
        context.uniforms["tile"] = tuple(tile)
        
        return {"ui": {"resolution": [result.shape[2], result.shape[1]]}, "result": (context, result)} # Changed resolution to use result shape

NODE_CLASS_MAPPINGS = {
    "ShaderGradientLinear": ShaderGradientLinear,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderGradientLinear": "Shader: Linear Gradient",
}
