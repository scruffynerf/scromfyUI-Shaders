from .includes.shader_manager import GLSLContext

class ShaderUniformVec3Pos:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_pos3"}),
                "pos": ("VEC3POS", {"default": "0.0,0.0,0.0"}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("VEC3", "GLSL_CONTEXT")
    RETURN_NAMES = ("vec3", "context")
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
            
        val = (coords[0], coords[1], coords[2])
        context.uniforms[name] = val
        return (val, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformVec3Pos": ShaderUniformVec3Pos,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformVec3Pos": "Shader Uniform Vec3 (Pos)",
}
