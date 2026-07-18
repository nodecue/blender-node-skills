---
id: index-normalized-shaping
name: Index-Normalized Shaping
description: "Shape per-element values along a sequence using Float Curve and Map Range for non-linear control."
category: utility
tags: index, float curve, map range, shaping, scale, gradual, layers
blender_support: "5.0+"
blender_verified: 5.1.1
status: stable
---

## Index-Normalized Shaping

**Intent:** Given sequential elements (layers, segments, points along a line), produce a shaped per-element value that varies non-linearly along the sequence. Typical use: tree branches that get progressively smaller and shorter toward the top, with artist-controllable falloff via Float Curve.

## Evidence

- `rules/geometry-read.md`: `GeometryNodeInputIndex`
- `rules/utilities-math.md`: `ShaderNodeMath`, `ShaderNodeFloatCurve`, `ShaderNodeMapRange`
- `rules/utilities-vector.md`: `ShaderNodeCombineXYZ`
- `rules/instances.md`: `GeometryNodeInstanceOnPoints`
- `rules/curve-operations.md`: `GeometryNodeSetCurveRadius`

## Signature

- **In:** `index` (INT), `total` (INT) — element index and total count
- **Out:** one or more shaped values (FLOAT or VECTOR) — per-element parameters
- **Params:** Float Curve shape (artist-tunable), Map Range min/max per output axis

## Data Flow

```
Index ─[INT]─→ Math(DIVIDE) ─[FLOAT]─→ Float Curve ─[FLOAT]─→ Reroute (normalized shaped signal)
                   ↑                                               ├─→ Map Range   ─→ Combine XYZ.X/.Y
            total ─┘                                               └─→ Map Range.N ─→ Combine XYZ.Z
                                                                                          ↓
                                                                                    [VECTOR] out
```

## Core Chain

1. `Index — GeometryNodeInputIndex`
2. `Math — ShaderNodeMath` (operation: DIVIDE)
   - `Value` ← Index
   - `Value` ← total count
   - Output: normalized 0..1
3. `Float Curve — ShaderNodeFloatCurve`
   - `Value` ← step 2 output
   - Output: shaped 0..1 (artist draws the falloff curve)
4. `Map Range — ShaderNodeMapRange` (one per independent axis/parameter)
   - `Value` ← Float Curve output
   - `From Min/Max` ← 0..1
   - `To Min/Max` ← target range for this axis
   - Output: remapped value
5. `Combine XYZ — ShaderNodeCombineXYZ` (if multiple axes)
   - Assemble per-axis values into a vector

## Key Properties

- Math operation: DIVIDE
- Map Range count depends on how many independent parameters need different ranges:
  - 1 Map Range: uniform scaling or single parameter
  - 2 Map Ranges: XY shared + Z separate (as in tree layers)
  - 3 Map Ranges: fully independent per-axis control
- Float Curve shape is the primary artist control — linear = even falloff, concave = fast start, convex = slow start

## Downstream Usage

- → `Instance on Points.Scale` for progressive instance scaling
- → `Set Curve Radius.Radius` for tapered tubes
- → any socket that needs per-element variation along a sequence

## Composes With

- Upstream: `Mesh Line`, `Resample Curve`, or any geometry where ordered indices are acceptable.
- Downstream: [density-controlled-scatter](density-controlled-scatter.md) or [distribution-archetype](distribution-archetype.md) when index-shaped values drive instance scale.

## Common Mistakes

- Float Curve input not in 0..1 range (clipped or flat output)
- Map Range From Min/Max not matching Float Curve output range
- Using same Map Range for axes that need different scaling (tree XY vs Z)
