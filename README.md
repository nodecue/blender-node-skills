English | [简体中文](README.zh-CN.md)

# NodeCue Blender Node Skills

An agent skill that teaches AI coding agents to **build Blender Geometry Nodes graphs correctly — and explain them so you can learn from the result**.

## Why install this?

Strong models can already produce a valid-looking Geometry Nodes graph without any skill. What they get wrong is everything that makes the graph *usable*: requirements silently dropped, wiring that doesn't actually take effect, no exposed controls, nothing to learn from.

We ran the same prompts through the same agent (Codex CLI + Blender MCP), with and without this skill:

| Prompt asked for | Without the skill | With the skill |
|---|---|---|
| Grass scatter **with a density mask** | Density mask **silently dropped** — no noise field, `Density Factor` never connected; 0 exposed controls | Noise → `Density Factor` wired; `Density`, `Scale Min`, `Scale Max` exposed; 2 teaching frames |
| Arc pipe from a curve | Profile curve **never connected** to `Curve to Mesh` — the pipe has no cross-section; 5 nodes, only 2 links | Profile wired; `Pipe Radius` exposed |
| Noise terrain **with height control** | 0 exposed controls | `Height`, `Noise Scale` exposed |

Both variants pass a naive "graph reaches output" check — the difference only shows when you look at whether the *request* was fulfilled. (Honest caveat: this is an operational ablation, not a lab-clean memory-free experiment; the harness to reproduce it ships in the [NodeCue repo](https://github.com/monswag/NodeCue).)

**On top-tier models the gap shifts from correctness to craft.** A comparison on Codex with gpt-5.6 (extra-high reasoning), same prompt both ways, produced correct geometry twice — but without the skill, the prompt had to explicitly demand explanatory frames, the model renamed and labeled every node with explanations (breaking the mapping between the graph, Blender's UI, and tutorials), left a redundant `Realize Instances` in the final graph, and used two extra nodes. With the skill: default node names, all teaching in bilingual frames, a temporary realize used to *verify* the instance count then removed, and a leaner 9-node graph — at the cost of a few more MCP calls. In short, the skill is **standing convention and verification discipline**: the things you would otherwise re-type in every prompt, and the things models skip when you forget to ask.

## What's inside

- `skills/geometry-nodes/SKILL.md` — build loop, reliability rules, the Geometry Nodes mental model (data-flow lane vs field lane)
- `skills/geometry-nodes/rules/` — 30+ node-family references with exact `bl_idname` and socket names
- `skills/geometry-nodes/patterns/` — verified graph patterns (distribution, stitching, displacement, density-controlled scatter, repeat-zone techniques, and more)

## Install

One command, works across Claude Code, Codex, Cursor, and other agents (via the open [skills CLI](https://github.com/vercel-labs/skills)):

```bash
npx skills add monswag/nodecue-blender-node-skills
```

Alternatives: Claude Code users can instead run `/plugin marketplace add monswag/nodecue-blender-node-skills` then `/plugin install blender-node-skills@nodecue`; or clone this repo and copy `skills/geometry-nodes/` into your agent's skills directory manually.

Runtime system prompts are intentionally not bundled: each agent brings its own behavior instructions and reads this skill as domain knowledge.

## Connecting to Blender

The skill works with whatever Blender access path your agent has:

- **Blender's official [MCP server](https://www.blender.org/lab/mcp-server/)** from Blender Lab (bundled from Blender 5.2 LTS, available as an add-on) — preferred
- The community [blender-mcp](https://github.com/ahujasid/blender-mcp) project
- The **[NodeCue Blender add-on](https://github.com/monswag/NodeCue)** — an in-Blender agent that bundles this same skill and runs with your own API key

## Annotation Language

Frame annotations and explanations follow the language of your prompt — describe the task in Chinese and you get Chinese teaching notes. Node names, socket names, and other Blender terms always stay in English so annotations map directly to Blender's UI and to mainstream tutorials.

## Scope and Accuracy

- **Geometry Nodes only, Blender 5.0+.** Rules follow the Blender 5.0 manual; most testing happens on 5.1. Node behavior can differ across Blender versions.
- **Shader Nodes and Compositing Nodes are planned** as sibling skill folders once they have verified rules and patterns.
- **Results can still be wrong.** The skill sharply reduces invented node names and dropped requirements, but an LLM-driven build can still produce incorrect graphs or misleading explanations — model quality matters. Inspect the graph in Blender before relying on it, and report failures.

## Feedback

Open an issue with the `Skill feedback` template when an agent gets a Blender node task wrong after reading this skill. Useful reports include the prompt, agent/tool name, model, what the graph got wrong, and any readback JSON or screenshots you can share.

Do not include API keys, private asset-library paths, or unreleasable `.blend` files in public issues.

## License

MIT — see [LICENSE](LICENSE). Node behavior in the rules is verified against the [Blender Manual](https://docs.blender.org/manual/en/latest/) (CC-BY-SA 4.0).
