# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history. When the task is finished, clear or overwrite with an empty template.

**Task:** Issue #10 first slice — self-contained agent governance files (AGENTS, PRODUCT, CURRENT, HANDOFF, learnings).

**Done:**

- New clone of public `main` at `a8de11f`.
- Branch `issue-10-github-primary` created on that clone.
- Issue #2 was locally integrated into the old development source and closed with a public factual comment; Issues #3/#4/#5 were merged into public main through PR #7/#8/#9 and closed.
- Five governance files added in this slice.

**Not done:**

- Tests/tools inventory for what must live in public git.
- Retirement of old dual-authority / sync process (no deletion of any old tree).
- Fresh-clone acceptance of skill, plugin, and live read-only.
- PR for this slice (commit locally only unless the user asks to push).

**Files touched:**

- `AGENTS.md`
- `docs/PRODUCT.md`
- `docs/CURRENT.md`
- `docs/HANDOFF.md`
- `docs/learnings.md`

**Risks / landmines:**

- Do not copy old dual-authority, release-copy, or sync-release rules into these files.
- Do not delete or instruct deletion of any old local repo.
- Do not claim unverified hosts (new VM, Claude, Pi) or plugin end-to-end mutation/image as done.
- Do not announce GitHub-primary migration complete; CURRENT still says in progress.

**Next action:** Independent review is complete; next push branch and open the first Issue #10 PR; inventory/tests/tools remain later slices.

**Last verified:** 2026-09-27
