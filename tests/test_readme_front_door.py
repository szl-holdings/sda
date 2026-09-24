from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
PROVENANCE = json.loads((ROOT / "SPACE_PROVENANCE.json").read_text(encoding="utf-8"))


def test_readme_is_a_compact_investor_first_front_door():
    body = re.sub(r"\A---\s.*?\s---\s*", "", README, flags=re.DOTALL)
    words = re.findall(r"\b[\w’'-]+\b", re.sub(r"<[^>]+>", " ", body))

    assert len(words) <= 550
    assert body.index("# SDA") < body.index("## Mission brief")
    assert body.index("## Mission brief") < body.index("## Run locally")
    assert "img.shields.io" not in body
    assert not re.search(r"^\s*\|.+\|\s*$", body, flags=re.MULTILINE)


def test_readme_uses_the_shared_responsive_estate_banner():
    assert (
        "https://huggingface.co/spaces/SZLHOLDINGS/README/resolve/main/"
        "assets/estate-banner-v2.svg"
    ) in README
    assert 'width="100%"' in README
    assert not re.search(r'width="\d+px"', README)


def test_readme_marks_folded_authority_without_live_promotion_claims():
    for label in (
        "FOLDED / ARCHIVE-BOUND / NOT CANONICAL",
        "CANONICAL:",
        "NO STANDALONE PUBLICATION",
        "NO STANDALONE RUNTIME QUALIFICATION",
        "HISTORICAL SNAPSHOT",
        "MODELED:",
        "CONJECTURE / ROADMAP",
    ):
        assert label in README

    assert "https://github.com/szl-holdings/khipu-sda-core" in README
    assert "Λ remains Conjecture 1 and advisory" in README
    assert "Effectors are" in README
    assert "does not establish prediction accuracy" in README
    assert "**OPERATIONAL:**" not in README
    assert "**SOURCE BOUND:**" not in README
    assert "https://szlholdings-sda.hf.space/readyz" not in README
    assert "https://szlholdings-sda.hf.space/api/build-info" not in README


def test_historical_space_provenance_has_current_authority_qualifier():
    assert PROVENANCE["record_state"] == "HISTORICAL_SNAPSHOT_SUPERSEDED"
    assert PROVENANCE["observed_at"] == "2026-07-30T16:00:00Z"
    authority = PROVENANCE["current_authority"]
    assert authority["canonical_repository"] == (
        "https://github.com/szl-holdings/khipu-sda-core"
    )
    assert authority["standalone_publication"] == "DISABLED_BY_FOLD_MARKER"
    assert authority["standalone_runtime_qualification"] == "NOT_CURRENT_AUTHORITY"


def test_readme_preserves_local_inspection_and_native_evidence_routes():
    for route in (
        "python server.py",
        "python -m pytest -q",
        "SPACE_PROVENANCE.json",
        "FOLD.md",
    ):
        assert route in README
