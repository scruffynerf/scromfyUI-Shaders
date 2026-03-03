# Agents.md - Shaders ComfyUI Node Development

## Core Principles & Rules

### Rule #1: Platform Parity (1:1:1)
**ALL** utility logic must be synchronized across three platforms. Any change to a `.lib` file MUST be mirrored in its Python and JS counterparts.
- **Source of Truth (GLSL)**: `/web/lib/*.lib`
- **Python Backend**: `/nodes/includes/lib_*.py`
- **JavaScript Frontend**: `/web/lib_*.js`

### Rule #2: Never Reinvent the Wheel
**NEVER** create new code when existing ComfyUI infrastructure can be reused. Always:
1. **Check existing nodes first** (ask and look in reference code)
2. **Check ComfyUI core** (ask and look in main comfy-org repo https://github.com/Comfy-Org/ComfyUI)
3. **Ask if unsure** - Don't assume you need to build from scratch, ask before you code.
4. **Extend, don't replace** - Wrap or extend existing functionality

### Rule #2: Follow ComfyUI's Integration Patterns
Study how ComfyUI can natively integrate Shaders:

### Rule #3: Keep It Modular
Build **single-purpose nodes** that can be composed:
- ✅ Good: `ShaderBuilder` outputs STRING
- ❌ Bad: `ShaderAllInOneGenerator` does everything

### Rule #4: Preserve Workflow Flexibility
Users should be able to:
- Mix Shader nodes with standard ComfyUI nodes
- Use existing nodes when possible

---

## Project Focus

### Primary Goal
TBD

### Success Criteria
A user can:
- ✅ TBD

---

## Build Strategy

### Phase 1: TBD
- ✅ TBD

### Phase 2: TBD
- ✅ TBD

### Phase 3: Node Development 
XX nodes implemented across these categories:

TBD:

### Phase 4: Documentation & Examples
- Create example workflows (one per mode)
- Write usage guides for each workflow
- Document parameter mappings (Shaders → ComfyUI)

---

## Technical Architecture

### How Shaders can integrate with ComfyUI

**Key Insight**: 

---

## Node Development Guidelines

### Input/Output Types
Match ComfyUI conventions:
- TBD

### Metadata Formatting
- TBD

---

## What We're NOT Building

TBD

---

## Questions to Ask Before Building

1. **Does a similar node exist?**
   - If yes → Reuse or extend it

2. **Does ComfyUI core provide this?**
   - If yes → Use the core functionality

3. **Can this be done with existing nodes connected together?**
   - If yes → Create a workflow example instead

4. **Is this feature used by >50% of users?**
   - If no → Consider making it optional/extensible

---

## Current Status

### What We Have

### Next Steps

---

## Code Style & Standards

### Follow Existing Patterns
TBD

### Node Template
TBD

### Documentation
Every node should have:
- Clear docstring explaining purpose
- Input parameter descriptions
- Output descriptions
- Example usage in comments

---

## Project Rules

- **Node Location**: Each node must reside in its own file within the `nodes/` directory, following the pattern `name_node.py`.
- **Loading Logic**: Use the existing dynamic loading mechanism in `__init__.py`. **DO NOT** implement the Jovi_GLSL loading system.
- **Utilities & Includes**: 
  - Python core logic: `nodes/includes/shader_manager.py`.
  - Standardized Mirrors: `nodes/includes/lib_*.py`.
- **GLSL Fragment Library**: All `.lib` files must reside in `/web/lib` for cross-platform availability.
- **Web Assets**: All JavaScript files must be placed directly in the `/web` directory (no subdirectories) for ComfyUI compatibility.
- **Documentation**: Maintain 1:1:1 parity tables in all library `README.md` files and keep `walkthrough.md` updated.
