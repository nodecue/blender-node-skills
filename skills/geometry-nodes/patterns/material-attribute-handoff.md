---
id: material-attribute-handoff
name: Material Attribute Handoff
description: "Pass material decisions or numeric masks through geometry with material index, material assignment, or named attributes."
category: utility
tags: material, attribute, mask, handoff, selection
blender_support: "5.0+"
blender_verified: 5.1
status: stable
---

## Material Attribute Handoff

**Intent:** Preserve a material decision or numeric mask so later nodes, materials, or explanation steps can identify which parts of geometry were affected.

## Evidence

- `rules/geometry-read.md`: `GeometryNodeInputMaterialIndex`, `GeometryNodeSetMaterial`, `GeometryNodeSetMaterialIndex`, `GeometryNodeInputNamedAttribute`
- `rules/attribute.md`: `GeometryNodeCaptureAttribute`, `GeometryNodeStoreNamedAttribute`
- `rules/color.md`: `ShaderNodeValToRGB` for color mapping from a factor
- `rules/utilities-math.md`: `FunctionNodeCompare`, `ShaderNodeMapRange`
- Blender 5.1 readback captured in the NodeCue dev repo (`tests/golden/skill_evals/gn_pattern_readbacks.json`) for `material-attribute-handoff`

## Signature

- **In:** `geometry` (GEOMETRY), `selection_or_mask` (BOOLEAN/FLOAT field)
- **Out:** geometry with material assignment, material index, or stored named attribute
- **Params:** material, material index, attribute name

## Data Flow

```
geometry ─[GEOMETRY]─→ Set Material / Set Material Index / Store Named Attribute ─→ output
mask ─[BOOLEAN/FLOAT]──────────────────────────────↑ Selection or Value
```

## Core Chain

1. Choose one handoff target:
   - `Set Material — GeometryNodeSetMaterial` when assigning an actual material to selected geometry.
   - `Set Material Index — GeometryNodeSetMaterialIndex` when selecting by material slot/index.
   - `Store Named Attribute — GeometryNodeStoreNamedAttribute` when storing a numeric mask or value for later readback.
2. If the mask is numeric and the target needs a boolean `Selection`, convert with `Compare — FunctionNodeCompare`.
3. If a numeric field needs display mapping, use `Color Ramp — ShaderNodeValToRGB` only as a verified color-mapping helper; do not assume it stores color data on geometry.
4. Read later with:
   - `Material Index — GeometryNodeInputMaterialIndex` for material indices.
   - `Named Attribute — GeometryNodeInputNamedAttribute` for named stored values; check `Exists`.

## Common Mistakes

- Setting material after `Join Geometry` when each branch needed a different material before joining.
- Assuming `Color Ramp` writes color attributes; it only maps a factor to color output.
- Reading a named attribute from a geometry path that did not pass through `Store Named Attribute`.
