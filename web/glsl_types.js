import { app } from "../../scripts/app.js";
import { Vector, Matrix } from "./lib_vector.js";

class Vec2PosWidget {
    constructor(...args) {
        const [inputName, opts] = args;
        this.name = inputName || 'Vec2Pos';
        this.type = 'VEC2POS';
        this.value = [0, 0];
        this.size = [200, 200];
        this.wY = 0;
        this.isDragging = false;
    }

    draw(ctx, node, widgetWidth, widgetY) {
        this.wY = widgetY;
        this.wWidth = widgetWidth;
        this.wHeight = 180; // Fixed sensible height

        ctx.save();
        ctx.translate(0, this.wY);

        // Background
        ctx.fillStyle = '#111';
        ctx.fillRect(0, 0, this.wWidth, this.wHeight);

        // Grid
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 1;
        ctx.beginPath();
        let sections = 10;
        let stepX = this.wWidth / sections;
        let stepY = this.wHeight / sections;
        for (let i = 0; i <= sections; i++) {
            ctx.moveTo(i * stepX, 0);
            ctx.lineTo(i * stepX, this.wHeight);
            ctx.moveTo(0, i * stepY);
            ctx.lineTo(this.wWidth, i * stepY);
        }
        ctx.stroke();

        // Axis
        ctx.strokeStyle = '#666';
        ctx.beginPath();
        ctx.moveTo(this.wWidth / 2, 0);
        ctx.lineTo(this.wWidth / 2, this.wHeight);
        ctx.moveTo(0, this.wHeight / 2);
        ctx.lineTo(this.wWidth, this.wHeight / 2);
        ctx.stroke();

        // Point
        let x = ((this.value[0] + 1.0) * 0.5) * this.wWidth;
        let y = ((this.value[1] + 1.0) * 0.5) * this.wHeight;

        ctx.fillStyle = this.isDragging ? '#0ff' : '#fff';
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.stroke();

        // Text
        ctx.fillStyle = '#aaa';
        ctx.textAlign = 'left';
        ctx.fillText(`${this.name}: [${this.value[0].toFixed(2)}, ${this.value[1].toFixed(2)}]`, 5, this.wHeight - 5);

        ctx.restore();
    }

    computeValue(pos) {
        const x = (pos[0] / this.wWidth - 0.5) * 2.0;
        const y = ((pos[1] - this.wY) / this.wHeight - 0.5) * 2.0;
        return [
            Math.max(-1, Math.min(1, x)),
            Math.max(-1, Math.min(1, y))
        ];
    }

    mouse(e, pos, node) {
        if (e.type === 'pointerdown') {
            this.isDragging = true;
            this.value = this.computeValue(pos);
            return true;
        } else if (e.type === 'pointermove' && this.isDragging) {
            this.value = this.computeValue(pos);
            return true;
        } else if (e.type === 'pointerup') {
            this.isDragging = false;
            return true;
        }
    }

    serializeValue() {
        return this.value.map(v => v.toFixed(3)).join(",");
    }
}

class Vec4ColorWidget {
    constructor(...args) {
        const [inputName, opts] = args;
        this.name = inputName || 'Vec4Color';
        this.type = 'VEC4COLOR';
        this.value = [1.0, 1.0, 1.0, 1.0];
        this.size = [200, 100];
        this.activeIdx = -1;
    }

    draw(ctx, node, widgetWidth, widgetY) {
        this.wY = widgetY;
        this.wWidth = widgetWidth;
        this.wHeight = 100;

        const labels = ['R', 'G', 'B', 'A'];
        const colors = ['#f55', '#5f5', '#55f', '#aaa'];

        ctx.save();
        ctx.translate(0, this.wY);

        // Main preview
        const r = Math.round(this.value[0] * 255);
        const g = Math.round(this.value[1] * 255);
        const b = Math.round(this.value[2] * 255);
        const a = this.value[3];

        ctx.fillStyle = '#333';
        ctx.fillRect(widgetWidth - 40, 0, 30, 30);
        ctx.fillStyle = `rgba(${r},${g},${b},${a})`;
        ctx.fillRect(widgetWidth - 40, 0, 30, 30);
        ctx.strokeStyle = '#fff';
        ctx.strokeRect(widgetWidth - 40, 0, 30, 30);

        for (let i = 0; i < 4; i++) {
            const y = 5 + i * 22;
            const val = this.value[i];
            ctx.fillStyle = '#222';
            ctx.fillRect(10, y, widgetWidth - 60, 15);
            ctx.fillStyle = colors[i];
            ctx.fillRect(10, y, (widgetWidth - 60) * val, 15);
            ctx.fillStyle = '#fff';
            ctx.textAlign = 'left';
            ctx.fillText(labels[i], 0, y + 12);
            ctx.textAlign = 'right';
            ctx.fillText(val.toFixed(2), widgetWidth - 55, y + 12);
        }
        ctx.restore();
    }

    mouse(e, pos, node) {
        if (e.type === 'pointerdown' || (e.type === 'pointermove' && this.activeIdx !== -1)) {
            const relX = pos[0] - 10;
            const relY = pos[1] - this.wY - 5;
            const sliderWidth = (this.wWidth || 200) - 60;

            if (e.type === 'pointerdown') {
                this.activeIdx = Math.floor(relY / 22);
                if (this.activeIdx < 0 || this.activeIdx > 3) {
                    this.activeIdx = -1;
                    return false;
                }
            }

            if (this.activeIdx !== -1) {
                const val = Math.max(0, Math.min(1, relX / sliderWidth));
                this.value[this.activeIdx] = val;
                node.setDirtyCanvas(true, true);
                return true;
            }
        } else if (e.type === 'pointerup') {
            this.activeIdx = -1;
            return true;
        }
    }

    serializeValue() {
        return this.value.map(v => v.toFixed(3)).join(",");
    }
}

class Vec3ColorWidget {
    constructor(...args) {
        const [inputName, opts] = args;
        this.name = inputName || 'Vec3Color';
        this.type = 'VEC3COLOR';
        this.value = [1.0, 1.0, 1.0];
        this.size = [200, 80];
        this.activeIdx = -1;
    }

    draw(ctx, node, widgetWidth, widgetY) {
        this.wY = widgetY;
        this.wWidth = widgetWidth;
        this.wHeight = 80;

        const labels = ['R', 'G', 'B'];
        const colors = ['#f55', '#5f5', '#55f'];

        ctx.save();
        ctx.translate(0, this.wY);

        const r = Math.round(this.value[0] * 255);
        const g = Math.round(this.value[1] * 255);
        const b = Math.round(this.value[2] * 255);

        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(widgetWidth - 40, 0, 30, 30);
        ctx.strokeStyle = '#fff';
        ctx.strokeRect(widgetWidth - 40, 0, 30, 30);

        for (let i = 0; i < 3; i++) {
            const y = 5 + i * 22;
            const val = this.value[i];
            ctx.fillStyle = '#222';
            ctx.fillRect(10, y, widgetWidth - 60, 15);
            ctx.fillStyle = colors[i];
            ctx.fillRect(10, y, (widgetWidth - 60) * val, 15);
            ctx.fillStyle = '#fff';
            ctx.textAlign = 'left';
            ctx.fillText(labels[i], 0, y + 12);
            ctx.textAlign = 'right';
            ctx.fillText(val.toFixed(2), widgetWidth - 55, y + 12);
        }
        ctx.restore();
    }

    mouse(e, pos, node) {
        if (e.type === 'pointerdown' || (e.type === 'pointermove' && this.activeIdx !== -1)) {
            const relX = pos[0] - 10;
            const relY = pos[1] - this.wY - 5;
            const sliderWidth = (this.wWidth || 200) - 60;

            if (e.type === 'pointerdown') {
                this.activeIdx = Math.floor(relY / 22);
                if (this.activeIdx < 0 || this.activeIdx > 2) {
                    this.activeIdx = -1;
                    return false;
                }
            }

            if (this.activeIdx !== -1) {
                const val = Math.max(0, Math.min(1, relX / sliderWidth));
                this.value[this.activeIdx] = val;
                node.setDirtyCanvas(true, true);
                return true;
            }
        } else if (e.type === 'pointerup') {
            this.activeIdx = -1;
            return true;
        }
    }

    serializeValue() {
        return this.value.map(v => v.toFixed(3)).join(",");
    }
}
class Vec3PosWidget {
    constructor(...args) {
        const [inputName, opts] = args;
        this.name = inputName || 'Vec3Pos';
        this.type = 'VEC3POS';
        this.value = [0, 0, 1.0];
        this.size = [200, 200];
        this.scale = 50;
        this.wY = 0;
        this.isDragging = false;

        this.camera = new Matrix();
        this.camera.rotateX(0.5);
        this.camera.rotateY(-0.5);
        this.vector = new Vector(this.value);
        this.shapes = [
            {
                edgeColour: '#555',
                nodes: [[-50, 0.0, 0], [50, 0.0, 0],
                [0.0, -50, 0], [0.0, 50, 0],
                [0.0, 0.0, -50], [0.0, 0.0, 50]],
                edges: [[0, 1], [2, 3], [4, 5]]
            },
            {
                textColour: '#fff',
                nodes: [[68, 0.0, 0], [-68, 0.0, 0],
                [0.0, 68, 0], [0.0, -68, 0],
                [0.0, 0.0, 68], [0.0, 0.0, -68]],
                text: ['x', '-x', 'y', '-y', 'z', '-z']
            }
        ];
    }

    getCenter() {
        return [this.wWidth * 0.5, this.wHeight * 0.5 + this.wY];
    }

    viewFromCamera(vertex) {
        let v = Array.isArray(vertex) ? new Vector(vertex) : vertex;
        let A = this.camera.getMult(v);
        const center = this.getCenter();
        return [A.x + center[0], A.y + center[1]];
    }

    draw(ctx, node, widgetWidth, widgetY) {
        this.wY = widgetY;
        this.wWidth = widgetWidth;
        this.wHeight = 180;

        ctx.save();

        ctx.fillStyle = '#111';
        ctx.fillRect(0, this.wY, this.wWidth, this.wHeight);

        // Draw gizmo shapes
        for (let shape of this.shapes) {
            ctx.strokeStyle = shape.edgeColour;
            if (shape.edges) {
                for (let edge of shape.edges) {
                    let p1 = this.viewFromCamera(shape.nodes[edge[0]]);
                    let p2 = this.viewFromCamera(shape.nodes[edge[1]]);
                    ctx.beginPath();
                    ctx.moveTo(p1[0], p1[1]);
                    ctx.lineTo(p2[0], p2[1]);
                    ctx.stroke();
                }
            }
            if (shape.text) {
                ctx.fillStyle = shape.textColour;
                ctx.font = '10px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                for (let i = 0; i < shape.nodes.length; i++) {
                    let p = this.viewFromCamera(shape.nodes[i]);
                    ctx.fillText(shape.text[i], p[0], p[1]);
                }
            }
        }

        // Draw point
        let p = this.viewFromCamera(this.value.map(v => v * this.scale));
        ctx.fillStyle = this.isDragging ? '#0ff' : '#fff';
        ctx.beginPath();
        ctx.arc(p[0], p[1], 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.stroke();

        ctx.fillStyle = '#aaa';
        ctx.textAlign = 'left';
        ctx.fillText(`${this.name}: [${this.value[0].toFixed(2)}, ${this.value[1].toFixed(2)}, ${this.value[2].toFixed(2)}]`, 5, this.wY + this.wHeight - 5);

        ctx.restore();
    }

    mouse(e, pos, node) {
        if (e.type === 'pointerdown') {
            this.isDragging = true;
            this.dragOffset = pos;
            let p = this.viewFromCamera(this.value.map(v => v * this.scale));
            let dx = p[0] - pos[0];
            let dy = p[1] - pos[1];
            this.overPoint = Math.sqrt(dx * dx + dy * dy) < 15;
            return true;
        }
        else if (e.type === 'pointermove' && this.isDragging) {
            let dx = 0.01 * (pos[0] - this.dragOffset[0]);
            let dy = 0.01 * (pos[1] - this.dragOffset[1]);

            if (this.overPoint) {
                let invM = this.camera.getInv();
                let vel = invM.getMult(new Vector(dx * 10, dy * 10, 0.0));
                this.value[0] += vel.x;
                this.value[1] += vel.y;
                this.value[2] += vel.z;
            }
            else {
                this.camera.rotateX(dy);
                this.camera.rotateY(dx);
            }
            this.dragOffset = [pos[0], pos[1]];
            return true;
        }
        else if (e.type === 'pointerup') {
            this.isDragging = false;
            return true;
        }
        return false;
    }

    serializeValue() {
        return this.value.map(v => v.toFixed(3)).join(",");
    }
}

app.registerExtension({
    name: "Scromfy.Types",
    getCustomWidgets() {
        return {
            VEC2POS: (node, inputName, inputData) => {
                return {
                    widget: node.addCustomWidget(new Vec2PosWidget(inputName, inputData)),
                    minWidth: 200,
                    minHeight: 180,
                }
            },
            VEC3POS: (node, inputName, inputData) => {
                return {
                    widget: node.addCustomWidget(new Vec3PosWidget(inputName, inputData)),
                    minWidth: 200,
                    minHeight: 180,
                }
            },
            VEC3COLOR: (node, inputName, inputData) => {
                return {
                    widget: node.addCustomWidget(new Vec3ColorWidget(inputName, inputData)),
                    minWidth: 200,
                    minHeight: 80,
                }
            },
            VEC4COLOR: (node, inputName, inputData) => {
                return {
                    widget: node.addCustomWidget(new Vec4ColorWidget(inputName, inputData)),
                    minWidth: 200,
                    minHeight: 100,
                }
            },
            GLSL_STRING: (node, inputName, inputData) => {
                const w = node.addWidget("text", inputName, inputData.default || "", (v) => { }, { multiline: true });
                w.value = inputData.default || "";
                return { widget: w };
            }
        }
    },

    nodeCreated(node) {
        // Automatically add size to labels for inputs that might have it
        const originalOnConnectionsChange = node.onConnectionsChange;
        node.onConnectionsChange = function (type, index, connected, link_info) {
            if (originalOnConnectionsChange) originalOnConnectionsChange.apply(this, arguments);

            if (connected && link_info) {
                const input = node.inputs[index];
                if (input && input.type === "IMAGE") {
                    // We can't easily get size here directly from link, 
                    // but we can mark it for the execution check
                }
            }
        };

        node.onExecuted = function (data) {
            if (data && data.resolution) {
                const [w, h] = data.resolution;
                for (let output of this.outputs) {
                    if (output.type === "IMAGE" || output.name === "image") {
                        output.label = `${output.name || "image"} (${w}x${h})`;
                    }
                }
            }
        };
    },

    // Listen for execution completion to update labels with real sizes
    async onAfterGraphExecuted() {
        for (const node of app.graph._nodes) {
            if (node.type && node.type.startsWith("Shader")) {
                // If it's a node we've executed and it has image inputs, 
                // we try to keep labels clean but show info if desired.
                // However, ComfyUI doesn't easily expose the output tensor shapes to the JS graph state
                // without extra backend updates. 

                // For now, let's at least update INT sliders that are named width/height
                if (node.widgets) {
                    for (const w of node.widgets) {
                        if (w.type === "number" || w.type === "slider") {
                            if (w.name === "width" || w.name === "height" || w.name === "intensity" || w.name === "threshold") {
                                // Update label if it's not already showing the value
                                // Actually ComfyUI does this by default if you use the right widget type
                            }
                        }
                    }
                }
            }
        }
    }
});
