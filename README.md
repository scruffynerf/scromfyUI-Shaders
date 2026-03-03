# scromfyUI-Shaders

> [!IMPORTANT]
> **Dedication**: This project is dedicated to the memory of **Alexander G. Morano** ([Amorano](https://github.com/Amorano)), also known as the author of Jovimetrix and Jovi_GLSL. We aim to preserve and advance the robust shader foundation he built for the ComfyUI community.

Shader nodes for ComfyUI. 

## Features
- **Dynamic GLSL Node Generation**: Highly customizable shader nodes ported and enhanced from Jovi_GLSL.
- **Unified 1:1:1 Library Architecture**: Guaranteed mathematical parity between the **GPU Render**, **Python Backend**, and **WebGL Frontend Preview**.
- **LYGIA Library Integration**: Industry-standard shader functions (noise, SDFs, etc.) bundled and resolved locally.
- **High-Performance Previews**: Real-time WebGL previews directly on-node and ModernGL-accelerated rendering for final output.
- **Interactive Widgets**: Specialized widgets for colors and positions with live feedback.

## Installation
1. Clone this repository into your `ComfyUI/custom_nodes` folder:
   ```bash
   git clone https://github.com/scruffynerf/scromfyUI-Shaders
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Look for nodes under the `Scromfy/Shaders` category in the ComfyUI node menu. 
The repository uses a dynamic scanning system that automatically loads all nodes from the `nodes/` directory.

## Progress & Specs
- [PROGRESS.md](docs/PROGRESS.md) — Current implementation status.
- [NODE_SPECS.md](docs/NODE_SPECS.md) — Detailed technical specifications and directory structure.

## Credits
This project builds upon the incredible work of the following repositories:
- **[Amorano/Jovi_GLSL](https://github.com/Amorano/Jovi_GLSL)** (Primary inspiration and foundation)
- **[patriciogonzalezvivo/comfyui_glslnodes](https://github.com/patriciogonzalezvivo/comfyui_glslnodes)** (Standards and LYGIA integration)
- **[koshimazaki/ComfyUI-Koshi-Nodes](https://github.com/koshimazaki/ComfyUI-Koshi-Nodes)** (Preview designs and orbital controls)
- **[AEmotionStudio/ComfyUI-ShaderNoiseKSampler](https://github.com/AEmotionStudio/ComfyUI-ShaderNoiseKSampler)** (Noise exploration concepts)
- **[peteromallet/ComfyUI_CreativeCode](https://github.com/peteromallet/ComfyUI_CreativeCode)** (Live coding implementation)
- **[AEmotionStudio/ShaderDump](https://github.com/AEmotionStudio/ShaderDump)** (ModernGL rendering techniques)
- **[jberg/butterchurn](https://github.com/jberg/butterchurn)** (Audio visualization inspiration)
- **[lygia.xyz](https://lygia.xyz/)** (Essential shader library by Patricio Gonzalez Vivo)
