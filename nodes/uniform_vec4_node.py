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

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC4")
    RETURN_NAMES = ("context", "vec4")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        x = kwargs.get("x (vec4)", 0.0)
        y = kwargs.get("y (vec4)", 0.0)
        z = kwargs.get("z (vec4)", 0.0)
        w = kwargs.get("w (vec4)", 0.0)
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        val = (float(x), float(y), float(z), float(w))
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec4": ShaderUniformVec4,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec4": "Shader Uniform Vec4",
}
