from .includes.shader_manager import GLSLContext

class ShaderUniformColor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_color"}),
                "color (vec3)": ("COLOR", {"default": [1.0, 1.0, 1.0]}),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("GLSL_CONTEXT", "VEC3")
    RETURN_NAMES = ("context", "color")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, **kwargs):
        name = kwargs.get("name")
        color = kwargs.get("color (vec3)")
        context = kwargs.get("context")
        if context is None:
            context = GLSLContext()
        
        # Handle string input from custom widget (if any) or tuple from other nodes
        if isinstance(color, str):
            coords = [float(x) for x in color.split(",")]
        else:
            coords = [float(x) for x in color]
            
        val = (coords[0], coords[1], coords[2])
        context.uniforms[name] = val
        return (context, val)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformColor": ShaderUniformColor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformColor": "Shader Uniform Color",
}
