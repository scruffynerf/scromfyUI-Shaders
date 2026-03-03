# Reference Shaders & Tech Analysis

This document summarizes the existing options for integrating Shader technology (GLSL, tensor-based graphics) into ComfyUI.

## 1. ComfyUI Node-Based Solutions

### ComfyUI-Koshi-Nodes
- **Focus**: High-quality post-processing effects (Hologram, Bloom, Glitch), Motion/V2V, and Generators.
- **Tech Stack**: Python, `moderngl` for GPU acceleration, WebGL for browser previews.
- **Pros**: 
    - Professional-grade effects.
    - Excellent live preview integration (no Preview Image node needed).
    - Includes 3D orbital controls for raymarched generators.
- **Cons**: Built-in shaders are mostly fixed; not designed for arbitrary user GLSL input.

### ComfyUI-ShaderNoiseKSampler
- **Focus**: Integrating shader-based noise directly into the diffusion sampling process.
- **Pros**:
    - Innovative use of shaders for "latent space navigation."
    - Extremely well documented with an in-node "Shader Matrix."
- **Cons**: Specialized for sampling/noise, not general-purpose image processing.

### ComfyUI_CreativeCode
- **Focus**: Live coding environment for GLSL and p5.js within ComfyUI.
- **Pros**:
    - "Code2Vid" node allows writing shaders directly in the UI.
    - Automatic UI widget creation (sliders, color pickers) via `@uniform` comments.
    - Real-time preview inside the node.
- **Cons**: Managing complex shader projects inside a node text area can be clunky.

### Jovi_GLSL
- **Focus**: Dynamic compilation of `.frag`/`.vert` files into nodes.
- **Pros**:
    - Scalable: add a file to a folder, get a node.
    - Structured uniform metadata (default, min, max, step) in comments.
    - Huge utility library of GLSL functions. 
- **Cons**: Documentation and setup can be complex.

### comfyui_glslnodes
- **Focus**: Clean, modern GLSL runner with library support.
- **Pros**:
    - Native support for the **LYGIA** shader library (very powerful for VFX).
    - Follows industry standards (GlslViewer/GlslCanvas).
- **Cons**: More focused on modular components (vec2, float, texture nodes) than a single "all-in-one" node.

---

## 2. Standalone & Utility Tools

- **ShaderDump**: A CLI tool that demonstrates how to wrap Shadertoy GLSL code into a Python/ModernGL environment for headless rendering. Great reference for the "backend" logic.
- **Butterchurn**: A WebGL port of Milkdrop. Fascinating for audio-reactive math, but highly JS-dependent.
- **milkdrop-preset-converter**: Useful if we want to bridge legacy mathematical visualizers into the ComfyUI pipeline.

---

## 3. Best Practices & Design Considerations

### Rendering Engine
- **ModernGL** is the de-facto standard for running GLSL in Python. It's fast, modern, and handles the OpenGL context well for headless environments like ComfyUI servers.

### User Interface (The "Wow" Factor)
- **Live Preview**: Essential. Users should see the shader result immediately.
- **Dynamic Widgets**: Parsinguniforms from GLSL comments (as seen in CreativeCode and Jovi_GLSL) is the best way to expose controls without manual node coding.
- **Shader Libraries**: Integrating LYGIA or a similar library provides immediate access to noise, SDFs, and lighting functions that make shaders much more powerful.

### Data Flow
- **Tensor Interoperability**: Nodes must efficiently convert between ComfyUI's torch tensors (B, H, W, C) and ModernGL textures/arrays.
- **Batching**: Support for multi-frame rendering (i.e. generating a batch of latent noise or a video sequence) is a core requirement for ComfyUI.

## 4. Refined Direction & Priorities

### Priority 1: Takeover and Enhancement of Jovi_GLSL
- **Goal**: Prevent bitrot of this robust system. 
- **Action**: Use `Jovi_GLSL` as the primary foundation for the "scromfyUI" node system.
- **Enhancement**: Improve its "Dynamic GLSL" system to be more resilient and compatible with modern ComfyUI standards.

### Priority 2: Native [LYGIA](https://lygia.xyz/) Integration
- **Goal**: Provide "industry standard" shader tools.
- **Action**: Integrate LYGIA library resolving at the node level (as seen in `glslnodes`). This allows users to `#include` professional-grade noise, lighting, and math functions effortlessly.
- **Why**: Authored by Patricio Gonzalez Vivo (Book of Shaders), it ensures the foundation is "done the right way."

### Priority 3: Better "Live Tweaking" UX
- **Goal**: Solve the "re-run vs clunky editor" problem.
- **Action**: 
    - Separate the **Editor** from the **Renderer**.
    - Develop a "Hot Reload" system where editing the `.frag` file (externally or in a dedicated side-panel) immediately updates the in-node preview without requiring a full Workflow Queue.
    - Support "Baking" or "Dumping" sequences (inspired by `butterchurn-video-creator`) for high-quality final exports.

## 5. Comparative Analysis: Jovi_GLSL vs. glslnodes

| Feature | Jovi_GLSL (Amorano) | comfyui_glslnodes (Patricio) | Best Practice for ScromfyUI |
| :--- | :--- | :--- | :--- |
| **Uniform Handling** | **Phase 1: Generic Nodes**: Start with explicit nodes (Float, Vec2, etc.) and manual connections for safety and predictability. | **Manual**: Mostly manual connection or generic nodes; harder to set precise ranges for non-tech users. | **Phase 1: Adopt glslnodes' manual/generic approach. Phase 2: Re-evaluate Jovi-style parsing.** |
| **Library Support** | Simple internal `#include` mechanism for a local folder. | **Industry Standard**: Native integration with **LYGIA**; resolves `#include "lygia/..."` locally or via web. | **Adopt glslnodes' LYGIA integration.** |
| **Passes & Feedback** | Mostly single-pass focused. | **Powerful**: Supports `#ifdef BUFFER_X` and `#ifdef DOUBLE_BUFFER_X` for feedback/fluid loops. | **Adopt glslnodes' Multi-Pass logic.** |
| **Node Architecture** | Dynamic class generation (`type()` magic). | Modular Python files for each feature. | **Adopt the user's "one-file-per-node" rule.** |
| **Rendering Backend** | ModernGL + custom `cozy` wrapper. | ModernGL (clean implementation). | **Use clean ModernGL directly.** |

## 6. Implementation Strategy (The Best of Both)

1.  **Phase 1: Stock Implementation**: 
    - Build generic uniform nodes (Float, Vec2, Vec3, Vec4, Texture) that output a `GLSL_CONTEXT`.
    - Build a "Stock" Shader Runner node that accepts this context.
    - Focus on stable ModernGL rendering and LYGIA inclusion.
2.  **Phase 2: Enhanced Metadata Parsing**: 
    - Once the core is stable, evaluate porting the Jovi-style `// uniform` comment parsing for automatic widget generation.
3.  **Local LYGIA Foundation**: Include the LYGIA library so shaders can use `#include "lygia/..."` without internet access.
4.  **Advanced Buffer System**: Implement the logic to detect `BUFFER_X` defines in the shader code and automatically setup textures/FBOs for multi-pass effects.
5.  **Audio Integration**: Bridge the audio analysis (inspired by Butterchurn/Milkdrop) into a `u_audio` or `u_spectrum` uniform for reactive shaders.
