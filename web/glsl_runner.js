
import { logger } from "./creative_utils.js";

export class GLSLRunner {
    constructor(container, width, height) {
        this.container = container;
        this.width = width;
        this.height = height;

        this.canvas = document.createElement("canvas");
        this.canvas.width = width;
        this.canvas.height = height;
        this.canvas.className = "sc-preview-canvas";
        this.container.appendChild(this.canvas);

        this.gl = this.canvas.getContext("webgl2") || this.canvas.getContext("webgl");
        this.program = null;
        this.vbo = null;
        this.startTime = Date.now();
        this.lastSource = "";

        this.initGL();
        // Start animation loop
        this.render = this.render.bind(this);
        requestAnimationFrame(this.render);
    }

    initGL() {
        const gl = this.gl;
        if (!gl) {
            logger.error("WebGL not supported");
            return;
        }

        const vertices = new Float32Array([
            -1, -1, 1, -1, -1, 1,
            -1, 1, 1, -1, 1, 1
        ]);
        this.vbo = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo);
        gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
    }

    async run(code, uniforms = {}) {
        if (!code) return;
        if (code === this.lastSource && JSON.stringify(uniforms) === this.lastUniforms) return;

        this.uniforms = uniforms;

        if (code !== this.lastSource) {
            await this.updateShader(code);
            this.lastSource = code;
        }
        this.lastUniforms = JSON.stringify(uniforms);
    }

    async updateShader(source) {
        const gl = this.gl;
        if (!gl) return;

        console.debug("[Scromfy] updateShader starting, length:", source.length);
        const resolvedSource = await this.resolveIncludes(source);
        console.debug("[Scromfy] Includes resolved, final length:", resolvedSource.length);

        const vert = `#version 300 es
            in vec2 pos;
            out vec2 uv;
            void main() {
                gl_Position = vec4(pos, 0.0, 1.0);
                uv = pos * 0.5 + 0.5;
            }
        `;

        const preamble = `
            uniform float iTime;
            uniform float u_time;
            uniform vec3 iResolution;
            uniform vec3 u_resolution;
            uniform vec4 iMouse;
        `;

        let fullSource = resolvedSource;
        const isWebGL2 = gl instanceof WebGL2RenderingContext;

        if (isWebGL2) {
            if (!fullSource.includes("#version")) {
                fullSource = "#version 300 es\nprecision highp float;\n" + preamble + fullSource;
            } else {
                // If version is present, we need to inject preamble after it
                const versionMatch = fullSource.match(/#version\s+\d+\s+es/);
                if (versionMatch) {
                    const end = versionMatch.index + versionMatch[0].length;
                    fullSource = fullSource.substring(0, end) + "\nprecision highp float;\n" + preamble + fullSource.substring(end);
                }
            }

            // Shadertoy compatibility
            if (fullSource.includes("void mainImage") && !fullSource.includes("void main()")) {
                console.log("[Scromfy] Wrapping mainImage into main()");
                fullSource += "\nout vec4 fragColor;\nvoid main() { mainImage(fragColor, gl_FragCoord.xy); }";
            }
        } else {
            // WebGL 1
            if (!fullSource.includes("precision")) {
                fullSource = "precision highp float;\n" + preamble + fullSource;
            }
        }

        console.log("[Scromfy] Compiling shaders...");
        const vs = this.compileShader(gl.VERTEX_SHADER, vert);
        const fs = this.compileShader(gl.FRAGMENT_SHADER, fullSource);

        if (!vs || !fs) {
            console.error("[Scromfy] Shader compilation failed");
            return;
        }

        const prog = gl.createProgram();
        gl.attachShader(prog, vs);
        gl.attachShader(prog, fs);
        gl.linkProgram(prog);

        if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
            console.error("[Scromfy] Shader Link Error:", gl.getProgramInfoLog(prog));
            return;
        }

        if (this.program) gl.deleteProgram(this.program);
        this.program = prog;
        console.log("[Scromfy] Shader program updated and active");
    }

    async resolveIncludes(source, depth = 0) {
        if (depth > 10) return source; // Prevent circular includes

        const includeRegex = /#include\s+["<]?([^"\s>]+)[">]?/g;
        let match;
        let resolved = source;
        const matches = [];

        while ((match = includeRegex.exec(source)) !== null) {
            matches.push({ full: match[0], path: match[1] });
        }

        for (const m of matches) {
            try {
                let fetchPath = m.path;
                if (fetchPath.startsWith("lygia/")) {
                    fetchPath = "./lygia/" + fetchPath.substring(6);
                } else if (fetchPath.startsWith("lib/")) {
                    fetchPath = "./lib/" + fetchPath.substring(4);
                } else if (fetchPath.startsWith(".lib/")) {
                    fetchPath = "./lib/" + fetchPath.substring(5);
                } else {
                    continue;
                }

                const response = await fetch(fetchPath);
                if (response.ok) {
                    const content = await response.text();
                    const nested = await this.resolveIncludes(content, depth + 1);
                    resolved = resolved.replace(m.full, nested);
                }
            } catch (e) {
                console.warn("Failed to resolve include:", m.path, e);
            }
        }
        return resolved;
    }

    compileShader(type, src) {
        const gl = this.gl;
        const s = gl.createShader(type);
        gl.shaderSource(s, src);
        gl.compileShader(s);
        if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
            const err = gl.getShaderInfoLog(s);
            console.error("[Scromfy] Shader Compile Error:", err);
            // logger.error("Shader Compile Error:", err); // Keep original logger if desired
            gl.deleteShader(s);
            return null;
        }
        return s;
    }

    render() {
        if (!this.gl || !this.program) {
            requestAnimationFrame(this.render);
            return;
        }

        const gl = this.gl;
        gl.viewport(0, 0, this.canvas.width, this.canvas.height);
        gl.clearColor(0, 0, 0, 1);
        gl.clear(gl.COLOR_BUFFER_BIT);

        gl.useProgram(this.program);

        const time = (Date.now() - this.startTime) / 1000.0;
        const timeLoc = gl.getUniformLocation(this.program, "iTime") || gl.getUniformLocation(this.program, "u_time");
        if (timeLoc) gl.uniform1f(timeLoc, time);

        const resLoc = gl.getUniformLocation(this.program, "iResolution") || gl.getUniformLocation(this.program, "u_resolution");
        if (resLoc) {
            try {
                gl.uniform3f(resLoc, this.width, this.height, 1.0);
            } catch (e) {
                gl.uniform2f(resLoc, this.width, this.height);
            }
        }

        // Custom Uniforms
        if (this.uniforms) {
            for (const [name, val] of Object.entries(this.uniforms)) {
                if (name.startsWith("_")) continue;
                const loc = gl.getUniformLocation(this.program, name);
                if (loc) {
                    if (typeof val === 'number') gl.uniform1f(loc, val);
                    else if (Array.isArray(val)) {
                        if (val.length === 2) gl.uniform2fv(loc, val);
                        else if (val.length === 3) gl.uniform3fv(loc, val);
                        else if (val.length === 4) gl.uniform4fv(loc, val);
                    }
                }
            }
        }

        const posLoc = gl.getAttribLocation(this.program, "pos");
        if (posLoc !== -1) {
            gl.enableVertexAttribArray(posLoc);
            gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo);
            gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);
        }

        gl.drawArrays(gl.TRIANGLES, 0, 6);
    }
}
