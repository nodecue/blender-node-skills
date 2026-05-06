---
id: surface-displacement
name: Surface Displacement
description: "Move geometry with Set Position using a verified vector direction and a field-driven magnitude."
category: deformation
tags: displacement, set position, normal, noise, vector
---

## Surface Displacement

**Intent:** Move points on a geometry with `Set Position`. The direction can come from `Normal` or another vector field; the magnitude can come from a constant, noise, proximity, or any verified float field.

## Evidence

- `rules/geometry-operations.md`: `GeometryNodeSetPosition`
- `rules/geometry-read.md`: `GeometryNodeInputNormal`, `GeometryNodeInputPosition`
- `rules/texture.md`: `ShaderNodeTexNoise`
- `rules/utilities-vector.md`: `ShaderNodeVectorMath`
- `rules/utilities-math.md`: `ShaderNodeMapRange`, `ShaderNodeMath`
- `patterns/normal-projection-removal.md`: verified vector projection chain for tangent-only variants
- `evals/gn_pattern_readbacks.json`: Blender 5.1 readback for `surface-displacement`

## Signature

- **In:** `geometry` (GEOMETRY), `direction` (VECTOR field), `magnitude` (FLOAT field or value)
- **Out:** displaced `geometry` (GEOMETRY)
- **Params:** strength, optional mask, optional noise scale/detail

## Data Flow

```
geometry ─[GEOMETRY]──────────────→ Set Position.Geometry ─→ output
direction ─[VECTOR]─→ Vector Math(SCALE) ─[VECTOR]─→ Set Position.Offset
magnitude ─[FLOAT]───────────────────────↑ Scale
```

## Core Chain

1. `Set Position — GeometryNodeSetPosition`
   - `Geometry` ← current geometry path
   - `Offset` ← verified vector offset
2. Direction candidate:
   - `Normal — GeometryNodeInputNormal` for surface-normal displacement.
   - Any other vector field only after readback confirms the output socket exists.
3. Magnitude candidate:
   - `Noise Texture — ShaderNodeTexNoise` `Factor` for organic variation.
   - `Map Range — ShaderNodeMapRange` or `Math — ShaderNodeMath` to remap/clamp magnitude.
4. `Vector Math — ShaderNodeVectorMath` with operation `SCALE`
   - `Vector` ← direction
   - `Scale` ← magnitude
   - `Vector` output → `Set Position.Offset`

## Variants

- **Masked displacement:** boolean field → `Set Position.Selection`.
- **Tangent-only displacement:** use [normal-projection-removal](normal-projection-removal.md) before `Set Position.Offset`.
- **Two-stage displacement:** capture original `Position` or `Normal` before the first displacement if the second stage must reference the original surface.

## Common Mistakes

- Connecting the magnitude field directly to `Set Position.Offset`; `Offset` expects a vector.
- Using `Set Position.Position` when the intended operation is an additive offset.
- Forgetting that a `Normal` read after a displacement may differ from the original normal.
