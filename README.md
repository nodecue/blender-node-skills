English | [简体中文](README.zh-CN.md)

# NodeCue Blender Node Skills

An agent skill that teaches AI coding agents to **build Blender Geometry Nodes graphs correctly — and explain them so you can learn from the result**: verified node and socket identities, proven graph patterns, readback-based self-repair, and teaching annotations in the language of your prompt.

## Why install this?

Same agent (Codex CLI, gpt-5.6, extra-high reasoning), same prompt, run twice through Blender MCP — once told not to use any skill, once with this skill:

> 在场景中添加一个立方体，2米大小，在立方体的顶部4个顶点处分别添加一个高0.2米，直径0.2米的圆锥。并对节点使用frame进行功能性解释。

| Without the skill | With the skill |
|---|---|
| ![Without the skill: every node renamed and labeled, a leftover Realize Instances node, 11 nodes](docs/images/comparison-no-skill.png) | ![With the skill: default node names, four bilingual teaching frames, 9 nodes](docs/images/comparison-with-skill.png) |

The geometry is correct both times — this is a strong model. The difference is what gets left behind:

- **Node names**: every node renamed and relabeled with an explanation (`Cube_2m`, "读取每个顶点的位置", "Z > 0.99 = 顶部顶点"...) vs. default Blender names (`Position`, `Compare`, `Cone`...). Renaming breaks the link between the graph, Blender's UI, and any tutorial that assumes default names.
- **Where the teaching lives**: explanations smeared across individual node labels vs. collected into four bilingual frames ("02 顶部四点 — Select Z > 0.99").
- **Leftover node**: a `Realize Instances` left sitting in the final graph vs. used only to verify the count (4 cones), then removed.
- **Graph size**: 11 nodes / 11 links vs. 9 nodes / 9 links for the identical result.
- **Cost**: 4 MCP calls (~4m17s) vs. 7 MCP calls (~5m46s) — the extra readback-verify-repair loop isn't free.

On a strong model, the skill isn't the difference between working and broken. It's standing convention (default names, frames, bilingual labels) and verification discipline (check before claiming done) instead of you re-typing "please explain with frames" and re-checking the result yourself, every time.

<details>
<summary>Mid-tier model ablation — here requirements get silently dropped without the skill</summary>

| Same agent, same prompt | Without the skill | With the skill |
|---|---|---|
| grass with a **density mask** | mask silently dropped | Noise → `Density Factor` wired; controls exposed |
| pipe along a curve | profile never connected — pipe has no cross-section | wired; `Pipe Radius` exposed |

From Codex + Blender MCP comparison runs (reproduction harness in the [NodeCue repo](https://github.com/monswag/NodeCue)).

</details>

## Install

One command, works across Claude Code, Codex, Cursor, and other agents (via the open [skills CLI](https://github.com/vercel-labs/skills)):

```bash
npx skills add monswag/nodecue-blender-node-skills
```

Alternatives: Claude Code plugin (`/plugin marketplace add monswag/nodecue-blender-node-skills`, then `/plugin install blender-node-skills@nodecue`), or clone and copy `skills/geometry-nodes/` into your agent's skills directory.

## Connecting to Blender

The skill works with whatever Blender access path your agent has:

- **Blender's official [MCP server](https://www.blender.org/lab/mcp-server/)** from Blender Lab (bundled from Blender 5.2 LTS, available as an add-on) — preferred
- The community [blender-mcp](https://github.com/ahujasid/blender-mcp) project
- The **[NodeCue Blender add-on](https://github.com/monswag/NodeCue)** — an in-Blender agent that bundles this same skill and runs with your own API key

## Scope and Accuracy

- **Geometry Nodes only, Blender 5.0+.** Rules follow the Blender 5.0 manual; most testing happens on 5.1. Shader Nodes and Compositing Nodes are planned as sibling skill folders.
- **Annotations follow your prompt's language** (Chinese prompt → Chinese teaching notes); Blender terms always stay in English so they map to the UI and tutorials.
- **Results can still be wrong.** The skill sharply reduces invented node names and dropped requirements, but model quality matters. Inspect the graph in Blender before relying on it, and report failures.

## Feedback

Open an issue with the `Skill feedback` template when an agent gets a Blender node task wrong after reading this skill. Include the prompt, agent/tool, model, and what the graph got wrong. No API keys, private asset-library paths, or unreleasable `.blend` files in public issues.

## License

MIT — see [LICENSE](LICENSE). Node behavior in the rules is verified against the [Blender Manual](https://docs.blender.org/manual/en/latest/) (CC-BY-SA 4.0).
