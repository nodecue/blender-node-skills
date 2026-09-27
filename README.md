English | [简体中文](README.zh-CN.md)

# NodeCue Blender Node Skills

The product available now is the shipped **v0.7 Geometry Nodes skill** at [`skills/geometry-nodes/`](skills/geometry-nodes/). It is [`SKILL.md`](skills/geometry-nodes/SKILL.md), four references, and four scripts:

- References: [`nodes.tsv`](skills/geometry-nodes/references/nodes.tsv), [`versions.md`](skills/geometry-nodes/references/versions.md), [`reuse.md`](skills/geometry-nodes/references/reuse.md), [`diagnostics.md`](skills/geometry-nodes/references/diagnostics.md)
- Scripts: [`read_graph.py`](skills/geometry-nodes/scripts/read_graph.py), [`probe_node.py`](skills/geometry-nodes/scripts/probe_node.py), [`capture.py`](skills/geometry-nodes/scripts/capture.py), [`inspect_assets.py`](skills/geometry-nodes/scripts/inspect_assets.py)

An agent uses it to build a Geometry Nodes graph you can check, or to explain a graph without changing it.

> **Status.** The v0.7 skill files above are the stable product in this repository. Installation paths, host behavior, and the agent-plugin packaging layer are still evolving. This README does not treat those paths as verified, and it does not promise that a path you use today will stay as it is. Before relying on an install or a host, read the latest README, the [releases](https://github.com/nodecue/blender-node-skills/releases), and the [issues](https://github.com/nodecue/blender-node-skills/issues). Feedback from real use on a real host is welcome.

## What the v0.7 skill does

1. Read the Blender version and the current graph.
2. Route candidate nodes with `references/nodes.tsv`. That file is a routing index. It is not something to wire from.
3. Resolve node, socket, and property identities in the running Blender before connecting anything.
4. Build, edit, or explain in slices small enough to check on their own. Explain stays read-only.
5. Verify an outcome derived from the request. A node count is only a fact about the graph. A size, a position, or a count the request asked for is the check that matters.
6. When the request mutates the graph, keep Blender's default node names and put the explanation on teaching frames.

[`inspect_assets.py`](skills/geometry-nodes/scripts/inspect_assets.py) and a project-local `NODECUE.md` are available when the task needs them. They do not replace a live read of Blender.

## Install the standalone skill

There is no NodeCue-accepted install command that covers Claude Code, Codex, Cursor, Pi, and other agents together. Skill locations and discovery differ by host. Follow the current skill-install documentation for the agent you are using.

**Manual path, for any host.** Clone or download this repository and place [`skills/geometry-nodes/`](skills/geometry-nodes/) where that agent installation recognizes skills.

**Convenience route.** This is the existing [skills CLI](https://github.com/vercel-labs/skills) command. NodeCue has not finished acceptance of how it behaves on each host. It does not configure Blender, and it does not install the unfinished plugin described below.

```bash
npx skills add nodecue/blender-node-skills
```

## Connect an agent to a running Blender

The skill does not create a Blender connection. It requires an execution channel that already works. That channel must run the shipped Python inside the running Blender and return the result. Python on the host, outside Blender, cannot see the open file.

MCP, or another integration the host already provides, can be that channel. NodeCue has not completed current per-host acceptance of those routes. That includes official and community MCP servers. This page does not rank any of them, and it does not include server setup. Use the documentation for the host and the transport you chose.

## The agent-plugin layer is unfinished

Packaging this skill as a NodeCue agent plugin is separate from the skill itself, and that packaging is not finished. Plugin commands are not a verified way to install the v0.7 skill.

The committed [`.claude-plugin/`](.claude-plugin/) metadata, [`plugin.json`](.claude-plugin/plugin.json) and [`marketplace.json`](.claude-plugin/marketplace.json), is an early Claude packaging surface. It is not proof that a current Claude host accepts the plugin. The commands `/plugin marketplace add nodecue/blender-node-skills` and `/plugin install blender-node-skills@nodecue` belong to that early surface. They are not the recommended install path, and NodeCue has not accepted them as verified. They do not configure Blender.

Codex is the next priority for plugin acceptance. Codex plugin support is not complete. Claude compatibility remains for a later validation pass.

## First use

This path uses only this public repository.

1. Install or locate the standalone skill, `skills/geometry-nodes/`.
2. Make sure the agent already has a working Blender execution channel.
3. Activate the Geometry Nodes skill and start from a test `.blend`.
4. Ask for a build, an edit, or an explanation. Then inspect the evaluated result in Blender. A tidy node graph is not the result.
5. If it fails, open an issue with the [Skill feedback](.github/ISSUE_TEMPLATE/skill-feedback.yml) template. Include the prompt, the agent or tool, the model, the Blender version, and what the result got wrong. Leave out API keys, credentials, private asset-library paths, and `.blend` files you cannot publish.

## Scope and accuracy

- **Geometry Nodes only.** Shader Nodes and Compositing Nodes are not shipped.
- **Versioned evidence is routing guidance.** [`versions.md`](skills/geometry-nodes/references/versions.md) and the `version` column in `nodes.tsv` cover Blender 4.5 LTS, 5.0, 5.1, and 5.2 LTS. They record where candidates exist and what some cross-version differences look like. They are not a guarantee that a graph behaves the same way on every one of those versions.
- **The running Blender is authoritative** for the current node, socket, property and RNA identity, and for legal values.
- **Input-reference reconstruction is not shipped.** Automatic visual QA of the evaluated output is not shipped either. [`capture.py`](skills/geometry-nodes/scripts/capture.py) captures the node editor. It does not judge the final evaluated render or viewport.
- **When a change is requested, frame notes follow the language of the prompt.** Node, socket, and identifier names stay as Blender shows them, so they still match the UI and tutorials.
- **Results can still be wrong.** Older static checks and runtime regression history are not acceptance on Claude, Codex, or any other host. This README does not treat those earlier runs as a current pass. Inspect the evaluated Blender output before relying on the graph.

## Dated example from a pre-v0.7 skill

The two images below are one historical session: Codex app, gpt-5.6, the same cube-and-cones request, once without that older skill and once with it, through a Blender MCP channel. They illustrate habits from a skill that predates v0.7. They are not v0.7 behavioral acceptance, not evidence that any host is supported now, and not a performance benchmark.

> *(Add a 2 m cube to the scene. At each of its top 4 vertices, add a cone 0.2 m tall and 0.2 m in diameter.)*

| Without that older skill (Codex app, gpt-5.6) | With that older skill (Codex app, gpt-5.6) |
|---|---|
| ![Historical session without the older skill: nodes renamed and labeled, a leftover Realize Instances node, 11 nodes](docs/images/comparison-no-skill.png) | ![Historical session with the older skill: default node names, four bilingual teaching frames, 9 nodes](docs/images/comparison-with-skill.png) |
| 11 nodes, renamed and relabeled, with a leftover `Realize Instances` | 9 nodes, default names, 4 bilingual frames |

What that session still shows:

- **Default Blender names.** Names such as `Position`, `Compare`, and `Cone` stay tied to the UI and to tutorials. Renames such as `Cube_2m`, and labels such as "读取每个顶点的位置", break that link.
- **Teaching frames.** Explanations sat on frames ("02 顶部四点 — Select Z > 0.99") in the skill-following column. The other prompt had to ask for frames in an extra sentence. That is a record of that run. It does not prove that a current session adds frames automatically.
- **Realize late.** `Realize Instances` was used to count the four cones and then removed. Realize only when a later operation needs real geometry, and do it as late as that operation allows.
- **Verification took extra work in that session.** The session recorded 4 MCP calls (about 4 minutes 17 seconds) without the skill and 7 MCP calls (about 5 minutes 46 seconds) with it. The extra calls were readback and repair. Those figures describe that session only. They are not a current benchmark.

Both columns produced the requested geometry. On that model, the visible difference was the graph left behind: default names, teaching frames, a temporary realize that did not remain, and a check before the run was called done.

## Feedback

Use the [Skill feedback](.github/ISSUE_TEMPLATE/skill-feedback.yml) template. Say what you asked, which agent and model you used, which Blender version was running, how the execution channel was provided, and what the evaluated result did. Send sanitized evidence only: no API keys, credentials, private paths, or `.blend` files you cannot publish.

## License

MIT. See [LICENSE](LICENSE). The [Blender Manual](https://docs.blender.org/manual/en/latest/) (CC-BY-SA 4.0) is a reference. The running Blender remains the authority for current identities and behavior.
