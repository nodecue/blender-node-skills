# Contributing

Public GitHub `main` is the product and development source. Branch from current public `main`. Work follows Issue → branch or worktree → pull request → review → merge.

## Where a change belongs

Skill behavior and guidance live under `skills/`. Plugin metadata, hooks, commands, README files, this guide, tests, tools, and other public files live in the same repository and the same pull-request path.

Open an issue before a larger change. The pull request links that issue and states the behavior or guidance that changes, the files in scope, the checks that were run, the evidence a reviewer can read, and the checks that were not run. Blender evidence names the Blender version. Host evidence names the host and the install or session that was exercised.

## Evidence

- Static checks cover text, links, tests, TSV generation, and plugin JSON. They do not prove live host discovery or live Blender behavior.
- Blender evidence covers the named version and the observed behavior.
- Host evidence covers the named host and the installation or session that was exercised. The current plugin acceptance target is Codex first. Claim support for a host after that host has been exercised.
- Owner acceptance is a separate decision from the checks above.

## What to leave out

Leave credentials, private corpora, machine-local absolute paths, and unrelated experiments out of issues, pull requests, and evidence.

A local commit, a public merge, closing an issue, a push, and a release are separate actions. Merge does not close the issue. Release still needs explicit authorization. This guide does not authorize a push or a release.
