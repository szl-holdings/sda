"""Honest deployment-source evidence for a public Hugging Face Space.

The Hugging Face repository head is measured independently from GitHub source
observations. A source reference never implies byte parity, a reproducible
build, or proof of the exact process revision during a rolling deployment.
"""
from __future__ import annotations

import json
import re
import threading
import time
import urllib.request
from datetime import datetime, timezone
from typing import Any


_SHA = re.compile(r"^[0-9a-f]{40}$")
_CACHE_LOCK = threading.Lock()
_CACHE: dict[str, dict[str, Any]] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _valid_sha(value: object) -> str | None:
    candidate = str(value or "").strip().lower()
    return candidate if _SHA.fullmatch(candidate) else None


def measure_hf_head(space_id: str, force: bool = False) -> dict[str, Any]:
    """Measure the Hub repository head; never label it as process provenance."""
    now = time.monotonic()
    with _CACHE_LOCK:
        cached = _CACHE.get(space_id)
        if not force and cached and now - float(cached["stored_at"]) < 60:
            return dict(cached["measurement"])

    endpoint = (
        f"https://huggingface.co/api/spaces/{space_id}"
        "?expand[]=sha&expand[]=lastModified"
    )
    request = urllib.request.Request(
        endpoint,
        headers={
            "Accept": "application/json",
            "User-Agent": "szl-source-attestation/2.0",
        },
    )
    revision = None
    last_modified = None
    error = None
    try:
        with urllib.request.urlopen(request, timeout=4) as response:
            payload = json.load(response)
        revision = _valid_sha(payload.get("sha"))
        candidate_time = payload.get("lastModified")
        if isinstance(candidate_time, str) and "T" in candidate_time:
            last_modified = candidate_time
    except Exception as exc:  # the contract reports unavailability, never guesses
        error = type(exc).__name__

    measurement: dict[str, Any] = {
        "hf_revision": revision,
        "last_modified": last_modified,
        "observed_at": _now_iso(),
        "state": "MEASURED" if revision else "UNAVAILABLE",
        "method": "HUGGINGFACE_API" if revision else "UNAVAILABLE",
        "resolver": endpoint,
    }
    if error:
        measurement["error"] = error
    with _CACHE_LOCK:
        _CACHE[space_id] = {
            "stored_at": time.monotonic(),
            "measurement": dict(measurement),
        }
    return measurement


def build_attestation(
    *,
    space_id: str,
    source: dict[str, Any],
    alignment_state: str,
    overlay_base_revision: str,
    force: bool = False,
) -> dict[str, Any]:
    measurement = measure_hf_head(space_id, force=force)
    revision = measurement["hf_revision"]
    return {
        "schema": "szl.deployment-source/v1",
        "source": dict(source),
        "deployment": {
            "hf_space": space_id,
            "hf_revision": revision,
        },
        "built_at": measurement["last_modified"],
        "observed_at": measurement["observed_at"],
        "transport_state": "REACHABLE",
        "evidence_state": "COMPUTED" if revision else "UNAVAILABLE",
        "verification_state": "STRUCTURAL_ONLY",
        "authority_state": "READ_ONLY",
        "alignment_state": alignment_state,
        "attestation_state": "UNSIGNED_STRUCTURAL",
        "claims": {
            "github_parity": "NOT_CLAIMED",
            "reproducible_build": "NOT_CLAIMED",
            "running_process_revision": "NOT_CLAIMED",
        },
        "extensions": {
            "schema": "szl.deployment-source-evidence/v1",
            "deployment_revision_evidence": {
                **measurement,
                "semantics": (
                    "Measured Hugging Face repository head; external verification "
                    "must confirm runtime SHA convergence after deployment."
                ),
            },
            "overlay": {
                "base_revision": overlay_base_revision,
                "base_revision_semantics": (
                    "Hugging Face head inspected before this attestation overlay."
                ),
            },
        },
        "limits": [
            "The Hugging Face revision is measured independently from GitHub evidence.",
            "A GitHub observation does not establish deployed-artifact equivalence.",
            "Repository-head evidence is not proof of the exact process revision during a rolling deploy.",
            "This unsigned structural document does not establish SLSA provenance or reproducible builds.",
        ],
    }

