# Contributing

Skill changes and the other public files follow different paths. This is the current interim arrangement. A later migration may make this GitHub repository the product authority. That migration is not in effect.

## Where a change belongs

- Skill behavior and guidance live under `skills/`. Maintainers compare a skill pull request with the common released baseline and reconcile the accepted result into the skill source that the release is built from. After that reconciliation, a later release keeps the accepted result.
- README files, this contributing guide, plugin metadata, hooks, commands, and other files outside `skills/` are maintained in this repository. Those changes stay on their public pull request.

## Issues and pull requests

Open an issue before a larger change. The pull request links that issue and states the behavior or guidance that changes, the files in scope, the checks that were run, the evidence a reviewer can read, and the checks that were not run. Blender evidence names the Blender version. Host evidence names the host and the install or session that was exercised.

Maintainers record the released baseline commit, the pull request head, and the accepted result. Attribution stays with the contribution.

## Equivalent changes and later adjustments

When the accepted skill result matches the skill files in the public pull request byte for byte, maintainers keep that pull request and its attribution when practical.

When maintainers make a substantive adjustment, or the public branch has moved past the reviewed head, they open a maintainer pull request with the accepted result. They mark the original contribution superseded or partially adopted, link the two pull requests in both directions, and preserve attribution.

Overlapping edits need a manual three-way comparison against the common baseline. Valid work from both sides stays in the reconciled result. A drift or packaging check reports that files differ. Maintainers reconcile the overlap by hand, then release the reconciled result.

## Evidence

- Static checks cover text, links, and diff hygiene.
- Unit tests cover the cases they execute.
- Blender evidence covers the named version and the observed behavior.
- Host evidence covers the named host and the installation or session that was exercised. The current plugin acceptance target is Codex first. Claim support for a host after that host has been exercised.
- Owner acceptance is a separate decision from the checks above.

## What to leave out

Leave credentials, private corpora, machine-local absolute paths, and unrelated experiments out of issues, pull requests, and evidence.

A local commit, a local release sync, a public merge, a push, a release, and closing an issue are separate actions. This guide does not authorize a push or a release.
