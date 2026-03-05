---
description: basic creative glsl workflow
---
1. Add the "✨ Creative Shader Render" node.
2. Enter the following code:
```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    uniform float speed; // 1.0; 0.0; 5.0; 0.1 | Animation Speed
    vec3 col = 0.5 + 0.5 * cos(iTime * speed + uv.xyx + vec3(0, 2, 4));
    fragColor = vec4(col, 1.0);
}
```
3. Notice that a "speed" slider automatically appears in the "Dynamic Uniforms" section.
4. Adjust the slider and see the preview update.
5. Queue Prompt to render the sequence.
