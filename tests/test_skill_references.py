"""Acceptance tests for the conditional references under `references/`.

These hold each file to the contract that decides whether it is worth its retrieval
cost: a narrow subject, an explicit read trigger, no inventory that will go stale,
and no fact that another file already owns.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "skills" / "geometry-nodes" / "references"
VERSIONS = REFS / "versions.md"
REUSE = REFS / "reuse.md"
DIAGNOSTICS = REFS / "diagnostics.md"
TSV = REFS / "nodes.tsv"
SKILL = ROOT / "skills" / "geometry-nodes" / "SKILL.md"
NODE_DUMPS = ROOT / "docs" / "node-dumps"

SHIPPED = [VERSIONS, REUSE, DIAGNOSTICS]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _body(path: Path) -> str:
    """The file without its YAML frontmatter."""
    text = _text(path)
    if text.startswith("---\n"):
        return text.split("---\n", 2)[2]
    return text


def _tsv_identifiers() -> set[str]:
    lines = _text(TSV).split("\n")[1:-1]
    return {line.split("\t")[0] for line in lines}


def _capture_attribute_inputs(dump_name: str) -> set[str]:
    dump = json.loads((NODE_DUMPS / dump_name).read_text(encoding="utf-8"))
    node = dump["nodes"]["GeometryNodeCaptureAttribute"]
    return {socket[0] for socket in node["in"]}


# --- shared -------------------------------------------------------------------
def test_versions_documents_blender_52_modifier_group_input_path():
    body = _body(VERSIONS)
    assert "In Blender 5.2" in body
    assert "modifier.properties.inputs.Socket_n.value" in body
    assert '`modifier["Socket_n"] = value`' in body
    assert "errors on this version" in body
    assert "do not assume this path is portable to other releases" in body


def test_capture_attribute_selection_input_is_version_bounded_by_dumps():
    assert "Selection" not in _capture_attribute_inputs("gn-4.5.12.json")
    assert "Selection" not in _capture_attribute_inputs("gn-5.0.1.json")
    assert "Selection" not in _capture_attribute_inputs("gn-5.1.2.json")
    assert "Selection" in _capture_attribute_inputs("gn-5.2.0.json")
    body = _body(VERSIONS)
    assert "5.2.0" in body and "GeometryNodeCaptureAttribute" in body


@pytest.mark.parametrize("path", SHIPPED, ids=lambda p: p.name)
def test_reference_exists_and_is_utf8(path):
    assert path.is_file()
    path.read_bytes().decode("utf-8")


@pytest.mark.parametrize("path", SHIPPED, ids=lambda p: p.name)
def test_reference_is_not_empty_or_a_placeholder(path):
    """R-LINK-02: no file exists only to match the target tree diagram."""
    body = _body(path).strip()
    assert len(body) > 800, f"{path.name} is {len(body)} chars; a stub is not a reference"
    assert "TODO" not in body and "TBD" not in body


@pytest.mark.parametrize("path", SHIPPED, ids=lambda p: p.name)
def test_reference_states_its_own_read_trigger(path):
    """A conditional reference has to say when it is worth opening."""
    body = _body(path)
    assert re.search(r"\*\*Read this only when\*\*", body), (
        f"{path.name} does not state the condition that warrants its cost"
    )


@pytest.mark.parametrize("path", SHIPPED, ids=lambda p: p.name)
def test_reference_carries_no_personal_absolute_path(path):
    for bad in ("/Users/", "/home/", "C:\\"):
        assert bad not in _text(path)


@pytest.mark.parametrize("path", SHIPPED, ids=lambda p: p.name)
def test_reference_stays_cheap_to_read(path):
    size = path.stat().st_size
    assert size < 7000, f"{path.name} is {size} bytes; a conditional read has to stay cheap"


def test_references_do_not_restate_each_other():
    """R-LINK-03: one fact, one authority.

    Compared on substantial sentences rather than words - a shared heading like
    "## Evidence" is not a duplicated fact, a shared 60-character claim is.
    """
    def claims(path):
        return {
            line.strip()
            for line in _body(path).split("\n")
            if len(line.strip()) >= 60 and not line.strip().startswith(("|", "#"))
        }

    for i, first in enumerate(SHIPPED):
        for second in SHIPPED[i + 1:]:
            shared = claims(first) & claims(second)
            assert not shared, f"{first.name} and {second.name} both assert: {shared}"


# --- R-VERSION-* --------------------------------------------------------------
# Sections where naming a node identifier is the point: a rename, a gate, a
# deprecation, or a version-specific interface change. Elsewhere, that restates nodes.tsv.
_VERSION_SECTIONS_THAT_MAY_NAME_NODES = (
    "Renamed, not removed",
    "Experimental gates",
    "Deprecated, with a replacement that is not a drop-in",
    "Blender 5.2 API notes",
)


def _sections(path):
    out, heading = {}, "(preamble)"
    for line in _body(path).split("\n"):
        if line.startswith("## "):
            heading = line[3:].strip()
        out.setdefault(heading, []).append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def test_versions_names_nodes_only_where_the_contract_allows():
    """R-VERSION-02: simple availability lives in nodes.tsv, not here.

    Checked by where an identifier appears, not by how many there are. A rename
    pair, a gated family and a deprecation each have to name nodes to be usable;
    a bare "this node exists on 5.1+" is the TSV's job.
    """
    identifiers = _tsv_identifiers()
    for heading, section in _sections(VERSIONS).items():
        if heading in _VERSION_SECTIONS_THAT_MAY_NAME_NODES:
            continue
        named = sorted(i for i in identifiers if i in section)
        assert not named, f"section {heading!r} names {named}; that restates nodes.tsv"


def test_versions_says_where_availability_actually_lives():
    assert "`nodes.tsv`" in _body(VERSIONS)


def test_the_sections_allowed_to_name_nodes_actually_do():
    """Guards the allow-list from quietly becoming a licence for anything."""
    sections = _sections(VERSIONS)
    for heading in _VERSION_SECTIONS_THAT_MAY_NAME_NODES:
        assert heading in sections, f"allow-listed section {heading!r} does not exist"


def test_versions_publishes_no_socket_lists_or_current_identities():
    body = _body(VERSIONS)
    for token in ("NodeSocket", "identifier `", "**Inputs:**", "**Outputs:**"):
        assert token not in body, f"{token} is a current-version identity, not a difference"


def test_versions_publishes_no_static_asset_inventory():
    """A capability boundary is allowed; a list of asset names is not."""
    body = _body(VERSIONS)
    for name in ("Scatter on Surface", "Curve to Tube", "Smooth by Angle", "Box Selection"):
        assert name not in body, f"{name} is inventory; it goes stale and reuse.md refuses it too"


def test_versions_covers_the_categories_its_contract_names():
    body = _body(VERSIONS)
    for heading in ("Renamed", "Experimental gates", "Deprecated", "Field capability"):
        assert heading in body, f"missing the {heading!r} section its contract requires"


def test_versions_defers_current_field_capability_to_the_probe():
    """The Field summary is a planning fact; the live answer is probe_node.py."""
    body = _body(VERSIONS)
    assert "probe_node.py" in body
    section = body.split("## Field capability", 1)[1].split("\n## ", 1)[0]
    assert len(section) < 700, "family-level summary, not an enumeration"
    assert not re.search(r"`(Function|Geometry)Node\w+`", section), (
        "the Field summary enumerates nodes; it should name families"
    )


def test_versions_says_probing_availability_is_a_write():
    assert "write" in _body(VERSIONS).lower()
    assert "Explain" in _body(VERSIONS)


# --- R-REUSE-* ----------------------------------------------------------------
def test_reuse_states_the_search_order():
    body = _body(REUSE)
    current = body.index("current `.blend`")
    bundled = body.index("bundled asset libraries")
    user = body.index("configured asset libraries")
    assert current < bundled < user, "search order must be current file, bundled, then user"


def test_reuse_carries_no_asset_inventory():
    """R-REUSE-03: what a library holds is read at runtime."""
    body = _body(REUSE)
    for name in ("Scatter on Surface", "Array", "Curve to Tube", "Cloth Dynamics",
                 "geometry_nodes_essentials", "Randomize Transforms"):
        assert name not in body, f"{name} is a stale-by-construction inventory entry"


def test_reuse_judges_by_comprehension_not_node_count():
    body = _body(REUSE)
    assert "not how many nodes" in body
    assert not re.search(r"[<>=\u2264\u2265]\s*\d+\s*nodes", body), (
        "a fixed node-count threshold is exactly what the contract rejects"
    )


def test_reuse_requires_reading_the_live_interface_and_identifiers():
    body = _body(REUSE)
    assert "identifier" in body, "interface socket names are not unique"
    assert "running Blender" in body


def test_reuse_keeps_appending_separate_from_inspection():
    body = _body(REUSE)
    assert "Build/Edit mutation" in body
    assert "Explain" in body


def test_reuse_covers_presenting_candidates_and_link_vs_append():
    body = _body(REUSE)
    assert "Present candidates" in body
    assert "Link" in body and "Append" in body


def test_reuse_does_not_reintroduce_removed_project_memory():
    body = _body(REUSE)
    assert "NODECUE.md" not in body
    assert "Recording what you learned" not in body


def test_reuse_routes_to_the_script_not_to_a_host():
    """R-REUSE-03 again: no host-specific orchestration."""
    body = _body(REUSE)
    assert "inspect_assets.py" in body
    for host in ("MCP", "Claude", "Codex", "execute_blender_code"):
        assert host not in body


# --- R-DIAG-* -----------------------------------------------------------------
def test_diagnostics_uses_the_three_column_table():
    body = _body(DIAGNOSTICS)
    assert "| Observed signal | Inspect next | Do not assume |" in body


def test_diagnostics_admission_bar_is_met():
    """R-DIAG-01: the file exists only if at least three entries share the trigger."""
    rows = [
        line for line in _body(DIAGNOSTICS).split("\n")
        if line.startswith("|") and not line.startswith("|---")
    ][1:]
    assert len(rows) >= 3, f"{len(rows)} rows; below the admission bar the file must not exist"
    for row in rows:
        assert len(row.split("|")) == 5, f"row is not three columns: {row}"


def test_diagnostics_carries_no_measurements_or_fixed_corrections():
    """R-DIAG-03: pivots, not case studies with numbers in them."""
    body = _body(DIAGNOSTICS)
    numbers = re.findall(r"(?<![\w.])\d+(?:\.\d+)?\s*(?:m|mm|verts?|vertices|degrees|°)", body)
    assert not numbers, f"measurements found: {numbers}"
    assert not re.search(r"[-+]?\d+\.\d+", body), "a decimal here is a fixed compensation value"


def test_diagnostics_prescribes_computing_placement_not_a_stored_offset():
    """R-DIAG-04: the source-origin pivot must not carry a cone-shaped answer."""
    body = _body(DIAGNOSTICS)
    origin_row = next(r for r in body.split("\n") if "evaluated bounds" in r)
    assert "Cone" not in origin_row and "cone" not in origin_row
    assert "offset" not in origin_row.lower() or "did not intend" in origin_row
    assert "Compute the correction from what you observe" in body


def test_diagnostics_is_a_table_not_an_essay():
    body = _body(DIAGNOSTICS)
    prose = [
        line for line in body.split("\n")
        if line.strip() and not line.startswith(("|", "#", "**Read"))
    ]
    assert len("\n".join(prose)) < 400, "the preamble has grown into an essay"


# --- R-LINK-01 / R-LINK-04: deferred to the SKILL.md rewrite -------------------
@pytest.mark.skip(reason="Phase 4 rewrites SKILL.md; R-LINK-01 and R-LINK-04 verify there")
def test_every_shipped_reference_has_a_read_trigger_in_skill_md():
    skill = _text(SKILL)
    for path in SHIPPED + [TSV]:
        assert f"references/{path.name}" in skill, f"{path.name} is shipped and unreachable"
