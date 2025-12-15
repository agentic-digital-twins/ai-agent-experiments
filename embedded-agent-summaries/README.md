✔️ Phi-2 when used in Chat mode with chat-style markdown prompts

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
