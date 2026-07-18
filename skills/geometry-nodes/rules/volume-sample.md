---
title: Volume Sample
section: volume
description: "Volume Nodes (Sample): Sample and derive grid fields such as gradient, curl, and divergence."
tags: advect, grid, sample, volume
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Volume Sample

Reference nodes for `Volume Sample`. Total: **7** nodes.

### Advect Grid — `GeometryNodeGridAdvect`
- **Notes:** The Advect Grid node moves voxel values through a velocity field over time using numerical integration. This operation is called advection and is commonly used in fluid, smoke, and motion simulation systems to evolve quantities such as density, temperature, or color according to a flow field. The node supports multiple integration schemes that trade off between speed, accuracy, and numerical stability. It can be used for both scalar and vector grids, provided the voxel size is uniform across the domain. Advection is conceptually equivalent to tracing each voxel backward through the velocity field by a small time step, sampling the grid value from the previous location, and assigning that value to the current voxel.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Velocity` (`VECTOR`)
  - `Time Step` (`FLOAT`)
  - `Integration Scheme` (`MENU: Semi-Lagrangian, Midpoint, Runge-Kutta 3, Runge-Kutta 4, MacCormack, BFECC`)
  - `Limiter` (`MENU: None, Clamp, Revert`)
- **Outputs:**
  - `Grid` (`FLOAT`)

### Grid Curl — `GeometryNodeGridCurl`
- **Notes:** The Grid Curl node computes the curl of a vector field stored in a voxel grid. Curl represents the local amount of rotational motion or circulation within a vector field—essentially, how much and in what direction the field “spins” around each point. In mathematical terms, the curl of a 3D vector field \(F = (Fx, Fy, Fz)\) is a vector that describes the infinitesimal rotation of the field, defined as: \[\nabla \times \mathbf{F} = \left(\frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z} \right) \mathbf{\hat{i}} + \left(\frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \right) \mathbf{\hat{j}} + \left(\frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right) \mathbf{\hat{k}}\] The resulting vector points along the axis of rotation, and its magnitude indicates the strength of that rotation. This operation is useful for generating turbulence or analyzing the rotational behavior of flow fields in simulations and procedural effects.
- **Inputs:**
  - `Grid` (`VECTOR`)
- **Outputs:**
  - `Curl` (`VECTOR`)

### Grid Divergence — `GeometryNodeGridDivergence`
- **Notes:** The Grid Divergence node computes the *divergence* of a vector field stored in a voxel grid. Divergence measures how much a field is “spreading out” or “converging” at each point, representing the net flow entering or leaving a voxel. A positive divergence value indicates that the field is expanding outward from that voxel (acting as a source), while a negative value indicates that the field is converging inward (acting as a sink). A divergence near zero means the field is locally balanced, with equal flow in and out. This operator is commonly used in fluid and smoke simulation workflows, where it helps enforce incompressibility or visualize the flow behavior of vector fields such as velocity grids. Mathematically, for a 3D vector field \(\mathbf{F} = (F_x, F_y, F_z)\), the divergence is defined as: \[\nabla \cdot \mathbf{F} = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z}\]
- **Inputs:**
  - `Grid` (`VECTOR`)
- **Outputs:**
  - `Divergence` (`FLOAT`)

### Grid Gradient — `GeometryNodeGridGradient`
- **Notes:** The Grid Gradient node calculates the gradient of a scalar voxel grid. The gradient is a vector field that describes both the direction and rate of the steepest increase in the grid’s values at each voxel. In other words, it shows how and where the scalar quantity (such as density, temperature, or distance) changes in 3D space. The direction of the gradient vector points toward increasing values, and its magnitude represents how quickly the value changes in that direction. Mathematically, for a scalar field \(f(x, y, z)\), the gradient is defined as: \[\nabla f = \frac{\partial f}{\partial x} \mathbf{\hat{i}} + \frac{\partial f}{\partial y} \mathbf{\hat{j}} + \frac{\partial f}{\partial z} \mathbf{\hat{k}}\] This operation is often used in procedural modeling or simulation workflows to derive direction fields from scalar quantities, such as computing surface normals from a signed distance field (SDF) or determining the flow direction in density or temperature fields.
- **Inputs:**
  - `Grid` (`FLOAT`)
- **Outputs:**
  - `Gradient` (`VECTOR`)

### Grid Laplacian — `GeometryNodeGridLaplacian`
- **Notes:** The Grid Laplacian node computes the Laplacian of a scalar voxel grid. The Laplacian measures how a value at each voxel differs from the average of its neighbors—essentially, how much the field “curves” or deviates locally. Mathematically, the Laplacian is defined as the divergence of the gradient of a scalar field. It is commonly used in physics and geometry for diffusion, smoothing, curvature analysis, and solving partial differential equations. For a scalar field \(f(x, y, z)\), the Laplacian \(\nabla^2 f\) is given by: \[\nabla^2 f = \nabla f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}\] The Laplacian is positive where the field has a local minimum (value smaller than its surroundings) and negative where it has a local maximum (value larger than its surroundings).
- **Inputs:**
  - `Grid` (`FLOAT`)
- **Outputs:**
  - `Laplacian` (`FLOAT`)

### Sample Grid — `GeometryNodeSampleGrid`
- **Notes:** The Sample Grid node retrieves values from a voxel grid at given positions in space. It evaluates the grid’s stored data (such as float, integer, boolean, or vector values) and returns the interpolated result for each queried position. This node is useful for reading data from grids created by other nodes (e.g. Mesh to SDF Grid, Field to Grid, or Points to SDF Grid) and using those values to drive procedural effects, geometry deformation, or shading.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Position` (`VECTOR`)
  - `Interpolation` (`MENU: Nearest Neighbor, Trilinear, Triquadratic`)
- **Outputs:**
  - `Value` (`FLOAT`)

### Sample Grid Index — `GeometryNodeSampleGridIndex`
- **Notes:** The Sample Grid Index node retrieves values directly from a voxel grid at specific voxel indices rather than at arbitrary spatial positions. Unlike the Sample Grid node, which interpolates between voxels in object space, this node reads the exact stored value of the voxel located at the specified integer coordinates. This makes it useful for working in index space, for example when performing voxel neighborhood lookups, procedural filtering, or sampling based on values from the Voxel Index node.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `X` (`INT`)
  - `Y` (`INT`)
  - `Z` (`INT`)
- **Outputs:**
  - `Value` (`FLOAT`)

