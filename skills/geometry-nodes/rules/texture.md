---
title: Texture
section: texture
description: "Texture Nodes: Procedural and image-based texture generators and samplers."
tags: brick, checker, gabor, image, noise, texture
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Texture

Reference nodes for `Texture`. Total: **10** nodes.

### Brick Texture — `ShaderNodeTexBrick`
- **Notes:** Generate a procedural texture producing bricks.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Color1` (`COLOR`)
  - `Color2` (`COLOR`)
  - `Mortar` (`COLOR`)
  - `Scale` (`FLOAT`)
  - `Mortar Size` (`FLOAT`)
  - `Mortar Smooth` (`FLOAT`)
  - `Bias` (`FLOAT`)
  - `Brick Width` (`FLOAT`)
  - `Row Height` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)
  - `Factor` (`FLOAT`)
- **Example:** Brick texture: Colors changed, Squash 0.62, Squash Frequency 3.
- **Tip:** Texture nodes can produce details at a higher frequency than geometry can show. This may cause artifacts such as Moiré type patterns or a lack of detail due to insufficient sampling points.

### Checker Texture — `ShaderNodeTexChecker`
- **Notes:** Generate a checkerboard texture.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Color1` (`COLOR`)
  - `Color2` (`COLOR`)
  - `Scale` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)
  - `Factor` (`FLOAT`)
- **Example:** Default Checker texture.
- **Tip:** Texture nodes can produce details at a higher frequency than geometry can show. This may cause artifacts such as Moiré type patterns or a lack of detail due to insufficient sampling points.

### Gabor Texture — `ShaderNodeTexGabor`
- **Notes:** Generate Gabor noise.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Scale` (`FLOAT`)
  - `Frequency` (`FLOAT`)
  - `Anisotropy` (`FLOAT`)
  - `Orientation` (`FLOAT`)
  - `Orientation` (`VECTOR`)
- **Outputs:**
  - `Value` (`FLOAT`)
  - `Phase` (`FLOAT`)
  - `Intensity` (`FLOAT`)
- **Example:** The following table demonstrates different outputs of the node with different parameters.

### Gradient Texture — `ShaderNodeTexGradient`
- **Notes:** Generate interpolated color and intensity values based on the input vector.
- **Inputs:**
  - `Vector` (`VECTOR`)
- **Outputs:**
  - `Color` (`COLOR`)
  - `Factor` (`FLOAT`)
- **Example:** Gradient texture using object coordinates.

### Image Texture — `GeometryNodeImageTexture`
- **Notes:** The Image Texture node is used to add an image file as a texture. The image data is sampled with the input Vector and outputs a Color and Alpha value.
- **Inputs:**
  - `Image` (`IMAGE`)
  - `Vector` (`VECTOR`)
  - `Frame` (`INT`)
- **Outputs:**
  - `Color` (`COLOR`)
  - `Alpha` (`FLOAT`)
- **Example:** Image Texture displacing a plane.
- **Tip:** Unlike the other texture nodes, this node operates differently in geometry nodes compared to the equivalent shader node. When not connected the Vector input has an implicit `position` attribute value.

### Magic Texture — `ShaderNodeTexMagic`
- **Notes:** Generate a psychedelic color texture.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Scale` (`FLOAT`)
  - `Distortion` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)
  - `Factor` (`FLOAT`)
- **Example:** Magic texture: Depth 10, Distortion 2.0.

### Noise Texture — `ShaderNodeTexNoise`
- **Notes:** Generate fractal Perlin noise.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `W` (`FLOAT`)
  - `Scale` (`FLOAT`)
  - `Detail` (`FLOAT`)
  - `Roughness` (`FLOAT`)
  - `Lacunarity` (`FLOAT`)
  - `Offset` (`FLOAT`)
  - `Gain` (`FLOAT`)
  - `Distortion` (`FLOAT`)
- **Outputs:**
  - `Factor` (`FLOAT`)
  - `Color` (`COLOR`)
- **Example:** Noise Texture with high detail.

### Voronoi Texture — `ShaderNodeTexVoronoi`
- **Notes:** Generate Worley noise based on the distance to random points. Typically used to generate textures such as stones, water, or biological cells.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `W` (`FLOAT`)
  - `Scale` (`FLOAT`)
  - `Detail` (`FLOAT`)
  - `Roughness` (`FLOAT`)
  - `Lacunarity` (`FLOAT`)
  - `Smoothness` (`FLOAT`)
  - `Exponent` (`FLOAT`)
  - `Randomness` (`FLOAT`)
- **Outputs:**
  - `Distance` (`FLOAT`)
  - `Color` (`COLOR`)
  - `Position` (`VECTOR`)
  - `W` (`FLOAT`)
  - `Radius` (`FLOAT`)
- **Example:** The difference between F1 and Smooth F1 can be used to create beveled Voronoi cells. Creating a hammered metal shader using the Voronoi Texture node.

### Wave Texture — `ShaderNodeTexWave`
- **Notes:** Generate procedural bands or rings with noise.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `Scale` (`FLOAT`)
  - `Distortion` (`FLOAT`)
  - `Detail` (`FLOAT`)
  - `Detail Scale` (`FLOAT`)
  - `Detail Roughness` (`FLOAT`)
  - `Phase Offset` (`FLOAT`)
- **Outputs:**
  - `Color` (`COLOR`)
  - `Factor` (`FLOAT`)
- **Example:** Wave Texture.
- **Tip:** In general, textures can be distorted by mixing their texture coordinates with another texture. The distortion built into the Wave Texture Node uses the Color output of the Noise Texture Node. To replicate this, center its value range around zero, multiply it by a factor proportional to Distortion/Scale and add the result onto the texture coordinates. Detail, Detail Scale and Roughness of the Wave Texture Node correspond to the inputs on the Noise Texture Node.

### White Noise Texture — `ShaderNodeTexWhiteNoise`
- **Notes:** Calculate a random value or color based on an input seed.
- **Inputs:**
  - `Vector` (`VECTOR`)
  - `W` (`FLOAT`)
- **Outputs:**
  - `Value` (`FLOAT`)
  - `Color` (`COLOR`)
- **Example:** Generating cell noise using the Snap vector operation and the White Noise node.

