"""Generate `references/nodes.tsv` from the versioned dumps plus reviewed metadata.

The TSV is a routing index, not a socket authority: it answers "which nodes are
worth introspecting for this intent", and live Blender answers everything else.
So every column here is either mechanical evidence or an explicitly reviewed
decision, and the manifest says which each row got.

Sources, all under `docs/node-dumps/`:

* `gn-<version>.json` — one per supported version, from `tools/introspect_nodes.py`.
  Decides which identifiers exist, their display names, and the `version` marker.
* `tsv-evidence-<version>.json` — from `tools/dump_tsv_evidence.py`. Carries the two
  facts the identity dumps do not: field socket display shapes, and Blender's own
  Add-menu category.

Reviewed decisions live in `tools/nodes_tsv_review.json`: exclusions, categories for
nodes Blender's Add menu does not list, a choice where a node sits in several menus,
and the sparse `note` values. Those are proposals until an owner approves them.

    python tools/gen_nodes_tsv.py                 # write the TSV and the manifest
    python tools/gen_nodes_tsv.py --check         # fail if either is out of date

`--check` is the idempotence gate: generating twice from the same evidence must
produce no diff.

## Socket display shape evidence is compared, reported, and not shipped

The TSV has no `field_io` column. Socket display shapes from `tsv-evidence-*.json`
are compared across versions and recorded in the manifest. Display shape changes
do not prove functional capability changes, and identical shapes do not prove identical
behavior. Live Blender remains authoritative at wiring time:

* `nodes.tsv` — find candidate nodes.
* `versions.md` — cross-version guidance.
* `probe_node.py` / `read_graph.py` — live socket state on the connected Blender.

`display_shape` is the mechanical source from evidence dumps:

| | shapes seen |
|---|---|
| 4.x | `CIRCLE`, `DIAMOND_DOT`, `DIAMOND` |
| 5.x | `LINE`, `CIRCLE`, `DIAMOND`, `VOLUME_GRID`, `LIST` |

The 4.x and 5.x draw vocabularies are not directly comparable. Shapes are compared
within each generation (such as 5.0 vs 5.1 vs 5.2), and the cross-generation boundary
is reported as transition counts. Shape changes do not prove capability changes, and
identical shapes do not prove identical capability.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DUMPS_DIR = ROOT / "docs" / "node-dumps"
REVIEW_PATH = ROOT / "tools" / "nodes_tsv_review.json"
TSV_PATH = ROOT / "skills" / "geometry-nodes" / "references" / "nodes.tsv"
MANIFEST_PATH = DUMPS_DIR / "nodes-tsv-manifest.md"

HEADER = ["bl_idname", "display_name", "category", "version", "note"]
VERSION_ORDER = ["4.5", "5.0", "5.1", "5.2"]
IDENTITY_DUMPS = {
    "4.5": "gn-4.5.12.json",
    "5.0": "gn-5.0.1.json",
    "5.1": "gn-5.1.2.json",
    "5.2": "gn-5.2.0.json",
}
# Keyed by **supported version**, matched by prefix. Blender's LTS identity is the
# second number: 4.5.13 is the same supported version as 4.5.12, and the third number
# is a maintenance release. So the glob finds whichever maintenance build was measured
# and a bump needs no code change. Measured 2026-09-02: 4.5.13 reports the same 297
# node types, socket shapes and menu paths as 4.5.12, byte for byte.
#
# A supported version whose file is absent is reported as an evidence gap in the
# manifest rather than interpolated from its neighbours - this repository has already
# shipped errors from interpolating across a version hole.
EVIDENCE_GLOBS = {v: f"tsv-evidence-{v}.*.json" for v in VERSION_ORDER}


def available_evidence() -> dict[str, str]:
    """The evidence dump on disk per supported version, keyed by supported version."""
    found = {}
    for version, pattern in EVIDENCE_GLOBS.items():
        matches = sorted(p.name for p in DUMPS_DIR.glob(pattern))
        if len(matches) > 1:
            raise GenerationError(
                f"{len(matches)} evidence dumps for supported version {version}: "
                f"{matches}. Keep one - the maintenance build that was measured."
            )
        if matches:
            found[version] = matches[0]
    return found

# See the module docstring. Keyed by the shape vocabulary a dump actually uses, so
# a re-dump of any version resolves itself rather than trusting a version string.
# Values are comparable inside a generation and not across one. See the docstring.
COMPARABLE_WITHIN_VOCABULARY = True
KNOWN_SHAPES = {"LINE", "CIRCLE", "DIAMOND", "DIAMOND_DOT", "VOLUME_GRID", "LIST"}


class GenerationError(Exception):
    """Raised when evidence cannot produce a defensible row."""


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# --- version -----------------------------------------------------------------
def version_marker(present: set[str]) -> str:
    idx = [i for i, v in enumerate(VERSION_ORDER) if v in present]
    if not idx:
        raise GenerationError("node present in no dump")
    contiguous = idx == list(range(idx[0], idx[-1] + 1))
    if not contiguous:
        return ",".join(VERSION_ORDER[i] for i in idx)
    if idx[-1] == len(VERSION_ORDER) - 1:
        return f"{VERSION_ORDER[idx[0]]}+"
    if idx[0] == idx[-1]:
        return f"{VERSION_ORDER[idx[0]]}-only"
    return f"{VERSION_ORDER[idx[0]]}-{VERSION_ORDER[idx[-1]]}"


# --- socket shape comparison (manifest only) ---------------------------------
def detect_vocabulary(evidence: dict) -> str:
    shapes = {
        shape
        for rec in evidence["field_shapes"].values()
        for shape in list(rec["in"].values()) + list(rec["out"].values())
    }
    if "LINE" in shapes:
        return "5.x"
    if "DIAMOND_DOT" in shapes:
        return "4.x"
    raise GenerationError(f"unrecognised socket shape vocabulary: {sorted(shapes)}")


# --- generation ---------------------------------------------------------------
def build(strict_unresolved: bool = True) -> tuple[list[list[str]], dict]:
    identity = {v: _load(DUMPS_DIR / name) for v, name in IDENTITY_DUMPS.items()}
    evidence_files = available_evidence()
    evidence = {v: _load(DUMPS_DIR / name) for v, name in evidence_files.items()}
    review = _load(REVIEW_PATH)

    vocabularies = {v: detect_vocabulary(e) for v, e in evidence.items()}
    groups: dict[str, list[str]] = {}
    for v in sorted(vocabularies, key=VERSION_ORDER.index):
        groups.setdefault(vocabularies[v], []).append(v)
    nodes = {v: d["nodes"] for v, d in identity.items()}
    exclusions = review.get("exclusions") or {}
    union = sorted(set().union(*(set(n) for n in nodes.values())) - set(exclusions))

    report = {
        "sources": {
            **{f"identity/{v}": {"file": n, "sha256_16": _sha(DUMPS_DIR / n),
                                 "blender": identity[v]["blender"], "nodes": len(nodes[v])}
               for v, n in IDENTITY_DUMPS.items()},
            **{f"evidence/{v}": {"file": n, "sha256_16": _sha(DUMPS_DIR / n),
                                 "blender": evidence[v]["blender"],
                                 "vocabulary": vocabularies[v],
                                 "creatable": evidence[v]["creatable"]}
               for v, n in evidence_files.items()},
            "review": {"file": REVIEW_PATH.name, "sha256_16": _sha(REVIEW_PATH)},
        },
        "identifier_counts": {v: len(n) for v, n in nodes.items()},
        "union": len(union),
        "exclusions": exclusions,
        "evidence_versions": sorted(evidence_files, key=VERSION_ORDER.index),
        "missing_evidence_versions": sorted(set(IDENTITY_DUMPS) - set(evidence_files),
                                            key=VERSION_ORDER.index),
        "identity_vs_evidence": {},
        "label_changes": {},
        "category_source": {},
        "category_reviewed": {},
        "category_unresolved": [],
        "field_conflicts": {},
        "field_missing": [],
        "field_compared": {"nodes": 0, "sockets": 0, "socket_set_changes": 0,
                           "vocabulary_groups": {}},
        "field_vocabulary_boundary": {},
        "notes": {},
        "version_markers": {},
    }

    # The identity dump and the evidence dump for one version must describe the
    # same creatable set, or one of them is stale.
    for v in evidence_files:
        only_identity = sorted(set(nodes[v]) - set(evidence[v]["field_shapes"]))
        only_evidence = sorted(set(evidence[v]["field_shapes"]) - set(nodes[v]))
        builds_differ = identity[v]["blender"] != evidence[v]["blender"]
        if only_identity or only_evidence or builds_differ:
            report["identity_vs_evidence"][v] = {
                "identity_blender": identity[v]["blender"],
                "evidence_blender": evidence[v]["blender"],
                "only_in_identity": only_identity,
                "only_in_evidence": only_evidence,
                "sets_agree": not (only_identity or only_evidence),
            }

    reviewed_categories = review.get("categories") or {}
    ambiguous_choice = review.get("ambiguous_category_choice") or {}
    reviewed_notes = review.get("notes") or {}

    rows = []
    for bl_idname in union:
        present = {v for v in VERSION_ORDER if bl_idname in nodes[v]}

        labels = {v: nodes[v][bl_idname].get("label", "") for v in VERSION_ORDER if v in present}
        newest = max(present, key=VERSION_ORDER.index)
        display_name = labels[newest]
        if len(set(labels.values())) > 1:
            report["label_changes"][bl_idname] = labels

        marker = version_marker(present)
        report["version_markers"].setdefault(marker, 0)
        report["version_markers"][marker] += 1

        category = _category(bl_idname, present, evidence, reviewed_categories,
                             ambiguous_choice, report)
        # Compared, reported, and deliberately not shipped. See _field_capability.
        _field_capability(bl_idname, present, evidence, vocabularies, groups, report)

        note = ""
        if bl_idname in reviewed_notes:
            entry = reviewed_notes[bl_idname]
            note = entry["note"] if isinstance(entry, dict) else entry
            report["notes"][bl_idname] = entry

        rows.append([bl_idname, display_name, category, marker, note])

    if strict_unresolved and report["category_unresolved"]:
        raise GenerationError(
            "unresolved categories (add them to nodes_tsv_review.json categories): "
            + ", ".join(report["category_unresolved"])
        )
    report["field_compared"]["vocabulary_groups"] = groups
    _validate(rows)
    return rows, report


def _category(bl_idname, present, evidence, reviewed, ambiguous_choice, report):
    for v in sorted(present & set(evidence), key=VERSION_ORDER.index, reverse=True):
        entries = evidence[v]["menu_paths"].get(bl_idname)
        if not entries:
            continue
        if len(entries) > 1:
            choice = ambiguous_choice.get(bl_idname)
            if not choice:
                report["category_unresolved"].append(bl_idname)
                return ""
            report["category_reviewed"][bl_idname] = {
                "category": choice["category"],
                "reason": choice["reason"],
                "kind": "ambiguous menu placement",
                "menus": [e["category"] for e in entries],
            }
            return choice["category"]
        report["category_source"][bl_idname] = {
            "version": v, "source": entries[0]["source"], "category": entries[0]["category"]
        }
        return entries[0]["category"]

    if bl_idname in reviewed:
        rec = reviewed[bl_idname]
        report["category_reviewed"][bl_idname] = {**rec, "kind": "absent from every Add menu"}
        return rec["category"]

    report["category_unresolved"].append(bl_idname)
    return ""


def _field_capability(bl_idname, present, evidence, vocabularies, groups, report):
    """Compare socket-level Field capability across versions. Maintainer evidence only.

    This does not become a TSV column, and it is not rolled up per node on the way
    out. Three files would otherwise answer the same question with three accuracies:
    `nodes.tsv` finds candidates, `versions.md` carries the few cross-version
    capability changes worth planning around, and `probe_node.py` reads the current
    node mode and this socket on the connected Blender. Only the last is right at
    wiring time.
    """
    per_version = {}
    for v in sorted(present & set(evidence), key=VERSION_ORDER.index):
        record = evidence[v]["field_shapes"].get(bl_idname)
        if record is None:
            continue
        per_version[v] = {
            side: {
                identifier: shape
                for identifier, shape in record[side].items()
            }
            for side in ("in", "out")
        }
    if not per_version:
        report["field_missing"].append(bl_idname)
        return

    report["field_compared"]["nodes"] += 1
    conflicts = {}
    boundary = report["field_vocabulary_boundary"]
    for side in ("in", "out"):
        identifiers = sorted({i for pv in per_version.values() for i in pv[side]})
        for identifier in identifiers:
            values = {
                v: pv[side][identifier]
                for v, pv in per_version.items()
                if identifier in pv[side]
            }
            report["field_compared"]["sockets"] += 1
            if len(values) != len(per_version):
                # The socket itself came or went. That is a socket-set change, which
                # the identity dumps and their diffs already carry; not a capability
                # change, and not this report's job.
                report["field_compared"]["socket_set_changes"] += 1

            # Compare only inside one shape vocabulary. Across the 4.x/5.x boundary
            # the shapes do not mean the same thing, so a difference there is not
            # evidence of anything - it is counted as boundary noise instead.
            for versions in groups.values():
                inside = {v: values[v] for v in versions if v in values}
                if len(set(inside.values())) > 1:
                    conflicts.setdefault(side, {})[identifier] = values
            per_group = {
                vocab: {values[v] for v in versions if v in values}
                for vocab, versions in groups.items()
            }
            settled = {
                vocab: next(iter(vals)) for vocab, vals in per_group.items()
                if len(vals) == 1
            }
            if len(settled) > 1 and len(set(settled.values())) > 1:
                key = tuple(f"{vocab}:{value}" for vocab, value in sorted(settled.items()))
                boundary[key] = boundary.get(key, 0) + 1
    if conflicts:
        report["field_conflicts"][bl_idname] = conflicts


def _validate(rows):
    seen = set()
    for row in rows:
        if len(row) != len(HEADER):
            raise GenerationError(f"row has {len(row)} cells: {row}")
        if row[0] in seen:
            raise GenerationError(f"duplicate bl_idname: {row[0]}")
        seen.add(row[0])
        for cell in row:
            if "\t" in cell or "\n" in cell or "\r" in cell:
                raise GenerationError(f"cell contains a tab or newline: {row[0]} {cell!r}")


def render_tsv(rows) -> str:
    lines = ["\t".join(HEADER)]
    lines += ["\t".join(row) for row in rows]
    return "\n".join(lines) + "\n"


def render_manifest(rows, report) -> str:
    out = [
        "# `nodes.tsv` generation manifest",
        "",
        "Generated by `tools/gen_nodes_tsv.py`. Regenerate with `--check` to confirm it",
        "is current. This is the reviewed record acceptance gate `T-10` asks for: every",
        "value here that a machine did not decide is named, with the reason.",
        "",
        f"Rows: **{len(rows)}** (union of the four identity dumps"
        f"{', minus ' + str(len(report['exclusions'])) + ' exclusions' if report['exclusions'] else ', no exclusions'}).",
        "",
        "## Sources",
        "",
        "| Role | File | sha256[:16] | Blender | Nodes |",
        "|---|---|---|---|---|",
    ]
    for key, rec in report["sources"].items():
        if key == "review":
            out.append(f"| review | `{rec['file']}` | `{rec['sha256_16']}` | — | — |")
        else:
            count = rec.get("nodes", rec.get("creatable"))
            extra = f" ({rec['vocabulary']} shapes)" if "vocabulary" in rec else ""
            out.append(
                f"| {key} | `{rec['file']}` | `{rec['sha256_16']}` | {rec['blender']}{extra} | {count} |"
            )

    out += ["", "## Coverage", ""]
    out.append("| Version | Identifiers in dump |")
    out.append("|---|---:|")
    for v, n in report["identifier_counts"].items():
        out.append(f"| {v} | {n} |")
    out.append(f"| **union** | **{report['union']}** |")

    if report["missing_evidence_versions"]:
        missing = ", ".join(report["missing_evidence_versions"])
        measured = ", ".join(report["evidence_versions"])
        out += [
            "",
            f"**Evidence gap.** No field-shape or menu evidence was read for {missing}:",
            "no such install is available here, and neither fact can be recovered from the",
            "identity dump. `category` is therefore agreed across the",
            f"measured versions ({measured}) and unverified for {missing}; they are not",
            "interpolated across the hole. `version` is unaffected — it comes from the",
            "identity dumps, which cover every version.",
        ]
    else:
        out += [
            "",
            "Field-shape and menu evidence was read for every supported version: "
            + ", ".join(report["evidence_versions"]) + ".",
        ]

    if report["identity_vs_evidence"]:
        out += [
            "",
            "### Identity and evidence measured on different maintenance builds",
            "",
            "Blender's LTS identity is the second number; the third is a maintenance",
            "release. A different maintenance build is not a different supported version,",
            "and the node sets are compared rather than assumed.",
            "",
        ]
        for v, rec in report["identity_vs_evidence"].items():
            verdict = (
                "node sets agree" if rec["sets_agree"]
                else f"**sets differ** - only in identity: {rec['only_in_identity'] or 'none'}; "
                     f"only in evidence: {rec['only_in_evidence'] or 'none'}"
            )
            out.append(
                f"- **{v}**: identity dump {rec['identity_blender']}, evidence "
                f"{rec['evidence_blender']}; {verdict}"
            )

    out += ["", "## Version markers", "", "| Marker | Rows |", "|---|---:|"]
    for marker, count in sorted(report["version_markers"].items()):
        out.append(f"| `{marker}` | {count} |")

    mechanical = len(report["category_source"])
    reviewed = len(report["category_reviewed"])
    out += [
        "",
        "## Category provenance",
        "",
        f"- **{mechanical}** rows read Blender's own Add menu "
        "(`menu_path` on the menu class, falling back to its `bl_label` where the build "
        "predates `menu_path`; every fallback label is unique).",
        f"- **{reviewed}** rows are reviewed decisions, listed below.",
        f"- **{len(report['category_unresolved'])}** unresolved.",
        "",
        "| bl_idname | Category | Kind | Reason |",
        "|---|---|---|---|",
    ]
    for bl_idname, rec in sorted(report["category_reviewed"].items()):
        out.append(f"| `{bl_idname}` | `{rec['category']}` | {rec['kind']} | {rec['reason']} |")

    out += [
        "",
        "## Socket display shapes across versions (maintainer only)",
        "",
        "**This is not a column in `nodes.tsv`.** It records mechanical socket display",
        "shapes from `tsv-evidence-*.json`. `probe_node.py` and `read_graph.py` report the",
        "live socket state (`display_shape`, `hide_value`, `has_default_value`, `type`)",
        "on the connected Blender; a static per-node value would invite being trusted instead.",
        "",
        "Derived from socket display shapes. Shapes are per socket and never rolled",
        "up per node: they move with the node's mode, and a node-level value would be the",
        "unstable abstraction the plan forbids.",
        "",
    ]
    compared = report["field_compared"]
    groups = compared["vocabulary_groups"]
    out += [
        f"Compared per socket: **{compared['sockets']} sockets** across "
        f"**{compared['nodes']} nodes** and {len(report['evidence_versions'])} versions. "
        f"{compared['socket_set_changes']} of those sockets do not exist in every version — "
        "a socket-set change, which the identity dumps and their diffs already carry, and "
        "not a capability change.",
        "",
        "### The 4.x/5.x shape vocabularies are not comparable",
        "",
        "`display_shape` is a draw-layer value and 5.x redrew it: "
        + "; ".join(f"**{vocab}** = {', '.join(vs)}" for vocab, vs in sorted(groups.items()))
        + ". Display shapes are therefore tracked **inside** a generation, and the boundary",
        "between generations is reported as raw transition counts rather than functional changes.",
        "A display shape change does not prove a capability change, and an identical shape does not",
        "prove identical capability.",
        "",
        "| Across the boundary | Sockets |",
        "|---|---:|",
    ]
    for key, count in sorted(report["field_vocabulary_boundary"].items(),
                             key=lambda kv: (-kv[1], kv[0])):
        out.append("| " + " → ".join(key) + f" | {count} |")
    out.append("")
    if report["field_conflicts"]:
        n_sockets = sum(
            len(v) for node in report["field_conflicts"].values() for v in node.values()
        )
        out += [
            f"**{n_sockets} sockets on {len(report['field_conflicts'])} nodes change display",
            "shape within a vocabulary generation (5.0 → 5.1/5.2).** Display shape changes do",
            "not prove capability changes, and identical display shapes do not prove identical capability;",
            "actual field capability must be verified against node mode, socket type, and live evaluation.",
            "Live Blender remains the authority.",
            "",
            "| bl_idname | Socket | Side | " + " | ".join(report["evidence_versions"]) + " |",
            "|---|---|---|" + "---|" * len(report["evidence_versions"]),
        ]
        for bl_idname, sides in sorted(report["field_conflicts"].items()):
            for side in ("in", "out"):
                for identifier, values in sorted(sides.get(side, {}).items()):
                    cells = [values.get(v, "—") for v in report["evidence_versions"]]
                    out.append(
                        f"| `{bl_idname}` | `{identifier}` | {side} | " + " | ".join(cells) + " |"
                    )
    else:
        out.append("No socket changes display shape inside a vocabulary generation.")

    if report["field_missing"]:
        out += [
            "",
            "No field evidence at all (present only in a version with no evidence dump): "
            + ", ".join(f"`{b}`" for b in report["field_missing"]),
        ]

    out += [
        "",
        "## Notes",
        "",
        f"**{len(report['notes'])}** of {len(rows)} rows carry a note. Each was screened",
        "against the plan's admission test: it changes candidate choice, verification or",
        "the next diagnostic action; it is not available from ordinary introspection; it",
        "belongs to one or a few named nodes; it prescribes no fixed repair; and it has",
        "retained evidence.",
        "",
        "| bl_idname | Note | Evidence |",
        "|---|---|---|",
    ]
    for bl_idname, entry in sorted(report["notes"].items()):
        note = entry["note"] if isinstance(entry, dict) else entry
        ev = entry.get("evidence", "—") if isinstance(entry, dict) else "—"
        out.append(f"| `{bl_idname}` | {note} | {ev} |")

    if report["label_changes"]:
        out += [
            "",
            "## Display names that changed between versions",
            "",
            "`display_name` takes the newest version's label.",
            "",
            "| bl_idname | Labels |",
            "|---|---|",
        ]
        for bl_idname, labels in sorted(report["label_changes"].items()):
            out.append(
                f"| `{bl_idname}` | "
                + ", ".join(f"{v}: {label!r}" for v, label in labels.items())
                + " |"
            )

    out += [
        "",
        "## Approval",
        "",
        "Acceptance gate `T-10`: **approved by the owner, 2026-09-03** — the reviewed",
        "category mappings and every note above, together with the 56-row removal",
        "manifest. The five-column schema stands; no Field column is restored.",
        "",
        "`G-TEST-02` is **not** covered by that approval: the generator, the reviewed",
        "decisions and the tests that judge them share one author, and an independent",
        "reviewer still has to confirm the decisions were not fitted to the tests.",
        "",
    ]
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="fail if the TSV or manifest on disk is out of date")
    args = parser.parse_args(argv)

    try:
        rows, report = build()
    except GenerationError as exc:
        print(f"generation failed: {exc}", file=sys.stderr)
        return 2

    tsv, manifest = render_tsv(rows), render_manifest(rows, report)

    if args.check:
        stale = []
        for path, want in ((TSV_PATH, tsv), (MANIFEST_PATH, manifest)):
            have = path.read_text(encoding="utf-8") if path.exists() else None
            if have != want:
                stale.append(path.relative_to(ROOT).as_posix())
        if stale:
            print("out of date: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"nodes.tsv and manifest are current ({len(rows)} rows)")
        return 0

    TSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    TSV_PATH.write_text(tsv, encoding="utf-8")
    MANIFEST_PATH.write_text(manifest, encoding="utf-8")
    print(
        f"wrote {TSV_PATH.relative_to(ROOT)} ({len(rows)} rows) and "
        f"{MANIFEST_PATH.relative_to(ROOT)}"
    )
    if report["field_conflicts"]:
        n_sockets = sum(
            len(v) for node in report["field_conflicts"].values() for v in node.values()
        )
        print(f"  {n_sockets} sockets on {len(report['field_conflicts'])} nodes change display "
              "shape within a vocabulary generation - maintainer evidence only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
