from .includes.shader_manager import GLSLContext

class ShaderUniformVec2Pos:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_pos"}),
                "pos (vec2)": ("VEC2POS", {"default": [0.0, 0.0]}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC2")
    RETURN_NAMES = ("context", "vec2")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        pos = kwargs.get("pos (vec2)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        
        # Handle string input from custom widget or tuple from other nodes
        if isinstance(pos, str):
            coords = [float(x) for x in pos.split(",")]
        else:
            coords = [float(x) for x in pos]
            
        val = (coords[0], coords[1])
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec2Pos": ShaderUniformVec2Pos,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec2Pos": "Shader Uniform Vec2 (Pos)",
}
