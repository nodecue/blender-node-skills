---
name: geometry-nodes
version: "0.6"
description: Use for Blender Geometry Nodes work requiring exact node and socket identities with live readback.
---

# Geometry Nodes

## Overview
Build, modify, and explain Geometry Nodes graphs through whatever Blender access path the host provides: pick correct node identities, sockets, conversions, and field consumers, then verify against live readback.

Work in small graph slices — plan intent, edit a few nodes, read the actual tree, repair, continue. The goal is a functional and teachable node graph, not a one-shot node inventory.

## Modes
- **Build** — create or modify a graph. Decide from the prompt and a readback of the current scene whether to start a new tree or extend and repair the active one.
- **Explain** — strictly read-only. Read the graph and explain it. Never create, connect, delete, mute, reorder, or write values in explain mode, including frames and teaching labels. When a change would improve the graph, describe it instead of making it.

## Build Loop
1. Parse the prompt into `target geometry`, `operation`, `driver signal`, `control parameters`, and `asset reuse candidates`.
2. Before any edit, settle the input source mode (Group Input Policy) and the running Blender version (Version Awareness).
3. Route to the narrowest rule or pattern file (Lookup), then match exact headings like `Node Name — bl_idname`.
4. Build 2-3 related nodes per slice: geometry trunk first, then field drivers, then optional branches.
5. Read the tree back after each slice. Continue only from actual node names, socket names/identifiers, links, and interface sockets returned by Blender.
6. Frame the slice with a teaching label once it verifies.
7. For graphs above 8 nodes, slice mode is mandatory. Do not emit or execute a full-graph node list first.
8. Keep Blender's default node names. Never rename ordinary nodes or use per-node labels for explanation — teaching notes, assumptions, and explanations belong on frames.

## Reliability Rules
1. Never invent `bl_idname`, node names, socket names, or writable property identifiers.
2. Blender may auto-rename nodes with `.001`; update every later reference to the actual returned name.
3. Resolve sockets by exact name or identifier from readback. Duplicate visible labels require identifiers.
4. Write values to exactly one target at a time — either a socket default (exact socket name/identifier from node readback) or a node property (exact writable RNA property identifier from node metadata). Never fall back silently between socket defaults and node properties.
5. After each value write, verify the expected readback field changed. If it did not, treat the write as failed.
6. Read existing interface sockets before adding one. Do not duplicate same-name same-direction sockets.
7. Keep one explicit geometry trunk from the chosen source to `Group Output`.
8. Field nodes do nothing visually until consumed by a data-flow node socket.
9. If a create/connect/write operation fails and returns suggestions or metadata, apply one direct correction, then read the tree again.
10. Temporary aliases used by a host tool are not graph content. Never write them into `node.name` or `node.label`.

### Evidence Requirements
Only use node behavior backed by this skill's rules, the local Geometry Nodes knowledge base, Blender manual exports, existing readback data, or a fresh Blender readback. Do not invent node identifiers, socket names, RNA properties, or unofficial abstractions. When adding a pattern or rule, include an `Evidence` section pointing to the rule files, knowledge-base entries, manual pages, or readback artifact behind it.

## Version Awareness
1. Read the Blender version (`bpy.app.version` or host metadata) before building.
2. Use only nodes and patterns available in that version. Entries marked `Blender 5.0+` must not be requested from 4.5, and entries marked `Blender 5.2+` must not be requested from 4.5/5.0/5.1.
3. When the running version is newer than an entry's `verified` versions, create the node live and read back its actual sockets instead of trusting the written socket list.
4. For entries with a `Compatibility` note, always resolve sockets from live readback — never reuse identifiers from an older baseline. 4.5 and 5.2 differ on visible socket names, menu sockets, dynamic defaults, and some socket subtypes.
5. `GeometryNodeList` exists on Blender 5.0-5.1 but was removed in 5.2; on 5.2+ use `GeometryNodeFieldToList` or `GeometryNodeClosureToList` instead. Version-bounded entries stay in the rules for as long as this skill supports the versions they apply to.

## Group Input Policy
| Mode | Use When | `Group Input.Geometry` |
|---|---|---|
| Process | Scatter/deform/annotate existing object geometry | Connected into the trunk |
| Generate | Create a primitive, procedural object, or asset assembly from scratch | Disconnected unless explicitly needed |

Only expose parameters the user explicitly named. "Scatter rocks with density control" exposes Density — not Seed, Rotation, Scale Min/Max, or overlap controls. Words like "complete" or "production-ready" do not mean "expose every parameter."

## Prompt Translation
Map prompt phrases to node roles before editing:

- "along normal/surface direction" -> direction source for displacement or alignment.
- "noise / random / mask / curve controlled" -> field producer plus shaping chain.
- "density / scale / seed control" -> explicitly named interface controls only.
- "grow / iterate / accumulate" -> repeat or simulation pattern depending on within-frame vs cross-frame state.
- "assemble / modules / existing node groups" -> group-node reuse and `Join Geometry` orchestration.

When wording is ambiguous, enumerate competing interpretations, choose one minimal interpretation, and record the assumption. Ask only when one unresolved choice materially changes topology.

## Geometry Nodes Mental Model
Geometry Nodes has two coupled lanes:

- **Data flow lane**: geometry sockets carry mesh, curve, points, volume, or instances from source to sink. These nodes transform visible geometry.
- **Field lane**: field-compatible sockets define per-element computations, evaluated lazily by downstream data-flow nodes.

Blender 5.2 adds two more data shapes: **lists** (first-class ordered value collections with generic element types — `Field to List`, `Filter List`, `Sort List`, `Get List Item`; the element type follows what you connect, not Float-only) and **bundles** (a geometry can carry an attached bundle alongside its components and attributes — `Set/Get Geometry Bundle`).

Every graph needs a reachable trunk: `chosen source -> geometry operations/conversions -> Group Output.Geometry`. The source can be `Group Input.Geometry`, a generated primitive, an imported/asset node group, or a branch assembled from several sources; generated graphs may leave `Group Input.Geometry` disconnected.

Common failure pattern: the data-flow trunk exists, but a field driver never reaches a concrete consumer such as `Selection`, `Offset`, `Scale`, `Density`, or `Material Index`.

### Core Concepts
- **Fields**: a field is a function evaluated per element in its consumer's context, so the same field on two consumers can differ if the geometry or domain changed. Preserve values across topology or representation changes with `Capture Attribute`. Circle sockets expect single values; diamond sockets accept fields.
- **Domains**: Point, Edge, Face, Face Corner, Spline, Instance. Conversion can interpolate or change meaning (boolean conversion follows set-like rules). Confirm the consumer's domain before wiring selections, masks, or captured attributes.
- **Geometry types**: one Geometry socket may hold Mesh, Curve, Point Cloud, Volume, and Instances together. Conversion nodes are semantic boundaries — after them, re-check available domains and attributes. Reroutes are organization-only and type-polymorphic; infer their type from connected neighbors.
- **Instances**: references with transforms, not copies. Processing usually applies to the unique source geometry, not per instance. Use `Realize Instances` only when later operations need per-instance unique geometry, and record whether the graph should preserve instances for performance or realize them for editability.
- **Types**: a valid link can still be semantically wrong when implicit conversion occurs. Numeric types may coerce, and vector/float/color conversions can change meaning — when relying on conversion, state why the interpretation is intended.

### Graph Relationship Rules
These are observable graph relationships, not Blender API concepts:

1. **Geometry path**: a Geometry socket chain must run from a chosen input, generated primitive, or group node to `Group Output.Geometry`.
2. **Field producer -> consumer**: field nodes only matter when their output reaches a concrete consuming socket such as `Selection`, `Offset`, `Scale`, `Density Factor`, or `Material Index`.
3. **Displacement**: a vector direction and a magnitude signal can form an offset for `Set Position.Offset`.
4. **Scatter**: a surface, curve, volume, or vertices become points before `Instance on Points`; keep instances unless later nodes require real geometry.
5. **Composition**: independent geometry branches join through real nodes such as `Join Geometry`, `Switch`, `Mesh Boolean`, or a reusable `Group`.
6. **Repeat propagation**: repeated geometry output feeds the next iteration's geometry input; read back zone items before assuming socket names.
7. **Asset composition**: reusable node groups can replace primitive subgraphs when their interface and purpose match the prompt better than rebuilding.

## Annotation Language
1. Write frame labels, teaching notes, and explanations in the language of the user's prompt, unless the user names another language.
2. Never translate node names, socket names, or `bl_idname` identifiers — keep them exactly as Blender displays them. Translated node names break the user's path from annotation to Blender's UI and to tutorials.
3. When the annotation language is not English, prefer short bilingual frame labels pairing the concept with its English Blender term, for example `噪声高度控制 — Noise Height Control`. Long labels get clipped in the node editor.

## Lookup
1. Parse intent into operations and representation transitions.
2. Open the narrowest rule file from the index below; open more only for nodes still missing.
3. Match the exact `Node Name — bl_idname`, then read `Inputs`, `Outputs`, `Notes`.
4. If a socket type is missing or unclear, infer cautiously and record the inference.

### Role Lookup
Use [`rules/node-role-catalog.md`](rules/node-role-catalog.md) when a prompt describes a role — source, field producer, shaper, consumer, point generator, instancer, branch combiner, or attribute handoff. It gives candidate nodes and common misuses without prescribing a single answer.

Use [`rules/readback-repair.md`](rules/readback-repair.md) when readback shows missing links, unchanged values, renamed nodes, duplicate socket labels, or visually inert graphs.

### Asset / Node Group Reuse
Use existing node groups when they are semantically closer than a primitive rebuild.

1. Inspect available asset node groups only through host-authorized Blender asset library access.
2. Compare asset purpose, interface sockets, tags/name, and expected output geometry.
3. Reuse only when the group's interface is understandable enough to wire and explain.
4. After inserting a group node, read its sockets and document what each connected input/output contributes.
5. If an asset is close but opaque, prefer a simpler primitive graph unless the user asked to reuse existing assets.

## Recommended Planning Notes
Keep planning notes compact and tied to execution:

- `Intent`: one-line goal.
- `Input Source Policy`: Process or Generate, with reason.
- `Slice Plan`: ordered slices of 2-3 nodes.
- `Current Slice Nodes`: exact `Node Name — bl_idname` for the active slice only.
- `Key Links`: source socket -> target socket in plain language.
- `Conversions`: mesh/curve/points/instances/volume boundaries.
- `Assumptions`: chosen interpretation for ambiguous topology choices.
- `Gaps`: missing nodes, sockets, assets, or unverified readback.

## Rules Index
- **Geometry core** — [state/identity/sampling reads](rules/geometry-read.md) · [trunk edits and transforms](rules/geometry-operations.md) · [capture/store/remove attributes](rules/attribute.md) · [generate-category remainder](rules/generate.md)
- **Diagnosis** — [role-based candidate nodes](rules/node-role-catalog.md) · [readback symptoms and repairs](rules/readback-repair.md)
- **Inputs** — [literal/asset-like](rules/input-constant.md) · [scene/object/camera/time/viewport](rules/input-scene.md) · [file import](rules/input-import.md) · [interactive gizmos](rules/input-gizmo.md)
- **Mesh** — [primitives](rules/mesh-primitives.md) · [topology/state reads](rules/mesh-read.md) · [edits/conversions](rules/mesh-operations.md)
- **Curve** — [primitives](rules/curve-primitives.md) · [state reads](rules/curve-read.md) · [edits/conversions](rules/curve-operations.md)
- **Points and instances** — [point distribution/conversions](rules/point.md) · [instance create/transform/realize](rules/instances.md)
- **Volume** — [grid sampling/differential operators](rules/volume-sample.md) · [grid construction/editing](rules/volume-operations.md)
- **Zones and system** — [simulation zones, cross-frame state](rules/simulation.md) · [layout/zone/system/tool support](rules/system-misc.md)
- **Utilities** — [field evaluation/statistics](rules/utilities-field.md) · [scalar/integer math/remap](rules/utilities-math.md) · [vector math/decompose/compose](rules/utilities-vector.md) · [rotation conversion/alignment](rules/utilities-rotation.md) · [matrix/transform compose/decompose](rules/utilities-matrix.md) · [string operations](rules/utilities-text.md) · [switch/random/join helpers](rules/utilities-misc.md)
- **Shading inputs** — [procedural/image textures](rules/texture.md) · [color transform/mix](rules/color.md)

## Patterns Index
**Archetypes**
- [`patterns/distribution-archetype.md`](patterns/distribution-archetype.md): scatter/instance a source across a target
- [`patterns/stitching-archetype.md`](patterns/stitching-archetype.md): compose multiple independent parts through Join Geometry

**Algorithmic**
- [`patterns/capture-then-propagate.md`](patterns/capture-then-propagate.md): freeze field values before geometry changes
- [`patterns/density-controlled-scatter.md`](patterns/density-controlled-scatter.md): control surface scatter with boolean or float density fields
- [`patterns/index-normalized-shaping.md`](patterns/index-normalized-shaping.md): per-element shaping via Index + Float Curve + Map Range
- [`patterns/material-attribute-handoff.md`](patterns/material-attribute-handoff.md): pass material decisions or numeric masks through geometry
- [`patterns/normal-projection-removal.md`](patterns/normal-projection-removal.md): surface-preserving deformation via vector projection
- [`patterns/points-to-volume-to-mesh.md`](patterns/points-to-volume-to-mesh.md): point cloud -> volume -> organic mesh
- [`patterns/repeat-zone-iterative-smoothing.md`](patterns/repeat-zone-iterative-smoothing.md): multi-pass smoothing with Repeat Zone
- [`patterns/repeat-zone-selection-expansion.md`](patterns/repeat-zone-selection-expansion.md): selection dilation with Repeat Zone + domain hop
- [`patterns/surface-displacement.md`](patterns/surface-displacement.md): move geometry with Set Position using verified vector and field drivers
