import os
import httpx
from .personas import Persona

LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://llm:8080")


async def _call_llm(prompt: str, n_predict: int = 256, temperature: float = 0.2) -> str:
    url = f"{LLM_BASE_URL}/completion"
    payload = {
        "prompt": prompt,
        "n_predict": n_predict,
        "temperature": temperature,
        "stop": ["</s>"],
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
    if isinstance(data, dict):
        if "content" in data:
            return data["content"]
        if "choices" in data and data["choices"]:
            return data["choices"][0].get("text", "")
    return str(data)


async def summarize_markdown(markdown_text: str) -> str:
    prompt = f"""
You are a concise technical summarization assistant running on a small embedded device.

Summarize the following markdown document.

Rules:
- Ignore navigation menus, boilerplate, and raw URLs.
- Focus on core meaning, key concepts, and operational implications.
- Return ONLY lines that follow this exact format:
  - Start 3–5 lines with "- " for bullet points.
  - Then one line starting with "Bottom line:" for the final summary.
- Do NOT include any other text before or after the bullets.

Markdown document:
{markdown_text}

Now write the summary using the required format:
"""
    raw = await _call_llm(prompt, n_predict=192, temperature=0.4)

    # Light cleanup: keep only bullet lines and a single Bottom line
    lines = [ln.strip() for ln in raw.splitlines()]
    bullets = [ln for ln in lines if ln.startswith("- ")]
    bottom = None
    for ln in lines:
        if ln.startswith("Bottom line:"):
            bottom = ln
            break

    # Limit bullets to at most 5
    bullets = bullets[:5]

    # If model didn’t follow format at all, fall back to the raw text
    if not bullets and not bottom:
        return raw.strip()

    parts = []
    parts.extend(bullets)
    if bottom:
        parts.append(bottom)
    return "\n".join(parts).strip()



async def persona_speech_text(neutral_summary: str, persona: Persona) -> str:
    system = persona["llmStyle"]["systemPrompt"]
    tone = persona["llmStyle"]["summaryTone"]

    prompt = f"""
{system}

You will be given a neutral summary of a technical or operational document.

Your task:
- Turn it into a spoken report.
- Start with a one-sentence headline.
- Then speak 3–5 short sentences.
- Use natural spoken language (no bullets, no markup).
- Aim for about 20–40 seconds of speech.
- {tone}

Neutral summary:
{neutral_summary}

Now produce the spoken report:
"""
    return await _call_llm(prompt, n_predict=256, temperature=0.7)
