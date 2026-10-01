"""Measured deterministic baseline for the agent-facing node query."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import runpy
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "geometry-nodes" / "scripts" / "find_nodes.py"
EVALUATOR = ROOT / "tools" / "eval_find_nodes.py"
CASES = json.loads((ROOT / "tests" / "fixtures" / "find_nodes_cases.json").read_text())


def _module():
    spec = importlib.util.spec_from_file_location("find_nodes", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


find_nodes = _module()


def _evaluator():
    spec = importlib.util.spec_from_file_location("eval_find_nodes", EVALUATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixed_intent_set_recall_at_five_and_irrelevant_rate():
    baseline = _evaluator().evaluate(limit=5)
    assert baseline["cases"] == 15
    assert baseline["recall_at_limit"] == 1.0
    assert baseline["top1_accuracy"] == 1.0
    assert baseline["irrelevant_result_rate"] == pytest.approx(2 / 3)


def test_version_filter_never_returns_an_unavailable_node():
    rows = {row["bl_idname"]: row for row in find_nodes._rows()}
    for version in find_nodes.SUPPORTED_VERSIONS:
        result = find_nodes.run({"query": "list string geometry attribute", "version": version, "limit": 20})
        assert result["ok"]
        assert all(find_nodes._available(rows[c["bl_idname"]]["version"], version)
                   for c in result["candidates"])

    old = find_nodes.run({"query": "mesh bevel", "version": "5.1", "limit": 20})
    assert "GeometryNodeMeshBevel" not in [c["bl_idname"] for c in old["candidates"]]
    new = find_nodes.run({"query": "mesh bevel", "version": "5.2", "limit": 20})
    assert "GeometryNodeMeshBevel" in [c["bl_idname"] for c in new["candidates"]]


def test_identical_queries_are_stable():
    params = {"query": "scatter objects across a mesh surface", "version": "5.2", "limit": 7}
    assert find_nodes.run(params) == find_nodes.run(params)


def test_result_keeps_live_blender_as_authority():
    result = find_nodes.run({"query": "capture attribute"})
    assert "live Blender" in result["authority"]
    assert "probe" in result["next"]
    forbidden = {"inputs", "outputs", "properties", "sockets"}
    assert all(not (forbidden & candidate.keys()) for candidate in result["candidates"])


def test_contract_rejects_invalid_parameters():
    assert find_nodes.run({})["ok"] is False
    assert find_nodes.run({"query": "cube", "version": "6.0"})["ok"] is False
    assert find_nodes.run({"query": "cube", "limit": 0})["ok"] is False
    assert find_nodes.run({"query": "cube", "limit": 21})["ok"] is False


def test_runpy_is_silent_and_cli_emits_one_document():
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        namespace = runpy.run_path(
            str(SCRIPT), init_globals={"NODECUE_PARAMS": {"query": "curve to mesh"}}
        )
    assert stream.getvalue() == ""
    assert namespace["result"]["candidates"][0]["bl_idname"] == "GeometryNodeCurveToMesh"

    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--", json.dumps({"query": "join geometry"})],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    assert len(lines) == 1
    assert json.loads(lines[0])["candidates"][0]["bl_idname"] == "GeometryNodeJoinGeometry"
