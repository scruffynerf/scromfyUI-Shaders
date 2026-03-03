import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderFilterRange:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "start": ("VEC3", {"default": [0.0, 0.0, 0.0]}),
                "end": ("VEC3", {"default": [1.0, 1.0, 1.0]}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("IMAGE", "GLSL_CONTEXT")
    RETURN_NAMES = ("image", "context")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Filter"

    def render(self, image, start, end, context=None):
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", "filter_range.frag")
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
        
        # Shader specific uniforms
        ctx.uniforms["start"] = tuple(start)
        ctx.uniforms["end"] = tuple(end)
            
        result = ctx.render(shader_code, image.shape[2], image.shape[1], base_path=os.path.dirname(shader_path))
        
        # Update context
        context.uniforms["start"] = tuple(start)
        context.uniforms["end"] = tuple(end)
        
        return (result, context)

NODE_CLASS_MAPPINGS = {
    "ShaderFilterRange": ShaderFilterRange,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderFilterRange": "Shader: Filter Range",
}
