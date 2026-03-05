// Scromfy Shaders - Color Conversion Utilities mirroring web/lib/convert.lib
// Mirror of nodes/includes/lib_convert.py and web/lib/convert.lib
// Ensure any changes here are mirrored across all versions.

import * as Const from "./lib_const.js";

// LAB constants
export const M_LAB_E = 0.008856;
export const M_LAB_K = 903.3;
export const M_LAB_16_116 = 16.0 / 116.0;

// Illuminants
export const M_D50 = [96.422, 100.0, 82.521];
export const M_D65 = [95.047, 100.0, 108.883];
export const M_D75 = [94.972, 100.0, 122.638];

export function convert_rgb2hsv(rgb) {
    let [r, g, b] = rgb;
    let max_v = Math.max(r, g, b);
    let min_v = Math.min(r, g, b);
    let d = max_v - min_v;

    let h = 0.0;
    if (d > 0) {
        if (max_v === r) {
            h = (g - b) / d + (g < b ? 6.0 : 0.0);
        } else if (max_v === g) {
            h = (b - r) / d + 2.0;
        } else if (max_v === b) {
            h = (r - g) / d + 4.0;
        }
        h /= 6.0;
    }

    let s = max_v === 0 ? 0 : d / max_v;
    let v = max_v;
    return [h, s, v];
}

export function convert_hsv2rgb(hsv) {
    let [h, s, v] = hsv;
    h = h % 1.0;
    s = Math.max(0.0, Math.min(1.0, s));
    v = Math.max(0.0, Math.min(1.0, v));

    let i = Math.floor(h * 6.0);
    let f = h * 6.0 - i;
    let p = v * (1.0 - s);
    let q = v * (1.0 - f * s);
    let t = v * (1.0 - (1.0 - f) * s);

    let mod = i % 6;
    if (mod === 0) return [v, t, p];
    if (mod === 1) return [q, v, p];
    if (mod === 2) return [p, v, t];
    if (mod === 3) return [p, q, v];
    if (mod === 4) return [t, p, v];
    return [v, p, q];
}

export function convert_rgb2xyz(rgb) {
    const pivot = (c) => c > 0.04045 ? Math.pow((c + 0.055) / 1.055, 2.4) : c / 12.92;
    let [r, g, b] = rgb.map(pivot);

    let x = r * 0.4124 + g * 0.3576 + b * 0.1805;
    let y = r * 0.2126 + g * 0.7152 + b * 0.0722;
    let z = r * 0.0193 + g * 0.1192 + b * 0.9505;

    return [x * 100.0, y * 100.0, z * 100.0];
}

export function convert_xyz2rgb(xyz) {
    let [x, y, z] = xyz.map(v => v / 100.0);
    let r = x * 3.2406 + y * -1.5372 + z * -0.4986;
    let g = x * -0.9689 + y * 1.8758 + z * 0.0415;
    let b = x * 0.0557 + y * -0.2040 + z * 1.0570;

    const pivot = (c) => c > 0.0031308 ? 1.055 * Math.pow(c, 1.0 / 2.4) - 0.055 : 12.92 * c;
    return [r, g, b].map(c => Math.max(0.0, Math.min(1.0, pivot(c))));
}

export function convert_xyz2lab(xyz) {
    let [x, y, z] = [xyz[0] / M_D65[0], xyz[1] / M_D65[1], xyz[2] / M_D65[2]];
    const pivot = (n) => n > M_LAB_E ? Math.pow(n, 1.0 / 3.0) : (M_LAB_K * n + 16.0) / 116.0;
    let [fx, fy, fz] = [x, y, z].map(pivot);

    let l = 116.0 * fy - 16.0;
    let a = 500.0 * (fx - fy);
    let b = 200.0 * (fy - fz);
    return [l, a, b];
}

export function convert_lab2xyz(lab) {
    let [l, a, b] = lab;
    let fy = (l + 16.0) / 116.0;
    let fx = a / 500.0 + fy;
    let fz = fy - b / 200.0;

    const pivot = (f) => {
        let f3 = Math.pow(f, 3.0);
        return f3 > M_LAB_E ? f3 : (116.0 * f - 16.0) / M_LAB_K;
    };

    let [x, y, z] = [fx, fy, fz].map(pivot);
    return [x * M_D65[0], y * M_D65[1], z * M_D65[2]];
}

export function convert_rgb2lab(rgb) {
    return convert_xyz2lab(convert_rgb2xyz(rgb));
}

export function convert_lab2rgb(lab) {
    return convert_xyz2rgb(convert_lab2xyz(lab));
}

export function convert_rgb2oklab(rgb) {
    let [r, g, b] = rgb;
    let l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b;
    let m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b;
    let s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b;

    l = Math.pow(l, 1.0 / 3.0);
    m = Math.pow(m, 1.0 / 3.0);
    s = Math.pow(s, 1.0 / 3.0);

    let L_out = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s;
    let a_out = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s;
    let b_out = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s;
    return [L_out, a_out, b_out];
}

export function convert_oklab2rgb(oklab) {
    let [L, a, b] = oklab;
    let l = L + 0.3963377774 * a + 0.2158037573 * b;
    let m = L - 0.1055613458 * a - 0.0638541728 * b;
    let s = L - 0.0894841775 * a - 1.2914855480 * b;

    l = Math.pow(l, 3.0);
    m = Math.pow(m, 3.0);
    s = Math.pow(s, 3.0);

    let R = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s;
    let G = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s;
    let B = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s;
    return [Math.max(0.0, Math.min(1.0, R)), Math.max(0.0, Math.min(1.0, G)), Math.max(0.0, Math.min(1.0, B))];
}
