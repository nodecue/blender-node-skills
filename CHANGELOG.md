# Changelog

## 0.1.0-alpha.0

Initial alpha package for standalone Blender node skills.

### Included

- `geometry-nodes` skill.
- Geometry Nodes `SKILL.md` entrypoint.
- Verified rule and pattern files for Geometry Nodes agent guidance.
- Small eval artifacts for skill activation and pattern readback checks.
- `npx @nodecue/blender-node-skills install` installer.
- `--skill`, `--all`, `--target`, and `--force` installer options.
- CI for install smoke and npm package dry-run.
- Feedback and security issue templates.

### Not Included Yet

- Shader Nodes skill.
- Compositing Nodes skill.
- Runtime system prompts.
- Model provider configuration.
- Blender MCP server or NodeCue add-on code.

### Package Direction

The package name is intentionally `blender-node-skills` instead of `geometry-nodes-skill` so Shader Nodes and Compositing Nodes can be added as separate skill folders once their rules and patterns are verified.
