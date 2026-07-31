# Changelog

## Unreleased

### Changed (2026-07-30 — skill becomes the only product surface)

- The NodeCue Blender add-on is retired. The skill no longer references it: the "Why install this?" comparison drops the add-on column, and the add-on is removed from the list of Blender access paths. Recommended path is this skill plus Blender's official Lab MCP server.
- Repository moved to the `nodecue` organization and renamed `blender-node-skills`. Install and marketplace commands now use `nodecue/blender-node-skills`.
- Scope corrected to **Blender 4.5 LTS through 5.2**. The previous "Blender 5.0+, rules follow the 5.0 manual, most testing on 5.1" statement predated the 4.5 live audit (350 node types created on Blender 4.5.12; 45 shared nodes diffed against 5.2.0). Differences between 5.0 and 5.1 are stated as not yet systematically audited.
- Pattern `Evidence` lines now cite `evals/gn_pattern_readbacks.json` inside this package instead of a path in a separate development repository, so every claim resolves from the skill alone.
- `SKILL.md` gained a `Modes` section carrying the strictly read-only Explain contract, which previously shipped only in the add-on's unpublished system prompt.

### Added

- **Blender 5.2 support (skill v0.6)**, verified by live readback on Blender 5.2: 36 new node entries across 15 rule files (the 5.2 release notes list 26; live enumeration found 10 more), each with `Version` and `Evidence` metadata. New Version Awareness rules: gate `5.2+` nodes on older Blenders, and resolve sockets via live readback for nodes whose identifiers changed. The mental model gains the 5.2 list and geometry-bundle data shapes.
- File-level `blender_support` / `blender_verified` frontmatter on all rules (5.1 + 5.2) and patterns (5.1; 5.2 golden readback regeneration pending). Version metadata uses two-part Blender versions only.

### Changed

- `GeometryNodeList` is now version-bounded to Blender 5.0-5.1 (removed in 5.2; use `Field to List` / `Closure to List` there); `Get List Item` and `List Length` rewritten for generic list sockets (no longer Float-only).
- `Compare` and `Random Value` carry Compatibility notes: Blender 5.2 changed their socket identifiers; agents must resolve sockets from readback instead of 5.1 baselines.

- "Why install this?" now compares the same build task two ways with real screenshots (`docs/images/comparison-*.png`): Codex app without the skill and Codex app with the skill. The skill-following run keeps default node names and organizes teaching frames; the no-skill run renames every node and leaves a stray `Realize Instances`. Each README quotes the prompt in its own primary language (English translation in README.md, original Chinese in README.zh-CN.md), trimmed to the core build request; a caption notes the no-skill run's prompt also had to explicitly ask for frame-based explanation, which the skill provides automatically.

### Removed

- The mid-tier ablation table (grass/pipe, dropped requirements) — the top-tier before/after screenshots now carry the "why install" argument alone.

- The repository is now a Claude Code plugin marketplace: `/plugin marketplace add nodecue/blender-node-skills` then `/plugin install blender-node-skills@nodecue` installs the skill without a terminal. Codex and other agents keep the clone-and-copy path.
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
