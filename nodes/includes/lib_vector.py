import math
import numpy as np
from .lib_const import M_DEG2RAD, M_TAU

# Scromfy Shaders - Vector Utilities mirroring web/lib/vector.lib
# Mirror of web/lib_vector.js and web/lib/vector.lib
# Ensure any changes here are mirrored across all versions.

class Vector:
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, (list, tuple)):
            self.x = x[0] if len(x) > 0 else 0
            self.y = x[1] if len(x) > 1 else 0
            self.z = x[2] if len(x) > 2 else 0
        else:
            self.x = x
            self.y = y
            self.z = z

    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def mult(self, s):
        self.x *= s
        self.y *= s
        self.z *= s
        return self

    def getSub(self, v):
        if isinstance(v, (list, tuple)):
            return Vector(self.x - v[0], self.y - (v[1] if len(v) > 1 else 0), self.z - (v[2] if len(v) > 2 else 0))
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def getLength(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def to_list(self):
        return [self.x, self.y, self.z]

class Matrix:
    def __init__(self):
        self.m = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

    def rotateX(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        m = self.m
        m1, m2, m4, m5, m7, m8 = m[1], m[2], m[4], m[5], m[7], m[8]
        m[1] = m1 * c - m2 * s
        m[2] = m1 * s + m2 * c
        m[4] = m4 * c - m5 * s
        m[5] = m4 * s + m5 * c
        m[7] = m7 * c - m8 * s
        m[8] = m7 * s + m8 * c

    def rotateY(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        m = self.m
        m0, m2, m3, m5, m6, m8 = m[0], m[2], m[3], m[5], m[6], m[8]
        m[0] = m0 * c + m2 * s
        m[2] = m2 * c - m0 * s
        m[3] = m3 * c + m5 * s
        m[5] = m5 * c - m3 * s
        m[6] = m6 * c + m8 * s
        m[8] = m8 * c - m6 * s

    def getMult(self, v):
        if isinstance(v, (list, tuple, np.ndarray)):
            vx, vy, vz = v[0], v[1], v[2] if len(v) > 2 else 0.0
        else:
            vx, vy, vz = v.x, v.y, v.z

        return Vector(
            vx * self.m[0] + vy * self.m[1] + vz * self.m[2],
            vx * self.m[3] + vy * self.m[4] + vz * self.m[5],
            vx * self.m[6] + vy * self.m[7] + vz * self.m[8]
        )

    def getInv(self):
        res = Matrix()
        res.m = [
            self.m[0], self.m[3], self.m[6],
            self.m[1], self.m[4], self.m[7],
            self.m[2], self.m[5], self.m[8]
        ]
        return res

def vec_project(a, b):
    a = np.array(a)
    b = np.array(b)
    return (np.dot(a, b) / np.dot(b, b)) * b

def vec_orthogonal2(v):
    v = np.array(v)
    return np.array([-v[1], v[0]])

def vec_orthogonal3(v):
    v = np.array(v)
    if abs(v[0]) > abs(v[1]):
        res = np.array([-v[2], 0.0, v[0]])
    else:
        res = np.array([0.0, v[2], -v[1]])
    return res / np.linalg.norm(res)

def vec_angle_between(a, b):
    a = np.array(a)
    b = np.array(b)
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    return math.acos(max(-1.0, min(1.0, np.dot(a_norm, b_norm))))

def vec_ndot(a, b):
    return a[0]*b[0] - a[1]*b[1]

def vec_rotation_uv(uv, angle_deg):
    uv = np.array(uv)
    cos_a = math.cos(angle_deg * M_DEG2RAD)
    sin_a = math.sin(angle_deg * M_DEG2RAD)
    return np.array([
        uv[0] * cos_a - uv[1] * sin_a,
        uv[0] * sin_a + uv[1] * cos_a
    ])

def vec_rotation_mat2(angle_deg):
    rotate_rad = (angle_deg % 360.0) / 360.0
    cos_a = math.cos(rotate_rad * M_TAU)
    sin_a = math.sin(rotate_rad * M_TAU)
    return np.array([
        [cos_a, -sin_a],
        [sin_a,  cos_a]
    ])

def vec_rotation_xy_mat3(angle_rads):
    c = np.cos(angle_rads)
    s = np.sin(angle_rads)
    return np.array([
        [c[1], 0.0, -s[1]],
        [s[1]*s[0], c[0], c[1]*s[0]],
        [s[1]*c[0], -s[0], c[1]*c[0]]
    ])

def vec_rotate2(v, angle_rad):
    v = np.array(v)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    return np.array([
        v[0] * cos_a - v[1] * sin_a,
        v[0] * sin_a + v[1] * cos_a
    ])

def vec_max(v):
    return np.max(v)
