---
title: Geometry Operations
section: geometry
description: "Geometry Nodes (Operations): Core geometry-level transforms, separation, deletion, and sorting."
tags: bake, bounding, convex, delete, geometry, operations
blender_support: "5.0+"
blender_verified: 5.1.1, 5.2.0
last_verified: "2026-07-18"
---

## Geometry Operations

Reference nodes for `Geometry Operations`. Total: **14** nodes.

### Bake — `GeometryNodeBake`
- **Notes:** The Bake node allows saving and loading intermediate geometries. This node bakes parts of the node tree for better performance. The data format used to store geometry data is not considered to be an import/export format. Volume objects, however, are saved using the OpenVDB file format which can be used interoperably.
- **Inputs:**
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Unnamed` (`CUSTOM`)
- **Tip:** It’s not guaranteed that data written with one Blender version can be read by another Blender version.


### Bounding Box — `GeometryNodeBoundBox`
- **Notes:** The Bounding Box node creates a box mesh with the minimum volume that encapsulates the geometry of the input. The node also can output the vector positions of the bounding dimensions. The mesh output and the Min and Max outputs do not take instances into account. Instead, for instanced geometry, a bounding box is computed for each instance rather than the whole geometry. To compute the bounding box including the instances, a Realize Instances Node can be used.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Use Radius` (`BOOLEAN`)
- **Outputs:**
  - `Bounding Box` (`GEOMETRY`)
  - `Min` (`VECTOR`)
  - `Max` (`VECTOR`)


### Convex Hull — `GeometryNodeConvexHull`
- **Notes:** The Convex Hull node outputs a convex mesh that is enclosing all points in the input geometry.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
- **Outputs:**
  - `Convex Hull` (`GEOMETRY`)
- **Tip:** When the node is used on a geometry with instances, the algorithm will run once per instance, resulting in many convex hull meshes in the instance geometries. The Realize Instances node can be used to get a convex hull of an entire geometry.
- **Warning:** Volumes are not supported by this node, and attributes are not automatically transferred to the result.
- **Tip:** This node is affected by the limitations of floating point precision. If points are too close together, they may be merged in the result mesh.


### Delete Geometry — `GeometryNodeDeleteGeometry`
- **Notes:** The Delete Geometry node removes the selected part of a geometry. It behaves similarly to the Delete tool in Edit Mode. The type of elements to be deleted can be specified with the domain and mode properties.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Example:** Probabilistic thinning — Random Value node (min 0, max 1) output to Compare node (LESS_THAN, threshold from mask) output to Delete Geometry `Selection` input. Mask can be a constant, noise texture, or painted weight. Elements where random value exceeds the mask are deleted.
- **Properties:**
  - `mode` (ALL, EDGE_FACE, ONLY_FACE)


### Is Edge Smooth — `GeometryNodeInputEdgeSmooth`
- **Notes:** The Is Edge Smooth node outputs true for each edge of the mesh that is not marked as sharp. Otherwise, if the edge is marked as sharp, then the node outputs false.
- **Inputs:** None
- **Outputs:**
  - `Smooth` (`BOOLEAN`)


### Merge by Distance — `GeometryNodeMergeByDistance`
- **Notes:** The Merge by Distance node merges selected mesh vertices or point cloud points within a given distance, merging surrounding geometry where necessary. This operation is similar to the Merge by Distance operator or the Weld Modifier.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Mode` (`MENU: All, Connected`)
  - `Distance` (`FLOAT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Example:** Using the selection input to only merge some of the points in a point cloud.


### Merge Points — `GeometryNodeMergePoints`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Merge points that lie within a distance threshold.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Merge ID` (`INT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)


### Separate Components — `GeometryNodeSeparateComponents`
- **Notes:** The Separate Components node splits a geometry into a separate output for each type of data in the geometry.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
  - `Curve` (`GEOMETRY`)
  - `Grease Pencil` (`GEOMETRY`)
  - `Point Cloud` (`GEOMETRY`)
  - `Volume` (`GEOMETRY`)
  - `Instances` (`GEOMETRY`)


### Separate Geometry — `GeometryNodeSeparateGeometry`
- **Notes:** The Separate Geometry node produces two geometry outputs. Based on the Selection input, the input geometry is split between the two outputs.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Selection` (`GEOMETRY`)
  - `Inverted` (`GEOMETRY`)
- **Tip:** This node can be combined with the Compare Node for a more precise control of which parts are separated to a given output geometry.


### Set Geometry Bundle — `GeometryNodeSetGeometryBundle`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Attach a bundle to geometry. In 5.2 a geometry can carry an attached bundle alongside components and attributes.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Bundle` (`BUNDLE`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)


### Set Position — `GeometryNodeSetPosition`
- **Notes:** The Set Position node controls the location of each point, the same way as controlling the `position` attribute. If the input geometry contains instances, this node will affect the location of the origin of each instance. The input node for this data is the Position Node.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Position` (`VECTOR`)
  - `Offset` (`VECTOR`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)


### Sort Elements — `GeometryNodeSortElements`
- **Notes:** The Sort Elements node rearranges geometry elements by changing their indices.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Group ID` (`INT`)
  - `Sort Weight` (`FLOAT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)


### Split to Instances — `GeometryNodeSplitToInstances`
- **Notes:** Splits a selection of geometry elements (such as faces) into groups, then turns each group into an instance.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Group ID` (`INT`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)
  - `Group ID` (`INT`)
- **Example:** In the example above, we start with a grid of 1000x1000 square faces serving as “pixels.” Then, we group these faces into patches by assigning them a group ID sampled from a Voronoi texture, and move each resulting instance by a random amount along the Z axis.
- **Tip:** Geometry that doesn’t match the selected domain will be removed. For example, if you choose Edge, any faces, splines, and instances in the input geometry will be lost.


### Transform Geometry — `GeometryNodeTransform`
- **Notes:** The Transform Geometry Node allows you to move, rotate or scale the geometry. The transformation is applied to the entire geometry, and not per element. The Set Position Node is used for moving individual points of a geometry. For transforming instances individually, the instance translate, rotate, or scale nodes can be used.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Mode` (`MENU: Components, Matrix`)
  - `Translation` (`VECTOR`)
  - `Rotation` (`ROTATION`)
  - `Scale` (`VECTOR`)
  - `Transform` (`MATRIX`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
