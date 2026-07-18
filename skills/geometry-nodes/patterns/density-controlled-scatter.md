---
id: density-controlled-scatter
name: Density Controlled Scatter
description: "Control surface scattering with boolean selection or float density fields before instancing."
category: instancing
tags: scatter, density, selection, instance, random
blender_support: "5.0+"
blender_verified: 5.1.1
status: stable
---

## Density Controlled Scatter

**Intent:** Place instances on a surface while controlling where and how densely points are generated. This is a specialization of [distribution-archetype](distribution-archetype.md), not a separate scatter architecture.

## Evidence

- `patterns/distribution-archetype.md`: point generator -> `GeometryNodeInstanceOnPoints`
- `rules/point.md`: `GeometryNodeDistributePointsOnFaces` with `Selection`, `Density`, `Density Factor`, and `Seed`
- `rules/instances.md`: `GeometryNodeInstanceOnPoints`, `GeometryNodeRealizeInstances`
- `rules/utilities-misc.md`: `FunctionNodeRandomValue`
- `rules/utilities-math.md`: `FunctionNodeCompare`, `ShaderNodeMapRange`
- `rules/texture.md`: `ShaderNodeTexNoise`, `ShaderNodeTexVoronoi`
- Blender 5.1 readback captured in the NodeCue dev repo (`tests/golden/skill_evals/gn_pattern_readbacks.json`) for `density-controlled-scatter`

## Signature

- **In:** surface `mesh` (GEOMETRY), `instance_source` (GEOMETRY)
- **Out:** scattered instances or realized geometry
- **Params:** density, seed, optional mask threshold, optional scale range

## Data Flow

```
mesh ─[GEOMETRY]─→ Distribute Points on Faces ─[points]─→ Instance on Points ─[instances]─→ output
mask ─[BOOLEAN]──────────────────────↑ Selection
density_field ─[FLOAT]───────────────↑ Density Factor
instance_source ─[GEOMETRY]────────────────────────────────↑ Instance
```

## Core Chain

1. `Distribute Points on Faces — GeometryNodeDistributePointsOnFaces`
   - `Mesh` ← target surface
   - `Selection` ← hard boolean mask, if available
   - `Density Factor` ← soft float density field, if available
   - `Seed` ← explicit seed only if the user asks for it
2. Density field candidates:
   - `Noise Texture — ShaderNodeTexNoise` or `Voronoi Texture — ShaderNodeTexVoronoi` `Factor` for procedural variation.
   - `Compare — FunctionNodeCompare` when a hard boolean selection is needed.
   - `Map Range — ShaderNodeMapRange` when the float field needs remapping before `Density Factor`.
3. `Instance on Points — GeometryNodeInstanceOnPoints`
   - `Points` ← distribute node `Points`
   - `Instance` ← source geometry
   - Optional `Scale` ← `Random Value — FunctionNodeRandomValue`
4. Optional `Realize Instances — GeometryNodeRealizeInstances` only when downstream needs real geometry.

## Common Mistakes

- Putting a boolean mask into `Density Factor` when the intent is strict inclusion/exclusion.
- Using `Mesh to Points` when the user asked for arbitrary surface density; it can only use existing mesh points.
- Realizing instances before scale/rotation/pick-index decisions are finished.
