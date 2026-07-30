import functools
import json
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402


class HealthRouteTests(unittest.TestCase):
    def test_packaged_surface_is_ready_with_external_feeds_unverified(self):
        payload = server.health_payload(ROOT)
        self.assertTrue(payload["ready"])
        self.assertEqual("READY_WITH_UNVERIFIED_EXTERNAL_FEEDS", payload["status"])
        self.assertEqual(
            "NOT_MEASURED", payload["external_dependencies"]["a11oy_compute_pool"]
        )
        self.assertEqual(
            "NOT_MEASURED",
            payload["external_dependencies"]["killinchu_common_operating_picture"],
        )
        self.assertEqual(
            "UNAVAILABLE",
            payload["external_dependencies"]["source_repository_relation"],
        )

    def test_missing_local_dependencies_fail_readiness_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = server.health_payload(directory)
        self.assertFalse(payload["ready"])
        self.assertEqual("NOT_READY", payload["status"])

    def test_live_and_health_routes_are_uncacheable(self):
        handler = functools.partial(server.HardenedHandler, directory=str(ROOT))
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            for route in ("/live", "/health"):
                with urlopen(
                    f"http://127.0.0.1:{httpd.server_port}{route}", timeout=3
                ) as response:
                    payload = json.load(response)
                    self.assertEqual(200, response.status)
                    self.assertEqual("no-store", response.headers["Cache-Control"])
                    self.assertEqual(server.SPACE_ID, payload["space_id"])
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=3)

    def test_health_route_returns_503_when_snapshot_is_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            handler = functools.partial(server.HardenedHandler, directory=directory)
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                with self.assertRaises(HTTPError) as caught:
                    urlopen(
                        f"http://127.0.0.1:{httpd.server_port}/health", timeout=3
                    )
                self.assertEqual(503, caught.exception.code)
                payload = json.loads(caught.exception.read())
                self.assertFalse(payload["ready"])
            finally:
                httpd.shutdown()
                httpd.server_close()
                thread.join(timeout=3)

    def test_readyz_requires_exact_source_binding(self):
        handler = functools.partial(server.HardenedHandler, directory=str(ROOT))
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            with self.assertRaises(HTTPError) as caught:
                urlopen(
                    f"http://127.0.0.1:{httpd.server_port}/readyz", timeout=3
                )
            self.assertEqual(503, caught.exception.code)
            payload = json.loads(caught.exception.read())
            self.assertFalse(payload["source_ready"])
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
