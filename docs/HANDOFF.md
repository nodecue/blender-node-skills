# HANDOFF

Overwrite this file on every agent switch. It is not a history log — Git holds history. When the task is finished, clear or overwrite with an empty template.

**Task:** Issue #10 second slice — public skill and plugin validation (tools, node dumps, pytest, inventory).

**Done:**

- Node dumps, TSV generator, review file, and dump helpers committed under `docs/node-dumps/` and `tools/`.
- Skill, runtime-script, field-shape, TSV, and static plugin-package tests under `tests/`.
- `requirements-dev.txt` (pytest) and documented `python -m pytest tests -q` plus `python tools/gen_nodes_tsv.py --check`.
- `docs/research/github-primary-inventory.md` records migrated vs historical vs excluded surfaces.

**Not done:**

- Fresh-clone acceptance on a machine that has only this repository.
- Host plugin validation (JSON tests are static only).
- Live read-only Blender check through this clone.
- Final GitHub-primary authority declaration; Issue #10 remains open.
- PR / push (commit locally only unless the user asks).

**Files touched:**

- `tools/` (`gen_nodes_tsv.py`, `nodes_tsv_review.json`, `introspect_nodes.py`, `dump_tsv_evidence.py`)
- `docs/node-dumps/`
- `tests/` including `test_plugin_package.py` and `golden/run_skill_runtime_scripts.py`
- `requirements-dev.txt`
- `docs/research/github-primary-inventory.md`
- `docs/CURRENT.md`, `docs/HANDOFF.md`, `AGENTS.md`

**Risks / landmines:**

- Do not claim Issue #10 or GitHub-primary cutover complete.
- Do not delete or instruct deletion of any old local repo.
- Do not restore dual-authority or release-sync process.
- Static plugin tests do not prove live host discovery.

**Next action:** Independent review of this slice; later slices prove fresh clone, plugin host, and live read-only before any authority cutover.

**Last verified:** 2026-09-27
