from .includes.shader_manager import GLSLContext

class ShaderUniformColor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_color"}),
                "r": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "g": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "b": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("VEC3", "GLSL_CONTEXT")
    RETURN_NAMES = ("color", "context")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, r, g, b, context=None):
        if context is None:
            context = GLSLContext()
        val = (float(r), float(g), float(b))
        context.uniforms[name] = val
        return (val, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformColor": ShaderUniformColor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformColor": "Shader Uniform Color",
}
