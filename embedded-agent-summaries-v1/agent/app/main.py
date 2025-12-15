from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os
from pathlib import Path

from .personas import get_persona_ids, get_persona
from .markdown_loader import load_markdown
from .llm_client import summarize_markdown, persona_speech_text
from .tts_client import synthesize_speech, TTSClientError, AUDIO_OUTPUT_DIR

app = FastAPI(title="Embedded Agent Summaries")

DOCS_DIR = os.environ.get("DOCS_DIR", "/docs")


class SummarizeRequest(BaseModel):
    doc_name: str
    persona_id: str

class TTSRequest(BaseModel):
    text: str
    persona_id: str | None = None

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/personas")
async def personas():
    return {"personas": get_persona_ids()}


@app.post("/summarize-and-speak")
async def summarize_and_speak(req: SummarizeRequest):
    persona = get_persona(req.persona_id)
    if not persona:
        raise HTTPException(status_code=400, detail="Unknown persona_id")

    try:
        md = load_markdown(DOCS_DIR, req.doc_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    neutral_summary = await summarize_markdown(md)
    spoken_text = await persona_speech_text(neutral_summary, persona)
    tts_result = await synthesize_speech(spoken_text, persona)

    return {
        "status": "ok",
        "persona": req.persona_id,
        "doc": req.doc_name,
        "neutral_summary": neutral_summary,
        "spoken_text": spoken_text,
        "tts_result": tts_result,
    }

@app.post("/tts")
async def tts(req: TTSRequest):
    """
    Debug endpoint: synthesize speech directly from text + persona_id.
    """
    persona = None
    if req.persona_id:
        persona = get_persona(req.persona_id)
        if persona is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown persona_id '{req.persona_id}'",
            )

    try:
        tts_result = await synthesize_speech(req.text, persona)
    except TTSClientError as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {e}")

    return {
        "status": "ok",
        "persona": req.persona_id,
        "spoken_text": req.text,
        "tts_result": tts_result,
    }

@app.get("/audio/list")
async def list_audio():
    """
    List all synthesized audio files, newest first.
    """
    items = []
    if not AUDIO_OUTPUT_DIR.exists():
        return {"items": []}

    for path in AUDIO_OUTPUT_DIR.rglob("*.wav"):
        rel = path.relative_to(AUDIO_OUTPUT_DIR)
        parts = rel.parts  # e.g. ['2025-12-15', 'calm_engineer', '<uuid>.wav']
        date_str = None
        persona_id = None
        filename = parts[-1]

        if len(parts) >= 3:
            date_str = parts[0]
            persona_id = parts[1]

        audio_id = Path(filename).stem
        stat = path.stat()
        items.append(
            {
                "audio_id": audio_id,
                "persona_id": persona_id,
                "date": date_str,
                "path": str(rel),
                "size_bytes": stat.st_size,
                "mtime": stat.st_mtime,
            }
        )

    # Newest first
    items.sort(key=lambda x: x["mtime"], reverse=True)
    return {"items": items}

@app.get("/audio/{audio_id}")
async def get_audio_file(audio_id: str):
    """
    Return a WAV file by audio_id. We search the hierarchy under AUDIO_OUTPUT_DIR.
    """
    if not AUDIO_OUTPUT_DIR.exists():
        raise HTTPException(status_code=404, detail="No audio directory")

    matches = list(AUDIO_OUTPUT_DIR.rglob(f"{audio_id}.wav"))
    if not matches:
        raise HTTPException(status_code=404, detail=f"Audio {audio_id} not found")

    return FileResponse(matches[0], media_type="audio/wav")


@app.get("/audio", response_class=HTMLResponse)
async def audio_browser():
    """
    Minimal HTML audio browser for quick manual testing.
    """
    if not AUDIO_OUTPUT_DIR.exists():
        return "<h1>No audio files yet</h1>"

    rows = []
    for path in AUDIO_OUTPUT_DIR.rglob("*.wav"):
        rel = path.relative_to(AUDIO_OUTPUT_DIR)
        parts = rel.parts
        date_str = ""
        persona_id = ""
        filename = parts[-1]
        if len(parts) >= 3:
            date_str = parts[0]
            persona_id = parts[1]
        audio_id = Path(filename).stem

        row = f"""
        <tr>
          <td>{date_str}</td>
          <td>{persona_id}</td>
          <td>{audio_id}</td>
          <td><audio controls src="/audio/{audio_id}"></audio></td>
        </tr>
        """
        rows.append(row)

    rows_html = "\\n".join(rows)
    html = f"""
    <html>
      <head>
        <title>Embedded Agent – Audio Browser</title>
        <style>
          body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #020617; color: #e5e7eb; padding: 2rem; }}
          table {{ border-collapse: collapse; width: 100%; max-width: 1200px; }}
          th, td {{ border-bottom: 1px solid #1f2937; padding: 0.5rem 0.75rem; text-align: left; }}
          th {{ background: #111827; position: sticky; top: 0; }}
          tr:hover {{ background: #0f172a; }}
          audio {{ width: 220px; }}
          h1 {{ margin-bottom: 1rem; }}
        </style>
      </head>
      <body>
        <h1>Embedded Agent – Audio Browser</h1>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Persona</th>
              <th>Audio ID</th>
              <th>Playback</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </body>
    </html>
    """
    return html
