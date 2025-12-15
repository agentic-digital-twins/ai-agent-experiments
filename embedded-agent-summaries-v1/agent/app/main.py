from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from .personas import get_persona_ids, get_persona
from .markdown_loader import load_markdown
from .llm_client import summarize_markdown, persona_speech_text
from .tts_client import request_tts

app = FastAPI(title="Embedded Agent Summaries")

DOCS_DIR = os.environ.get("DOCS_DIR", "/docs")


class SummarizeRequest(BaseModel):
    doc_name: str
    persona_id: str


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
    tts_result = await request_tts(spoken_text, persona)

    return {
        "status": "ok",
        "persona": req.persona_id,
        "doc": req.doc_name,
        "neutral_summary": neutral_summary,
        "spoken_text": spoken_text,
        "tts_result": tts_result,
    }
