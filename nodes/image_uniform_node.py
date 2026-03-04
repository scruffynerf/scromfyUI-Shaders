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

    RETURN_TYPES = ("GLSL_CONTEXT", "IMAGE")
    RETURN_NAMES = ("context", "image")
    FUNCTION = "append"
    CATEGORY = "Scromfy/Shaders/Uniforms"

    def append(self, name, image, context=None):
        if context is None:
            context = GLSLContext()
        # Keep reference to the image tensor
        context.textures[name] = image
        return {"ui": {"resolution": [image.shape[2], image.shape[1]]}, "result": (context, image)}

NODE_CLASS_MAPPINGS = {
    "ShaderUniformImage": ShaderUniformImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderUniformImage": "Shader Uniform Image",
}
