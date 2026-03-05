
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
            // Inject uniforms as variables in p5 instance
            for (const [k, v] of Object.entries(uniforms)) {
                p[k] = v;
            }

            try {
                // We use s_eval to execute the code in the context of the sketch
                // This is a simplified version of what P5Preview.js does
                const setupFunc = new Function('p', 'uniforms', `${transpiled}\nif(typeof setup === 'function') setup();`);
                const drawFunc = new Function('p', 'uniforms', `${transpiled}\nif(typeof draw === 'function') draw();`);

                p.setup = () => {
                    p.createCanvas(this.width, this.height);
                    try { setupFunc(p, uniforms); } catch (e) { logger.error("P5 Setup Error:", e); }
                };

                p.draw = () => {
                    try { drawFunc(p, uniforms); } catch (e) { logger.error("P5 Draw Error:", e); }
                };
            } catch (e) {
                logger.error("P5 Compilation Error:", e);
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
