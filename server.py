"""Atlas local server: serves atlas.html and saves your data to atlas-data.json.

Run:  python server.py        (optional port: python server.py 8000)
Open: http://localhost:8000/atlas.html
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "atlas-data.json")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
HOSTS = {f"localhost:{PORT}", f"127.0.0.1:{PORT}"}
ORIGINS = {f"http://{h}" for h in HOSTS}
PUBLIC = {"/atlas.html", "/favicon.ico"}


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
        if path in ("/", ""):
            return self._reply(302, extra={"Location": "/atlas.html"})
        if path not in PUBLIC:
            return self._reply(404, b"Not found", "text/plain")
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/data" or not self._trusted():
            return self._reply(403, b"{}")
        if "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._reply(415, b"{}")
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            json.loads(raw)
        except ValueError:
            return self._reply(400, b"{}")
        tmp = DATA + ".tmp"
        with open(tmp, "wb") as f:
            f.write(raw)
        os.replace(tmp, DATA)
        return self._reply(200, b"{}")

    def log_message(self, fmt, *args):
        if "/api/data" not in (args[0] if args else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    print(f"Atlas running at http://localhost:{PORT}/atlas.html")
    print(f"Your data is saved in {DATA}")
    print("Press Ctrl+C to stop.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
