#!/usr/bin/env python3
"""Publish the SDA runtime files with an exact GitHub source binding."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

from huggingface_hub import HfApi

_SHA = re.compile(r"^[0-9a-f]{40}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ROOT_FILES = (
    "Dockerfile",
    "LICENSE",
    "README.md",
    "SPACE_PROVENANCE.json",
    "index.html",
    "server.py",
    "szl_source_attestation.py",
)


def source_binding(repository: str, revision: str) -> dict[str, str]:
    repository = repository.strip()
    revision = revision.strip().lower()
    if not _REPOSITORY.fullmatch(repository):
        sys.exit("Source repository must be an owner/name identifier.")
    if not _SHA.fullmatch(revision):
        sys.exit("Source revision must be an exact 40-character Git SHA.")
    return {
        "schema": "szl.source-binding/v1",
        "source_repository": repository,
        "source_revision": revision,
        "source_path": "",
        "relation": "exact-runtime-file-set",
        "evidence_url": f"https://github.com/{repository}/tree/{revision}",
    }


def build_release(source: Path, destination: Path, binding: dict[str, str]) -> None:
    for relative in ROOT_FILES:
        path = source / relative
        if not path.is_file():
            sys.exit(f"Required runtime file is missing: {relative}")
        shutil.copy2(path, destination / relative)
    assets = source / "assets"
    if not assets.is_dir():
        sys.exit("Required runtime directory is missing: assets")
    shutil.copytree(assets, destination / "assets")
    (destination / "SOURCE_BINDING.json").write_text(
        json.dumps(binding, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", default=".")
    parser.add_argument("--repo-id", default="SZLHOLDINGS/sda")
    parser.add_argument("--token", required=True)
    parser.add_argument(
        "--source-repository",
        default=os.environ.get("GITHUB_REPOSITORY", "szl-holdings/sda"),
    )
    parser.add_argument("--source-revision", default=os.environ.get("GITHUB_SHA", ""))
    args = parser.parse_args()

    source = Path(args.source_dir).resolve()
    binding = source_binding(args.source_repository, args.source_revision)
    with tempfile.TemporaryDirectory(prefix="szl-sda-space-") as temporary:
        release = Path(temporary) / "release"
        release.mkdir()
        build_release(source, release, binding)
        HfApi(token=args.token).upload_folder(
            repo_id=args.repo_id,
            repo_type="space",
            folder_path=str(release),
            commit_message=(
                "deploy: bind SDA runtime to "
                f"{binding['source_repository']}@{binding['source_revision']}"
            ),
        )
    print(
        f"Deployed source-bound SDA runtime to {args.repo_id} "
        f"from {binding['source_repository']}@{binding['source_revision']}"
    )


if __name__ == "__main__":
    main()
