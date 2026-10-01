from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "quality.yml"


def test_quality_workflow_exposes_the_two_public_gates():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "pull_request:" in text
    assert "push:" in text and "- main" in text
    assert "permissions:\n  contents: read" in text
    assert text.count("persist-credentials: false") == 2
    assert "name: Static tests" in text
    assert "python -m pip install -r requirements-dev.txt" in text
    assert "cache-dependency-path: requirements-dev.txt" in text
    assert "python -m pytest tests -q" in text
    assert "name: nodes.tsv consistency" in text
    assert "python tools/gen_nodes_tsv.py --check" in text


def test_quality_workflow_does_not_claim_live_host_acceptance():
    text = WORKFLOW.read_text(encoding="utf-8").lower()

    for forbidden in ("nodecue_blender", "blender.app", "release", "secrets."):
        assert forbidden not in text
