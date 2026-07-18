---
title: Mesh Primitives
section: mesh
description: "Mesh Nodes (Primitives): Generate parametric mesh primitives."
tags: cone, cube, cylinder, mesh, primitives
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Mesh Primitives

Reference nodes for `Mesh Primitives`. Total: **9** nodes.

### Cone — `GeometryNodeMeshCone`
- **Notes:** Generates a cone mesh that is optionally truncated. Note: If the top and bottom radii are both zero, this node will output a single line.
- **Inputs:**
  - `Vertices` (`INT`)
  - `Side Segments` (`INT`)
  - `Fill Segments` (`INT`)
  - `Radius Top` (`FLOAT`)
  - `Radius Bottom` (`FLOAT`)
  - `Depth` (`FLOAT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `Top` (`BOOLEAN`)
  - `Bottom` (`BOOLEAN`)
  - `Side` (`BOOLEAN`)
  - `UV Map` (`VECTOR`)
- **Tip:** If the top and bottom radii are both zero, this node will output a single line.


### Cube Grid Topology — `GeometryNodeCubeGridTopology`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Generate a cube-grid mesh topology primitive (voxel-style grid of cubes).
- **Inputs:**
  - `Bounds Min` (`VECTOR`)
  - `Bounds Max` (`VECTOR`)
  - `Resolution X` (`INT`)
  - `Resolution Y` (`INT`)
  - `Resolution Z` (`INT`)
  - `Min X` (`INT`)
  - `Min Y` (`INT`)
  - `Min Z` (`INT`)
- **Outputs:**
  - `Topology` (`BOOLEAN`)


### Cube — `GeometryNodeMeshCube`
- **Notes:** The Cube node generates a cuboid mesh with variable side lengths and subdivisions. The inside of the mesh is still hollow like a normal cube.
- **Inputs:**
  - `Size` (`VECTOR`)
  - `Vertices X` (`INT`)
  - `Vertices Y` (`INT`)
  - `Vertices Z` (`INT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `UV Map` (`VECTOR`)


### Cylinder — `GeometryNodeMeshCylinder`
- **Notes:** The Cylinder node generates a cylinder mesh. It is similar to the Cone node but always uses the same radius for the circles at the top and bottom.
- **Inputs:**
  - `Vertices` (`INT`)
  - `Side Segments` (`INT`)
  - `Fill Segments` (`INT`)
  - `Radius` (`FLOAT`)
  - `Depth` (`FLOAT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `Top` (`BOOLEAN`)
  - `Side` (`BOOLEAN`)
  - `Bottom` (`BOOLEAN`)
  - `UV Map` (`VECTOR`)


### Grid — `GeometryNodeMeshGrid`
- **Notes:** The Grid node generates a planar mesh on the XY plane.
- **Inputs:**
  - `Size X` (`FLOAT`)
  - `Size Y` (`FLOAT`)
  - `Vertices X` (`INT`)
  - `Vertices Y` (`INT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `UV Map` (`VECTOR`)


### Ico Sphere — `GeometryNodeMeshIcoSphere`
- **Notes:** The Icosphere node generates a spherical mesh that consists of equally sized triangles.
- **Inputs:**
  - `Radius` (`FLOAT`)
  - `Subdivisions` (`INT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `UV Map` (`VECTOR`)


### Mesh Circle — `GeometryNodeMeshCircle`
- **Notes:** The Mesh Circle node generates a circular ring of edges that is optionally filled with faces.
- **Inputs:**
  - `Vertices` (`INT`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)


### Mesh Line — `GeometryNodeMeshLine`
- **Notes:** The Mesh Line node generates vertices in a line and connects them with edges.
- **Inputs:**
  - `Count` (`INT`)
  - `Resolution` (`FLOAT`)
  - `Start Location` (`VECTOR`)
  - `Offset` (`VECTOR`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)


### UV Sphere — `GeometryNodeMeshUVSphere`
- **Notes:** The UV Sphere node generates a spherical mesh mostly out of quads except for triangles at the top and bottom.
- **Inputs:**
  - `Segments` (`INT`)
  - `Rings` (`INT`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `UV Map` (`VECTOR`)
