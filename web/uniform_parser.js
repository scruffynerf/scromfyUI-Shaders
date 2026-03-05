
export function parseUniforms(code) {
    const uniforms = new Map();

    // 1. Parse @uniform float name = 1.0;
    const creativePattern = /@uniform\s+(float|int|bool|vec2|vec3|vec4|)\s*([A-Za-z_]\w*)(?:\s*=\s*([^;\n]+))?/gi;
    let match;
    while ((match = creativePattern.exec(code)) !== null) {
        let [, type, name, rawDefault] = match;
        if (!type) type = "float";
        uniforms.set(name, {
            name, type,
            default: rawDefault ? rawDefault.trim() : null,
            source: 'creative'
        });
    }

    // 2. Parse Jovi style: uniform float speed; // 1.0; 0.0; 2.0; 0.01 | Description
    const joviPattern = /uniform\s+(float|int|bool|vec2|vec3|vec4)\s+([A-Za-z_]\w*)\s*;\s*\/\/\s*([^|]+)/gi;
    while ((match = joviPattern.exec(code)) !== null) {
        const [, type, name, metaStr] = match;
        const parts = metaStr.split(';').map(p => p.trim());

        // If we already have it from @uniform, just update meta
        const existing = uniforms.get(name) || { name, type, source: 'jovi' };

        existing.default = parts[0] || existing.default;
        existing.min = parts[1] || null;
        existing.max = parts[2] || null;
        existing.step = parts[3] || null;

        uniforms.set(name, existing);
    }

    return Array.from(uniforms.values());
}

export function createUniformControl(def, currentValue, onChange) {
    const container = document.createElement("div");
    container.className = "sc-uniform-item";

    const label = document.createElement("div");
    label.className = "sc-uniform-label";
    label.textContent = def.name;
    container.appendChild(label);

    const row = document.createElement("div");
    row.className = "sc-uniform-row";
    container.appendChild(row);

    const inputs = [];
    const type = def.type || "float";

    const update = () => {
        let val;
        if (type === "bool") {
            val = inputs[0].checked;
        } else if (type === "float" || type === "int") {
            val = parseFloat(inputs[0].value) || 0;
        } else if (type.startsWith("vec")) {
            val = inputs.map(i => parseFloat(i.value) || 0);
        }
        onChange(val);
    };

    if (type === "bool") {
        const input = document.createElement("input");
        input.type = "checkbox";
        input.checked = !!currentValue;
        input.onchange = update;
        row.appendChild(input);
        inputs.push(input);
    } else {
        const count = type === "vec4" ? 4 : type === "vec3" ? 3 : type === "vec2" ? 2 : 1;
        for (let i = 0; i < count; i++) {
            const input = document.createElement("input");
            input.className = "sc-input";
            input.type = "number";
            input.step = def.step || (type === "int" ? "1" : "0.01");
            if (def.min !== null) input.min = def.min;
            if (def.max !== null) input.max = def.max;

            const startVal = Array.isArray(currentValue) ? currentValue[i] : currentValue;
            input.value = startVal !== undefined ? startVal : (def.default || 0);

            input.oninput = update;
            row.appendChild(input);
            inputs.push(input);
        }
    }

    return container;
}
