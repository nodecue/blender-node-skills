---
title: Curve Read
section: curve
description: "Curve Nodes (Read): Query curve state, spline properties, and curve-derived fields."
tags: curve, endpoint, handle, read
---

## Curve Read

Reference nodes for `Curve Read`. Total: **13** nodes.

### Curve Length — `GeometryNodeCurveLength`
- **Notes:** The Curve Length node outputs the length of all splines added together. Accumulated length of all splines of the curve.
- **Inputs:**
  - `Curve` (`GEOMETRY`)
- **Outputs:**
  - `Length` (`FLOAT`)

### Curve Handle Positions — `GeometryNodeInputCurveHandlePositions`
- **Notes:** Gets the two handle positions of each control point in a Bézier spline. You can use the Set Handle Positions Node to change these positions.
- **Inputs:**
  - `Relative` (`BOOLEAN`)
- **Outputs:**
  - `Left` (`VECTOR`)
  - `Right` (`VECTOR`)

### Curve Tangent — `GeometryNodeInputTangent`
- **Notes:** The Curve Tangent node outputs the direction that a curve points in at each control point, depending on the direction of the curve (which can be controlled with the Reverse Curve Node). The output values are normalized vectors.
- **Inputs:** None
- **Outputs:**
  - `Tangent` (`VECTOR`)
- **Tip:** For NURBS and Bézier spline curves, keep in mind that the value retrieved from this node is the value at every control point, which may not correspond to the visible evaluated points. For example, a Bézier spline might have 48 evaluated points, but only four control points, if its resolution is 12. For NURBS splines the difference may be even more pronounced and the result may not be as expected. A Resample Curve Node can be used to create a poly spline, where there is a control point for every evaluated point.

### Curve Tilt — `GeometryNodeInputCurveTilt`
- **Notes:** The Curve Tilt node outputs the angle used to turn the curve normal around the direction of the curve tangent in its evaluated points. Keep in mind that the output is per control point, just like the values that can be controlled in curve Edit Mode. For NURBS and Bézier splines, the values will be interpolated to the final evaluated points. The input node for this data is the Set Curve Tilt node.
- **Inputs:** None
- **Outputs:**
  - `Tilt` (`FLOAT`)

### Curve of Point — `GeometryNodeCurveOfPoint`
- **Notes:** The Curve of Point node retrieves the index of the curve a control point is part of. This node is conceptually similar to the Face of Corner Node .
- **Inputs:**
  - `Point Index` (`INT`)
- **Outputs:**
  - `Curve Index` (`INT`)
  - `Index in Curve` (`INT`)

### Endpoint Selection — `GeometryNodeCurveEndpointSelection`
- **Notes:** The Endpoint Selection node provides a selection for an arbitrary number of endpoints in each spline in a curve.
- **Inputs:**
  - `Start Size` (`INT`)
  - `End Size` (`INT`)
- **Outputs:**
  - `Selection` (`BOOLEAN`)
- **Example:** Anywhere the geometry is a curve, this node can be used to generate a selection of only the first and last points of each spline. Used with: Instance on Points.
- **Tip:** The selection operates for every control point. This may not correspond to the evaluated points displayed in the viewport for NURBS and Bézier splines, where one control point may correspond to many evaluated points.
- **Tip:** To use this data after the curve has been converted to another data type like mesh or a point cloud, the Capture Attribute Node can be used.

### Handle Type Selection — `GeometryNodeCurveHandleTypeSelection`
- **Notes:** Creates a selection based on the handle types of the control points. The handle type of each control point can be changed with the Set Handle Type Node .
- **Inputs:** None
- **Outputs:**
  - `Selection` (`BOOLEAN`)

### Is Spline Cyclic — `GeometryNodeInputSplineCyclic`
- **Notes:** The Is Spline Cyclic controls whether each of the curve splines start and endpoints form a connection. Its output corresponds to the built-in `cyclic` attribute on the curve spline domain. The node to set this data is the Set Spline Cyclic Node.
- **Inputs:** None
- **Outputs:**
  - `Cyclic` (`BOOLEAN`)

### Offset Point in Curve — `GeometryNodeOffsetPointInCurve`
- **Notes:** The Offset Point in Curve node retrieves other points in the same curve as the input control point. This is like starting at a specific control point and walking along neighboring points toward the start or end of the curve. Conceptually the operation is similar to the Offset Corner in Face Node, but the point index doesn’t wrap around to the other end of the curve unless it is cyclic.
- **Inputs:**
  - `Point Index` (`INT`)
  - `Offset` (`INT`)
- **Outputs:**
  - `Is Valid Offset` (`BOOLEAN`)
  - `Point Index` (`INT`)

### Points of Curve — `GeometryNodePointsOfCurve`
- **Notes:** The Points of Curve node retrieves indices of specific control points in a curve.
- **Inputs:**
  - `Curve Index` (`INT`)
  - `Weights` (`FLOAT`)
  - `Sort Index` (`INT`)
- **Outputs:**
  - `Point Index` (`INT`)
  - `Total` (`INT`)

### Spline Length — `GeometryNodeSplineLength`
- **Notes:** The Spline Length node outputs the total length of each spline, as a distance, or a number of points. This is different than the Curve Length node, which adds up the total length for all of the curve’s splines. The output values correspond to the spline domain, but the node can be used to output a value for every curve control point as well.
- **Inputs:** None
- **Outputs:**
  - `Length` (`FLOAT`)
  - `Point Count` (`INT`)

### Spline Parameter — `GeometryNodeSplineParameter`
- **Notes:** The Spline Parameter node outputs how far along each spline a control point is. The Factor output is different from dividing the index by the total number of control points, because the control points might not be equally spaced along the curve. The first value is zero, so the output corresponds to the length at the control point rather than including the length of the following segment. When used on the spline domain, the node outputs the portion of the total length of the curve (including all splines) has been traversed at the start of each spline. The order of the curve’s splines is visible in the Spreadsheet Editor.
- **Inputs:** None
- **Outputs:**
  - `Factor` (`FLOAT`)
  - `Length` (`FLOAT`)
  - `Index` (`INT`)
- **Example:** The parameter used to control the radius of the curve. The beginning of the spline has a radius of 0, the end has a radius of 1.
- **Tip:** For NURBS and Bézier spline curves, keep in mind that the value retrieved from this node is the value at every control point, which may not correspond to the visible evaluated points. For NURBS splines the difference may be even more pronounced and the result may not be as expected. A Resample Curve Node node can be used to create a poly spline, where there is a control point for every evaluated point.
- **Tip:** When the Length is zero, the Factor is arbitrary. In this case the result is exceptionally calculated dividing the index by the total number of control points or curves.

### Spline Resolution — `GeometryNodeInputSplineResolution`
- **Notes:** The Spline Resolution outputs the number of evaluated curve points that will be generated for every control point on the spline. This node works for NURBS, Bézier, and Catmull Rom splines. For poly splines, there is a one-to-one correspondence between original points and evaluated points, so the resolution does not have an effect. On Bézier splines, the resolution does not have an effect on segments between vector handles, since there are no extra evaluated points between the neighboring control points. The node to set this data is the Set Spline Resolution Node.
- **Inputs:** None
- **Outputs:**
  - `Resolution` (`INT`)

