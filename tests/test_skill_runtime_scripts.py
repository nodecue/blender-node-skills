"""Contract tests for the Geometry Nodes runtime scripts.

The static half runs anywhere: it holds the scripts to the contract
the skill relies on without needing Blender. The integration half runs the real checks
inside Blender and is skipped when no Blender is available.
"""

from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "geometry-nodes" / "scripts"
GOLDEN = ROOT / "tests" / "golden" / "run_skill_runtime_scripts.py"

SCRIPT_NAMES = [
    "find_nodes.py",
    "read_graph.py",
    "capture.py",
    "probe_node.py",
    "inspect_assets.py",
    "layout_graph.py",
    "verify_result.py",
]


def _source(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8")


def _tree(name: str) -> ast.Module:
    return ast.parse(_source(name))


def _top_level_functions(name: str) -> set[str]:
    return {n.name for n in _tree(name).body if isinstance(n, ast.FunctionDef)}


def _dotted(node: ast.AST) -> str:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def _call_names(name: str) -> list[str]:
    """Dotted names of every call the module actually makes.

    Prose is not code: these checks read the AST so a docstring that *describes*
    a forbidden call does not count as making one.
    """
    return [_dotted(n.func) for n in ast.walk(_tree(name)) if isinstance(n, ast.Call)]


def _imports(name: str) -> set[str]:
    out: set[str] = set()
    for node in ast.walk(_tree(name)):
        if isinstance(node, ast.Import):
            out |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.add(node.module.split(".")[0])
    return out


@pytest.mark.parametrize("name", SCRIPT_NAMES)
def test_script_exists(name):
    assert (SCRIPTS / name).is_file(), f"{name} is missing from the runtime package"


@pytest.mark.parametrize("name", SCRIPT_NAMES)
def test_callable_entrypoint(name):
    """A host must be able to invoke the file without re-authoring its body."""
    assert "run" in _top_level_functions(name)


@pytest.mark.parametrize("name", SCRIPT_NAMES)
def test_returns_through_both_channels(name):
    src = _source(name)
    assert "print(json.dumps(" in src, "stdout channel missing"
    # The host reads `result`. Printing the same payload as well doubles what
    # lands in the caller's context, so only the CLI channel prints.
    assert "result = run(NODECUE_PARAMS)" in src, "runpy result must not print"
    assert "_emit(run(NODECUE_PARAMS))" not in src, "runpy channel prints its payload"
    assert "NODECUE_PARAMS" in src, "host-injected parameter channel missing"
    assert '__name__ == "__main__"' in src, "CLI channel missing"


@pytest.mark.parametrize("name", SCRIPT_NAMES)
def test_documented(name):
    doc = ast.get_docstring(_tree(name))
    assert doc and len(doc) > 200, "each script documents its own contract"


@pytest.mark.parametrize("name", SCRIPT_NAMES)
def test_no_absolute_user_paths(name):
    src = _source(name)
    for bad in ("/Users/", "/home/", "C:\\\\"):
        assert bad not in src, f"{name} carries an unresolved absolute path"


@pytest.mark.parametrize("name", SCRIPT_NAMES)
def test_no_broad_orphan_purge(name):
    """A broad purge would take the user's unrelated unused datablocks with it."""
    assert not [c for c in _call_names(name) if c.endswith("orphans_purge")]


def test_layout_graph_check_and_apply_are_distinct():
    src = _source("layout_graph.py")
    assert '"check"' in src and '"apply"' in src
    assert "graph_correctness" in src
    assert "not_evaluated" in src
    assert "location_absolute" in src
    assert "protected" in src
    assert "mutated" in src
    assert "_rollback_layout" in src
    assert "_PROTECTED_EPS" in src
    assert "node.parent" in src
    calls = _call_names("layout_graph.py")
    assert not [c for c in calls if c.startswith("bpy.ops")], "layout uses data API, not operators"


def test_read_graph_reports_layout_facts():
    src = _source("read_graph.py")
    assert '"location"' in src
    assert '"location_absolute"' in src
    assert '"width"' in src
    assert '"height"' in src


def test_read_graph_defaults_to_compact_summary_and_keeps_full_mode():
    src = _source("read_graph.py")
    assert 'params.get("detail", "summary")' in src
    assert 'detail == "summary"' in src
    assert 'payload["node_names"]' in src
    assert 'payload["issues"]' in src
    assert 'payload["nodes"]' in src
    assert 'detail must be \'summary\' or \'full\'' in src


def test_read_graph_is_read_only():
    """Explain mode depends on this script not writing. Enforce it statically."""
    calls = _call_names("read_graph.py")
    assert not [c for c in calls if c.startswith("bpy.ops")], "no operators"
    mutating = [c for c in calls
                if c.rsplit(".", 1)[-1] in {"new", "remove", "clear", "batch_remove"}]
    assert not mutating, f"read_graph.py must not call {mutating}"
    assert "setattr" not in calls
    # Writing a socket default or a node property is an attribute assignment.
    targets = [
        t for node in ast.walk(_tree("read_graph.py"))
        if isinstance(node, (ast.Assign, ast.AugAssign))
        for t in (node.targets if isinstance(node, ast.Assign) else [node.target])
        if isinstance(t, ast.Attribute)
    ]
    assert not targets, "read_graph.py must not assign to any attribute"


def test_probe_node_is_compact_by_default_and_keeps_full_mode():
    src = _source("probe_node.py")
    assert 'params.get("detail", "compact")' in src
    assert "detail must be 'compact' or 'full'" in src
    assert '"inactive_inputs"' in src and '"inactive_outputs"' in src


@pytest.mark.parametrize("name", ["probe_node.py", "read_graph.py", "verify_result.py"])
def test_unknown_parameters_are_rejected_not_ignored(name):
    """An ignored misspelt key silently answers a different question."""
    src = _source(name)
    assert "_PARAMS" in src and "unknown parameter(s)" in src


def test_verify_result_reports_values_persistence_and_cleans_up():
    src = _source("verify_result.py")
    for token in ("ATTRIBUTE_CONSTANT_EVERYWHERE", "ATTRIBUTE_ALL_ZERO",
                  "ATTRIBUTE_MISSING", "GROUP_NOT_SAVED", "use_fake_user",
                  "counts_restored", "evaluated_geometry"):
        assert token in src, token
    calls = _call_names("verify_result.py")
    assert not [c for c in calls if c.startswith("bpy.ops")], "data API, not operators"


def test_probe_node_cleans_up_what_it_creates():
    src = _source("probe_node.py")
    assert "node_groups.remove" in src
    assert "counts_restored" in src
    assert "uuid" in src, "the temporary tree needs a unique name"


def test_capture_never_forces_a_redraw():
    """wm.redraw_timer segfaults Blender, from a timer-driven host and from a
    --python startup script alike. Measured twice on 5.2.1; both crash in
    redraw_timer_exec.

    The staged prepare/capture/restore API exists so Blender's own event loop
    does the redrawing. Calling the operator would take Blender down with it.
    """
    src = _source("capture.py")
    sites = [c for c in _call_names("capture.py") if c.endswith("redraw_timer")]
    assert not sites, f"capture.py must not call redraw_timer, found {sites}"
    assert "tag_redraw()" in src
    assert {"prepare", "capture", "restore", "all"} <= set(
        k.value for n in ast.walk(_tree("capture.py"))
        if isinstance(n, ast.Dict) for k in n.keys
        if isinstance(k, ast.Constant) and isinstance(k.value, str)
    ), "the staged API is the supported path"


def test_capture_restores_ui_state():
    src = _source("capture.py")
    assert "back_to_previous" in src
    assert "ui_restored" in src
    assert "graph_unchanged" in src


def test_inspect_assets_refuses_paths_outside_configured_libraries():
    src = _source("inspect_assets.py")
    assert "_authorized" in src
    assert "asset_libraries" in src
    assert "allowed_roots" in src
    assert "realpath" in src, "the guard has to resolve symlinks"


def test_inspect_assets_does_not_append_into_the_working_file():
    """Bringing a group in for real is a Build/Edit mutation, not discovery."""
    src = _source("inspect_assets.py")
    assert "counts_restored" in src
    assert src.count("libraries.load") >= 1


def test_inspect_assets_cleans_every_collection_it_watches():
    """A real user asset brings objects, meshes and materials, not only groups.

    Measured on 5.2.1: one 14-node group out of a third-party library loaded 22
    datablocks. Cleaning node_groups alone left 7 objects in the user's session.
    """
    tree = _tree("inspect_assets.py")
    consts = {
        n.targets[0].id: [e.value for e in n.value.elts]
        for n in tree.body
        if isinstance(n, ast.Assign)
        and isinstance(n.targets[0], ast.Name)
        and isinstance(n.value, ast.Tuple)
    }
    watched, order = set(consts["_WATCHED"]), consts["_REMOVE_ORDER"]
    assert watched <= set(order), sorted(watched - set(order))
    assert "objects" in order and order.index("objects") < order.index("meshes"), (
        "objects must go first so their data drops to zero users"
    )
    assert order.index("meshes") < order.index("node_groups")


@pytest.mark.parametrize("name", SCRIPT_NAMES)
def test_no_network_and_no_subprocess(name):
    """Asset discovery reads the local filesystem and nothing else."""
    banned = {"urllib", "requests", "socket", "http", "ftplib", "smtplib",
              "asyncio", "subprocess", "shutil"}
    assert not (_imports(name) & banned), sorted(_imports(name) & banned)


def _blender() -> str | None:
    override = os.environ.get("NODECUE_BLENDER")
    if override and Path(override).exists():
        return override
    for candidate in (
        "/Applications/Blender.app/Contents/MacOS/Blender",
        shutil.which("blender"),
    ):
        if candidate and Path(candidate).exists():
            return candidate
    return None


@pytest.mark.skipif(_blender() is None, reason="no Blender executable found")
def test_runtime_scripts_in_blender():
    """The real checks: read-only reads, targeted cleanup, library guard."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "checks.json"
        proc = subprocess.run(
            [_blender(), "-b", "--factory-startup", "--python", str(GOLDEN), "--", str(out)],
            capture_output=True,
            text=True,
            timeout=600,
        )
        assert out.exists(), proc.stdout[-4000:] + proc.stderr[-4000:]
        payload = json.loads(out.read_text(encoding="utf-8"))

    failed = [c for c in payload["checks"] if not c["pass"]]
    assert not failed, json.dumps(failed, indent=1)[:4000]
    assert proc.returncode == 0
    assert payload["total"] >= 40
