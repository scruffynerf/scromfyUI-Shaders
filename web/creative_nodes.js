
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

        // Add auto-bake interceptor
        const orgQueuePrompt = app.queuePrompt;
        app.queuePrompt = async function () {
            const p5Renders = app.graph._nodes.filter(n => n.type === "CreativeP5Render");
            for (const node of p5Renders) {
                if (node.needsBake && node.needsBake()) {
                    console.log(`[Scromfy] Auto-baking node ${node.id} before queue...`);
                    await node.doBake();
                }
            }
            return orgQueuePrompt.apply(app, arguments);
        };
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
            } else if (nodeData.name === "CreativeUniforms") {
                setupUniformsNode(node, nodeData);
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

function setupUniformsNode(node, nodeData) {
    const codeWidget = node.widgets.find(w => w.name === "shader_code");
    const customUniformWidget = node.widgets.find(w => w.name === "custom_uniforms");

    hideWidget(codeWidget);
    hideWidget(customUniformWidget);

    const root = document.createElement("div");
    root.className = "sc-node";

    const uniformGrid = document.createElement("div");
    uniformGrid.className = "sc-uniform-grid";
    root.appendChild(uniformGrid);

    node.addDOMWidget("creative_uniforms_ui", "UI", root);

    node.updateUniforms = function (code) {
        const defs = parseUniforms(code);
        uniformGrid.innerHTML = "";

        let currentUniforms = {};
        try { currentUniforms = JSON.parse(customUniformWidget.value); } catch (e) { }

        defs.forEach(def => {
            const ctrl = createUniformControl(def, currentUniforms[def.name], (val) => {
                currentUniforms[def.name] = val;
                customUniformWidget.value = JSON.stringify(currentUniforms);
                app.graph.setDirtyCanvas(true, true);
            });
            uniformGrid.appendChild(ctrl);
        });
    };

    let lastCode = "";
    const pollId = setInterval(() => {
        if (!node.graph) return;
        const inputSlot = node.findInputSlot("shader_code");
        if (inputSlot === -1) return;
        const origin = node.getInputNode(inputSlot);
        if (origin) {
            const widget = origin.widgets?.find(w => w.name === "shader_code" || w.name === "p5_code" || w.name === "code");
            const currentCode = widget ? widget.value : "";
            if (currentCode !== lastCode) {
                lastCode = currentCode;
                node.updateUniforms(currentCode);
            }
        }
    }, 500);

    node.onRemoved = () => clearInterval(pollId);
}

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
            let currentCode = codeWidget.value;
            let finalCode = await window.scromfyAI.generate(prompt, currentCode, isP5 ? "js" : "glsl", settings);

            codeWidget.value = finalCode;
            if (editor) editor.setValue(finalCode);
            app.graph.setDirtyCanvas(true, true);

            // Wait a moment for graph to propagate and let polling/manual trigger happen
            setTimeout(async () => {
                // Find any connected render nodes to check for errors
                const renderNodes = findConnectedRenderNodes(node);
                for (const rn of renderNodes) {
                    const result = await rn.updatePreview();
                    if (result && !result.success) {
                        console.log("[Scromfy] AI code failed validation, attempting auto-fix...", result.error);
                        aiBtn.textContent = "Auto-fixing...";
                        const fixPrompt = `The code you just generated failed with the following error:\n\n${result.error}\n\nPlease fix the code to resolve this error while keeping the original functionality: ${prompt}`;
                        const fixedCode = await window.scromfyAI.generate(fixPrompt, finalCode, isP5 ? "js" : "glsl", settings);
                        codeWidget.value = fixedCode;
                        if (editor) editor.setValue(fixedCode);
                        app.graph.setDirtyCanvas(true, true);
                        break;
                    }
                }
                aiBtn.textContent = "Generate Code";
                aiBtn.disabled = false;
                aiQuery.value = "";
            }, 500);

        } catch (e) {
            alert("AI Error: " + e.message);
            aiBtn.textContent = "Generate Code";
            aiBtn.disabled = false;
        }
    };
}

function findConnectedRenderNodes(loaderNode) {
    const renders = [];
    const outputs = loaderNode.outputs;
    if (!outputs) return renders;

    for (const output of outputs) {
        if (!output.links) continue;
        for (const linkId of output.links) {
            const link = app.graph.links[linkId];
            if (!link) continue;
            const targetNode = app.graph.getNodeById(link.target_id);
            if (targetNode && (targetNode.type === "CreativeShaderRender" || targetNode.type === "CreativeP5Render")) {
                renders.push(targetNode);
            }
        }
    }
    return renders;
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

    const toolSection = document.createElement("div");
    toolSection.className = "sc-section";

    const refreshBtn = document.createElement("button");
    refreshBtn.className = "sc-btn";
    refreshBtn.textContent = "Refresh Preview";
    refreshBtn.onclick = () => node.updatePreview();
    toolSection.appendChild(refreshBtn);
    root.appendChild(toolSection);

    node.addDOMWidget("creative_ui", "UI", root);

    if (isP5) {
        node.p5Runner = new P5Runner(previewContainer, 512, 512);

        node.needsBake = function () {
            let u = {};
            const cuv = node.widgets.find(w => w.name === "custom_uniforms");
            try { u = JSON.parse(cuv.value); } catch (e) { }
            return !u || !u._p5_uid;
        };

        node.doBake = async function () {
            const code = node.getConnectedCode();
            if (!code) return;
            const frames = node.widgets.find(w => w.name === "frames")?.value || 1;
            const cacheId = await node.p5Runner.bake(frames);
            let uniforms = {};
            try { uniforms = JSON.parse(customUniformWidget.value); } catch (e) { }
            uniforms._p5_uid = cacheId;
            customUniformWidget.value = JSON.stringify(uniforms);
        };
    } else {
        node.glslRunner = new GLSLRunner(previewContainer, 512, 512);
    }

    node.getConnectedCode = function () {
        const inputName = isP5 ? "p5_code" : "shader_code";
        const slot = this.findInputSlot(inputName);
        if (slot === -1) return "";
        const originNode = this.getInputNode(slot);
        if (originNode) {
            const widget = originNode.widgets?.find(w => w.name === "shader_code" || w.name === "p5_code" || w.name === "code");
            if (widget) return widget.value;
        }
        return "";
    };

    node.getConnectedUniforms = function () {
        // Try to get uniforms from connected CreativeUniforms node
        const slot = this.findInputSlot("uniforms");
        if (slot !== -1) {
            const origin = this.getInputNode(slot);
            if (origin && origin.type === "CreativeUniforms") {
                const widget = origin.widgets?.find(w => w.name === "custom_uniforms");
                if (widget) {
                    try { return JSON.parse(widget.value); } catch (e) { }
                }
            }
        }
        return {};
    };

    node.updatePreview = async function () {
        try {
            const code = this.getConnectedCode();
            if (!code) {
                messageOverlay.style.display = "flex";
                return { success: false, error: "No code" };
            }
            messageOverlay.style.display = "none";

            const u = this.getConnectedUniforms();

            // Mark as needing bake if code changed
            if (isP5 && code !== node._lastBakedCode) {
                let currU = {};
                try { currU = JSON.parse(customUniformWidget.value); } catch (e) { }
                delete currU._p5_uid;
                customUniformWidget.value = JSON.stringify(currU);
                node._lastBakedCode = code;
            }

            if (isP5) {
                if (!node.p5Runner) node.p5Runner = new P5Runner(previewContainer, 512, 512);
                return await node.p5Runner.run(code, u);
            } else {
                if (!node.glslRunner) {
                    previewContainer.querySelectorAll("canvas").forEach(c => c.remove());
                    node.glslRunner = new GLSLRunner(previewContainer, 512, 512);
                }
                return await node.glslRunner.run(code, u);
            }
        } catch (err) {
            return { success: false, error: err.message };
        }
    };

    const pollId = setInterval(() => {
        if (!node.graph) return;
        node.updatePreview();
    }, 500);

    node.updatePreview();
}
