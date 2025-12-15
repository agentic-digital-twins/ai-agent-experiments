# Embedded Agent Summaries (Phi-2 GGUF + llama.cpp + Docker)

Minimal learning project that shows how to:

1. Run a small SLM (Phi-2 Q4_K_M) locally via `llama.cpp` in Docker.
2. Expose an `agent` service (FastAPI) that:
   - reads markdown docs
   - summarizes them with the LLM
   - converts the neutral summary into persona-style spoken text
3. Call a `tts` service stub that you can later swap for real TTS.

## Quick start

```bash
git clone <this-repo>
cd embedded-agent-summaries-v1

# 1) Download the Phi-2 GGUF model (once)
./scripts/get-model.sh

# 2) Build and run all services
docker compose build
docker compose up
```

In another terminal, test the pipeline:

```bash
# List personas
curl http://localhost:8001/personas

# Summarize and "speak" sample-1.md as calm_engineer
curl -X POST http://localhost:8001/summarize-and-speak   -H "Content-Type: application/json"   -d '{"doc_name":"sample-1.md","persona_id":"calm_engineer"}' | jq
```

You should see:

- `embedded-llm` container loading the Phi-2 model and answering completion requests.
- `embedded-agent` returning `neutral_summary` and persona-shaped `spoken_text`.
- `embedded-tts` logging the text it would turn into audio.

## Model

We use **Phi-2 Q4_K_M (GGUF)**:

- Downloaded from Hugging Face via the script `scripts/get-model.sh`.
- Stored under `./models/phi-2-q4_K_M.gguf`.
- Mounted into the `llm` container and loaded by `llama.cpp`.

You can edit `scripts/get-model.sh` and `docker-compose.yml` to swap to another GGUF
model later (e.g. Phi-3 Mini, Qwen2, TinyLlama, etc.).

## Services

- `llm` – `llama.cpp` HTTP server over GGUF model
- `agent` – FastAPI app, persona + markdown summarization
- `tts` – FastAPI stub, logs text + persona voice settings

This is intentionally bare-bones to be a clean starting point
for embedded / RPi-style local agents with TTS.
