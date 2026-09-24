from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = (
    ROOT / ".github/workflows/ci.yml",
    ROOT / ".github/workflows/codeql.yml",
)


def test_pr_workflows_bind_and_prove_exact_source_revision():
    expected_env = (
        "SOURCE_REVISION: ${{ github.event.pull_request.head.sha || github.sha }}"
    )
    for workflow in WORKFLOWS:
        text = workflow.read_text(encoding="utf-8")
        assert expected_env in text, workflow
        assert "ref: ${{ env.SOURCE_REVISION }}" in text, workflow
        assert "persist-credentials: false" in text, workflow
        assert "git rev-parse HEAD" in text, workflow
        assert 'test "$actual" = "$SOURCE_REVISION"' in text, workflow
