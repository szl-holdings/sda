from pathlib import Path
from unittest.mock import Mock

import pytest

from scripts import hf_space_drift_check as drift

ROOT = Path(__file__).resolve().parents[1]
DENIAL = "Standalone Space verification is disabled for folded repositories."


def test_folded_verifier_stops_before_arguments_or_network(monkeypatch):
    parse = Mock(side_effect=AssertionError("arguments must not be parsed"))
    network = Mock(side_effect=AssertionError("provider must not be contacted"))
    monkeypatch.setattr(drift.argparse.ArgumentParser, "parse_args", parse)
    monkeypatch.setattr(drift.urllib.request, "urlopen", network)

    with pytest.raises(SystemExit, match=DENIAL):
        drift.main()

    parse.assert_not_called()
    network.assert_not_called()


def test_alternate_folded_source_cannot_be_qualified(tmp_path, monkeypatch):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    (source / "FOLD.md").write_text("archive-bound\n", encoding="utf-8")

    monkeypatch.setattr(drift, "REPOSITORY_ROOT", checkout)
    with pytest.raises(SystemExit, match=DENIAL):
        drift.require_standalone_verification(source)


def test_unfolded_source_passes_only_the_local_verification_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(drift, "REPOSITORY_ROOT", tmp_path)
    drift.require_standalone_verification(tmp_path)


def test_repository_fold_marker_is_currently_present():
    assert (ROOT / "FOLD.md").is_file()
