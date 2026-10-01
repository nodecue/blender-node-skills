"""Find plausible Geometry Nodes from the reviewed routing index.

This is a deterministic candidate query, not a Blender identity authority. It
reads ``references/nodes.tsv``, filters by the requested Blender version, ranks
display/category/identifier/note text, and returns a short candidate list. Probe
every candidate in the running Blender with ``probe_node.py`` before wiring.

Invocation:

    python scripts/find_nodes.py -- '{"query": "scatter points on faces", "version": "5.2"}'

    import runpy
    result = runpy.run_path(
        SCRIPT, init_globals={"NODECUE_PARAMS": {"query": "curve to mesh"}}
    )["result"]

Parameters:
    query       required natural-language intent
    version     optional: 4.5, 5.0, 5.1, or 5.2
    limit       optional result count, default 5, maximum 20

The result is stable for identical TSV content and parameters. Match scores are
internal baseline evidence, not semantic certainty.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


TSV_PATH = Path(__file__).resolve().parents[1] / "references" / "nodes.tsv"
SUPPORTED_VERSIONS = ("4.5", "5.0", "5.1", "5.2")
STOP_WORDS = {"a", "an", "and", "by", "for", "from", "in", "into", "of", "on", "the", "to", "with"}
ALIASES = {
    "scatter": ("distribute", "points"),
    "surface": ("faces", "mesh"),
    "surfaces": ("faces", "mesh"),
    "objects": ("instance",),
    "object": ("instance",),
    "copies": ("instance",),
    "copy": ("instance",),
    "combine": ("join",),
    "distance": ("proximity",),
    "closest": ("nearest",),
    "remember": ("store",),
    "named": ("attribute",),
}


def _tokens(text):
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOP_WORDS]


def _query_terms(query):
    terms = []
    for token in _tokens(query):
        for term in (token, *ALIASES.get(token, ())):
            if term not in terms:
                terms.append(term)
    return terms


def _available(marker, version):
    if version is None:
        return True
    if marker.endswith("+"):
        return SUPPORTED_VERSIONS.index(version) >= SUPPORTED_VERSIONS.index(marker[:-1])
    if marker.endswith("-only"):
        return version == marker[:-5]
    return False


def _rows():
    with TSV_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _score(row, query, terms):
    display_text = " ".join(_tokens(row["display_name"]))
    display = set(_tokens(row["display_name"]))
    category = set(_tokens(row["category"]))
    identifier = set(_tokens(row["bl_idname"]))
    note = set(_tokens(row["note"]))
    normalized_query = " ".join(_tokens(query))

    score = 0
    reasons = []
    if normalized_query and normalized_query == display_text:
        score += 1000
        reasons.append("exact display name")
    elif normalized_query and normalized_query in display_text:
        score += 250
        reasons.append("display phrase")

    for term in terms:
        if term in display:
            score += 30
            reasons.append(f"display:{term}")
        elif term in category:
            score += 12
            reasons.append(f"category:{term}")
        elif term in identifier:
            score += 8
            reasons.append(f"identifier:{term}")
        elif term in note:
            score += 3
            reasons.append(f"note:{term}")
    return score, reasons


def run(params=None):
    params = params or {}
    query = str(params.get("query") or "").strip()
    if not query:
        return {"ok": False, "error": "pass a non-empty `query`"}

    version = params.get("version")
    if version is not None:
        version = str(version)
        if version not in SUPPORTED_VERSIONS:
            return {
                "ok": False,
                "error": f"unsupported version {version!r}",
                "versions": list(SUPPORTED_VERSIONS),
            }

    try:
        limit = int(params.get("limit", 5))
    except (TypeError, ValueError):
        return {"ok": False, "error": "`limit` must be an integer from 1 to 20"}
    if not 1 <= limit <= 20:
        return {"ok": False, "error": "`limit` must be an integer from 1 to 20"}

    terms = _query_terms(query)
    ranked = []
    for row in _rows():
        if not _available(row["version"], version):
            continue
        score, reasons = _score(row, query, terms)
        if score:
            ranked.append((score, row["display_name"].lower(), row["bl_idname"], row, reasons))
    ranked.sort(key=lambda item: (-item[0], item[1], item[2]))

    candidates = []
    for score, _display_sort, _id_sort, row, reasons in ranked[:limit]:
        candidates.append({
            "bl_idname": row["bl_idname"],
            "display_name": row["display_name"],
            "category": row["category"],
            "version": row["version"],
            "note": row["note"] or None,
            "score": score,
            "matched": reasons,
        })

    return {
        "ok": True,
        "query": query,
        "version": version,
        "limit": limit,
        "terms": terms,
        "candidates": candidates,
        "authority": "routing candidates only; live Blender is authoritative",
        "next": "probe candidate bl_idnames in the running Blender before wiring sockets or setting properties",
    }


def _emit(payload):
    print(json.dumps(payload, ensure_ascii=False))
    return payload


def _argv_params():
    if "--" not in sys.argv:
        return {}
    rest = sys.argv[sys.argv.index("--") + 1:]
    return json.loads(rest[0]) if rest else {}


if __name__ == "__main__":
    result = _emit(run(_argv_params()))
elif "NODECUE_PARAMS" in globals():
    result = run(NODECUE_PARAMS)  # noqa: F821 - injected by the host
