import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderGradientCircular:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "start_color (vec4)": ("VEC4", {"default": [0.0, 0.0, 0.0, 1.0]}),
                "end_color (vec4)": ("VEC4", {"default": [1.0, 1.0, 1.0, 1.0]}),
                "center (vec2)": ("VEC2", {"default": [0.5, 0.5]}),
                "radius": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0, "step": 0.01}),
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
        center = kwargs.get("center (vec2)")
        radius = kwargs.get("radius")
        reverse = kwargs.get("reverse")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", "gradient_circular.frag")
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
        ctx.uniforms["center"] = tuple(center)
        ctx.uniforms["radius"] = float(radius)
        ctx.uniforms["reverse"] = reverse
            
        result = ctx.render(shader_code, width, height, base_path=os.path.dirname(shader_path))
        
        # Update context
        context.uniforms["start"] = tuple(start_color)
        context.uniforms["end"] = tuple(end_color)
        context.uniforms["center"] = tuple(center)
        context.uniforms["radius"] = float(radius)
        context.uniforms["reverse"] = reverse
        
        return {"ui": {"resolution": [width, height]}, "result": (context, result)}

NODE_CLASS_MAPPINGS = {
    "ShaderGradientCircular": ShaderGradientCircular,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderGradientCircular": "Shader: Circular Gradient",
}
