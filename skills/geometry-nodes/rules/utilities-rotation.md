---
title: Utilities Rotation
section: utilities
description: "Utilities (Rotation): Rotation conversion, alignment, and rotation-space operations."
tags: align, axes, axis, euler, rotation, utilities
blender_support: "5.0+"
blender_verified: 5.1.1, 5.2.0
last_verified: "2026-07-18"
---

## Utilities Rotation

Reference nodes for `Utilities Rotation`. Total: **11** nodes.

### Align Rotation to Vector — `FunctionNodeAlignRotationToVector`
- **Notes:** The Align Rotation to Vector node rotates an Euler rotation into the given direction.
- **Inputs:**
  - `Rotation` (`ROTATION`)
  - `Factor` (`FLOAT`)
  - `Vector` (`VECTOR`)
- **Outputs:**
  - `Rotation` (`ROTATION`)

### Axes to Rotation — `FunctionNodeAxesToRotation`
- **Notes:** Creates a rotation based on two axis directions. Tip: In many cases, these directions are a normal and tangent on a mesh or curve.
- **Inputs:**
  - `Primary Axis` (`VECTOR`)
  - `Secondary Axis` (`VECTOR`)
- **Outputs:**
  - `Rotation` (`ROTATION`)
- **Tip:** In many cases, these directions are a normal and tangent on a mesh or curve.

### Axis Angle to Rotation — `FunctionNodeAxisAngleToRotation`
- **Notes:** The Axis Angle to Rotation node converts a axis angle rotation to a standard rotation value.
- **Inputs:**
  - `Axis` (`VECTOR`)
  - `Angle` (`FLOAT`)
- **Outputs:**
  - `Rotation` (`ROTATION`)

### Euler to Rotation — `FunctionNodeEulerToRotation`
- **Notes:** The Euler to Rotation node creates a rotation value from an Euler rotation.
- **Inputs:**
  - `Euler` (`VECTOR`)
- **Outputs:**
  - `Rotation` (`ROTATION`)

### Invert Rotation — `FunctionNodeInvertRotation`
- **Notes:** The Invert Rotation node inverts a rotation.
- **Inputs:**
  - `Rotation` (`ROTATION`)
- **Outputs:**
  - `Rotation` (`ROTATION`)

### Quaternion to Rotation — `FunctionNodeQuaternionToRotation`
- **Notes:** The Quaternion to Rotation node converts a quaternion rotation to a standard rotation.
- **Inputs:**
  - `W` (`FLOAT`)
  - `X` (`FLOAT`)
  - `Y` (`FLOAT`)
  - `Z` (`FLOAT`)
- **Outputs:**
  - `Rotation` (`ROTATION`)

### Rotate Rotation — `FunctionNodeRotateRotation`
- **Notes:** The Rotate Rotation node applies an additional rotation to a given one. To rotate an Euler Rotation , first use the Euler to Rotation Node .
- **Inputs:**
  - `Rotation` (`ROTATION`)
  - `Rotate By` (`ROTATION`)
- **Outputs:**
  - `Rotation` (`ROTATION`)

### Rotate Vector — `FunctionNodeRotateVector`
- **Notes:** The Rotate Vector node rotates a vector by a given rotation value.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Rotation` (`ROTATION`)
- **Outputs:**
  - `Vector` (`VECTOR`)

### Rotation to Euler — `FunctionNodeRotationToEuler`
- **Notes:** The Rotation to Euler node converts a standard rotation socket value to an Euler rotation.
- **Inputs:**
  - `Rotation` (`ROTATION`)
- **Outputs:**
  - `Euler` (`VECTOR`)

### Rotation to Axis Angle — `FunctionNodeRotationToAxisAngle`
- **Notes:** Convert a rotation to axis angle components.
- **Inputs:**
  - `Rotation` (`ROTATION`)
- **Outputs:**
  - `Axis` (`VECTOR`)
  - `Angle` (`FLOAT`)

### Rotation to Quaternion — `FunctionNodeRotationToQuaternion`
- **Notes:** The Rotation to Quaternion node converts a standard rotation value to a quaternion rotation .
- **Inputs:**
  - `Rotation` (`ROTATION`)
- **Outputs:**
  - `W` (`FLOAT`)
  - `X` (`FLOAT`)
  - `Y` (`FLOAT`)
  - `Z` (`FLOAT`)

