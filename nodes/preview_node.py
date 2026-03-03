import torch
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderPreview:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "shader_code": ("STRING", {"multiline": True, "forceInput": True}),
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("IMAGE", "GLSL_CONTEXT")
    RETURN_NAMES = ("image", "context")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders"

    def render(self, shader_code, width, height, context=None):
        if context is None:
            context = GLSLContext()
            
        # Backend render for final output
        ctx = ShaderContext()
        # Transfer uniforms from GLSL_CONTEXT
        for k, v in context.uniforms.items():
            ctx.uniforms[k] = v
        # Transfer textures
        for k, v in context.textures.items():
            ctx.set_texture(k, v)
            
        result = ctx.render(shader_code, width, height)
        
        # We also return the context so it can be chained
        return (result, context)

NODE_CLASS_MAPPINGS = {
    "ShaderPreview": ShaderPreview,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderPreview": "Shader Preview (WebGL Live)",
}
