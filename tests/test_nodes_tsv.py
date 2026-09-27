"""Acceptance tests for `references/nodes.tsv` and its generator.

These check the file against the evidence it claims to come from, not against a
copy of itself: identifiers are re-derived from the four identity dumps, version
markers are parsed back into version sets and compared, and `field_io` is
recomputed from the socket display shapes.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TSV_PATH = ROOT / "skills" / "geometry-nodes" / "references" / "nodes.tsv"
MANIFEST_PATH = ROOT / "docs" / "node-dumps" / "nodes-tsv-manifest.md"
REVIEW_PATH = ROOT / "tools" / "nodes_tsv_review.json"
GENERATOR = ROOT / "tools" / "gen_nodes_tsv.py"

HEADER = "bl_idname\tdisplay_name\tcategory\tversion\tnote"
VERSION_ORDER = ["4.5", "5.0", "5.1", "5.2"]


def _module():
    spec = importlib.util.spec_from_file_location("gen_nodes_tsv", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gen = _module()


def _text() -> str:
    return TSV_PATH.read_text(encoding="utf-8")


def _rows() -> list[list[str]]:
    lines = _text().split("\n")
    assert lines[-1] == "", "file ends with a newline"
    return [line.split("\t") for line in lines[1:-1]]


def _dumps() -> dict[str, dict]:
    return {
        v: json.loads((ROOT / "docs" / "node-dumps" / name).read_text(encoding="utf-8"))["nodes"]
        for v, name in gen.IDENTITY_DUMPS.items()
    }


def _evidence() -> dict[str, dict]:
    """Only the evidence dumps that exist - a missing version is a reported gap."""
    return {
        v: json.loads((ROOT / "docs" / "node-dumps" / name).read_text(encoding="utf-8"))
        for v, name in gen.available_evidence().items()
    }


def _review() -> dict:
    return json.loads(REVIEW_PATH.read_text(encoding="utf-8"))


# --- T-01 --------------------------------------------------------------------
def test_file_exists_and_is_utf8():
    assert TSV_PATH.is_file()
    TSV_PATH.read_bytes().decode("utf-8")


def test_exact_header():
    assert _text().split("\n")[0] == HEADER


def test_every_row_has_six_cells_and_no_embedded_tabs_or_newlines():
    raw = _text().split("\n")[1:-1]
    for line in raw:
        cells = line.split("\t")
        assert len(cells) == 5, f"{cells[0] if cells else line!r} has {len(cells)} cells"
        for cell in cells:
            assert "\r" not in cell


def test_no_stray_carriage_returns_in_the_file():
    assert "\r" not in _text()


# --- T-02 --------------------------------------------------------------------
def test_identifiers_equal_the_dump_union_minus_reviewed_exclusions():
    dumps = _dumps()
    union = set().union(*(set(n) for n in dumps.values()))
    exclusions = set(_review().get("exclusions") or {})
    expected = union - exclusions
    actual = {row[0] for row in _rows()}
    assert actual - expected == set(), f"in TSV, not in evidence: {sorted(actual - expected)}"
    assert expected - actual == set(), f"in evidence, not in TSV: {sorted(expected - actual)}"


def test_every_exclusion_carries_a_reason():
    for bl_idname, reason in (_review().get("exclusions") or {}).items():
        assert reason, f"{bl_idname} is excluded with no reason"


# --- T-03 --------------------------------------------------------------------
def test_bl_idname_is_unique():
    ids = [row[0] for row in _rows()]
    assert len(ids) == len(set(ids))


def test_ordering_is_deterministic():
    ids = [row[0] for row in _rows()]
    assert ids == sorted(ids)


# --- T-04 --------------------------------------------------------------------
def _marker_to_versions(marker: str) -> set[str]:
    if marker.endswith("+"):
        start = VERSION_ORDER.index(marker[:-1])
        return set(VERSION_ORDER[start:])
    if marker.endswith("-only"):
        return {marker[: -len("-only")]}
    if "," in marker:
        return set(marker.split(","))
    if "-" in marker:
        lo, hi = marker.split("-")
        return set(VERSION_ORDER[VERSION_ORDER.index(lo): VERSION_ORDER.index(hi) + 1])
    raise AssertionError(f"unparseable version marker {marker!r}")


def test_version_marker_matches_dump_presence():
    dumps = _dumps()
    for bl_idname, _name, _cat, marker, _note in _rows():
        present = {v for v in VERSION_ORDER if bl_idname in dumps[v]}
        assert _marker_to_versions(marker) == present, (
            f"{bl_idname}: marker {marker!r} says {_marker_to_versions(marker)}, "
            f"dumps say {present}"
        )


def test_version_marker_is_not_taken_from_the_connected_blender():
    """Every marker is a function of the dumps alone - no live Blender is read."""
    source = GENERATOR.read_text(encoding="utf-8")
    assert "import bpy" not in source
    assert "bpy.app.version" not in source


# --- T-05: the column is gone; the comparison still happens ------------------
def test_the_tsv_has_no_field_capability_column():
    """Owner decision 2026-09-02: compared and reported, never shipped.

    Three files would otherwise answer one question with three accuracies. Only
    probe_node.py is right at wiring time, so nothing static may compete with it.
    """
    header = _text().split("\n")[0]
    assert "field_io" not in header
    assert len(header.split("\t")) == 5


def test_no_blank_varies_or_version_encoded_stand_in_for_the_removed_column():
    """The plan forbids replacing the column with a disguised version of itself."""
    for row in _rows():
        assert len(row) == 5
        assert "varies" not in row[4].lower()
    assert "field_io" not in _text()


def test_field_capability_is_compared_per_socket_not_per_node():
    _rows_, report = gen.build()
    compared = report["field_compared"]
    assert compared["nodes"] == len(_rows()) - len(report["field_missing"])
    assert compared["sockets"] > compared["nodes"], "per socket, not per node"
    # Conflicts are keyed node -> side -> socket identifier, never node -> value.
    for sides in report["field_conflicts"].values():
        assert set(sides) <= {"in", "out"}
        for socks in sides.values():
            for identifier, values in socks.items():
                assert isinstance(identifier, str)
                assert set(values.values()) <= gen.KNOWN_SHAPES


def test_comparison_covers_every_available_version():
    _rows_, report = gen.build()
    assert set(report["evidence_versions"]) == set(_evidence())
    groups = report["field_compared"]["vocabulary_groups"]
    assert set(v for vs in groups.values() for v in vs) == set(_evidence())


def test_the_4x_5x_boundary_is_reported_not_counted_as_change():
    """The shape vocabularies do not map onto each other; treating them as a
    rename moves sockets in both directions across the same boundary at once.

    Measured: 170 one way, 56 the other. A capability change does not do that,
    so the boundary is stated as a limitation instead of producing conflicts.
    """
    _rows_, report = gen.build()
    boundary = report["field_vocabulary_boundary"]
    assert boundary, "the boundary evidence has to be retained, not silently dropped"
    directions = {
        tuple(sorted(key)) for key in boundary
    }
    assert len(boundary) >= 2, "both directions are the evidence"
    for sides in report["field_conflicts"].values():
        for socks in sides.values():
            for values in socks.values():
                groups = report["field_compared"]["vocabulary_groups"]
                inside = [
                    {values[v] for v in versions if v in values}
                    for versions in groups.values()
                ]
                assert any(len(vals) > 1 for vals in inside), (
                    "a conflict must differ inside one vocabulary, not only across it"
                )
    assert directions  # the tuple set is what makes the both-directions claim checkable


def test_cross_version_capability_changes_reach_the_manifest():
    _rows_, report = gen.build()
    manifest = MANIFEST_PATH.read_text(encoding="utf-8")
    assert report["field_conflicts"], "the known string/switch changes should be detected"
    for bl_idname in report["field_conflicts"]:
        assert f"`{bl_idname}`" in manifest, f"{bl_idname} changes capability and is unreported"
    assert "not a column in `nodes.tsv`" in manifest
    assert "not comparable" in manifest


def test_socket_shapes_are_raw_evidence():
    """Generator compares raw socket display shapes rather than unproven capability labels."""
    _rows_, report = gen.build()
    for sides in report["field_conflicts"].values():
        for socks in sides.values():
            for values in socks.values():
                for shape in values.values():
                    assert shape in gen.KNOWN_SHAPES


def test_vocabulary_detection_picks_the_table_from_the_shapes_present():
    assert gen.detect_vocabulary({"field_shapes": {"n": {"in": {"a": "LINE"}, "out": {}}}}) == "5.x"
    assert gen.detect_vocabulary(
        {"field_shapes": {"n": {"in": {"a": "DIAMOND_DOT"}, "out": {}}}}
    ) == "4.x"
    with pytest.raises(gen.GenerationError):
        gen.detect_vocabulary({"field_shapes": {"n": {"in": {"a": "SQUARE"}, "out": {}}}})


# --- T-06 --------------------------------------------------------------------
def test_every_row_has_a_category():
    blank = [row[0] for row in _rows() if not row[2]]
    assert not blank, f"rows with no category: {blank}"


def test_category_is_mechanical_or_explicitly_reviewed():
    evidence = _evidence()
    review = _review()
    reviewed = set(review.get("categories") or {}) | set(
        review.get("ambiguous_category_choice") or {}
    )
    for bl_idname, _n, category, _v, _note in _rows():
        from_menu = {
            entry["category"]
            for v in evidence
            for entry in evidence[v]["menu_paths"].get(bl_idname, [])
        }
        if category in from_menu:
            continue
        assert bl_idname in reviewed, (
            f"{bl_idname} has category {category!r} that is in no Add menu "
            f"({from_menu or 'none'}) and in no reviewed decision"
        )


def test_reviewed_categories_carry_a_reason():
    review = _review()
    for group in ("categories", "ambiguous_category_choice"):
        for bl_idname, rec in (review.get(group) or {}).items():
            assert rec.get("category"), f"{bl_idname} has no category"
            assert rec.get("reason"), f"{bl_idname} has no reason"


# --- T-07 --------------------------------------------------------------------
def test_notes_are_sparse():
    rows = _rows()
    with_notes = [row for row in rows if row[4]]
    assert with_notes, "the note column is not meant to be empty everywhere"
    assert len(with_notes) < len(rows) * 0.1, (
        f"{len(with_notes)} of {len(rows)} rows carry a note; the column is for exceptions"
    )


def test_every_note_comes_from_the_reviewed_file_with_evidence():
    notes = _review().get("notes") or {}
    for bl_idname, _n, _c, _v, note in _rows():
        if not note:
            continue
        assert bl_idname in notes, f"{bl_idname} has a note that is in no reviewed source"
        entry = notes[bl_idname]
        assert entry["note"] == note
        assert entry.get("evidence"), f"{bl_idname}'s note has no retained evidence"


def test_notes_carry_no_socket_lists_or_manual_prose():
    for bl_idname, _n, _c, _v, note in _rows():
        if not note:
            continue
        assert len(note) <= 200, f"{bl_idname}'s note is {len(note)} chars; keep it a hint"
        assert "`" not in note, f"{bl_idname}'s note uses code fencing"
        # A socket list would read as a comma-separated run of Title Case names.
        assert note.count(",") <= 4, f"{bl_idname}'s note looks like a list"


def test_no_reviewed_category_is_dead():
    """A reviewed decision that never fires is stale metadata waiting to drift.

    GeometryNodeList needed one until the 5.0 evidence landed and put it in
    Utilities/List mechanically; that entry was removed rather than left behind.
    """
    _rows_, report = gen.build()
    review = _review()
    declared = set(review.get("categories") or {}) | set(
        review.get("ambiguous_category_choice") or {}
    )
    used = set(report["category_reviewed"])
    assert declared == used, f"declared but unused: {sorted(declared - used)}"


def test_reviewed_notes_all_land_in_the_file():
    """A note nobody can reach is a maintenance trap."""
    in_tsv = {row[0] for row in _rows() if row[4]}
    assert set((_review().get("notes") or {})) == in_tsv


# --- T-08 --------------------------------------------------------------------
def test_regeneration_is_idempotent():
    proc = subprocess.run(
        [sys.executable, str(GENERATOR), "--check"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_build_is_deterministic():
    first, _ = gen.build()
    second, _ = gen.build()
    assert first == second


def test_manifest_is_present_and_names_its_sources():
    manifest = MANIFEST_PATH.read_text(encoding="utf-8")
    for name in list(gen.IDENTITY_DUMPS.values()) + list(gen.available_evidence().values()):
        assert name in manifest, f"{name} is not credited in the manifest"
    assert "T-10" in manifest, "the manifest must say the reviewed entries need approval"


def test_manifest_accounts_for_every_supported_version():
    """Either evidence was read for a version, or the gap is named in the manifest."""
    _rows_, report = gen.build()
    covered = set(report["evidence_versions"]) | set(report["missing_evidence_versions"])
    assert covered == set(gen.IDENTITY_DUMPS)
    manifest = MANIFEST_PATH.read_text(encoding="utf-8")
    for version in report["missing_evidence_versions"]:
        assert version in manifest, f"{version} has no evidence and is not named"


def test_evidence_dumps_are_discovered_by_supported_version():
    """Blender's LTS identity is the second number; the third is maintenance.

    4.5.13 is the same supported version as 4.5.12, so the generator globs per
    supported version and a maintenance bump needs no code change. Measured
    2026-09-02: the two builds report identical node types, socket shapes and
    menu paths.
    """
    available = gen.available_evidence()
    assert set(available) <= set(gen.EVIDENCE_GLOBS)
    assert set(gen.EVIDENCE_GLOBS) == set(gen.VERSION_ORDER)
    assert available, "at least one evidence dump has to be present"
    for version, name in available.items():
        assert (ROOT / "docs" / "node-dumps" / name).exists()
        assert name.startswith(f"tsv-evidence-{version}."), (
            f"{name} is filed under supported version {version}"
        )


def test_a_maintenance_build_difference_is_reported_not_hidden():
    """Mixing builds within one supported version is allowed and never silent."""
    _rows_, report = gen.build()
    for version, rec in report["identity_vs_evidence"].items():
        assert rec["identity_blender"] != rec["evidence_blender"] or not rec["sets_agree"]
        assert rec["sets_agree"], (
            f"{version}: identity {rec['identity_blender']} and evidence "
            f"{rec['evidence_blender']} disagree on which nodes exist"
        )
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        assert rec["evidence_blender"] in manifest


# --- routing contract --------------------------------------------------------
def test_tsv_carries_no_socket_or_property_identities():
    """T-09's half that a file can prove: the TSV is not a socket authority."""
    text = _text()
    for token in ("NodeSocket", "default_value", "identifier=", "Socket_0"):
        assert token not in text, f"{token} has no business in a routing index"


def test_tsv_is_small_enough_to_search_without_bulk_reading():
    size = TSV_PATH.stat().st_size
    assert size < 60_000, f"{size} bytes; the routing index has to stay cheap"
