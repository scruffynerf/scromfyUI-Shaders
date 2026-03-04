from .includes.shader_manager import GLSLContext

class ShaderExamineContext:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "context": ("GLSL_CONTEXT",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "examine"
    CATEGORY = "Scromfy/Shaders/Util"

    def examine(self, context):
        if not isinstance(context, GLSLContext):
            return (f"Invalid Context: {type(context)}",)
        
        lines = []
        lines.append("=== GLSL CONTEXT ===")
        
        # Uniforms
        lines.append(f"\nUniforms ({len(context.uniforms)}):")
        if not context.uniforms:
            lines.append("  (None)")
        else:
            # Sort by name for readability
            for name in sorted(context.uniforms.keys()):
                val = context.uniforms[name]
                lines.append(f"  - {name}: {val} ({type(val).__name__})")
        
        # Textures
        lines.append(f"\nTextures ({len(context.textures)}):")
        if not context.textures:
            lines.append("  (None)")
        else:
            for name in sorted(context.textures.keys()):
                tex = context.textures[name]
                # Try to get some info about the texture if possible
                try:
                    import moderngl
                    if isinstance(tex, moderngl.Texture):
                        lines.append(f"  - {name}: {tex.width}x{tex.height} ({tex.components} components)")
                    else:
                        lines.append(f"  - {name}: {type(tex).__name__}")
                except:
                    lines.append(f"  - {name}: Registered")

        return ("\n".join(lines),)

NODE_CLASS_MAPPINGS = {
    "ShaderExamineContext": ShaderExamineContext,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShaderExamineContext": "Shader: Examine Context",
}
