from .includes.shader_manager import GLSLContext

class ShaderUniformVec4Color:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_color"}),
                "color (vec4)": ("VEC4COLOR", {"default": [1.0, 1.0, 1.0, 1.0]}),
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
        color = kwargs.get("color (vec4)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        
        # Handle string input from custom widget or tuple from other nodes
        if isinstance(color, str):
            channels = [float(x) for x in color.split(",")]
        else:
            channels = [float(x) for x in color]
            
        val = (channels[0], channels[1], channels[2], channels[3])
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec4Color": ShaderUniformVec4Color,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec4Color": "Shader Uniform Vec4 (Color)",
}
