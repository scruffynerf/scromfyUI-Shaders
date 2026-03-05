
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
        window.scromfyAI = new AIAssistant();
    },

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (!nodeData.category?.startsWith("Scromfy/Shaders/Creative")) return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);
            const node = this;
            node.serialize_widgets = true;

            if (nodeData.name === "CreativeShaderRender" || nodeData.name === "CreativeP5Render") {
                setupRenderNode(node, nodeData);
            } else if (nodeData.name === "CreativeGLSLLoader" || nodeData.name === "CreativeP5Loader") {
                setupLoaderNode(node, nodeData);
            }
        };

        if (nodeData.name === "CreativeShaderRender" || nodeData.name === "CreativeP5Render") {
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function () {
                onConnectionsChange?.apply(this, arguments);
                if (this.updatePreview) this.updatePreview();
            };
        }
    }
});

function setupLoaderNode(node, nodeData) {
    const isP5 = nodeData.name === "CreativeP5Loader";
    const selectWidget = node.widgets.find(w => w.name === (isP5 ? "select_p5" : "select_shader"));
    const codeWidget = node.widgets.find(w => w.name === (isP5 ? "p5_code" : "shader_code"));

    if (!codeWidget) return;

    hideWidget(codeWidget);

    const root = document.createElement("div");
    root.className = "sc-node";

    const editorContainer = document.createElement("div");
    editorContainer.className = "sc-editor-container";
    root.appendChild(editorContainer);

    const toolSection = document.createElement("div");
    toolSection.className = "sc-section";
    const aiTitle = document.createElement("div");
    aiTitle.className = "sc-title";
    aiTitle.textContent = "AI Assistant";
    toolSection.appendChild(aiTitle);

    const aiQuery = document.createElement("textarea");
    aiQuery.className = "sc-input";
    aiQuery.style.width = "100%";
    aiQuery.style.height = "60px";
    aiQuery.style.marginBottom = "8px";
    aiQuery.placeholder = "Describe changes (e.g., 'Make it reactive to time')...";
    toolSection.appendChild(aiQuery);

    const aiBtn = document.createElement("button");
    aiBtn.className = "sc-btn sc-btn-primary";
    aiBtn.style.width = "100%";
    aiBtn.textContent = "Generate Code";
    toolSection.appendChild(aiBtn);

    root.appendChild(toolSection);
    node.addDOMWidget("creative_loader_ui", "UI", root);

    // AI Settings Resolver
    node.getAISettings = function () {
        const slot = this.findInputSlot("ai_settings");
        if (slot !== -1) {
            const origin = this.getInputNode(slot);
            if (origin && origin.type === "CreativeAIConfig") {
                // CreativeAIConfig outputs settings in its first output
                // But since it's a Python node, we might need to rely on the graph values
                // For now, let's assume we can pull it if it was processed, or use defaults
            }
        }
        return null;
    };

    let editor;
    createEditor(editorContainer, codeWidget.value, isP5 ? "javascript" : "glsl", (val) => {
        codeWidget.value = val;
        app.graph.setDirtyCanvas(true, true);
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

    aiBtn.onclick = async () => {
        const prompt = aiQuery.value;
        if (!prompt) {
            alert("Please enter a prompt for the AI.");
            return;
        }

        // Try to get AI settings from connected node
        let settings = null;
        const aiSlot = node.findInputSlot("ai_settings");
        if (aiSlot !== -1) {
            const aiNode = node.getInputNode(aiSlot);
            if (aiNode) {
                // Pull widgets from the config node
                const urlW = aiNode.widgets?.find(w => w.name === "api_url");
                const modelW = aiNode.widgets?.find(w => w.name === "model");
                if (urlW && modelW) {
                    settings = { api_url: urlW.value, model: modelW.value };
                }
            }
        }

        aiBtn.textContent = "Generating...";
        aiBtn.disabled = true;
        try {
            const newCode = await window.scromfyAI.generate(prompt, codeWidget.value, isP5 ? "js" : "glsl", settings);
            codeWidget.value = newCode;
            if (editor) editor.setValue(newCode);
            aiQuery.value = ""; // Clear query on success
            app.graph.setDirtyCanvas(true, true);
        } catch (e) {
            alert("AI Error: " + e.message);
        }
        aiBtn.textContent = "Generate Code";
        aiBtn.disabled = false;
    };
}

function setupRenderNode(node, nodeData) {
    const isP5 = nodeData.name === "CreativeP5Render";
    const customUniformWidget = node.widgets.find(w => w.name === "custom_uniforms");

    node.widgets.forEach(hideWidget);

    const root = document.createElement("div");
    root.className = "sc-node";

    // Preview area with message overlay
    const previewContainer = document.createElement("div");
    previewContainer.className = "sc-preview-container";

    const messageOverlay = document.createElement("div");
    messageOverlay.style.cssText = "position: absolute; top:0; left:0; width:100%; height:100%; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.7); color: #888; font-style: italic; z-index: 10; padding: 20px; text-align: center; pointer-events: none;";
    messageOverlay.textContent = "Please connect a Loader...";
    previewContainer.appendChild(messageOverlay);
    root.appendChild(previewContainer);

    const uniformGrid = document.createElement("div");
    uniformGrid.className = "sc-uniform-grid";
    const uniformSection = document.createElement("div");
    uniformSection.className = "sc-section";
    const uniformTitle = document.createElement("div");
    uniformTitle.className = "sc-title";
    uniformTitle.textContent = "Dynamic Uniforms";
    uniformSection.appendChild(uniformTitle);
    uniformSection.appendChild(uniformGrid);
    root.appendChild(uniformSection);

    const toolSection = document.createElement("div");
    toolSection.className = "sc-section";
    if (isP5) {
        const bakeBtn = document.createElement("button");
        bakeBtn.className = "sc-btn";
        bakeBtn.textContent = "Bake Animation";
        toolSection.appendChild(bakeBtn);

        bakeBtn.onclick = async () => {
            const code = node.getConnectedCode();
            if (!code) {
                alert("Please connect a P5 Loader first.");
                return;
            }
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

        node.p5Runner = new P5Runner(previewContainer, 512, 512);
    } else {
        node.glslRunner = new GLSLRunner(previewContainer, 512, 512);
    }

    const refreshBtn = document.createElement("button");
    refreshBtn.className = "sc-btn";
    refreshBtn.style.marginLeft = "8px";
    refreshBtn.textContent = "Refresh Preview";
    refreshBtn.onclick = () => node.updatePreview();
    toolSection.appendChild(refreshBtn);
    root.appendChild(toolSection);

    node.addDOMWidget("creative_ui", "UI", root);

    node.getConnectedCode = function () {
        const inputName = isP5 ? "p5_code" : "shader_code";
        const slot = this.findInputSlot(inputName);
        if (slot === -1) {
            // console.debug(`[Scromfy] Slot ${inputName} not found on node`);
            return "";
        }

        const originNode = this.getInputNode(slot);
        if (originNode) {
            // Find the code widget by name
            const widget = originNode.widgets?.find(w => w.name === "shader_code" || w.name === "p5_code" || w.name === "code");
            if (widget) {
                return widget.value;
            } else {
                // Secondary check: if it's a simple string primitive, it might have a 'value' property or 'widgets[0]'
                const fallbackWidget = originNode.widgets?.[0];
                if (fallbackWidget && (fallbackWidget.name === "value" || fallbackWidget.type === "text" || fallbackWidget.type === "customtext")) {
                    return fallbackWidget.value;
                }
            }
        }
        return "";
    };

    node.updatePreview = function () {
        const code = this.getConnectedCode();
        // console.debug(`[Scromfy] updatePreview triggered for ${nodeData.name}, code length:`, code?.length);

        if (!code) {
            const isConnected = this.inputs?.some(i => i.link !== null);
            messageOverlay.textContent = isConnected ? "Connection detected but no code found in source node." : "Please connect a Loader...";
            messageOverlay.style.display = "flex";
            console.log(`[Scromfy] ${nodeData.name}: No code found, showing overlay.`);
            return;
        }

        console.log(`[Scromfy] ${nodeData.name}: Code found (len: ${code.length}), updating...`);
        messageOverlay.style.display = "none";
        this.updateUniforms(code);

        let u = {};
        try { u = JSON.parse(customUniformWidget.value); } catch (e) { }

        if (isP5) {
            if (!node.p5Runner) {
                node.p5Runner = new P5Runner(previewContainer, 512, 512);
            }
            node.p5Runner.run(code, u);
        } else {
            if (!node.glslRunner) {
                // Remove any existing canvases before creating a new runner to avoid stacking
                previewContainer.querySelectorAll("canvas").forEach(c => c.remove());
                node.glslRunner = new GLSLRunner(previewContainer, 512, 512);
            }
            node.glslRunner.run(code, u);
        }
    };

    node.updateUniforms = function (code) {
        const defs = parseUniforms(code);
        uniformGrid.innerHTML = "";

        let currentUniforms = {};
        try { currentUniforms = JSON.parse(customUniformWidget.value); } catch (e) { }

        defs.forEach(def => {
            const ctrl = createUniformControl(def, currentUniforms[def.name], (val) => {
                currentUniforms[def.name] = val;
                customUniformWidget.value = JSON.stringify(currentUniforms);
                this.updatePreview();
            });
            uniformGrid.appendChild(ctrl);
        });
    };

    let lastCode = "";
    const pollId = setInterval(() => {
        if (!node.graph) return; // Keep interval alive but wait for graph

        const currentCode = node.getConnectedCode();
        if (currentCode !== lastCode) {
            console.log(`[Scromfy] Poll detected code change for node ${node.id} (${nodeData.name})`);
            lastCode = currentCode;
            node.updatePreview();
        }
    }, 500); // 500ms is enough and safer

    const onRemoved = node.onRemoved;
    node.onRemoved = function () {
        onRemoved?.apply(this, arguments);
        clearInterval(pollId);
    };

    node.updatePreview();
}
