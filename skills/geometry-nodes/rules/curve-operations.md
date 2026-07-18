---
title: Curve Operations
section: curve
description: "Curve Nodes (Operations): Modify, resample, convert, and edit existing curve geometry."
tags: curve, operations, set
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Curve Operations

Reference nodes for `Curve Operations`. Total: **22** nodes.

### Curve to Mesh — `GeometryNodeCurveToMesh`
- **Notes:** The Curve to Mesh node converts all splines of a curve to a mesh. Optionally, a profile curve can be provided to give the curve a custom shape. The node transfers attributes to the result. Attributes that are built-in on meshes but not curves, like `sharp_face`, will be transferred to the correct domain as well.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Profile Curve` (`GEOMETRY`)
  - `Scale` (`FLOAT`)
  - `Fill Caps` (`BOOLEAN`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
- **Example:** Edge-to-tube visualization — Mesh to Curve converts mesh edges into curves, then Curve to Mesh with a Curve Circle profile (small radius) sweeps a tube along each edge. Useful for wireframe rendering, edge highlighting, and structural visualization.
- **Tip:** The output mesh has sharp edges set from the profile curve tagged automatically. If any splines in the profile curve are Bézier splines and any of the control points use Free or Vector handles, the corresponding edges will be shaded sharp.


### Curve to Points — `GeometryNodeCurveToPoints`
- **Notes:** The Curve to Points node generates a point cloud from a curve.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Count` (`INT`)
  - `Length` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)
  - `Tangent` (`VECTOR`)
  - `Normal` (`VECTOR`)
  - `Rotation` (`ROTATION`)


### Curves to Grease Pencil — `GeometryNodeCurvesToGreasePencil`
- **Notes:** The Curves to Grease Pencil node Converts top-level curve instances into Grease Pencil layers
- **Inputs:**
  - `Curves` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Instances as Layers` (`BOOLEAN`)
- **Outputs:**
  - `Grease Pencil` (`GEOMETRY`)
- **Example:** Create a Grease Pencil layer from a curve. Set Curve Radius controls stroke width. Used with: Set Curve Radius.


### Deform Curves on Surface — `GeometryNodeDeformCurvesOnSurface`
- **Notes:** The Deform Curves on Surface node translates and rotates each curve based on the difference in its root position. The root position is defined by UV coordinates stored on each curve and the UV Map selected for the purpose in the Curves surface settings. The transformation is calculated based on the difference of the original mesh (before shape keys and modifiers are evaluated), and the final mesh. Unlike other geometry nodes, this node has quite a few implicit inputs: - The original and evaluated mesh are retrieved from the modifier object’s surface property. This means the node only works for curves objects. - The original and evaluated UV map are also retrieved from the object’s surface property. - A 3D vector attribute named `rest_position`, used for calculating tangents for rotating curves that are consistent with the tangents calculated on the original mesh (the rotation needs to be calculated from the normal and tangent of the original and evaluated meshes). - A 2D vector attribute on the curve domain named `surface_uv_coordinate` to store the location of the root positions on the surface mesh’s UV map. In future development, this node will be generalized so the setup is more flexible. Parts of the internal operation are similar to the Sample UV Surface Node.
- **Inputs:**
  - `Curves` (`GEOMETRY`)
- **Outputs:**
  - `Curves` (`GEOMETRY`)
- **Warning:** In order to achieve consistent deformation after the Subdivision Surface Modifier, the UV Smooth option of the modifier should be set to None. Otherwise the surface UV map will be subdivided in a way that may invalidate the curve UV attachement points stored in the `surface_uv_coordinate` attribute.


### Fill Curve — `GeometryNodeFillCurve`
- **Notes:** The Fill Curve node generates a mesh using the constrained Delaunay triangulation algorithm with the curves as boundaries. The mesh is only generated flat with a local Z of 0.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Group ID` (`INT`)
  - `Mode` (`MENU: Triangles, N-gons`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)
- **Example:** One or many “single point spline” can be used to customize the triangulation of the filled-in curves.


### Fillet Curve — `GeometryNodeFilletCurve`
- **Notes:** The Fillet Curve rounds corners on curve control points, similar to the effect of the Bevel Modifier on a 2D mesh. However, a key difference is that the rounded portions created by the Fillet Curve node are always portions of a circle.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Radius` (`FLOAT`)
  - `Limit Radius` (`BOOLEAN`)
  - `Mode` (`MENU: Bézier, Poly`)
  - `Count` (`INT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
- **Example:** The node can be used to round the corners of simple 3D poly splines.


### Interpolate Curves — `GeometryNodeInterpolateCurves`
- **Notes:** Generate new curves on points by interpolating between existing curves. This is useful to have a smaller set of original curves to make editing easier and faster while still generating high-density curves for the viewport or a final render.
- **Inputs:**
  - `Guide Curves` (`GEOMETRY`)
  - `Guide Up` (`VECTOR`)
  - `Guide Group ID` (`INT`)
  - `Points` (`GEOMETRY`)
  - `Point Up` (`VECTOR`)
  - `Point Group ID` (`INT`)
  - `Max Neighbors` (`INT`)
- **Outputs:**
  - `Curves` (`GEOMETRY`)
  - `Closest Index` (`INT`)
  - `Closest Weight` (`FLOAT`)


### Resample Curve — `GeometryNodeResampleCurve`
- **Notes:** The Resample Curve node creates a poly spline for each input spline. In the Count and Length modes, the control points of the new poly splines will have uniform spacing.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Mode` (`MENU: Evaluated, Count, Length`)
  - `Count` (`INT`)
  - `Length` (`FLOAT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
- **Tip:** Use a field as an input to have a different count/length for each spline.


### Reverse Curve — `GeometryNodeReverseCurve`
- **Notes:** The Reverse Curve node swaps the start and end of splines. The shape of the splines is not changed.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
- **Tip:** When used on the Profile input of the Curve to Mesh Node, this node fill flip the normals of the resulting mesh.


### Sample Curve — `GeometryNodeSampleCurve`
- **Notes:** The Sample Curve calculates a point on a curve at a certain distance from the start of the curve, specified by the length or factor inputs. It also outputs data retrieved from that position on the curve. The sampled values are linearly interpolated from the values at the evaluated curve points at each side of the sampled point.
- **Inputs:**
  - `Curves` (`GEOMETRY`)
  - `Value` (`FLOAT`)
  - `Factor` (`FLOAT`)
  - `Length` (`FLOAT`)
  - `Curve Index` (`INT`)
- **Outputs:**
  - `Value` (`FLOAT`)
  - `Position` (`VECTOR`)
  - `Tangent` (`VECTOR`)
  - `Normal` (`VECTOR`)
- **Example:** Here, the Count mode of the Resample Curve Node is recreated, except a mesh is used for the result instead of a curve. Used with: Resample Curve.
- **Tip:** When the curve contains multiple splines, the sample position is found based on the total accumulated length, including the lengths of all previous splines. The order of the splines is the same order as displayed in the Spreadsheet Editor.
- **Properties:**
  - `mode` (FACTOR, LENGTH) — FACTOR: Find sample positions on the curve using a factor of its total length; LENGTH: Find sample positions on the curve using a distance from its beginning


### Set Curve Normal — `GeometryNodeSetCurveNormal`
- **Notes:** The Set Curve Normal controls the method used to calculate curve normals for every curve. The node doesn’t set the normals directly, those are calculated later as necessary. Combined with the tilt attribute value at each control point, this will define the final normals accessible with the Normal Node. Internally this node adjusts the values of the `normal_mode` attribute on each curve.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Mode` (`MENU: Minimum Twist, Z Up, Free`)
  - `Normal` (`VECTOR`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)


### Set Curve Radius — `GeometryNodeSetCurveRadius`
- **Notes:** The Set Curve Radius controls the radius of the curve, used for operations like the size of the profile in the Curve to Mesh node. The value is set for every control point, and is then interpolated to each evaluated point in between the control points. The input node for this data is the Radius node.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Radius` (`FLOAT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)


### Set Curve Tilt — `GeometryNodeSetCurveTilt`
- **Notes:** The Set Curve Tilt controls the tilt angle at each curve control point. That angle rotates normal vector which is generated at each point when evaluating the curve. The normal then can be retrieved with the Normal Node. The rotation of the normal vector is an Axis Angle rotation. It is the same as the Vector Rotate Node operation with the tangent vector as the axis, the raw evaluated normal is used as the original vector, and the tilt as the rotation angle. The input node for this data is the Curve Tilt Node.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Tilt` (`FLOAT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)


### Set Handle Positions — `GeometryNodeSetCurveHandlePositions`
- **Notes:** The Set Handle Positions node sets the positions for the handles of Bézier curves. They can be used to alter the generated shape of the curve. The input node for this data is the Curve Handle Positions Node. See the Bézier curves page for more details.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Position` (`VECTOR`)
  - `Offset` (`VECTOR`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
- **Example:** Here, the handles are adjusted to the same position as the control points, but offset down in the Z direction slightly. Used with: Set Spline Type.
- **Tip:** When the position is changed, Auto handle types will be converted to Aligned, and Vector handle types will be converted to Free.
- **Tip:** The left and right handles cannot be changed at the same time with this node. That is because it would break the alignment for left and right handles at the same control point.
- **Tip:** The handle positions are the global position of the handle, they are not relative to the position of the corresponding control point.


### Set Handle Type — `GeometryNodeCurveSetHandles`
- **Notes:** Sets the handle type for the points on the Bézier curve that are in the selection. A selection for a certain handle type can be retrieved with the Handle Type Selection Node .
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
- **Properties:**
  - `handle_type` (FREE, AUTO, VECTOR, ALIGN) — FREE: The handle can be moved anywhere, and does not influence the point's other ha...; AUTO: The location is automatically calculated to be smooth; VECTOR: The location is calculated to point to the next/previous control point
  - `mode` (LEFT, RIGHT) — LEFT: Use the left handles; RIGHT: Use the right handles


### Set NURBS Order — `GeometryNodeSetNURBSOrder`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Set the NURBS order of curve splines.
- **Inputs:**
  - `Curves` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Order` (`INT`)
- **Outputs:**
  - `Curves` (`GEOMETRY`)


### Set NURBS Weight — `GeometryNodeSetNURBSWeight`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Set NURBS control-point weights.
- **Inputs:**
  - `Curves` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Weight` (`FLOAT`)
- **Outputs:**
  - `Curves` (`GEOMETRY`)


### Set Spline Cyclic — `GeometryNodeSetSplineCyclic`
- **Notes:** The Set Spline Cyclic node changes whether splines loop back on themselves – that is, whether their first and last control points are connected. You can use the Is Spline Cyclic Node to read this property.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Cyclic` (`BOOLEAN`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)


### Set Spline Resolution — `GeometryNodeSetSplineResolution`
- **Notes:** The Set Spline Resolution node sets the value for how many evaluated points should be generated on the curve for every control point. It only has an effect on NURBS, Bézier, and Catmull Rom splines. In case of Bézier splines, the resolution does not have an effect on segments between vector handles. The evaluated points are displayed in the viewport, used in the Curve to Mesh Node node, and optionally used in the Resample Curve Node. The input node for this data is the Spline Resolution Node.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Resolution` (`INT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)


### Set Spline Type — `GeometryNodeCurveSplineType`
- **Notes:** Sets the spline type for the splines in the curve component that are in the selection.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
- **Properties:**
  - `spline_type` (CATMULL_ROM, POLY, BEZIER, NURBS)


### Subdivide Curve — `GeometryNodeSubdivideCurve`
- **Notes:** The Subdivide Curve node adds more control points in between existing control points on the curve input. For Bézier and poly splines, the shape of the spline will not be changed at all. With Bézier curves, this can be used to increase the control on the shape of the curve while still having the higher-level provided by Bézier splines. Unlike the Resample Curve Node, where they are converted to poly splines.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Cuts` (`INT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)


### Trim Curve — `GeometryNodeTrimCurve`
- **Notes:** The Trim Curve node shortens each spline in the curve by removing sections at the start and end of each spline. Bézier splines will still be Bézier splines in the output, with the first and last control point and its handles moved as necessary to preserve the shape. NURBS splines will be transformed into poly splines in order to be trimmed.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
  - `Selection` (`BOOLEAN`)
  - `Start` (`FLOAT`)
  - `End` (`FLOAT`)
  - `Start` (`FLOAT`)
  - `End` (`FLOAT`)
- **Outputs:**
  - `Curve` (`GEOMETRY`)
- **Warning:** Currently the Trim Curve node does not support cyclic splines.
- **Warning:** Since curve normals are calculated the final curve, this node may change the resulting normals when the *Minimum twist method is used, since the Minimum* method considers the entire length of the curve to decide the final normals. In some cases the Capture Attribute Node could be used to avoid this, by saving the original normals to be used later.
