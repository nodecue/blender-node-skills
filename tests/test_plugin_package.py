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


def test_readmes_close_the_official_mcp_first_use_loop():
    for readme in (ROOT / "README.md", ROOT / "README.zh-CN.md"):
        text = readme.read_text(encoding="utf-8")
        assert "https://projects.blender.org/lab/blender_mcp" in text
        install_command = "pip install git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp"
        assert install_command in text
        assert "https://lab.blender.org/" in text
        assert "blender-mcp" in text
        assert "stdio" in text.lower()
        assert "bpy.app.version_string" in text
        assert "bpy.data.filepath" in text
        assert "active object name" in text or "活动对象名称" in text
        assert ".mcp.json" in text
        assert "NODECUE.md" not in text
        assert "docs/images/comparison-" not in text
        assert "CC-BY-SA" not in text
        assert "docs.blender.org/manual" not in text


def test_readmes_do_not_keep_the_pre_v07_comparison_claims():
    for readme in (ROOT / "README.md", ROOT / "README.zh-CN.md"):
        text = readme.read_text(encoding="utf-8").lower()
        old_claims = ("4 minutes 17 seconds", "5 minutes 46 seconds", "4 分 17 秒", "5 分 46 秒")
        for old_claim in old_claims:
            assert old_claim not in text
        assert "dated example from a pre-v0.7 skill" not in text
        assert "v0.7 之前的历史示例" not in text


def test_plugin_and_mcp_carry_no_machine_local_paths():
    for path in (PLUGIN, MCP):
        text = path.read_text(encoding="utf-8")
        for bad in ("/Users/", "/home/", "C:\\"):
            assert bad not in text
