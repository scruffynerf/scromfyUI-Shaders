# AI API Keys

To use the AI Assistant with external APIs (like OpenAI or Anthropic), you can store your API keys here.

### Instructions

1. Create a new `.txt` file in this directory.
2. Name the file after the **domain** or **host_port** of the API.
   * Example for OpenAI: `api.openai.com.txt`
   * Example for Anthropic: `api.anthropic.com.txt`
   * Example for a specific local URL: `localhost_11434.txt` (No `http://`, no colons).
3. Paste the API key as the only content in the file.

### Security
* This directory contains a `.gitignore` that ignores all `*.txt` files to prevent accidental commits of your keys.
* The Scromfy backend looks for these files when proxying requests to ensure your keys are never exposed to the frontend.
