---
title: Utilities Vector
section: utilities
description: "Utilities (Vector): Vector math and vector component composition/separation."
tags: combine, radial, separate, utilities, vector
last_verified: "2026-07-29"
---

## Utilities Vector

Reference nodes for `Utilities Vector`. Total: **6** nodes.

### Combine XYZ — `ShaderNodeCombineXYZ`
- **Notes:** Create a vector from X, Y, and Z components.
- **Inputs:**
  - `X` (`FLOAT`)
  - `Y` (`FLOAT`)
  - `Z` (`FLOAT`)
- **Outputs:**
  - `Vector` (`VECTOR`)
- **Tip:** The vector is not normalized.

### Radial Tiling — `ShaderNodeRadialTiling`
- **Version:** Blender `5.0+`; not in 4.5.
- **Evidence:** Absent from the Blender 4.5 manual (`docs/blender-manual-gn-4.5/`); documented from 5.0 in `docs/blender-manual-gn-5.0/utilities/vector/radial_tiling.md`.
- **Notes:** Transform Coordinate System for Radial Tiling.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Sides` (`FLOAT`)
  - `Roundness` (`FLOAT`)
- **Outputs:**
  - `Segment Coordinates` (`VECTOR`)
  - `Segment ID` (`FLOAT`)
  - `Segment Width` (`FLOAT`)
  - `Segment Rotation` (`FLOAT`)
- **Example:** The coordinates provided by the Segment Coordinates output can be used to tile textures in a radially symmetric manner, which is demonstrated by radially tiling a heart texture in the following examples.

### Separate XYZ — `ShaderNodeSeparateXYZ`
- **Notes:** Split a vector into its X, Y, and Z components.
- **Inputs:**
  - `Vector` (`VECTOR`)
- **Outputs:**
  - `X` (`FLOAT`)
  - `Y` (`FLOAT`)
  - `Z` (`FLOAT`)

### Vector Curves — `ShaderNodeVectorCurve`
- **Compatibility:** The factor input is visibly named `Fac` in Blender 4.5 and `Factor` in Blender 5.2; its identifier remains `Fac`.
- **Notes:** Map input vector components with curves.
- **Inputs:**
  - `Factor` (`FLOAT`)
  - `Vector` (`VECTOR`)
- **Outputs:**
  - `Vector` (`VECTOR`)

### Vector Math — `ShaderNodeVectorMath`
- **Notes:** Perform vector math operation.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Vector` (`VECTOR`)
  - `Vector` (`VECTOR`)
  - `Scale` (`FLOAT`)
- **Outputs:**
  - `Vector` (`VECTOR`)
  - `Value` (`FLOAT`)
- **Properties:**
  - `operation` (ADD, SUBTRACT, MULTIPLY, DIVIDE, MULTIPLY_ADD, CROSS_PRODUCT, PROJECT, REFLECT, REFRACT, FACEFORWARD, DOT_PRODUCT, DISTANCE, LENGTH, SCALE, NORMALIZE, ABSOLUTE, POWER, SIGN, MINIMUM, MAXIMUM, FLOOR, CEIL, FRACTION, MODULO, WRAP, SNAP, SINE, COSINE, TANGENT) — MULTIPLY: Entry-wise multiply; DIVIDE: Entry-wise divide; MULTIPLY_ADD: A * B + C

### Vector Rotate — `ShaderNodeVectorRotate`
- **Notes:** Rotate a vector around a pivot point (center).
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Center` (`VECTOR`)
  - `Axis` (`VECTOR`)
  - `Angle` (`FLOAT`)
  - `Rotation` (`VECTOR`)
- **Outputs:**
  - `Vector` (`VECTOR`)
- **Example:** Vector Rotate node example.
