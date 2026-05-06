# NodeCue Geometry Nodes Skill

Standalone Geometry Nodes skill for NodeCue, Codex, Claude, and other agent workflows.

The skill teaches agents how to reason about Geometry Nodes graphs: node identities, sockets, field/data-flow relationships, readback repair, reusable patterns, and teachable frame organization.

## Install

Default Codex skill install:

```bash
npx @nodecue/geometry-nodes-skill install
```

Custom skills directory:

```bash
npx @nodecue/geometry-nodes-skill install --target /path/to/skills --force
```

This installs:

```text
<target>/geometry-nodes/
```

## Contents

- `SKILL.md` - entrypoint and high-level Geometry Nodes rules
- `SYSTEM_PROMPT.md` - generic Geometry Nodes agent system prompt template
- `rules/` - node family rules and safety notes
- `patterns/` - verified graph patterns
- `evals/` - small validation artifacts

## Scope

This alpha package covers Geometry Nodes only. Shader Nodes and Compositing Nodes will be separate future skill areas.
