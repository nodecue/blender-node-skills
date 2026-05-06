---
title: Color
section: color
description: "Color Nodes: General-purpose color construction, conversion, and blending utilities."
tags: blackbody, color, combine, gamma, mix, separate
---

## Color

Reference nodes for `Color`. Total: **8** nodes.

### Blackbody — `ShaderNodeBlackbody`
- **Notes:** The Blackbody node converts a blackbody temperature to RGB value. This can be useful for materials that emit light at natural occurring frequencies.
- **Inputs:**
  - `Temperature` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)
- **Example:** Example of the color ranges of the Blackbody node.

### Color Ramp — `ShaderNodeValToRGB`
- **Notes:** Map values to colors with the use of a gradient.
- **Inputs:**
  - `Factor` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)
  - `Alpha` (`FLOAT`)
- **Example:** An often overlooked use case of the Color Ramp is to turn a black-and-white image into a colored image with transparency.

### Combine Color — `FunctionNodeCombineColor`
- **Notes:** Combines four grayscale channels into one color image, based on a particular Color Model . Standard color output.
- **Inputs:**
  - `Red` (`FLOAT`)
  - `Green` (`FLOAT`)
  - `Blue` (`FLOAT`)
  - `Alpha` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)

### Gamma — `ShaderNodeGamma`
- **Notes:** Apply a gamma correction.
- **Inputs:**
  - `Color` (`COLOR`)
  - `Gamma` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)
- **Example:** Example of a Gamma node.

### Mix — `ShaderNodeMix`
- **Notes:** Mix values by a factor.
- **Inputs:**
  - `Factor` (`FLOAT`)
  - `Factor` (`VECTOR`)
  - `A` (`FLOAT`)
  - `B` (`FLOAT`)
  - `A` (`VECTOR`)
  - `B` (`VECTOR`)
  - `A` (`COLOR`)
  - `B` (`COLOR`)
  - `A` (`ROTATION`)
  - `B` (`ROTATION`)
- **Outputs:**
  - `Result` (`FLOAT`)
  - `Result` (`VECTOR`)
  - `Result` (`COLOR`)
  - `Result` (`ROTATION`)
- **Example:** See the Mix Color Node for additional examples. Used with: Mix Color.

### Mix (Legacy) — `ShaderNodeMixRGB`
- **Notes:** Mix two input colors.
- **Inputs:**
  - `Factor` (`FLOAT`)
  - `Color1` (`COLOR`)
  - `Color2` (`COLOR`)
- **Outputs:**
  - `Color` (`COLOR`)

### RGB Curves — `ShaderNodeRGBCurve`
- **Notes:** The RGB Curves Node performs level adjustments on each color channel.
- **Inputs:**
  - `Factor` (`FLOAT`)
  - `Color` (`COLOR`)
- **Outputs:**
  - `Color` (`COLOR`)
- **Example:** Below are some common curves you can use to achieve desired effects. From left to right: 1. Lighten shadows 2. Negative 3. Decrease contrast 4. Used with: Mix Color.
- **Tip:** To define the black and white levels, use the eyedropper to select a color sample of a displayed image.

### Separate Color — `FunctionNodeSeparateColor`
- **Notes:** Splits an image into its channels, based on a particular Color Model .
- **Inputs:**
  - `Color` (`COLOR`)
- **Outputs:**
  - `Red` (`FLOAT`)
  - `Green` (`FLOAT`)
  - `Blue` (`FLOAT`)
  - `Alpha` (`FLOAT`)
