# Geometry Nodes node dumps

Per-version identity dumps of every node type creatable in a `GeometryNodeTree`,
read straight out of a running Blender by `tools/introspect_nodes.py`. Each
record carries the node's label, tooltip, every input and output socket as
`[name, identifier, type, rna_class]`, and its writable RNA properties with
enum values.

The fourth socket field exists because `socket.type` is coarse: a 3D and a 2D
vector both read `VECTOR`, and only the RNA class separates
`NodeSocketVector` from `NodeSocketVector2D`. That difference is a real
compatibility risk — three components fed into a 2D socket silently lose one.

Each dump also records `experimental`: every boolean under
`preferences.experimental` with its factory-startup value. See
[RNA-creatable is not available](#rna-creatable-is-not-available) for why a dump
that omits this is not enough to answer "can I use this node".

These are **evidence, not product**. Nothing here ships inside
`skills/geometry-nodes/`; the skill consumes the *differences* between
these files, which is the part no single install can report about itself.

## Files

| File | Blender | Creatable node types | Source |
|---|---|---|---|
| `gn-4.5.12.json` | 4.5.12 LTS | 297 | `blender_vers/stable/blender-4.5.12-…` |
| `gn-5.0.1.json` | 5.0.1 | 321 | PyPI `bpy==5.0.1` wheel (cp311, arm64) — no `experimental` key |
| `gn-5.1.2.json` | 5.1.2 | 333 | `blender_vers/stable/blender-5.1.2-…` |
| `gn-5.2.0.json` | 5.2.0 LTS | 360 | `/Applications/Blender.app` |

The `tsv-evidence-*.json` files come from `tools/dump_tsv_evidence.py` and add
the two facts the identity dumps lack: field socket display shapes and the Add
menu each node lives in. Two of them were taken on a later patch release than
the matching identity dump (4.5.13 against 4.5.12, 5.2.1 against 5.2.0). The
node sets agree; `nodes-tsv-manifest.md` records both versions per source.

The chain is unbroken: **297 → 321 → 333 → 360**. Historical adjacent-version
counts (dump-diff markdown is not shipped in this repository):

| Span | Added | Removed | Socket diffs |
|---|---:|---:|---:|
| 4.5.12 vs 5.0.1 | 31 | 7 | 35 |
| 5.0.1 vs 5.1.2 | 13 | 1 | 7 |
| 5.1.2 vs 5.2.0 | 27 | 0 | 10 |
| 4.5.12 vs 5.2.0 (spans three) | 70 | 7 | 45 |
| 5.0.1 vs 5.2.0 (spans two) | 40 | 1 | 16 |

### Why 5.1 was worth downloading

5.1 was previously skipped as unobtainable — "not installed locally and PyPI has
no 5.1 wheel". The wheel part is true; the conclusion was not. The official
archive carries `blender-5.1.{0,1,2}-macos-arm64.dmg` under
`https://download.blender.org/release/Blender5.1/`, so "cannot get it" was
really "did not download it". One download closed the gap.

Interpolating across the hole had already produced shipped errors. Everything
that appeared between 5.0 and 5.2 was attributed to 5.2, because 5.2 was the
only dump that had it:

- `GeometryNodeList` was documented as 5.0–5.1, removed in 5.2. It exists on
  **5.0 only** and was removed in **5.1**.
- `GeometryNodeFieldToList`, its replacement, was documented as 5.2+. It exists
  from **5.1** — an agent on 5.1 was told to use a node that had been deleted
  and that its replacement was unavailable.
- Ten further nodes carried a `5.2+` bound that should have read `5.1+`.
- `GeometryNodeListGetItem` renamed its element-type property from `data_type`
  to `socket_type` in **5.1**, not 5.2 — a rename no 5.0/5.2 comparison can
  place.

5.1 is also the minimum version of Blender's official Lab MCP, so the gap sat
exactly where that channel starts.

## RNA-creatable is not available

**These dumps report what `nodes.new()` accepts, which is a larger set than what
a user can actually use.** While a feature is experimental its node types are
already registered, so `nodes.new()` succeeds and readback looks entirely
normal — but the preference gating the feature is off, the node is not in the
editor's Add menu, and the graph will not behave. The creatable set gives a
**false positive** for the whole experimental period.

This is measured, not inferred. On 5.1.2, dumping with
`use_geometry_nodes_lists` and `use_geometry_bundle` forced **on** produces the
same 333 creatable types as the default-off dump — the set does not move. The
flags change whether the feature works, not whether the class registers, so no
amount of node introspection can see the gate. That is why `experimental` is
recorded as a separate top-level key.

Measured flag states (`--factory-startup`, so these are defaults):

| Preference | 4.5.12 | 5.0.1 | 5.1.2 | 5.2.0 | Gates |
|---|---|---|---|---|---|
| `use_new_volume_nodes` | present, **off** | ? | absent | absent | the volume/SDF grid nodes |
| `use_bundle_and_closure_nodes` | present, **off** | ? | absent | absent | bundle and closure nodes |
| `use_geometry_nodes_lists` | absent | ? | present, **off** | absent | `ListGetItem`, `ListLength`, `FieldToList` |
| `use_geometry_bundle` | absent | ? | present, **off** | absent | `Get`/`SetGeometryBundle` |

A flag disappearing is the feature graduating: the 5.2 column has none of these,
and 5.2 is where each of those features gets its first manual page.

This resolves a discrepancy the version audit raised. Eleven volume/SDF grid
nodes are marked `5.0+` in the rules even though the 4.5.12 dump can create
them — `use_new_volume_nodes` is why, and **those markers are correct as
written.** The same mechanism explains why `GeometryNodeFieldToList` exists in
the 5.1 RNA but has no 5.1 manual page.

**Known gap: the 5.0 column is untested.** There is no local 5.0 install and
`gn-5.0.1.json` came from the PyPI wheel before this field existed, so it
carries no `experimental` key. The absence of a 5.0 manual page for the lists
nodes suggests they were experimental there too, but that is inference, not
measurement — the same kind of inference that produced the errors above. Closing
it needs a 5.0 build from the release archive, or a wheel run once the field
exists.

## Regenerating

`--factory-startup` is required — user add-ons register extra node types and
would change the set of creatable classes.

### The versions root

Keeping every build under one root is what makes this reproducible. The layout
is one directory per release channel, each holding builds extracted as
downloaded:

```
~/blender_vers/<channel>/blender-<version>-<platform>+<tag>.<hash>/
```

`tools/introspect_nodes.py --discover` walks that root, takes each version from
its directory name, and dumps every build it finds to `gn-<version>.json`:

```bash
python tools/introspect_nodes.py --discover --dry-run
```

Drop `--dry-run` to write the dumps. `BLENDER_VERSIONS_ROOT` (default
`~/blender_vers`) or `--versions-root` moves the root; `stable` wins when two
channels carry the same version, and non-Blender builds (upbge, bforartists)
are skipped by name.

**This layout is a maintainer convention, not a product assumption.** Nothing
in `skills/` knows about it, and no path to it is written into any tool.

Builds come from `https://download.blender.org/release/Blender<major.minor>/`,
which archives every release including the ones with no `bpy` wheel.

### One install at a time

```bash
python tools/introspect_nodes.py --blender "/Applications/Blender.app/Contents/MacOS/Blender" \
  --output docs/node-dumps/gn-5.2.0.json
```

or by driving Blender yourself:

```bash
"/Applications/Blender.app/Contents/MacOS/Blender" -b --factory-startup \
  --python tools/introspect_nodes.py -- --output docs/node-dumps/gn-5.2.0.json
```

For a version with no local install, use the PyPI wheel in its own venv
(Python 3.11):

```bash
python3.11 -m venv /tmp/bpy501 && /tmp/bpy501/bin/pip install bpy==5.0.1
/tmp/bpy501/bin/python tools/introspect_nodes.py --output docs/node-dumps/gn-5.0.1.json
```

The wheel dump was cross-checked against a run with `BLENDER_USER_RESOURCES`
pointed at an empty directory: byte-identical, so the local `Blender/5.0/`
config contributes nothing.

Dump-diff tooling is not part of this public repository. Identity dumps here
are the inputs to `tools/gen_nodes_tsv.py`.

The 4.5.12 and 5.1.2 dumps were both reproduced byte-for-byte from the versions
root on 2026-08-08, including the 4.5.12 one originally taken from
`/Applications/Blender 4.5.app`.

## Agreement with the manual 4.5 → 5.2 audit

The 4.5.12 → 5.2.0 comparison reproduces the earlier manual socket audit exactly: 45 socket
differences, and the same 45 node types — set equality, not just a matching
count.

Reaching that required the RNA class field. On the
`[name, identifier, type]` triple the diff found 44, missing
`GeometryNodeCameraInfo`, whose `Sensor` and `Shift` outputs are 3D vectors on
4.5 and 2D on 5.2 — `len(socket.default_value)` is 3 then 2, verified live —
while `socket.type` reads `VECTOR` on both. That change landed between 5.0 and
5.2; the 4.5 → 5.0 diff does not contain it.
