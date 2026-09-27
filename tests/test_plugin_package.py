"""Static package contract for the Codex plugin metadata files.

These tests read committed JSON. They do not start a host, install a plugin,
or prove live discovery.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
MCP = ROOT / ".mcp.json"


def _load(path: Path) -> dict:
    assert path.is_file(), f"missing {path.relative_to(ROOT)}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_codex_plugin_json_is_valid_and_names_this_package():
    data = _load(PLUGIN)
    assert data["name"] == "blender-node-skills"
    assert data["version"]
    assert data["license"] == "MIT"
    assert "geometry-nodes" in " ".join(data.get("keywords") or [])


def test_codex_plugin_points_at_committed_skills_and_mcp_entry():
    data = _load(PLUGIN)
    skills = data["skills"]
    mcp = data["mcpServers"]
    assert skills in {"./skills/", "skills/", "./skills"}
    skills_dir = (ROOT / skills).resolve()
    assert skills_dir.is_dir()
    assert (skills_dir / "geometry-nodes" / "SKILL.md").is_file()
    mcp_path = (ROOT / mcp).resolve()
    assert mcp_path.is_file()
    assert mcp_path == MCP.resolve()


def test_codex_plugin_does_not_own_skill_workflow():
    """Plugin metadata is install/entry only. Skill knowledge stays in skills/."""
    text = PLUGIN.read_text(encoding="utf-8")
    for token in ("nodes.tsv", "probe_node.py", "read_graph.py", "versions.md"):
        assert token not in text


def test_mcp_json_declares_blender_stdio_entry():
    data = _load(MCP)
    blender = data["mcpServers"]["blender"]
    assert blender["command"] == "blender-mcp"
    assert blender.get("args") == []


def test_plugin_and_mcp_carry_no_machine_local_paths():
    for path in (PLUGIN, MCP):
        text = path.read_text(encoding="utf-8")
        for bad in ("/Users/", "/home/", "C:\\"):
            assert bad not in text
