## What changes

<!-- The behavior or guidance that changes, and the issue it addresses (Refs #...). -->

## Verification

- [ ] `python -m pytest tests -q`
- [ ] `python tools/gen_nodes_tsv.py --check` (if `nodes.tsv`, its review data, or the dumps changed)
- [ ] Live Blender run — version: <!-- e.g. 5.2.1, or "not run" -->
- [ ] Agent host run — host and install: <!-- or "not run" -->

## Checklist

- [ ] `CHANGELOG.md` has a line under **Unreleased** (or this change is not user-visible)
- [ ] No credentials, private paths, or unpublishable `.blend` files
