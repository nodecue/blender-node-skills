---
title: Instances
section: instances
description: "Instance Nodes: Create, transform, and realize instanced geometry workflows."
tags: instance, instances
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Instances

Reference nodes for `Instances`. Total: **12** nodes.

### Instance Bounds — `GeometryNodeInputInstanceBounds`
- **Notes:** The Instance Bounds node outputs the axis-aligned bounding box of each instance in the input geometry. This can be used to determine the spatial extent of instances, for example, to position or scale objects based on their size.
- **Inputs:**
  - `Use Radius` (`BOOLEAN`)
- **Outputs:**
  - `Min` (`VECTOR`)
  - `Max` (`VECTOR`)
- **Warning:** Only top-level instances are considered; the bounds do not include nested instances inside the instance geometry. This avoids the performance cost of realizing nested instances for accurate bounds. See Nested Instancing for more information.


### Instance on Points — `GeometryNodeInstanceOnPoints`
- **Notes:** The Instance on Points node adds a reference to a geometry to each of the points present in the input geometry. Instances are a fast way to add the same geometry to a scene many times without duplicating the underlying data. The node works on any geometry type with a Point domain, including meshes, point clouds, and curve control points. Any attributes on the points from the Geometry input will be available on the instance domain of the generated instances.
- **Inputs:**
  - `Points` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Instance` (`GEOMETRY`)
  - `Pick Instance` (`BOOLEAN`)
  - `Instance Index` (`INT`)
  - `Rotation` (`ROTATION`)
  - `Scale` (`VECTOR`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)
- **Example:** Vertex-to-instance visualization — Feed mesh geometry into Instance on Points with a small Ico Sphere as the Instance input. Each vertex gets a visible sphere placed on it. Useful for debugging vertex positions, visualizing point distributions, and understanding mesh topology.
- **Tip:** The Make Instances Real operator can be used to create objects from instances generated with this node.
- **Warning:** To instance object types that do not contain geometry, like a light object, the Object Info Node can be used. Other objects like Metaball objects are not supported for instancing.


### Instance Reference — `GeometryNodeInputInstanceReference`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Output the reference (instanced data) of each instance for grouping or switching per source.
- **Inputs:** None
- **Outputs:**
  - `Reference Index` (`INT`)


### Instance Rotation — `GeometryNodeInputInstanceRotation`
- **Notes:** The Instance Rotation outputs the XYZ Euler rotation of each top-level instance in the local space of the modifier object. The Instances page contains more information about geometry instances.
- **Inputs:** None
- **Outputs:**
  - `Rotation` (`ROTATION`)
- **Tip:** Though rotations are often displayed in units of degrees in the spreadsheet or node editor, they are stored internally in radians, so this node outputs radians.


### Instance Scale — `GeometryNodeInputInstanceScale`
- **Notes:** The Instance Scale outputs the size of top-level instances on each axis in the local space of the modifier object. The Instances page contains more information about geometry instances.
- **Inputs:** None
- **Outputs:**
  - `Scale` (`VECTOR`)


### Instance Transform — `GeometryNodeInstanceTransform`
- **Notes:** The Instance Transform outputs the Transformation Matrix of each top-level instance in the local space of the modifier object. The Instances page contains more information about geometry instances.
- **Inputs:** None
- **Outputs:**
  - `Transform` (`MATRIX`)


### Instances to Points — `GeometryNodeInstancesToPoints`
- **Notes:** The Instances to Points node generates points at the origins of top-level instances. Attributes on the instance domain are moved to the point cloud points.
- **Inputs:**
  - `Instances` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Position` (`VECTOR`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)
- **Tip:** Top-level instances are those that are owned by the node’s input geometry. Instances owned by other instances, i.e. nested instances, are not considered by this node.


### Realize Instances — `GeometryNodeRealizeInstances`
- **Notes:** The Realize Instances node makes any instances (efficient duplicates of the same geometry) into real geometry data. This makes it possible to affect each instance individually, whereas without this node, the exact same changes are applied to every instance of the same geometry. However, performance can become much worse when the input contains many instances of complex geometry, which is a fundamental limitation when procedurally processing geometry.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Realize All` (`BOOLEAN`)
  - `Depth` (`INT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Tip:** If the input contains multiple volume instances, only the first volume component is moved to the output.
- **Tip:** The `id` attribute receives special handling to prevent duplicate values. `id` values or indices of each instance are combined with `id` values from the geometry data points. - Vertex groups are preserved when realizing instances or joining geometries. If the domain and type propagation rules above result with the vertex domain and float type, then an attribute will be a vertex group on the output mesh.


### Rotate Instances — `GeometryNodeRotateInstances`
- **Notes:** The Rotate Instances node rotates geometry instances in local or global space. The Instances page contains more information about geometry instances.
- **Inputs:**
  - `Instances` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Rotation` (`ROTATION`)
  - `Pivot Point` (`VECTOR`)
  - `Local Space` (`BOOLEAN`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)


### Scale Instances — `GeometryNodeScaleInstances`
- **Notes:** The Scale Instances node scales geometry instances in local or global space. The Instances page contains more information about geometry instances.
- **Inputs:**
  - `Instances` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Scale` (`VECTOR`)
  - `Center` (`VECTOR`)
  - `Local Space` (`BOOLEAN`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)


### Set Instance Transform — `GeometryNodeSetInstanceTransform`
- **Notes:** The Set Instance Transform node Transforms geometry instances using a Transformation Matrix . The Instances page contains more information about geometry instances.
- **Inputs:**
  - `Instances` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Transform` (`MATRIX`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)


### Translate Instances — `GeometryNodeTranslateInstances`
- **Notes:** The Translate Instances node moves top-level geometry instances in local or global space. The Instances page contains more information about geometry instances.
- **Inputs:**
  - `Instances` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Translation` (`VECTOR`)
  - `Local Space` (`BOOLEAN`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)
