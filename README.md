# Atlas

Chief of staff for VR training work in Unity. Keeps you on track through the pipeline
(Brief, Design, Build, Test, Review, Push), logs your day, checks in, and runs a weekly reflection.

## Run it

Needs Python. On Windows, double-click `start-atlas.bat`, or run:

    python server.py

Then open http://localhost:8000/atlas.html. Stop with Ctrl+C.

Your tasks, log, reflections, chat and settings are saved in `atlas-data.json` next to the server
when using the local server, or in this browser's local storage when opening the HTML directly.
The JSON file is ignored by git, but it is plaintext on your computer; keep the file private.

## Claude API

Add your Anthropic API key on the "Chat with Atlas" page. The key is held in memory for the
current page session and is not saved with app data. Re-enter it after reloading the page.

Your explicit chat messages are sent to the Claude API. When "Share my work context with Atlas"
is enabled, Atlas may also send your open tasks, today's log, and latest weekly reflection answers
to help answer questions, create check-in questions, and prepare weekly plans and summaries.
When sharing is off, those features use generic prompts instead of your task, log, or reflection
content. Your local data remains saved either way.

Opening `atlas.html` directly (no server) also works, but data is then kept only in that browser.
