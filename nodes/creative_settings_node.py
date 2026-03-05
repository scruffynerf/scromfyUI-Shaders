
import os

class CreativeSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
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
        # Just return the dictionary of settings
        return (kwargs,)

NODE_CLASS_MAPPINGS = {
    "CreativeSettings": CreativeSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeSettings": "⚙️ Creative Settings",
}
