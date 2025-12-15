import wave
from pathlib import Path

import pytest

from agent.app.tts_client import synthesize_speech, TTSClientError


@pytest.mark.asyncio
@pytest.mark.integration
async def test_piper_tts_generates_wav(tmp_path, monkeypatch):
    # Route audio output to a temp dir, and talk to Piper via localhost
    monkeypatch.setenv("TTS_AUDIO_DIR", str(tmp_path))
    # monkeypatch.setenv("TTS_PIPER_URL", "http://localhost:5000")
    # talk to the *container* via Docker network
    monkeypatch.setenv("TTS_PIPER_URL", "http://piper:5000")

    text = "Hello, this is the captain speaking. Testing Piper TTS."

    result = await synthesize_speech(text=text, persona="calm_engineer")

    assert result["status"] == "ok"
    assert "audio_id" in result
    assert "audio_path" in result

    audio_path = Path(result["audio_path"])
    assert audio_path.exists(), f"WAV file not created: {audio_path}"

    # Basic WAV sanity checks
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


def test_persona_voice_mapping(monkeypatch, tmp_path):
    # Create a temporary persona_voices.yaml
    config_path = tmp_path / "persona_voices.yaml"
    config_path.write_text(
        "calm_engineer: en_US-kathleen-low\n"
        "captain: en_US-ryan-high\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("PERSONA_VOICE_CONFIG", str(config_path))

    # Reload module-level mapping
    from importlib import reload
    import agent.app.tts_client as tts_client

    reload(tts_client)

    assert tts_client.resolve_piper_voice("calm_engineer") == "en_US-kathleen-low"
    assert tts_client.resolve_piper_voice("captain") == "en_US-ryan-high"
    # Unknown persona falls back to default
    assert tts_client.resolve_piper_voice("unknown") == tts_client.DEFAULT_VOICE
