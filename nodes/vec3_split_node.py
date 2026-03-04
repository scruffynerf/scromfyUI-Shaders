from .includes.shader_manager import GLSLContext

class ShaderVec3Split:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector (vec3)": ("VEC3",),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("context", "x", "y", "z")
    FUNCTION = "split"
    CATEGORY = "Scromfy/Shaders/Util"

    def split(self, **kwargs):
        vector = kwargs.get("vector (vec3)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        
        x = float(vector[0])
        y = float(vector[1])
        z = float(vector[2])
        
        return (context, x, y, z)

NODE_CLASS_MAPPINGS = {
    "ShaderVec3Split": ShaderVec3Split,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderVec3Split": "Vec3 Split",
}
