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
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from szl_source_attestation import build_attestation

PORT = 7860
DIRECTORY = "/app"
SPACE_ID = "SZLHOLDINGS/sda"
HF_OVERLAY_BASE_REVISION = "05cd77a1e728f59ab920e04bd632e7ff64a25b2e"
SOURCE_OBSERVATION = {
    "repository": "szl-holdings/sda",
    "commit": None,
    "path": "",
    "state": "PENDING_SOURCE_RESOLUTION",
    "relation": "UNKNOWN",
    "evidence_url": "https://api.github.com/repos/szl-holdings/sda",
    "observation": {
        "observed_at": "2026-07-11T22:00:20Z",
        "http_status": 404,
        "meaning": (
            "The inferred name-matched GitHub repository was not found. "
            "No source commit or parity claim is available."
        ),
    },
}

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

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-SZL-Transport-State", "REACHABLE")
        self.send_header("X-SZL-Evidence-State", payload.get("evidence_state", "UNAVAILABLE"))
        self.send_header("X-SZL-Authority-State", "READ_ONLY")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/.well-known/szl-source.json":
            force = parse_qs(parsed.query).get("refresh", ["0"])[0] == "1"
            payload = build_attestation(
                space_id=SPACE_ID,
                source=SOURCE_OBSERVATION,
                alignment_state="UNKNOWN",
                overlay_base_revision=HF_OVERLAY_BASE_REVISION,
                force=force,
            )
            self._send_json(payload)
            return
        super().do_GET()

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
