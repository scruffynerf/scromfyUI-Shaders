import torch
from .includes.shader_manager import ShaderContext

class ShaderGrayscale:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "r_weight": ("FLOAT", {"default": 0.299, "min": 0.0, "max": 1.0, "step": 0.001}),
                "g_weight": ("FLOAT", {"default": 0.587, "min": 0.0, "max": 1.0, "step": 0.001}),
                "b_weight": ("FLOAT", {"default": 0.114, "min": 0.0, "max": 1.0, "step": 0.001}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Color"

    def render(self, image, r_weight, g_weight, b_weight):
        shader_path = "shaders/color_grayscale.frag"
        with open(shader_path, "r") as f:
            shader_code = f.read()
            
        ctx = ShaderContext()
        ctx.set_texture("image", image)
        ctx.uniforms["convert"] = (float(r_weight), float(g_weight), float(b_weight))
        
        result = ctx.render(shader_code, image.shape[2], image.shape[1])
        return (result,)

NODE_CLASS_MAPPINGS = {
    "ShaderGrayscale": ShaderGrayscale,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderGrayscale": "Shader Grayscale",
}
