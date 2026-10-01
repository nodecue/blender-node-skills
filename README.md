English | [简体中文](README.zh-CN.md)

# NodeCue Blender Node Skills

> **Archived (2026-10-02). This project is no longer maintained.**
>
> A paired test on 2026-10-01 used Codex (`gpt-5.6-sol`), Blender 5.2.2 and the official Blender Lab MCP, with one run per condition on a 50-check Geometry Nodes task:
>
> | | Score | Codex time | Input tokens |
> | --- | --- | --- | --- |
> | No skill | 50/50 | 183 s | 456k |
> | This v0.7 skill | 50/50 | 273 s | 899k |
> | A 1.6 KB conventions-only skill | 50/50 | 223 s | 708k |
>
> A strong agent with the official MCP already built the graph correctly without help. The v0.7 skill's workflow and scripts added turns and context but did not reduce errors. Most errors were recoverable Blender 5.2 API changes, such as setting modifier inputs through `modifier.properties.inputs`. A short conventions-only skill did help readability: Blender node names kept, titled frames, no overlaps. The harder problems — values that are wrong without raising an error, and whether a result *looks* right — are not addressed by this kind of skill.
>
> The code stays available for reference. It will not be updated, and issues are closed.

The product available now is the shipped **v0.7 Geometry Nodes skill** at [`skills/geometry-nodes/`](skills/geometry-nodes/). It is [`SKILL.md`](skills/geometry-nodes/SKILL.md), four references, and four scripts:

- References: [`nodes.tsv`](skills/geometry-nodes/references/nodes.tsv), [`versions.md`](skills/geometry-nodes/references/versions.md), [`reuse.md`](skills/geometry-nodes/references/reuse.md), [`diagnostics.md`](skills/geometry-nodes/references/diagnostics.md)
- Scripts: [`find_nodes.py`](skills/geometry-nodes/scripts/find_nodes.py), [`read_graph.py`](skills/geometry-nodes/scripts/read_graph.py), [`probe_node.py`](skills/geometry-nodes/scripts/probe_node.py), [`capture.py`](skills/geometry-nodes/scripts/capture.py), [`inspect_assets.py`](skills/geometry-nodes/scripts/inspect_assets.py), [`verify_result.py`](skills/geometry-nodes/scripts/verify_result.py)

An agent uses it to build a Geometry Nodes graph you can check, or to explain a graph without changing it.

> **Status.** The shipped **v0.7 Geometry Nodes skill** is the published stable product boundary. Public GitHub `main` is the product and development source. The Codex plugin is merged into public `main`. It is not a tagged plugin release. A Codex plugin has completed **local** acceptance in two layers. **A.** A fresh Codex task outside this repository, with the Codex plugin already installed, auto-discovered the `geometry-nodes` skill, auto-obtained the Blender MCP tool, connected to portable Blender 5.1.2, and returned a live read-only read of real version, file state, the active object, and no GN modifier. That path proves plugin install, discovery, MCP entry, and live read-only. **B.** Separate live host tests on the same blender-mcp transport verified Blender 5.1.2 portable and 5.2.2 target identification and isolation, plus minimal GN create, nodes/links/socket readback, evaluated bounds, and viewport evidence. Layer B was run independently; it is not plugin end-to-end mutation or image acceptance. GitHub install on a new machine or VM, Claude, Pi, and other hosts are unverified. This project is evolving. Before relying on an install or a host, read the latest README, the [releases](https://github.com/nodecue/blender-node-skills/releases), and the [issues](https://github.com/nodecue/blender-node-skills/issues). Feedback from real use on a real host is welcome.

## What the v0.7 skill does

1. Read the Blender version and the current graph.
2. Route candidate nodes with `references/nodes.tsv`. That file is a routing index. It is not something to wire from.
3. Resolve node, socket, and property identities in the running Blender before connecting anything.
4. Build, edit, or explain in slices small enough to check on their own. Explain stays read-only.
5. Verify an outcome derived from the request. A node count is only a fact about the graph. A size, a position, or a count the request asked for is the check that matters.
6. When the request mutates the graph, keep Blender's default node names and put the explanation on teaching frames.

[`inspect_assets.py`](skills/geometry-nodes/scripts/inspect_assets.py) is available when the task needs it. It does not replace a live read of Blender.

## Install the standalone skill

There is no NodeCue-accepted install command that covers Claude Code, Codex, Cursor, Pi, and other agents together. Skill locations and discovery differ by host. Follow the current skill-install documentation for the agent you are using.

**Manual path, for any host.** Clone or download this repository and place [`skills/geometry-nodes/`](skills/geometry-nodes/) where that agent installation recognizes skills.

**Convenience route.** This is the existing [skills CLI](https://github.com/vercel-labs/skills) command. NodeCue has not finished acceptance of how it behaves on each host. It does not configure Blender, and it does not install the Codex plugin described below.

```bash
npx skills add nodecue/blender-node-skills
```

## Connect an agent to a running Blender

The skill does not create a Blender connection. It requires an execution channel that already works. That channel must run the shipped Python inside the running Blender and return the result. Python on the host, outside Blender, cannot see the open file.

The minimal setup described here uses the official [Blender Lab MCP](https://projects.blender.org/lab/blender_mcp) over stdio. Install its server with the upstream command:

```bash
pip install git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp
```

The Blender extension is a separate part: add the Blender Lab Extensions repository (`https://lab.blender.org/`), find and install the MCP extension, enable it, then start its server from the extension preferences. The upstream project owns these steps and may change them. The client command used by this repository is `blender-mcp` with no arguments, as shown in [`.mcp.json`](.mcp.json); keep it available on the host's `PATH` and restart the MCP client after configuration.

After connecting, use this read-only smoke prompt:

> Without changing anything, report `bpy.app.version_string`, the current `.blend` file path (`bpy.data.filepath`), and the active object name (or `none`).

The connection is ready when the returned values describe the Blender window you intended to use. Do not continue if the host cannot return them.

**Blender Lab MCP** requires **Blender 5.1 or newer** as its runtime floor. That floor is separate from the v0.7 skill's knowledge coverage of Blender 4.5 LTS and 5.0 in [`versions.md`](skills/geometry-nodes/references/versions.md) and `nodes.tsv`. Skill routing still records those older versions; Lab MCP does not run on them.

## Codex plugin (merged on public main)

Packaging this skill as a NodeCue agent plugin is separate from the shipped v0.7 skill. The Codex plugin is merged into public `main`. It is not a tagged plugin release. Local acceptance is the two layers below. Plugin commands are not a general verified way to install the v0.7 skill.

Local Codex evidence, in two layers:

- **A. Fresh Codex plugin task (live read-only).** A Codex task started outside this repository, with the Codex plugin already installed, auto-discovered the `geometry-nodes` skill, auto-obtained the Blender MCP tool, connected to portable Blender **5.1.2**, and returned a live **read-only** read of real version, file state, the active object, and no GN modifier. That path proves plugin install, discovery, MCP entry, and live read-only.
- **B. Separate blender-mcp transport / live host tests.** Independent acceptance on the same blender-mcp transport verified Blender **5.1.2 portable** and **5.2.2** target identification and isolation, plus minimal GN **create**, nodes/links/socket **readback**, **evaluated bounds**, and **viewport evidence**. Layer B was not completed by the fresh Codex plugin task in A. It is not plugin end-to-end mutation or image acceptance.

Still unverified: GitHub install on a new machine or VM; Claude; Pi; other hosts. Packaging and install steps may still change.

The committed [`.claude-plugin/`](.claude-plugin/) metadata, [`plugin.json`](.claude-plugin/plugin.json) and [`marketplace.json`](.claude-plugin/marketplace.json), is an early Claude packaging surface. It is not proof that a current Claude host accepts the plugin. Those early Claude plugin commands are not a recommended or verified install path. They do not configure Blender. Claude compatibility remains for a later validation pass.

## First use

This path uses only this public repository.

1. Install or locate the standalone skill, `skills/geometry-nodes/`.
2. Connect the agent to Blender using the setup above and pass the read-only smoke prompt.
3. Activate the Geometry Nodes skill and start from a test `.blend`.
4. Ask for a build, an edit, or an explanation. Then inspect the evaluated result in Blender. A tidy node graph is not the result.
5. If it fails, open an issue with the [Skill feedback](.github/ISSUE_TEMPLATE/skill-feedback.yml) template. Include the prompt, the agent or tool, the model, the Blender version, and what the result got wrong. Leave out API keys, credentials, private asset-library paths, and `.blend` files you cannot publish.

## Scope and accuracy

- **Geometry Nodes only.** Shader Nodes and Compositing Nodes are not shipped.
- **Versioned evidence is routing guidance.** [`versions.md`](skills/geometry-nodes/references/versions.md) and the `version` column in `nodes.tsv` cover Blender 4.5 LTS, 5.0, 5.1, and 5.2 LTS. They record where candidates exist and what some cross-version differences look like. They are not a guarantee that a graph behaves the same way on every one of those versions. Skill knowledge for 4.5 and 5.0 is separate from Blender Lab MCP, which requires Blender 5.1 or newer.
- **The running Blender is authoritative** for the current node, socket, property and RNA identity, and for legal values.
- **Input-reference reconstruction is not shipped.** Automatic visual QA of the evaluated output is not shipped either. [`capture.py`](skills/geometry-nodes/scripts/capture.py) captures the node editor. It does not judge the final evaluated render or viewport.
- **When a change is requested, frame notes follow the language of the prompt.** Node, socket, and identifier names stay as Blender shows them, so they still match the UI and tutorials.
- **Results can still be wrong.** Older static checks and runtime regression history are not acceptance on Claude, Codex, or any other host. This README does not treat those earlier runs as a current pass. Inspect the evaluated Blender output before relying on the graph.

## Feedback

Use the [Skill feedback](.github/ISSUE_TEMPLATE/skill-feedback.yml) template. Say what you asked, which agent and model you used, which Blender version was running, how the execution channel was provided, and what the evaluated result did. Send sanitized evidence only: no API keys, credentials, private paths, or `.blend` files you cannot publish.

## License

MIT. See [LICENSE](LICENSE). The running Blender remains the authority for current identities and behavior.
