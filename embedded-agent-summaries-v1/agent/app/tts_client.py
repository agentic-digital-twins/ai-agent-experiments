import os
import httpx
from .personas import Persona
import os
import uuid
import pathlib
import logging
from typing import Dict, Optional
import yaml


import requests  # add to your agent Docker image requirements

logger = logging.getLogger(__name__)

PIPER_URL = os.getenv("TTS_PIPER_URL", "http://piper:5000")
DEFAULT_VOICE = os.getenv("TTS_PIPER_DEFAULT_VOICE", "en_US-kathleen-low")

# Simple persona-to-Piper voice mapping
PERSONA_VOICE_MAP: Dict[str, str] = {
    "calm_engineer": "en_US-kathleen-low",
    "excited_host": "en_US-amy-low",
    "captain": "en_US-ryan-high",
    # Add more as you define them
}

def load_persona_voice_map(path: str = "persona_voices.yaml") -> Dict[str, str]:
    p = pathlib.Path(path)
    if not p.exists():
        return {}
    with p.open("r") as f:
        return yaml.safe_load(f) or {}

AUDIO_OUTPUT_DIR = pathlib.Path(os.getenv("TTS_AUDIO_DIR", "audio_out"))
AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def resolve_piper_voice(persona: Optional[str]) -> str:
    if persona and persona in PERSONA_VOICE_MAP:
        return PERSONA_VOICE_MAP[persona]
    return DEFAULT_VOICE

class TTSClientError(Exception):
    pass


def synthesize_speech(
    text: str,
    persona: Optional[str] = None,
) -> Dict[str, str]:
    """
    Synthesize speech using Piper and return a dict matching
    the existing agent TTS response structure.

    Returned structure (example):
    {
        "status": "ok",
        "audio_id": "48412896-aace-4731-9939-1a4ce8f88f52",
        "spoken_text": text,
        "audio_path": "audio_out/48412896-aace-4731-9939-1a4ce8f88f52.wav",
        "backend": "piper",
    }
    """
    if not text or not text.strip():
        raise TTSClientError("Text for TTS must not be empty")

    voice = resolve_piper_voice(persona)
    audio_id = str(uuid.uuid4())
    audio_path = AUDIO_OUTPUT_DIR / f"{audio_id}.wav"

    logger.info(f"[TTS] Synthesizing with Piper voice='{voice}', id={audio_id}")

    try:
        # Adjust payload format to your Piper HTTP wrapper
        payload = {
            "text": text,
            "voice": voice,
            "format": "wav",
        }

        # Some Piper frontends use POST /synthesize, some /
        resp = requests.post(f"{PIPER_URL}/synthesize", json=payload, timeout=30)

        if resp.status_code != 200:
            logger.error(
                "Piper TTS error: %s %s", resp.status_code, resp.text[:200]
            )
            raise TTSClientError(
                f"Piper TTS HTTP {resp.status_code}: {resp.text[:200]}"
            )

        wav_bytes = resp.content
        if not wav_bytes:
            raise TTSClientError("Piper returned empty audio")

        with audio_path.open("wb") as f:
            f.write(wav_bytes)

    except (requests.RequestException, OSError) as e:
        logger.exception("Failed to synthesize with Piper")
        raise TTSClientError(str(e)) from e

    # Keep API surface compatible; add fields but don’t remove old ones
    return {
        "status": "ok",
        "audio_id": audio_id,
        "spoken_text": text,
        "audio_path": str(audio_path),
        "backend": "piper",
        "voice": voice,
    }
