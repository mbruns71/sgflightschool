#!/usr/bin/env python3
"""
Local preview server for the built site.

Rebuilds first, then serves site/ on http://localhost:8788 with Cloudflare
Pages-style clean URLs (/courses -> /courses/index.html) and _redirects support.

Note: this avoids `python3 -m http.server`, whose argparse defaults call
os.getcwd() — which raises PermissionError inside Box CloudStorage folders.
"""
import functools
import http.server
import os
import socketserver
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
PORT = 8788


def load_redirects():
    rules = {}
    path = os.path.join(SITE, "_redirects")
    if not os.path.exists(path):
        return rules
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                rules[parts[0]] = (parts[1], int(parts[2]) if len(parts) > 2 else 302)
    return rules


REDIRECTS = load_redirects()


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        clean = self.path.split("?")[0].rstrip("/") or "/"
        if clean in REDIRECTS:
            target, code = REDIRECTS[clean]
            self.send_response(code)
            self.send_header("Location", target)
            self.end_headers()
            return
        # Clean URLs: /courses -> /courses/index.html
        if clean != "/" and "." not in os.path.basename(clean):
            candidate = os.path.join(SITE, clean.lstrip("/"), "index.html")
            if os.path.exists(candidate):
                self.path = clean.rstrip("/") + "/index.html"
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


def main():
    sys.path.insert(0, ROOT)
    import build
    build.main()

    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=SITE)
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Serving {SITE} at http://localhost:{PORT}", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
