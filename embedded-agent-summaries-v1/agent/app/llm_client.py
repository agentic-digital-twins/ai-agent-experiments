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
    system = (
        "You are a summarization assistant running on an embedded device. "
        "You take markdown documents and produce clear, neutral summaries."
    )
    user = f"""
You will be given a markdown document.

Instructions:
1. Ignore navigation menus, boilerplate, and raw URLs.
2. Focus on core meaning, key concepts, and any operational implications.
3. Output:
   - 3–5 bullet-style lines (use '-' at start)
   - Then a single 'Bottom line:' sentence.

Markdown:
\"\"\"{markdown_text}\"\"\"
"""
    prompt = f"### System\n{system}\n\n### User\n{user}\n\n### Assistant\n"
    return await _call_llm(prompt, n_predict=256, temperature=0.1)


async def persona_speech_text(neutral_summary: str, persona: Persona) -> str:
    system = persona["llmStyle"]["systemPrompt"]
    tone = persona["llmStyle"]["summaryTone"]

    user = f"""
You are preparing a spoken report based on this neutral summary:
\"\"\"{neutral_summary}\"\"\"
Constraints:
- Start with a brief headline in one sentence.
- Then speak 3–5 short sentences.
- Use natural spoken language, not bullet points.
- The total length should be about 20–40 seconds when read aloud.
- {tone}
Return plain text only, no markdown.
"""
    prompt = f"### System\n{system}\n\n### User\n{user}\n\n### Assistant\n"
    return await _call_llm(prompt, n_predict=256, temperature=0.7)
