---
title: Input Constant
section: input
description: "Input Nodes (Constant): Constant values and datablock references used as reusable inputs."
tags: boolean, color, constant, image, input, integer, rotation, string, vector
blender_support: "5.0+"
blender_verified: 5.1.1, 5.2.0
last_verified: "2026-07-18"
---

## Input Constant

Reference nodes for `Input Constant`. Total: **14** nodes.

### Boolean — `FunctionNodeInputBool`
- **Notes:** The Boolean node provides a Boolean value.
- **Inputs:** None
- **Outputs:**
  - `Boolean` (`BOOLEAN`)


### Collection — `GeometryNodeInputCollection`
- **Notes:** The Collection input node outputs a single collection. It can be connected to other collection sockets to make using the same collection in multiple places more convenient.
- **Inputs:** None
- **Outputs:**
  - `Collection` (`COLLECTION`)


### Color — `FunctionNodeInputColor`
- **Notes:** The Color node outputs the color value chosen with the color picker widget.
- **Inputs:** None
- **Outputs:**
  - `Color` (`COLOR`)
- **Tip:** Dragging colors from a color picker button into a node editor creates a Color node. Alpha values are preserved, if the source color has no alpha, a value of 1.0 is used.


### Font — `GeometryNodeInputFont`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Font data-block input for text/string-to-curves workflows.
- **Inputs:** None
- **Outputs:**
  - `Font` (`FONT`)


### Image — `GeometryNodeInputImage`
- **Notes:** Image node.  The Image node provides access to a image file which allows you to conveniently enter and switch images for multiple nodes in the tree. See also Image Info Node
- **Inputs:** None
- **Outputs:**
  - `Image` (`IMAGE`)


### Integer Vector — `FunctionNodeInputIntVector`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Constant integer vector input (integer counterpart of the Vector input).
- **Inputs:** None
- **Outputs:**
  - `Vector` (`INT_VECTOR`)


### Integer — `FunctionNodeInputInt`
- **Notes:** The Integer node provides an integer value.
- **Inputs:** None
- **Outputs:**
  - `Integer` (`INT`)


### Material — `GeometryNodeInputMaterial`
- **Notes:** The Material input node outputs a single material. It can be connected to other material sockets to make using the same material name in multiple places more convenient.
- **Inputs:** None
- **Outputs:**
  - `Material` (`MATERIAL`)
- **Tip:** The Material node can also be added by dragging and dropping a material data-block into the node editor. This will add the node and select the dropped material in the Data-Block Menu.


### Menu — `FunctionNodeInputMenu`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Menu constant input; exposes a menu socket for switch-style group interfaces.
- **Inputs:** None
- **Outputs:**
  - `Menu` (`MENU`)


### Object — `GeometryNodeInputObject`
- **Notes:** The Object input node outputs a single object. It can be connected to other object sockets to make using the same object in multiple places more convenient.
- **Inputs:** None
- **Outputs:**
  - `Object` (`OBJECT`)


### Rotation — `FunctionNodeInputRotation`
- **Notes:** The Rotation input creates a rotation from euler rotation values. Standard rotation output.
- **Inputs:** None
- **Outputs:**
  - `Rotation` (`ROTATION`)


### String — `FunctionNodeInputString`
- **Notes:** The String input node creates a single string. It can be connected to attribute name sockets to make using the same attribute name in multiple places more convenient.
- **Inputs:** None
- **Outputs:**
  - `String` (`STRING`)


### Value — `ShaderNodeValue`
- **Notes:** Input numerical values to other nodes in the tree.
- **Inputs:** None
- **Outputs:**
  - `Value` (`FLOAT`)
- **Tip:** From this you can also make different values proportional to each other by adding a Math Node in between the different links.


### Vector — `FunctionNodeInputVector`
- **Notes:** The Vector input node creates a single vector. Standard vector output.
- **Inputs:** None
- **Outputs:**
  - `Vector` (`VECTOR`)
