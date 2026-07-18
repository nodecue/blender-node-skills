---
title: Curve Primitives
section: curve
description: "Curve Nodes (Primitives): Generate curve geometry from parametric primitive sources."
tags: arc, bézier, curve, primitives
blender_support: "5.0+"
blender_verified: 5.1.1, 5.2.0
last_verified: "2026-07-18"
---

## Curve Primitives

Reference nodes for `Curve Primitives`. Total: **8** nodes.

### Arc — `GeometryNodeCurveArc`
- **Notes:** The Arc node generates a poly spline arc. The node has two modes, Radius and Points.
- **Inputs:**
  - `Resolution` (`INT`)
  - `Start` (`VECTOR`)
  - `Middle` (`VECTOR`)
  - `End` (`VECTOR`)
  - `Radius` (`FLOAT`)
  - `Start Angle` (`FLOAT`)
  - `Sweep Angle` (`FLOAT`)
  - `Offset Angle` (`FLOAT`)
  - `Connect Center` (`BOOLEAN`)
  - `Invert Arc` (`BOOLEAN`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
  - `Center` (`VECTOR`)
  - `Normal` (`VECTOR`)
  - `Radius` (`FLOAT`)
- **Warning:** Because of the finite resolution, the middle point does not necessarily lie on the generated arc.

### Bézier Segment — `GeometryNodeCurvePrimitiveBezierSegment`
- **Notes:** The Bézier Segment node generates a 2D Bézier spline from the given control points and handles.
- **Inputs:**
  - `Resolution` (`INT`)
  - `Start` (`VECTOR`)
  - `Start Handle` (`VECTOR`)
  - `End Handle` (`VECTOR`)
  - `End` (`VECTOR`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)

### Curve Circle — `GeometryNodeCurvePrimitiveCircle`
- **Notes:** The Curve Circle node generates a poly spline circle. Note: Because of the finite resolution, the three points do not necessarily lie on the generated curve.
- **Inputs:**
  - `Resolution` (`INT`)
  - `Point 1` (`VECTOR`)
  - `Point 2` (`VECTOR`)
  - `Point 3` (`VECTOR`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
  - `Center` (`VECTOR`)
- **Warning:** Because of the finite resolution, the three points do not necessarily lie on the generated curve.

### Curve Line — `GeometryNodeCurvePrimitiveLine`
- **Notes:** The Curve Line node generates poly spline line.
- **Inputs:**
  - `Start` (`VECTOR`)
  - `End` (`VECTOR`)
  - `Direction` (`VECTOR`)
  - `Length` (`FLOAT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)

### Quadratic Bézier — `GeometryNodeCurveQuadraticBezier`
- **Notes:** The Quadratic Bézier node generates a poly spline curve from the given control points. The generated shape is a parabola.
- **Inputs:**
  - `Resolution` (`INT`)
  - `Start` (`VECTOR`)
  - `Middle` (`VECTOR`)
  - `End` (`VECTOR`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)

### Quadrilateral — `GeometryNodeCurvePrimitiveQuadrilateral`
- **Notes:** The Quadrilateral node generates a polygon with four points, with different modes.
- **Inputs:**
  - `Width` (`FLOAT`)
  - `Height` (`FLOAT`)
  - `Bottom Width` (`FLOAT`)
  - `Top Width` (`FLOAT`)
  - `Offset` (`FLOAT`)
  - `Bottom Height` (`FLOAT`)
  - `Top Height` (`FLOAT`)
  - `Point 1` (`VECTOR`)
  - `Point 2` (`VECTOR`)
  - `Point 3` (`VECTOR`)
  - `Point 4` (`VECTOR`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)

### Spiral — `GeometryNodeCurveSpiral`
- **Notes:** The Spiral node generates a poly spline in a spiral shape. It can be used to create springs or other similar objects. By default the spiral twists in a clockwise fashion.
- **Inputs:**
  - `Resolution` (`INT`)
  - `Rotations` (`FLOAT`)
  - `Start Radius` (`FLOAT`)
  - `End Radius` (`FLOAT`)
  - `Height` (`FLOAT`)
  - `Reverse` (`BOOLEAN`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)

### Star — `GeometryNodeCurveStar`
- **Notes:** The Star node generates a poly spline in a star pattern by connecting alternating points of two circles. The points on the inner circle are offset by a rotation so that they lie in between the points on the outer circle. This offset can be changed with the twist input.
- **Inputs:**
  - `Points` (`INT`)
  - `Inner Radius` (`FLOAT`)
  - `Outer Radius` (`FLOAT`)
  - `Twist` (`FLOAT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
  - `Outer Points` (`BOOLEAN`)

