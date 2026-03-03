# Scromfy Shaders - Color Conversion Utilities mirroring shaders/lib/convert.lib
# Mirror of web/lib_convert.js and shaders/lib/convert.lib
# Ensure any changes here are mirrored across all versions.

import math
import numpy as np
from .lib_const import M_PI, M_EPSILON, M_DEG2RAD

# LAB constants
M_LAB_E = 0.008856
M_LAB_K = 903.3
M_LAB_16_116 = 16.0 / 116.0

# Illuminants
M_D50 = [96.422, 100.0, 82.521]
M_D65 = [95.047, 100.0, 108.883]
M_D75 = [94.972, 100.0, 122.638]

def convert_rgb2hsv(rgb):
    r, g, b = rgb
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    d = max_c - min_c
    
    h = 0.0
    if d > 0:
        if max_c == r:
            h = (g - b) / d + (6.0 if g < b else 0.0)
        elif max_c == g:
            h = (b - r) / d + 2.0
        elif max_c == b:
            h = (r - g) / d + 4.0
        h /= 6.0
    
    s = 0 if max_c == 0 else d / max_c
    v = max_c
    return [h, s, v]

def convert_hsv2rgb(hsv):
    h, s, v = hsv
    h = h % 1.0
    s = max(0.0, min(1.0, s))
    v = max(0.0, min(1.0, v))
    
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    
    mod = int(i % 6)
    if mod == 0: return [v, t, p]
    if mod == 1: return [q, v, p]
    if mod == 2: return [p, v, t]
    if mod == 3: return [p, q, v]
    if mod == 4: return [t, p, v]
    return [v, p, q]

def convert_rgb2xyz(rgb):
    def pivot(c):
        return math.pow((c + 0.055) / 1.055, 2.4) if c > 0.04045 else c / 12.92
    r, g, b = [pivot(c) for c in rgb]
    
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    
    return [x * 100.0, y * 100.0, z * 100.0]

def convert_xyz2rgb(xyz):
    x, y, z = [v / 100.0 for v in xyz]
    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570
    
    def pivot(c):
        return 1.055 * math.pow(c, 1.0/2.4) - 0.055 if c > 0.0031308 else 12.92 * c
    return [max(0.0, min(1.0, pivot(c))) for c in [r, g, b]]

def convert_xyz2lab(xyz):
    x, y, z = [xyz[0] / M_D65[0], xyz[1] / M_D65[1], xyz[2] / M_D65[2]]
    def pivot(n):
        return math.pow(n, 1.0/3.0) if n > M_LAB_E else (M_LAB_K * n + 16.0) / 116.0
    fx, fy, fz = [pivot(v) for v in [x, y, z]]
    
    l = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return [l, a, b]

def convert_lab2xyz(lab):
    l, a, b = lab
    fy = (l + 16.0) / 116.0
    fx = a / 500.0 + fy
    fz = fy - b / 200.0
    
    def pivot(f):
        f3 = math.pow(f, 3.0)
        return f3 if f3 > M_LAB_E else (116.0 * f - 16.0) / M_LAB_K
    
    x, y, z = [pivot(f) for f in [fx, fy, fz]]
    return [x * M_D65[0], y * M_D65[1], z * M_D65[2]]

def convert_rgb2lab(rgb):
    return convert_xyz2lab(convert_rgb2xyz(rgb))

def convert_lab2rgb(lab):
    return convert_xyz2rgb(convert_lab2xyz(lab))

def convert_rgb2oklab(rgb):
    r, g, b = rgb
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    
    l = math.pow(l, 1.0/3.0)
    m = math.pow(m, 1.0/3.0)
    s = math.pow(s, 1.0/3.0)
    
    L_out = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a_out = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    b_out = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return [L_out, a_out, b_out]

def convert_oklab2rgb(oklab):
    L, a, b = oklab
    l = L + 0.3963377774 * a + 0.2158037573 * b
    m = L - 0.1055613458 * a - 0.0638541728 * b
    s = L - 0.0894841775 * a - 1.2914855480 * b
    
    l = math.pow(l, 3.0)
    m = math.pow(m, 3.0)
    s = math.pow(s, 3.0)
    
    R = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    G = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    B = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return [max(0.0, min(1.0, R)), max(0.0, min(1.0, G)), max(0.0, min(1.0, B))]
