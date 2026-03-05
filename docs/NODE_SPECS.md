# SHADER Nodes - Technical Specifications

## Implementation Rules
### 1:1:1 Platform Parity
Every utility function added to the project must be implemented in three places to ensure synchronization between the **JS Preview**, **Python Backend**, and **GPU Render**:

| Platform | Path | Extension | Use Case |
| :--- | :--- | :--- | :--- |
| **GLSL** | `web/lib/` | `.lib` | Native Fragment Shaders |
| **Python** | `nodes/includes/` | `lib_*.py` | Backend Rendering & Logic |
| **JavaScript** | `web/` | `lib_*.js` | Frontend Preview & Widgets |

## Project Structure
- `nodes/`: Python node definitions (one per file).
- `nodes/includes/`: Core rendering logic (`shader_manager.py`) and library mirrors.
- `web/`: Frontend JS extensions and library mirrors.
- `web/lib/`: GLSL utility library (`.lib` files).
- `web/lygia/`: Consolidated LYGIA library.
- `graphic_code/frag/`: Library of `.frag` files.

## Auto-Registration
All nodes in `nodes/` are auto-discovered and registered by `__init__.py`.
