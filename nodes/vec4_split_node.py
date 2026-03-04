from .includes.shader_manager import GLSLContext

class ShaderVec4Split:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector (vec4)": ("VEC4",),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "FLOAT", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("context", "x", "y", "z", "w")
    FUNCTION = "split"
    CATEGORY = "Scromfy/Shaders/Util"

    def split(self, **kwargs):
        vector = kwargs.get("vector (vec4)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        
        x = float(vector[0])
        y = float(vector[1])
        z = float(vector[2])
        w = float(vector[3])
        
        return (context, x, y, z, w)

NODE_CLASS_MAPPINGS = {
    "ShaderVec4Split": ShaderVec4Split,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderVec4Split": "Vec4 Split",
}
