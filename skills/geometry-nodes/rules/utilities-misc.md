---
title: Utilities Misc
section: utilities
description: "Utilities (Misc): Switch/control-flow style helpers, randomization, and mixed utilities."
tags: align, misc, random, rotate, rotation, utilities
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Utilities Misc

Reference nodes for `Utilities Misc`. Total: **11** nodes.

### Align Euler to Vector — `FunctionNodeAlignEulerToVector`
- **Notes:** The Align Euler to Vector node rotates an Euler rotation into the given direction. Important This node is deprecated, use the Align Rotation to Vector Node instead.
- **Inputs:**
  - `Rotation` (`VECTOR`)
  - `Factor` (`FLOAT`)
  - `Vector` (`VECTOR`)
- **Outputs:**
  - `Rotation` (`VECTOR`)
- **Tip:** This node is deprecated, use the Align Rotation to Vector Node instead.


### For Each Geometry Element Input — `GeometryNodeForeachGeometryElementInput`
- **Notes:** This zone type allows executing nodes for each element of a geometry. For example, the nodes can process every face of a mesh, or every instance. The For Each Element zone.  The...
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Index` (`INT`)
  - `Element` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)


### Index Switch — `GeometryNodeIndexSwitch`
- **Notes:** The Index Switch node outputs one of its inputs based on an integer Index value. Only the selected input is evaluated, making this node useful for switching between multiple data inputs efficiently.
- **Inputs:**
  - `Index` (`INT`)
  - `0` (`GEOMETRY`)
  - `1` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Output` (`GEOMETRY`)
- **Tip:** The Menu Switch node provides similar functionality, but exposes the selection as a user-friendly menu rather than an index.
- **Tip:** When the Index input is connected to a Menu Switch node set to Integer Type, the corresponding menu labels will automatically be shown next to the index value. This provides a clearer context for what each numeric index represents, making node networks more readable.


### Join Geometry — `GeometryNodeJoinGeometry`
- **Notes:** The Join Geometry node merges separately generated geometries into a single one. If the geometry inputs contain different types of data, the output will also contain different data types.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
- **Warning:** The node cannot handle the case when more than one geometry input has a volume component.
- **Tip:** Vertex groups are preserved when realizing instances or joining geometries. If the domain and type propagation rules above result with the vertex domain and float type, then an attribute will be a vertex group on the output mesh.


### Menu Switch — `GeometryNodeMenuSwitch`
- **Notes:** The Menu Switch node outputs one of its inputs based on a selected menu item. Only the active input is evaluated, allowing efficient switching between multiple options. The available menu entries are defined by the user. Menu items can be added and removed, as well as renamed and reordered in the editor side bar. Renaming a menu entry keeps existing links of the matching input socket. The menu can be used in node groups and the nodes modifier UI. Connecting the menu input with a Group Input node will expose the menu as a group input. A menu socket in a node group, reroute node, or other pass-through nodes needs to be connected to a Menu Switch node in order to work. An unconnected menu socket will show an empty menu by default. Connecting multiple Menu Switch nodes to the same output socket creates a conflict (even when the menu entries are the same). To avoid this a menu switch can be wrapped in a node group. Multiple node groups of the same type can be connected to the same menu, since they contain the same menu switch node. | !../../../_images/node-types_GeometryNodeMenuSwitch_conflict.webp Conflict caused by connecting different menus. | !../../../_images/node-types_GeometryNodeMenuSwitch_group_wrapper.webp Same node group can be connected without conflict. | | --- | --- |
- **Inputs:**
  - `Menu` (`MENU: A, B`)
  - `A` (`GEOMETRY`)
  - `B` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Output` (`GEOMETRY`)
  - `A` (`BOOLEAN`)
  - `B` (`BOOLEAN`)
- **Tip:** The Index Switch Node is similar but it exposes the choices as an integer index.


### Random Value — `FunctionNodeRandomValue`
- **Compatibility:** Blender 5.2 changed socket identifiers and made `Min`/`Max`/`Value` generic. Do not reuse 5.1 socket identifiers; resolve sockets from live readback.
- **Notes:** The Random Value node outputs a white noise like value as a Float , Integer , Vector , or Boolean field.
- **Inputs:**
  - `Min` (`VECTOR`)
  - `Max` (`VECTOR`)
  - `Min` (`FLOAT`)
  - `Max` (`FLOAT`)
  - `Min` (`INT`)
  - `Max` (`INT`)
  - `Probability` (`FLOAT`)
  - `ID` (`INT`)
  - `Seed` (`INT`)
- **Outputs:**
  - `Value` (`VECTOR`)
  - `Value` (`FLOAT`)
  - `Value` (`INT`)
  - `Value` (`BOOLEAN`)


### Repeat Input — `GeometryNodeRepeatInput`
- **Notes:** A Repeat Zone executes a set of nodes multiple times. The zone consists of an input node on the left, an output node on the right, and an orange area in the middle for placing the...
- **Inputs:**
  - `Iterations` (`INT`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Iteration` (`INT`)
  - `Unnamed` (`CUSTOM`)


### Repeat Output — `GeometryNodeRepeatOutput`
- **Notes:** A Repeat Zone executes a set of nodes multiple times. In headless extraction this node keeps explicit `Geometry` plus zone-typed `CUSTOM` passthrough sockets.
- **Inputs:**
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Geometry` (`GEOMETRY`)
  - `Unnamed` (`CUSTOM`)


### Rotate Euler — `FunctionNodeRotateEuler`
- **Notes:** The Rotate Euler node rotates an Euler rotation. Important This node is deprecated, use the Rotate Rotation Node instead.
- **Inputs:**
  - `Rotation` (`VECTOR`)
  - `Rotate By` (`VECTOR`)
  - `Axis` (`VECTOR`)
  - `Angle` (`FLOAT`)
- **Outputs:**
  - `Rotation` (`VECTOR`)
- **Tip:** This node is deprecated, use the Rotate Rotation Node instead.


### Switch — `GeometryNodeSwitch`
- **Notes:** The Switch node outputs one of two inputs depending on a condition. Only the input that is passed through the node is computed.
- **Inputs:**
  - `Switch` (`BOOLEAN`)
  - `False` (`GEOMETRY`)
  - `True` (`GEOMETRY`)
- **Outputs:**
  - `Output` (`GEOMETRY`)
- **Tip:** The Menu Switch Node and Index Switch Node can be used to switch between an arbitrary amount of inputs.


### Tag Filter — `GeometryNodeTagFilter`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Filter/select elements by tag membership (5.2 tag system).
- **Inputs:**
  - `Tag Filter` (`STRING`)
  - `Tags` (`STRING`)
- **Outputs:**
  - `Match` (`BOOLEAN`)
