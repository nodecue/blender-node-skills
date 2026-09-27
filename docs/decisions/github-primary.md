# Decision: public GitHub main is the product authority

## Decision

Public GitHub `main` for `nodecue/blender-node-skills` is the sole
authoritative product and development source. Contributors branch from public
`main` and follow Issue → branch or worktree → pull request → review → merge.

Live Blender remains the authority for current node, socket, property, and RNA
identity and legal values. GitHub `main` is the source of the skill, plugin
packaging, tests, and project documentation.

## Rationale

Public PR #11 added cold-start governance. Public PR #12 migrated public
maintenance evidence, tools, and tests. A later fresh clone of `main`
`007a98e9d1e5398f0c4f3cf6932451e9a17f97f9` passed static validation. Treating
any remaining local checkout as a second source would recreate two product
trees.

## Authority boundaries

- **Public GitHub `main`:** skill, plugin metadata, tests, tools, and public
  docs. Issues and PRs are the execution path.
- **Live Blender:** current identities and legal values at runtime.
- **Old local checkout:** archive candidate only. Do not reconcile it back
  into public `main`. Do not delete it from this decision.
- **Merge, release, and issue close** are separate actions. A merge does not
  close the issue. A release still needs explicit authorization.

## Validation evidence

Keep these layers distinct.

**Static (fresh clone of public `main`):**

- `python -m pytest tests -q`: 172 passed, 1 skipped (optional real-Blender
  runtime test without `NODECUE_BLENDER`).
- `python tools/gen_nodes_tsv.py --check`: current, 368 rows.
- Codex plugin validator: passed.

**Blender runtime (same fresh clone, `NODECUE_BLENDER` set):**

- portable Blender 5.1.2: `tests/test_skill_runtime_scripts.py` 36 passed.
- target Blender 5.2.2: the same 36 passed.

**Installed plugin (narrower, earlier):**

- A genuinely fresh Codex task auto-discovered the skill and Blender MCP
  entry and completed live read-only against portable Blender 5.1.2.
- Separate host tests proved mutation/readback/viewport on 5.1.2 and 5.2.2.
  Those were not the same fresh-plugin end-to-end mutation or image run.

Unverified: new-machine/VM GitHub install, Claude, Pi, plugin end-to-end
mutation, image acceptance.

## Consequences

- Contribution docs describe one GitHub-primary path.
- Codex plugin is described as merged into public `main`, not as a tagged
  plugin release unless a later tagged release says otherwise.
- Next product work is Issue #6 deterministic Geometry Nodes layout.
- find_nodes, Jev, Shader, and Compositor stay deferred.
- Cleanup of the old local checkout is documented in
  `docs/cleanup/old-local-source.md` and is non-destructive until a later
  explicit authorization.
