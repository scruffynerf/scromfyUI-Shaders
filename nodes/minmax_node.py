import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderMinMax:
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

    RETURN_TYPES = ("IMAGE", "GLSL_CONTEXT")
    RETURN_NAMES = ("image", "context")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Filter"

    def render(self, image, context=None):
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", "filter_minmax.frag")
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
        
        return (result, context)

NODE_CLASS_MAPPINGS = {
    "ShaderMinMax": ShaderMinMax,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderMinMax": "Shader: MinMax Filter",
}
