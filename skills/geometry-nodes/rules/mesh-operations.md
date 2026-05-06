---
title: Mesh Operations
section: mesh
description: "Mesh Nodes (Operations): Mesh topology modification, conversion, and surface operations."
tags: corners, dual, mesh, operations
---

## Mesh Operations

Reference nodes for `Mesh Operations`. Total: **32** nodes.

### Corners of Edge — `GeometryNodeCornersOfEdge`
- **Notes:** Selects a neighboring face corner of an edge and outputs its index. This node is a bit special because it operates in two different domains. First, it evaluates a Weight for each corner in the geometry. Then, for each item in the context domain, it will: - Pick an edge from the geometry based on the Edge Index. - Find some (not all) face corners connected to this edge – see below. - Sort these corners by their associated weight. - Pick a corner from the above sorted list based on the Sort Index, where 0 means the corner with the lowest weight, 1 means the corner with the second-lowest weight and so on. - Output the geometry-wide index of this corner. A graphic for which corners are returned for a given edge - Red: selected edge. - Blue: the corners whose index can be retrieved using this node. - Purple: the corners that can be retrieved by offsetting the blue corner indices using the Offset Corner in Face Node.
- **Inputs:**
  - `Edge Index` (`INT`)
  - `Weights` (`FLOAT`)
  - `Sort Index` (`INT`)
- **Outputs:**
  - `Corner Index` (`INT`)
  - `Total` (`INT`)
- **Tip:** As illustrated below, the node only looks at one corner per connected face. Even though the edge has four neighboring corners, Corner Index can only return the indexes of two of them, and Total will similarly return 2. You can use the Offset Corner in Face Node to retrieve the indexes of the other corners.

### Corners of Face — `GeometryNodeCornersOfFace`
- **Notes:** Selects a corner of a face and outputs its index. This node is a bit special because it operates in two different domains. First, it evaluates a Weight for each corner in the geometry. Then, for each item in the context domain, it will: - Pick a face from the geometry based on the Face Index. - Find the corners of this face. - Sort these corners by their associated weight. - Pick a corner from the above sorted list based on the Sort Index, where 0 means the corner with the lowest weight, 1 means the corner with the second-lowest weight and so on. - Output the geometry-wide index of this corner.
- **Inputs:**
  - `Face Index` (`INT`)
  - `Weights` (`FLOAT`)
  - `Sort Index` (`INT`)
- **Outputs:**
  - `Corner Index` (`INT`)
  - `Total` (`INT`)

### Corners of Vertex — `GeometryNodeCornersOfVertex`
- **Notes:** Selects a neighboring face corner of a vertex and outputs its index. This node is a bit special because it operates in two different domains. First, it evaluates a Weight for each corner in the geometry. Then, for each item in the context domain, it will: - Pick a vertex from the geometry based on the Vertex Index. - Find the face corners adjacent to this vertex. - Sort these corners by their associated weight. - Pick a corner from the above sorted list based on the Sort Index, where 0 means the corner with the lowest weight, 1 means the corner with the second-lowest weight and so on. - Output the geometry-wide index of this corner.
- **Inputs:**
  - `Vertex Index` (`INT`)
  - `Weights` (`FLOAT`)
  - `Sort Index` (`INT`)
- **Outputs:**
  - `Corner Index` (`INT`)
  - `Total` (`INT`)

### Dual Mesh — `GeometryNodeDualMesh`
- **Notes:** The Dual Mesh Node converts a mesh into its dual, i.e. faces are turned into vertices and vertices are turned into faces. This also means that attributes which were on the face domain are transferred to the point domain in the dual mesh.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Keep Boundaries` (`BOOLEAN`)
- **Outputs:**
  - `Dual Mesh` (`GEOMETRY`)
- **Example:** The Dual Mesh Node combines nicely with triangulated meshes. In this case an Ico Sphere is used, which is made up of nice and evenly spaced triangles.
- **Warning:** The Dual Mesh node only works on manifold geometry. To work with non-manifold geometry it’s best to remesh the geometry first.

### Edge Paths to Curves — `GeometryNodeEdgePathsToCurves`
- **Notes:** The Edge Paths to Curves node output curves that follow paths across mesh edges.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Start Vertices` (`BOOLEAN`)
  - `Next Vertex Index` (`INT`)
- **Outputs:**
  - `Curves` (`GEOMETRY`)
- **Tip:** This node is meant to use the output of the Shortest Edge Paths Node. It is similar to the Edge Paths to Selection Node, but it creates a curve that follow each path, rather than a selection of every visited edge.

### Edge Paths to Selection — `GeometryNodeEdgePathsToSelection`
- **Notes:** The Edge Paths to Selection node follows paths across mesh edges and outputs a selection of every visited edge.
- **Inputs:**
  - `Start Vertices` (`BOOLEAN`)
  - `Next Vertex Index` (`INT`)
- **Outputs:**
  - `Selection` (`BOOLEAN`)
- **Tip:** This node is meant to use the output of the Shortest Edge Paths Node. It can be combined with the Separate Geometry Node to remove any unused edges.

### Edges of Corner — `GeometryNodeEdgesOfCorner`
- **Notes:** The Edges of Corner node retrieves the edges on both sides of a face corner.
- **Inputs:**
  - `Corner Index` (`INT`)
- **Outputs:**
  - `Next Edge Index` (`INT`)
  - `Previous Edge Index` (`INT`)

### Edges of Vertex — `GeometryNodeEdgesOfVertex`
- **Notes:** Selects a neighboring edge of a vertex and outputs its index. This node is a bit special because it operates in two different domains. First, it evaluates a Weight for each edge in the geometry. Then, for each item in the context domain, it will: - Pick a vertex from the geometry based on the Vertex Index. - Find the edges connected to this vertex. - Sort these edges by their associated weight. - Pick an edge from the above sorted list based on the Sort Index, where 0 means the edge with the lowest weight, 1 means the edge with the second-lowest weight and so on. - Output the geometry-wide index of this edge.
- **Inputs:**
  - `Vertex Index` (`INT`)
  - `Weights` (`FLOAT`)
  - `Sort Index` (`INT`)
- **Outputs:**
  - `Edge Index` (`INT`)
  - `Total` (`INT`)

### Extrude Mesh — `GeometryNodeExtrudeMesh`
- **Notes:** The Extrude Mesh Node generates new edges or faces on the selected geometry elements and moves them by a certain offset. The operations are similar to the extrude tools in mesh edit mode, though there are some differences. Most importantly, the node never keeps the back-faces of the extrusion in place, they are always removed. Attribute propagation rules may also be different.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Offset` (`VECTOR`)
  - `Offset Scale` (`FLOAT`)
  - `Individual` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `Top` (`BOOLEAN`)
  - `Side` (`BOOLEAN`)
- **Example:** Here, the selection outputs are used to set materials on certain faces of the mesh. Used with: Random Value.
- **Properties:**
  - `mode` (VERTICES, EDGES, FACES)

### Face of Corner — `GeometryNodeFaceOfCorner`
- **Notes:** Retrieves the face that a face corner is part of.
- **Inputs:**
  - `Corner Index` (`INT`)
- **Outputs:**
  - `Face Index` (`INT`)
  - `Index in Face` (`INT`)

### Flip Faces — `GeometryNodeFlipFaces`
- **Notes:** The Flip Faces Node reverses the order of the vertices and edges of each selected face. The most common use of this node is to flip the normals of a face. Any face corner domain attributes of selected faces are also reversed. Though this node is usually used to affect normals, it is not called “Flip Normals” for an important reason. The node does not actually interact with normals directly. Normals are defined by the right hand rule, so if a face’s vertex list is reversed, then its normal will point in the opposite direction.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Mesh to Curve — `GeometryNodeMeshToCurve`
- **Notes:** The Mesh to Curve node converts a mesh into one or more curve splines. Two different conversion modes are supported, depending on the desired output: - *Edges: Turns each string of connected mesh edges into a poly spline. Whenever two or more edge strings intersect, they will be split into separate splines. - Faces: Creates a cyclic spline from each mesh face. This mode is generally much faster than Edges*, as it parallelizes easily and can share face and corner attributes without needing to copy them. Loose vertices are ignored – they will not be turned into single-point splines. Attributes, both named and unnamed ones, are transferred to the resulting splines. If there is a `radius` attribute, it will be applied as such, although you may find it more convenient to use the Set Curve Radius Node for this.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)

### Mesh Boolean — `GeometryNodeMeshBoolean`
- **Notes:** The Mesh Boolean Node allows you to cut, subtract, and join the geometry of two inputs. This node offers the same operations as the Boolean modifier.
- **Inputs:**
  - `Mesh 1` (`GEOMETRY`)
  - `Mesh 2` (`GEOMETRY`)
  - `Self Intersection` (`BOOLEAN`)
  - `Hole Tolerant` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `Intersecting Edges` (`BOOLEAN`)
- **Properties:**
  - `operation` (INTERSECT, UNION, DIFFERENCE) — INTERSECT: Keep the part of the mesh that is common between all operands; UNION: Combine meshes in an additive way; DIFFERENCE: Combine meshes in a subtractive way
  - `solver` (EXACT, FLOAT, MANIFOLD) — EXACT: Slower solver with the best results for coplanar faces; FLOAT: Simple solver with good performance, without support for overlapping geometry; MANIFOLD: Fastest solver that works only on manifold meshes but gives better results

### Mesh to Density Grid — `GeometryNodeMeshToDensityGrid`
- **Notes:** The Mesh to Density Grid node converts a mesh into a *density grid*, where each voxel stores a scalar value representing how far it lies inside or near the surface of the mesh. This can be used to generate fog volumes, soft-body representations, or as input to volumetric and field-based effects. The resulting grid contains smooth gradients that transition from high values inside the mesh to low values outside, allowing for continuous blending and sampling operations.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Density` (`FLOAT`)
  - `Voxel Size` (`FLOAT`)
  - `Gradient Width` (`FLOAT`)
- **Outputs:**
  - `Density Grid` (`FLOAT`)

### Mesh to Points — `GeometryNodeMeshToPoints`
- **Notes:** The Mesh to Points node generates a point cloud from a mesh.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Position` (`VECTOR`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)

### Mesh to SDF Grid — `GeometryNodeMeshToSDFGrid`
- **Notes:** The Mesh to SDF Grid node converts a mesh into a Signed Distance Field (SDF) grid. Each voxel in the resulting grid stores the shortest distance to the surface of the mesh, with the sign indicating whether the voxel is inside or outside the mesh. Positive values represent distances outside the mesh, negative values represent distances inside the mesh, and zero corresponds to the mesh surface. SDF grids are useful for many applications, including surface reconstruction, collision detection, morphing, and volumetric modeling.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Voxel Size` (`FLOAT`)
  - `Band Width` (`INT`)
- **Outputs:**
  - `SDF Grid` (`FLOAT`)

### Mesh to Volume — `GeometryNodeMeshToVolume`
- **Notes:** The Mesh to Volume node creates a fog volumes based on the shape of a mesh. The volume is created with a grid of the name "density" .
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Density` (`FLOAT`)
  - `Resolution Mode` (`MENU: Amount, Size`)
  - `Voxel Size` (`FLOAT`)
  - `Voxel Amount` (`FLOAT`)
  - `Interior Band Width` (`FLOAT`)
- **Outputs:**
  - `Volume` (`GEOMETRY`)

### Offset Corner in Face — `GeometryNodeOffsetCornerInFace`
- **Notes:** Retrieves another corner in the same face as the input corner. This is like “rotating” the input corner around in its face. Conceptually the operation is similar to the Offset Point in Curve Node.
- **Inputs:**
  - `Corner Index` (`INT`)
  - `Offset` (`INT`)
- **Outputs:**
  - `Corner Index` (`INT`)

### Pack UV Islands — `GeometryNodeUVPackIslands`
- **Notes:** The Pack UV Islands Node scales islands of a UV map and moves them so they fill the UV space as much as possible.
- **Inputs:**
  - `UV` (`VECTOR`)
  - `Selection` (`BOOLEAN`)
  - `Margin` (`FLOAT`)
  - `Rotate` (`BOOLEAN`)
  - `Method` (`MENU: Bounding Box, Convex Hull, Exact Shape`)
- **Outputs:**
  - `UV` (`VECTOR`)
- **Tip:** The Pack Islands operator performs a similar operation in the UV editor.

### Sample Nearest Surface — `GeometryNodeSampleNearestSurface`
- **Notes:** The Sample Nearest Surface node finds values at the closest points on the surface of a source mesh geometry. Non-face attributes are interpolated across the surface. This node is similar to the Geometry Proximity Node, but it gives the value of any attribute at the closest surface point, not just its position.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Value` (`FLOAT`)
  - `Group ID` (`INT`)
  - `Sample Position` (`VECTOR`)
  - `Sample Group ID` (`INT`)
- **Outputs:**
  - `Value` (`FLOAT`)
  - `Is Valid` (`BOOLEAN`)
- **Tip:** Because the node samples the surface of a mesh rather than its edges or vertices, values from loose points and edges are ignored.

### Sample UV Surface — `GeometryNodeSampleUVSurface`
- **Notes:** The Sample UV Surface node finds values on a mesh’s surface at specific UV locations. Internally the process is a “reverse UV lookup” from a location in 2D space. The node then finds the face that corresponds to each UV coordinate, and the location within that face.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Value` (`FLOAT`)
  - `UV Map` (`VECTOR`)
  - `Sample UV` (`VECTOR`)
- **Outputs:**
  - `Value` (`FLOAT`)
  - `Is Valid` (`BOOLEAN`)
- **Tip:** Because of the node’s method of computation, the UV map should not have any overlapping faces. If the UV map is sampled at a location with no faces or overlapping faces, the node will output the default value for the data type, which is zeros for most types.

### Scale Elements — `GeometryNodeScaleElements`
- **Notes:** Scales the selected faces or edges, letting you specify a scaling factor and pivot point for each one. Connected faces/edges are scaled together using their average factor and pivot point.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Scale` (`FLOAT`)
  - `Center` (`VECTOR`)
  - `Scale Mode` (`MENU: Uniform, Single Axis`)
  - `Axis` (`VECTOR`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Example:** The node is useful when combined with the Extrude Mesh Node, especially in Individual mode where connected faces aren’t extruded together. Used with: Extrude Mesh.

### Set Face Set — `GeometryNodeToolSetFaceSet`
- **Notes:** The Set Face Set node controls which face set that faces are in. The input node for this data is the Face Set Node . Note: This node can only be used in the Tool context .
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Face Set` (`INT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
- **Warning:** This node can only be used in the Tool context.

### Set Mesh Normal — `GeometryNodeSetMeshNormal`
- **Notes:** The Set Mesh Normal node stores a normal vector for each mesh element. This can be used to control shading appearance and influence subsequent operations that rely on surface normals.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Remove Custom` (`BOOLEAN`)
  - `Edge Sharpness` (`BOOLEAN`)
  - `Face Sharpness` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Set Shade Smooth — `GeometryNodeSetShadeSmooth`
- **Notes:** The Set Shade Smooth node controls whether the mesh’s faces look smooth in the viewport and renders. The smooth status of both edges and faces can be controlled, corresponding to the `sharp_edge` and `sharp_face` attributes. The input node for this data is the Is Face Smooth Node.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Shade Smooth` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Split Edges — `GeometryNodeSplitEdges`
- **Notes:** Like the Edge Split Modifier, the Split Edges node splits and duplicates edges within a mesh, breaking ‘links’ between faces around those split edges.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
- **Tip:** Because of mesh topology requirements, sometimes more or fewer edges than are selected will be split.

### Subdivide Mesh — `GeometryNodeSubdivideMesh`
- **Notes:** The Subdivide Mesh node adds new faces to mesh geometry using a simple interpolation for deformation.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Level` (`INT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Subdivision Surface — `GeometryNodeSubdivisionSurface`
- **Notes:** The Subdivision Surface node adds new faces to mesh geometry using a Catmull-Clark subdivision method.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Level` (`INT`)
  - `Edge Crease` (`FLOAT`)
  - `Vertex Crease` (`FLOAT`)
  - `Limit Surface` (`BOOLEAN`)
  - `UV Smooth` (`MENU: None, Keep Corners, Keep Corners, Junctions, Keep Corners, Junctions, Concave, Keep Boundaries, All`)
  - `Boundary Smooth` (`MENU: Keep Corners, All`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Triangulate — `GeometryNodeTriangulate`
- **Notes:** The Triangulate node converts all faces in a mesh (quads and n-gons) to triangular faces. It functions the same as the Triangulate tool in Edit Mode.
- **Inputs:**
  - `Mesh` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Quad Method` (`MENU: Beauty, Fixed, Fixed Alternate, Shortest Diagonal, Longest Diagonal`)
  - `N-gon Method` (`MENU: Beauty, Clip`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### UV Tangent — `GeometryNodeUVTangent`
- **Notes:** The UV Tangent node generates tangent direction vectors based on a specified UV map. Tangents are unit-length vectors that lie along the surface of the geometry and point in the direction of increasing U coordinates in the UV space. They are commonly used in shading and texturing workflows, for example in normal mapping or anisotropic effects. This node allows for either exact or approximate tangent computation, offering a balance between precision and performance depending on the use case.
- **Inputs:**
  - `Method` (`MENU: Exact, Fast`)
  - `UV` (`VECTOR`)
- **Outputs:**
  - `Tangent` (`VECTOR`)

### UV Unwrap — `GeometryNodeUVUnwrap`
- **Notes:** The UV Unwrap Node generates a UV map islands based on a selection of seam edges. The node implicitly performs a Pack Islands operation upon completion, because the results may not be generally useful otherwise.
- **Inputs:**
  - `Selection` (`BOOLEAN`)
  - `Seam` (`BOOLEAN`)
  - `Margin` (`FLOAT`)
  - `Fill Holes` (`BOOLEAN`)
  - `Method` (`MENU: Angle Based, Conformal`)
- **Outputs:**
  - `UV` (`VECTOR`)
- **Tip:** The Unwrap operator performs a similar operation in the UV editor. Unlike the Unwrap operator, the node doesn’t perform aspect ratio correction, because it is trivial to implement with a Vector Math Node.
- **Warning:** In order for Blender to recognize the created attribute as a UV map, it must be created with the Store Named Attribute Node on the Face Corner domain with the 2D Vector data type. This is necessary because there is no 2D Vector socket type.

### Vertex of Corner — `GeometryNodeVertexOfCorner`
- **Notes:** Outputs the index of the vertex that a face corner is attached to.
- **Inputs:**
  - `Corner Index` (`INT`)
- **Outputs:**
  - `Vertex Index` (`INT`)

