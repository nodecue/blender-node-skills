---
title: Input Gizmo
section: input
description: "Input Nodes (Gizmo): Interactive viewport gizmo-driven inputs for tool and group control."
tags: dial, gizmo, input, linear, transform
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Input Gizmo

Reference nodes for `Input Gizmo`. Total: **3** nodes.

### Dial Gizmo — `GeometryNodeGizmoDial`
- **Notes:** The Dial Gizmo node is ideal for creating gizmos that control angles.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Position` (`VECTOR`)
  - `Up` (`VECTOR`)
  - `Screen Space` (`BOOLEAN`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Transform` (`GEOMETRY`)

### Linear Gizmo — `GeometryNodeGizmoLinear`
- **Notes:** The Linear Gizmo node provides the most widely applicable gizmo. It can e.g. be used to control the height of something.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Position` (`VECTOR`)
  - `Direction` (`VECTOR`)
- **Outputs:**
  - `Transform` (`GEOMETRY`)

### Transform Gizmo — `GeometryNodeGizmoTransform`
- **Notes:** The Transform Gizmo node provides a compound gizmo that can control a position, rotation and scale.
- **Inputs:**
  - `Value` (`MATRIX`)
  - `Position` (`VECTOR`)
  - `Rotation` (`ROTATION`)
- **Outputs:**
  - `Transform` (`GEOMETRY`)
- **Tip:** The rotation input is ignored by the 3D viewport if the transform orientation is set to global.

