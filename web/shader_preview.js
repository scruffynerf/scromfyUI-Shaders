import { app } from "/scripts/app.js";

class ShaderPreviewWidget {
    constructor(inputName, node) {
        this.name = inputName;
        this.type = "SHADER_PREVIEW";
        this.node = node;
        this.size = [512, 512];

        // WebGL state
        this.canvas = document.createElement("canvas");
        this.gl = this.canvas.getContext("webgl2") || this.canvas.getContext("webgl");
        this.program = null;
        this.vbo = null;
        this.startTime = Date.now();
        this.lastSource = "";
        this.uniforms = {};

        this.initGL();
    }

    initGL() {
        const gl = this.gl;
        if (!gl) return;

        // Square quad
        const vertices = new Float32Array([
            -1, -1, 1, -1, -1, 1,
            -1, 1, 1, -1, 1, 1
        ]);
        this.vbo = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo);
        gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
    }

    async updateShader(source) {
        const gl = this.gl;
        if (!gl || !source) return;

        // Resolve includes before compiling
        const resolvedSource = await this.resolveIncludes(source);

        // Minimal shadertoy-like wrapper
        const vert = `#version 300 es
            in vec2 pos;
            out vec2 uv;
            void main() {
                gl_Position = vec4(pos, 0.0, 1.0);
                uv = pos * 0.5 + 0.5;
            }
        `;

        let fullSource = resolvedSource;
        const preamble = `
            uniform float iTime;
            uniform float u_time;
            uniform vec3 iResolution;
            uniform vec3 u_resolution;
            uniform vec4 iMouse;
        `;

        if (gl instanceof WebGL2RenderingContext) {
            const versionMatch = resolvedSource.match(/#version\s+\d+\s+es/);
            if (versionMatch) {
                const endPos = versionMatch.index + versionMatch[0].length;
                fullSource = resolvedSource.slice(0, endPos) + "\nprecision highp float;\n" + preamble + resolvedSource.slice(endPos);
            } else {
                fullSource = "#version 300 es\nprecision highp float;\n" + preamble + resolvedSource;
            }
        } else {
            fullSource = preamble + resolvedSource;
        }

        const vs = this.compileShader(gl.VERTEX_SHADER, vert);
        const fs = this.compileShader(gl.FRAGMENT_SHADER, fullSource);

        if (!vs || !fs) return;

        const prog = gl.createProgram();
        gl.attachShader(prog, vs);
        gl.attachShader(prog, fs);
        gl.linkProgram(prog);

        if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
            console.error(gl.getProgramInfoLog(prog));
            return;
        }

        if (this.program) gl.deleteProgram(this.program);
        this.program = prog;
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
            console.error(gl.getShaderInfoLog(s));
            gl.deleteShader(s);
            return null;
        }
        return s;
    }

    draw(ctx, node, widgetWidth, widgetY) {
        // Try to get updated code from the node inputs
        this.updateFromInputs();

        if (!this.gl || !this.program) return;

        const gl = this.gl;
        const w = widgetWidth;
        const h = widgetWidth;

        if (this.canvas.width !== w || this.canvas.height !== h) {
            this.canvas.width = w;
            this.canvas.height = h;
            gl.viewport(0, 0, w, h);
        }

        gl.useProgram(this.program);

        // Standard Uniforms
        const timeLoc = gl.getUniformLocation(this.program, "iTime");
        const utimeLoc = gl.getUniformLocation(this.program, "u_time");
        const time = (Date.now() - this.startTime) / 1000.0;
        if (timeLoc) gl.uniform1f(timeLoc, time);
        if (utimeLoc) gl.uniform1f(utimeLoc, time);

        const resLoc = gl.getUniformLocation(this.program, "iResolution");
        const uresLoc = gl.getUniformLocation(this.program, "u_resolution");
        if (resLoc) gl.uniform3f(resLoc, w, h, 1.0);
        if (uresLoc) gl.uniform3f(uresLoc, w, h, 1.0);

        // Dynamic Uniforms from context
        if (this.uniforms) {
            for (const [name, val] of Object.entries(this.uniforms)) {
                const loc = gl.getUniformLocation(this.program, name);
                if (loc) {
                    if (typeof val === 'number') gl.uniform1f(loc, val);
                    else if (Array.isArray(val)) {
                        if (val.length === 2) gl.uniform2fv(loc, val);
                        else if (val.length === 3) gl.uniform3fv(loc, val);
                        else if (val.length === 4) gl.uniform4fv(loc, val);
                    }
                    else if (typeof val === 'string') {
                        // Handle comma-separated strings from widgets
                        const parts = val.split(',').map(parseFloat);
                        if (parts.length === 1) gl.uniform1f(loc, parts[0]);
                        else if (parts.length === 2) gl.uniform2fv(loc, parts);
                        else if (parts.length === 3) gl.uniform3fv(loc, parts);
                        else if (parts.length === 4) gl.uniform4fv(loc, parts);
                    }
                }
            }
        }

        // Set attributes
        const posLoc = gl.getAttribLocation(this.program, "pos");
        if (posLoc !== -1) {
            gl.enableVertexAttribArray(posLoc);
            gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo);
            gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);
        }

        gl.drawArrays(gl.TRIANGLES, 0, 6);

        // Draw the canvas into the ComfyUI node's 2D context
        ctx.drawImage(this.canvas, 0, widgetY, w, h);
    }

    updateFromInputs() {
        const node = this.node;
        if (!node.inputs) return;

        let code = "";
        let uniforms = {};

        // 1. Get code from the first input
        const codeInput = node.inputs.find(i => i.name === "shader_code");
        if (codeInput && codeInput.link) {
            const link = app.graph.links[codeInput.link];
            if (link) {
                const fromNode = app.graph.getNodeById(link.origin_id);
                if (fromNode.widgets) {
                    const codeWidget = fromNode.widgets.find(w => w.name === "code");
                    if (codeWidget) code = codeWidget.value;
                }
            }
        }

        // 2. Get uniforms from context
        const ctxInput = node.inputs.find(i => i.type === "GLSL_CONTEXT");
        if (ctxInput && ctxInput.link) {
            this.collectUniforms(ctxInput.link, uniforms);
        }

        if (code && code !== this.lastSource) {
            this.updateShader(code);
            this.lastSource = code;
        }
        this.uniforms = uniforms;
    }

    collectUniforms(linkId, target) {
        const link = app.graph.links[linkId];
        if (!link) return;
        const fromNode = app.graph.getNodeById(link.origin_id);

        if (fromNode.widgets) {
            const nameWidget = fromNode.widgets.find(w => w.name === "name");
            const valWidget = fromNode.widgets.find(w => w.name === "value" || w.name === "pos" || w.name === "color" || w.name === "float" || w.name === "int");
            if (nameWidget && valWidget) {
                target[nameWidget.value] = valWidget.value;
            }
        }

        const upstreamCtx = fromNode.inputs?.find(i => i.type === "GLSL_CONTEXT");
        if (upstreamCtx && upstreamCtx.link) {
            this.collectUniforms(upstreamCtx.link, target);
        }
    }
}

app.registerExtension({
    name: "Scromfy.Preview",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ShaderPreview") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                this.previewWidget = new ShaderPreviewWidget("preview", this);
                this.addCustomWidget(this.previewWidget);
                return r;
            };
        }
    }
});
