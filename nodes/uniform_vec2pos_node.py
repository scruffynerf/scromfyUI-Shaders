from .includes.shader_manager import GLSLContext

class ShaderUniformVec2Pos:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_pos"}),
                "x (vec2)": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "y (vec2)": ("FLOAT", {"default": 0.0, "step": 0.01}),
            },
            "optional": {
                "pos (vec2)": ("VEC2POS",),
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC2")
    RETURN_NAMES = ("context", "vec2")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        x = kwargs.get("x", 0.0)
        y = kwargs.get("y", 0.0)
        pos = kwargs.get("pos (vec2)")
        context = kwargs.get("context")
        
        if context is None:
            context = GLSLContext()
        
        if pos is not None:
            # Handle string input from custom widget or tuple from other nodes
            if isinstance(pos, str):
                coords = [float(val_str) for val_str in pos.split(",")]
            else:
                coords = [float(val_item) for val_item in pos]
            val = (coords[0], coords[1])
        else:
            val = (float(x), float(y))
            
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec2Pos": ShaderUniformVec2Pos,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec2Pos": "Shader Uniform Vec2 (Pos)",
}
