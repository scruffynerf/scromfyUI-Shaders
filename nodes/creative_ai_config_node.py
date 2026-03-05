
class CreativeAIConfig:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_url": ("STRING", {"default": "http://localhost:11434/v1/chat/completions"}),
                "model": ("STRING", {"default": "llama3"}),
            }
        }
    
    RETURN_TYPES = ("SCROMFY_AI_SETTINGS",)
    FUNCTION = "pack"
    CATEGORY = "Scromfy/Shaders/Creative"

    def pack(self, api_url, model):
        return ({"api_url": api_url, "model": model},)

NODE_CLASS_MAPPINGS = {
    "CreativeAIConfig": CreativeAIConfig,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeAIConfig": "🤖 Creative AI Config",
}
