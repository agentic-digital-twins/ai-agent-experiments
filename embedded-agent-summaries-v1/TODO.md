TODO: Jim

5. About that Flask “development server” warning

This bit in your logs:

WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

…is coming from Flask inside the piper-http image. It’s totally fine for:

Local dev

An internal Docker-only microservice behind your agent

If/when you ever productize this:

You’d either:

Put a Gunicorn/Uvicorn + Nginx front-end in front of the Piper process, or

Use Piper’s C++/Wyoming server and wrap it yourself.

But that’s well beyond our current “embedded agent baseline + TTS” scope.
