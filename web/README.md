# Scromfy Shaders - Web Libraries

This directory contains JavaScript utility libraries used for the WebGL Live Preview.

### ⚠️ Synchronization Rule (1:1:1 Parity)
**All utility logic must be synchronized across three platforms. The GLSL `.lib` file is the source of the name.**

| GLSL (`/web/lib`) | Python (`/nodes/includes`) | JavaScript (`/web`) |
| :--- | :--- | :--- |
| `const.lib` | `lib_const.py` | `lib_const.js` |
| `convert.lib` | `lib_convert.py` | `lib_convert.js` |
| `vector.lib` | `lib_vector.py` | `lib_vector.js` |
| `shading.lib` | `lib_shading.py` | `lib_shading.js` |

This ensures that frontend preview (WebGL), backend rendering (ModernGL), and GPU shaders stay perfectly consistent.
