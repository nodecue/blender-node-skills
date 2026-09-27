# CURRENT

Living direction for agents. Update this when the user changes mind. Do not treat chat history as more authoritative than this file.

## Established

- Public GitHub `main` is the sole authoritative product and development source. GitHub Issues and pull requests are the execution path. Issue #10 is complete pending merge of this documentation cutover.
- Shipped product is the v0.7 Geometry Nodes skill at `skills/geometry-nodes/`, with build/edit/explain judgment, version routing, live introspection, verification, and teaching structure.
- Plugin installs, environments, and provides entry points only. It does not own skill knowledge. The Codex plugin is merged into public `main`. It is not a tagged plugin release.
- Live Blender is authority for node/socket/property/RNA identity and legal values.
- Geometry Nodes is the only shipped runtime. Shader/Compositor, input-reference reconstruction, and automatic evaluated-output QA are not shipped.
- Fresh-clone static validation from public `main` passed: `python -m pytest tests -q` (172 passed, 1 skipped without `NODECUE_BLENDER`); `python tools/gen_nodes_tsv.py --check` current, 368 rows; Codex plugin validator passed. Those static checks are distinct from live Blender and from installed-plugin host proof.
- With `NODECUE_BLENDER` set on that same fresh clone: portable Blender 5.1.2 and target Blender 5.2.2 each ran `tests/test_skill_runtime_scripts.py` with 36 passed. That is Blender runtime proof, not host plugin discovery.
- Installed-plugin acceptance remains narrower: a genuinely fresh Codex task auto-discovered the skill and Blender MCP entry and completed live read-only against portable Blender 5.1.2. Separate host tests proved mutation/readback/viewport on 5.1.2 and 5.2.2; those were not the same fresh-plugin end-to-end mutation/image run. New machines/VMs, Claude, and Pi are unverified.
- Next current product work is Issue #6 deterministic Geometry Nodes layout. find_nodes, Jev, Shader, and Compositor remain deferred.
- Future work goes Issue → branch/worktree → PR → review → merge. Merge, release, and issue close are separate actions. Jev may only be an optional measured reranking experiment, not a dependency.
- GitHub Issues are the execution backlog. Do not create `docs/BACKLOG.md`.
- Large manuals, experiments, private corpora, session transcripts, absolute paths, credentials, `.blend` files, and machine artifacts stay out of the public repo.
- The old local checkout is a preserved archive candidate. It is not a second authority. Do not copy changes from it back into public `main`. See `docs/cleanup/old-local-source.md`. This slice does not delete it.

## Current slice

Issue #10 final documentation cutover: declare public `main` authoritative, record acceptance evidence, and leave a non-destructive cleanup manifest.

Documented development path for a fresh clone:

```bash
pip install -r requirements-dev.txt
python -m pytest tests -q
python tools/gen_nodes_tsv.py --check
```

Those commands cover committed skill, TSV, and plugin-JSON tests. They do not prove live host plugin discovery or live Blender behavior.

## Out of scope / do not do

- Delete, rename, move, or empty any old local NodeCue directory.
- Implement Issue #6 deterministic layout in this slice.
- Ship find_nodes, Jev, or Shader/Compositor runtime.
- Expand host claims beyond what is already verified.
- Claim new-machine/VM, Claude, Pi, plugin end-to-end mutation, or image acceptance.
- Restore a second product source or copy unpublished local work back into public `main`.

## Open

- Merge of this cutover PR and close of Issue #10 (separate from this local commit).
- Issue #6 deterministic Geometry Nodes layout as the next product work.
- Where manuals, private corpora, and private evidence stay (they do not land in public git).
- Later archive of the old local checkout, only after the cleanup manifest checks, and only with explicit later authorization.

## Experimental

None in this slice.

## Acceptance sketch

Someone should be able to:

1. Cold-start an agent from files in this repo only (AGENTS → PRODUCT → CURRENT → HANDOFF → git diff).
2. Treat public GitHub `main` as the sole product and development source.
3. Distinguish static tests, installed-plugin proof, and Blender runtime proof.
4. Read `docs/cleanup/old-local-source.md` as a non-destructive archive plan.
5. Keep #6, Shader, find_nodes, and Jev out of the shipped product until their own issues land.
