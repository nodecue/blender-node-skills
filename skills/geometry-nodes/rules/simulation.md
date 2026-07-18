---
title: Simulation Zones
section: system
description: "Simulation zone boundary nodes and frame-to-frame state flow."
tags: geometry, simulation, system, zone
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Simulation Zones

Reference nodes for `Simulation Zones`. Total: **3** nodes.

### Simulation Input — `GeometryNodeSimulationInput`
- **Notes:** Simulation zones allow frame-to-frame feedback. Headless extraction exposes no inputs and a `Delta Time` output.
- **Inputs:** None
- **Outputs:**
  - `Delta Time` (`FLOAT`)


### Simulation Output — `GeometryNodeSimulationOutput`
- **Notes:** Simulation zone output boundary. Headless extraction exposes `Skip`, `Geometry`, and zone-typed `CUSTOM` passthrough sockets.
- **Inputs:**
  - `Skip` (`BOOLEAN`)
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)


### XPBD Solver — `GeometryNodeXPBDSolver`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Physics release notes; Blender 5.2.0 live readback (experimental).
- **Notes:** XPBD physics solver node. Marked experimental in Blender 5.2 - do not use as a stable default path.
- **Inputs:**
  - `World` (`BUNDLE`)
  - `Delta Time` (`FLOAT`)
  - `Filter` (`STRING`)
  - `Simulation to World` (`MATRIX`)
  - `Substeps` (`INT`)
  - `Constraint Iterations` (`INT`)
  - `Solver Path` (`STRING`)
  - `Begin` (`FLOAT`)
  - `End` (`FLOAT`)
- **Outputs:**
  - `World` (`BUNDLE`)
