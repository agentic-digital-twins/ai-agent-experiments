from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tts-stub")

app = FastAPI(title="Embedded TTS Stub")


class SpeakRequest(BaseModel):
    text: str
    voice_id: str
    speaking_rate: float = 1.0
    pitch: float = 0.0


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/speak")
async def speak(req: SpeakRequest):
    audio_id = str(uuid.uuid4())
    logger.info(
        f"[TTS STUB] id={audio_id} voice={req.voice_id} "
        f"rate={req.speaking_rate} pitch={req.pitch} text={req.text[:120]!r}..."
    )
    return {
        "status": "ok",
        "audio_id": audio_id,
        "note": "This is a stub; plug in real TTS here.",
    }
