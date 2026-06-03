# NodeCue Blender Node Skills

Standalone Blender node skills for NodeCue, Codex, Claude, and other agent workflows.

The alpha release includes the Geometry Nodes skill. Shader Nodes and Compositing Nodes are planned as separate skill folders in this same package once they have verified rules and patterns.

The Geometry Nodes skill teaches agents how to reason about node graphs: node identities, sockets, field/data-flow relationships, readback repair, reusable patterns, and teachable frame organization.

## Install

Default Codex skill install:

```bash
npx @nodecue/blender-node-skills install
```

Custom skills directory:

```bash
npx @nodecue/blender-node-skills install --target /path/to/skills --force
```

Install a specific bundled skill:

```bash
npx @nodecue/blender-node-skills install --skill geometry-nodes
```

Install all bundled skills:

```bash
npx @nodecue/blender-node-skills install --all
```

This installs:

```text
<target>/geometry-nodes/
```

## Contents

- `skills/geometry-nodes/SKILL.md` - entrypoint and high-level Geometry Nodes rules
- `skills/geometry-nodes/rules/` - node family rules and safety notes
- `skills/geometry-nodes/patterns/` - verified graph patterns
- `skills/geometry-nodes/evals/` - small validation artifacts

Runtime system prompts are intentionally not bundled here. Each agent should provide its own behavior instructions, then read this skill as domain knowledge.

## Feedback

Use the `Skill feedback` issue template when an agent gets a Blender node task wrong after reading this package. Useful reports include the prompt, agent/tool name, execution path, generated graph issue, and any readback JSON or screenshots you can share.

Do not include API keys, private asset-library paths, or unreleasable `.blend` files in public issues.

## Scope

This alpha package covers Geometry Nodes only. The package and installer are intentionally named for Blender node skills so Shader Nodes and Compositing Nodes can be added without changing the repo or npm package again.
