import os
import json
import asyncio
import aiohttp
from aiohttp import web
from server import PromptServer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# GRAPHIC CODE DIR (contains frag/ and p5/)
GRAPHIC_CODE_DIR = os.path.join(os.path.dirname(BASE_DIR), "graphic_code")
P5_CACHE_DIR = os.path.join(BASE_DIR, "p5_cache")

os.makedirs(GRAPHIC_CODE_DIR, exist_ok=True)
os.makedirs(P5_CACHE_DIR, exist_ok=True)

@PromptServer.instance.routes.get("/scromfy/graphic_code")
async def list_shaders(request):
    shaders = []
    for root, _, files in os.walk(GRAPHIC_CODE_DIR):
        for f in files:
            if f.endswith((".glsl", ".frag", ".js")):
                rel_path = os.path.relpath(os.path.join(root, f), GRAPHIC_CODE_DIR)
                shaders.append({
                    "name": rel_path.replace("\\", "/"),
                    "type": "p5" if f.endswith(".js") else "glsl"
                })
    return web.json_response(shaders)

@PromptServer.instance.routes.get("/scromfy/graphic_code/{name:.+}")
async def get_shader(request):
    name = request.match_info["name"]
    path = os.path.join(GRAPHIC_CODE_DIR, name)
    if not os.path.exists(path):
        return web.Response(status=404, text="Shader not found")
    
    with open(path, "r") as f:
        code = f.read()
    
    return web.json_response({"code": code, "name": name})

@PromptServer.instance.routes.post("/scromfy/graphic_code")
async def save_shader(request):
    data = await request.json()
    name = data.get("name")
    code = data.get("code")
    
    if not name or not code:
        return web.Response(status=400, text="Missing name or code")
    
    # Ensure extension
    if not name.endswith((".glsl", ".frag", ".js")):
        name += ".frag"
        
    path = os.path.join(GRAPHIC_CODE_DIR, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w") as f:
        f.write(code)
        
    return web.json_response({"status": "ok"})

@PromptServer.instance.routes.post("/scromfy/p5/upload")
async def upload_p5_frame(request):
    reader = await request.multipart()
    
    cache_id = None
    filename = None
    file_data = None
    
    while True:
        part = await reader.next()
        if not part: break
        
        if part.name == "cache_id":
            cache_id = await part.text()
        elif part.name == "image":
            filename = part.filename
            file_data = await part.read()
            
    if not cache_id or not file_data:
        return web.Response(status=400, text="Missing cache_id or image data")
        
    target_dir = os.path.join(P5_CACHE_DIR, cache_id)
    os.makedirs(target_dir, exist_ok=True)
    
    with open(os.path.join(target_dir, filename), "wb") as f:
        f.write(file_data)
        
    return web.json_response({"status": "ok"})

# --- AI PROXY ---

@PromptServer.instance.routes.post("/scromfy/ai/generate")
async def ai_generate(request):
    data = await request.json()
    prompt = data.get("prompt")
    system_prompt = data.get("system", "You are a creative coding expert.")
    api_url = data.get("api_url", "http://localhost:11434/v1/chat/completions") # Default to local Ollama
    model = data.get("model", "llama3")
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as resp:
                if resp.status != 200:
                    err_text = await resp.text()
                    return web.Response(status=resp.status, text=f"AI API Error: {err_text}")
                
                result = await resp.json()
                # Handle standard OpenAI response format
                content = result["choices"][0]["message"]["content"]
                return web.json_response({"content": content})
    except Exception as e:
        return web.Response(status=500, text=f"Proxy Error: {str(e)}")

@PromptServer.instance.routes.get("/scromfy/ai/models")
async def list_ai_models(request):
    api_url = request.query.get("api_url", "http://localhost:11434/v1/models")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    return web.json_response({"models": []})
                result = await resp.json()
                # Support OpenAI / Ollama v1 models format
                models = [m["id"] for m in result.get("data", [])]
                return web.json_response({"models": models})
    except:
        return web.json_response({"models": []})

def setup_creative_api():
    # Routes are registered via decorators on PromptServer.instance.routes
    pass
