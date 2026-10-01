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
    assert baseline["cases"] == 36
    assert baseline["recall_at_limit"] == pytest.approx(35 / 36)
    assert baseline["top1_accuracy"] == pytest.approx(33 / 36)
    assert baseline["irrelevant_result_rate"] == pytest.approx(124 / 178)

    # display-name echoes (the original 15) versus agent-style wording
    echo = baseline["by_kind"]["echo"]
    assert (echo["cases"], echo["recall_at_limit"], echo["top1_accuracy"]) == (15, 1.0, 1.0)
    assert echo["irrelevant_result_rate"] == pytest.approx(51 / 75)
    agent = baseline["by_kind"]["agent"]
    assert agent["cases"] == 21
    assert agent["recall_at_limit"] == pytest.approx(20 / 21)
    assert agent["top1_accuracy"] == pytest.approx(18 / 21)
    assert agent["irrelevant_result_rate"] == pytest.approx(73 / 103)


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


def _ids(result):
    return [candidate["bl_idname"] for candidate in result["candidates"]]


def _cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], check=True, capture_output=True, text=True
    )


def test_cli_accepts_positional_json_with_or_without_separator():
    payload = json.dumps({"query": "join geometry"})
    for args in ((payload,), ("--", payload)):
        document = json.loads(_cli(*args).stdout)
        assert document["ok"] is True
        assert document["candidates"][0]["bl_idname"] == "GeometryNodeJoinGeometry"


def test_cli_invalid_json_reports_expected_invocation():
    for args in (("not json",), ("--", "{bad"), ("[1]",), ()):
        document = json.loads(_cli(*args).stdout)
        assert document["ok"] is False
        assert "find_nodes.py" in document["error"]
        assert "non-empty" not in document["error"]


def test_queries_returns_per_intent_candidates_with_own_limit():
    intents = ["raycast", "store named attribute", "object info", "bounding box"]
    result = find_nodes.run({"queries": intents, "limit": 3})
    assert result["ok"] and "candidates" not in result
    assert [entry["query"] for entry in result["results"]] == intents
    assert all(len(entry["candidates"]) <= 3 for entry in result["results"])
    assert "live Blender" in result["authority"] and "probe" in result["next"]
    firsts = [_ids({"candidates": entry["candidates"]})[0] for entry in result["results"]]
    assert firsts == [
        "GeometryNodeRaycast",
        "GeometryNodeStoreNamedAttribute",
        "GeometryNodeObjectInfo",
        "GeometryNodeBoundBox",
    ]


def test_queries_validation():
    assert find_nodes.run({"queries": []})["ok"] is False
    assert find_nodes.run({"queries": ["ok", ""]})["ok"] is False
    assert find_nodes.run({"queries": "raycast"})["ok"] is False
    assert find_nodes.run({"queries": ["a"] * (find_nodes.MAX_QUERIES + 1)})["ok"] is False
    assert find_nodes.run({"query": "raycast", "queries": ["raycast"]})["ok"] is False


def test_long_multi_intent_query_still_surfaces_raycast():
    long_query = (
        "raycast mesh boundary shortest edge paths store named attribute object info "
        "transform point curve length bounding box"
    )
    result = find_nodes.run({"query": long_query, "limit": 5})
    assert "GeometryNodeRaycast" in _ids(result)
    split = find_nodes.run({"queries": long_query.split(" mesh ")[0:1] + [
        "boundary shortest edge paths", "store named attribute",
        "object info transform", "point curve length bounding box"]})
    assert _ids(split["results"][0])[0] == "GeometryNodeRaycast"


def test_plural_and_irregular_forms_normalize_to_the_same_terms():
    for plural, singular in [("edges", "edge"), ("vertices", "vertex"), ("points", "point"),
                             ("faces", "face"), ("curves", "curve"), ("instances", "instance"),
                             ("meshes", "mesh"), ("boundaries", "boundary"), ("matrices", "matrix")]:
        assert find_nodes._tokens(plural) == find_nodes._tokens(singular) == [singular]
    assert _ids(find_nodes.run({"query": "realize instances"}))[0] == "GeometryNodeRealizeInstances"
    assert (_ids(find_nodes.run({"query": "edges of vertices"}))
            == _ids(find_nodes.run({"query": "edge of vertex"})))


def test_object_is_not_aliased_to_instance():
    assert "instance" not in find_nodes._query_terms("object info")
    ids = _ids(find_nodes.run({"query": "object info", "limit": 20}))
    assert ids[0] == "GeometryNodeObjectInfo"
    assert "GeometryNodeInstanceTransform" not in ids[:5]


def test_alias_targets_exist_in_the_index():
    vocabulary = set()
    for _row, _display, fields in find_nodes._index()[0]:
        for tokens in fields.values():
            vocabulary |= tokens
    for key, targets in find_nodes.ALIASES.items():
        assert all(target in vocabulary for target in targets), key


def test_empty_result_returns_ok_with_hint():
    single = find_nodes.run({"query": "zzzqqq"})
    assert single["ok"] is True and single["candidates"] == []
    assert "nodes.tsv" in single["hint"]
    multi = find_nodes.run({"queries": ["zzzqqq", "raycast"]})
    assert "hint" in multi["results"][0] and "hint" not in multi["results"][1]


def test_ties_prefer_fuller_display_name_matches_then_alphabetical():
    # "weld vertices" names Merge by Distance in full; it must outrank partial hits
    assert _ids(find_nodes.run({"query": "weld vertices", "limit": 1})) == ["GeometryNodeMergeByDistance"]
    first = find_nodes.run({"query": "mesh edge point curve", "limit": 20})
    assert first == find_nodes.run({"query": "mesh edge point curve", "limit": 20})
