import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderSobel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "IMAGE")
    RETURN_NAMES = ("context", "image")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Filter"

    def render(self, **kwargs):
        image = kwargs.get("image")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", "filter_sobel.frag")
        with open(shader_path, 'r') as f:
            shader_code = f.read()
            
        ctx = ShaderContext()
        # Transfer uniforms
        for k, v in context.uniforms.items():
            ctx.uniforms[k] = v
        # Transfer textures
        for k, v in context.textures.items():
            ctx.set_texture(k, v)
        
        # Shader specific texture
        ctx.set_texture("image", image)
            
        result = ctx.render(shader_code, image.shape[2], image.shape[1], base_path=os.path.dirname(shader_path))
        
        # Update context (though Sobel doesn't add uniforms, it might be part of a chain)
        return (context, result)

NODE_CLASS_MAPPINGS = {
    "ShaderSobel": ShaderSobel,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderSobel": "Shader: Sobel Edges",
}
