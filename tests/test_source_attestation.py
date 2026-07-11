from __future__ import annotations

import functools
import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402
import szl_source_attestation  # noqa: E402


MEASUREMENT = {
    "hf_revision": "a" * 40,
    "last_modified": "2026-07-11T22:00:00.000Z",
    "observed_at": "2026-07-11T22:00:01Z",
    "state": "MEASURED",
    "method": "TEST_FIXTURE",
    "resolver": "https://example.invalid/hf-head",
}


class SourceAttestationTests(unittest.TestCase):
    def test_unknown_source_never_invents_commit_or_parity(self):
        with patch.object(szl_source_attestation, "measure_hf_head", return_value=MEASUREMENT):
            payload = szl_source_attestation.build_attestation(
                space_id=server.SPACE_ID,
                source=server.SOURCE_OBSERVATION,
                alignment_state="UNKNOWN",
                overlay_base_revision=server.HF_OVERLAY_BASE_REVISION,
            )
        self.assertIsNone(payload["source"]["commit"])
        self.assertEqual("PENDING_SOURCE_RESOLUTION", payload["source"]["state"])
        self.assertEqual("UNKNOWN", payload["source"]["relation"])
        self.assertEqual("UNKNOWN", payload["alignment_state"])
        self.assertEqual("NOT_CLAIMED", payload["claims"]["github_parity"])
        self.assertEqual("a" * 40, payload["deployment"]["hf_revision"])

    def test_well_known_route_is_json_no_store_and_hardened(self):
        handler = functools.partial(server.HardenedHandler, directory=str(ROOT))
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.object(szl_source_attestation, "measure_hf_head", return_value=MEASUREMENT):
                with urlopen(
                    f"http://127.0.0.1:{httpd.server_port}/.well-known/szl-source.json?refresh=1",
                    timeout=3,
                ) as response:
                    payload = json.load(response)
                    self.assertEqual(200, response.status)
                    self.assertEqual("application/json; charset=utf-8", response.headers["Content-Type"])
                    self.assertEqual("no-store", response.headers["Cache-Control"])
                    self.assertEqual("nosniff", response.headers["X-Content-Type-Options"])
                    self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
                    self.assertEqual("COMPUTED", response.headers["X-SZL-Evidence-State"])
                    self.assertEqual("UNKNOWN", payload["alignment_state"])
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()

