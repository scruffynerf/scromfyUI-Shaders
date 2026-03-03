from .includes.shader_manager import GLSLContext

class ShaderUniformVec4Color:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_color4"}),
                "color": ("VEC4COLOR", {"default": "1.0,1.0,1.0,1.0"}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("VEC4", "GLSL_CONTEXT")
    RETURN_NAMES = ("vec4", "context")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, color, context=None):
        if context is None:
            context = GLSLContext()
        
        # Handle string input from custom widget or tuple from other nodes
        if isinstance(color, str):
            channels = [float(x) for x in color.split(",")]
        else:
            channels = [float(x) for x in color]
            
        val = (channels[0], channels[1], channels[2], channels[3])
        context.uniforms[name] = val
        return (val, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec4Color": ShaderUniformVec4Color,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec4Color": "Shader Uniform Vec4 (Color)",
}
