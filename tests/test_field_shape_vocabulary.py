"""Behavioral tests for socket display shapes and runtime introspection.

`display_shape` is a draw-layer fact whose vocabulary changed in 5.x.
Runtime scripts report raw mechanical facts — `display_shape`, `hide_value`
(when present), and `has_default_value` — rather than guessing an unproven
tri-state field capability.
"""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = {
    "read_graph": ROOT / "skills" / "geometry-nodes" / "scripts" / "read_graph.py",
    "probe_node": ROOT / "skills" / "geometry-nodes" / "scripts" / "probe_node.py",
}
DUMPS_DIR = ROOT / "docs" / "node-dumps"


@pytest.mark.parametrize("name", sorted(SCRIPTS))
def test_runtime_scripts_detect_vocabulary_from_rna(name):
    """The vocabulary detector must query the registered enum items."""
    source = SCRIPTS[name].read_text(encoding="utf-8")
    assert "def shape_vocabulary()" in source
    assert "display_shape" in source and "enum_items" in source
    assert '"LINE"' in source


@pytest.mark.parametrize("name", sorted(SCRIPTS))
def test_runtime_scripts_do_not_emit_unproven_field_tristate(name):
    """Neither script should assign rec['field'] or define a shape-to-capability map."""
    source = SCRIPTS[name].read_text(encoding="utf-8")
    assert "SHAPE_VOCABULARIES" not in source
    assert 'rec["field"]' not in source
    assert "field_capability" not in source


@pytest.mark.parametrize("name", sorted(SCRIPTS))
def test_runtime_scripts_emit_raw_facts(name):
    """_socket must record display_shape, hide_value (when present), and has_default_value."""
    source = SCRIPTS[name].read_text(encoding="utf-8")
    assert '"display_shape"' in source
    assert '"hide_value"' in source
    assert '"has_default_value"' in source


def test_evidence_dumps_contain_version_specific_shapes():
    """4.5 evidence uses DIAMOND_DOT and no LINE; 5.2 uses LINE and no DIAMOND_DOT."""
    e45 = json.loads((DUMPS_DIR / "tsv-evidence-4.5.13.json").read_text(encoding="utf-8"))
    e52 = json.loads((DUMPS_DIR / "tsv-evidence-5.2.1.json").read_text(encoding="utf-8"))

    shapes_45 = {
        s for n in e45["field_shapes"].values() for side in ("in", "out") for s in n[side].values()
    }
    shapes_52 = {
        s for n in e52["field_shapes"].values() for side in ("in", "out") for s in n[side].values()
    }

    assert "DIAMOND_DOT" in shapes_45 and "LINE" not in shapes_45
    assert "LINE" in shapes_52 and "DIAMOND_DOT" not in shapes_52


def test_archetype_socket_shapes_in_evidence():
    """Verify raw display shapes for key archetype sockets in versioned evidence."""
    e45 = json.loads((DUMPS_DIR / "tsv-evidence-4.5.13.json").read_text(encoding="utf-8"))
    e52 = json.loads((DUMPS_DIR / "tsv-evidence-5.2.1.json").read_text(encoding="utf-8"))

    # Set Position: Selection vs Offset
    assert e45["field_shapes"]["GeometryNodeSetPosition"]["in"]["Selection"] == "DIAMOND_DOT"
    assert e45["field_shapes"]["GeometryNodeSetPosition"]["in"]["Offset"] == "DIAMOND_DOT"

    # In 5.2 both are DIAMOND, proving display_shape alone cannot distinguish them
    assert e52["field_shapes"]["GeometryNodeSetPosition"]["in"]["Selection"] == "DIAMOND"
    assert e52["field_shapes"]["GeometryNodeSetPosition"]["in"]["Offset"] == "DIAMOND"

    # Constant output vs Field output
    assert e52["field_shapes"]["ShaderNodeValue"]["out"]["Value"] == "LINE"
    assert e52["field_shapes"]["GeometryNodeInputPosition"]["out"]["Position"] == "DIAMOND"


def _blender_bin() -> str | None:
    for candidate in (
        "/Applications/Blender.app/Contents/MacOS/Blender",
        shutil.which("blender"),
    ):
        if candidate and Path(candidate).exists():
            return candidate
    return None


@pytest.mark.skipif(_blender_bin() is None, reason="no Blender executable found")
def test_live_socket_archetypes_behavior():
    """Live Blender oracle: verifies raw facts across the five socket archetypes."""
    code = """
import bpy, json

tree = bpy.data.node_groups.new("TestArchetypes", "GeometryNodeTree")

# 1. Geometry socket
mesh_cube = tree.nodes.new("GeometryNodeMeshCube")
geom_sock = mesh_cube.outputs["Mesh"]

# 2. Field input with hidden value (no literal typing in UI)
set_pos = tree.nodes.new("GeometryNodeSetPosition")
sel_sock = set_pos.inputs["Selection"]

# 3. Field input with default value (accepts literal or field)
offset_sock = set_pos.inputs["Offset"]

# 4. Constant / single output
val_node = tree.nodes.new("ShaderNodeValue")
const_out = val_node.outputs[0]

# 5. Field output
pos_node = tree.nodes.new("GeometryNodeInputPosition")
field_out = pos_node.outputs["Position"]

results = {
    "geom": {
        "type": geom_sock.type,
        "has_def": hasattr(geom_sock, "default_value"),
    },
    "field_hidden": {
        "hide_value": getattr(sel_sock, "hide_value", False),
        "shape": getattr(sel_sock, "display_shape", None),
    },
    "field_literal": {
        "hide_value": getattr(offset_sock, "hide_value", False),
        "has_def": hasattr(offset_sock, "default_value"),
        "shape": getattr(offset_sock, "display_shape", None),
    },
    "const_out": {
        "shape": getattr(const_out, "display_shape", None),
    },
    "field_out": {
        "shape": getattr(field_out, "display_shape", None),
    }
}
bpy.data.node_groups.remove(tree)
print("NODE_ARCHETYPES_JSON:" + json.dumps(results))
"""
    proc = subprocess.run(
        [_blender_bin(), "-b", "--factory-startup", "--python-expr", code],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    line = [l for l in proc.stdout.splitlines() if "NODE_ARCHETYPES_JSON:" in l][0]
    data = json.loads(line.partition("NODE_ARCHETYPES_JSON:")[2])

    assert data["geom"]["type"] == "GEOMETRY"
    assert data["geom"]["has_def"] is False
    assert data["field_hidden"]["hide_value"] is True
    assert data["field_literal"]["hide_value"] is False
    assert data["field_literal"]["has_def"] is True
    assert data["field_out"]["shape"] == "DIAMOND"
