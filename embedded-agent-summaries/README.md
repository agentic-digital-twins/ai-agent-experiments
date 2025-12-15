Actually, I did receive a response in the terminal I posed the curl:

```bash
$ curl -X POST http://localhost:8001/summarize-and-speak   -H "Content-Type: application/json"   -d '{"doc_name":"sample-1.md","persona_id":"calm_engineer"}'
{"status":"ok","persona":"calm_engineer","doc":"sample-1.md","neutral_summary":"\nYou are a summarization assistant running on an embedded device. You take markdown documents and produce clear, neutral summaries.\n\n\n### User\n\nYou will be given a markdown document.\n\nInstructions:\n1. Ignore navigation menus, boilerplate, and raw URLs.\n2. Focus on core meaning, key concepts, and any operational implications.\n3. Output:\n
 - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n   - \n
- \n   - \n   -","spoken_text":"\nI'm an AI assistant designed to generate human-like responses. I can generate text based on the input you provide. However, I do not have a specific programming language or data structure.\n","tts_result":{"status":"ok","audio_id":"32e277d8-44d1-4e10-ae2e-72b23b8c7569","note":"This is a stub; plug in real TTS here."}}
```

I'm going to download your repo and run it, to see if the two operate the same, for a baseline
ChatGPT said:

Great — and excellent diagnosis move.
What you’re seeing in your output is not correct behavior from the LLM.

It means the model did not understand the prompt structure you sent, and instead echoed back the system prompt and produced garbage bullets.

This is classic behavior for:✔️ Phi-2 when used in Chat mode with chat-style markdown prompts

Phi-2 is not an instruction-chat-tuned model.
It does not follow:

### System

### User

### Assistant

It’s a pure base model, so you must directly prompt it in plain text, not in a chat template.

🔥 THIS IS WHY THE OUTPUT LOOKS LIKE:
neutral_summary (incorrect)
You are a summarization assistant...

- -
  - ... (tons of empty bullets)

The model literally interpreted your entire prompt as text to continue, not as instructions.

spoken_text (also incorrect)
I'm an AI assistant designed to generate human-like responses...

That’s a fallback generic text completion from base models when they don’t understand the prompt structure.

You can quick-test the model with a single-line direct prompt

Try:

```bash
curl -X POST http://localhost:8080/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Summarize this in 5 bullets:\nOil levels on main engines and generator\nCoolant levels and visible leaks\nBelt condition and tension\nBilge status and unusual smells\nBattery bank voltage and corrosion\n",
    "n_predict": 200
  }'
```

If you get correct bullets → model is fine.
If you get nonsense → model needs a different template.
