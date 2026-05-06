---
title: Generate
section: generate
description: "Generate Nodes: Procedural generators that create or duplicate geometry components."
tags: duplicate, generate
---

## Generate

Reference nodes for `Generate`. Total: **1** nodes.

### Duplicate Elements — `GeometryNodeDuplicateElements`
- **Notes:** The Duplicate Elements node creates a new geometry with the specified elements from the input duplicated an arbitrary number of times. The positions of elements are not changed, so all of the duplicates will be at the exact same location.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Amount` (`INT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
  - `Duplicate Index` (`INT`)
- **Example:** Combined with the Geometry to Instance Node, this can be used to create a basic efficient “Array” operation. Used with: Geometry to Instance, instances.

