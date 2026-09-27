# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history.

**Task:** Issue #6 deterministic Geometry Nodes layout (skill/runtime helper).

**Done:**

- `docs/CURRENT.md` names Issue #6 as the current slice.
- `skills/geometry-nodes/scripts/layout_graph.py` with `check` (read-only) and `apply` (authorized mutation).
- `apply` snapshots every node's parent and local location. A failed protected-node check rolls back parent and location in parent-safe order (`rolled_back`).
- Protected nodes are compared with `_PROTECTED_EPS` (1e-5), separate from layout `_EPS` (0.51).
- Golden case: authorized frame `Keep` with protected child `Off Trunk`; apply is rejected and parent/local/absolute stay put.
- `read_graph.py` reports `location`, `location_absolute`, `width`, `height`, and `dimensions` when present.
- SKILL.md routes `layout_graph.py`. Explain may check; Build/Edit may apply to an explicit authorized set.
- Commit `e0fb710` pushed on `codex/issue-6-layout`; PR #14 is open and mergeable.

**Not done:**

- Merge, Issue close, and release (separate actions; none performed).
- Inferring semantic grouping (out of scope by design).
- Plugin-owned layout workflow.

**Files touched:**

- `docs/CURRENT.md`, `docs/HANDOFF.md`
- `skills/geometry-nodes/SKILL.md`
- `skills/geometry-nodes/scripts/read_graph.py`
- `skills/geometry-nodes/scripts/layout_graph.py` (new)
- `tests/test_skill_runtime_scripts.py`
- `tests/test_skill_entrypoint.py`
- `tests/golden/run_skill_runtime_scripts.py`

**Last verified:** 2026-09-27

- `NODECUE_BLENDER=/Applications/Blender.app/Contents/MacOS/Blender /tmp/nodecue-issue6-venv/bin/python -m pytest tests -q` — 182 passed, 1 optional test skipped; Blender runtime integration passed.
- Direct: `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tests/golden/run_skill_runtime_scripts.py -- /tmp/layout-checks.json` — 103/103 passed, Blender 5.2.2 LTS.
- `python tools/gen_nodes_tsv.py --check` — current, 368 rows.

**Next action:** Review and accept PR #14. Merge, Issue close, and release remain separate actions.
