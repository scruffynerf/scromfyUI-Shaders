from .includes.shader_manager import GLSLContext

class ShaderUniformVec4Color:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_color"}),
                "r": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "g": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "b": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "a": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "color (vec4)": ("VEC4COLOR",),
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC4")
    RETURN_NAMES = ("context", "vec4")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        r = kwargs.get("r", 1.0)
        g = kwargs.get("g", 1.0)
        b = kwargs.get("b", 1.0)
        a = kwargs.get("a", 1.0)
        color = kwargs.get("color (vec4)")
        context = kwargs.get("context")
        
        if context is None:
            context = GLSLContext()
        
        if color is not None:
             if isinstance(color, str):
                val = tuple(float(x) for x in color.split(","))
             else:
                val = tuple(color)
        else:
            val = (float(r), float(g), float(b), float(a))
            
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec4Color": ShaderUniformVec4Color,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec4Color": "Shader Uniform Vec4 (Color)",
}
