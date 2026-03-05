
export const GLSL_LANGUAGE_DEF = {
    keywords: [
        'void', 'bool', 'int', 'float', 'vec2', 'vec3', 'vec4', 'sampler2D',
        'uniform', 'in', 'out', 'const', 'if', 'else', 'for', 'return'
    ],
    builtins: [
        'sin', 'cos', 'tan', 'atan', 'abs', 'floor', 'ceil', 'fract', 'mod',
        'min', 'max', 'clamp', 'mix', 'step', 'smoothstep', 'length', 'distance',
        'dot', 'cross', 'normalize', 'texture'
    ]
};

let monacoPromise = null;

export function loadMonaco() {
    if (monacoPromise) return monacoPromise;

    monacoPromise = new Promise((resolve) => {
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js";
        script.onload = () => {
            window.require.config({ paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs" } });
            window.require(["vs/editor/editor.main"], () => {
                registerGLSL();
                resolve(window.monaco);
            });
        };
        document.head.appendChild(script);
    });
    return monacoPromise;
}

function registerGLSL() {
    const monaco = window.monaco;
    monaco.languages.register({ id: 'glsl' });
    monaco.languages.setMonarchTokensProvider('glsl', {
        keywords: GLSL_LANGUAGE_DEF.keywords,
        builtins: GLSL_LANGUAGE_DEF.builtins,
        tokenizer: {
            root: [
                [/\/\/.*$/, 'comment'],
                [/\d+/, 'number'],
                [/[a-z_]\w*/, {
                    cases: {
                        '@keywords': 'keyword',
                        '@builtins': 'predefined',
                        '@default': 'identifier'
                    }
                }],
                [/[{}()\[\]]/, '@brackets'],
                [/[<>!=&|+\-*/%]/, 'operator'],
            ]
        }
    });

    monaco.editor.defineTheme('scromfy-dark', {
        base: 'vs-dark',
        inherit: true,
        rules: [
            { token: 'keyword', foreground: '569cd6' },
            { token: 'predefined', foreground: 'dcdcaa' },
            { token: 'identifier', foreground: '9cdcfe' },
            { token: 'comment', foreground: '6a9955', fontStyle: 'italic' },
        ],
        colors: {
            'editor.background': '#1a1a1a',
            'editor.lineHighlightBackground': '#222',
        }
    });
}

export async function createEditor(container, code, language = 'glsl', onChange) {
    const monaco = await loadMonaco();
    const editor = monaco.editor.create(container, {
        value: code,
        language: language,
        theme: 'scromfy-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 13,
        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
        tabSize: 4,
        padding: { top: 10 },
    });

    if (onChange) {
        editor.onDidChangeModelContent(() => {
            onChange(editor.getValue());
        });
    }

    return editor;
}
