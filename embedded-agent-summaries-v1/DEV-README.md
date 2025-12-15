The integration test assumes piper is running at localhost:5000 (because you’ll run it via docker compose up).

It writes audio into a tmp_path so tests don’t pollute ./audio.

To run tests from the repo root of this project:

cd ai-agent-experiments/embedded-agent-summaries-v1

# Start services (llm + piper + agent)

docker compose up -d --build

# Run tests on host (ensure pytest is installed in your dev env)

pytest tests/test_tts_piper.py -m integration -vv

# Run tests inside agent container (optional)

If you prefer to run tests inside the agent container, you can docker compose exec agent pip install pytest once and then run pytest from there.

5️⃣ Manual end-to-end verification

Once everything’s wired:

Bring the stack up:

cd ai-agent-experiments/embedded-agent-summaries-v1
docker compose up -d --build

Sanity-check Piper directly (from host):

This depends on the exact Piper HTTP image you use, but roughly:

curl -X POST http://localhost:5000/synthesize \
 -H "Content-Type: application/json" \
 -d '{"text": "Piper TTS is now online.", "voice": "en_US-kathleen-low", "format": "wav"}' \
 --output piper_test.wav

You should get a playable piper_test.wav.

Hit the agent summary endpoint (your existing flow):

Assuming your FastAPI app is on http://localhost:8001 and you have docs/sample-1.md:

curl -X POST http://localhost:8001/summarize \
 -H "Content-Type: application/json" \
 -d '{
"doc_name": "sample-1.md",
"persona_id": "calm_engineer"
}'

You should get back JSON like:

{
"status": "ok",
"persona": "calm_engineer",
"doc": "sample-1.md",
"neutral_summary": "...",
"spoken_text": "...",
"tts_result": {
"status": "ok",
"audio_id": "48412896-aace-4731-9939-1a4ce8f88f52",
"spoken_text": "...",
"audio_path": "/audio/48412896-aace-4731-9939-1a4ce8f88f52.wav",
"backend": "piper",
"voice": "en_US-kathleen-low"
}
}

Grab the WAV from the host:

It will be under:

ls audio/

# should see <audio_id>.wav

Play it and confirm you’re hearing the persona’s spoken report.

#2️⃣ Re-run docker compose
docker compose pull # optional, but nice to ensure latest images
docker compose up -d --build
Then check logs for Piper:

bash
Copy code
docker compose logs -f piper

Piper Testing

From the upstream piper.http_server code:
GitHub

The server exposes only one route: /

Accepted methods: GET, POST

For POST:

It expects the raw request body to be the text (UTF-8), not JSON

For GET:

It expects a query param ?text=...

Response:

Raw WAV bytes

So these two calls are valid:

# Option A: GET with ?text=

curl "http://localhost:5000/?text=Hello+from+Piper" --output piper_test_get.wav

# Option B: POST with raw body

curl -X POST "http://localhost:5000/" \
 --data "Hello from Piper via POST" \
 --output piper_test_post.wav

# Option C: Will return a 500

curl http://localhost:5000/ || echo "Got something (even 404) from piper-http"

Your earlier curl http://localhost:5000/ had no text, so the server raised ValueError("No text provided") and returned 500. That’s why you saw the HTML 500 page.
