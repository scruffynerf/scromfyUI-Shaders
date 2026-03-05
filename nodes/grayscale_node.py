import os
import torch
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderGrayscale:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "r_weight": ("FLOAT", {"default": 0.299, "min": 0.0, "max": 1.0, "step": 0.001}),
                "g_weight": ("FLOAT", {"default": 0.587, "min": 0.0, "max": 1.0, "step": 0.001}),
                "b_weight": ("FLOAT", {"default": 0.114, "min": 0.0, "max": 1.0, "step": 0.001}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "IMAGE")
    RETURN_NAMES = ("context", "image")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Color"

    def render(self, **kwargs):
        image = kwargs.get("image")
        r_weight = kwargs.get("r_weight")
        g_weight = kwargs.get("g_weight")
        b_weight = kwargs.get("b_weight")
        context = kwargs.get("context")
        
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "graphic_code", "frag", "color_grayscale.frag")
        with open(shader_path, "r") as f:
            shader_code = f.read()
            
        ctx = ShaderContext()
        # Transfer context
        for k, v in context.uniforms.items():
            ctx.uniforms[k] = v
        for k, v in context.textures.items():
            ctx.set_texture(k, v)
        
        ctx.set_texture("image", image)
        ctx.uniforms["convert"] = (float(r_weight), float(g_weight), float(b_weight))
        
        result = ctx.render(shader_code, image.shape[2], image.shape[1], base_path=os.path.dirname(shader_path))
        
        # Update context
        context.uniforms["convert"] = (float(r_weight), float(g_weight), float(b_weight))
        
        return (context, result)

NODE_CLASS_MAPPINGS = {
    "ShaderGrayscale": ShaderGrayscale,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderGrayscale": "Shader: Grayscale",
}
