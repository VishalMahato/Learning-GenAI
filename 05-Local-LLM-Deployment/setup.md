# Running Open WebUI with Ollama (Qwen-3 0.5B)

This guide explains how to run Ollama and Open WebUI in Docker on Windows, connect them, and use the Qwen-3 0.5B model.

---

## 1) Start the containers

### Ollama
Run these in PowerShell:

```powershell
docker pull ollama/ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Open WebUI

```powershell
docker pull ghcr.io/open-webui/open-webui:main
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

- Ollama API: `http://localhost:11434`
- Open WebUI: `http://localhost:3000`

---

## 2) Connect Open WebUI to Ollama

1. Open `http://localhost:3000` in your browser.
2. Go to: Admin → Settings → Connections → LLM Providers → Ollama.
3. Set Base URL to:

   ```
   http://host.docker.internal:11434
   ```

   On Windows, `host.docker.internal` lets containers reach services on the host.
4. Click Save, then Test / Sync.

---

## 3) Download Qwen-3 0.6B

In Open WebUI:
- Go to Admin → Models (or Models Hub / Add Model).
- Search for `qwen`.
- Select `qwen:0.5b` (Qwen-3 0.5B) and click Download / Pull.

Open WebUI will instruct Ollama to download the model into the shared volume at `/root/.ollama`.

### Alternative: pull via CLI

```powershell
docker exec -it ollama ollama pull qwen:0.5b
```

---

## 4) Use the model in Open WebUI

1. In the chat window, open the model selector and choose `qwen:0.5b`.
2. Try a prompt such as:

   ```
   hello
   ```

You should see a response from Qwen-3 0.5B.

