
import os
from .includes.creative_utils import get_available_p5_sketches, GRAPHIC_CODE_DIR

DEFAULT_P5 = """function setup() {
  createCanvas(512, 512);
}

function draw() {
  background(0);
  fill(255);
  ellipse(width/2, height/2, 50, 50);
}"""

class CreativeP5Loader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "select_p5": (get_available_p5_sketches(),),
                "p5_code": ("STRING", {"multiline": True, "default": DEFAULT_P5, "dynamicPrompts": False}),
            },
            "optional": {
                "ai_settings": ("SCROMFY_AI_SETTINGS",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("code",)
    FUNCTION = "load"
    CATEGORY = "Scromfy/Shaders/Creative"

    def load(self, select_p5, p5_code):
        return (p5_code,)

NODE_CLASS_MAPPINGS = {
    "CreativeP5Loader": CreativeP5Loader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreativeP5Loader": "⚙️ P5.js Sketch Loader",
}
