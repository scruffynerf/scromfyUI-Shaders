void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord.xy / iResolution.xy;
    // Simple red/blue gradient
    fragColor = vec4(uv.x, 0.0, uv.y, 1.0);
}
