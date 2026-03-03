from .includes.shader_manager import GLSLContext

class ShaderUniformVec2Pos:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_pos"}),
                "pos": ("VEC2POS", {"default": "0.0,0.0"}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("VEC2", "GLSL_CONTEXT")
    RETURN_NAMES = ("vec2", "context")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, pos, context=None):
        if context is None:
            context = GLSLContext()
        
        # Handle string input from custom widget or tuple from other nodes
        if isinstance(pos, str):
            coords = [float(x) for x in pos.split(",")]
        else:
            coords = [float(x) for x in pos]
            
        val = (coords[0], coords[1])
        context.uniforms[name] = val
        return (val, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec2Pos": ShaderUniformVec2Pos,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec2Pos": "Shader Uniform Vec2 (Pos)",
}
