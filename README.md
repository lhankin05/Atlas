# Atlas

Chief of staff for VR training work in Unity. Keeps you on track through the pipeline
(Brief, Design, Build, Test, Review, Push), logs your day, checks in, and runs a weekly reflection.

## Run it

Needs Python 3. Open a terminal in this folder and run:

    python server.py

Then open http://localhost:8000/atlas.html. Stop with Ctrl+C.

On first run, Atlas creates `openai-api-key.txt` next to `server.py`. Paste your OpenAI API key
into that file and save it. Put only the key in the file, on one line. You do not need to enter
the key in the webpage or restart the server after changing the file.

The key file is ignored by git and is never served to the browser. Atlas sends AI requests through
the local Python server, which reads the key file and calls OpenAI. The server listens only on
`127.0.0.1` (this computer).

## Data and privacy

Your tasks, log, reflections, chat and settings are saved in `atlas-data.json` next to the server
when using the local server, or in this browser's local storage when opening the HTML directly.
The JSON file and API key file are ignored by git, but are plaintext on your computer; keep them
private.

When "Share my work context with Atlas" is enabled, Atlas may send your open tasks, today's log,
and latest weekly reflection answers to OpenAI to help answer questions, create check-in questions,
and prepare weekly plans and summaries. When sharing is off, those features use generic prompts
instead of your task, log, or reflection content. Your explicit chat messages are sent to OpenAI
whenever you use chat.

Run Atlas through `python server.py` for AI features. Opening `atlas.html` directly still lets you
use the task tracker, but the local OpenAI proxy is not available.
