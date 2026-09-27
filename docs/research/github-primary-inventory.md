# GitHub-primary inventory (Issue #10 post-acceptance)

This note records what public GitHub `main` owns after Issue #10 acceptance,
what remains historical or private, and what stays excluded. Public `main` is
the sole product and development source. The old local checkout is an archive
candidate, not a second authority.

Public PR #11 added cold-start governance. Public PR #12 migrated public
maintenance evidence, tools, and tests and is merged in `main`
`007a98e9d1e5398f0c4f3cf6932451e9a17f97f9`.

## Migrated authoritative product and maintenance inputs

These live in this repository and are the inputs a fresh clone uses:

- Geometry Nodes skill at `skills/geometry-nodes/` (`SKILL.md`, references,
  runtime scripts).
- Codex plugin static packaging: `.codex-plugin/plugin.json`, `.mcp.json`.
  The plugin is merged into public `main`. It is not a tagged plugin release.
- Node identity dumps and TSV evidence under `docs/node-dumps/`.
- TSV generator and review decisions: `tools/gen_nodes_tsv.py`,
  `tools/nodes_tsv_review.json`.
- Dump helpers: `tools/introspect_nodes.py`, `tools/dump_tsv_evidence.py`.
- Focused pytest coverage under `tests/` for skill structure, runtime scripts,
  field-shape vocabulary, TSV generation, and the plugin JSON contract.
- Agent governance: `AGENTS.md`, `docs/PRODUCT.md`, `docs/CURRENT.md`,
  `docs/HANDOFF.md`, `docs/learnings.md`, `docs/decisions/github-primary.md`,
  `docs/cleanup/old-local-source.md`.

`skills/geometry-nodes/references/nodes.tsv` is regenerated from the dumps and
review file in this repo. `python tools/gen_nodes_tsv.py --check` is the
idempotence gate.

## Acceptance evidence (keep these layers distinct)

A separate fresh clone of GitHub `main` passed:

- **Static tests.** `python -m pytest tests -q`: 172 passed, 1 skipped. The skip
  was the optional real-Blender runtime test without `NODECUE_BLENDER`.
- **TSV check.** `python tools/gen_nodes_tsv.py --check`: current, 368 rows.
- **Codex plugin validator:** passed (static packaging, not live host
  discovery).

From that same fresh clone, setting `NODECUE_BLENDER` explicitly produced
**Blender runtime proof**:

- portable Blender 5.1.2: `tests/test_skill_runtime_scripts.py` 36 passed.
- target Blender 5.2.2: the same 36 passed.

**Installed-plugin proof** remains narrower and earlier: a genuinely fresh
Codex task auto-discovered the skill and Blender MCP entry and completed live
read-only against portable Blender 5.1.2. Separate host tests proved
mutation/readback/viewport on 5.1.2 and 5.2.2. Those host tests were not the
same fresh-plugin end-to-end mutation or image run.

Unverified: GitHub install on a new machine or VM; Claude; Pi; other hosts;
plugin end-to-end mutation; image acceptance.

## Historical or private (not in public git)

These remain outside this repository. They are not a second public product
authority. This record does not delete them:

- Prior development checkout and its former local-only process.
- Private corpora, session transcripts, credentials, machine artifacts.
- Trap-measurement and runtime-baseline experiment notes cited as evidence
  behind nine `nodes.tsv` notes (those notes themselves are reviewed and
  shipped; the original experiment trees are not).
- Full manuals and other unpublished documentation.

See `docs/cleanup/old-local-source.md` for what may later be archived and what
must be retained.

## Deliberately excluded

Do not migrate these as part of Issue #10:

- Retired add-on, sidecar, socket server, and gn_mcp_server.
- Shader or Compositor runtime.
- find_nodes and Jev.
- Issue #6 deterministic layout.
- Former local-only release-sync implementation and tests.
- Private or local asset libraries and `.blend` files.
- Dump-diff tooling and skip-version diffs that are not required to regenerate
  `nodes.tsv`.

## Issue #10 status

Authority cutover is declared in documentation. Push, PR merge, and Issue close
remain separate later actions. Next current product work is Issue #6.
