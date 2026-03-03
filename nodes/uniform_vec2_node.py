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

    RETURN_TYPES = ("VEC2", "GLSL_CONTEXT")
    RETURN_NAMES = ("vec2", "context")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, x, y, context=None):
        if context is None:
            context = GLSLContext()
        val = (float(x), float(y))
        context.uniforms[name] = val
        return (val, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec2": ShaderUniformVec2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec2": "Shader Uniform Vec2",
}
