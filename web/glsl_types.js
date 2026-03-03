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
    }

    draw(ctx, node, widgetWidth, widgetY) {
        this.wY = widgetY;
        this.wWidth = widgetWidth;
        this.wHeight = node.size[1] - widgetY;

        ctx.save();
        ctx.translate(0, this.wY);

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

        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    mouse(e, pos, node) {
        if (e.type === 'pointermove' || e.type === 'pointerdown') {
            const x = (pos[0] / this.wWidth - 0.5) * 2.0;
            const y = ((pos[1] - this.wY) / this.wHeight - 0.5) * 2.0;
            this.value = [x, y];
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
        this.size = [200, 40];
    }

    draw(ctx, node, widgetWidth, widgetY) {
        const r = Math.round(this.value[0] * 255);
        const g = Math.round(this.value[1] * 255);
        const b = Math.round(this.value[2] * 255);
        const a = this.value[3];

        ctx.fillStyle = `rgba(${r},${g},${b},${a})`;
        ctx.fillRect(10, widgetY, widgetWidth - 20, 30);
        ctx.strokeStyle = "#fff";
        ctx.strokeRect(10, widgetY, widgetWidth - 20, 30);

        ctx.fillStyle = "#fff";
        ctx.textAlign = "center";
        ctx.fillText(`${this.name}: ${this.serializeValue()}`, widgetWidth / 2, widgetY + 20);
    }

    mouse(e, pos, node) {
        // Simple click to cycle or we can add a real picker later
        if (e.type === 'pointerdown') {
            // Placeholder: for now just rotate color to show it works
            this.value = [Math.random(), Math.random(), Math.random(), 1.0];
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

        this.camera = new Matrix();
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
        let A = this.camera.getMult(vertex);
        const center = this.getCenter();
        return [A.x + center[0], A.y + center[1]];
    }

    draw(ctx, node, widgetWidth, widgetY) {
        this.wY = widgetY;
        this.wWidth = widgetWidth;
        this.wHeight = node.size[1] - widgetY;

        ctx.save();

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
        ctx.fillStyle = this.overPoint ? '#fff' : '#999';
        ctx.beginPath();
        ctx.arc(p[0], p[1], 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    mouse(e, pos, node) {
        if (e.type === 'pointerdown') {
            this.dragOffset = pos;
            let p = this.viewFromCamera(this.value.map(v => v * this.scale));
            let dx = p[0] - pos[0];
            let dy = p[1] - pos[1];
            this.overPoint = Math.sqrt(dx * dx + dy * dy) < 10;
        }
        else if (e.type === 'pointermove') {
            let dx = 0.01 * (pos[0] - this.dragOffset[0]);
            let dy = 0.01 * (pos[1] - this.dragOffset[1]);

            if (this.overPoint) {
                let invM = this.camera.getInv();
                let vel = invM.getMult([dx, dy, 0.0]);
                this.value[0] += vel.x * 2;
                this.value[1] += vel.y * 2;
                this.value[2] += vel.z * 2;
            }
            else {
                this.camera.rotateX(dy);
                this.camera.rotateY(dx);
            }
            this.dragOffset = pos;
        }
        return true;
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
                    minHeight: 200,
                }
            },
            VEC3POS: (node, inputName, inputData) => {
                return {
                    widget: node.addCustomWidget(new Vec3PosWidget(inputName, inputData)),
                    minWidth: 200,
                    minHeight: 200,
                }
            },
            VEC4COLOR: (node, inputName, inputData) => {
                return {
                    widget: node.addCustomWidget(new Vec4ColorWidget(inputName, inputData)),
                    minWidth: 200,
                    minHeight: 40,
                }
            },
            GLSL_STRING: (node, inputName, inputData) => {
                // For now, use a simple multiline string node, we can upgrade to ACE later
                const w = node.addWidget("text", inputName, inputData.default || "", (v) => { }, { multiline: true });
                w.value = inputData.default || "";
                return { widget: w };
            }
        }
    }
});
