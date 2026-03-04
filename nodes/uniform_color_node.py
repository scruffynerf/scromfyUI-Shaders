from .includes.shader_manager import GLSLContext

class ShaderUniformColor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_color"}),
                "r": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "g": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "b": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "color (vec3)": ("VEC3COLOR",),
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC3")
    RETURN_NAMES = ("context", "color")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        r = kwargs.get("r", 1.0)
        g = kwargs.get("g", 1.0)
        b = kwargs.get("b", 1.0)
        color = kwargs.get("color (vec3)")
        context = kwargs.get("context")
        
        if context is None:
            context = GLSLContext()
        
        if color is not None:
             if isinstance(color, str):
                val = tuple(float(x) for x in color.split(","))
             else:
                val = tuple(color)
        else:
            val = (float(r), float(g), float(b))
            
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformColor": ShaderUniformColor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformColor": "Shader Uniform Color",
}
