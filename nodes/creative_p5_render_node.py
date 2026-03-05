import os
import json
import torch
import numpy as np
from PIL import Image, ImageOps
from .includes.creative_utils import P5_CACHE_DIR

class CreativeP5Render:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "p5_code": ("STRING", {"forceInput": True}),
                "width": ("INT", {"default": 512}),
                "height": ("INT", {"default": 512}),
                "frames": ("INT", {"default": 1}),
            },
            "optional": {
                "settings": ("SCROMFY_SETTINGS",),
                "custom_uniforms": ("STRING", {"default": "{}"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "code")
    FUNCTION = "render"
    CATEGORY = "Scromfy/Shaders/Creative"

    def render(self, p5_code, **kwargs):
        settings = kwargs.get("settings")
        width = kwargs.get("width", 512)
        height = kwargs.get("height", 512)
        frames = kwargs.get("frames", 1)
        custom_uniforms = kwargs.get("custom_uniforms", "{}")

        if settings:
            width = settings.get("width", width)
            height = settings.get("height", height)
            frames = settings.get("frames", frames)
        
        try: uniforms = json.loads(custom_uniforms)
        except: uniforms = {}
        
        cache_id = uniforms.get("_p5_uid")
        if not cache_id:
            raise ValueError("P5 Render Error: No baked animation found. Please click 'Bake Animation' in the node UI.")
        
        cache_dir = os.path.join(P5_CACHE_DIR, str(cache_id))
        if not os.path.exists(cache_dir):
            raise ValueError(f"P5 Render Error: Cache directory {cache_id} not found.")

        files = sorted([f for f in os.listdir(cache_dir) if f.lower().endswith('.png')])
        if not files:
            raise ValueError(f"P5 Render Error: No frames found in cache {cache_id}.")

        images = []
        for f in files:
            img = Image.open(os.path.join(cache_dir, f))
            img = ImageOps.exif_transpose(img).convert("RGB")
            img_np = np.array(img).astype(np.float32) / 255.0
            images.append(torch.from_numpy(img_np))
        
        if len(images) < frames:
            while len(images) < frames:
                images.extend(images[:frames - len(images)])
        elif len(images) > frames:
            images = images[:frames]
            
        return (torch.stack(images), p5_code)

NODE_CLASS_MAPPINGS = {
    "CreativeP5Render": CreativeP5Render,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeP5Render": "🎨 Creative P5 Render",
}
