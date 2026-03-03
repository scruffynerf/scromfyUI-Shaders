from .includes.shader_manager import GLSLContext

class ShaderUniformImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "u_texture"}),
                "image": ("IMAGE",),
            },
            "optional": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("IMAGE", "GLSL_CONTEXT")
    RETURN_NAMES = ("image", "context")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, image, context=None):
        if context is None:
            context = GLSLContext()
        # Keep reference to the image tensor
        context.textures[name] = image
        return (image, context)

NODE_CLASS_MAPPINGS = {
    "ShaderUniformImage": ShaderUniformImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformImage": "Shader Uniform Image",
}
