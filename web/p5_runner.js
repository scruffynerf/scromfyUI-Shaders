
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

        const sketch = (p) => {
            // Inject uniforms as properties of p
            for (const [k, v] of Object.entries(uniforms)) {
                p[k] = v;
            }

            p.setup = () => {
                p.createCanvas(this.width, this.height);
            };

            try {
                // Use with(p) to allow global-style p5 code in instance mode
                const wrapper = new Function('p', 'uniforms', `
                    with(p) {
                        ${transpiled}
                        if (typeof setup === 'function') {
                            const userSetup = setup;
                            p.setup = () => {
                                p.createCanvas(${this.width}, ${this.height});
                                userSetup();
                            };
                        }
                        if (typeof draw === 'function') {
                            p.draw = draw;
                        }
                    }
                `);
                wrapper(p, uniforms);
            } catch (e) {
                logger.error("P5 Evaluation Error:", e);
            }
        };

        this.instance = new p5(sketch, this.container);
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
