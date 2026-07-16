# Changelog

## Unreleased

### Added

- Real side-by-side screenshots in the "Why install this?" section: same agent (Codex CLI, gpt-5.6, extra-high reasoning), same prompt, with and without the skill (`docs/images/comparison-*.png`). The mid-tier ablation table moves into a collapsed `<details>` section.

- The repository is now a Claude Code plugin marketplace: `/plugin marketplace add monswag/nodecue-blender-node-skills` then `/plugin install blender-node-skills@nodecue` installs the skill without a terminal. Codex and other agents keep the clone-and-copy path.
- Chinese README (`README.zh-CN.md`) with a language switcher.
- SKILL.md v0.5: annotation-language rule (follow the prompt language, never translate Blender terms, prefer short bilingual frame labels).

### Changed

- README rewritten around what the skill is for: building Geometry Nodes graphs correctly and teaching through frame annotations. It now states which agents it works with, which combinations were actually tested, that results can still be wrong, and the Blender 5.0+ / Geometry-Nodes-only scope.
- Install paths are the Claude Code plugin marketplace or `git clone` + copy; the repository content is just the skill.

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
