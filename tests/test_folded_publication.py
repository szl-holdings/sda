from pathlib import Path
from unittest.mock import Mock

import pytest

from scripts import hf_space_deploy as deploy

ROOT = Path(__file__).resolve().parents[1]
DENIAL = "Standalone Space publication is disabled for folded repositories."


def test_folded_repository_has_no_standalone_publish_workflow():
    assert (ROOT / "FOLD.md").is_file()
    assert not (ROOT / ".github/workflows/hf-space-deploy.yml").exists()


def test_folded_entrypoint_stops_before_credentials_or_provider(monkeypatch):
    parse = Mock(side_effect=AssertionError("arguments must not be parsed"))
    client = Mock(side_effect=AssertionError("provider must not be contacted"))
    stage = Mock(side_effect=AssertionError("release must not be staged"))
    monkeypatch.setattr(deploy.argparse.ArgumentParser, "parse_args", parse)
    monkeypatch.setattr(deploy, "HfApi", client)
    monkeypatch.setattr(deploy.tempfile, "TemporaryDirectory", stage)
    with pytest.raises(SystemExit, match=DENIAL):
        deploy.main()
    parse.assert_not_called()
    client.assert_not_called()
    stage.assert_not_called()


def test_alternate_source_cannot_bypass_repository_fold(tmp_path, monkeypatch):
    copy = Mock(side_effect=AssertionError("runtime files must not be copied"))
    monkeypatch.setattr(deploy.shutil, "copy2", copy)
    with pytest.raises(SystemExit, match=DENIAL):
        deploy.build_release(tmp_path, tmp_path / "release", {})
    copy.assert_not_called()


@pytest.mark.parametrize("marker_is_directory", [False, True])
def test_source_fold_marker_also_denies_publication(tmp_path, monkeypatch, marker_is_directory):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    marker = source / "FOLD.md"
    if marker_is_directory:
        marker.mkdir()
    else:
        marker.write_text("archive-bound\n", encoding="utf-8")
    monkeypatch.setattr(deploy, "REPOSITORY_ROOT", checkout)
    with pytest.raises(SystemExit, match=DENIAL):
        deploy.require_standalone_publication(source)


def test_unfolded_source_passes_only_the_local_fold_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(deploy, "REPOSITORY_ROOT", tmp_path)
    deploy.require_standalone_publication(tmp_path)


def test_source_binding_remains_a_pure_local_operation():
    binding = deploy.source_binding("szl-holdings/sda", "a" * 40)
    assert binding["source_revision"] == "a" * 40
    assert binding["relation"] == "exact-runtime-file-set"


class _Api:
    def __init__(self, exists):
        self.exists = exists
        self.uploads = 0

    def repo_exists(self, repo_id, repo_type=None):
        assert repo_type == "space"
        return self.exists

    def upload_folder(self, **_):
        self.uploads += 1


def test_absent_target_space_fails_closed_before_upload():
    api = _Api(exists=False)
    with pytest.raises(SystemExit, match="Space absent: example-owner/absent"):
        deploy.require_existing_space(api, "example-owner/absent")
    assert api.uploads == 0


def test_existing_target_space_passes_the_existence_gate():
    deploy.require_existing_space(_Api(exists=True), "example-owner/present")


def test_malformed_target_is_refused():
    with pytest.raises(SystemExit, match="owner/name"):
        deploy.require_existing_space(_Api(exists=True), "not a repo id")


def test_no_executable_file_targets_the_retired_space_id():
    for relative in (
        "server.py",
        "szl_source_attestation.py",
        "scripts/hf_space_deploy.py",
        "scripts/hf_space_drift_check.py",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "SZLHOLDINGS/sda" not in text, relative
