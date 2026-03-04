import os
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderNormalMap:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "scalar": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "detail": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "flip": ("BOOLEAN", {"default": False}),
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
        image = kwargs.get("image")
        scalar = kwargs.get("scalar")
        detail = kwargs.get("detail")
        flip = kwargs.get("flip")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", "create_normal.frag")
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
        ctx.uniforms["scalar"] = float(scalar)
        ctx.uniforms["detail"] = float(detail)
        ctx.uniforms["flip"] = flip
            
        result = ctx.render(shader_code, image.shape[2], image.shape[1], base_path=os.path.dirname(shader_path))
        
        # Update context
        context.uniforms["scalar"] = float(scalar)
        context.uniforms["detail"] = float(detail)
        context.uniforms["flip"] = flip
        
        return (context, result)

NODE_CLASS_MAPPINGS = {
    "ShaderNormalMap": ShaderNormalMap,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderNormalMap": "Shader: Normal Map",
}
