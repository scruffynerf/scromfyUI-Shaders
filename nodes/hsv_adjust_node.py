import torch
import os
from .includes.shader_manager import ShaderContext

class ShaderHSVAdjust:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "hue": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
                "saturation": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01}),
                "value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Color"

    def render(self, image, hue, saturation, value):
        # Get the directory where the shader is located for include resolution
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders")
        shader_path = os.path.join(base_dir, "color_hsv.frag")
        
        with open(shader_path, "r") as f:
            shader_code = f.read()
            
        ctx = ShaderContext()
        ctx.set_texture("image", image)
        ctx.uniforms["HSV"] = (float(hue), float(saturation), float(value))
        
        result = ctx.render(shader_code, image.shape[2], image.shape[1], base_dir=base_dir)
        return (result,)

NODE_CLASS_MAPPINGS = {
    "ShaderHSVAdjust": ShaderHSVAdjust,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderHSVAdjust": "Shader HSV Adjust",
}
