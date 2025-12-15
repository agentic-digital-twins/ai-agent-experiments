import os
import httpx
from .personas import Persona

TTS_BASE_URL = os.environ.get("TTS_BASE_URL", "http://tts:8000")


async def request_tts(text: str, persona: Persona):
    payload = {
        "text": text,
        "voice_id": persona["ttsStyle"]["voiceId"],
        "speaking_rate": persona["ttsStyle"]["speakingRate"],
        "pitch": persona["ttsStyle"]["pitch"],
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{TTS_BASE_URL}/speak", json=payload)
        resp.raise_for_status()
        return resp.json()
