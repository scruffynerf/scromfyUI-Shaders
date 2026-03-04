from .includes.shader_manager import GLSLContext

class ShaderVec2Split:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector (vec2)": ("VEC2",),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("context", "x", "y")
    FUNCTION = "split"
    CATEGORY = "Scromfy/Shaders/Util"

    def split(self, **kwargs):
        vector = kwargs.get("vector (vec2)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        
        x = float(vector[0])
        y = float(vector[1])
        
        return (context, x, y)

NODE_CLASS_MAPPINGS = {
    "ShaderVec2Split": ShaderVec2Split,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderVec2Split": "Vec2 Split",
}
