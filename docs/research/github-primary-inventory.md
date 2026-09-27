# GitHub-primary inventory (Issue #10 validation slice)

This note records what this public repository now owns, what remains historical
or private, and what is still excluded. It does not declare the GitHub-primary
cutover complete. Old local trees stay in place until a later slice says
otherwise.

## Migrated authoritative product and maintenance inputs

These now live in this repository and are the inputs a fresh clone uses:

- Geometry Nodes skill at `skills/geometry-nodes/` (`SKILL.md`, references,
  runtime scripts).
- Codex plugin static packaging: `.codex-plugin/plugin.json`, `.mcp.json`.
- Node identity dumps and TSV evidence under `docs/node-dumps/`.
- TSV generator and review decisions: `tools/gen_nodes_tsv.py`,
  `tools/nodes_tsv_review.json`.
- Dump helpers: `tools/introspect_nodes.py`, `tools/dump_tsv_evidence.py`.
- Focused pytest coverage under `tests/` for skill structure, runtime scripts,
  field-shape vocabulary, TSV generation, and the plugin JSON contract.
- Agent governance: `AGENTS.md`, `docs/PRODUCT.md`, `docs/CURRENT.md`,
  `docs/HANDOFF.md`, `docs/learnings.md`.

`skills/geometry-nodes/references/nodes.tsv` is regenerated from the dumps and
review file in this repo. `python tools/gen_nodes_tsv.py --check` is the
idempotence gate.

## Historical or private (not in public git)

These remain outside this repository. They are not a second public product
authority, and they are not deleted by this slice:

- Prior development checkout and its dual-authority / release-copy process.
- Private corpora, session transcripts, credentials, machine artifacts.
- Trap-measurement and runtime-baseline experiment notes cited as evidence
  behind nine `nodes.tsv` notes (those notes themselves are reviewed and
  shipped; the original experiment trees are not).
- Full manuals and other unpublished documentation.

## Deliberately excluded

Do not migrate these as part of Issue #10:

- Retired add-on, sidecar, socket server, and gn_mcp_server.
- Shader or Compositor runtime.
- find_nodes and Jev.
- Issue #6 deterministic layout.
- Release-sync implementation and tests.
- Private or local asset libraries and `.blend` files.
- Dump-diff tooling and skip-version diffs that are not required to regenerate
  `nodes.tsv`.

## Still required before Issue #10 can close

1. **Fresh-clone validation** of skill files, `pytest`, and
   `tools/gen_nodes_tsv.py --check` on a machine that has only this repository
   and the documented dev dependency.
2. **Plugin validation** on a host that installs from this repository (static
   JSON tests here do not prove live discovery).
3. **Live read-only Blender check** of version, file state, and graph
   introspection through the skill scripts.
4. **Final authority declaration** in `docs/CURRENT.md` that public `main` is
   the product source, plus a later cleanup manifest. No deletion of any old
   local tree in that step unless a later issue explicitly authorizes it.
