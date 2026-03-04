from .includes.shader_manager import GLSLContext

class ShaderUniformVec3:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_vec3"}),
                "value (vec3)": ("VEC3", {"default": [0.0, 0.0, 0.0]}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC3")
    RETURN_NAMES = ("context", "vec3")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        val = kwargs.get("value (vec3)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec3": ShaderUniformVec3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec3": "Shader Uniform Vec3",
}
