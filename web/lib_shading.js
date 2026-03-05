// Scromfy Shaders - Shading Utilities mirroring web/lib/shading.lib
// Mirror of nodes/includes/lib_shading.py and web/lib/shading.lib
// Ensure any changes here are mirrored across all versions.

// (Stub for future WebGL 3D preview shading logic)
export const SHADING_SCHARR_X = [
    [1.0, 10.0 / 3.0, 1.0],
    [0.0, 0.0, 0.0],
    [-1.0, -10.0 / 3.0, -1.0]
];

export const SHADING_SCHARR_Y = [
    [1.0, 0.0, -1.0],
    [10.0 / 3.0, 0.0, -10.0 / 3.0],
    [1.0, 0.0, -1.0]
];
