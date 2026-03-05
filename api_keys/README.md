# AI API Keys

To use the AI Assistant with external APIs (like OpenAI or Anthropic), you can store your API keys here.

### Instructions

1. Create a new `.txt` file in this directory.
2. Name the file after the **domain** or the **full URL** of the API (replace slashes with underscores or just use the domain).
   * Example for OpenAI: `api.openai.com.txt`
   * Example for Anthropic: `api.anthropic.com.txt`
   * Example for a specific local URL: `http:__localhost:11434.txt`
3. Paste the API key as the only content in the file.

### Security
* This directory contains a `.gitignore` that ignores all `*.txt` files to prevent accidental commits of your keys.
* The Scromfy backend looks for these files when proxying requests to ensure your keys are never exposed to the frontend.
