# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history.

**Task:** Issue #23 compact `read_graph.py` output and eliminate duplicate runpy/MCP payloads.

**Done:**

- PR #14 merged and Issue #6 closed after acceptance review.
- PR #20 and PR #22 merged; Issues #18 and #21 are closed.
- The active `main` ruleset requires pull requests and both checks, blocks branch deletion and force-push, and retains administrator bypass for recovery.
- Issue #23 created with the confirmed compact/full and stdout-channel acceptance contract.
- `read_graph.py` now defaults to `detail: "summary"`, returning tree/users, names, selection, trunk, and deterministic issues without full sockets, properties, links, or interface.
- Explicit `detail: "full"` preserves the previous detailed/scoped/paginated payload.
- `NODECUE_PARAMS` runpy invocation returns only through `result`; CLI invocation still prints one JSON document.
- Static contract tests and Blender golden checks cover summary fields, explicit full mode, runpy silence, one-document CLI output, and a 54-node size/reduction target.

**Not done:**

- Live Blender golden execution for Issue #23: direct macOS background Blender is the known SIGSEGV path and was not retried. Run through an already-running Blender MCP/Python channel when available.
- Commit, push, PR, review, merge, Issue #23 close, or release.
- Issue #15 `find_nodes` or Issue #19 VM evaluation.

**Files touched:**

- `docs/CURRENT.md`, `docs/HANDOFF.md`
- `skills/geometry-nodes/SKILL.md`
- `skills/geometry-nodes/references/versions.md`
- `skills/geometry-nodes/scripts/read_graph.py`
- `tests/test_skill_runtime_scripts.py`
- `tests/golden/run_skill_runtime_scripts.py`

**Risks / landmines:**

- Direct background Blender on this macOS host terminates with the known `ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` SIGSEGV. Do not repeat that path; use an already-running Blender MCP/Python channel.
- Summary findings are intentionally limited to facts already computed by trunk readback. Do not expand this slice into Issue #17's general structured-delivery system.

**Next action:** Review the patch, commit and push, create the Issue #23 PR, and wait for both hosted checks. Live runtime evidence remains separate.

**Last verified:** 2026-10-01

- Static `read_graph.py` contract tests: 45 passed, 1 live test deselected.
- Filtered public suite: 181 passed, 1 skipped, 2 known background-Blender cases deselected.
- `python3 tools/gen_nodes_tsv.py --check`: current, 368 rows.
- `git diff --check`: clean before final documentation update; rerun before commit.
