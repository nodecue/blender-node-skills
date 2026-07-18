---
id: distribution-archetype
name: 分布术 (Distribution Archetype)
description: "Scatter instances on a surface, along a curve, or at mesh vertices — the canonical point-generator → Instance on Points pipeline."
category: instancing
tags: 分布术, scatter, instance, distribute, 散布, 实例
blender_support: "5.0+"
blender_verified: 5.1.1
status: stable
---

## 分布术 (Distribution Archetype)

**Intent:** Place many copies of a source object across a target geometry. The target becomes a *point carrier* (surface, curve, or vertex set); the source is *instanced* on those points. Randomization (scale, rotation, density) attaches as field drivers to the `Instance on Points` node's per-instance sockets.

Recognize this archetype from prompts like: "在地形上分布石头", "沿曲线放置路灯", "草地上长草", "每个顶点放一个实例".

## Evidence

- `rules/point.md`: `GeometryNodeDistributePointsOnFaces`, `GeometryNodeDistributePointsInVolume`
- `rules/curve-operations.md`: `GeometryNodeCurveToPoints`
- `rules/mesh-operations.md`: `GeometryNodeMeshToPoints`
- `rules/instances.md`: `GeometryNodeInstanceOnPoints`, `GeometryNodeRealizeInstances`
- `rules/utilities-misc.md`: `FunctionNodeRandomValue`, `FunctionNodeAlignEulerToVector`

## Signature

- **In:** `target` (GEOMETRY — surface/curve/mesh), `instance_source` (GEOMETRY or collection) — what gets placed
- **Out:** `geometry` (GEOMETRY) — instances (or realized mesh if `Realize Instances` is added)
- **Params:** density, seed, per-instance scale range, per-instance rotation, optional density mask

## Data Flow

```
target ─[GEOMETRY]──→ Point Generator ─[points]──→ Instance on Points ─[instances]─→ output
                                                         ↑
instance_source (or Collection Info) ────────────────────┤ Instance
random scale / rotation / pick index ────────────────────┘
```

## Core Chain

1. **Point generator** — pick ONE based on target type:
   - Surface → `Distribute Points on Faces — GeometryNodeDistributePointsOnFaces`
   - Curve → `Curve to Points — GeometryNodeCurveToPoints`
   - Existing vertices → `Mesh to Points — GeometryNodeMeshToPoints`
   - Volume → `Distribute Points in Volume — GeometryNodeDistributePointsInVolume`
2. `Instance on Points — GeometryNodeInstanceOnPoints`
   - `Points` ← point generator's `Points` output
   - `Instance` ← instance source geometry (see Instance Source variants)
3. Optional: `Realize Instances — GeometryNodeRealizeInstances` before output if downstream needs real mesh (e.g. further booleans, export). Skip if instances should stay instances.

## Instance Source Variants

- **Single object** — wire source mesh (e.g. `Mesh Cube`, `Object Info`) directly into `Instance`.
- **Random from collection** — `Collection Info — GeometryNodeCollectionInfo` with `Separate Children = True` → `Instance` input; `Instance Index` socket takes `Random Value (INT)` to pick per point.
- **Nested instances** (instances of instances) — source is itself an instancer group. Leave unrealized so the outer scatter keeps them cheap.

## Field Drivers

- **Density mask**: boolean field (`Position` -> `Compare`, `Named Attribute` -> `Compare`, or `Geometry Proximity` distance -> `Compare`) -> `Distribute Points on Faces.Selection`. Or a float field -> `Density Factor` for smooth falloff.
- **Per-instance scale variation**: `Random Value (VECTOR)` → `Scale` input of `Instance on Points`. Seed per-instance via the distribute node's `id` output.
- **Align to surface normal** (A1 + M3): `Distribute Points on Faces` outputs `Normal` → `Align Euler to Vector — FunctionNodeAlignEulerToVector` with axis Z → `Rotation` input of `Instance on Points`. Without this, instances point up instead of hugging the surface.
- **Curve-tangent alignment**: `Curve to Points` outputs `Tangent` and `Normal`; use the rotation alignment node available in the current Blender rule set before wiring the `Rotation` input.

## Composes With

- [capture-then-propagate] — capture per-point attributes (id, random value) before Instance on Points if you need them downstream.
- [stitching-archetype] — a scatter output is often one branch feeding a Join at the composition root.

## Common Mistakes

- Forgetting rotation alignment → instances all stand straight up regardless of surface orientation.
- Realizing instances too early → loses per-instance data, balloons memory, breaks later per-instance edits.
- Wiring Collection Info without `Separate Children` → get one merged lump instead of per-child pick.
- Using `Mesh to Points` for surface scatter with `Count > vertex count` → oversampling-impossible; switch to `Distribute Points on Faces`.
- Connecting density mask to `Density` float socket when it's actually boolean selection → use `Selection` input for pass/fail masks, `Density Factor` for float weights.
