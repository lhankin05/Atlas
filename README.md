# Atlas

Chief of staff for VR training work in Unity. Keeps you on track through the pipeline
(Brief, Design, Build, Test, Review, Push), logs your day, checks in, and runs a weekly reflection.

## Run it

Needs Python. On Windows, double-click `start-atlas.bat`, or run:

    python server.py

Then open http://localhost:8000/atlas.html. Stop with Ctrl+C.

Your tasks, log, reflections, chat and API key are saved in `atlas-data.json` next to the server.
That file is ignored by git, so it never gets pushed. Close and reopen as often as you like.

## Claude API

Add your Anthropic API key on the "Chat with Atlas" page. It is used for chat, check-in questions,
the weekly summary and the next-week plan. If "Share my tasks and today's log" is ticked, that
context is sent to the API with each request.

Opening `atlas.html` directly (no server) also works, but data is then kept only in that browser.
