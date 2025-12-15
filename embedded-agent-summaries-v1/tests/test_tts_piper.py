import os
import wave
import pathlib
import pytest

from agent.tts_client import synthesize_speech, AUDIO_OUTPUT_DIR, TTSClientError

@pytest.mark.integration
def test_piper_tts_generates_wav(tmp_path, monkeypatch):
    # Route output to a temp directory for clean test
    monkeypatch.setenv("TTS_AUDIO_DIR", str(tmp_path))

    text = "Hello, this is the captain speaking. Testing Piper TTS."
    result = synthesize_speech(text=text, persona="calm_engineer")

    assert result["status"] == "ok"
    assert "audio_id" in result
    assert "audio_path" in result

    audio_path = pathlib.Path(result["audio_path"])
    assert audio_path.exists(), f"WAV file not created: {audio_path}"

    # Basic WAV validation
    with wave.open(str(audio_path), "rb") as wav_file:
        n_channels = wav_file.getnchannels()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()

    assert n_channels >= 1
    assert framerate > 0
    assert n_frames > 0


def test_empty_text_raises():
    with pytest.raises(TTSClientError):
        synthesize_speech(text="", persona="calm_engineer")



from agent.tts_client import resolve_piper_voice, PERSONA_VOICE_MAP, DEFAULT_VOICE

def test_persona_voice_mapping_known():
    assert resolve_piper_voice("calm_engineer") == PERSONA_VOICE_MAP["calm_engineer"]

def test_persona_voice_mapping_default():
    assert resolve_piper_voice("nonexistent_persona") == DEFAULT_VOICE
    assert resolve_piper_voice(None) == DEFAULT_VOICE
