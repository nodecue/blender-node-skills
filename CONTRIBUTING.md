# Contributing

Thanks for helping. Bug reports from real use are as valuable as code: if the skill built or explained a graph wrongly, open an issue with the [Skill feedback](.github/ISSUE_TEMPLATE/skill-feedback.yml) template.

## Repository layout

| Path | What it is |
|---|---|
| `skills/geometry-nodes/` | The shipped skill: `SKILL.md`, `references/`, and the `scripts/` that run inside Blender |
| `.claude-plugin/`, `.codex-plugin/`, `.mcp.json` | Plugin metadata for Claude Code and Codex, and the `blender-mcp` stdio entry |
| `tests/` | Static tests that run anywhere; `tests/golden/` runs the skill scripts inside a real Blender |
| `tools/` | Maintainer tools: dump node identities from Blender, generate `nodes.tsv`, evaluate `find_nodes` |
| `docs/node-dumps/` | Per-version node dumps that `nodes.tsv` is generated from. Evidence, not shipped |
| `.github/` | CI quality gates, issue and pull request templates |

## Set up and run the checks

Python 3.11 or newer.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests -q                 # what CI runs
python tools/gen_nodes_tsv.py --check     # nodes.tsv and its manifest are up to date
python tools/eval_find_nodes.py           # find_nodes recall/accuracy, when you touch routing
```

The runtime-script integration test runs only when a Blender executable is found: set `NODECUE_BLENDER` to its path, or put `blender` on `PATH`. To run the Blender-side checks directly:

```bash
blender -b --factory-startup --python tests/golden/run_skill_runtime_scripts.py -- out.json
```

## Changing the node index

`skills/geometry-nodes/references/nodes.tsv` and `docs/node-dumps/nodes-tsv-manifest.md` are generated. Do not edit them by hand. Edit the reviewed metadata in `tools/nodes_tsv_review.json` (or add a dump with `tools/introspect_nodes.py`, see [`docs/node-dumps/README.md`](docs/node-dumps/README.md)), then run:

```bash
python tools/gen_nodes_tsv.py
```

## Pull requests

- Branch from `main`. Open an issue first for a larger change.
- Keep `SKILL.md` short: it is loaded into the agent's context every time. Put conditional detail in `references/`.
- Add a line under **Unreleased** in [`CHANGELOG.md`](CHANGELOG.md) for any user-visible change.
- Say what you verified and where: static checks only, which Blender version, which agent host. Static checks do not prove live Blender or host behavior, so name what was not run.
- Leave out credentials, private asset libraries, machine-local absolute paths, and `.blend` files you cannot publish.

## Releases

A maintainer moves **Unreleased** to a version heading, bumps `version` in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `.codex-plugin/plugin.json` together, and tags the commit `vX.Y.Z`.
