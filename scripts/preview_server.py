#!/usr/bin/env python3
"""Local preview server for lightthebe.am.

Mimics Cloudflare Pages clean-URL routing so /players, /stats, /about, /beam, etc.
resolve to their .html files, and applies the _redirects map. Dev-only; not deployed.
"""
import http.server
import os
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8788
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Subset of _redirects that matters for clicking around the preview.
REDIRECTS = {
    "/index.html": "/",
    "/home": "/",
    "/facts": "/stats",
    "/facts.html": "/stats",
    "/lore": "/stats",
    "/coaches": "/totals",
    "/coaches.html": "/totals",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path in REDIRECTS:
            self.send_response(301)
            self.send_header("Location", REDIRECTS[path])
            self.end_headers()
            return
        # Clean URLs: /players -> players.html when no literal file exists.
        if path != "/" and not os.path.splitext(path)[1]:
            candidate = os.path.join(ROOT, path.lstrip("/") + ".html")
            if os.path.isfile(candidate):
                self.path = path + ".html"
        return super().do_GET()

    def log_message(self, *args):
        pass


with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"preview serving {ROOT} at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
