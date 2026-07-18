---
id: repeat-zone-iterative-smoothing
name: Repeat Zone Iterative Smoothing
description: "Use a Repeat Zone to iteratively refine geometry (smoothing, relaxation, simulation steps)."
category: deformation
tags: repeat zone, iteration, smoothing, relaxation, blur, simulation
blender_support: "5.0+"
blender_verified: 5.1.1
status: stable
---

## Repeat Zone Iterative Smoothing

**Intent:** Many algorithms require multiple passes to converge: mesh smoothing, Laplacian relaxation, diffusion effects, iterative simulation steps. A Repeat Zone runs a sub-graph N times, passing geometry through each iteration.

## Evidence

- `rules/utilities-misc.md`: `GeometryNodeRepeatInput`, `GeometryNodeRepeatOutput`
- `rules/attribute.md`: `GeometryNodeBlurAttribute`, `GeometryNodeCaptureAttribute`
- `rules/geometry-operations.md`: `GeometryNodeSetPosition`
- `rules/utilities-vector.md`: `ShaderNodeVectorMath`
- `rules/utilities-math.md`: `ShaderNodeMath`
- `patterns/normal-projection-removal.md`: tangent-preserving vector correction

## Signature

- **In:** `geometry` (GEOMETRY) — geometry to refine
- **Out:** `smoothed` (GEOMETRY) — refined geometry after N iterations
- **Params:** `iterations` (INT) — number of passes, `weight` (FLOAT) — per-iteration blend factor

## Data Flow

```
geometry ─[GEOMETRY]─→ Repeat Input(iterations=N) ─→ [per-iteration body] ─→ Repeat Output ─→ smoothed
                                                          │
                                                    Blur Attribute or
                                                    manual averaging →
                                                    Mix(weight) →
                                                    Set Position
```

## Core Chain

1. `Repeat Input — GeometryNodeRepeatInput`
   - `Iterations` ← iteration count
   - `Geometry` ← input geometry (passed through each iteration)
2. Per-iteration body (two approaches):
   - **Simple:** `Blur Attribute — GeometryNodeBlurAttribute` on Position, with weight mask to exclude pinned vertices
   - **Manual:** neighbor position averaging via Edges of Vertex + Evaluate at Index, then Mix between current and averaged position
3. `Set Position — GeometryNodeSetPosition`
   - `Geometry` ← current iteration geometry
   - `Position` ← blended result (Mix between original position and smoothed position, controlled by weight)
4. `Repeat Output — GeometryNodeRepeatOutput`
   - `Geometry` ← Set Position output → feeds back into next iteration

## Key Properties

- `weight` controls how aggressively each iteration moves vertices (0 = no change, 1 = full snap to smoothed position). Lower values (0.1–0.5) give more stable convergence.
- Pinned/immovable vertices: use a boolean mask to set weight to 0 for vertices that should not move

## Variants

- **With normal projection:** add [normal-projection-removal] inside the loop to keep smoothing tangent to the surface
- **With capture:** use [capture-then-propagate] before the loop to preserve original positions for blending
- **Multi-attribute:** pass additional attributes through the Repeat Zone items to smooth multiple fields simultaneously

## Composes With

- [normal-projection-removal] inside the loop body for surface-preserving smoothing
- [capture-then-propagate] before the loop to freeze reference values
- [material-attribute-handoff](material-attribute-handoff.md) when a stored numeric mask controls the smoothing weight

## Common Mistakes

- Too many iterations without weight damping — geometry collapses or oscillates
- Forgetting to pass geometry through Repeat Output (loop body disconnected, geometry unchanged)
- Not realizing that fields are re-evaluated each iteration — Position inside the loop reflects the updated positions from the previous iteration (this is usually desired)
