import torch
import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderBloom:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 1.0, "step": 0.01}),
                "intensity": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 200.0, "step": 0.1}),
                "blur_size": ("FLOAT", {"default": 3.0, "min": 0.0, "max": 100.0, "step": 0.1}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "IMAGE")
    RETURN_NAMES = ("context", "image")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Filter"

    def render(self, image, threshold, intensity, blur_size, context=None):
        if context is None:
            context = GLSLContext()

        # Get the directory where the shader is located for include resolution
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders")
        shader_path = os.path.join(base_dir, "filter_bloom.frag")
        
        with open(shader_path, "r") as f:
            shader_code = f.read()
            
        ctx = ShaderContext()
        # Transfer context
        for k, v in context.uniforms.items():
            ctx.uniforms[k] = v
        for k, v in context.textures.items():
            ctx.set_texture(k, v)

        ctx.set_texture("image", image)
        ctx.uniforms["threshold"] = float(threshold)
        ctx.uniforms["intensity"] = float(intensity)
        ctx.uniforms["blurSize"] = float(blur_size)
        
        result = ctx.render(shader_code, image.shape[2], image.shape[1], base_path=base_dir)

        # Update context
        context.uniforms["threshold"] = float(threshold)
        context.uniforms["intensity"] = float(intensity)
        context.uniforms["blurSize"] = float(blur_size)

        return {"ui": {"resolution": [image.shape[2], image.shape[1]]}, "result": (context, result)}

NODE_CLASS_MAPPINGS = {
    "ShaderBloom": ShaderBloom,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderBloom": "Shader Bloom",
}
