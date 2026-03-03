# Scromfy Shaders - Mathematical Constants mirroring shaders/lib/const.lib
# Mirror of web/lib_const.js and shaders/lib/const.lib
# Ensure any changes here are mirrored across all versions.

import math

M_EPSILON = 1.0e-10

M_DEG2RAD = math.pi / 180.0
M_RAD2DEG = 180.0 / math.pi

M_PI = math.pi
M_TAU = 2.0 * math.pi

M_PI_INV = 1.0 / math.pi
M_TAU_INV = 1.0 / M_TAU

M_PI_2 = math.pi / 2.0
M_PI_4 = math.pi / 4.0
M_3PI_4 = 3.0 * math.pi / 4.0

M_PHI = (1.0 + math.sqrt(5.0)) / 2.0
M_PHI_INV = 1.0 / M_PHI
M_PHI_SQ = M_PHI * M_PHI
M_PHI_SQRT5 = M_PHI / math.sqrt(5.0)
M_GOLD_ANG = math.pi * (3.0 - math.sqrt(5.0))

M_E = math.e
M_LOG2E = math.log2(math.e)
M_LOG10E = math.log10(math.e)
M_LN2 = math.log(2.0)
M_LN10 = math.log(10.0)

M_SQRT2 = math.sqrt(2.0)
M_SQRT3 = math.sqrt(3.0)
M_SQRT2_INV = 1.0 / M_SQRT2
M_SQRT3_INV = 1.0 / M_SQRT3
M_SQRT5 = math.sqrt(5.0)
