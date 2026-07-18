---
title: Utilities Math
section: utilities
description: "Utilities (Math): Scalar, integer, comparison, mapping, and curve math helpers."
tags: bit, boolean, compare, float, integer, map, math, utilities
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Utilities Math

Reference nodes for `Utilities Math`. Total: **10** nodes.

### Bit Math — `FunctionNodeBitMath`
- **Notes:** The Bit Math node performs bitwise operations on 32-bit integer values. It is useful for low-level data manipulation and logic operations. The result of the bitwise operation.
- **Inputs:**
  - `A` (`INT`)
  - `B` (`INT`)
  - `Shift` (`INT`)
- **Outputs:**
  - `Value` (`INT`)

### Boolean Math — `FunctionNodeBooleanMath`
- **Notes:** The Boolean Math node performs a basic logical operation on its inputs. Standard Boolean output.
- **Inputs:**
  - `Boolean` (`BOOLEAN`)
  - `Boolean` (`BOOLEAN`)
- **Outputs:**
  - `Boolean` (`BOOLEAN`)
- **Properties:**
  - `operation` (AND, OR, NOT, NAND, NOR, XNOR, XOR, IMPLY, NIMPLY) — AND: True when both inputs are true; OR: True when at least one input is true; NOT: Opposite of the input

### Clamp — `ShaderNodeClamp`
- **Notes:** Clamp a value between a minimum and a maximum.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Min` (`FLOAT`)
  - `Max` (`FLOAT`)
- **Outputs:**
  - `Result` (`FLOAT`)
- **Example:** The Voronoi Texture node outputs a value whose minimum is zero. We can use the Clamp node to clamp this value such that the minimum is 0.2.

### Compare — `FunctionNodeCompare`
- **Compatibility:** Blender 5.2 changed socket identifiers and made `A`/`B` generic. Do not reuse 5.1 socket identifiers; resolve sockets from live readback.
- **Notes:** The Compare node takes two inputs and does an operation to determine whether they are similar. The node can work on all generic data types, and has modes for vectors that contain more complex comparisons, which can help to reduce the number of necessary nodes, and make a node tree more readable.
- **Inputs:**
  - `A` (`FLOAT`)
  - `B` (`FLOAT`)
  - `A` (`INT`)
  - `B` (`INT`)
  - `A` (`VECTOR`)
  - `B` (`VECTOR`)
  - `A` (`COLOR`)
  - `B` (`COLOR`)
  - `A` (`STRING`)
  - `B` (`STRING`)
  - `C` (`FLOAT`)
  - `Angle` (`FLOAT`)
  - `Epsilon` (`FLOAT`)
- **Outputs:**
  - `Result` (`BOOLEAN`)
- **Example:** Here, the compare node is used with the Direction mode to compare the direction of the sphere’s face normals to the “direction” of the cube object’s location.
- **Properties:**
  - `operation` (LESS_THAN, LESS_EQUAL, GREATER_THAN, GREATER_EQUAL, EQUAL, NOT_EQUAL, BRIGHTER, DARKER) — LESS_THAN: True when the first input is smaller than second input; LESS_EQUAL: True when the first input is smaller than the second input or equal; GREATER_THAN: True when the first input is greater than the second input
  - `mode` (ELEMENT, LENGTH, AVERAGE, DOT_PRODUCT, DIRECTION) — ELEMENT: Compare each element of the input vectors; LENGTH: Compare the length of the input vectors; AVERAGE: Compare the average of the input vectors elements

### Float Curve — `ShaderNodeFloatCurve`
- **Notes:** Map an input float to a curve and outputs a float value.
- **Inputs:**
  - `Factor` (`FLOAT`)
  - `Value` (`FLOAT`)
- **Outputs:**
  - `Value` (`FLOAT`)

### Float to Integer — `FunctionNodeFloatToInt`
- **Notes:** The Float To Integer node takes a single floating point number input and converts it to an integer with a choice of methods.
- **Inputs:**
  - `Float` (`FLOAT`)
- **Outputs:**
  - `Integer` (`INT`)

### Hash Value — `FunctionNodeHashValue`
- **Notes:** The Hash Value node takes a value input and hashes this to an integer.
- **Inputs:**
  - `Value` (`INT`)
  - `Seed` (`INT`)
- **Outputs:**
  - `Hash` (`INT`)
- **Warning:** Hashes cannot be relied upon to be used as unique identifiers because they are not guaranteed to be unique. It can be used to generate somewhat stable randomness especially in cases where White Noise does not offer enough flexibility.

### Integer Math — `FunctionNodeIntegerMath`
- **Notes:** The Integer Math node performs math operations. Standard integer output.
- **Inputs:**
  - `Value` (`INT`)
  - `Value` (`INT`)
  - `Value` (`INT`)
- **Outputs:**
  - `Value` (`INT`)

### Map Range — `ShaderNodeMapRange`
- **Notes:** Remap a value from a range to a target range.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `From Min` (`FLOAT`)
  - `From Max` (`FLOAT`)
  - `To Min` (`FLOAT`)
  - `To Max` (`FLOAT`)
  - `Steps` (`FLOAT`)
  - `Vector` (`VECTOR`)
  - `From Min` (`VECTOR`)
  - `From Max` (`VECTOR`)
  - `To Min` (`VECTOR`)
  - `To Max` (`VECTOR`)
  - `Steps` (`VECTOR`)
- **Outputs:**
  - `Result` (`FLOAT`)
  - `Vector` (`VECTOR`)
- **Example:** The Noise Texture node outputs a value in the range [0, 1]. We can use the Map Range node to remap this value into the range [-1, 1].

### Math — `ShaderNodeMath`
- **Notes:** Perform math operations.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Value` (`FLOAT`)
  - `Value` (`FLOAT`)
- **Outputs:**
  - `Value` (`FLOAT`)
- **Properties:**
  - `operation` (ADD, SUBTRACT, MULTIPLY, DIVIDE, MULTIPLY_ADD, POWER, LOGARITHM, SQRT, INVERSE_SQRT, ABSOLUTE, EXPONENT, MINIMUM, MAXIMUM, LESS_THAN, GREATER_THAN, SIGN, COMPARE, SMOOTH_MIN, SMOOTH_MAX, ROUND, FLOOR, CEIL, TRUNC, FRACT, MODULO, FLOORED_MODULO, WRAP, SNAP, PINGPONG, SINE, COSINE, TANGENT, ARCSINE, ARCCOSINE, ARCTANGENT, ARCTAN2, SINH, COSH, TANH, RADIANS, DEGREES) — MULTIPLY_ADD: A * B + C; POWER: A power B; LOGARITHM: Logarithm A base B

