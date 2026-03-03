from .includes.shader_manager import GLSLContext

class ShaderUniformVec4:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_vec4"}),
                "x": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "y": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "z": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "w": ("FLOAT", {"default": 0.0, "step": 0.01}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("VEC4", "GLSL_CONTEXT")
    RETURN_NAMES = ("vec4", "context")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, x, y, z, w, context=None):
        if context is None:
            context = GLSLContext()
        val = (float(x), float(y), float(z), float(w))
        context.uniforms[name] = val
        return (val, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec4": ShaderUniformVec4,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec4": "Shader Uniform Vec4",
}
