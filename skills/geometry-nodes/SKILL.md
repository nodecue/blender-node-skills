---
name: geometry-nodes
version: "0.4"
description: Use when an agent must plan, build, modify, explain, or debug Blender Geometry Nodes with exact node identities, socket/link correctness, field/data-flow reasoning, asset node-group reuse, and readback-based repair.
---

# Geometry Nodes

## Overview
This skill guides Geometry Nodes graph construction and explanation. Use it to choose correct node identities, sockets, conversions, field consumers, and verification steps while using whatever Blender access path the host provides.

Work in small graph slices: plan intent, create or edit a few nodes, read the actual tree, repair mistakes, then continue. The goal is a functional and teachable node graph, not a one-shot node inventory.

## Evidence Requirements
Only use node behavior that is backed by this skill's rules, the local Geometry Nodes knowledge base, Blender manual exports, existing readback data, or a fresh Blender readback. Do not invent node identifiers, socket names, RNA properties, or unofficial abstractions.

When adding a new pattern or rule, include an `Evidence` section that points to the rule files, knowledge-base entries, manual pages, or readback artifact used to justify it.

## Build Loop
1. Parse the prompt into `target geometry`, `operation`, `driver signal`, `control parameters`, and `asset reuse candidates`.
2. Choose input source mode before editing:
   - **Process**: operate on existing geometry; keep `Group Input.Geometry` in the trunk.
   - **Generate**: create geometry from primitives/assets; bypass incoming geometry unless the user requested it.
3. Route to the narrowest rule or pattern file, then use exact headings like `Node Name — bl_idname`.
4. Build 2-3 related nodes at a time: geometry trunk first, then field drivers, then optional branches.
5. Read back the tree after each slice. Continue only from actual node names, socket names/identifiers, links, and interface sockets returned by Blender.
6. Frame related nodes with teaching labels after the slice verifies.
7. For graphs above 8 nodes, slice mode is mandatory. Do not emit or execute a full-graph node list first.
8. Do not rename ordinary Blender nodes or use per-node labels for explanation. Keep Blender's default node names; put all teaching notes, assumptions, and explanations on frames.

## Reliability Rules
1. Never invent `bl_idname`, node names, socket names, or writable property identifiers.
2. Blender may auto-rename nodes with `.001`; update all later references to the actual returned name.
3. Resolve sockets by exact name or identifier from readback. Duplicate visible labels require identifiers.
4. Write values to exactly one target at a time:
   - socket default: exact socket name/identifier from node readback.
   - node property: exact writable RNA property identifier from node metadata.
   Never fall back silently between socket defaults and node properties.
5. After each value write, verify the expected readback field changed. If it did not, treat the write as failed.
6. Before adding a group interface socket, read existing interface sockets. Do not duplicate same-name same-direction sockets.
7. Expose only controls the user explicitly named. Words like "complete" or "production-ready" do not mean "expose every parameter."
8. Keep one explicit geometry trunk from the chosen source to `Group Output`.
9. Field nodes do nothing visually until consumed by a data-flow node socket.
10. If a create/connect/write operation fails and returns suggestions or metadata, use one direct correction, then read the tree again.
11. Temporary aliases used by a host tool are not graph content. They must not be written into `node.name` or `node.label`.

## Geometry Nodes Mental Model
Geometry Nodes has two coupled lanes:

- **Data flow lane**: geometry sockets carry mesh, curve, points, volume, or instances from source to sink. These nodes transform visible geometry.
- **Field lane**: field-compatible sockets define per-element computations. Fields are evaluated lazily by downstream data-flow nodes.

Every graph needs a reachable trunk:

`chosen source -> geometry operations/conversions -> Group Output.Geometry`

The source can be `Group Input.Geometry`, a generated primitive, an imported/asset node group, or a branch assembled from several sources. Generated graphs may leave `Group Input.Geometry` disconnected.

Common failure pattern: the data-flow trunk exists, but a field driver is never connected to a concrete consumer such as `Selection`, `Offset`, `Scale`, `Density`, or `Material Index`.

## Core Concepts

### Fields
- A field is a function evaluated per element in the context of a consumer node.
- The same field connected to two consumers can produce different results if the geometry/domain changed.
- Preserve field values across topology or representation changes with `Capture Attribute`.
- Circle sockets expect single values. Diamond sockets can accept fields.

### Domains
- Common domains: Point, Edge, Face, Face Corner, Spline, Instance.
- Domain conversion can interpolate or change meaning. Boolean domain conversion follows set-like rules.
- Always confirm the target consumer's domain before wiring selections, masks, or captured attributes.

### Geometry Types
- A Geometry socket may contain Mesh, Curve, Point Cloud, Volume, and Instances together.
- Conversion nodes are semantic boundaries. After Mesh/Curve/Points/Volume conversion, re-check available domains and attributes.
- Reroutes are organization-only and type-polymorphic; infer their type from connected neighbors.

### Instances
- Instances are references with transforms, not full copies.
- Processing usually applies to unique source geometry, not each instance.
- Use `Realize Instances` only when later operations need per-instance unique geometry.
- Record whether the graph should preserve instances for performance or realize them for editability.

### Types
- Valid links can still be semantically wrong when implicit conversion occurs.
- Numeric types may coerce; vector/float/color conversions can change meaning.
- When relying on conversion, state why the interpretation is intended.

## Graph Relationship Rules
These are observable graph relationships, not Blender API concepts:

1. **Geometry path**: a Geometry socket chain must run from a chosen input, generated primitive, or group node to `Group Output.Geometry`.
2. **Field producer -> consumer**: field nodes only matter when their output reaches a concrete consuming socket such as `Selection`, `Offset`, `Scale`, `Density Factor`, or `Material Index`.
3. **Displacement**: a vector direction and a magnitude signal can form an offset for `Set Position.Offset`.
4. **Scatter**: a surface, curve, volume, or vertices become points before `Instance on Points`; keep instances unless later nodes require real geometry.
5. **Composition**: independent geometry branches join through real nodes such as `Join Geometry`, `Switch`, `Mesh Boolean`, or a reusable `Group`.
6. **Repeat propagation**: repeated geometry output feeds the next iteration's geometry input; read back zone items before assuming socket names.
7. **Asset composition**: reusable node groups can replace primitive subgraphs when their interface and purpose match the prompt better than rebuilding.

## Prompt Translation
Map prompt phrases to node roles before editing:

- "along normal/surface direction" -> direction source for displacement or alignment.
- "noise / random / mask / curve controlled" -> field producer plus shaping chain.
- "density / scale / seed control" -> explicitly named interface controls only.
- "grow / iterate / accumulate" -> repeat or simulation pattern depending on within-frame vs cross-frame state.
- "assemble / modules / existing node groups" -> group-node reuse and `Join Geometry` orchestration.

When wording is ambiguous, enumerate competing interpretations, choose one minimal interpretation, and record the assumption. Ask only when one unresolved choice materially changes topology.

## Group Input Policy
| Mode | Use When | Group Input.Geometry |
|---|---|---|
| Process | Scatter/deform/annotate existing object geometry | Connected into trunk |
| Generate | Create a primitive, procedural object, or asset assembly from scratch | Disconnected unless explicitly needed |

Parameter exposure rule: Only expose parameters the user explicitly named. Example: "scatter rocks with density control" exposes Density, not Seed, Rotation, Scale Min/Max, or overlap controls.

## Asset / Node Group Reuse
Use existing node groups when they are semantically closer than a primitive rebuild.

1. Inspect available asset node groups only through host-authorized Blender asset library access.
2. Compare asset purpose, interface sockets, tags/name, and expected output geometry.
3. Reuse only when the group's interface is understandable enough to wire and explain.
4. After inserting a group node, read its sockets and document what each connected input/output contributes.
5. If an asset is close but opaque, prefer a simpler primitive graph unless the user asked to reuse existing assets.

## Role Lookup
Use [`rules/node-role-catalog.md`](rules/node-role-catalog.md) when a prompt describes a role such as source, field producer, shaper, consumer, point generator, instancer, branch combiner, or attribute handoff. The catalog gives candidate nodes and common misuses without prescribing a single answer.

Use [`rules/readback-repair.md`](rules/readback-repair.md) when readback shows missing links, unchanged values, renamed nodes, duplicate socket labels, or visually inert graphs.

## Node Lookup Procedure
1. Parse intent into operations and representation transitions.
2. Open the narrowest rule file from the index.
3. Match exact `Node Name — bl_idname`.
4. Read `Inputs`, `Outputs`, then `Notes`.
5. If socket type is missing or unclear, infer cautiously and record the inference.
6. Open additional rules only for missing required nodes.

## Recommended Planning Notes
Keep planning notes compact and tied to execution:

- `Intent`: one-line goal.
- `Input Source Policy`: Process or Generate, with reason.
- `Slice Plan`: ordered slices of 2-3 nodes.
- `Current Slice Nodes`: exact `Node Name — bl_idname` only for the active slice.
- `Key Links`: source socket -> target socket in plain language.
- `Conversions`: mesh/curve/points/instances/volume boundaries.
- `Assumptions`: chosen interpretation for ambiguous topology choices.
- `Gaps`: missing nodes, sockets, assets, or unverified readback.

## Rules Index
### Geometry Core
- [`rules/geometry-read.md`](rules/geometry-read.md): geometry state reads and identity/sampling reads
- [`rules/geometry-operations.md`](rules/geometry-operations.md): geometry trunk edits and transforms
- [`rules/attribute.md`](rules/attribute.md): capture/store/remove attribute workflows
- [`rules/node-role-catalog.md`](rules/node-role-catalog.md): role-based candidate nodes with evidence-backed constraints
- [`rules/readback-repair.md`](rules/readback-repair.md): observable readback symptoms and repairs

### Input Families
- [`rules/input-constant.md`](rules/input-constant.md): literal/asset-like inputs
- [`rules/input-scene.md`](rules/input-scene.md): scene/object/camera/time/viewport inputs
- [`rules/input-import.md`](rules/input-import.md): file import nodes
- [`rules/input-gizmo.md`](rules/input-gizmo.md): interactive gizmo inputs

### Representation Families
- [`rules/mesh-primitives.md`](rules/mesh-primitives.md): mesh source generation
- [`rules/mesh-read.md`](rules/mesh-read.md): mesh topology/state reads
- [`rules/mesh-operations.md`](rules/mesh-operations.md): mesh edits/conversions
- [`rules/curve-primitives.md`](rules/curve-primitives.md): curve source generation
- [`rules/curve-read.md`](rules/curve-read.md): curve state reads
- [`rules/curve-operations.md`](rules/curve-operations.md): curve edits/conversions
- [`rules/point.md`](rules/point.md): point distribution/conversions
- [`rules/instances.md`](rules/instances.md): instance create/transform/realize
- [`rules/volume-sample.md`](rules/volume-sample.md): grid sampling/differential operators
- [`rules/volume-operations.md`](rules/volume-operations.md): volume/grid construction/editing
- [`rules/generate.md`](rules/generate.md): generate-category remainder

### Utility Families
- [`rules/texture.md`](rules/texture.md): procedural/image texture nodes
- [`rules/color.md`](rules/color.md): color transform/mix nodes
- [`rules/simulation.md`](rules/simulation.md): simulation zone boundary nodes and frame-to-frame state flow
- [`rules/utilities-field.md`](rules/utilities-field.md): field evaluation/statistics
- [`rules/utilities-math.md`](rules/utilities-math.md): scalar/integer math/remap
- [`rules/utilities-vector.md`](rules/utilities-vector.md): vector math/decompose/compose
- [`rules/utilities-rotation.md`](rules/utilities-rotation.md): rotation conversion/alignment
- [`rules/utilities-matrix.md`](rules/utilities-matrix.md): matrix/transform compose/decompose
- [`rules/utilities-text.md`](rules/utilities-text.md): string operations
- [`rules/utilities-misc.md`](rules/utilities-misc.md): switch/random/join helpers
- [`rules/system-misc.md`](rules/system-misc.md): layout/zone/system/tool support

## Patterns Index
**Archetype patterns**:
- [`patterns/distribution-archetype.md`](patterns/distribution-archetype.md): scatter/instance a source across a target
- [`patterns/stitching-archetype.md`](patterns/stitching-archetype.md): compose multiple independent parts through Join Geometry

**Algorithmic patterns**:
- [`patterns/capture-then-propagate.md`](patterns/capture-then-propagate.md): freeze field values before geometry changes
- [`patterns/density-controlled-scatter.md`](patterns/density-controlled-scatter.md): control surface scatter with boolean or float density fields
- [`patterns/index-normalized-shaping.md`](patterns/index-normalized-shaping.md): per-element shaping via Index + Float Curve + Map Range
- [`patterns/material-attribute-handoff.md`](patterns/material-attribute-handoff.md): pass material decisions or numeric masks through geometry
- [`patterns/normal-projection-removal.md`](patterns/normal-projection-removal.md): surface-preserving deformation via vector projection
- [`patterns/points-to-volume-to-mesh.md`](patterns/points-to-volume-to-mesh.md): point cloud -> volume -> organic mesh
- [`patterns/repeat-zone-iterative-smoothing.md`](patterns/repeat-zone-iterative-smoothing.md): multi-pass smoothing with Repeat Zone
- [`patterns/repeat-zone-selection-expansion.md`](patterns/repeat-zone-selection-expansion.md): selection dilation with Repeat Zone + domain hop
- [`patterns/surface-displacement.md`](patterns/surface-displacement.md): move geometry with Set Position using verified vector and field drivers
