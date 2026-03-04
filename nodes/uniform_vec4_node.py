from .includes.shader_manager import GLSLContext

class ShaderUniformVec4:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_vec4"}),
                "value (vec4)": ("VEC4", {"default": [0.0, 0.0, 0.0, 0.0]}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC4")
    RETURN_NAMES = ("context", "vec4")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        val = kwargs.get("value (vec4)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec4": ShaderUniformVec4,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec4": "Shader Uniform Vec4",
}
