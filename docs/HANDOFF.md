# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history.

**Task:** Review and merge PR #22 for Issue #21 after integrating the new pull-request quality gates.

**Done:**

- PR #14 merged; Issue #6 remains open because closing it is a separate action.
- PR #20 merged and Issue #18 closed. Its workflow adds separate read-only `Static tests` and `nodes.tsv consistency` jobs; contract tests keep those gates scoped to public static checks.
- The active `main` ruleset requires pull requests and both checks, blocks branch deletion and force-push, and retains administrator bypass for recovery.
- Removed the `NODECUE.md` project-memory workflow from the shipped Geometry Nodes entrypoint, reuse reference, and both READMEs.
- Removed the pre-v0.7 comparison section and historical call/time claims from both READMEs; removed its two image assets.
- Added concise bilingual setup for the official Blender Lab MCP server/extension and a read-only smoke prompt for version, current file, and active object.
- Kept `.mcp.json` as the existing `blender-mcp` command with no arguments.
- Removed Blender Manual attribution from both READMEs.
- Added Blender 5.2 modifier-input and Capture Attribute Selection notes to `references/versions.md`; the Capture Attribute version boundary is checked against the repository's live dumps.
- Added a concise host-specific background-Blender failure lesson with the safe fallback.
- Created PR #22 and integrated the latest `main` while preserving the CI facts and Issue #21 direction.

**Not done:**

- PR #22 hosted checks, review, merge, Issue #21 close, or release.
- Issue #6 close.
- `read_graph.py` compaction, Issue #15 `find_nodes`, or Issue #19 VM evaluation.

**Files touched:**

- `.github/workflows/quality.yml`, `tests/test_ci_workflow.py` (from merged PR #20)
- `docs/CURRENT.md`, `docs/HANDOFF.md`
- `README.md`, `README.zh-CN.md`
- `skills/geometry-nodes/SKILL.md`
- `skills/geometry-nodes/references/reuse.md`
- `skills/geometry-nodes/references/versions.md`
- `docs/lessons/headless-blender-macos.md`
- `tests/test_skill_entrypoint.py`, `tests/test_skill_references.py`, `tests/test_plugin_package.py`
- Removed `docs/images/comparison-no-skill.png` and `docs/images/comparison-with-skill.png`

**Risks / landmines:**

- Upstream MCP setup can change. The README links to the official repository and keeps the server setup short; no server code is vendored.
- The modifier-input API/error note was supplied as a confirmed Blender 5.2 fact; repository dumps do not record modifier writes, so it was documented as version-bound and was not independently exercised in this turn.
- Direct background Blender on this macOS host terminates with the known `ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` SIGSEGV. Do not repeat that path; use an already-running Blender MCP/Python channel.

**Next action:** Commit and push the resolved merge, wait for both hosted checks, then review PR #22. Merge and Issue #21 close remain separate actions.

**Last verified:** 2026-10-01

- PR #20 hosted checks passed before merge: `Static tests` and `nodes.tsv consistency`.
- Issue #21 filtered suite before integrating `main`: 178 passed, 1 skipped, 2 known background-Blender cases deselected.
- `python3 tools/gen_nodes_tsv.py --check`: current, 368 rows.
- Rerun static checks and `git diff --check` after conflict resolution.
