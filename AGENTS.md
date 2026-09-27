# AGENTS.md

Project-specific guidance. Product core, live direction, and task progress live elsewhere:

- `docs/PRODUCT.md` — stable product core
- `docs/CURRENT.md` — live direction for this stage
- `docs/HANDOFF.md` — active-task handoff (overwrite only)

This repository is self-contained. Do not require a global `AGENTS.md`, user-home paths, another local checkout, chat history, or absolute machine paths.

## Project intent

NodeCue helps agents build and explain Blender Geometry Nodes graphs with exact node and socket identities. Authoritative product core: `docs/PRODUCT.md`.

## Source hierarchy and cold start

Read only files inside this repository, in this order:

1. `AGENTS.md` (this file)
2. `docs/PRODUCT.md`
3. `docs/CURRENT.md`
4. `docs/HANDOFF.md`
5. current `git diff` and uncommitted working tree

Deeper notes (`docs/decisions/`, `docs/research/`, `docs/lessons/`) only when the task needs them. Create those files when there is content; do not add empty directories.

GitHub history, Issues, and PRs hold facts. Do not duplicate long process here.

GitHub-primary migration is still in progress. Treat `docs/CURRENT.md` as the live statement of what is authoritative now. Do not assume the migration is finished or that any old local source may be deleted.

## NodeCue boundaries

- Shipped product knowledge and workflow live in `skills/geometry-nodes/`.
- The plugin installs, sets environment, and provides entry points. It must not copy skill knowledge or workflow, and must not restore retired add-on or sidecar runtimes.
- Live Blender is the authority for current node, socket, property, and RNA identity and legal values.
- Geometry Nodes is the only shipped runtime. Do not implement Shader or Compositor as shipped product.
- Do not copy large manuals, experiments, private corpora, session transcripts, credentials, `.blend` files, or machine artifacts into this public repo.

## Protect existing work

Keep changes scoped. Do not rewrite unrelated skill, plugin, README, or CONTRIBUTING files unless the assigned task names them.

## Scope and acceptance

For non-trivial implement work, before coding:

1. Restate the goal in plain language.
2. Propose 3–5 observable checks the user can perform.
3. Wait for confirmation when the request is ambiguous or would change direction.

When the user changes direction, update `docs/CURRENT.md` first, then continue.

There is no accepted unified public test command in this repository. Do not invent unverified test, build, or install commands.

## Handoff and one editor

Default: one editing agent at a time. Other agents may read, review, or advise. Serialize if two agents would touch the same file.

When leaving:

1. Overwrite `docs/HANDOFF.md` (never append; never create dated handoff files).
2. Commit if appropriate, or leave a working tree the next agent can inspect.
3. Stop editing.

`docs/HANDOFF.md` is a live scratch pad. Git holds history.

## Learning loop (sparingly)

- User workflow notes: append to `docs/learnings.md`
- Consequential choices: `docs/decisions/<topic>.md` when there is a real decision
- Reusable research: `docs/research/<topic>.md` when there is a real research note

Do not promote every discovery into permanent structure. GitHub Issues are the execution backlog; do not create `docs/BACKLOG.md`.
