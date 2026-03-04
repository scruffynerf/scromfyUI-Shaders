from .includes.shader_manager import GLSLContext

class ShaderUniformVec3:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_vec3"}),
                "x": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "y": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "z": ("FLOAT", {"default": 0.0, "step": 0.01}),
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
        x = kwargs.get("x (vec3)", 0.0)
        y = kwargs.get("y (vec3)", 0.0)
        z = kwargs.get("z (vec3)", 0.0)
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        val = (float(x), float(y), float(z))
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec3": ShaderUniformVec3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec3": "Shader Uniform Vec3",
}
