from .includes.shader_manager import GLSLContext

class ShaderUniformInt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_int"}),
                "value": ("INT", {"default": 1, "min": -10000, "max": 10000, "step": 1}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "INT")
    RETURN_NAMES = ("context", "int")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, value, context=None):
        if context is None:
            context = GLSLContext()
        context.uniforms[name] = int(value)
        return (context, int(value))

NODE_CLASS_MAPPINGS = {
    "ShaderUniformInt": ShaderUniformInt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformInt": "Shader Uniform Int",
}
