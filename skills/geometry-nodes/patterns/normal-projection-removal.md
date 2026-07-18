---
id: normal-projection-removal
name: Normal Projection Removal
description: "Remove the normal component from a displacement vector, keeping only the tangent-to-surface part."
category: deformation
tags: normal, tangent, projection, displacement, vector math, surface
blender_support: "5.0+"
blender_verified: 5.1.1
status: stable
---

## Normal Projection Removal

**Intent:** When displacing vertices, sometimes you want movement only along the surface (tangential), not poking through it (normal direction). This pattern subtracts the normal component from a displacement vector, projecting it onto the surface tangent plane.

## Evidence

- `rules/geometry-read.md`: `GeometryNodeInputNormal`
- `rules/utilities-vector.md`: `ShaderNodeVectorMath` operations `DOT_PRODUCT`, `SCALE`, `SUBTRACT`
- `rules/geometry-operations.md`: `GeometryNodeSetPosition`

## Signature

- **In:** `displacement` (VECTOR) — the raw displacement vector, `normal` (VECTOR) — surface normal at the element
- **Out:** `tangent_displacement` (VECTOR) — displacement with normal component removed

## Data Flow

```
displacement ─[VECTOR]─→ Vector Math(DOT_PRODUCT) ─[FLOAT]─→ (scale factor)
normal ──────────────────────↑                                       │
                                                                     ↓
normal ─[VECTOR]─→ Vector Math(SCALE, by dot product) ─[VECTOR]─→ normal_component
                                                                     │
displacement ─[VECTOR]─→ Vector Math(SUBTRACT, normal_component) ─→ tangent_displacement
```

## Core Chain

1. `Vector Math — ShaderNodeVectorMath` (operation: DOT_PRODUCT)
   - `Vector` ← displacement
   - `Vector` ← Normal (from `GeometryNodeInputNormal`)
   - Output: `Value` (FLOAT) — how much of displacement is along the normal
2. `Vector Math — ShaderNodeVectorMath` (operation: SCALE)
   - `Vector` ← Normal
   - `Scale` ← dot product result from step 1
   - Output: `Vector` — the normal component of displacement
3. `Vector Math — ShaderNodeVectorMath` (operation: SUBTRACT)
   - `Vector` ← original displacement
   - `Vector` ← normal component from step 2
   - Output: `Vector` — tangent displacement (normal component removed)

## Math Behind It

This is vector projection: `tangent = v - (v · n) * n` where `v` is displacement and `n` is the unit normal. The dot product gives the scalar projection, scaling the normal by it gives the normal component, and subtracting yields the tangent component.

## Downstream Usage

- → Set Position `Offset` or `Position` input for surface-preserving deformation
- → Mix node to blend between full displacement and tangent-only displacement

## Composes With

- Used inside [repeat-zone-iterative-smoothing] to keep mesh relaxation tangent to the surface
- Upstream: any displacement source (Noise Texture, computed offset, neighbor averaging)
- Downstream: Set Position for applying the projected displacement

## Common Mistakes

- Normal not normalized — if Normal has non-unit length, the projection is incorrect (built-in Normal node is already normalized)
- Applying to instances instead of mesh — instances don't have per-vertex normals
- Forgetting that Normal changes after Set Position — if chaining multiple displacements, re-read Normal or use Capture Attribute
