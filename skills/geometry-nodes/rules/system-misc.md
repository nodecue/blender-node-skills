---
title: System Misc
section: system
description: "System Nodes: Node-tree structure, zones, layout helpers, and system-level support nodes."
tags: boolean, curve, integer, misc, system
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## System Misc

Reference nodes for `System Misc`. Total: **19** nodes.

### Closure to List — `GeometryNodeClosureToList`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Build a list by evaluating a closure Count times (index-driven). Pairs with Evaluate Closure workflows.
- **Inputs:**
  - `Count` (`INT`)
  - `Closure` (`CLOSURE`)
- **Outputs:**
  - `Unnamed` (`CUSTOM`)


### Field to List — `GeometryNodeFieldToList`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Evaluate a field Count times into a list. Bridges the field lane into the new 5.2 list data type; list sockets are generic (element type set by the connected value).
- **Inputs:**
  - `Count` (`INT`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Unnamed` (`CUSTOM`)


### Filter List — `GeometryNodeFilterList`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Filter list items with a boolean selection; outputs the selected list and the inverted remainder.
- **Inputs:**
  - `List` (`FLOAT`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Selection` (`FLOAT`)
  - `Inverted` (`FLOAT`)


### For Each Geometry Element Output — `GeometryNodeForeachGeometryElementOutput`
- **Notes:** This zone type allows executing nodes for each element of a geometry. For example, the nodes can process every face of a mesh, or every instance. The For Each Element zone.  The...
- **Inputs:**
  - `Unnamed` (`CUSTOM`)
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)


### Frame — `NodeFrame`
- **Notes:** Collect related nodes together in a common area. Useful for organization when the re-usability of a node group is not required.
- **Inputs:** None
- **Outputs:** None


### Get List Item — `GeometryNodeListGetItem`
- **Version:** NodeCue support `Blender 5.0+`; verified `5.1`, `5.2`.
- **Compatibility:** Blender 5.2 made list sockets generic (was `FLOAT`).
- **Notes:** Generic list socket in 5.2: element type follows the connected list (socket_type/data_type enum), not Float-only. Resolve via live readback.
- **Inputs:**
  - `List` (`FLOAT`)
  - `Index` (`INT`)
- **Outputs:**
  - `Value` (`FLOAT`)


### Grease Pencil to Curves — `GeometryNodeGreasePencilToCurves`
- **Notes:** The Grease Pencil to Curves node converts each Grease Pencil layer into an instance that contains curves.
- **Inputs:**
  - `Grease Pencil` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Layers as Instances` (`BOOLEAN`)
- **Outputs:**
  - `Curves` (`GEOMETRY`)


### Group — `GeometryNodeGroup`
- **Notes:** A Group Node combines a set of nodes into a single one, and selectively exposes inputs and outputs of those nodes. Group nodes can simplify a node tree by hiding away complexity and reusing functionality.
- **Inputs:** None
- **Outputs:** None


### List — `GeometryNodeList`
- **Version:** Blender `5.0`-`5.1` only; removed in Blender `5.2`.
- **Evidence:** Blender 5.1 runtime readback (not documented in the 5.0/5.1 manual); removal confirmed by Blender 5.2 live probe.
- **Compatibility:** Removed in 5.2 - on Blender 5.2+ use `GeometryNodeFieldToList` or `GeometryNodeClosureToList` instead.
- **Notes:** Create a list of values (legacy list constructor).
- **Inputs:**
  - `Count` (`INT`)
  - `Value` (`FLOAT`)
- **Outputs:**
  - `List` (`FLOAT`)

### List Length — `GeometryNodeListLength`
- **Version:** NodeCue support `Blender 5.0+`; verified `5.1`, `5.2`.
- **Compatibility:** Blender 5.2 made list sockets generic (was `FLOAT`).
- **Notes:** Generic list socket in 5.2: element type follows the connected list (socket_type/data_type enum), not Float-only. Resolve via live readback.
- **Inputs:**
  - `List` (`FLOAT`)
- **Outputs:**
  - `Length` (`INT`)


### Merge Layers — `GeometryNodeMergeLayers`
- **Notes:** Combines multiple Grease Pencil Layers into a single layer. See also Merge Layers Operator
- **Inputs:**
  - `Grease Pencil` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Group ID` (`INT`)
- **Outputs:**
  - `Grease Pencil` (`GEOMETRY`)


### Named Layer Selection — `GeometryNodeInputNamedLayerSelection`
- **Notes:** The Named Layer Selection node outputs a Boolean field whose index value is true for Grease Pencil layers whose name matches a string input.
- **Inputs:**
  - `Name` (`STRING`)
- **Outputs:**
  - `Selection` (`BOOLEAN`)
- **Warning:** The specified layer must already exist in the object. - If no matching layer is found, the selection will be false for all elements.


### Reroute — `NodeReroute`
- **Notes:** A single-socket organization tool that supports one input and multiple outputs. Socket type is context-driven and adapts to connected links (for example can switch from color to geometry in GN trees).
- **Inputs:**
  - `Input` (`CUSTOM`)
- **Outputs:**
  - `Output` (`CUSTOM`)


### Set Grease Pencil Color — `GeometryNodeSetGreasePencilColor`
- **Notes:** The Set Grease Pencil Color node sets the color and opacity attributes of strokes and fills on Grease Pencil geometry.
- **Inputs:**
  - `Grease Pencil` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Color` (`COLOR`)
  - `Opacity` (`FLOAT`)
- **Outputs:**
  - `Grease Pencil` (`GEOMETRY`)


### Set Grease Pencil Depth — `GeometryNodeSetGreasePencilDepth`
- **Notes:** The Set Grease Pencil Depth node sets the Grease Pencil depth order to use.
- **Inputs:**
  - `Grease Pencil` (`GEOMETRY`)
- **Outputs:**
  - `Grease Pencil` (`GEOMETRY`)


### Set Grease Pencil Softness — `GeometryNodeSetGreasePencilSoftness`
- **Notes:** The Set Grease Pencil Softness node sets a stroke’s softness, which controls how much a stroke’s edges fade out. Higher softness values create more transparent, blurred edges, while lower values produce crisper, more defined strokes.
- **Inputs:**
  - `Grease Pencil` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Softness` (`FLOAT`)
- **Outputs:**
  - `Grease Pencil` (`GEOMETRY`)


### Sort List — `GeometryNodeSortList`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Sort list items by a sort weight, optionally within groups (Group ID) and restricted by Selection.
- **Inputs:**
  - `List` (`FLOAT`)
  - `Selection` (`BOOLEAN`)
  - `Group ID` (`INT`)
  - `Sort Weight` (`FLOAT`)
- **Outputs:**
  - `List` (`FLOAT`)


### Viewer — `GeometryNodeViewer`
- **Notes:** The Viewer node allows viewing data from inside a geometry node group in both the Spreadsheet Editor and the 3D Viewport. Any geometry or attribute connected to the viewer can be visualized in the viewport, and its evaluated attribute values can be inspected in the spreadsheet. Other data can also be viewed and inspected such as scaler values and grids by showing them in the spreadsheet.
- **Inputs:**
  - `Unnamed` (`CUSTOM`)
- **Outputs:** None
- **Example:** Visualizing the Noise Texture Factor on the default cube. Visualizing the Index Attribute as text on the default cube.
- **Tip:** The Viewer node cannot be used in the Tool context—only in the Modifier context.
- **Tip:** Only number keys (1–9) are supported.
- **Warning:** Complex data types such as geometry or grids cannot be previewed this way and must be visualized using the Viewer node or the Spreadsheet editor.
- **Warning:** The Geometry socket must be first.


### Warning — `GeometryNodeWarning`
- **Notes:** Outputs a custom message that can be referenced in the Warnings panel of the Geometry Nodes Modifier. This allows node groups to communicate expectations about input values. By default, warnings are propagated through all parent node groups. However, this can be controlled using the Warning Propagation setting on each node.
- **Inputs:**
  - `Show` (`BOOLEAN`)
  - `Message` (`STRING`)
- **Outputs:**
  - `Show` (`BOOLEAN`)
