# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history.

**Task:** Issue #18 automated pull-request quality gates.

**Done:**

- PR #14 merged as `ece4b3a`; Issue #6 remains open because Issue close is separate.
- `.github/workflows/quality.yml` adds separate `Static tests` and `nodes.tsv consistency` jobs for pull requests and pushes to `main`.
- Workflow permissions are read-only and it contains no live-host, release, secret, or VM behavior.
- `tests/test_ci_workflow.py` holds the workflow to the public command and boundary contract.
- `docs/CURRENT.md` records that `nodes.tsv` stays until Issue #15 provides measured replacement evidence.

**Not done:**

- Commit, push, PR, review, merge, or Issue #18 close.
- Live Blender/plugin/VM/image acceptance; that belongs to Issue #19.
- Issue #15 `find_nodes` implementation.
- Issue #6 close or any release.

**Files touched:**

- `.github/workflows/quality.yml` (new)
- `tests/test_ci_workflow.py` (new)
- `docs/CURRENT.md`
- `docs/HANDOFF.md`

**Last verified:** 2026-09-28

- Full local suite with Blender 5.2.2 available: 184 passed, 1 explicitly deferred documentation-rule test skipped.
- `python tools/gen_nodes_tsv.py --check`: current, 368 rows.
- Workflow YAML parses; workflow contract tests: 2 passed.

**Next action:** Commit, push, and open the Issue #18 PR; verify both GitHub checks run on the hosted runner.
