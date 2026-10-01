"""Measure the deterministic find_nodes baseline on the committed intent set."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "geometry-nodes" / "scripts" / "find_nodes.py"
CASES_PATH = ROOT / "tests" / "fixtures" / "find_nodes_cases.json"


def _query_module():
    spec = importlib.util.spec_from_file_location("find_nodes", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(limit=5):
    query = _query_module()
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    hits = top1 = returned = irrelevant = 0
    details = []
    for case in cases:
        result = query.run({"query": case["query"], "version": case["version"], "limit": limit})
        ids = [candidate["bl_idname"] for candidate in result["candidates"]]
        relevant = set(case.get("relevant") or [case["target"]])
        hit = case["target"] in ids
        first = bool(ids and ids[0] == case["target"])
        hits += hit
        top1 += first
        returned += len(ids)
        irrelevant += sum(node_id not in relevant for node_id in ids)
        details.append({**case, "returned": ids, "hit": hit, "top1": first})
    return {
        "cases": len(cases),
        "limit": limit,
        "recall_at_limit": hits / len(cases),
        "top1_accuracy": top1 / len(cases),
        "irrelevant_result_rate": irrelevant / returned if returned else 0.0,
        "details": details,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
