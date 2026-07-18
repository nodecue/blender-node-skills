---
title: Node Role Catalog
section: workflow
description: "Evidence-backed candidate node roles for open-ended Geometry Nodes planning."
tags: role, planning, candidate, readback
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Node Role Catalog

Use this catalog to choose candidate nodes by role. It does not prescribe a single graph for a prompt; it narrows the search to nodes already covered by local rules and the knowledge base.

## Evidence

- `rules/geometry-read.md`: `NodeGroupInput`, `NodeGroupOutput`, `GeometryNodeInputPosition`, `GeometryNodeInputNormal`, `GeometryNodeInputNamedAttribute`, `GeometryNodeInputMaterialIndex`, `GeometryNodeGeometryToInstance`
- `rules/geometry-operations.md`: `GeometryNodeSetPosition`, `GeometryNodeTransform`, `GeometryNodeDeleteGeometry`, `GeometryNodeSeparateGeometry`
- `rules/point.md`: `GeometryNodeDistributePointsOnFaces`, `GeometryNodeDistributePointsInVolume`
- `rules/curve-operations.md`: `GeometryNodeCurveToPoints`
- `rules/mesh-operations.md`: `GeometryNodeMeshToPoints`, `GeometryNodeMeshBoolean`
- `rules/instances.md`: `GeometryNodeInstanceOnPoints`, `GeometryNodeRealizeInstances`
- `rules/attribute.md`: `GeometryNodeCaptureAttribute`, `GeometryNodeStoreNamedAttribute`
- `rules/texture.md`: `ShaderNodeTexNoise`, `ShaderNodeTexVoronoi`, `ShaderNodeTexGradient`
- `rules/utilities-math.md`: `FunctionNodeCompare`, `ShaderNodeMapRange`, `ShaderNodeMath`
- `rules/utilities-vector.md`: `ShaderNodeVectorMath`, `ShaderNodeCombineXYZ`
- `rules/utilities-misc.md`: `GeometryNodeJoinGeometry`, `GeometryNodeSwitch`, `FunctionNodeRandomValue`

## Geometry Sources

- `NodeGroupInput`: use when the user wants to process the modifier object's existing geometry.
- Mesh and curve primitives from the primitive rule files: use when the user wants generated geometry.
- `GeometryNodeGroup`: use only after reading the group's actual interface sockets.
- Common misuse: connecting generated geometry and `Group Input.Geometry` in parallel without a real composition node.

## Field Producers

- `GeometryNodeInputPosition`: spatial gradients, masks, and coordinate-driven deformation.
- `GeometryNodeInputNormal`: surface direction for displacement or orientation.
- `GeometryNodeInputIndex`: ordered per-element variation when element order is acceptable.
- `FunctionNodeRandomValue`: per-element random float, vector, integer, or boolean values.
- `ShaderNodeTexNoise`, `ShaderNodeTexVoronoi`, `ShaderNodeTexGradient`: procedural float/color fields.
- `GeometryNodeInputNamedAttribute`, `GeometryNodeInputMaterialIndex`: read existing stored data.
- Common misuse: leaving a producer unconnected to a consuming socket.

## Field Shapers

- `FunctionNodeCompare`: convert numeric/vector conditions to boolean selections.
- `ShaderNodeMapRange`: remap a float range before it drives a socket.
- `ShaderNodeMath`: scalar arithmetic and clamping.
- `ShaderNodeVectorMath`: vector scaling, projection, normalization, and composition math.
- `ShaderNodeCombineXYZ`: assemble a vector from scalar axes.
- Common misuse: sending a float mask to a boolean selection without an explicit comparison when a hard selection is required.

## Geometry Consumers

- `GeometryNodeSetPosition`: consumes vector fields through `Position` or `Offset` to move points.
- `GeometryNodeDeleteGeometry`, `GeometryNodeSeparateGeometry`: consume boolean `Selection` fields.
- `GeometryNodeSetMaterial`, `GeometryNodeSetMaterialIndex`: consume selection/material fields on supported geometry types.
- `GeometryNodeDistributePointsOnFaces`: consumes `Selection` and `Density Factor` for surface point distribution.
- `GeometryNodeInstanceOnPoints`: consumes point geometry and optional per-instance `Selection`, `Rotation`, `Scale`, and `Instance Index`.
- Common misuse: building a field chain but never wiring it into one of these consumers.

## Composition Nodes

- `GeometryNodeJoinGeometry`: keep multiple geometry branches in one output without fusing surfaces.
- `GeometryNodeSwitch`: choose one geometry/value path from alternatives.
- `GeometryNodeMeshBoolean`: use when mesh surfaces must be combined by boolean operation.
- `GeometryNodeGeometryToInstance`: group multiple inputs as instances rather than joined geometry.
- `GeometryNodeRealizeInstances`: convert instances to real geometry only when downstream operations need unique mesh data.
- Common misuse: using Join Geometry when a boolean surface operation is required, or realizing instances before it is necessary.

## Attribute Handoff

- `GeometryNodeCaptureAttribute`: temporary anonymous data for use later in the same geometry flow.
- `GeometryNodeStoreNamedAttribute`: named data for later reading by name.
- `GeometryNodeInputNamedAttribute`: read a named attribute and check whether it exists.
- Common misuse: reading from an upstream or sibling geometry path that never received the captured/stored attribute.
