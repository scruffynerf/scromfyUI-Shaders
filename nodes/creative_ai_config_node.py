
class CreativeAIConfig:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_url": ("STRING", {"default": "http://localhost:11434/v1/chat/completions"}),
                "model": ("STRING", {"default": "llama3"}),
                "max_retries": ("INT", {"default": 1, "min": 0, "max": 5}),
                "system_prompt": ("STRING", {
                    "multiline": True, 
                    "default": "You are an expert GLSL (or P5) coder, you are being given existing code and the user request of how to change or adapt it."
                }),
            }
        }
    
    RETURN_TYPES = ("SCROMFY_AI_SETTINGS",)
    FUNCTION = "pack"
    CATEGORY = "Scromfy/Shaders/Creative"

    def pack(self, api_url, model, max_retries, system_prompt):
        return ({"api_url": api_url, "model": model, "max_retries": max_retries, "system_prompt": system_prompt},)

NODE_CLASS_MAPPINGS = {
    "CreativeAIConfig": CreativeAIConfig,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeAIConfig": "🤖 Creative AI Config",
}
