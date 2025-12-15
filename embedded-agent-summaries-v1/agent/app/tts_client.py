import logging
import os
import uuid
from pathlib import Path
from typing import Dict, Optional, Union

import httpx
import yaml

from .personas import Persona

logger = logging.getLogger(__name__)

PIPER_BASE_URL = os.getenv("TTS_PIPER_URL", "http://piper:5000")
AUDIO_OUTPUT_DIR = Path(os.getenv("TTS_AUDIO_DIR", "/audio"))
PERSONA_VOICE_CONFIG = Path(
    os.getenv("PERSONA_VOICE_CONFIG", "/app/config/persona_voices.yaml")
)
DEFAULT_VOICE = os.getenv("TTS_PIPER_DEFAULT_VOICE", "en_US-kusal-medium")


class TTSClientError(Exception):
    pass


def _load_persona_voice_map() -> Dict[str, str]:
    if not PERSONA_VOICE_CONFIG.exists():
        logger.warning(
            "Persona voice config not found at %s; using defaults",
            PERSONA_VOICE_CONFIG,
        )
        return {}
    try:
        with PERSONA_VOICE_CONFIG.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            logger.warning("Persona voice config is not a mapping")
            return {}
        return {str(k): str(v) for k, v in data.items()}
    except Exception as e:
        logger.exception("Failed to load persona voice config: %s", e)
        return {}


_PERSONA_VOICE_MAP: Dict[str, str] = _load_persona_voice_map()


def _persona_key(persona: Optional[Union[Persona, str]]) -> Optional[str]:
    if persona is None:
        return None
    if isinstance(persona, dict):
        return persona.get("id")
    if isinstance(persona, str):
        return persona
    return None


def resolve_piper_voice(persona: Optional[Union[Persona, str]]) -> str:
    pid = _persona_key(persona)
    if pid and pid in _PERSONA_VOICE_MAP:
        return _PERSONA_VOICE_MAP[pid]
    return DEFAULT_VOICE


async def synthesize_speech(
    text: str,
    persona: Optional[Union[Persona, str]] = None,
) -> Dict[str, str]:
    """
    Call Piper HTTP server and write a WAV file.

    Contract stays the same for the agent:
        - status
        - audio_id
        - spoken_text

    And we add:
        - audio_path
        - backend
        - voice
    """
    if not text or not text.strip():
        raise TTSClientError("Text for TTS must not be empty")

    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    voice = resolve_piper_voice(persona)
    audio_id = str(uuid.uuid4())
    audio_path = AUDIO_OUTPUT_DIR / f"{audio_id}.wav"

    logger.info(
        "[TTS] Synthesizing with Piper voice='%s', id=%s, len(text)=%d",
        voice,
        audio_id,
        len(text),
    )

    # IMPORTANT: Piper's http_server expects:
    #   - URL: "/" (root)
    #   - Method: GET with ?text=... OR POST with raw body text
    # It returns raw WAV bytes.

    # We'll use POST with raw text body.
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                PIPER_BASE_URL,  # e.g. "http://piper:5000"
                content=text.encode("utf-8"),
                headers={"Content-Type": "text/plain; charset=utf-8"},
                # NOTE: vanilla http_server.py does NOT support voice selection
                # via query or JSON. The voice/model is fixed by the container.
                # persona→voice is future-proofing for when we switch to a
                # multi-voice wrapper, but right now it's effectively cosmetic.
            )

        if resp.status_code != 200:
            snippet = resp.text[:200]
            logger.error(
                "Piper TTS error: HTTP %s – %s", resp.status_code, snippet
            )
            raise TTSClientError(
                f"Piper TTS HTTP {resp.status_code}: {snippet}"
            )

        wav_bytes = resp.content
        if not wav_bytes:
            raise TTSClientError("Piper returned empty audio")

        with audio_path.open("wb") as f:
            f.write(wav_bytes)

    except (httpx.RequestError, OSError) as e:
        logger.exception("Failed to synthesize with Piper")
        raise TTSClientError(str(e)) from e

    return {
        "status": "ok",
        "audio_id": audio_id,
        "spoken_text": text,
        "audio_path": str(audio_path),
        "backend": "piper",
        "voice": voice,
    }
