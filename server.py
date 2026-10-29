"""Atlas local server: serves the app, persists local data, and proxies OpenAI requests.

Run: python server.py
Open: http://localhost:8000/atlas.html
Set OPENAI_API_KEY in a local .env file beside this script.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "atlas-data.json")
ENV_FILE = os.path.join(ROOT, ".env")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
HOSTS = {f"localhost:{PORT}", f"127.0.0.1:{PORT}"}
ORIGINS = {f"http://{h}" for h in HOSTS}
PUBLIC = {"/atlas.html", "/favicon.ico"}


def load_env():
    """Load simple KEY=value entries without requiring an extra dependency."""
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except FileNotFoundError:
        pass


def openai_chat(payload):
    load_env()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OpenAI API key not found. Add OPENAI_API_KEY=... to the local .env file and restart Atlas.")
    messages = payload.get("messages", [])
    if not isinstance(messages, list) or not messages:
        raise ValueError("A non-empty messages array is required.")
    chat_messages = []
    system = payload.get("system", "")
    if system:
        chat_messages.append({"role": "system", "content": str(system)[:20000]})
    for item in messages[-40:]:
        role = item.get("role")
        content = item.get("content")
        if role not in ("user", "assistant") or not isinstance(content, str):
            continue
        chat_messages.append({"role": role, "content": content[:20000]})
    request_body = json.dumps({
        "model": str(payload.get("model") or "gpt-4.1-mini"),
        "messages": chat_messages,
        "max_tokens": max(100, min(int(payload.get("max_tokens", 1200)), 4000)),
        "temperature": 0.3
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=request_body,
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
        return {"text": result["choices"][0]["message"]["content"].strip()}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except ValueError:
            pass
        raise RuntimeError("OpenAI API error: " + str(detail)[:800])


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _reply(self, code, body=b"", ctype="application/json", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _json(self, code, value):
        return self._reply(code, json.dumps(value).encode("utf-8"))

    def _trusted(self):
        origin = self.headers.get("Origin")
        return self.headers.get("Host") in HOSTS and (origin is None or origin in ORIGINS)

    def do_GET(self):
        path = self.path.split("?")[0]
        if not self._trusted():
            return self._reply(403, b"{}")
        if path == "/api/data":
            try:
                with open(DATA, "rb") as f:
                    body = f.read()
            except FileNotFoundError:
                body = b"{}"
            return self._reply(200, body)
        if path in ("", "/"):
            return self._reply(302, extra={"Location": "/atlas.html"})
        if path not in PUBLIC:
            return self._reply(404, b"Not found", "text/plain")
        return super().do_GET()

    def do_POST(self):
        if not self._trusted():
            return self._reply(403, b"{}")
        if "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._reply(415, b"{}")
        try:
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            payload = json.loads(raw)
        except (ValueError, json.JSONDecodeError):
            return self._reply(400, b'{"error":"Invalid JSON"}')
        path = self.path.split("?")[0]
        if path == "/api/data":
            tmp = DATA + ".tmp"
            with open(tmp, "wb") as f:
                f.write(raw)
            os.replace(tmp, DATA)
            return self._json(200, {})
        if path == "/api/ai":
            try:
                return self._json(200, openai_chat(payload))
            except ValueError as exc:
                return self._json(400, {"error": str(exc)})
            except RuntimeError as exc:
                return self._json(502, {"error": str(exc)})
            except Exception as exc:
                return self._json(502, {"error": "Could not reach OpenAI: " + str(exc)[:500]})
        return self._reply(404, b'{"error":"Not found"}')

    def log_message(self, fmt, *args):
        if "/api/data" not in (args[0] if args else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    load_env()
    print(f"Atlas running at http://localhost:{PORT}/atlas.html")
    print(f"Your data is saved in {DATA}")
    if not os.environ.get("OPENAI_API_KEY"):
        print("OpenAI key not found. Create .env from .env.example and add your key.")
    print("Press Ctrl+C to stop.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
