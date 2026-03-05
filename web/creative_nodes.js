
import { app } from "/scripts/app.js";
import {
    logger,
    hideWidget,
    detectCodeType,
    ensureStyle
} from "./creative_utils.js";
import { parseUniforms, createUniformControl } from "./uniform_parser.js";
import { createEditor } from "./monaco_setup.js";
import { AIAssistant } from "./ai_assistant.js";
import { P5Runner } from "./p5_runner.js";
import { GLSLRunner } from "./glsl_runner.js";

app.registerExtension({
    name: "Scromfy.CreativeNodes",
    async setup() {
        ensureStyle();
        // Setup AI Assistant
        window.scromfyAI = new AIAssistant();
    },

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (!nodeData.category?.startsWith("Scromfy/Shaders/Creative")) return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);
            const node = this;

            // Common setup for all creative nodes
            node.serialize_widgets = true;

            if (nodeData.name === "CreativeShaderRender" || nodeData.name === "CreativeP5Render") {
                setupRenderNode(node, nodeData);
            } else if (nodeData.name === "CreativeGLSLLoader" || nodeData.name === "CreativeP5Loader") {
                setupLoaderNode(node, nodeData);
            }
        };
    }
});

function setupLoaderNode(node, nodeData) {
    const isP5 = nodeData.name === "CreativeP5Loader";
    const selectWidget = node.widgets.find(w => w.name === (isP5 ? "select_p5" : "select_shader"));
    const codeWidget = node.widgets.find(w => w.name === (isP5 ? "p5_code" : "shader_code"));

    if (!codeWidget) return;

    // Hide the multiline text widget, we'll use Monaco
    hideWidget(codeWidget);

    const root = document.createElement("div");
    root.className = "sc-node";

    const editorContainer = document.createElement("div");
    editorContainer.className = "sc-editor-container";
    root.appendChild(editorContainer);

    node.addDOMWidget("creative_loader_ui", "UI", root);

    let editor;
    createEditor(editorContainer, codeWidget.value, isP5 ? "javascript" : "glsl", (val) => {
        codeWidget.value = val;
    }).then(ed => editor = ed);

    if (selectWidget) {
        selectWidget.callback = async (value) => {
            if (!value || value === "None") return;
            try {
                const res = await fetch(`/scromfy/graphic_code/${value}`);
                const data = await res.json();
                if (data.code) {
                    codeWidget.value = data.code;
                    if (editor) editor.setValue(data.code);
                    app.graph.setDirtyCanvas(true, true);
                }
            } catch (err) {
                logger.error("Failed to load:", err);
            }
        };
    }
}

function setupRenderNode(node, nodeData) {
    const isP5 = nodeData.name === "CreativeP5Render";
    const codeWidget = node.widgets.find(w => w.name === (isP5 ? "p5_code" : "shader_code"));
    const customUniformWidget = node.widgets.find(w => w.name === "custom_uniforms");

    // Hide standard widgets to use custom UI
    node.widgets.forEach(hideWidget);

    const root = document.createElement("div");
    root.className = "sc-node";

    // 1. Preview Area
    const previewContainer = document.createElement("div");
    previewContainer.className = "sc-preview-container";
    root.appendChild(previewContainer);

    // 2. Editor Area
    const editorContainer = document.createElement("div");
    editorContainer.className = "sc-editor-container";
    root.appendChild(editorContainer);

    // 3. Uniforms Area
    const uniformSection = document.createElement("div");
    uniformSection.className = "sc-section";
    const uniformTitle = document.createElement("div");
    uniformTitle.className = "sc-title";
    uniformTitle.textContent = "Dynamic Uniforms";
    const uniformGrid = document.createElement("div");
    uniformGrid.className = "sc-uniform-grid";
    uniformSection.appendChild(uniformTitle);
    uniformSection.appendChild(uniformGrid);
    root.appendChild(uniformSection);

    // 4. AI & Tools Area
    const toolSection = document.createElement("div");
    toolSection.className = "sc-section";
    const aiBtn = document.createElement("button");
    aiBtn.className = "sc-btn sc-btn-primary";
    aiBtn.textContent = "Ask AI Assistant";
    toolSection.appendChild(aiBtn);

    if (isP5) {
        const bakeBtn = document.createElement("button");
        bakeBtn.className = "sc-btn";
        bakeBtn.style.marginLeft = "8px";
        bakeBtn.textContent = "Bake Animation";
        toolSection.appendChild(bakeBtn);

        node.p5Runner = new P5Runner(previewContainer, 512, 512);

        bakeBtn.onclick = async () => {
            const frames = node.widgets.find(w => w.name === "frames")?.value || 1;
            bakeBtn.textContent = "Baking...";
            const cacheId = await node.p5Runner.bake(frames, (p) => {
                bakeBtn.textContent = `Baking ${Math.round(p * 100)}%`;
            });

            let uniforms = {};
            try { uniforms = JSON.parse(customUniformWidget.value); } catch (e) { }
            uniforms._p5_uid = cacheId;
            customUniformWidget.value = JSON.stringify(uniforms);
            bakeBtn.textContent = "Bake Animation";
        };
    } else {
        node.glslRunner = new GLSLRunner(previewContainer, 512, 512);
    }

    root.appendChild(toolSection);
    node.addDOMWidget("creative_ui", "UI", root);

    // Initialize Monaco
    let editor;
    createEditor(editorContainer, codeWidget.value, isP5 ? "javascript" : "glsl", (val) => {
        codeWidget.value = val;
        updateUniforms(val);
        let u = {};
        try { u = JSON.parse(customUniformWidget.value); } catch (e) { }
        if (isP5) {
            node.p5Runner.run(val, u);
        } else {
            node.glslRunner.run(val, u);
        }
    }).then(ed => editor = ed);

    // Uniform syncing
    function updateUniforms(code) {
        const defs = parseUniforms(code);
        uniformGrid.innerHTML = "";

        let currentUniforms = {};
        try { currentUniforms = JSON.parse(customUniformWidget.value); } catch (e) { }

        defs.forEach(def => {
            const ctrl = createUniformControl(def, currentUniforms[def.name], (val) => {
                currentUniforms[def.name] = val;
                customUniformWidget.value = JSON.stringify(currentUniforms);
                if (editor) {
                    const code = editor.getValue();
                    if (isP5) node.p5Runner.run(code, currentUniforms);
                    else node.glslRunner.run(code, currentUniforms);
                }
            });
            uniformGrid.appendChild(ctrl);
        });
    }

    aiBtn.onclick = async () => {
        const prompt = window.prompt("What should I generate/fix?");
        if (!prompt) return;
        aiBtn.textContent = "Generating...";
        try {
            const newCode = await window.scromfyAI.generate(prompt, codeWidget.value, isP5 ? "js" : "glsl");
            codeWidget.value = newCode;
            if (editor) editor.setValue(newCode);
            updateUniforms(newCode);
        } catch (e) {
            alert("AI Error: " + e.message);
        }
        aiBtn.textContent = "Ask AI Assistant";
    };

    updateUniforms(codeWidget.value);

    // Initial preview run
    setTimeout(() => {
        let u = {};
        try { u = JSON.parse(customUniformWidget.value); } catch (e) { }
        if (isP5) {
            if (node.p5Runner) node.p5Runner.run(codeWidget.value, u);
        } else {
            if (node.glslRunner) node.glslRunner.run(codeWidget.value, u);
        }
    }, 100);
}
