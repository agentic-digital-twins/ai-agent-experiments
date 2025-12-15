import wave
from pathlib import Path

import pytest

from agent.app.tts_client import (
    synthesize_speech,
    TTSClientError,
    resolve_piper_voice,
    DEFAULT_VOICE,
)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_piper_tts_generates_wav(tmp_path, monkeypatch):
    # Use temp dir for audio output and talk to Piper via docker network name
    monkeypatch.setenv("TTS_AUDIO_DIR", str(tmp_path))
    monkeypatch.setenv("TTS_PIPER_URL", "http://piper:5000")

    text = "Hello, this is the captain speaking. Testing Piper TTS."

    result = await synthesize_speech(text=text, persona="calm_engineer")

    assert result["status"] == "ok"
    assert "audio_id" in result
    assert "audio_path" in result

    audio_path = Path(result["audio_path"])
    assert audio_path.exists(), f"WAV file not created: {audio_path}"

    # Basic WAV checks
    with wave.open(str(audio_path), "rb") as wav_file:
        n_channels = wav_file.getnchannels()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()

    assert n_channels >= 1
    assert framerate > 0
    assert n_frames > 0


@pytest.mark.asyncio
async def test_empty_text_raises():
    with pytest.raises(TTSClientError):
        await synthesize_speech(text="", persona="calm_engineer")


def test_persona_voice_mapping_default():
    # If persona is unknown, we should get the default voice
    assert resolve_piper_voice("nonexistent_persona") == DEFAULT_VOICE
    assert resolve_piper_voice(None) == DEFAULT_VOICE
