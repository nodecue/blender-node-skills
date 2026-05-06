---
title: Input Import
section: input
description: "Input Nodes (Import): File-based geometry and data import nodes."
tags: import, input
---

## Input Import

Reference nodes for `Input Import`. Total: **6** nodes.

### Import CSV — `GeometryNodeImportCSV`
- **Notes:** The Import CSV node reads data from a CSV (Comma-Separated Values) file and generates a point cloud. Each row in the file becomes a point, with numeric columns imported as attributes. Attribute names are taken from the header row (if present), and types are inferred from the first value in each column: - Integer values create integer attributes. - Float values create float attributes. This node is useful for visualizing external datasets in Geometry Nodes, such as for scientific visualization or procedural generation based on tabular data.
- **Inputs:**
  - `Path` (`STRING`)
  - `Delimiter` (`STRING`)
- **Outputs:**
  - `Point Cloud` (`GEOMETRY`)
- **Tip:** Only integer and float columns are supported. Other types, such as strings, are ignored.

### Import OBJ — `GeometryNodeImportOBJ`
- **Notes:** The Import OBJ node loads geometry data from a.obj file and outputs it as instances. Each object defined in the OBJ file is imported as a separate instance, which helps to preserve scene structure and optimize performance. This approach allows for efficient manipulation and reuse of the geometry within Geometry Nodes workflows. This node is useful for importing static 3D assets created in other modeling software.
- **Inputs:**
  - `Path` (`STRING`)
- **Outputs:**
  - `Instances` (`GEOMETRY`)
- **Tip:** The node imports only mesh geometry; materials and textures are not imported.

### Import PLY — `GeometryNodeImportPLY`
- **Notes:** The Import PLY node imports mesh data from a.ply (Polygon File Format or Stanford Triangle Format) file. PLY files typically store geometry from 3D scanning or modeling software and can include vertex attributes such as colors or normals. The geometry is imported as a single mesh. This node allows procedural workflows to incorporate external static geometry directly into Geometry Nodes.
- **Inputs:**
  - `Path` (`STRING`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Import STL — `GeometryNodeImportSTL`
- **Notes:** The Import STL node imports mesh geometry from a.stl (Stereolithography) file. STL files are commonly used for 3D printing and CAD applications and contain only surface geometry, typically as a collection of triangles with no color, texture, or other attributes. This node enables incorporating external STL assets into Geometry Nodes for procedural processing or visualization.
- **Inputs:**
  - `Path` (`STRING`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)

### Import Text — `GeometryNodeImportText`
- **Notes:** The Import Text node reads the contents of a plain text file and outputs it as a single string. This can be useful in motion graphics or data-driven workflows where external text needs to be processed or displayed.
- **Inputs:**
  - `Path` (`STRING`)
- **Outputs:**
  - `String` (`STRING`)
- **Tip:** Currently, only files with the.txt extension are supported.

### Import VDB — `GeometryNodeImportVDB`
- **Notes:** The Import VDB node loads volumetric data from a.vdb file and outputs it as a Volume geometry. All grids present in the file are loaded and included in the resulting volume. This node is useful for importing simulation data or procedural volumes created in external software.
- **Inputs:**
  - `Path` (`STRING`)
- **Outputs:**
  - `Volume` (`GEOMETRY`)

