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

    RETURN_TYPES = ("VEC3", "GLSL_CONTEXT")
    RETURN_NAMES = ("vec3", "context")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, x, y, z, context=None):
        if context is None:
            context = GLSLContext()
        val = (float(x), float(y), float(z))
        context.uniforms[name] = val
        return (val, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec3": ShaderUniformVec3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec3": "Shader Uniform Vec3",
}
