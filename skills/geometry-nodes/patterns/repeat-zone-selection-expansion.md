---
id: repeat-zone-selection-expansion
name: Repeat Zone Selection Expansion
description: "Use a Repeat Zone with domain hopping to iteratively grow (dilate) a boolean selection by N rings."
category: branching
tags: repeat zone, selection, expand, dilate, domain, evaluate on domain, boolean
blender_support: "5.0+"
blender_verified: 5.1.1
status: stable
---

## Repeat Zone Selection Expansion

**Intent:** Grow a boolean selection outward by N rings of adjacent elements. Each iteration "hops" the boolean across domains (e.g. face→edge→face) using Evaluate on Domain, which spreads the true values to neighboring elements. Wrapping this in a Repeat Zone lets you control how many rings to expand.

## Evidence

- `rules/utilities-field.md`: `GeometryNodeFieldOnDomain`
- `rules/utilities-misc.md`: `GeometryNodeRepeatInput`, `GeometryNodeRepeatOutput`
- `rules/utilities-math.md`: `ShaderNodeMath`
- `rules/geometry-operations.md`: `GeometryNodeSeparateGeometry`, `GeometryNodeDeleteGeometry`

## Signature

- **In:** `geometry` (GEOMETRY), `selection` (BOOLEAN) — initial selection to expand, `loops` (INT) — number of expansion rings
- **Out:** `geometry` (GEOMETRY) — unchanged, `selection` (BOOLEAN) — expanded selection

## Data Flow

```
selection ─→ EvaluateOnDomain(face→point) ─→ RepeatInput(iterations=loops)
geometry ──────────────────────────────────→ RepeatInput
                                                │
                        ┌───────────────────────┘
                        ↓ (per iteration)
                  EvaluateOnDomain(point→edge, value)
                        ↓
                  EvaluateOnDomain(edge→face, value)
                        ↓
                  Math(MAXIMUM) or just pass through
                        ↓
                  RepeatOutput ──→ expanded selection
```

## Core Chain

1. `Evaluate on Domain — GeometryNodeFieldOnDomain` (pre-loop)
   - Convert initial selection to the starting domain (e.g. face boolean evaluated on point domain)
   - Output: boolean field ready for iteration
2. `Repeat Input — GeometryNodeRepeatInput`
   - `Iterations` ← loops count
   - `Geometry` ← input geometry (passed through unchanged)
   - `Value` ← pre-converted selection boolean
3. Per-iteration body:
   - `Evaluate on Domain — GeometryNodeFieldOnDomain` (point→edge)
     - Takes the current boolean, evaluates it on the edge domain — any edge touching a selected point becomes true
   - `Evaluate on Domain — GeometryNodeFieldOnDomain` (edge→face)
     - Takes the edge boolean, evaluates it on the face domain — any face touching a selected edge becomes true
   - `Math — ShaderNodeMath` (operation: MAXIMUM or ADD with clamp)
     - Combines the spread boolean to ensure it stays in 0–1 range
4. `Repeat Output — GeometryNodeRepeatOutput`
   - `Geometry` ← passthrough
   - `Value` ← expanded boolean, fed back for next iteration

## Key Properties

- The domain hop sequence determines expansion behavior: face→edge→face expands face selections, point→edge→point expands vertex selections
- Each iteration expands by one ring of adjacency
- Geometry passes through unchanged — only the boolean field is modified
- The Math node ensures the boolean stays valid after domain interpolation (Evaluate on Domain averages booleans, so values may not be exactly 0 or 1)

## Variants

- **Shrink/erode selection:** invert the boolean before expanding, then invert back — or use NOT + expand + NOT
- **Smooth selection boundary:** use fewer iterations with Blur Attribute after expansion for soft falloff
- **Weighted expansion:** replace the boolean with a float weight and use Blur Attribute inside the loop instead of domain hopping

## Composes With

- [repeat-zone-iterative-smoothing](repeat-zone-iterative-smoothing.md) — similar Repeat Zone structure for iterative algorithms.
- [material-attribute-handoff](material-attribute-handoff.md) — store or assign the expanded selection after verification.

## Common Mistakes

- Wrong domain hop sequence for the selection type (face selection needs face→edge→face, not point→edge→point)
- Forgetting the Math node to re-booleanize — Evaluate on Domain averages booleans across neighbors, producing fractional values
- Not passing geometry through the Repeat Zone (geometry is needed for domain evaluation context even if it doesn't change)
