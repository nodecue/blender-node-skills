# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history.

**Task:** Issue #21: remove project memory and historical comparison material; add concise official Blender Lab MCP first-use setup.

**Done:**

- Updated `docs/CURRENT.md` first: this cleanup precedes Issue #15 `find_nodes`; resume Issue #19 paired VM acceptance after #15.
- Removed the `NODECUE.md` project-memory workflow from the shipped Geometry Nodes entrypoint, reuse reference, and both READMEs.
- Removed the pre-v0.7 comparison section and historical call/time claims from both READMEs; removed its two image assets.
- Added concise bilingual setup for the official Blender Lab MCP server/extension and a read-only smoke prompt for version, current file, and active object.
- Kept `.mcp.json` as the existing `blender-mcp` command with no arguments.
- Removed Blender Manual attribution from both READMEs.
- Added Blender 5.2 modifier-input and Capture Attribute Selection notes to `references/versions.md`; the Capture Attribute version boundary is checked against the repository's live dumps.
- Added a concise host-specific background-Blender failure lesson with the safe fallback.

**Not done:**

- Push, PR creation, merge, Issue close, release, `find_nodes`, and VM evaluation are not done.

**Files touched:**

- `docs/CURRENT.md`, `docs/HANDOFF.md`
- `README.md`, `README.zh-CN.md`
- `skills/geometry-nodes/SKILL.md`
- `skills/geometry-nodes/references/reuse.md`
- `skills/geometry-nodes/references/versions.md`
- `docs/lessons/headless-blender-macos.md`
- `tests/test_skill_entrypoint.py`, `tests/test_skill_references.py`, `tests/test_plugin_package.py`
- Removed `docs/images/comparison-no-skill.png` and `docs/images/comparison-with-skill.png`

**Risks / landmines:**

- Upstream setup can change. The README links to the official repository and keeps the server setup short; no server code is vendored.
- The official upstream setup uses `pip install git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp`, a separately installed Blender extension, and starting its server from extension preferences.
- `.mcp.json` remains the NodeCue package entry; host-specific MCP config file locations are not documented here.
- The modifier-input API/error note was supplied as a confirmed Blender 5.2 fact; repository dumps do not record modifier writes, so it was documented as version-bound and was not independently exercised in this turn.

**Next action:** Hand off the local commit for review. Do not push or create a PR in this slice.

**Last verified:** 2026-10-01

- `python3 tools/gen_nodes_tsv.py --check` — current, 368 rows.
- Filtered public suite, run in an available local test environment with cache disabled and the two background-Blender cases deselected — 178 passed, 1 skipped, 2 deselected.
- The complete requested pytest command was also attempted. Both deselected tests start host Blender in background and crashed with `ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` (return code -11); no repeated headless attempt was made.
- The host's default `python3` has no `pytest` module. The filtered run used an already-available local test environment.
- `git diff --check` — clean.
