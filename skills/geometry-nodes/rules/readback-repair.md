---
title: Readback Repair
section: workflow
description: "Observable readback symptoms and repair rules for Geometry Nodes graph construction."
tags: readback, repair, socket, link, verify
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Readback Repair

Use this after each small edit slice. Repair only facts visible in Blender readback: nodes, links, socket names/identifiers, property values, interface sockets, and geometry output reachability.

## Evidence

- `rules/geometry-read.md`: `NodeGroupInput`, `NodeGroupOutput`, field/context nodes, material read nodes
- `rules/geometry-operations.md`: `GeometryNodeSetPosition`, `GeometryNodeDeleteGeometry`, `GeometryNodeSeparateGeometry`
- `rules/utilities-misc.md`: `GeometryNodeJoinGeometry`, `GeometryNodeSwitch`
- `rules/mesh-operations.md`: `GeometryNodeMeshBoolean`
- `rules/instances.md`: `GeometryNodeRealizeInstances`
- `rules/attribute.md`: `GeometryNodeCaptureAttribute`
- `rules/geometry-read.md`: `GeometryNodeInputNamedAttribute`
- Existing socket-server tests cover exact socket lookup, duplicate socket labels, socket default writes, property writes, and readback.

## Symptoms And Repairs

### `Group Output.Geometry` has no incoming link

- Check whether the graph is Process or Generate mode.
- Connect the intended geometry result to the actual `Group Output` node's `Geometry` input.
- If multiple branches should survive, join or switch them with a real composition node before `Group Output`.

### A field chain exists but the viewport does not change

- Find the field producer's downstream consumer.
- Wire it into a concrete consuming socket such as `Selection`, `Offset`, `Scale`, `Density Factor`, or `Material Index`.
- If there is no consumer, remove the unused field chain or finish the intended connection.

### A write operation reports success but readback is unchanged

- Confirm whether the target is a socket default or a node RNA property.
- Retry against exactly one target: socket default by socket name/identifier, or property by property identifier.
- Do not silently fall back between socket defaults and node properties.

### A later action cannot find a node created earlier

- Blender may rename duplicate nodes with suffixes such as `.001`.
- Use the node name returned by the create/readback result for all later links and writes.

### A socket label appears more than once

- Use the socket identifier from readback when labels are duplicated.
- If a node has repeat/multi-input sockets, read the sockets again after each link because Blender may expose another input.

### Join Geometry gives a result but topology is wrong

- `GeometryNodeJoinGeometry` preserves separate geometry components in one output.
- If the prompt needs a fused mesh surface, use a mesh operation such as `GeometryNodeMeshBoolean` where appropriate.
- If the prompt needs alternatives, use `GeometryNodeSwitch` instead of joining both branches.

### Instance edits do not affect individual copies

- Check whether the operation is being applied before or after instancing.
- Preserve instances for performance when no unique per-copy mesh edit is needed.
- Add `GeometryNodeRealizeInstances` only when downstream operations require real geometry data.

### Captured or stored data is missing downstream

- For `GeometryNodeCaptureAttribute`, use the geometry output from the capture node; sibling/upstream geometry paths do not carry that anonymous attribute.
- For named attributes, check `GeometryNodeInputNamedAttribute.Exists` before relying on the value.
