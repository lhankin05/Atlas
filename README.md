# Atlas

A local project-management dashboard for VR training development. Atlas tracks work through Brief, Design, Build, Test, Review and Push, records daily notes, supports AI chat, and includes guided daily and weekly reflections.

## Run it

Requires Python 3.9 or newer. Copy `.env.example` to `.env` and add your OpenAI API key:

    OPENAI_API_KEY=your_real_key_here

Keep `.env` private; it is ignored by Git. Then run:

    python server.py

Open http://localhost:8000/atlas.html. Stop the server with Ctrl+C.

The server reads the key from `.env` and sends AI requests to OpenAI. The key is not stored in the webpage or sent to the browser. Your tasks, chat, notes and reflections are saved to `atlas-data.json` beside the server; that file is ignored by Git. Do not expose this development server to a public network.

## Daily workflow

Use Home to log updates as you work. At the end of the day, open **End-of-day review**, answer the short guided questions, and ask Atlas to compare your notes with existing open tasks. It suggests a summary, blockers, tomorrow's first priority, and potential new tasks. Review the suggestions and approve only the tasks you want added. Weekly reflection remains available separately.

Opening `atlas.html` directly from disk is not supported for AI features; run the local server so the API key stays on the server.
