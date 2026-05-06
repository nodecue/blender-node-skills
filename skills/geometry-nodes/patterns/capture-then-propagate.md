---
id: capture-then-propagate
name: Capture Then Propagate
description: "Freeze a field value into geometry with Capture Attribute so it survives downstream geometry changes."
category: utility
tags: capture attribute, anonymous attribute, field, preserve, freeze
---

## Capture Then Propagate

**Intent:** A field is re-evaluated every time a data flow node consumes it. If geometry changes between two consumers (e.g. two Set Position nodes), the same field produces different results. Capture Attribute freezes the field result at a specific point in the graph, storing it as an anonymous attribute that persists through geometry changes.

## Evidence

- `rules/attribute.md`: `GeometryNodeCaptureAttribute`
- `rules/geometry-operations.md`: `GeometryNodeSetPosition`
- `rules/geometry-read.md`: `GeometryNodeInputPosition`, `GeometryNodeInputNormal`

## Signature

- **In:** `geometry` (GEOMETRY), `field` (any type) — the field to freeze
- **Out:** `geometry` (GEOMETRY) — with captured attribute attached, `captured_value` (same type) — the frozen field output
- **Params:** `domain` — which domain to evaluate the field on

## Data Flow

```
geometry ─[GEOMETRY]─→ Capture Attribute ─[GEOMETRY]─→ (downstream ops that change geometry)
field ──────────────────────↑       │
                                    └─[captured_value]──→ (use later, value unchanged)
```

## Core Chain

1. `Capture Attribute — GeometryNodeCaptureAttribute`
   - `Geometry` ← current geometry state
   - `Value` ← the field to freeze (e.g. Position, Normal, a computed value)
   - Set `domain` to match the field's intended evaluation domain
   - Output `Geometry`: geometry now carries the captured data as an anonymous attribute
   - Output `Value`: the captured field, usable downstream regardless of geometry changes

## When to Use

- **Before chained Set Position:** capture original Position before first displacement, use captured value in second displacement
- **Before topology changes:** capture a field before Subdivide, Extrude, or any operation that changes element count
- **Before representation conversion:** capture attributes before Mesh to Curve or similar, since some attributes are lost
- **Before Duplicate Elements:** capture original indices or values that will be duplicated

## When NOT to Use

- If the field is only consumed once — Capture Attribute adds overhead for no benefit
- If the field is a constant (single value, not varying per element) — it won't change regardless

## Composes With

- [surface-displacement](surface-displacement.md) — capture original position or normal before chained displacement.
- [repeat-zone-iterative-smoothing](repeat-zone-iterative-smoothing.md) — freeze reference values before an iterative loop.

## Common Mistakes

- Placing Capture Attribute too late (after the geometry has already changed)
- Forgetting to use the Geometry output (using the original geometry instead, which doesn't carry the captured data)
- Capturing on the wrong domain (capturing on Point domain but needing per-Face values)
