import json
from .includes.creative_utils import get_creative_gpu, DEFAULT_SHADER

class CreativeShaderRender:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shader_code": ("STRING", {"forceInput": True}),
                "width": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 8}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 8}),
                "frames": ("INT", {"default": 1, "min": 1, "max": 1000}),
                "fps": ("FLOAT", {"default": 24.0}),
                "time_start": ("FLOAT", {"default": 0.0}),
            },
            "optional": {
                "settings": ("SCROMFY_SETTINGS",),
                "channels": ("SCROMFY_CHANNELS",),
                "custom_uniforms": ("STRING", {"default": "{}"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "code")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Creative"

    def render(self, shader_code, width, height, frames, fps, time_start, settings=None, channels=None, custom_uniforms="{}"):
        if settings:
            shader_code = settings.get("shader_code", shader_code)
            width = settings.get("width", width)
            height = settings.get("height", height)
            frames = settings.get("frames", frames)
            fps = settings.get("fps", fps)
            time_start = settings.get("time_start", time_start)
        
        ch_data = channels if channels else {}
        wrap = ch_data.get("texture_wrap", "repeat")
        filt = ch_data.get("texture_filter", "linear")
        
        try: uniforms = json.loads(custom_uniforms)
        except: uniforms = {}

        gpu = get_creative_gpu()
        images = gpu.render(shader_code, width, height, frames, fps, time_start, uniforms, ch_data, wrap, filt)
        
        return (images, shader_code)

NODE_CLASS_MAPPINGS = {
    "CreativeShaderRender": CreativeShaderRender,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeShaderRender": "✨ Creative Shader Render",
}
