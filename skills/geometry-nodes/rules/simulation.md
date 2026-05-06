---
title: Simulation Zones
section: system
description: "Simulation zone boundary nodes and frame-to-frame state flow."
tags: geometry, simulation, system, zone
---

## Simulation Zones

Reference nodes for `Simulation Zones`. Total: **2** nodes.

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
