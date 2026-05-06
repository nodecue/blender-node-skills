---
title: Geometry Read
section: geometry
description: "Geometry Nodes (Read): Read geometry state, identity, and context-dependent geometry fields."
tags: geometry, group, id, index, material, normal, read
---

## Geometry Read

Reference nodes for `Geometry Read`. Total: **24** nodes.

### Active Element — `GeometryNodeToolActiveElement`
- **Notes:** The Active Element node outputs the index of the Active point, edge, face, or layer. Note: This node can only be used in the Tool context .
- **Inputs:** None
- **Outputs:**
  - `Index` (`INT`)
  - `Exists` (`BOOLEAN`)
- **Warning:** This node can only be used in the Tool context.

### Geometry Proximity — `GeometryNodeProximity`
- **Notes:** The Geometry Proximity node computes the closest location on the target geometry.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Group ID` (`INT`)
  - `Sample Position` (`VECTOR`)
  - `Sample Group ID` (`INT`)
- **Outputs:**
  - `Position` (`VECTOR`)
  - `Distance` (`FLOAT`)
  - `Is Valid` (`BOOLEAN`)
- **Example:** Proximity-based selection — Feed reference objects (via Collection Info → Instances to Points) into Geometry Proximity's Geometry input. The Distance output → Compare(LESS_THAN, radius) creates a boolean selection for elements near the reference points. Useful for local effects, proximity masks, and object-driven selections.
- **Tip:** The Map Range Node is often helpful to use with the distance output of this node to create a falloff with a maximum distance.

### Geometry to Instance — `GeometryNodeGeometryToInstance`
- **Notes:** The Geometry to Instance node turns every connected input geometry into an instance. Visually, the node has a similar result as the Join Geometry Node, but it outputs the result as separate instances instead. The geometry data itself isn’t actually joined. The node can be used in combination with the Pick Instances option in the Instance on Points Node, as a way to pick between geometry generated in the node tree (as opposed to picking from separate instances from the Collection Info Node, for example).
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)
- **Example:** The node used in combination with the Instance on Points Node to choose between multiple primitives for instancing. Used with: Instance on Points.
- **Warning:** This node can be much faster than the join geometry node when the inputs are large geometries. This is because the join geometry node must actually create a larger mesh, or a larger curve. Even though the operation is simple, just creating a large mesh can have a significant cost. This node can be better, because instead of merging large geometries, it just groups them together as instances.

### Group Input — `NodeGroupInput`
- **Notes:** Expose connected data from inside a node group as inputs to its interface.
- **Inputs:** None
- **Outputs:**
  - `Unnamed` (`CUSTOM`)

### Group Output — `NodeGroupOutput`
- **Notes:** Output data from inside of a node group.
- **Inputs:**
  - `Unnamed` (`CUSTOM`)
- **Outputs:** None

### ID — `GeometryNodeInputID`
- **Notes:** The ID node gives an integer value indicating the stable random identifier of each element on the point domain, which is stored in the `id` attribute. The node to set this data is the Set ID Node node.
- **Inputs:** None
- **Outputs:**
  - `ID` (`INT`)
- **Warning:** Unlike other built-in attributes, the `id` attribute does not always exist. In that case, this node will output the index.

### Index — `GeometryNodeInputIndex`
- **Notes:** The Index node gives an integer value indicating the position of each element in the list, starting at zero. This depends on the internal order of the data in the geometry, which is not necessarily visible in the 3D Viewport. However, the index value is visible in the left-most column in the Spreadsheet Editor.
- **Inputs:** None
- **Outputs:**
  - `Index` (`INT`)
- **Example:** Grid row/column selection — For a Grid with known width W: Index → Math(MODULO, W) → Compare(EQUAL, column) selects a column; Index → Math(DIVIDE, W) → Math(FLOOR) → Compare(EQUAL, row) selects a row. Useful for checkerboard patterns, stripe effects, and grid-based procedural selections.
- **Warning:** Indices in geometry data are often defined by the internals of complex algorithms that create it. If no inputs change, indices will be the same when the same node tree is executed multiple times. However, they may not be predictable when inputs to nodes that generate geometry or change its topology are adjusted. Additionally, updates to algorithms in newer versions of Blender may change the order of generated elements. To avoid relying on consistent indices, it is recommended to calculate them locally, or to avoid operations that change topology when they must be consistent over time.

### Index of Nearest — `GeometryNodeIndexOfNearest`
- **Notes:** The *Index of Nearest* node is a way to find other close elements in the same geometry. If needed you can use Group ID to determine the group of neighbors to be analyzed together. This is an alternative to the Sample Nearest Node node. The main difference is that this node does not require a geometry input, because the geometry from the field context is used.
- **Inputs:**
  - `Position` (`VECTOR`)
  - `Group ID` (`INT`)
- **Outputs:**
  - `Index` (`INT`)
  - `Has Neighbor` (`BOOLEAN`)
- **Tip:** This is often combined with the Evaluate at Index Node or the Sample Index Node node.

### Material Index — `GeometryNodeInputMaterialIndex`
- **Notes:** The Material Index node outputs which material in the list of materials of the geometry each element corresponds to. Currently the node supports mesh data, where `material_index` is a built-in attribute on faces. The node to set this data is the Set Material Index node.
- **Inputs:** None
- **Outputs:**
  - `Material Index` (`INT`)

### Material Selection — `GeometryNodeMaterialSelection`
- **Notes:** The Material Selection node provides a selection for meshes that use this material. Since the `material_index` is stored on each face, the output will be implicitly interpolated to a different domain when necessary. For example, every vertex connected to a selected face will be selected.
- **Inputs:**
  - `Material` (`MATERIAL`)
- **Outputs:**
  - `Selection` (`BOOLEAN`)

### Named Attribute — `GeometryNodeInputNamedAttribute`
- **Notes:** The Named Attribute node outputs the data of an attribute based on the context of where it is connected (the Field Context ).
- **Inputs:**
  - `Name` (`STRING`)
- **Outputs:**
  - `Attribute` (`FLOAT`)
  - `Exists` (`BOOLEAN`)

### Normal — `GeometryNodeInputNormal`
- **Notes:** The Normal node returns a vector for each evaluated point indicating the normal direction. The output can depend on the attribute domain used in the node evaluating the field, but the output is always a normalized unit vector. - *Face: On the face domain, the normal is the “up” direction of the face. - Mesh Vertices: For mesh vertices, the normal is an average of the surrounding face normals. If the vertex does not have any connected faces, the output is simply the normalized position of that vertex. - Edge: The normal output for each edge is the average of the edge’s two vertex normals. - Face Corner: The output for each face corner is the same as the face normal of the corresponding face. - Curve Control Points:* The output of this node when used for curve geometry is the evaluated normal of the curve, which depends on the twist method. The normal vector is always perpendicular to the direction of the curve’s path at every point.
- **Inputs:** None
- **Outputs:**
  - `Normal` (`VECTOR`)
  - `True Normal` (`VECTOR`)
- **Tip:** For NURBS and Bézier spline curves, keep in mind that the value retrieved from this node is the value at every control point, which may not correspond to the visible evaluated points. For NURBS splines the difference may be even more pronounced and the result may not be as expected. A Resample Curve Node can be used to create a poly spline, where there is a control point for every evaluated point.

### Position — `GeometryNodeInputPosition`
- **Notes:** The Position node outputs a vector of each point of the geometry the node is connected to. The node can work on geometry domains besides points. In that case, the position data will be automatically interpolated to the new domain. For example, when used as part of the input to the Split Edges Node, the position for each edge will be the average position of the edge’s two vertices. For instances themselves, the output is the origin of each instance. However, if the node is for a geometry node that adjusts data inside instances, the position output of this node will be in the local space of each instance. See the Instance Processing page for more details.
- **Inputs:** None
- **Outputs:**
  - `Position` (`VECTOR`)

### Radius — `GeometryNodeInputRadius`
- **Notes:** The Radius node outputs the radius value at each point on the evaluated geometry. For curves, this value is used for things like determining the size of the mesh created in the Curve to Mesh node. For point clouds, the value is used for the display size of the point in the viewport.
- **Inputs:** None
- **Outputs:**
  - `Radius` (`FLOAT`)

### Raycast — `GeometryNodeRaycast`
- **Notes:** The Raycast node intersects rays from one geometry onto another. The source geometry is defined by the context of the node that the Raycast node is connected to. Each ray computes hit points on the target mesh and outputs normals, distances and any surface attribute specified.
- **Inputs:**
  - `Target Geometry` (`GEOMETRY`)
  - `Attribute` (`FLOAT`)
  - `Interpolation` (`MENU: Interpolated, Nearest`)
  - `Source Position` (`VECTOR`)
  - `Ray Direction` (`VECTOR`)
  - `Ray Length` (`FLOAT`)
- **Outputs:**
  - `Is Hit` (`BOOLEAN`)
  - `Hit Position` (`VECTOR`)
  - `Hit Normal` (`VECTOR`)
  - `Hit Distance` (`FLOAT`)
  - `Attribute` (`FLOAT`)

### Replace Material — `GeometryNodeReplaceMaterial`
- **Notes:** The Replace Material node swaps one material with another. Replacing a material with this node is more efficient than creating a selection of all faces with the old material with the Material Selection Node and then using the Set Material Node.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Old` (`MATERIAL`)
  - `New` (`MATERIAL`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Tip:** Currently this node only adjusts mesh data.

### Sample Index — `GeometryNodeSampleIndex`
- **Notes:** The Sample Index node retrieves values from a source geometry at a specific index.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Value` (`FLOAT`)
  - `Index` (`INT`)
- **Outputs:**
  - `Value` (`FLOAT`)
- **Example:** Here the node is used to copy the positions of one object to another. Used with: Topology.
- **Tip:** If the Geometry used for the input is the same as the geometry from the field context, this node is equivalent to the Evaluate at Index Node. Using that node is usually preferable since avoiding the geometry socket makes the whole setup easier to use in other situations and share.
- **Tip:** Different components can have same attribute domain (Points). This node simply uses first component that not empty for such domain, checked in the order of: Mesh, Point Cloud, Curve. The Separate Components Node can be used to sample directly from a specific component.

### Sample Nearest — `GeometryNodeSampleNearest`
- **Notes:** The Sample Nearest node retrieves the index of the geometry element in its input geometry that is closest to the input position. This node is similar to the Geometry Proximity Node, but it outputs the index of the closest element instead of its distance from the current location.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Sample Position` (`VECTOR`)
- **Outputs:**
  - `Index` (`INT`)
- **Example:** Combining this node with the Sample Index Node gives a setup that can retrieve the closest attribute value from another geometry. Used with: Sample Index.
- **Tip:** If you want to find nearest to each point in same geometry, its better to use the Index of Nearest node.

### Selection — `GeometryNodeToolSelection`
- **Notes:** The Selection node outputs true for geometry that is selected, and false elsewhere. The corresponding data flow node is the Set Selection Node.
- **Inputs:** None
- **Outputs:**
  - `Boolean` (`BOOLEAN`)
  - `Float` (`FLOAT`)
- **Warning:** This node can only be used in the Tool context.

### Set Geometry Name — `GeometryNodeSetGeometryName`
- **Notes:** The Set Geometry Name node stores a custom name on the geometry, overriding the name which might come from the Object Info Node or a Grease Pencil to Curves Node. The name is displayed in the spreadsheet and can helpful for debugging purposes.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Name` (`STRING`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)

### Set ID — `GeometryNodeSetID`
- **Notes:** The Set ID node fills the `id` attribute on the input geometry. If the attribute does not exist yet, it will be created with a default value of zero. The ID is also created by the Distribute Points on Faces, and it is used in the Random Value Node and other nodes if it exists. The input node for this data is the ID Node.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `ID` (`INT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)

### Set Material — `GeometryNodeSetMaterial`
- **Notes:** The Set Material changes the material assignment in the specified selection, by adjusting the `material_index` attribute. If the material is already used on the geometry, the existing material index will be reused.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Material` (`MATERIAL`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Warning:** This node adjusts mesh, point clouds, and volume data; other data types do not support materials.

### Set Material Index — `GeometryNodeSetMaterialIndex`
- **Notes:** The Set Material Index node sets the material index for a geometry. The node to get this data is the Material Index node.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Material Index` (`INT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)

### Set Selection — `GeometryNodeToolSetSelection`
- **Notes:** The Set Selection node controls which geometry is selected . The input node for this data is the Selection Node . Note: This node can only be used in the Tool context .
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Warning:** This node can only be used in the Tool context.

