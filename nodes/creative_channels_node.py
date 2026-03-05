class CreativeChannels:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "iChannel0": ("IMAGE",),
                "iChannel1": ("IMAGE",),
                "iChannel2": ("IMAGE",),
                "iChannel3": ("IMAGE",),
                "texture_wrap": (["repeat", "clamp", "mirror"], {"default": "repeat"}),
                "texture_filter": (["linear", "nearest"], {"default": "linear"}),
            }
        }
    
    RETURN_TYPES = ("SCROMFY_CHANNELS",)
    FUNCTION = "pack"
    CATEGORY = "Scromfy/Shaders/Creative"

    def pack(self, **kwargs):
        return (kwargs,)

NODE_CLASS_MAPPINGS = {
    "CreativeChannels": CreativeChannels,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeChannels": "🖼️ Creative Channels",
}
