from .includes.shader_manager import GLSLContext

class ShaderUniformFloat:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_float"}),
                "value": ("FLOAT", {"default": 1.0, "min": -10000.0, "max": 10000.0, "step": 0.01}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "FLOAT")
    RETURN_NAMES = ("context", "float")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, value, context=None):
        if context is None:
            context = GLSLContext()
        context.uniforms[name] = float(value)
        return (context, float(value))

NODE_CLASS_MAPPINGS = {
    "ShaderUniformFloat": ShaderUniformFloat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformFloat": "Shader Uniform Float",
}
