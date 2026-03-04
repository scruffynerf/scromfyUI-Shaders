import torch
from .includes.shader_manager import ShaderContext, GLSLContext
import os

class ShaderFileLoader:
    @classmethod
    def INPUT_TYPES(s):
        # Scan shaders directory
        shader_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders")
        shaders = []
        if os.path.exists(shader_dir):
            shaders = [f for f in os.listdir(shader_dir) if f.endswith(".frag")]
        
        return {
            "required": {
                "shader_file": (shaders,),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "load"
    CATEGORY = "Scromfy/Shaders"

    def load(self, shader_file):
        shader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shaders", shader_file)
        with open(shader_path, 'r') as f:
            return (f.read(),)

NODE_CLASS_MAPPINGS = {
    "ShaderFileLoader": ShaderFileLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderFileLoader": "Shader: File Loader",
}
