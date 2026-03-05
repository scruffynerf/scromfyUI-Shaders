import json

class CreativeUniforms:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "shader_code": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "custom_uniforms": ("STRING", {"default": "{}"}),
            }
        }

    RETURN_TYPES = ("SCROMFY_UNIFORMS",)
    FUNCTION = "process"
    CATEGORY = "Scromfy/Shaders/Creative"

    def process(self, shader_code, custom_uniforms="{}"):
        # The frontend will handle the parsing and slider generation
        # We just pass the string through, which will be updated by the JS widgets
        return (custom_uniforms,)

NODE_CLASS_MAPPINGS = {
    "CreativeUniforms": CreativeUniforms
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeUniforms": "Creative Uniforms"
}
