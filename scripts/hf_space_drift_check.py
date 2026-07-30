#!/usr/bin/env python3
"""Verify live SDA runtime files and source binding against GitHub."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

from hf_space_deploy import ROOT_FILES

_SHA = re.compile(r"^[0-9a-f]{40}$")
RESOLVE = "https://huggingface.co/spaces/{repo}/resolve/main/{path}"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def runtime_files(source: Path) -> list[Path]:
    files = [source / relative for relative in ROOT_FILES]
    files.extend(sorted(path for path in (source / "assets").rglob("*") if path.is_file()))
    return files


def fetch(repo: str, relative: str) -> bytes:
    with urllib.request.urlopen(
        RESOLVE.format(repo=repo, path=relative),
        timeout=30,
    ) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", default=".")
    parser.add_argument("--repo-id", default="SZLHOLDINGS/sda")
    parser.add_argument("--source-revision", required=True)
    args = parser.parse_args()

    source = Path(args.source_dir).resolve()
    revision = args.source_revision.strip().lower()
    if not _SHA.fullmatch(revision):
        sys.exit("Expected source revision is not an exact Git SHA.")

    failed = False
    files = runtime_files(source)
    for path in files:
        if not path.is_file():
            print(f"MISSING-SOURCE {path.relative_to(source).as_posix()}")
            failed = True
            continue
        relative = path.relative_to(source).as_posix()
        local = digest(path.read_bytes())
        try:
            live = digest(fetch(args.repo_id, relative))
        except Exception as exc:  # noqa: BLE001
            print(f"MISSING-LIVE {relative} ({exc})")
            failed = True
            continue
        state = "OK" if local == live else "MISMATCH"
        print(f"{local[:16]} {live[:16]} {state} {relative}")
        failed = failed or state != "OK"

    try:
        binding = json.loads(fetch(args.repo_id, "SOURCE_BINDING.json"))
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"Source binding unavailable: {exc}")
    expected = {
        "schema": "szl.source-binding/v1",
        "source_repository": "szl-holdings/sda",
        "source_revision": revision,
        "source_path": "",
        "relation": "exact-runtime-file-set",
    }
    for key, value in expected.items():
        if binding.get(key) != value:
            print(
                f"BINDING-MISMATCH {key}: "
                f"expected {value!r}, observed {binding.get(key)!r}"
            )
            failed = True
    if failed:
        sys.exit("Live SDA runtime is not aligned with the exact GitHub source.")
    print(
        f"Aligned {len(files)} runtime files and source binding "
        f"to szl-holdings/sda@{revision}."
    )


if __name__ == "__main__":
    main()
