
export class AIAssistant {
    constructor() {
        this.apiUrl = localStorage.getItem("scromfy_ai_url") || "http://localhost:11434/v1/chat/completions";
        this.model = localStorage.getItem("scromfy_ai_model") || "llama3";
    }

    async generate(prompt, currentCode, type = "glsl", settings = null) {
        let systemPrompt = settings?.system_prompt || `You are a creative coding expert specializing in ${type.toUpperCase()}.
        If GLSL, follow Shadertoy conventions (mainImage, iTime, iResolution).
        Return ONLY the code block. No explanations.`;

        const fullPrompt = currentCode ?
            `Current code:\n\`\`\`${type}\n${currentCode}\n\`\`\`\n\nTask: ${prompt}` :
            prompt;

        const url = settings?.api_url || this.apiUrl;
        const model = settings?.model || this.model;

        const response = await fetch("/scromfy/ai/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prompt: fullPrompt,
                system: systemPrompt,
                api_url: url,
                model: model
            })
        });

        if (!response.ok) {
            const err = await response.text();
            throw new Error(err);
        }

        const data = await response.json();
        // Strip markdown code blocks if AI returns them
        let code = data.content;
        code = code.replace(/```(?:glsl|javascript|p5\.js|js)?\n?([\s\S]*?)```/gi, '$1').trim();
        return code;
    }

    async getModels() {
        try {
            const resp = await fetch(`/scromfy/ai/models?api_url=${encodeURIComponent(this.apiUrl.replace('/chat/completions', '/models'))}`);
            const data = await resp.json();
            return data.models || [];
        } catch (e) {
            return [];
        }
    }

    saveSettings(url, model) {
        this.apiUrl = url;
        this.model = model;
        localStorage.setItem("scromfy_ai_url", url);
        localStorage.setItem("scromfy_ai_model", model);
    }
}
