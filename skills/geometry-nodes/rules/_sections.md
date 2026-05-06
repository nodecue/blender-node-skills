## 1. Geometry Core (geometry)

Geometry read/write/transform operations — the trunk of every node tree.

## 2. Mesh (mesh)

Mesh primitives, topology reads, and mesh-specific operations (boolean, extrude, subdivide).

## 3. Curve (curve)

Curve primitives, reads, and operations (resample, trim, fill, to-mesh/points conversion).

## 4. Instances (instances)

Instance creation, transform, and realization. Core of scatter/array workflows.

## 5. Point (point)

Point distribution and point cloud operations. Bridge between mesh surfaces and instance placement.

## 6. Input (input)

Constant values, scene data, gizmos, and file imports that feed into the graph.

## 7. Utilities (utilities)

Math, vector, rotation, matrix, text, field, and misc helper nodes. The field-shaping layer.

## 8. Texture (texture)

Procedural and image texture nodes. Primary signal sources for field-driven workflows.

## 9. Attribute (attribute)

Capture, store, remove named attributes. Bridge between field computations and persistent data.

## 10. Volume (volume)

Volume/grid construction, sampling, and differential operators.

## 11. Color (color)

Color mixing and transformation nodes.

## 12. Simulation (simulation)

Simulation zone nodes for frame-to-frame state.

## 13. System (system)

Layout, zones, reroute, and tool support nodes.
