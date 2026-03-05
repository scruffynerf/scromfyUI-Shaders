
import os
from .includes.creative_utils import get_available_frag_shaders, GRAPHIC_CODE_DIR, DEFAULT_SHADER

class CreativeGLSLLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "select_shader": (get_available_frag_shaders(),),
                "shader_code": ("STRING", {"multiline": True, "default": DEFAULT_SHADER, "dynamicPrompts": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("code",)
    FUNCTION = "load"
    CATEGORY = "Scromfy/Shaders/Creative"

    def load(self, select_shader, shader_code):
        # The frontend handles updating shader_code when select_shader changes.
        # This node just passes the code along.
        return (shader_code,)

NODE_CLASS_MAPPINGS = {
    "CreativeGLSLLoader": CreativeGLSLLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeGLSLLoader": "⚙️ GLSL Shader Loader",
}
