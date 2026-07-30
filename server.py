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
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from szl_source_attestation import build_attestation

PORT = 7860
DIRECTORY = "/app"
SPACE_ID = "SZLHOLDINGS/sda"
HF_OVERLAY_BASE_REVISION = "05cd77a1e728f59ab920e04bd632e7ff64a25b2e"
SOURCE_BINDING_FILENAME = "SOURCE_BINDING.json"
_SHA = re.compile(r"^[0-9a-f]{40}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REQUIRED_ASSETS = (
    "index.html",
    "assets/cop.js",
    "assets/scene.js",
    "assets/sda-fabric.js",
    "assets/style.css",
    "assets/three.module.min.js",
)
SNAPSHOT_FILE = "assets/snapshot-compute-pool.json"

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


def local_dependency_state(directory=DIRECTORY):
    """Validate only Space-local assets; external operational feeds stay unknown."""
    root = Path(directory)
    assets = {}
    ready = True
    for relative in REQUIRED_ASSETS:
        path = root / relative
        present = path.is_file() and path.stat().st_size > 0
        assets[relative] = "READY" if present else "MISSING_OR_EMPTY"
        ready = ready and present

    snapshot_path = root / SNAPSHOT_FILE
    snapshot_state = "READY"
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        if not isinstance(snapshot, (dict, list)):
            raise ValueError("snapshot must be structured JSON")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        snapshot_state = "MISSING_OR_INVALID"
        ready = False
    return {
        "ready": ready,
        "assets": assets,
        "compute_pool_snapshot": snapshot_state,
    }


def load_source_binding(directory=DIRECTORY):
    unavailable = {
        "repository": "szl-holdings/sda",
        "commit": None,
        "path": "",
        "state": "UNAVAILABLE",
        "relation": "exact-runtime-file-set",
        "evidence_url": None,
    }
    try:
        payload = json.loads(
            (Path(directory) / SOURCE_BINDING_FILENAME).read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, json.JSONDecodeError):
        return unavailable
    repository = str(payload.get("source_repository", "")).strip()
    revision = str(payload.get("source_revision", "")).strip().lower()
    if (
        payload.get("schema") != "szl.source-binding/v1"
        or not _REPOSITORY.fullmatch(repository)
        or not _SHA.fullmatch(revision)
        or payload.get("source_path") != ""
        or payload.get("relation") != "exact-runtime-file-set"
    ):
        return unavailable
    return {
        "repository": repository,
        "commit": revision,
        "path": "",
        "state": "SOURCE_BOUND",
        "relation": "exact-runtime-file-set",
        "evidence_url": f"https://github.com/{repository}/tree/{revision}",
    }


def build_source_attestation(directory=DIRECTORY, *, force=False):
    source = load_source_binding(directory)
    source_bound = source["state"] == "SOURCE_BOUND"
    payload = build_attestation(
        space_id=SPACE_ID,
        source=source,
        alignment_state="SOURCE_BOUND_DEPLOYMENT" if source_bound else "UNAVAILABLE",
        overlay_base_revision=source["commit"] or HF_OVERLAY_BASE_REVISION,
        force=force,
    )
    if source_bound:
        payload["verification_state"] = "SOURCE_BOUND"
        payload["claims"]["github_parity"] = "EXACT_RUNTIME_FILE_SET"
        payload["limits"] = [
            "GitHub parity is scoped to the runtime files selected by the deploy workflow.",
            "The deployment workflow verifies every shipped runtime file by SHA-256.",
            "External feeds, operational accuracy, and reproducible builds are not claimed.",
        ]
    return payload


def live_payload():
    return {
        "schema": "szl.space-health/v1",
        "space_id": SPACE_ID,
        "status": "LIVE",
        "ready": None,
        "transport_state": "REACHABLE",
        "evidence_state": "PROCESS_LIVENESS_ONLY",
        "verification_state": "STRUCTURAL_ONLY",
        "authority_state": "READ_ONLY",
    }


def health_payload(directory=DIRECTORY):
    dependencies = local_dependency_state(directory)
    source = load_source_binding(directory)
    return {
        "schema": "szl.space-health/v1",
        "space_id": SPACE_ID,
        "status": (
            "READY_WITH_UNVERIFIED_EXTERNAL_FEEDS"
            if dependencies["ready"]
            else "NOT_READY"
        ),
        "ready": dependencies["ready"],
        "transport_state": "REACHABLE",
        "evidence_state": (
            "LOCAL_DEPENDENCIES_VERIFIED"
            if dependencies["ready"]
            else "LOCAL_DEPENDENCY_FAILURE"
        ),
        "verification_state": "STRUCTURAL_ONLY",
        "authority_state": "READ_ONLY",
        "dependencies": dependencies,
        "external_dependencies": {
            "a11oy_compute_pool": "NOT_MEASURED",
            "killinchu_common_operating_picture": "NOT_MEASURED",
            "source_repository_relation": source["state"],
        },
        "health_boundary": (
            "Readiness covers the local read-only SDA visualization and packaged "
            "snapshot only; it does not assert live sensors, effectors, orbital "
            "capability, compute, or external feeds."
        ),
    }


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
        self.send_header(
            "X-SZL-Verification-State",
            payload.get("verification_state", "UNAVAILABLE"),
        )
        self.send_header("X-SZL-Authority-State", "READ_ONLY")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlsplit(self.path)
        directory = self.directory or DIRECTORY
        if parsed.path in {"/live", "/livez", "/healthz"}:
            self._send_json(live_payload())
            return
        if parsed.path in {"/health", "/readyz"}:
            payload = health_payload(directory)
            if parsed.path == "/readyz":
                source_bound = (
                    payload["external_dependencies"]["source_repository_relation"]
                    == "SOURCE_BOUND"
                )
                payload["source_ready"] = source_bound
                payload["ready"] = bool(payload["ready"] and source_bound)
                payload["status"] = (
                    "READY_WITH_UNVERIFIED_EXTERNAL_FEEDS"
                    if payload["ready"]
                    else "NOT_READY"
                )
            self._send_json(payload, 200 if payload["ready"] else 503)
            return
        if parsed.path == "/api/build-info":
            source = load_source_binding(directory)
            source_bound = source["state"] == "SOURCE_BOUND"
            payload = {
                "transport_state": "REACHABLE",
                "evidence_state": "OBSERVED" if source_bound else "UNAVAILABLE",
                "verification_state": "SOURCE_BOUND" if source_bound else "UNAVAILABLE",
                "authority_state": "READ_ONLY",
                "service": "sda",
                "version": "1.0",
                "build": {
                    "state": "OBSERVED" if source_bound else "UNAVAILABLE",
                    "revision": source["commit"],
                    "repository": source["repository"],
                    "path": source["path"],
                },
                "source_revision": source["commit"],
                "source_revision_state": "OBSERVED" if source_bound else "UNAVAILABLE",
                "github_huggingface_alignment": (
                    "SOURCE_BOUND_DEPLOYMENT" if source_bound else "UNAVAILABLE"
                ),
                "receipt_minted": False,
            }
            self._send_json(payload, 200 if source_bound else 503)
            return
        if parsed.path == "/.well-known/szl-source.json":
            force = parse_qs(parsed.query).get("refresh", ["0"])[0] == "1"
            payload = build_source_attestation(directory, force=force)
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
