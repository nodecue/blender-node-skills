"""Measure the deterministic find_nodes baseline on the committed intent set.

Cases carry a ``kind``: ``echo`` (query mostly repeats the display name) or
``agent`` (wording an agent would naturally use). Metrics are reported for the
whole set and per kind. ``--script PATH`` evaluates another copy of the script,
for before/after comparisons.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "geometry-nodes" / "scripts" / "find_nodes.py"
CASES_PATH = ROOT / "tests" / "fixtures" / "find_nodes_cases.json"


def _query_module(script=SCRIPT):
    spec = importlib.util.spec_from_file_location("find_nodes", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _summarize(details, limit):
    returned = sum(len(item["returned"]) for item in details)
    irrelevant = sum(item["irrelevant"] for item in details)
    count = len(details)
    return {
        "cases": count,
        "limit": limit,
        "recall_at_limit": sum(item["hit"] for item in details) / count if count else 0.0,
        "top1_accuracy": sum(item["top1"] for item in details) / count if count else 0.0,
        "irrelevant_result_rate": irrelevant / returned if returned else 0.0,
    }


def evaluate(limit=5, script=SCRIPT):
    query = _query_module(script)
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    details = []
    for case in cases:
        result = query.run({"query": case["query"], "version": case["version"], "limit": limit})
        ids = [candidate["bl_idname"] for candidate in result["candidates"]]
        relevant = set(case.get("relevant") or [case["target"]])
        details.append({
            **case,
            "returned": ids,
            "hit": case["target"] in ids,
            "top1": bool(ids and ids[0] == case["target"]),
            "irrelevant": sum(node_id not in relevant for node_id in ids),
        })
    summary = _summarize(details, limit)
    summary["by_kind"] = {
        kind: _summarize([item for item in details if item["kind"] == kind], limit)
        for kind in sorted({item["kind"] for item in details})
    }
    summary["details"] = details
    return summary


if __name__ == "__main__":
    args = sys.argv[1:]
    path = Path(args[args.index("--script") + 1]) if "--script" in args else SCRIPT
    report = evaluate(script=path)
    if "--brief" in args:
        report["details"] = [d for d in report["details"] if not d["hit"] or not d["top1"]]
    print(json.dumps(report, ensure_ascii=False, indent=2))
