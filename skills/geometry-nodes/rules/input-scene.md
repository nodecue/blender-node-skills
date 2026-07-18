---
title: Input Scene
section: input
description: "Input Nodes (Scene): Scene, object, camera, viewport, and time-dependent context inputs."
tags: active, camera, collection, image, input, scene
blender_support: "5.0+"
blender_verified: 5.1.1, 5.2.0
last_verified: "2026-07-18"
---

## Input Scene

Reference nodes for `Input Scene`. Total: **14** nodes.

### 3D Cursor — `GeometryNodeTool3DCursor`
- **Notes:** The 3D Cursor node outputs the position and orientation of the 3D cursor in the scene. Note: This node can only be used in the Tool context .
- **Inputs:** None
- **Outputs:**
  - `Location` (`VECTOR`)
  - `Rotation` (`ROTATION`)
- **Warning:** This node can only be used in the Tool context.


### Active Camera — `GeometryNodeInputActiveCamera`
- **Notes:** The Active Camera node outputs the scene’s current active camera.
- **Inputs:** None
- **Outputs:**
  - `Active Camera` (`OBJECT`)


### Bone Info — `GeometryNodeBoneInfo`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Read transform info for an armature bone by name.
- **Inputs:**
  - `Armature` (`OBJECT`)
  - `Bone Name` (`STRING`)
- **Outputs:**
  - `Pose` (`MATRIX`)
  - `Local Pose` (`MATRIX`)
  - `Transform Pose` (`MATRIX`)
  - `Rest Pose` (`MATRIX`)
  - `Rest Length` (`FLOAT`)
  - `Exists` (`BOOLEAN`)


### Camera Info — `GeometryNodeCameraInfo`
- **Notes:** The Camera Info node outputs the information about the selected camera object. It can be used to customize geometry based on the camera’s parameters, for example when building camera-based visual effects or aligning geometry with the camera view.
- **Inputs:**
  - `Camera` (`OBJECT`)
- **Outputs:**
  - `Projection Matrix` (`MATRIX`)
  - `Focal Length` (`FLOAT`)
  - `Sensor` (`VECTOR`)
  - `Shift` (`VECTOR`)
  - `Clip Start` (`FLOAT`)
  - `Clip End` (`FLOAT`)
  - `Focus Distance` (`FLOAT`)
  - `Is Orthographic` (`BOOLEAN`)
  - `Orthographic Scale` (`FLOAT`)


### Collection Children — `GeometryNodeCollectionChildren`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** List the child collections of a collection as collection references.
- **Inputs:**
  - `Collection` (`COLLECTION`)
  - `Recursive` (`BOOLEAN`)
- **Outputs:**
  - `Collections` (`COLLECTION`)
  - `Objects` (`OBJECT`)


### Collection Info — `GeometryNodeCollectionInfo`
- **Notes:** The Collection Info node gets information from collections. This can be useful to control parameters in the geometry node tree with an external collection.
- **Inputs:**
  - `Collection` (`COLLECTION`)
  - `Separate Children` (`BOOLEAN`)
  - `Reset Children` (`BOOLEAN`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)
- **Tip:** A Collection Info node can be added quickly by dragging a collection into the node editor.


### Image Info — `GeometryNodeImageInfo`
- **Notes:** The Image Info node gets information from image and animation. This can be useful to generate parameters in the geometry node for arbitrary images. Image information can be either general or frame-specific.
- **Inputs:**
  - `Image` (`IMAGE`)
  - `Frame` (`INT`)
- **Outputs:**
  - `Width` (`INT`)
  - `Height` (`INT`)
  - `Has Alpha` (`BOOLEAN`)
  - `Frame Count` (`INT`)
  - `FPS` (`FLOAT`)


### Is Viewport — `GeometryNodeIsViewport`
- **Notes:** The Is Viewport node outputs true when geometry nodes are evaluated for the viewport. For the final render the node outputs false.
- **Inputs:** None
- **Outputs:**
  - `Is Viewport` (`BOOLEAN`)


### Mouse Position — `GeometryNodeToolMousePosition`
- **Notes:** The Mouse Position node returns information about the mouse cursor such as its position and the region’s dimensions.
- **Inputs:** None
- **Outputs:**
  - `Mouse X` (`INT`)
  - `Mouse Y` (`INT`)
  - `Region Width` (`INT`)
  - `Region Height` (`INT`)
- **Tip:** When using this node, enable Wait for Click. to wait for a mouse click input (LMB) before running the operator from a menu.
- **Warning:** This node can only be used in the Tool context.


### Object Info — `GeometryNodeObjectInfo`
- **Notes:** The Object Info node gets information from objects. This can be useful to control parameters in the geometry node tree with an external object, either directly by using its geometry, or via its transformation properties. An Object Info node can be added quickly by dragging an object into the node editor.
- **Inputs:**
  - `Object` (`OBJECT`)
  - `As Instance` (`BOOLEAN`)
- **Outputs:**
  - `Transform` (`MATRIX`)
  - `Location` (`VECTOR`)
  - `Rotation` (`ROTATION`)
  - `Scale` (`VECTOR`)
  - `Geometry` (`GEOMETRY`)


### Sample Sound Frequencies — `GeometryNodeSampleSoundFrequencies`
- **Version:** Blender `5.2+`; verified `5.2.0`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Sample amplitude of a sound data-block across frequency bands at a given time; drives audio-reactive setups.
- **Inputs:**
  - `Sound` (`SOUND`)
  - `Time` (`FLOAT`)
  - `All Channels` (`BOOLEAN`)
  - `Channel` (`INT`)
  - `Low` (`FLOAT`)
  - `High` (`FLOAT`)
  - `FFT Size` (`MENU`)
  - `Window Function` (`MENU`)
- **Outputs:**
  - `Amplitude` (`FLOAT`)


### Scene Time — `GeometryNodeInputSceneTime`
- **Notes:** The Scene Time node outputs the current time in the scene’s animation in units of seconds or frames.
- **Inputs:** None
- **Outputs:**
  - `Seconds` (`FLOAT`)
  - `Frame` (`FLOAT`)


### Self Object — `GeometryNodeSelfObject`
- **Notes:** The Self Object node outputs the object that contains the geometry nodes modifier currently being executed. This can be used to retrieve the original transforms. When evaluated in the Tool context, this node returns the Active object.
- **Inputs:** None
- **Outputs:**
  - `Self Object` (`OBJECT`)
- **Tip:** The geometry cannot be retrieved from this object with the Object Info Node, since its final geometry is still being evaluated.


### Viewport Transform — `GeometryNodeViewportTransform`
- **Notes:** The Viewport Transform node retrieves the view direction and location of the 3D Viewport . Note: This node can only be used in the Tool context .
- **Inputs:** None
- **Outputs:**
  - `Projection` (`MATRIX`)
  - `View` (`MATRIX`)
  - `Is Orthographic` (`BOOLEAN`)
- **Warning:** This node can only be used in the Tool context.
