import os
from .includes.creative_utils import get_available_shaders, DEFAULT_SHADER, GRAPHIC_CODE_DIR

class CreativeSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "select_shader": (get_available_shaders(), {"default": "None"}),
                "shader_code": ("STRING", {"default": DEFAULT_SHADER, "multiline": True}),
                "width": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 8}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 8}),
                "frames": ("INT", {"default": 1, "min": 1, "max": 1000}),
                "fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 120.0}),
                "time_start": ("FLOAT", {"default": 0.0}),
            }
        }
    
    RETURN_TYPES = ("SCROMFY_SETTINGS",)
    FUNCTION = "pack"
    CATEGORY = "Scromfy/Shaders/Creative"

    def pack(self, **kwargs):
        shader = kwargs.get("select_shader")
        if shader and shader != "None":
            path = os.path.join(GRAPHIC_CODE_DIR, shader)
            if os.path.exists(path):
                with open(path, "r") as f:
                    kwargs["shader_code"] = f.read()
        return (kwargs,)

NODE_CLASS_MAPPINGS = {
    "CreativeSettings": CreativeSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeSettings": "⚙️ Creative Settings",
}
