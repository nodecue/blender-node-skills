# Changelog

## Unreleased

The repository is now just the skill plus a plain git-checkout install.

### Changed

- README rewritten around what the skill is for: building Geometry Nodes graphs correctly and teaching through frame annotations. It now states which agents it works with, which combinations were actually tested, that results can still be wrong, and the Blender 5.0+ / Geometry-Nodes-only scope.
- Install is `git clone` + copy the skill folder into your agent's skills directory.

### Removed

- npm distribution: installer (`bin/install.js`), `package.json`, install smoke test, npm publishing docs and workflows. The npm route was never published and added maintenance surface without helping the target users; it can return later if demand shows.
- `SECURITY.md` (folded into the README feedback section).

## 0.1.0-alpha.1

Alpha package metadata update for the first public repository pass.

### Added

- GitHub checkout install fallback for testing before the npm package is published.

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
