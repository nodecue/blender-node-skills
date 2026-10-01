# CURRENT

Living direction for agents. Update this when the user changes mind. Do not treat chat history as more authoritative than this file.

## Established

- Public GitHub `main` is the sole authoritative product and development source. GitHub Issues and pull requests are the execution path. Issue #10 is complete and closed.
- Shipped product is the v0.7 Geometry Nodes skill at `skills/geometry-nodes/`, with build/edit/explain judgment, version routing, live introspection, verification, and teaching structure.
- Plugin installs, environments, and provides entry points only. It does not own skill knowledge. The Codex plugin is merged into public `main`. It is not a tagged plugin release.
- Live Blender is authority for node/socket/property/RNA identity and legal values.
- Geometry Nodes is the only shipped runtime. Shader/Compositor, input-reference reconstruction, and automatic evaluated-output QA are not shipped.
- Fresh-clone static validation from public `main` passed: `python -m pytest tests -q` (172 passed, 1 skipped without `NODECUE_BLENDER`); `python tools/gen_nodes_tsv.py --check` current, 368 rows; Codex plugin validator passed. Those static checks are distinct from live Blender and from installed-plugin host proof.
- With `NODECUE_BLENDER` set on that same fresh clone: portable Blender 5.1.2 and target Blender 5.2.2 each ran `tests/test_skill_runtime_scripts.py` with 36 passed. That is Blender runtime proof, not host plugin discovery.
- Installed-plugin acceptance remains narrower: a genuinely fresh Codex task auto-discovered the skill and Blender MCP entry and completed live read-only against portable Blender 5.1.2. Separate host tests proved mutation/readback/viewport on 5.1.2 and 5.2.2; those were not the same fresh-plugin end-to-end mutation/image run. New machines/VMs, Claude, and Pi are unverified.
- Issue #6 deterministic layout is merged in PR #14 and closed after acceptance review.
- Issue #18 automated pull-request quality gates is merged in PR #20 and closed. Pull requests run separate `Static tests` and `nodes.tsv consistency` jobs; the active `main` ruleset requires a pull request and both checks, prevents deletion and force-push, and retains administrator bypass for recovery.
- Keep `nodes.tsv` as the reviewed routing index for now. Only reduce its role after Issue #15 measures that `find_nodes` preserves recall, version routing, and maintainability; do not remove it on anecdotal results.
- Future work goes Issue → branch/worktree → PR → review → merge. Merge, release, and issue close are separate actions. Jev may only be an optional measured reranking experiment after a deterministic `find_nodes` baseline, not a dependency.
- GitHub Issues are the execution backlog. Do not create `docs/BACKLOG.md`.
- Large manuals, experiments, private corpora, session transcripts, absolute paths, credentials, `.blend` files, and machine artifacts stay out of the public repo.
- The old local checkout is a preserved archive candidate. It is not a second authority. Do not copy changes from it back into public `main`. See `docs/cleanup/old-local-source.md`. This slice does not delete it.

## Current slice

Issue #15: add a deterministic agent-facing `find_nodes` baseline over the reviewed `nodes.tsv` routing index.

- Accept a short intent query, optional Blender version, and result limit; return a concise, stable candidate list with match reasons.
- Filter version availability before ranking so a version-specific query never recommends an unavailable node.
- Commit a fixed intent evaluation set and report recall plus irrelevant-result rate at a fixed cutoff.
- Direct every result to live `probe_node.py` inspection before wiring; the query never claims socket, property, or legal-value authority.
- Keep `nodes.tsv` as the reviewed source and deterministic fallback. Do not add Jev or another model dependency in this slice.

Documented development path for a fresh clone:

```bash
pip install -r requirements-dev.txt
python -m pytest tests -q
python tools/gen_nodes_tsv.py --check
```

Those commands cover committed skill, TSV, and plugin-JSON tests. They do not prove live host plugin discovery or live Blender behavior.

## Out of scope / do not do

- Implement Jev, Shader, or Compositor in this slice.
- Add persistent helpers/caching inside Blender or vendor the official MCP server.
- Add live Blender, GUI, MCP, VM, screenshot, or agent runs to the fast PR workflow.
- Remove or deprecate `nodes.tsv` before measured `find_nodes` evidence exists.
- Expand host claims beyond what is already verified.
- Start Issue #19 VM tests as part of this cleanup.
- Rewrite CHANGELOG or unpublished Shader/Compositor issue drafts.
- Delete, rename, move, or empty any old local NodeCue directory.
- Restore a second product source or copy unpublished local work back into public `main`.

## Open

- Host plugin discovery on new machines/VMs, Claude, and Pi.
- Issue #15 measured `find_nodes` baseline after the PR gates land.
- Issue #19 paired no-skill/skill VM acceptance with refreshed image evidence.
- Whether later slices add measured reranking (Jev) — optional experiment only.
- Where manuals, private corpora, and private evidence stay (they do not land in public git).
- Later archive of the old local checkout, only after the cleanup manifest checks, and only with explicit later authorization.

## Experimental

None in this slice.

## Acceptance sketch

Someone should be able to:

1. Search shipped skill/README content and find no `NODECUE.md` memory workflow or Blender Manual attribution.
2. Read the concise official MCP setup pointer and see that `.mcp.json` invokes the same `blender-mcp` stdio command.
3. Follow the read-only smoke prompt and receive Blender version, current file, and active object from the live host.
4. Find no old comparison images, elapsed-time claims, or MCP-call-count claims in either README.
5. Open a pull request and see required `Static tests` and `nodes.tsv consistency` jobs while keeping those static gates distinct from live Blender acceptance.
