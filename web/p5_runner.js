
import { logger } from "./creative_utils.js";

export function transpileP5(code) {
    let js = code;

    // Convert Processing style to JS if detected
    // void setup() -> function setup()
    js = js.replace(/void\s+setup\s*\(\s*\)/g, 'function setup()');
    js = js.replace(/void\s+draw\s*\(\s*\)/g, 'function draw()');

    // float x = 1.0; -> let x = 1.0;
    js = js.replace(/\b(float|int|boolean|string)\s+(\w+)\s*=/g, 'let $2 =');

    return js;
}

export class P5Runner {
    constructor(container, width, height) {
        this.container = container;
        this.width = width;
        this.height = height;
        this.instance = null;
        this.canvas = null;
    }

    async run(code, uniforms = {}) {
        if (this.instance) {
            this.instance.remove();
        }

        const transpiled = transpileP5(code);

        // Setup the global scope for the sketch to access uniforms
        window._scromfyUniforms = uniforms;

        let compileError = null;

        const sketch = (p) => {
            // Inject uniforms as properties of p
            for (const [k, v] of Object.entries(uniforms)) {
                p[k] = v;
            }

            p.setup = () => {
                const canvas = p.createCanvas(this.width, this.height);
                canvas.attribute('class', 'sc-preview-canvas');
                // Ensure the canvas is at the bottom of the container, behind the overlay
                canvas.parent(this.container);
            };

            try {
                // Use with(p) to allow global-style p5 code in instance mode
                const wrapper = new Function('p', 'uniforms', `
                    with(p) {
                        try {
                            ${transpiled}
                            if (typeof setup === 'function') {
                                const userSetup = setup;
                                p.setup = () => {
                                    const canvas = p.createCanvas(${this.width}, ${this.height});
                                    canvas.attribute('class', 'sc-preview-canvas');
                                    canvas.parent(p.canvas_parent);
                                    userSetup();
                                };
                            }
                            if (typeof draw === 'function') {
                                p.draw = draw;
                            }
                        } catch (innerError) {
                            p.scromfyError = innerError.message;
                            throw innerError;
                        }
                    }
                `);
                p.canvas_parent = this.container;
                wrapper(p, uniforms);
            } catch (e) {
                logger.error("P5 Evaluation Error:", e);
                compileError = e.message;
            }
        };

        try {
            this.instance = new p5(sketch, this.container);
            if (compileError) return { success: false, error: compileError };
            return { success: true };
        } catch (e) {
            return { success: false, error: e.message };
        }
    }

    async bake(frameCount, onProgress) {
        if (!this.instance) return;

        const cacheId = `p5_${Date.now()}`;
        this.instance.noLoop();

        for (let i = 0; i < frameCount; i++) {
            this.instance.redraw();
            // Capture frame
            const canvas = this.container.querySelector('canvas');
            const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));

            // Upload
            const formData = new FormData();
            formData.append('cache_id', cacheId);
            formData.append('image', blob, `frame_${i.toString().padStart(4, '0')}.png`);

            await fetch('/scromfy/p5/upload', { method: 'POST', body: formData });

            if (onProgress) onProgress(i / frameCount);
        }

        this.instance.loop();
        return cacheId;
    }
}
