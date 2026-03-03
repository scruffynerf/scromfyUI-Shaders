// name: CIRCULAR GRADIENT
// desc: Generate a two color circular gradient
// category: CREATE
// control: res,

uniform vec4 start;    // 0,0,0,255;;;; rgb | inner color
uniform vec4 end;      // ;;;; rgba         | outer color
uniform vec2 center;   // 0.5,0.5;0;1;0.01  | center position
uniform float radius;  // 0.5;0;2;0.01      | radius size
uniform bool reverse;  //                   | reverse the starting direction

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord / iResolution.xy;
    float dist = distance(uv, center) / radius;
    if (reverse) {
        dist = 1.0 - dist;
    }
    fragColor = mix(start, end, clamp(dist, 0.0, 1.0));
}
