---
title: Utilities Matrix
section: utilities
description: "Utilities (Matrix): Matrix and transform composition/decomposition utilities."
tags: combine, invert, matrix, multiply, utilities
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Utilities Matrix

Reference nodes for `Utilities Matrix`. Total: **12** nodes.

### Combine Matrix — `FunctionNodeCombineMatrix`
- **Notes:** The Combine Matrix node constructs a 4x4 matrix from its individual values.
- **Inputs:**
  - `Column 1 Row 1` (`FLOAT`)
  - `Column 1 Row 2` (`FLOAT`)
  - `Column 1 Row 3` (`FLOAT`)
  - `Column 1 Row 4` (`FLOAT`)
  - `Column 2 Row 1` (`FLOAT`)
  - `Column 2 Row 2` (`FLOAT`)
  - `Column 2 Row 3` (`FLOAT`)
  - `Column 2 Row 4` (`FLOAT`)
  - `Column 3 Row 1` (`FLOAT`)
  - `Column 3 Row 2` (`FLOAT`)
  - `Column 3 Row 3` (`FLOAT`)
  - `Column 3 Row 4` (`FLOAT`)
  - `Column 4 Row 1` (`FLOAT`)
  - `Column 4 Row 2` (`FLOAT`)
  - `Column 4 Row 3` (`FLOAT`)
  - `Column 4 Row 4` (`FLOAT`)
- **Outputs:**
  - `Matrix` (`MATRIX`)


### Combine Transform — `FunctionNodeCombineTransform`
- **Notes:** The Combine Transform node combines a translation vector, a rotation vector, and a scale vector into a Transformation Matrix .
- **Inputs:**
  - `Translation` (`VECTOR`)
  - `Rotation` (`ROTATION`)
  - `Scale` (`VECTOR`)
- **Outputs:**
  - `Transform` (`MATRIX`)


### Invert Matrix — `FunctionNodeInvertMatrix`
- **Notes:** Returns the inverse of the given matrix.
- **Inputs:**
  - `Matrix` (`MATRIX`)
- **Outputs:**
  - `Matrix` (`MATRIX`)
  - `Invertible` (`BOOLEAN`)


### Matrix Determinant — `FunctionNodeMatrixDeterminant`
- **Notes:** The Matrix Determinant node computes the determinant of the passed in matrix.
- **Inputs:**
  - `Matrix` (`MATRIX`)
- **Outputs:**
  - `Determinant` (`FLOAT`)


### Matrix SVD — `FunctionNodeMatrixSVD`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Singular value decomposition of a matrix into rotation/scale factors.
- **Inputs:**
  - `Matrix` (`MATRIX`)
- **Outputs:**
  - `U` (`MATRIX`)
  - `S` (`VECTOR`)
  - `V` (`MATRIX`)


### Multiply Matrices — `FunctionNodeMatrixMultiply`
- **Notes:** The Multiply Matrices node performs a matrix multiplication on two input matrices.
- **Inputs:**
  - `Matrix` (`MATRIX`)
  - `Matrix` (`MATRIX`)
- **Outputs:**
  - `Matrix` (`MATRIX`)


### Project Point — `FunctionNodeProjectPoint`
- **Notes:** Applies a projection matrix to a point. Specifically, this node turns the given Euclidean vector (X, Y, Z) into the homogeneous vector (X, Y, Z, 1), multiplies the given projection matrix by it, and turns the resulting homogeneous vector back into a Euclidean one by dividing it by the absolute value of its W component. This last step is also known as perspective division.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Transform` (`MATRIX`)
- **Outputs:**
  - `Vector` (`VECTOR`)


### Separate Matrix — `FunctionNodeSeparateMatrix`
- **Notes:** The Separate Matrix node splits a 4x4 matrix into its individual values.
- **Inputs:**
  - `Matrix` (`MATRIX`)
- **Outputs:**
  - `Column 1 Row 1` (`FLOAT`)
  - `Column 1 Row 2` (`FLOAT`)
  - `Column 1 Row 3` (`FLOAT`)
  - `Column 1 Row 4` (`FLOAT`)
  - `Column 2 Row 1` (`FLOAT`)
  - `Column 2 Row 2` (`FLOAT`)
  - `Column 2 Row 3` (`FLOAT`)
  - `Column 2 Row 4` (`FLOAT`)
  - `Column 3 Row 1` (`FLOAT`)
  - `Column 3 Row 2` (`FLOAT`)
  - `Column 3 Row 3` (`FLOAT`)
  - `Column 3 Row 4` (`FLOAT`)
  - `Column 4 Row 1` (`FLOAT`)
  - `Column 4 Row 2` (`FLOAT`)
  - `Column 4 Row 3` (`FLOAT`)
  - `Column 4 Row 4` (`FLOAT`)


### Separate Transform — `FunctionNodeSeparateTransform`
- **Notes:** The Separate Transform node separates a Transformation Matrix into a translation vector, a rotation vector, and a scale vector.
- **Inputs:**
  - `Transform` (`MATRIX`)
- **Outputs:**
  - `Translation` (`VECTOR`)
  - `Rotation` (`ROTATION`)
  - `Scale` (`VECTOR`)


### Transform Direction — `FunctionNodeTransformDirection`
- **Notes:** The Transform Direction node multiplies a Transformation Matrix by a vector.
- **Inputs:**
  - `Direction` (`VECTOR`)
  - `Transform` (`MATRIX`)
- **Outputs:**
  - `Direction` (`VECTOR`)


### Transform Point — `FunctionNodeTransformPoint`
- **Notes:** The Transform Point node applies a Transformation Matrix to a position vector.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Transform` (`MATRIX`)
- **Outputs:**
  - `Vector` (`VECTOR`)


### Transpose Matrix — `FunctionNodeTransposeMatrix`
- **Notes:** The Transpose Matrix node flips a matrix over its diagonal. See also Transpose on Wikipedia.
- **Inputs:**
  - `Matrix` (`MATRIX`)
- **Outputs:**
  - `Matrix` (`MATRIX`)
