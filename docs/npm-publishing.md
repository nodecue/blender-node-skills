# npm Publishing

Use this before publishing `@nodecue/blender-node-skills` for the first public alpha.

## Current Package

- Package: `@nodecue/blender-node-skills`
- Version: `0.1.0-alpha.0`
- Recommended first dist-tag: `alpha`
- Default installer command after publish:

```bash
npx @nodecue/blender-node-skills install
```

## Before Publishing

- Confirm the `@nodecue` npm scope exists and your npm account can publish public packages under it.
- If the `@nodecue` npm scope is unavailable, do not silently rename in the workflow. Decide the fallback package name first, then update `package.json`, README install commands, and release docs together.
- Configure the repository secret `NPM_TOKEN` in GitHub before running a real publish.
- Keep the GitHub repository private until the dry-run workflow succeeds.

## Local Checks

Run these from the skill repository root:

```bash
npm test
npm pack --dry-run
npm publish --dry-run --access public --tag alpha
```

The package contents should include only:

- `bin/`
- `skills/`
- `README.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `package.json`

It should not include local archives, `.env`, debug `.blend` files, caches, or test temp output.

## GitHub Workflow

Run the `Publish npm package` workflow manually:

1. First run with `publish=false` and `tag=alpha`.
2. Confirm the workflow passes install smoke, pack dry-run, and npm publish dry-run.
3. Add or verify the `NPM_TOKEN` repository secret.
4. Run again with `publish=true` and `tag=alpha`.

The workflow intentionally defaults to dry-run. A real publish requires explicitly selecting `publish=true`.

## After Publishing

Verify install from npm:

```bash
npx @nodecue/blender-node-skills install --force
```

Then confirm the installed skill folder contains:

```text
geometry-nodes/SKILL.md
geometry-nodes/rules/
geometry-nodes/patterns/
geometry-nodes/evals/
```

## Public Messaging

Describe this as an alpha Geometry Nodes skill package for agent workflows. Shader Nodes and Compositing Nodes are planned but not included yet.

Do not describe this as a complete Blender automation system. It is a reusable node-domain skill that can help NodeCue and external agents reason about Blender node graphs.
