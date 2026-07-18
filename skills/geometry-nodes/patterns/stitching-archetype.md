---
id: stitching-archetype
name: 拼接术 (Stitching Archetype)
description: "Compose multiple independent sub-models (primitives, node groups, scatter outputs) into one assembly via Join Geometry."
category: generation
tags: 拼接术, assembly, join, 组装, modular, composition
blender_support: "5.0+"
blender_verified: 5.1
status: stable
---

## 拼接术 (Stitching Archetype)

**Intent:** The output is conceptually several independent parts — roof + walls + floor, trunk + branches + leaves, multiple furniture pieces. Each part is built (or pre-built as a node group) separately, then joined into a single geometry at a single composition root.

Recognize this archetype from prompts like: "拆成屋顶、墙、地面拼装", "把主干、树枝、树叶组装成一棵树", "用多个 node group 拼装成一栋木屋". The verb is **组装 / 拼接 / compose**, not *add* or *deform*.

## Evidence

- `rules/utilities-misc.md`: `GeometryNodeJoinGeometry`, `GeometryNodeSwitch`
- `rules/mesh-operations.md`: `GeometryNodeMeshBoolean`
- `rules/geometry-operations.md`: `GeometryNodeTransform`
- `rules/geometry-read.md`: `GeometryNodeGroup`
- `rules/geometry-read.md`: `GeometryNodeSetMaterial`, `GeometryNodeSetMaterialIndex`
- `rules/instances.md`: `GeometryNodeRealizeInstances`

## Signature

- **In:** N independent geometries, typically from `Group` nodes (sub-trees) or primitives, optionally each with its own transform
- **Out:** `geometry` (GEOMETRY) — merged assembly
- **Params:** per-branch toggles, per-branch transforms, material slots per branch

## Data Flow

```
branch_A (Group / primitive / scatter) ─┐
branch_B (Group / primitive / scatter) ─┼─→ Join Geometry ─→ (optional root Transform) ─→ output
branch_C (Group / primitive / scatter) ─┘
```

## Core Chain

1. Build each branch independently. Each branch is either:
   - A `Group — GeometryNodeGroup` call to a pre-built sub-tree (asset library module, reusable part).
   - An inline primitive + small transform/material chain.
   - A scatter sub-tree (see [distribution-archetype]) producing instances.
2. `Join Geometry — GeometryNodeJoinGeometry` as the single composition root.
   - Each branch feeds one of the multi-input `Geometry` slots.
   - Order matters only for first-wins attribute propagation (see mistakes).
3. Optional root-level `Transform Geometry — GeometryNodeTransform` after Join for placing the whole assembly.
4. Output `Geometry` → `Group Output` node's `Geometry` input.

## Variants

- **Pure Group composition** (A9 canonical): every branch is a `GeometryNodeGroup` call. The outer graph is almost entirely Group + Join + a few Switches for toggles. Example: procedural building where roof/walls/floor are each a sub-group.
- **Mixed (Group + inline)**: some branches are pre-built sub-groups, others are small inline chains (a floor primitive, a material tag). Common in cabin-style compositions.
- **Per-branch material tagging**: insert `Set Material — GeometryNodeSetMaterial` on each branch *before* Join so each part carries its own material. Doing this *after* Join requires a selection mask.

## Field Drivers

Rarely used at the composition root itself. Field drivers belong inside each branch (scatter density, per-primitive deform). Controls visible at this layer are typically:
- Boolean `Group Input` toggles → `Switch — GeometryNodeSwitch` to include/exclude a branch.
- Integer/float `Group Input` params routed into each sub-group's interface, not consumed at this root.

## Composes With

- [distribution-archetype] — any branch can be a scatter; its output plugs into Join like any other geometry.
- Any primitive or curve-swept structure pattern — they become leaf branches of the assembly.

## When NOT to Use

- Two geometries that must produce a watertight merged surface (overlapping/interpenetrating) → use `Mesh Boolean` (A4), not Join. Join preserves separate meshes; Boolean fuses them into a new surface.
- Switching between *alternatives* based on a toggle → use `Switch` alone, not Join. Join is for keeping multiple parts simultaneously.

## Common Mistakes

- **Joining before setting per-branch material** → if all branches share the same material afterwards, you lose per-part slot assignment.
- **Confusing Join with Boolean** → Join keeps inputs as disjoint islands in one geometry; Boolean computes a new merged surface via CSG. Picking the wrong one produces visually-similar-but-topologically-different results.
- **Building the whole assembly inline** instead of extracting reusable parts as Group nodes → the graph becomes unmaintainable and parts can't be swapped.
- **Realizing too early inside branches** — if a branch produces instances (scatter), keep them as instances through Join; only realize at the very end if downstream truly requires a mesh.
- **Forgetting that Join is multi-input** — adding new branches is free; don't chain pairs of Joins when one Join with N inputs works.
