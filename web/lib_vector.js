// Scromfy Shaders - Vector Utilities mirroring shaders/lib/vector.lib
// Mirror of nodes/includes/lib_vector.py and shaders/lib/vector.lib
// Ensure any changes here are mirrored across all versions.

export class Vector {
    constructor(x, y, z) {
        if (Array.isArray(x)) {
            this.x = x[0] || 0;
            this.y = x[1] || 0;
            this.z = x[2] || 0;
        } else {
            this.x = x || 0;
            this.y = y || 0;
            this.z = z || 0;
        }
    }

    add(v) {
        this.x += v.x;
        this.y += v.y;
        this.z += v.z;
    }

    mult(s) {
        this.x *= s;
        this.y *= s;
        this.z *= s;
    }

    getSub(v) {
        if (Array.isArray(v)) {
            return new Vector(this.x - v[0], this.y - v[1], (v[2] !== undefined) ? this.z - v[2] : 0);
        }
        return new Vector(this.x - v.x, this.y - v.y, this.z - v.z);
    }

    getLength() {
        return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
    }

    to_array() {
        return [this.x, this.y, this.z];
    }
}

export class Matrix {
    constructor() {
        this.m = [1, 0, 0, 0, 1, 0, 0, 0, 1];
    }

    rotateX(angle) {
        const c = Math.cos(angle);
        const s = Math.sin(angle);
        const m = this.m;
        const m1 = m[1], m2 = m[2], m4 = m[4], m5 = m[5], m7 = m[7], m8 = m[8];
        m[1] = m1 * c - m2 * s;
        m[2] = m1 * s + m2 * c;
        m[4] = m4 * c - m5 * s;
        m[5] = m4 * s + m5 * c;
        m[7] = m7 * c - m8 * s;
        m[8] = m7 * s + m8 * c;
    }

    rotateY(angle) {
        const c = Math.cos(angle);
        const s = Math.sin(angle);
        const m = this.m;
        const m0 = m[0], m2 = m[2], m3 = m[3], m5 = m[5], m6 = m[6], m8 = m[8];
        m[0] = m0 * c + m2 * s;
        m[2] = m2 * c - m0 * s;
        m[3] = m3 * c + m5 * s;
        m[5] = m5 * c - m3 * s;
        m[6] = m6 * c + m8 * s;
        m[8] = m8 * c - m6 * s;
    }

    getMult(v) {
        const x = (Array.isArray(v)) ? v[0] : v.x;
        const y = (Array.isArray(v)) ? v[1] : v.y;
        const z = (Array.isArray(v)) ? v[2] : v.z;
        return new Vector(
            x * this.m[0] + y * this.m[1] + z * this.m[2],
            x * this.m[3] + y * this.m[4] + z * this.m[5],
            x * this.m[6] + y * this.m[7] + z * this.m[8]
        );
    }

    getInv() {
        const res = new Matrix();
        res.m = [
            this.m[0], this.m[3], this.m[6],
            this.m[1], this.m[4], this.m[7],
            this.m[2], this.m[5], this.m[8]
        ];
        return res;
    }
}

import { M_DEG2RAD, M_TAU } from "./lib_const.js";

export function vec_project(a, b) {
    const dot = a[0] * b[0] + a[1] * b[1] + (a[2] || 0) * (b[2] || 0);
    const b_sq = b[0] * b[0] + b[1] * b[1] + (b[2] || 0) * (b[2] || 0);
    const s = dot / b_sq;
    return b.map(v => v * s);
}

export function vec_orthogonal2(v) {
    return [-v[1], v[0]];
}

export function vec_orthogonal3(v) {
    let res;
    if (Math.abs(v[0]) > Math.abs(v[1])) {
        res = [-(v[2] || 0), 0.0, v[0]];
    } else {
        res = [0.0, (v[2] || 0), -v[1]];
    }
    const len = Math.sqrt(res[0] * res[0] + res[1] * res[1] + res[2] * res[2]);
    return res.map(v => v / len);
}

export function vec_angle_between(a, b) {
    const dot = a[0] * b[0] + a[1] * b[1] + (a[2] || 0) * (b[2] || 0);
    const aLen = Math.sqrt(a[0] * a[0] + a[1] * a[1] + (a[2] || 0) * (a[2] || 0));
    const bLen = Math.sqrt(b[0] * b[0] + b[1] * b[1] + (b[2] || 0) * (b[2] || 0));
    return Math.acos(Math.max(-1.0, Math.min(1.0, dot / (aLen * bLen))));
}

export function vec_ndot(a, b) {
    return a[0] * b[0] - a[1] * b[1];
}

export function vec_rotation_uv(uv, angle_deg) {
    const cos_a = Math.cos(angle_deg * M_DEG2RAD);
    const sin_a = Math.sin(angle_deg * M_DEG2RAD);
    return [
        uv[0] * cos_a - uv[1] * sin_a,
        uv[0] * sin_a + uv[1] * cos_a
    ];
}

export function vec_rotation_mat2(angle_deg) {
    const rotate_rad = (angle_deg % 360.0) / 360.0;
    const cos_a = Math.cos(rotate_rad * M_TAU);
    const sin_a = Math.sin(rotate_rad * M_TAU);
    return [
        [cos_a, -sin_a],
        [sin_a, cos_a]
    ];
}

export function vec_rotation_xy_mat3(angle_rads) {
    const cx = Math.cos(angle_rads[0]);
    const sx = Math.sin(angle_rads[0]);
    const cy = Math.cos(angle_rads[1]);
    const sy = Math.sin(angle_rads[1]);
    // Note: Python implementation was slightly different, but mat3 in GLSL is column-major
    // To match our specific use case in preview:
    return [
        [cy, 0.0, -sy],
        [sy * sx, cx, cy * sx],
        [sy * cx, -sx, cy * cx]
    ];
}

export function vec_rotate2(v, angle_rad) {
    const cos_a = Math.cos(angle_rad);
    const sin_a = Math.sin(angle_rad);
    return [
        v[0] * cos_a - v[1] * sin_a,
        v[0] * sin_a + v[1] * cos_a
    ];
}

export function vec_max(v) {
    return Math.max(...v);
}
