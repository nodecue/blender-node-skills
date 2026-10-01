---
title: Cross-Version Differences
description: "What one Blender cannot report about another: renames, experimental gates, deprecations with non-drop-in replacements, the shapes socket changes take, and the bundled-asset capability boundary."
last_verified: "2026-10-01"
---

# Cross-version differences

Supported: **4.5 LTS, 5.0, 5.1, 5.2 LTS**.

**Read this only when** the user names a target version, the plan has to hold on more
than one version, a candidate node is unavailable on the connected version, or a
migration is requested. An ordinary build on the connected Blender does not need it.

Which nodes exist on which version is in `nodes.tsv` — the `version` column. This file
carries only what that column cannot say.

## Renamed, not removed

A rename reads as a removal plus an addition. Both rows are in `nodes.tsv`; the fact that
they are the same node is here.

| 4.5 identifier | 5.0+ identifier |
|---|---|
| `GeometryNodeClosureInput` | `NodeClosureInput` |
| `GeometryNodeClosureOutput` | `NodeClosureOutput` |
| `GeometryNodeCombineBundle` | `NodeCombineBundle` |
| `GeometryNodeSeparateBundle` | `NodeSeparateBundle` |
| `GeometryNodeEvaluateClosure` | `NodeEvaluateClosure` |

`ShaderNodeCombineRGB` and `ShaderNodeSeparateRGB` are 4.5-only and were dropped, not
renamed. `FunctionNodeCombineColor` and `FunctionNodeSeparateColor` exist on all four
versions and are the portable choice.

## Experimental gates

**A node existing is not the feature being usable.** While a feature is experimental its
node types are already registered — `nodes.new()` succeeds and readback looks normal —
but the preference is off, so the user cannot reach the node in the editor and the graph
will not behave. Nothing in a dump or a readback shows this.

Measured on each install, factory startup:

| Preference | 4.5 | 5.0 | 5.1 | 5.2 |
|---|---|---|---|---|
| `use_bundle_and_closure_nodes` | present, **off** | absent | absent | absent |
| `use_new_volume_nodes` | present, **off** | absent | absent | absent |
| `use_geometry_nodes_lists` | absent | present, **off** | present, **off** | absent |
| `use_geometry_bundle` | absent | absent | present, **off** | absent |

Absent means the gate is gone and the feature is official. Target the first version where
the preference is absent, unless the user says they enabled it.

The list family is the clearest case: `GeometryNodeList` exists on 5.0 alone and is
replaced in 5.1 by `GeometryNodeFieldToList` — the release that removes it is the release
that introduces the replacement. Both sit behind `use_geometry_nodes_lists` on 5.0 and
5.1, and the whole family is ungated from 5.2. List work should target 5.2.

Probing availability by creating a node is a **write**: Build/Edit only, never Explain.

## Deprecated, with a replacement that is not a drop-in

Neither the dumps nor RNA carries a deprecation flag, and both deprecated nodes still
create successfully on every supported version. Nothing in a live readback will tell you
to stop using them.

| Deprecated | Replace with |
|---|---|
| `FunctionNodeAlignEulerToVector` | `FunctionNodeAlignRotationToVector` |
| `FunctionNodeRotateEuler` | `FunctionNodeRotateRotation` |

Both pairs exist on all four versions, so the substitution is portable — but the rotation
travels on a different socket type in each pair, so an existing wire will not attach
without a conversion. Read both nodes live before swapping.

## What a socket change looks like when a plan is ported

Do not carry a socket list from one version to another. Resolve sockets from live
readback on the version you are connected to. These are the shapes the differences take,
and each fails differently:

- **A menu socket appears.** Positional wiring shifts by one, and the node does nothing
  sensible until the menu is set. A menu socket takes a string whose legal values live on
  the socket.
- **A generic socket's type follows what is connected.** The switch family reports
  different socket types on different versions; neither the type nor the identifier is
  stable across the step.
- **Inputs are appended.** Old identifiers still work, so a copied socket list is
  incomplete rather than wrong — which is why it fails late.

## Blender 5.2 API notes

- **Geometry Nodes modifier inputs.** In Blender 5.2, write a group input through
  `modifier.properties.inputs.Socket_n.value`, where `Socket_n` is the identifier read
  from the live node-group interface. The legacy `modifier["Socket_n"] = value` form
  errors on this version. Inspect the connected Blender's RNA before applying a
  version-specific modifier write; do not assume this path is portable to other releases.
- **Capture Attribute.** The Blender 5.2.0 node dump includes a `Selection` input on
  `GeometryNodeCaptureAttribute`; the 4.5.12, 5.0.1, and 5.1.2 dumps do not. Treat it as
  a 5.2-era interface addition and read the actual socket from the running version.

## Field capability

Field capability varies by node, mode, socket, and evaluation context across
Blender releases. Do not rely on static cross-version capability assumptions
or general family assertions: display shape transitions in draw layers do not
prove functional capability changes, and identical shapes do not prove identical
behavior.

For the connected Blender, `scripts/probe_node.py` and `scripts/read_graph.py`
report live socket state (`display_shape`, `hide_value`, `has_default_value`,
`type`). When a task depends on field evaluation, verify the specific node mode,
connections, and evaluated results against the running Blender.

## Bundled assets: a capability boundary

Whether a general-purpose asset library exists at all is a version fact:

| Blender | General-purpose Geometry Nodes assets |
|---|---|
| 4.5 | **none** — one smoothing group plus a hair-specific library |
| 5.0, 5.1 | an essentials library |
| 5.2 | essentials plus a dynamics library (cloth, hair, colliders, effectors) |

The asset directory is named differently on 4.5 than on 5.x; resolve it at runtime rather
than hardcoding either. A plan built around an essentials asset has no 4.5 path at all —
not a degraded one, none.

What is in a library and whether reusing one beats building the graph: `reuse.md`.
Enumerating them: `scripts/inspect_assets.py`.

## Evidence

Four live readbacks plus the experimental preferences, per version, in the development
repository under `docs/node-dumps/`. Not shipped.
