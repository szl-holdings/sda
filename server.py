#!/usr/bin/env python3
"""Hardened static file server for the SZL SDA Space.

Serves exactly the same files as `python -m http.server 7860` (same /app
directory, same port 7860) but adds security response headers on every response:
  - Content-Security-Policy      (tuned to this page's real resources)
  - Strict-Transport-Security    max-age=31536000; includeSubDomains
  - X-Content-Type-Options       nosniff
  - Referrer-Policy              strict-origin-when-cross-origin
  - Server                       clean "szl" banner (suppresses SimpleHTTP/Python
                                  version disclosure)

Additive / non-breaking: no ports or file paths change. The CSP permits every
resource this Space actually uses: the inline ES-module importmap that maps
'three' -> ./assets/three.module.min.js, self-hosted module + classic scripts,
inline styles, the self-hosted SVG favicon + data:/blob: images, and the
read-only cross-origin verify fetches to a-11-oy.com and killinchu, so the
WebGL scene and the SDA verify widget keep working.
"""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 7860
DIRECTORY = "/app"

CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "base-uri 'self'; "
    "object-src 'none'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: blob:; "
    "font-src 'self'; "
    "connect-src 'self' https://a-11-oy.com "
    "https://szlholdings-killinchu.hf.space; "
    "frame-ancestors 'self' https://huggingface.co https://*.hf.space https://*.huggingface.co"
)


class HardenedHandler(SimpleHTTPRequestHandler):
    server_version = "szl"
    sys_version = ""

    def version_string(self):
        return "szl"

    def end_headers(self):
        self.send_header("Content-Security-Policy", CONTENT_SECURITY_POLICY)
        self.send_header(
            "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
        )
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()


if __name__ == "__main__":
    handler = functools.partial(HardenedHandler, directory=DIRECTORY)
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), handler)
    print(f"Serving hardened static site from {DIRECTORY} on 0.0.0.0:{PORT}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
