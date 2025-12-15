from typing import Dict, List, Optional, TypedDict


class LlmStyle(TypedDict):
    systemPrompt: str
    summaryTone: str


class TtsStyle(TypedDict):
    voiceId: str
    speakingRate: float
    pitch: float


class Persona(TypedDict):
    id: str
    name: str
    llmStyle: LlmStyle
    ttsStyle: TtsStyle


_PERSONAS: Dict[str, Persona] = {
    "calm_engineer": {
        "id": "calm_engineer",
        "name": "Calm Engineer",
        "llmStyle": {
            "systemPrompt": (
                "You are a calm, technically precise engineer on a small power vessel. "
                "You summarize information clearly for operators and avoid hype."
            ),
            "summaryTone": "Be concise; highlight risks and actions.",
        },
        "ttsStyle": {
            "voiceId": "en_US-male-low",
            "speakingRate": 0.9,
            "pitch": -1.0,
        },
    },
    "brisk_captain": {
        "id": "brisk_captain",
        "name": "Brisk Captain",
        "llmStyle": {
            "systemPrompt": (
                "You are the captain of a vessel. You are direct, confident, and brief. "
                "You focus on decisions and next steps."
            ),
            "summaryTone": "Be punchy, emphasize priorities.",
        },
        "ttsStyle": {
            "voiceId": "en_US-male-mid",
            "speakingRate": 1.05,
            "pitch": 0.0,
        },
    },
}


def get_persona_ids() -> List[str]:
    return list(_PERSONAS.keys())


def get_persona(pid: str) -> Optional[Persona]:
    return _PERSONAS.get(pid)
