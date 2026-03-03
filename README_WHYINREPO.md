# Why LYGIA is Bundled in the Repository

We have chosen to bundle a **pruned version** of the [LYGIA Shader Library](https://lygia.xyz/) directly into this repository instead of using a Git submodule.

### Reasoning

1.  **Optimized Footprint**: 
    The full LYGIA library supports many languages (HLSL, WGSL, MSL, etc.) and is quite large (~9MB+). By bundling it, we were able to use the `prune.py` utility to keep **only the GLSL files**, significantly reducing the storage and download size for ComfyUI users.

2.  **Seamless Installation**: 
    Git submodules require users to use specific flags like `--recursive` when cloning. Bundling the files ensures the custom nodes work immediately upon installation without requiring additional git commands or manual downloads.

3.  **Universal Offline Support**:
    - **Backend**: The Python-based `moderngl` renderer can resolve `#include "lygia/..."` directives from the consolidated `web/lygia` directory.
    - **Frontend**: The WebGL-based preview widget can resolve the same includes from the `web/lygia` directory. 
    This provides a consistent, high-performance experience without needing a round-trip to the lygia.xyz servers during shader development.

4.  **Version Consistency**: 
    Bundling ensures that the specific version of LYGIA the nodes were tested with is always present, preventing breaking changes from upstream updates from affecting your workflows unexpectedly.

### Single Source of Truth
To avoid redundancy, LYGIA is stored in a single location that both the backend and frontend can access:
- **Consolidated Location**: `web/lygia`

### How it works:
- **Backend (Python)**: The `ShaderContext` resolver is configured to look inside the `web/lygia` folder on the disk.
- **Frontend (WebGL)**: ComfyUI serves the `web` directory, so the JS widget can `fetch` the files directly from the browser.
