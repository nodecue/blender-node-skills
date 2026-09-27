# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history. When the task is finished, clear or overwrite with an empty template.

**Task:** Issue #10 final documentation cutover — declare public GitHub `main` authoritative.

**Done:**

- Public `main` stated as the sole product and development source in `AGENTS.md`, `CONTRIBUTING.md`, README files, and `docs/CURRENT.md`.
- Codex plugin described as merged into public `main`, not as a tagged plugin release.
- Fresh-clone static evidence, installed-plugin read-only evidence, and Blender runtime pytest evidence recorded separately.
- `docs/research/github-primary-inventory.md` updated as a post-acceptance record.
- `docs/decisions/github-primary.md` records the authority decision.
- `docs/cleanup/old-local-source.md` is a non-destructive archive/cleanup manifest. Nothing was deleted.

**Not done:**

- Push, pull request, merge, and Issue #10 close (this local commit only).
- Issue #6 deterministic Geometry Nodes layout.
- New-machine/VM, Claude, Pi, plugin end-to-end mutation, or image acceptance.

**Files touched:**

- `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `README.zh-CN.md`
- `docs/CURRENT.md`, `docs/HANDOFF.md`
- `docs/research/github-primary-inventory.md`
- `docs/decisions/github-primary.md`
- `docs/cleanup/old-local-source.md`

**Risks / landmines:**

- Do not treat the old local checkout as a second source or copy it back into public `main`.
- Do not delete or instruct deletion of that checkout; the cleanup manifest does not authorize deletion.
- Keep static tests, installed-plugin proof, and Blender runtime proof distinct.
- Merge, release, and issue close remain separate actions. Release still needs explicit authorization.

**Next action:** Open and merge the documentation PR for this commit, then close Issue #10. Next product work is Issue #6.

**Last verified:** 2026-09-27
