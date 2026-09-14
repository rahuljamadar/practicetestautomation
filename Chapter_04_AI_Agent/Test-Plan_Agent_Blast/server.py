"""Local server for the Test Plan Agent browser app.

BLAST Phase 5 (Trigger): run the app locally in the browser.
Serves index.html and exposes POST /generate which runs the
deterministic Python tools and returns rendered markdown.

Usage:  python server.py
Then:   open http://127.0.0.1:8000
"""

import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(ROOT, "tools")

PORT = 8000


def run_tool(script, payload):
    """Run a tools/ script with JSON on stdin, return (returncode, output)."""
    proc = subprocess.run(
        [sys.executable, os.path.join(TOOLS, script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=ROOT,
    )
    return proc.returncode, proc.stdout


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="application/json; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html_path = os.path.join(ROOT, "index.html")
            with open(html_path, "rb") as fh:
                self._send(200, fh.read().decode("utf-8"), "text/html; charset=utf-8")
        else:
            self._send(404, json.dumps({"error": "Not found"}))

    def do_POST(self):
        if self.path != "/generate":
            self._send(404, json.dumps({"error": "Not found"}))
            return

        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            self._send(400, json.dumps({"ok": False, "error": "Invalid JSON"}))
            return

        # BLAST Phase 2 (Link) handshake: validate, then generate.
        rc, out = run_tool("validate_requirement.py", payload)
        if rc != 0:
            self._send(200, json.dumps({"ok": False, "errors": json.loads(out)["errors"]}))
            return

        rc, out = run_tool("test_plan_generator.py", payload)
        if rc != 0:
            self._send(500, json.dumps({"ok": False, "error": out}))
            return

        md_path = os.path.join(ROOT, ".tmp", "test_plan_output.md")
        with open(md_path, "r", encoding="utf-8") as fh:
            markdown = fh.read()

        self._send(200, json.dumps({
            "ok": True,
            "markdown": markdown,
            "meta": json.loads(out),
        }))

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[server] {fmt % args}\n")


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Test Plan Agent running at http://127.0.0.1:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.shutdown()


if __name__ == "__main__":
    main()
