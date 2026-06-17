#!/usr/bin/env python3
"""Minimal Tier-1 stand-in agent: /healthz and /run."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = os.environ.get("AGENT_VERSION", "0")
PORT = int(os.environ.get("AGENT_PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, {"status": "ok", "version": VERSION})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/run":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
            self._send(200, {"ran": data.get("task", "noop"), "version": VERSION})
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, *_args):
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
