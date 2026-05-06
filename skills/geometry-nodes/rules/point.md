---
title: Point
section: point
description: "Point Nodes: Create, distribute, sample, and convert point-based geometry."
tags: distribute, point, points
---

## Point

Reference nodes for `Point`. Total: **9** nodes.

### Distribute Points in Grid — `GeometryNodeDistributePointsInGrid`
- **Notes:** The Distribute Points in Grid node generates points within the active region of a voxel grid. The number and placement of points can be controlled using the grid’s density values and various distribution parameters. This node is useful for scattering geometry procedurally inside a volumetric region, such as distributing particles in a fog volume, populating points in a simulation domain, or sampling areas defined by a signed distance field (SDF) or density grid.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Density` (`FLOAT`)
  - `Seed` (`INT`)
  - `Spacing` (`VECTOR`)
  - `Threshold` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)

### Distribute Points in Volume — `GeometryNodeDistributePointsInVolume`
- **Notes:** The Distribute Points in Volume node creates points inside of volume grids. The node has two basic modes of operation: distributing points randomly, or in a regular grid. Both methods operate on all of the float grids in the volume.
- **Inputs:**
  - `Volume` (`GEOMETRY`)
  - `Mode` (`MENU: Random, Grid`)
  - `Density` (`FLOAT`)
  - `Seed` (`INT`)
  - `Spacing` (`VECTOR`)
  - `Threshold` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)

### Distribute Points on Faces — `GeometryNodeDistributePointsOnFaces`
- **Notes:** The Distribute Points on Faces node places points on the surface of the input geometry object. Point, corner, and polygon attributes of the input geometry are transferred to the generated points. That includes vertex weights and UV maps. Additionally, the node has Normal and Rotation outputs. The node also generates a stable ID, stored in the built-in `id` attribute, used as a stable identifier for each point. When the mesh is deformed or the density changes the values will be consistent for each remaining point. This attribute is used in the Random Value and Instance on Points nodes.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Distance Min` (`FLOAT`)
  - `Density Max` (`FLOAT`)
  - `Density` (`FLOAT`)
  - `Density Factor` (`FLOAT`)
  - `Seed` (`INT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)
  - `Normal` (`VECTOR`)
  - `Rotation` (`ROTATION`)
- **Properties:**
  - `distribute_method` (RANDOM, POISSON) — RANDOM: Distribute points randomly on the surface; POISSON: Distribute the points randomly on the surface while taking a minimum distance...

### Points — `GeometryNodePoints`
- **Notes:** The Points node generate a point cloud with positions and radii defined by fields.
- **Inputs:**
  - `Count` (`INT`)
  - `Position` (`VECTOR`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)
- **Tip:** Since the point cloud is created from scratch, the Position and Radius inputs can only depend on the index node. Regular input nodes like the position won’t work.

### Points to Curves — `GeometryNodePointsToCurves`
- **Notes:** The Points to Curves node generates a Curves geometry by taking all points and inserting them to new curves. All Attributes from points are propagated to Curve Points. Built-in curves attributes stored in points will be ignored.
- **Inputs:**
  - `Points` (`GEOMETRY`)
  - `Curve Group ID` (`INT`)
  - `Weight` (`FLOAT`)
- **Outputs:**
  - `Curves` (`GEOMETRY`)
- **Example:** The above example creates a curve Array with connections between curves. Used with: Arc primitive, Duplicate Elements, Curve to Points.
- **Tip:** To simplify thinking about points, attributes and their positions in each curve, The weight of each point in curve can be associated with a point attributes value. The sorting and grouping will be reflected on the attributes as like on the Weight and Group ID.
- **Tip:** If points of curve have the same Weight value, the order will be the same as its original relative location. Without any Weight and Group ID inputs, each point will have the same indices in the curve.

### Points to SDF Grid — `GeometryNodePointsToSDFGrid`
- **Notes:** The Points to SDF Grid node generates a Signed Distance Field (SDF)*grid from a set of input points. Each voxel in the resulting grid stores the shortest signed distance to the nearest point, allowing points to be represented as smooth, volumetric shapes. Positive values represent distances outside the influence of the points, negative values represent distances inside, and zero corresponds to the surface of the generated implicit sphere around each point. This node is useful for constructing volumetric fields or collision volumes from particles, instances, or procedurally generated point clouds.
- **Inputs:**
  - `Points` (`GEOMETRY`)
  - `Radius` (`FLOAT`)
  - `Voxel Size` (`FLOAT`)
- **Outputs:**
  - `SDF Grid` (`FLOAT`)

### Points to Vertices — `GeometryNodePointsToVertices`
- **Notes:** The Points to Vertices node generate a mesh vertex in the output geometry for each point cloud point in the input geometry.
- **Inputs:**
  - `Points` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Points to Volume — `GeometryNodePointsToVolume`
- **Notes:** The Points to Volume node generates a fog volume sphere around every point in the input geometry. The new volume grid is named “density”. It usually makes sense to combine this node with the Volume to Mesh Node.
- **Inputs:**
  - `Points` (`GEOMETRY`)
  - `Density` (`FLOAT`)
  - `Resolution Mode` (`MENU: Amount, Size`)
  - `Voxel Size` (`FLOAT`)
  - `Voxel Amount` (`FLOAT`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Volume` (`GEOMETRY`)
- **Tip:** This node expects that point positions are not extremely large. For position values of many billions, the behavior isn’t guaranteed, and it may be unstable.

### Set Point Radius — `GeometryNodeSetPointRadius`
- **Notes:** The Set Point Radius node controls the size each selected point cloud point should display with in the viewport. The input node for this data is the Radius Node .
- **Inputs:**
  - `Points` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)

