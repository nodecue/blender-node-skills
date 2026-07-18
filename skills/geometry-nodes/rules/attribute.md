---
title: Attribute
section: attribute
description: "Attribute Nodes: Read, capture, store, and manage geometry attributes across domains."
tags: attribute, blur, capture, domain
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Attribute

Reference nodes for `Attribute`. Total: **9** nodes.

### Attribute Statistic — `GeometryNodeAttributeStatistic`
- **Notes:** The Attribute Statistic node evaluates a field on a geometry and outputs a statistic about the entire data set.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Attribute` (`FLOAT`)
- **Outputs:**
  - `Mean` (`FLOAT`)
  - `Median` (`FLOAT`)
  - `Sum` (`FLOAT`)
  - `Min` (`FLOAT`)
  - `Max` (`FLOAT`)
  - `Range` (`FLOAT`)
  - `Standard Deviation` (`FLOAT`)
  - `Variance` (`FLOAT`)


### Blur Attribute — `GeometryNodeBlurAttribute`
- **Notes:** The Blur Attribute node smooths attribute values between neighboring geometry elements. The goal of each step is mixing values of each element with its neighbors. The weight for element is factor for multiplying all neighbor’s values before accumulating them as new primitive value. Blurring will only work with certain geometry types and attribute domains. Therefore, the attribute can only be affected on the Meshes and Curves components. The domains this node works on is based on the field context of the node’s evaluation. Only domains with explicit relations with their neighbors will work with this node. Explicit relations for correct blurring are vertices, edges, and faces of meshes, and curve control points. All attribute data types are supported except for boolean attributes.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Iterations` (`INT`)
  - `Weight` (`FLOAT`)
- **Outputs:**
  - `Value` (`FLOAT`)
- **Example:** Input is Mesh Plane. First Subdivide Mesh Node add some faces for capture color with Random Value Node used as hue in Combine Color Node on this. Used with: Subdivide Mesh, Random Value, Combine Color.
- **Tip:** Blurring of face corner attributes is not handled by this node, because the ideal behavior for mixing face corner values is not clear.


### Capture Attribute — `GeometryNodeCaptureAttribute`
- **Notes:** The Capture Attribute node stores one or more fields on a geometry, and outputs those same fields so they can be read by other nodes. This storing and retrieving of a field can also be done with the Store Named Attribute Node and the Named Attribute Node respectively. The difference is that the Capture Attribute node creates an anonymous attribute, meaning there’s no need to specify a name and there’s no clutter at the end. This makes the node ideal for temporary data storage. A common use case is saving information that would normally be lost while converting geometry – see the example below.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
- **Warning:** The new attribute is only available in the geometry produced by this node. It can’t be read in the geometry of “sibling” or “upstream” nodes.


### Domain Size — `GeometryNodeAttributeDomainSize`
- **Notes:** The Domain Size outputs the size of an attribute domain on the selected geometry type, for example, the number of edges in a mesh, or the number of points in a point cloud. For more information about attribute domains, see the geometry attributes page.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
- **Outputs:**
  - `Point Count` (`INT`)
  - `Edge Count` (`INT`)
  - `Face Count` (`INT`)
  - `Face Corner Count` (`INT`)
  - `Spline Count` (`INT`)
  - `Instance Count` (`INT`)
  - `Layer Count` (`INT`)


### Get Attribute Names — `GeometryNodeGetAttributeNames`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** List the attribute names present on geometry as a string list; consume with list nodes.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Filter Data Type` (`BOOLEAN`)
  - `Data Type` (`MENU`)
  - `Filter Domain` (`BOOLEAN`)
  - `Domain` (`MENU`)
- **Outputs:**
  - `Names` (`STRING`)


### Remove Named Attribute — `GeometryNodeRemoveAttribute`
- **Notes:** The Remove Named Attribute node deletes an attribute with a certain name from its geometry input. Any attribute that exists on geometry data will be automatically propagated when the geometry storing it is changed, which can be an expensive operation, so using this node can be a simple way to optimize the performance of a geometry node tree or even to lower the memory usage of the entire scene. Almost all named attributes can be removed. For certain Built-In Attributes, removing it will mean that a default value will be used instead. For example, removing the cyclic attribute on curves means that all curves will be non-cyclic.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Pattern Mode` (`MENU: Exact, Wildcard`)
  - `Name` (`STRING`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)


### Rename Attribute — `GeometryNodeRenameAttribute`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Rename an attribute on geometry without copying its data.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Mode` (`MENU`)
  - `Old` (`STRING`)
  - `New` (`STRING`)
  - `Overwrite` (`BOOLEAN`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)


### Store Named Attribute — `GeometryNodeStoreNamedAttribute`
- **Notes:** The Store Named Attribute node stores the result of a field on a geometry as an attribute with the specified name. If the attribute already exists, the data type and domain will be updated to the values chosen in the node. However, keep in mind that the domain and data type of Built-In Attributes cannot be changed. Compared with the Capture Attribute Node, this node basically does the same thing, but the attribute gets a name instead of an anonymous reference. For reusing the data in the same node tree, the Capture Attribute node might be preferable since it does not create the chance for name conflicts in the input geometry.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Name` (`STRING`)
  - `Value` (`FLOAT`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Example:** Multi-attribute mark/clear — Chain multiple Store Named Attribute nodes in series (Geometry output → next Geometry input) to write several boolean or value attributes in one pass. For example, store "pinned_edge" and "pinned_vertex" booleans on different domains so downstream tools can read either attribute with Named Attribute + Exists guard. Pair with Remove Named Attribute to clear attributes when toggling off.
- **Tip:** If the input geometry contains multiple geometry component types, the attribute will be created on each component that has the chosen domain.


### Transfer Attributes — `GeometryNodeTransferAttributes`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Transfer multiple attributes between geometries in one node using a shared mapping; wide input set, read sockets via live readback.
- **Inputs:**
  - `Target` (`GEOMETRY`)
  - `Target Point ID` (`INT`)
  - `Target Edge ID` (`INT`)
  - `Target Face ID` (`INT`)
  - `Target Corner ID` (`INT`)
  - `Target Curve ID` (`INT`)
  - `Target Instance ID` (`INT`)
  - `Source` (`GEOMETRY`)
  - `Source Point ID` (`INT`)
  - `Source Edge ID` (`INT`)
  - `Source Face ID` (`INT`)
  - `Source Corner ID` (`INT`)
  - `Source Curve ID` (`INT`)
  - `Source Instance ID` (`INT`)
  - `Pattern Mode` (`MENU`)
  - `Attribute Names` (`STRING`)
  - `Exclude Names` (`BOOLEAN`)
- **Outputs:**
  - `Target` (`GEOMETRY`)
  - `Transferred Names` (`STRING`)
