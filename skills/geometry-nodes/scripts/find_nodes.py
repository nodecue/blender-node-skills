"""Find plausible Geometry Nodes from the reviewed routing index.

This is a deterministic candidate query, not a Blender identity authority. It
reads ``references/nodes.tsv``, filters by the requested Blender version, ranks
display/category/identifier/note text, and returns a short candidate list. Probe
every candidate in the running Blender with ``probe_node.py`` before wiring.

Ranking is lexical: tokens are singularized (edges -> edge, vertices -> vertex),
rare terms weigh more than common ones (IDF over the TSV), a candidate whose
whole display name is covered by the query gets a bonus, and a small explicit
alias table maps common wording to Blender vocabulary. Ties break by fraction of
display-name tokens matched, display hit count, then alphabetically.

Invocation (JSON is the first positional argument, with or without ``--``):

    python scripts/find_nodes.py '{"query": "scatter points on faces", "version": "5.2"}'
    python scripts/find_nodes.py -- '{"queries": ["raycast", "store named attribute"]}'

    import runpy
    result = runpy.run_path(
        SCRIPT, init_globals={"NODECUE_PARAMS": {"query": "curve to mesh"}}
    )["result"]

Parameters (pass `query` or `queries`, not both):
    query       natural-language intent; one ranked `candidates` list
    queries     list of up to 12 intents; returns `results: [{query, candidates}]`
                with its own top-k per intent. Prefer this for multi-step tasks:
                one short query per intent ranks better than one long mixed query.
    version     optional: 4.5, 5.0, 5.1, or 5.2
    limit       optional result count (per intent), default 5, maximum 20

When nothing matches, `ok` stays true, candidates are empty, and `hint` says to
rephrase with Blender vocabulary or grep `references/nodes.tsv`.

The result is stable for identical TSV content and parameters. Match scores are
internal baseline evidence, not semantic certainty.
"""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path


TSV_PATH = Path(__file__).resolve().parents[1] / "references" / "nodes.tsv"
SUPPORTED_VERSIONS = ("4.5", "5.0", "5.1", "5.2")
MAX_QUERIES = 12
STOP_WORDS = {"a", "an", "and", "by", "for", "from", "in", "into", "of", "on", "the", "to", "with"}
IRREGULAR_PLURALS = {"vertices": "vertex", "indices": "index", "matrices": "matrix", "axes": "axis"}
# Keys are normalized (singular) token tuples; every target must be a real term in
# nodes.tsv. Keep this table small and reviewed. Do not alias `object`: it pushed
# Instance Transform above Object Info.
ALIASES = {
    ("scatter",): ("distribute", "point"),
    ("surface",): ("face", "mesh"),
    ("copy",): ("instance",),
    ("combine",): ("join",),
    ("distance",): ("proximity",),
    ("closest",): ("nearest",),
    ("remember",): ("store",),
    ("named",): ("attribute",),
    ("ray",): ("raycast",),
    ("ray", "cast"): ("raycast",),
    ("weld",): ("merge", "distance"),
    ("merge", "vertex"): ("distance",),
    ("merge", "point"): ("distance",),
    ("if",): ("switch",),
    ("else",): ("switch",),
    ("choose",): ("switch",),
    ("select", "between"): ("switch",),
    ("silhouette",): ("neighbor", "edge"),
    ("outline",): ("neighbor", "edge"),
    ("border",): ("neighbor", "edge"),
    ("boundary",): ("neighbor",),
    ("camera", "space"): ("transform", "point"),
    ("world", "space"): ("transform", "point"),
    ("local", "space"): ("transform", "point"),
    ("world", "local"): ("transform", "point"),
}
RARE_IDF = 6.0
FIELD_WEIGHTS = (("display", 30), ("category", 12), ("identifier", 8), ("note", 3))
EMPTY_HINT = (
    "no candidates: rephrase with Blender node vocabulary (one intent per query, "
    "or use `queries`), or grep references/nodes.tsv"
)
USAGE = "expected JSON as the first argument: python find_nodes.py '{\"query\": \"curve to mesh\"}'"


def _singular(token):
    if token in IRREGULAR_PLURALS:
        return IRREGULAR_PLURALS[token]
    if len(token) < 4 or token.endswith(("ss", "us", "is")):
        return token
    if token.endswith("ies"):
        return token[:-3] + "y"
    if token.endswith(("ches", "shes", "xes")):
        return token[:-2]
    if token.endswith("s"):
        return token[:-1]
    return token


def _tokens(text):
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return [_singular(token) for token in re.findall(r"[a-z0-9]+", text.lower())
            if token not in STOP_WORDS]


def _query_terms(query):
    tokens = _tokens(query)
    terms = []
    for token in tokens:
        if token not in terms:
            terms.append(token)
    present = set(tokens)
    for key, targets in ALIASES.items():
        # phrase keys match when every word is present, in any order or distance
        if present.issuperset(key):
            terms.extend(term for term in targets if term not in terms)
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


_INDEX = []


def _index():
    """Rows with pre-tokenized fields plus IDF weights over the whole TSV (cached)."""
    if not _INDEX:
        _INDEX.append(_build_index())
    return _INDEX[0]


def _build_index():
    entries = []
    document_frequency = {}
    for row in _rows():
        display_list = _tokens(row["display_name"])
        fields = {
            "display": set(display_list),
            "category": set(_tokens(row["category"])),
            "identifier": set(_tokens(row["bl_idname"])),
            "note": set(_tokens(row["note"])),
        }
        for token in set().union(*fields.values()):
            document_frequency[token] = document_frequency.get(token, 0) + 1
        entries.append((row, display_list, fields))
    total = len(entries)
    idf = {token: math.log(total / count) + 1.0 for token, count in document_frequency.items()}
    return entries, idf


def _score(display_list, fields, idf, query, terms):
    display_text = " ".join(display_list)
    normalized_query = " ".join(_tokens(query))
    term_set = set(terms)

    score = 0.0
    reasons = []
    if normalized_query and normalized_query == display_text:
        score += 1000
        reasons.append("exact display name")
    elif normalized_query and normalized_query in display_text:
        score += 250
        reasons.append("display phrase")

    display = fields["display"]
    # display hits are normalized by name length so multi-word names do not
    # outscore a short exact name just by having more tokens
    display_scale = len(display) ** 0.5 if display else 1.0
    for term in terms:
        for field, weight in FIELD_WEIGHTS:
            if term in fields[field]:
                scale = display_scale if field == "display" else 1.0
                score += weight * idf.get(term, 1.0) / scale
                reasons.append(f"{field}:{term}")
                break

    matched_display = display & term_set
    if display and score and display <= term_set:
        # the whole display name is named by the query: reward it
        bonus = 60 * sum(idf.get(token, 1.0) for token in display) / len(display)
        if len(display) == 1 and idf.get(next(iter(display)), 1.0) < RARE_IDF:
            bonus *= 0.4  # a common single word (Points, Object) is weak evidence
        score += bonus
        reasons.append("covers name")
    coverage = len(matched_display) / len(display) if display else 0.0
    return score, reasons, coverage, len(matched_display)


def _rank(query, version, limit):
    entries, idf = _index()
    terms = _query_terms(query)
    ranked = []
    for row, display_list, fields in entries:
        if not _available(row["version"], version):
            continue
        score, reasons, coverage, display_hits = _score(display_list, fields, idf, query, terms)
        if score:
            ranked.append((-round(score, 3), -coverage, -display_hits,
                           row["display_name"].lower(), row["bl_idname"], row, reasons))
    ranked.sort(key=lambda item: item[:5])

    candidates = []
    for neg_score, _cov, _hits, _display_sort, _id_sort, row, reasons in ranked[:limit]:
        candidates.append({
            "bl_idname": row["bl_idname"],
            "display_name": row["display_name"],
            "category": row["category"],
            "version": row["version"],
            "note": row["note"] or None,
            "score": round(-neg_score, 1),
            "matched": reasons,
        })
    return terms, candidates


def run(params=None):
    params = params or {}
    query = str(params.get("query") or "").strip()
    queries = params.get("queries")
    if query and queries is not None:
        return {"ok": False, "error": "pass either `query` or `queries`, not both"}
    if queries is not None:
        if (not isinstance(queries, list) or not queries
                or not all(isinstance(item, str) and item.strip() for item in queries)):
            return {"ok": False, "error": "`queries` must be a non-empty list of non-empty strings"}
        if len(queries) > MAX_QUERIES:
            return {"ok": False, "error": f"`queries` accepts at most {MAX_QUERIES} intents"}
        queries = [item.strip() for item in queries]
    elif not query:
        return {"ok": False, "error": "pass a non-empty `query` (or a `queries` list)"}

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

    authority = "routing candidates only; live Blender is authoritative"
    next_step = "probe candidate bl_idnames in the running Blender before wiring sockets or setting properties"

    if queries is not None:
        results = []
        for item in queries:
            _terms, candidates = _rank(item, version, limit)
            entry = {"query": item, "candidates": candidates}
            if not candidates:
                entry["hint"] = EMPTY_HINT
            results.append(entry)
        return {
            "ok": True,
            "version": version,
            "limit": limit,
            "results": results,
            "authority": authority,
            "next": next_step,
        }

    terms, candidates = _rank(query, version, limit)
    result = {
        "ok": True,
        "query": query,
        "version": version,
        "limit": limit,
        "terms": terms,
        "candidates": candidates,
    }
    if not candidates:
        result["hint"] = EMPTY_HINT
    result["authority"] = authority
    result["next"] = next_step
    return result


def _emit(payload):
    print(json.dumps(payload, ensure_ascii=False))
    return payload


def _argv_params():
    """Return (params, error); JSON is the first positional arg, with or without `--`."""
    args = sys.argv[1:]
    if "--" in args:
        args = args[args.index("--") + 1:]
    if not args:
        return {}, USAGE
    try:
        params = json.loads(args[0])
    except json.JSONDecodeError:
        return {}, f"argument is not valid JSON; {USAGE}"
    if not isinstance(params, dict):
        return {}, f"argument must be a JSON object; {USAGE}"
    return params, None


def _main():
    params, error = _argv_params()
    return _emit({"ok": False, "error": error} if error else run(params))


if __name__ == "__main__":
    result = _main()
elif "NODECUE_PARAMS" in globals():
    result = run(NODECUE_PARAMS)  # noqa: F821 - injected by the host
