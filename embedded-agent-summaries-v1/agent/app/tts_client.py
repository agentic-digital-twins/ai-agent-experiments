import logging
import os
import uuid
import wave
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import httpx
import yaml

from .personas import Persona

logger = logging.getLogger(__name__)

# Base URL for the Piper HTTP server (root URL, no path)
PIPER_BASE_URL = os.getenv("TTS_PIPER_URL", "http://piper:5000")

# Root directory where all audio will be stored, e.g. /audio
AUDIO_OUTPUT_DIR = Path(os.getenv("TTS_AUDIO_DIR", "/audio"))

# Path to YAML config that maps persona ids to Piper voice ids
PERSONA_VOICE_CONFIG = Path(
    os.getenv("PERSONA_VOICE_CONFIG", "/app/config/persona_voices.yaml")
)

# Default Piper voice if persona is unmapped
DEFAULT_VOICE = os.getenv("TTS_PIPER_DEFAULT_VOICE", "en_US-kusal-medium")


class TTSClientError(Exception):
    """Raised when TTS synthesis fails."""


def _load_persona_voice_map() -> Dict[str, str]:
    """Load persona->voice mapping from YAML config file, if present."""
    if not PERSONA_VOICE_CONFIG.exists():
        logger.warning(
            "Persona voice config not found at %s; falling back to defaults",
            PERSONA_VOICE_CONFIG,
        )
        return {}

    try:
        with PERSONA_VOICE_CONFIG.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            logger.warning(
                "Persona voice config at %s is not a mapping; ignoring",
                PERSONA_VOICE_CONFIG,
            )
            return {}
        return {str(k): str(v) for k, v in data.items()}
    except Exception as e:
        logger.exception("Failed to load persona voice config: %s", e)
        return {}


# Loaded once at import time
_PERSONA_VOICE_MAP: Dict[str, str] = _load_persona_voice_map()


def _persona_key(persona: Optional[Union[Persona, str]]) -> Optional[str]:
    """Normalize persona identifier to its id string."""
    if persona is None:
        return None
    if isinstance(persona, dict):
        return persona.get("id")
    if isinstance(persona, str):
        return persona
    return None


def resolve_piper_voice(persona: Optional[Union[Persona, str]]) -> str:
    """Resolve which Piper voice id to use for a given persona."""
    pid = _persona_key(persona)
    if pid and pid in _PERSONA_VOICE_MAP:
        return _PERSONA_VOICE_MAP[pid]
    return DEFAULT_VOICE


def _get_output_dir(persona: Optional[Union[Persona, str]]) -> Path:
    """Get the directory where this audio file should be stored.

    Structure:
        <AUDIO_ROOT_DIR>/<YYYY-MM-DD>/<persona-id-or-default>/
    """
    today = datetime.utcnow().strftime("%Y-%m-%d")
    pid = _persona_key(persona) or "default"
    out_dir = AUDIO_OUTPUT_DIR / today / pid
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


async def synthesize_speech(
    text: str,
    persona: Optional[Union[Persona, str]] = None,
) -> Dict[str, str]:
    """Synthesize speech using Piper HTTP server and write it to a WAV file.

    The public contract for the agent remains:
      - status
      - audio_id
      - spoken_text

    Additional fields:
      - audio_path: filesystem path to the generated WAV
      - backend: 'piper'
      - voice: Piper voice id (from persona mapping)
      - sample_rate, channels, frames: basic WAV metadata
    """
    if not text or not text.strip():
        raise TTSClientError("Text for TTS must not be empty")

    out_dir = _get_output_dir(persona)
    voice = resolve_piper_voice(persona)
    audio_id = str(uuid.uuid4())
    audio_path = out_dir / f"{audio_id}.wav"

    logger.info(
        "[TTS] Synthesizing with Piper voice='%s', id=%s, len(text)=%d, dir=%s",
        voice,
        audio_id,
        len(text),
        out_dir,
    )

    # Piper's http_server exposes a single route at '/', and expects:
    #   - POST with raw UTF-8 text in the body
    # It returns raw WAV bytes.
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                PIPER_BASE_URL,
                content=text.encode("utf-8"),
                headers={"Content-Type": "text/plain; charset=utf-8"},
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

        # Extract some basic WAV metadata
        with wave.open(str(audio_path), "rb") as wf:
            channels = wf.getnchannels()
            sample_rate = wf.getframerate()
            frames = wf.getnframes()

    except (httpx.RequestError, OSError, wave.Error) as e:
        logger.exception("Failed to synthesize with Piper")
        raise TTSClientError(str(e)) from e

    return {
        "status": "ok",
        "audio_id": audio_id,
        "spoken_text": text,
        "audio_path": str(audio_path),
        "backend": "piper",
        "voice": voice,
        "channels": channels,
        "sample_rate": sample_rate,
        "frames": frames,
    }
