from .includes.shader_manager import GLSLContext

class ShaderUniformVec3Pos:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_pos"}),
                "pos (vec3)": ("VEC3POS", {"default": [0.0, 0.0, 1.0]}),
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
        pos = kwargs.get("pos (vec3)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        
        # Handle string input from custom widget or tuple from other nodes
        if isinstance(pos, str):
            coords = [float(x) for x in pos.split(",")]
        else:
            coords = [float(x) for x in pos]
            
        val = (coords[0], coords[1], coords[2])
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec3Pos": ShaderUniformVec3Pos,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec3Pos": "Shader Uniform Vec3 (Pos)",
}
