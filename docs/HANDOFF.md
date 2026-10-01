# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history.

**Task:** Issue #15 deterministic agent-facing `find_nodes` baseline.

**Done:**

- PR #14, #20, #22, and #24 are merged; Issues #6, #18, #21, and #23 are closed.
- The active `main` ruleset requires pull requests and both checks, blocks branch deletion and force-push, and retains administrator bypass for recovery.
- Added `scripts/find_nodes.py`: deterministic text ranking over the reviewed `nodes.tsv`, with optional 4.5/5.0/5.1/5.2 filtering and stable tie-breaking.
- Results remain routing candidates only and explicitly require live `probe_node.py` inspection before wiring.
- Kept `nodes.tsv` as the reviewed source and fallback; no Jev, embedding, model, network, or Blender dependency was added.
- Added a committed 15-intent evaluation set and `tools/eval_find_nodes.py` for reproducible recall, top-1, and irrelevant-result metrics.
- Updated the skill loop and package/readme discovery surfaces. `find_nodes.py` runs in ordinary host Python; Blender-facing scripts still run through the live execution channel.

**Not done:**

- Commit, push, PR, review, merge, Issue #15 close, or release.
- Jev experiment or Issue #19 VM evaluation.

**Files touched:**

- `README.md`, `README.zh-CN.md`
- `docs/PRODUCT.md`, `docs/CURRENT.md`, `docs/HANDOFF.md`
- `skills/geometry-nodes/SKILL.md`
- `skills/geometry-nodes/scripts/find_nodes.py` (new)
- `tools/eval_find_nodes.py` (new)
- `tests/fixtures/find_nodes_cases.json` (new)
- `tests/test_find_nodes.py` (new)
- `tests/test_plugin_package.py`, `tests/test_skill_entrypoint.py`, `tests/test_skill_runtime_scripts.py`

**Risks / landmines:**

- The fixed baseline is deliberately small and lexical. Its top-5 irrelevant-result rate is visible rather than hidden; do not claim general semantic retrieval from 15 cases.
- Aliases are a small deterministic query vocabulary, not node/socket authority. Availability still comes from `nodes.tsv`, and all live identities must be probed in Blender.
- Jev remains an optional later experiment against this exact baseline and cannot become a hard dependency.

**Next action:** Review, commit, push, create the Issue #15 PR, and wait for both required hosted checks.

**Last verified:** 2026-10-01

- Fixed 15-intent baseline at 5 results: recall 1.0, top-1 accuracy 1.0, irrelevant-result rate 0.6667 using the committed relevant-candidate labels.
- Filtered public suite: 194 passed, 1 skipped, 2 known background-Blender cases deselected.
- `python3 tools/gen_nodes_tsv.py --check`: current, 368 rows.
- `git diff --check`: clean before final handoff update; rerun before commit.
