---
title: Utilities Field
section: utilities
description: "Utilities (Field): Evaluate, aggregate, and transform fields across domains."
tags: accumulate, evaluate, field, utilities
blender_support: "5.0+"
blender_verified: 5.1.1, 5.2.0
last_verified: "2026-07-18"
---

## Utilities Field

Reference nodes for `Utilities Field`. Total: **6** nodes.

### Accumulate Field — `GeometryNodeAccumulateField`
- **Notes:** The Accumulate Field node counts a running total of its input values, in the order defined by the geometry’s indices. The node’s essential operation is just addition, but instead of only outputting the final total, it outputs the current value at every element.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Group ID` (`INT`)
- **Outputs:**
  - `Leading` (`FLOAT`)
  - `Trailing` (`FLOAT`)
  - `Total` (`FLOAT`)
- **Example:** A few examples of input values and the node’s results. Used with: Random Value.

### Evaluate at Index — `GeometryNodeFieldAtIndex`
- **Notes:** The Evaluate at Index node allows accessing data of other elements in the context geometry. It is similar to the Sample Index Node. The main difference is that this node does not require a geometry input, because the geometry from the field context is used. This node is also similar to the Evaluate on Domain Node node, except that the value to retrieve from the specified domain is specified by an index rather than an automatic domain interpolation.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Index` (`INT`)
- **Outputs:**
  - `Value` (`FLOAT`)

### Evaluate on Domain — `GeometryNodeFieldOnDomain`
- **Notes:** The Evaluate on Domain allows evaluating a field for a different attribute domain than the domain from the field context. For example, the face index could be used instead of the face corner index, when setting the values of a UV Map
- **Inputs:**
  - `Value` (`FLOAT`)
- **Outputs:**
  - `Value` (`FLOAT`)
- **Tip:** This node is not necessary to retrieve data from other attribute domains; that is done automatically. Its utility comes from the fact that it’s possible to control when the domain interpolation happens. Normally, input nodes interpolate their data to the current context’s domain as soon as they create their output.
- **Tip:** It may be preferable to use this node over the Capture Attribute Node, since it allows using a specific attribute domain without requiring a geometry socket input, which allows creating more reusable node groups.
- **Tip:** The method of retrieving data from another domain is somewhat similar to the Evaluate at Index Node.

### Field Average — `GeometryNodeFieldAverage`
- **Notes:** The Field Average calculates the mean and median of a given field.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Group ID` (`INT`)
- **Outputs:**
  - `Mean` (`FLOAT`)
  - `Median` (`FLOAT`)

### Field Min & Max — `GeometryNodeFieldMinAndMax`
- **Notes:** The Field Min & Max calculates the minimum and maximum of a given field. The lowest value in each group. The highest value in each group.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Group ID` (`INT`)
- **Outputs:**
  - `Min` (`FLOAT`)
  - `Max` (`FLOAT`)

### Field Variance — `GeometryNodeFieldVariance`
- **Notes:** The Field Variance node computes the variance and standard deviation of a field over a given domain. This is useful for measuring how much a value varies across geometry or within specific groups. For example, it can be used to analyze the spread of values like weights, positions, or custom attributes within each group defined by the Group ID.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Group ID` (`INT`)
- **Outputs:**
  - `Standard Deviation` (`FLOAT`)
  - `Variance` (`FLOAT`)

