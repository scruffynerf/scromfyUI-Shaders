from .includes.shader_manager import GLSLContext

class ShaderUniformVec2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_vec2"}),
                "x": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "y": ("FLOAT", {"default": 0.0, "step": 0.01}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC2")
    RETURN_NAMES = ("context", "vec2")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        x = kwargs.get("x (vec2)", 0.0)
        y = kwargs.get("y (vec2)", 0.0)
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        val = (float(x), float(y))
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec2": ShaderUniformVec2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec2": "Shader Uniform Vec2",
}
