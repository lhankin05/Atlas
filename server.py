"""Atlas local server: serves the app, saves data, and proxies OpenAI requests.

Run:  python server.py        (optional port: python server.py 8000)
Open: http://localhost:8000/atlas.html
"""
import json
import os
import sys
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "atlas-data.json")
API_KEY_FILE = os.path.join(ROOT, "openai-api-key.txt")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
HOSTS = {f"localhost:{PORT}", f"127.0.0.1:{PORT}"}
ORIGINS = {f"http://{h}" for h in HOSTS}
PUBLIC = {"/atlas.html", "/favicon.ico"}
MAX_REQUEST_BYTES = 1_000_000


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

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length < 0 or length > MAX_REQUEST_BYTES:
            raise ValueError("Request is too large.")
        raw = self.rfile.read(length)
        return json.loads(raw)

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
        if path in ("/", ""):
            return self._reply(302, extra={"Location": "/atlas.html"})
        if path not in PUBLIC:
            return self._reply(404, b"Not found", "text/plain")
        return super().do_GET()

    def do_POST(self):
        if not self._trusted():
            return self._json(403, {"error": {"message": "Request must come from the local Atlas page."}})
        if "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._json(415, {"error": {"message": "Expected a JSON request."}})
        try:
            payload = self._read_json()
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": {"message": "Invalid or oversized JSON request."}})

        if self.path == "/api/data":
            tmp = DATA + ".tmp"
            with open(tmp, "wb") as f:
                f.write(json.dumps(payload).encode("utf-8"))
            os.replace(tmp, DATA)
            return self._json(200, {})

        if self.path == "/api/chat":
            return self._chat(payload)

        return self._json(404, {"error": {"message": "Unknown API endpoint."}})

    def _chat(self, payload):
        try:
            with open(API_KEY_FILE, "r", encoding="utf-8") as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            api_key = ""

        if not api_key:
            return self._json(400, {"error": {"message": "Add your OpenAI API key to openai-api-key.txt beside server.py, then try again."}})

        system = payload.get("system", "")
        messages = payload.get("messages", [])
        model = payload.get("model") or "gpt-5.5"
        max_tokens = payload.get("max_tokens", 1024)
        if not isinstance(system, str) or not isinstance(messages, list) or not messages:
            return self._json(400, {"error": {"message": "The request needs a system prompt and at least one message."}})
        if not isinstance(model, str) or not model.strip() or not isinstance(max_tokens, int) or not 1 <= max_tokens <= 8192:
            return self._json(400, {"error": {"message": "Invalid model or output token limit."}})
        if any(not isinstance(m, dict) or m.get("role") not in ("user", "assistant") or not isinstance(m.get("content"), str) for m in messages):
            return self._json(400, {"error": {"message": "Messages must have user/assistant roles and text content."}})

        request_body = {
            "model": model.strip(),
            "messages": [{"role": "system", "content": system}] + messages,
            "max_completion_tokens": max_tokens,
        }
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(request_body).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))
            text = result["choices"][0]["message"].get("content") or ""
            return self._json(200, {"content": [{"text": text}]})
        except urllib.error.HTTPError as e:
            try:
                details = json.loads(e.read().decode("utf-8"))
                message = details.get("error", {}).get("message", "OpenAI API request failed.")
            except (ValueError, UnicodeDecodeError):
                message = "OpenAI API request failed with status " + str(e.code) + "."
            return self._json(e.code if 400 <= e.code < 600 else 502, {"error": {"message": message}})
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, ValueError) as e:
            message = str(e) if isinstance(e, urllib.error.URLError) else "Could not read a valid response from OpenAI."
            return self._json(502, {"error": {"message": message}})

    def log_message(self, fmt, *args):
        if "/api/data" not in (args[0] if args else "") and "/api/chat" not in (args[0] if args else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    # Create a private local key file on first run; it is excluded from Git.
    if not os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "w", encoding="utf-8") as f:
            f.write("")
    print(f"Atlas running at http://localhost:{PORT}/atlas.html")
    print(f"Your data is saved in {DATA}")
    print(f"Put your OpenAI API key in {API_KEY_FILE}")
    print("Press Ctrl+C to stop.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
