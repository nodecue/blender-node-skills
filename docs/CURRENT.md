# CURRENT

Living direction for agents. Update this when the user changes mind. Do not treat chat history as more authoritative than this file.

## Established

- Shipped product is the v0.7 Geometry Nodes skill at `skills/geometry-nodes/`, with build/edit/explain judgment, version routing, live introspection, verification, and teaching structure.
- Plugin installs, environments, and provides entry points only. It does not own skill knowledge.
- Live Blender is authority for node/socket/property/RNA identity and legal values.
- Geometry Nodes is the only shipped runtime. Shader/Compositor, input-reference reconstruction, and automatic evaluated-output QA are not shipped.
- Codex plugin is on public `main`. A fresh installed-plugin task verified automatic discovery, MCP, and live read-only. Independent blender-mcp host mutation, readback, and viewport passed. That is not the same as a fresh-task plugin end-to-end mutation/image. New machines/VMs, Claude, and Pi are unverified.
- Open Issues: #10 GitHub-primary migration (current work); #6 deterministic layout (after migration).
- Future skill, plugin, find_nodes, and Jev work goes Issue → branch/worktree → PR → review → merge → close. Jev may only be an optional measured reranking experiment, not a dependency.
- GitHub Issues are the execution backlog. Do not create `docs/BACKLOG.md`.
- Large manuals, experiments, private corpora, session transcripts, absolute paths, credentials, `.blend` files, and machine artifacts stay out of the public repo.

## Current slice

Issue #10 GitHub-primary migration.

Target: public `main` is the authoritative product source. The migration is still in progress. Do not declare any old local source retired or deletable.

This slice: add self-contained agent governance files so a new agent can cold-start from this repo alone.

Later slices (not this commit): authority inventory; decide which tests and tools belong in public; retire old dual-authority / sync rules in process (without deleting the old tree from here); fresh-clone validation.

## Out of scope / do not do

- Delete or empty any old local NodeCue directory.
- Implement Issue #6 deterministic layout.
- Ship find_nodes, Jev, or Shader/Compositor runtime.
- Expand host claims beyond what is already verified.
- Copy old dual-authority, release-copy, `_release_repos`, or `sync_release_repos` rules into this repo.
- Add unverified unified test/build/install commands.
- Edit README, CONTRIBUTING, skill, or plugin files in this slice.

## Open

- Which public tests and tools must move into this GitHub-primary repo.
- Where manuals, private corpora, and private evidence go (they do not land in public git).
- How old local sync and dual-authority process is retired after public `main` is actually authoritative.

## Experimental

- New-clone fresh acceptance of skill, plugin, and live read-only on a machine that has only this repository.

## Acceptance sketch

When the Issue #10 migration slice is done, someone should be able to:

1. Cold-start an agent from files in this repo only (AGENTS → PRODUCT → CURRENT → HANDOFF → git diff).
2. Read an authority inventory that says what public git owns vs what still lives elsewhere — without treating old sources as already gone.
3. Fresh-clone and validate the Geometry Nodes skill, plugin install/entry, and live read-only introspection.
4. See a cleanup manifest of what must not remain as a second authority, without any deletion in that step.
5. Keep #6, Shader, find_nodes, and Jev out of the shipped product until their own issues land.
