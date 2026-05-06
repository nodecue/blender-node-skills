---
title: Mesh Read
section: mesh
description: "Mesh Nodes (Read): Query mesh topology and mesh-domain measurements."
tags: edge, edges, mesh, read
---

## Mesh Read

Reference nodes for `Mesh Read`. Total: **13** nodes.

### Edge Angle — `GeometryNodeInputMeshEdgeAngle`
- **Notes:** The Edge Angle node calculates the angle in radians between two faces that meet at an edge. For the Face, Face Corner, and Point domains, the node uses simple domain interpolation to move values from the mesh’s edges.
- **Inputs:** None
- **Outputs:**
  - `Unsigned Angle` (`FLOAT`)
  - `Signed Angle` (`FLOAT`)
- **Tip:** The output of this node depends on the density of the mesh. If there are more edges closer together and the curvature of the mesh stays the same, the edge angle will be different.

### Edge Neighbors — `GeometryNodeInputMeshEdgeNeighbors`
- **Notes:** The Edge Neighbors node outputs topology information relating to each edge of a mesh. Using the Face Count output to create a curve on a mesh’s boundary edges.
- **Inputs:** None
- **Outputs:**
  - `Face Count` (`INT`)
- **Example:** Boundary edge detection — Edge Neighbors `Face Count` output to Compare node (EQUAL, B=1) gives a boolean true for boundary edges (edges with only one adjacent face). Useful for finding open edges, UV seams, mesh cleanup.

### Edge Vertices — `GeometryNodeInputMeshEdgeVertices`
- **Notes:** The Edge Vertices node outputs the position and index of the two vertices of each of a mesh’s edges.
- **Inputs:** None
- **Outputs:**
  - `Vertex Index 1` (`INT`)
  - `Vertex Index 2` (`INT`)
  - `Position 1` (`VECTOR`)
  - `Position 2` (`VECTOR`)
- **Tip:** The order of the two vertices of an edge is arbitrary. In some cases it may be predictable based on the internals of the algorithm that created the mesh, but in general the order should not be relied upon.

### Edges to Face Groups — `GeometryNodeEdgesToFaceGroups`
- **Notes:** The Edges to Face Groups node group faces into regions surrounded by the selected boundary edges.
- **Inputs:**
  - `Boundary Edges` (`BOOLEAN`)
- **Outputs:**
  - `Face Group ID` (`INT`)

### Face Area — `GeometryNodeInputMeshFaceArea`
- **Notes:** The Face Area node outputs the surface area of a mesh’s faces. The units are in Blender units no matter the unit system, equivalent to meters-squared at the default unit scale.
- **Inputs:** None
- **Outputs:**
  - `Area` (`FLOAT`)
- **Example:** Combined with the Attribute Statistic Node, this node can be used to calculate the total surface area of a mesh. Used with: Attribute Statistic.
- **Tip:** For quads and N-gons, when the face’s vertices are not planar, the output is not necessarily the same as the sum of every one of the face’s triangles visible in the viewport. In this case it should only be used an approximation. In some cases, the Triangulate Node can be used to get an exact value.

### Face Group Boundaries — `GeometryNodeMeshFaceSetBoundaries`
- **Notes:** The Face Group Boundaries Node finds the edges which lie on the boundaries of specified regions. These edges could be used to mark seams for UV unwrapping, for example.
- **Inputs:**
  - `Face Group ID` (`INT`)
- **Outputs:**
  - `Boundary Edges` (`BOOLEAN`)
- **Example:** Combined with the UV Unwrap Node, this node is used to turn the face sets (right cube) into a UV map for a texture (left cube). Used with: UV Unwrap.

### Face Set — `GeometryNodeToolFaceSet`
- **Notes:** The Face Set Node outputs which face set a face is in, and whether or not face sets exist in the mesh at all. The corresponding data flow node is the Set Face Set Node.
- **Inputs:** None
- **Outputs:**
  - `Face Set` (`INT`)
  - `Exists` (`BOOLEAN`)
- **Warning:** This node can only be used in the Tool context.

### Face Neighbors — `GeometryNodeInputMeshFaceNeighbors`
- **Notes:** The Face Neighbors node outputs topology information relating to each face of a mesh.
- **Inputs:** None
- **Outputs:**
  - `Vertex Count` (`INT`)
  - `Face Count` (`INT`)

### Is Face Smooth — `GeometryNodeInputShadeSmooth`
- **Notes:** The Is Face Smooth node outputs true for each face of the mesh if that face is marked to render smooth shaded. Otherwise, if the face is marked to render as flat shaded, then the node outputs false.
- **Inputs:** None
- **Outputs:**
  - `Smooth` (`BOOLEAN`)

### Is Face Planar — `GeometryNodeInputMeshFaceIsPlanar`
- **Notes:** The Is Face Planar node outputs whether every triangle of a quads or N-gons is on the same plane as all of the others, in other words, if they have the same normal. For example, a non-planar face can be created by moving a single vertex in a face but not the others. Triangles will always be planar.
- **Inputs:**
  - `Threshold` (`FLOAT`)
- **Outputs:**
  - `Planar` (`BOOLEAN`)
- **Example:** Combined with the Set Material Node, this node is used to visualize all non-planar faces in a mesh. Used with: Set Material.

### Mesh Island — `GeometryNodeInputMeshIsland`
- **Notes:** The Mesh Island node outputs information about separate connected regions, or “islands” of a mesh. Whenever two vertices are connected together by an edge, they are considered as part of the same island, and will have the same Island Index output. This node’s behavior is similar to the Select Linked operator in edit mode, or the Random per Island output of the Geometry shader node.
- **Inputs:** None
- **Outputs:**
  - `Island Index` (`INT`)
  - `Island Count` (`INT`)

### Shortest Edge Paths — `GeometryNodeInputShortestEdgePaths`
- **Notes:** The Shortest Edge Paths node finds paths along mesh edges to a selection of end vertices. The cost used to define “shortest” can be set to anything. By default there is a constant cost for every edge, but a typical input would be the length of each edge. The output is encoded with vertex indices, and is meant to be used on the vertex domain. For each vertex, the Next Vertex Index output gives the index of the following vertex in the path to the “closest” endpoint. The node is implemented with Dijkstra’s algorithm.
- **Inputs:**
  - `End Vertex` (`BOOLEAN`)
  - `Edge Cost` (`FLOAT`)
- **Outputs:**
  - `Next Vertex Index` (`INT`)
  - `Total Cost` (`FLOAT`)
- **Example:** Shortest Edge Paths on a deformed Ico Sphere. Gradient-colored maze showing shortest paths to a target sphere. Organic branching structure on Suzanne.
- **Tip:** The edge length is a natural input to the Edge Cost. It can be implemented with the Edge Vertices Node and the Vector Math Node set to the Distance operation.
- **Tip:** This node can be used with the Edge Paths to Selection Node or the Edge Paths to Curves Node to generate new geometry based on the paths.

### Vertex Neighbors — `GeometryNodeInputMeshVertexNeighbors`
- **Notes:** The Vertex Neighbors node outputs topology information relating to each vertex of a mesh.
- **Inputs:** None
- **Outputs:**
  - `Vertex Count` (`INT`)
  - `Face Count` (`INT`)
- **Example:** Corner vertex detection — Vertex Neighbors `Face Count` output to Compare node (LESS_THAN, threshold) identifies corner or boundary vertices. Useful for mesh analysis, automatic pinning, feature detection.

