
export const logger = {
    debug: (...args) => console.log("[ScromfyCreative]", ...args),
    info: (...args) => console.info("[ScromfyCreative]", ...args),
    warn: (...args) => console.warn("[ScromfyCreative]", ...args),
    error: (...args) => console.error("[ScromfyCreative]", ...args),
};

export function hideWidget(widget) {
    if (!widget) return;
    widget.hidden = true;
    // Don't change type, as it may break serialization/validation for INT types
    widget.computeSize = () => [0, 0];
    if (widget.inputEl) {
        widget.inputEl.style.display = "none";
    }
}

export function detectCodeType(code) {
    if (!code) return "glsl";
    const normalize = code.replace(/\/\/.*$/gm, "").replace(/\/\*[\s\S]*?\*\//g, "").toLowerCase();

    const isP5 = /\bfunction\s+(setup|draw)\b/.test(normalize) ||
        /\bsetup\s*=\s*function\b/.test(normalize) ||
        /\bcreateCanvas\s*\(/.test(normalize) ||
        /\b(background|stroke|fill|ellipse|rect)\s*\(/.test(normalize);

    if (isP5) return "p5";

    const isGLSL = /\bvoid\s+mainimage\s*\(/.test(normalize) ||
        /#version\s+\d+/.test(normalize) ||
        /\buniform\s+(?:float|int|vec|sampler)\b/.test(normalize);

    return isGLSL ? "glsl" : "glsl";
}

export function ensureStyle() {
    const styleId = "scromfy-creative-style";
    if (document.getElementById(styleId)) return;
    const style = document.createElement("style");
    style.id = styleId;
    style.textContent = `
        .sc-node {
            width: 100%; height: 100%; display: flex; flex-direction: column; gap: 6px; padding: 10px;
            background: #111; border-radius: 8px; color: #eee; font-family: 'Inter', sans-serif;
        }
        .sc-section { border: 1px solid #333; border-radius: 6px; background: #1a1a1a; padding: 8px; margin-bottom: 6px; }
        .sc-title { font-size: 11px; font-weight: bold; color: #888; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px; }
        .sc-editor-container { width: 100%; height: 350px; background: #000; border-radius: 4px; overflow: hidden; position: relative; }
        .sc-preview-container { width: 100%; aspect-ratio: 16/9; background: #000; border-radius: 4px; position: relative; overflow: hidden; }
        .sc-preview-canvas { width: 100%; height: 100%; object-fit: contain; }
        .sc-uniform-grid { display: grid; grid-template-columns: 1fr; gap: 8px; }
        .sc-uniform-item { display: flex; flex-direction: column; gap: 4px; padding: 6px; background: #222; border-radius: 4px; border: 1px solid #333; }
        .sc-uniform-label { font-size: 10px; color: #aaa; }
        .sc-uniform-row { display: flex; gap: 4px; }
        .sc-input { background: #000; border: 1px solid #444; color: #fff; border-radius: 3px; padding: 2px 6px; font-size: 12px; height: 24px; }
        .sc-btn { background: #333; border: 1px solid #444; color: #fff; padding: 4px 12px; border-radius: 4px; cursor: pointer; font-size: 11px; transition: 0.2s; }
        .sc-btn:hover { background: #444; border-color: #666; }
        .sc-btn-primary { background: #2a5a8a; border-color: #3b6b9b; }
        .sc-btn-primary:hover { background: #3b6b9b; }
        .sc-error-box { background: #311; color: #f88; padding: 8px; border-radius: 4px; font-size: 11px; white-space: pre-wrap; display: none; margin-top: 8px; border: 1px solid #522; }
    `;
    document.head.appendChild(style);
}
