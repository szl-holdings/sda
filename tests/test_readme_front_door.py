from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


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


def test_readme_keeps_evidence_and_operational_state_separate():
    for label in (
        "OPERATIONAL",
        "SOURCE BOUND",
        "NOT MEASURED",
        "MODELED",
        "CONJECTURE / ROADMAP",
    ):
        assert label in README

    assert "Λ remains Conjecture 1 and advisory" in README
    assert "effectors are simulated" in README
    assert "Receipt verification establishes integrity and origin" in README
    assert "does not establish prediction accuracy" in README


def test_readme_routes_builders_and_verifiers_to_native_evidence():
    for route in (
        "https://szlholdings-sda.hf.space/readyz",
        "https://szlholdings-sda.hf.space/api/build-info",
        "python server.py",
        "python -m pytest -q",
        "SPACE_PROVENANCE.json",
    ):
        assert route in README
