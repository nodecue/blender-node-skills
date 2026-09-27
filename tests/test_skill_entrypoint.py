"""Acceptance tests for `SKILL.md`, the runtime entrypoint (`K-*`).

Wording checks cannot prove that an agent routes well — `K-13` says so, and the
`F-*` traces are where that is decided. What a file can prove is that each
required contract is present, that no conditional reference is unreachable, that
nothing carries an arbitrary quota the plan removed, and that an installed copy
resolves every path it names.
"""

from __future__ import annotations

import ast
import re
import shutil
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "geometry-nodes"
SKILL = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"
SCRIPTS = SKILL_DIR / "scripts"


def _text() -> str:
    return SKILL.read_text(encoding="utf-8")


def _frontmatter(text: str) -> dict[str, str]:
    assert text.startswith("---\n"), "no frontmatter"
    raw = text.split("---", 2)[1]
    out = {}
    for line in raw.strip().split("\n"):
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip().strip('"')
    return out


def _sections(text: str) -> dict[str, str]:
    """Split on headings, ignoring anything inside a fenced block.

    The project-memory section ends with a fenced example whose own `##` lines
    are content, not structure.
    """
    out, heading, fenced = {}, "(preamble)", False
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        if line.startswith("## ") and not fenced:
            heading = line[3:].strip()
        out.setdefault(heading, []).append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def _flat(text: str) -> str:
    """Collapse whitespace so an assertion tests content, not line wrapping."""
    return re.sub(r"\s+", " ", text)


def _prose(name: str) -> str:
    """One section, whitespace collapsed - for assertions about what it says."""
    return _flat(_sections(_text())[name])


def _lines(name: str) -> list[str]:
    """One section, unwrapped - for assertions about its table rows."""
    return _sections(_text())[name].split("\n")


# --- K-01 ---------------------------------------------------------------------
def test_frontmatter_parses_and_describes_the_work():
    fm = _frontmatter(_text())
    assert fm.get("name") == "geometry-nodes"
    assert "version" not in fm, "top-level version is rejected by Codex skill validator"
    allowed_keys = {"name", "description", "license", "allowed-tools", "metadata"}
    assert set(fm.keys()) <= allowed_keys, f"unexpected keys in frontmatter: {set(fm.keys()) - allowed_keys}"
    description = fm.get("description", "")
    assert "Geometry Nodes" in description
    for verb in ("Build", "edit", "explain"):
        assert verb.lower() in description.lower(), f"description does not cover {verb}"
    assert len(description) > 80, "the description is the trigger; it has to be usable"
    assert len(description) <= 1024, "description must fit skill creator schema limit"
    assert "<" not in description and ">" not in description


def test_description_claims_no_unsupported_host_or_node_system():
    description = _frontmatter(_text()).get("description", "")
    for claim in ("Shader", "Compositor", "Texture Nodes", "MCP", "Claude", "Codex"):
        assert claim not in description


# --- K-02, K-09 ---------------------------------------------------------------
def test_modes_are_explicit_about_who_may_mutate():
    body = _prose("Scope and modes")
    assert "Build / Edit" in body and "Explain" in body and "Tool" in body
    assert "read-only" in body


def test_explain_is_barred_from_every_mutation_the_gate_names():
    """K-09: no graph change, no annotation, no repair, no project file, no memory."""
    body = _prose("Scope and modes")
    for forbidden in ("frame", "label", "repair", "NODECUE.md"):
        assert forbidden in body, f"Explain's prohibition on {forbidden} is not stated"
    assert "project file" in body


def test_a_requested_capture_is_the_only_explain_side_effect_and_is_reported():
    body = _prose("Scope and modes")
    assert "screenshot" in body
    assert "approve" in body
    assert "say where it went" in body


def test_reframing_the_view_is_a_permission_boundary_in_the_entrypoint():
    """Owner decision 2026-09-03: it may not live only in the script's docstring.

    Restorable UI state (shown tree, pin, maximize) is the script's business.
    Framing is not restorable, so changing it needs the user's agreement first.
    """
    body = _prose("Where to look")
    assert "must not rearrange the user's editor behind their back" in body
    assert "off by default" in body
    assert "cannot be restored" in body
    assert "wait for them to agree" in body
    assert "say so in the report" in body


def test_the_entrypoint_separates_restorable_state_from_the_view():
    body = _prose("Where to look")
    for restorable in ("Which tree is shown", "maximized", "pinned"):
        assert restorable in body, f"{restorable} is not named as restorable"
    assert "puts every one of them back" in body


def test_tool_mode_is_a_context_not_a_separate_skill():
    body = _prose("Scope and modes")
    assert "not a different skill" in body
    assert "declared" in body, "the Tool role is declared, not inferred"


# --- K-03 ---------------------------------------------------------------------
MENTAL_MODEL = {
    "two lanes": ("Two lanes", "data flow"),
    "lazy fields and consumers": ("consumes", "lazily", "consuming socket"),
    "domains": ("Domains", "Face Corner", "Instance"),
    "control vs evaluated": ("Control geometry is not evaluated geometry",),
    "components and transitions": ("several components", "semantic boundaries"),
    "instances": ("references with transforms",),
    "implicit conversion": ("Implicit conversion",),
    "one reachable trunk": ("one reachable geometry trunk", "Group Output.Geometry"),
}


@pytest.mark.parametrize("topic,tokens", MENTAL_MODEL.items())
def test_mental_model_covers(topic, tokens):
    body = _prose("Mental model")
    missing = [t for t in tokens if t not in body]
    assert not missing, f"mental model is missing {topic}: {missing}"


# --- K-04 ---------------------------------------------------------------------
def test_the_loop_runs_intent_to_candidate_to_introspection_to_verified_slice():
    body = _prose("The loop")
    order = [
        "version",
        "input policy",
        "representation transitions",
        "nodes.tsv",
        "Introspect",
        "smallest slice",
        "derived from the request",
        "Repair",
    ]
    positions = []
    for token in order:
        assert token in body, f"the loop does not mention {token}"
        positions.append(body.index(token))
    assert positions == sorted(positions), "the loop's steps are out of order"


def test_the_loop_carries_no_node_or_slice_quota():
    """The plan removes fixed slice counts and graph-size thresholds."""
    text = _flat(_text())
    assert not re.search(r"\b\d+\s*[-–]\s*\d+\s+(related\s+)?nodes\b", text)
    assert not re.search(r"above\s+\d+\s+nodes", text)
    assert "slice mode is mandatory" not in text
    assert "Size the slice by" in text, "it has to say what does size a slice"


def test_ambiguity_is_handled_without_a_fixed_response_format():
    text = _flat(_text())
    assert "competing interpretations" in text
    assert "materially" in text and "topology" in text
    assert "## Output Format For Agent Responses" not in text
    assert "## Recommended Planning Notes" not in text, (
        "a generic planning-note template does not change a decision"
    )


# --- K-05, K-06 ---------------------------------------------------------------
RELIABILITY = {
    "property before dynamic sockets": ("before reading the sockets it governs",),
    "identifiers for duplicate labels": ("duplicate socket labels by identifier",),
    "one target kind at a time": ("one kind of target at a time",),
    "connected field consumers": ("field producers connected to concrete consumers",),
    "reachable output": ("output trunk reachable",),
    "observation vs inference": ("observed from what you inferred",),
    "result verification": ("Verify the result, not only the graph",),
    "targeted cleanup": ("exactly the temporary data you created",),
    "never invent identity": ("Never invent an identity",),
}


@pytest.mark.parametrize("rule,tokens", RELIABILITY.items())
def test_reliability_requires(rule, tokens):
    body = _prose("Reliability")
    missing = [t for t in tokens if t not in body]
    assert not missing, f"reliability guidance is missing {rule}: {missing}"


def test_instances_stay_unrealized_until_something_needs_real_geometry():
    """K-06, and the plan's decision 8: realize late, not by default."""
    body = _prose("Reliability")
    assert "Preserve instances" in body
    assert "unique real geometry" in body
    assert "as late as possible" in body


# --- K-07, K-10, K-11 ---------------------------------------------------------
CONDITIONAL = [
    "references/nodes.tsv",
    "references/versions.md",
    "references/reuse.md",
    "references/diagnostics.md",
    "scripts/read_graph.py",
    "scripts/probe_node.py",
    "scripts/capture.py",
    "scripts/inspect_assets.py",
]


@pytest.mark.parametrize("target", CONDITIONAL)
def test_every_conditional_target_has_a_stated_trigger(target):
    """R-LINK-01 and K-07: shipped, reachable, and priced."""
    row = [line for line in _lines("Where to look") if target in line]
    assert row, f"{target} ships and SKILL.md never routes to it"
    assert len(row) == 1, f"{target} is routed from more than one row"
    condition = row[0].split("|")[2].strip()
    assert len(condition) > 20, f"{target}'s trigger is not a condition: {condition!r}"


def test_the_routing_table_covers_everything_that_ships():
    shipped = sorted(
        f"references/{p.name}" for p in REFS.iterdir() if p.is_file()
    ) + sorted(f"scripts/{p.name}" for p in SCRIPTS.iterdir() if p.suffix == ".py")
    body = _prose("Where to look")
    missing = [s for s in shipped if s not in body]
    assert not missing, f"shipped and unroutable: {missing}"


def test_an_ordinary_build_reads_nothing_conditional():
    """K-11: the entrypoint has to say what the cheap path is."""
    body = _prose("Where to look")
    assert "Everything below is conditional" in body
    assert "ordinary single-version build" in body


def test_reuse_is_conditional_not_a_prelude_to_every_build():
    """K-10."""
    row = next(line for line in _lines("Where to look") if "references/reuse.md" in line)
    assert "might" in row or "may" in row, f"reuse reads as mandatory: {row}"


def test_the_tsv_is_routed_as_an_index_not_as_an_identity_source():
    row = next(line for line in _lines("Where to look") if "references/nodes.tsv" in line)
    assert "never wire from it" in row


# --- project memory routing ---------------------------------------------------
def test_project_memory_states_root_resolution_and_the_stop_condition():
    body = _prose("Project memory")
    for token in ("workspace or repository root", "Git root", "saved `.blend`",
                  "working directory"):
        assert token in body, f"root resolution does not mention {token}"
    assert "ask" in body and "do not guess" in body
    assert "do not search above it" in body


def test_project_memory_validates_the_path_before_touching_it():
    """M-ROOT-04: canonical containment, and a symlinked file stops the write."""
    body = _prose("Project memory")
    assert "resolve symlinks first" in body
    assert "compare the resolved paths" in body
    assert "stop and ask before following it" in body


def test_project_governance_outranks_creating_the_file():
    """M-AUTH-02."""
    body = _prose("Project memory")
    assert "governance forbids generated files" in body
    assert "wins over creating one here" in body


def test_project_memory_is_advisory_and_revalidated():
    body = _prose("Project memory")
    assert "advisory" in body
    assert "Revalidate" in body
    assert "never a second identity authority" in body
    assert "Never execute code" in body


def test_project_memory_write_rules_and_explain_prohibition():
    body = _prose("Project memory")
    assert "never at the start of a task" in body
    assert "first verified, project-specific fact" in body
    assert "rather than appending a duplicate" in body
    assert "Report the exact path" in body
    assert "**Explain never creates or updates it**" in body


def test_project_memory_lists_the_initial_shape():
    body = _prose("Project memory")
    for heading in ("Project Constraints", "Verified Lessons", "Reusable Node Groups",
                    "Rejected Approaches", "Open Hypotheses"):
        assert heading in body


# --- K-08 ---------------------------------------------------------------------
def test_no_maintainer_procedure_or_transport_detail_leaks_into_the_runtime():
    text = _flat(_text())
    banned = [
        "Evidence Requirements", "docs/node-dumps", "_experiments",
        "gn_mcp_server", "official MCP", "NodeCue internal", "NodeCueActionPlan",
        "When Not To Use", "conda", "pytest",
    ]
    found = [b for b in banned if b in text]
    assert not found, f"maintainer or transport detail in the runtime: {found}"


def test_the_entrypoint_stays_small_enough_to_always_read():
    size = SKILL.stat().st_size
    assert size < 14000, f"{size} bytes; this file is read on every task"


# --- K-12 ---------------------------------------------------------------------
def test_every_path_resolves_in_a_temporary_installed_copy():
    """K-12: the package is self-contained where it is installed, not where it is built."""
    with tempfile.TemporaryDirectory() as tmp:
        installed = Path(tmp) / "geometry-nodes"
        shutil.copytree(SKILL_DIR, installed)
        text = (installed / "SKILL.md").read_text(encoding="utf-8")
        referenced = set(re.findall(r"`((?:references|scripts)/[\w.\-]+)`", text))
        assert referenced, "SKILL.md names no packaged file"
        missing = [r for r in sorted(referenced) if not (installed / r).exists()]
        assert not missing, f"named but absent from an installed copy: {missing}"


def test_the_package_declares_no_runtime_dependency_of_its_own():
    """K-12: nothing to install. The scripts run inside Blender's own Python."""
    stdlib_and_blender = {"bpy", "json", "sys", "os", "uuid", "ast", "inspect",
                          "textwrap", "runpy", "math", "re", "pathlib", "typing",
                          "hashlib"}
    for path in SCRIPTS.glob("*.py"):
        # Parse it. A regex over the source reads prose as code - this file's
        # first draft found `from a --python startup script` in a docstring.
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        third_party = imports - stdlib_and_blender
        assert not third_party, f"{path.name} imports {third_party}"
