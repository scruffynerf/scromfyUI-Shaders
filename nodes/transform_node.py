import os
import math
from .includes.shader_manager import ShaderContext, GLSLContext

class ShaderTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "offset (vec2)": ("VEC2", {"default": [0.0, 0.0]}),
                "scale (vec2)": ("VEC2", {"default": [1.0, 1.0]}),
                "rotate": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.01}),
                "tile (vec2)": ("VEC2", {"default": [1.0, 1.0]}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "IMAGE")
    RETURN_NAMES = ("context", "image")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Transform"

    def render(self, **kwargs):
        image = kwargs.get("image")
        offset = kwargs.get("offset (vec2)")
        scale = kwargs.get("scale (vec2)")
        rotate = kwargs.get("rotate")
        tile = kwargs.get("tile (vec2)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
            
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", "transform.frag")
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
        ctx.uniforms["offset"] = tuple(offset)
        ctx.uniforms["scale"] = tuple(scale)
        ctx.uniforms["rotate"] = float(rotate) * math.pi / 180.0
        ctx.uniforms["tile"] = tuple(tile)
            
        result = ctx.render(shader_code, image.shape[2], image.shape[1], base_path=os.path.dirname(shader_path))
        
        # Update context
        context.uniforms["offset"] = tuple(offset)
        context.uniforms["scale"] = tuple(scale)
        context.uniforms["rotate"] = float(rotate) * math.pi / 180.0
        context.uniforms["tile"] = tuple(tile)
        
        return (context, result)

NODE_CLASS_MAPPINGS = {
    "ShaderTransform": ShaderTransform,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderTransform": "Shader: Transform",
}
