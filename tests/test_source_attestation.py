from __future__ import annotations

import functools
import json
import sys
import tempfile
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
    @staticmethod
    def _write_binding(directory, revision="b" * 40):
        (Path(directory) / "SOURCE_BINDING.json").write_text(
            json.dumps(
                {
                    "schema": "szl.source-binding/v1",
                    "source_repository": "szl-holdings/sda",
                    "source_revision": revision,
                    "source_path": "",
                    "relation": "exact-runtime-file-set",
                }
            ),
            encoding="utf-8",
        )

    def test_exact_runtime_binding_is_reported_without_accuracy_overclaim(self):
        with tempfile.TemporaryDirectory() as directory:
            self._write_binding(directory)
            with patch.object(
                szl_source_attestation, "measure_hf_head", return_value=MEASUREMENT
            ):
                payload = server.build_source_attestation(directory)
        self.assertEqual("b" * 40, payload["source"]["commit"])
        self.assertEqual("SOURCE_BOUND", payload["source"]["state"])
        self.assertEqual("exact-runtime-file-set", payload["source"]["relation"])
        self.assertEqual("SOURCE_BOUND_DEPLOYMENT", payload["alignment_state"])
        self.assertEqual("EXACT_RUNTIME_FILE_SET", payload["claims"]["github_parity"])
        self.assertEqual("NOT_CLAIMED", payload["claims"]["reproducible_build"])
        self.assertEqual("a" * 40, payload["deployment"]["hf_revision"])

    def test_well_known_route_is_json_no_store_and_hardened(self):
        with tempfile.TemporaryDirectory() as directory:
            self._write_binding(directory)
            handler = functools.partial(server.HardenedHandler, directory=directory)
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                with patch.object(
                    szl_source_attestation, "measure_hf_head", return_value=MEASUREMENT
                ):
                    with urlopen(
                        f"http://127.0.0.1:{httpd.server_port}/.well-known/szl-source.json?refresh=1",
                        timeout=3,
                    ) as response:
                        payload = json.load(response)
                        self.assertEqual(200, response.status)
                        self.assertEqual(
                            "application/json; charset=utf-8",
                            response.headers["Content-Type"],
                        )
                        self.assertEqual("no-store", response.headers["Cache-Control"])
                        self.assertEqual(
                            "nosniff", response.headers["X-Content-Type-Options"]
                        )
                        self.assertIn(
                            "default-src 'self'",
                            response.headers["Content-Security-Policy"],
                        )
                        self.assertEqual(
                            "COMPUTED", response.headers["X-SZL-Evidence-State"]
                        )
                        self.assertEqual(
                            "SOURCE_BOUND_DEPLOYMENT", payload["alignment_state"]
                        )
            finally:
                httpd.shutdown()
                httpd.server_close()
                thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()

