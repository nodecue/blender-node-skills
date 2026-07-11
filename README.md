English | [简体中文](README.zh-CN.md)

# NodeCue Blender Node Skills

An agent skill that teaches AI coding agents how to **build Blender Geometry Nodes graphs correctly — and explain them so you can learn from the result**.

Point an agent at this skill and ask for a node setup in plain language ("scatter grass on this surface with a density mask"). The agent reads the skill as domain knowledge and builds the actual node graph in Blender: exact node identities and sockets, verified graph patterns, field/data-flow reasoning, and readback-based self-correction. The generated graph carries **teaching annotations** — frames that label each logical block and explain why the nodes are organized that way — so the output is something you can study, not just use.

This is not a preset library and not a Python snippet generator. It is the knowledge layer that makes a general agent competent at Blender node systems.

## What's Inside

- `skills/geometry-nodes/SKILL.md` — entrypoint: build loop, reliability rules, the Geometry Nodes mental model (data-flow lane vs field lane), and indexes into rules and patterns
- `skills/geometry-nodes/rules/` — 30+ node-family references with exact `bl_idname` and socket names
- `skills/geometry-nodes/patterns/` — verified graph patterns (distribution, stitching, displacement, density-controlled scatter, repeat-zone techniques, and more)

## Works With

Any agent that can read skill files and drive Blender:

- **Claude Code / Codex CLI / other agent CLIs** — connect to Blender through an MCP server: Blender's official [MCP server](https://www.blender.org/lab/mcp-server/) from Blender Lab (bundled from Blender 5.2 LTS, available as an add-on), or the community [blender-mcp](https://github.com/ahujasid/blender-mcp) project
- **[NodeCue Blender add-on](https://github.com/monswag/NodeCue)** — an in-Blender agent that bundles this same skill and runs with your own API key

## Tested Combinations

What we have actually verified so far:

- Codex CLI + Blender's official MCP server (with-skill vs no-skill ablation runs)
- NodeCue built-in agent with OpenRouter models (kimi-k2.6, deepseek-v4-pro), including automated graph-structure checks: required nodes present, geometry trunk reaches Group Output, field drivers reach real consumers, teaching frames present

Claude Code and other MCP-capable agents follow the same path but have not been formally evaluated yet — reports welcome.

## Install

```bash
git clone https://github.com/monswag/nodecue-blender-node-skills.git
```

Copy the skill folder into your agent's skills directory:

```bash
# Claude Code
cp -r nodecue-blender-node-skills/skills/geometry-nodes ~/.claude/skills/

# Codex
cp -r nodecue-blender-node-skills/skills/geometry-nodes ~/.codex/skills/
```

For other agents, copy `skills/geometry-nodes/` to wherever that agent loads skills from.

Runtime system prompts are intentionally not bundled: each agent brings its own behavior instructions and reads this skill as domain knowledge.

## Annotation Language

Frame annotations and explanations follow the language of your prompt — describe the task in Chinese and you get Chinese teaching notes. Node names, socket names, and other Blender terms always stay in English so annotations map directly to Blender's UI and to mainstream tutorials.

## Scope and Accuracy

- **Geometry Nodes only, Blender 5.0+.** Rules follow the Blender 5.0 manual; most testing happens on 5.1. Node behavior can differ across Blender versions.
- **Shader Nodes and Compositing Nodes are planned** as sibling skill folders in this same repository once they have verified rules and patterns.
- **Results can be wrong.** The skill sharply reduces invented node names and broken links, but an LLM-driven build can still produce incorrect graphs or misleading explanations — model quality matters. Inspect the graph in Blender before relying on it, and report failures.

## Feedback

Open an issue with the `Skill feedback` template when an agent gets a Blender node task wrong after reading this skill. Useful reports include the prompt, agent/tool name, model, what the graph got wrong, and any readback JSON or screenshots you can share.

Do not include API keys, private asset-library paths, or unreleasable `.blend` files in public issues.

## License

MIT — see [LICENSE](LICENSE).
