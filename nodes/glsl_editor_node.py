class GlslEditor:
    """
    Basic GLSL Editor using standard ComfyUI multiline string widget.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "code": ("STRING", {"multiline": True, "default": "// Write your GLSL code here\nvoid mainImage(out vec4 fragColor, in vec2 fragCoord) {\n    fragColor = vec4(fragCoord.xy / iResolution.xy, 0.0, 1.0);\n}"}),
                "type": (["fragment", "fragment (shadertoy)"], {"default": "fragment"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("code",)
    FUNCTION = "main"
    CATEGORY = "Scromfy/Shaders/Editors"

    def main(self, code, type):
        return (code,)

NODE_CLASS_MAPPINGS = {
    "GlslEditor": GlslEditor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GlslEditor": "GLSL Editor (Basic)",
}
