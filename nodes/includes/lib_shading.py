import numpy as np

# Scromfy Shaders - Shading Utilities mirroring shaders/lib/shading.lib
# Mirror of web/lib_shading.js and shaders/lib/shading.lib
# Ensure any changes here are mirrored across all versions.

SHADING_SCHARR_X = np.array([
    [1.0, 10.0/3.0, 1.0],
    [0.0, 0.0, 0.0],
    [-1.0, -10.0/3.0, -1.0]
])

SHADING_SCHARR_Y = np.array([
    [1.0, 0.0, -1.0],
    [10.0/3.0, 0.0, -10.0/3.0],
    [1.0, 0.0, -1.0]
])

def shading_normal(pos, func_get_pos):
    e = 0.0001
    k = np.array([1.0, -1.0])
    
    def get_x(p):
        return func_get_pos(p)[0]
    
    n = (
        np.array([1.0, -1.0, -1.0]) * get_x(pos + np.array([e, -e, -e])) +
        np.array([-1.0, -1.0, 1.0]) * get_x(pos + np.array([-e, -e, e])) +
        np.array([-1.0, 1.0, -1.0]) * get_x(pos + np.array([-e, e, -e])) +
        np.array([1.0, 1.0, 1.0]) * get_x(pos + np.array([e, e, e]))
    )
    return n / np.linalg.norm(n)

def shading_fresnel(f0, h, l):
    f0 = np.array(f0)
    h = np.array(h)
    l = np.array(l)
    dot_hl = np.clip(np.dot(h, l), 0.0, 1.0)
    import math
    return f0 + (1.0 - f0) * math.pow(1.0 - dot_hl, 5.0)

def shading_phong_light(kd, ks, view, light_dir, pos, normal, color, ref, shininess):
    kd = np.array(kd)
    ks = np.array(ks)
    vl = (pos - view) / np.linalg.norm(pos - view)
    diffuse = kd * max(0.0, np.dot(vl, normal))
    specular_val = max(0.0, np.dot(vl, ref))
    
    h = (vl - light_dir) / np.linalg.norm(vl - light_dir)
    f = shading_fresnel(ks, h, vl)
    specular = np.power(specular_val, shininess)
    
    return color * (diffuse * (1.0 - f) + specular * f)
