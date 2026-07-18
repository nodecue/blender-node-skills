---
title: Volume Operations
section: volume
description: "Volume Nodes (Operations): Build, transform, and process voxel grids and volume geometry."
tags: field, get, grid, operations, prune, volume
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Volume Operations

Reference nodes for `Volume Operations`. Total: **24** nodes.

### Clip Grid — `GeometryNodeGridClip`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Clip a volume grid against bounds.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Min X` (`INT`)
  - `Min Y` (`INT`)
  - `Min Z` (`INT`)
  - `Max X` (`INT`)
  - `Max Y` (`INT`)
  - `Max Z` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### Field to Grid — `GeometryNodeFieldToGrid`
- **Notes:** The Field to Grid node creates one or more new voxel grids by evaluating geometry fields on the topology of an existing grid. This allows generating new volumetric data (such as density, temperature, velocity, or distance fields) directly from field inputs defined in the node tree. Each input field is sampled at the voxel positions of the provided topology grid, producing a corresponding output grid that matches the same resolution, transform, and domain. This enables consistent evaluation of multiple attributes or procedural quantities across the same volume structure.
- **Inputs:**
  - `Topology` (`FLOAT`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `Unnamed` (`CUSTOM`)
- **Tip:** When a color field is connected, it will be evaluated as a Vector data type, since color grids are not currently supported.


### Get Named Grid — `GeometryNodeGetNamedGrid`
- **Notes:** The Get Named Grid node retrieves a specific voxel grid from a volume geometry by its name. Each volume object can contain multiple grids (for example, density, color, temperature, or velocity), and this node allows accessing one of them for further processing in the node tree. The retrieved grid can then be sampled, modified, or converted to geometry using other grid or SDF nodes.
- **Inputs:**
  - `Volume` (`GEOMETRY`)
  - `Name` (`STRING`)
  - `Remove` (`BOOLEAN`)
- **Outputs:**
  - `Volume` (`GEOMETRY`)
  - `Grid` (`FLOAT`)


### Grid Dilate & Erode — `GeometryNodeGridDilateAndErode`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Morphological dilate/erode on a volume grid.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Connectivity` (`MENU`)
  - `Tiles` (`MENU`)
  - `Steps` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### Grid Info — `GeometryNodeGridInfo`
- **Notes:** The Grid Info node retrieves structural and metadata information about a voxel grid. It provides details such as the grid’s spatial transform and background value, which describe how the grid is positioned in space and what value is stored in inactive (empty) voxels. This node is useful for inspecting or reusing grid parameters in other grid operations, such as aligning transforms, matching resolutions, or reconstructing fields with consistent background values.
- **Inputs:**
  - `Grid` (`FLOAT`)
- **Outputs:**
  - `Transform` (`MATRIX`)
  - `Background Value` (`FLOAT`)


### Grid Mean — `GeometryNodeGridMean`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Mean (box) filter over a volume grid.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Width` (`INT`)
  - `Iterations` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### Grid Median — `GeometryNodeGridMedian`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Median filter over a volume grid.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Width` (`INT`)
  - `Iterations` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### Grid to Mesh — `GeometryNodeGridToMesh`
- **Notes:** The Grid to Mesh node converts a voxel grid into a polygonal mesh by extracting an isosurface at a specified threshold value. This process is similar to the Marching Cubes algorithm used in many volumetric modeling systems. The resulting mesh represents the boundary where the grid’s values cross the given threshold—typically the surface of a signed distance field (SDF) or density grid. This makes it possible to convert procedural volumetric data into geometry for rendering, simulation, or further modeling operations.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Threshold` (`FLOAT`)
  - `Adaptivity` (`FLOAT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)


### Grid to Points — `GeometryNodeGridToPoints`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2.0 live readback.
- **Notes:** Convert active grid voxels to points with per-voxel outputs.
- **Inputs:**
  - `Grid` (`FLOAT`)
- **Outputs:**
  - `Points` (`GEOMETRY`)
  - `Value` (`FLOAT`)
  - `X` (`INT`)
  - `Y` (`INT`)
  - `Z` (`INT`)
  - `Is Tile` (`BOOLEAN`)
  - `Extent` (`INT`)


### Prune Grid — `GeometryNodeGridPrune`
- **Notes:** The Prune Grid node optimizes the storage of a voxel grid by collapsing uniform regions into coarser tiles or inner nodes, reducing memory usage and improving performance. This node performs the inverse operation of the Voxelize Grid node. While voxelization expands sparse tiles into dense voxels, pruning detects large uniform areas and replaces them with more compact representations. This is especially useful after operations that create large regions of constant values, such as filling, clipping, or thresholding.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Mode` (`MENU: Inactive, Threshold, SDF`)
  - `Threshold` (`FLOAT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### SDF Grid Boolean — `GeometryNodeSDFGridBoolean`
- **Notes:** The SDF Grid Boolean node performs boolean operations between two or more *Signed Distance Field (SDF)* grids. This allows combining, subtracting, or intersecting volumetric shapes directly in grid space, similar to mesh boolean operations but with smooth and continuous results. The node computes the resulting signed distance field by applying mathematical operations to the input grids, preserving the SDF property where each voxel stores the shortest distance to the nearest surface. This makes it useful for blending or sculpting complex volumes procedurally.
- **Inputs:**
  - `Grid 1` (`FLOAT`)
  - `Grid 2` (`FLOAT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### SDF Grid Fillet — `GeometryNodeSDFGridFillet`
- **Notes:** The SDF Fillet node smooths or rounds off concave internal corners in a Signed Distance Field (SDF) grid. It modifies the field to produce softer transitions between surfaces that...
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Iterations` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### SDF Grid Laplacian — `GeometryNodeSDFGridLaplacian`
- **Notes:** The SDF Grid Laplacian node applies Laplacian flow smoothing to a Signed Distance Field (SDF) grid. This process gradually smooths the surface of the SDF by diffusing fine details and noise across neighboring voxels, resulting in a cleaner, more uniform field. Laplacian flow is a computationally efficient alternative to mean curvature flow smoothing. It is particularly useful for refining SDFs generated from meshes or boolean operations, where sharp transitions or voxel artifacts may occur. The operation helps improve the quality of surfaces before converting the SDF back into a mesh.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Iterations` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### SDF Grid Mean Curvature — `GeometryNodeSDFGridMeanCurvature`
- **Notes:** The SDF Grid Mean Curvature node applies mean curvature flow smoothing to a Signed Distance Field (SDF) grid. This operation evolves the surface of the field over time based on its mean curvature, causing high-curvature (sharp or noisy) regions to smooth out more rapidly than flatter areas. Unlike simple averaging or Laplacian smoothing, mean curvature flow adapts to the geometric features of the surface, providing a more natural, shape-preserving smoothing process. It can be used to refine complex SDF surfaces, remove small artifacts, and create organically blended transitions between features. This node is particularly effective after boolean operations or mesh-to-SDF conversion, where the resulting fields may contain high-frequency noise.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Iterations` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### SDF Grid Mean — `GeometryNodeSDFGridMean`
- **Notes:** The SDF Grid Mean node applies mean (box) filter smoothing to amSigned Distance Field (SDF) grid. This operation averages voxel values within a local neighborhood to smooth out small variations and noise while preserving the overall shape of the field. The filter works as a fast, separable averaging operation—sometimes called a box filter—and is well suited for general-purpose smoothing or softening of SDF data after boolean, voxelization, or other volumetric operations.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Width` (`INT`)
  - `Iterations` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### SDF Grid Median — `GeometryNodeSDFGridMedian`
- **Notes:** The SDF Grid Median node applies a median filter to a Signed Distance Field (SDF) grid. This operation smooths the field by replacing each voxel value with the median of its neighboring values, effectively removing noise and small artifacts while preserving sharp features and edges. Unlike mean or Laplacian smoothing, the median filter is non-linear and better suited for cleaning up impulsive noise (isolated spikes or dips) in the grid. It maintains the overall structure and boundaries of the surface, making it useful for refining SDFs generated from noisy or voxelized meshes.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Width` (`INT`)
  - `Iterations` (`INT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### SDF Grid Offset — `GeometryNodeSDFGridOffset`
- **Notes:** The SDF Grid Offset node offsets the surface of a Signed Distance Field (SDF) by a specified world-space distance. This operation effectively dilates (expands) or erodes (contracts) the surface while maintaining the correct signed distance values across the field. A positive offset increases the surface thickness by pushing it outward, while a negative offset shrinks it inward. This is a fundamental operation in volumetric modeling, useful for adjusting wall thickness, creating shells, expanding collision volumes, or controlling blend margins between shapes.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Distance` (`FLOAT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### Set Grid Background — `GeometryNodeSetGridBackground`
- **Notes:** The Set Grid Background node defines the background value for a voxel grid. This value is used when sampling regions of the grid that do not contain any explicitly stored voxels, such as inactive areas or tiles that have not been initialized. By default, empty voxels in a grid evaluate to zero or another implicit value. This node allows customizing that behavior, which can be useful when constructing grids procedurally or when combining multiple grids.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Background` (`FLOAT`)
- **Outputs:**
  - `Grid` (`FLOAT`)


### Set Grid Transform — `GeometryNodeSetGridTransform`
- **Notes:** The Set Grid Transform node defines the spatial transform of a voxel grid, converting its index space (voxel coordinates) into object space. By default, voxel grids use a transform that maps integer voxel indices directly to object space coordinates. This node allows specifying a custom transform, enabling operations such as repositioning, rotating, or scaling a grid relative to an object or scene.
- **Inputs:**
  - `Grid` (`FLOAT`)
  - `Transform` (`MATRIX`)
- **Outputs:**
  - `Is Valid` (`BOOLEAN`)
  - `Grid` (`FLOAT`)


### Store Named Grid — `GeometryNodeStoreNamedGrid`
- **Notes:** The Store Named Grid node stores a voxel grid inside a volume geometry under a specified name. This allows multiple grids (such as density, temperature, or velocity) to be contained within a single volume object and accessed later using the Get Named Grid node. If a grid with the same name already exists in the input volume, it will be replaced by the new grid. This makes it possible to update or overwrite grids during a geometry node evaluation, for example when generating or modifying simulation fields.
- **Inputs:**
  - `Volume` (`GEOMETRY`)
  - `Name` (`STRING`)
  - `Grid` (`FLOAT`)
- **Outputs:**
  - `Volume` (`GEOMETRY`)


### Volume Cube — `GeometryNodeVolumeCube`
- **Notes:** The Volume Cube generates a volume by evaluating a density field on a 3D grid. The Density field can only depend on the Position Node. The grid points are equally spaced between the Min and Max bounds of the grid.
- **Inputs:**
  - `Density` (`FLOAT`)
  - `Background` (`FLOAT`)
  - `Min` (`VECTOR`)
  - `Max` (`VECTOR`)
  - `Resolution X` (`INT`)
  - `Resolution Y` (`INT`)
  - `Resolution Z` (`INT`)
- **Outputs:**
  - `Volume` (`GEOMETRY`)


### Volume to Mesh — `GeometryNodeVolumeToMesh`
- **Notes:** The Volume to Mesh node generates a mesh on the “surface” of a volume. The surface is defined by a threshold value. All voxels with a larger value than the threshold are considered to be inside.
- **Inputs:**
  - `Volume` (`GEOMETRY`)
  - `Resolution Mode` (`MENU: Grid, Amount, Size`)
  - `Voxel Size` (`FLOAT`)
  - `Voxel Amount` (`FLOAT`)
  - `Threshold` (`FLOAT`)
  - `Adaptivity` (`FLOAT`)
- **Outputs:**
  - `Mesh` (`GEOMETRY`)


### Voxel Index — `GeometryNodeInputVoxelIndex`
- **Notes:** The Voxel Index node outputs the integer index of the voxel that the field is currently being evaluated on. Unlike a position in object space, the voxel index refers to the discrete cell coordinates inside a voxel grid. This makes it possible to reason about neighboring voxels directly in index space, without converting through world or object space. This node can be combined with nodes such as Integer Math and Sample Grid Index to sample values from nearby voxels by offsetting the indices.
- **Inputs:** None
- **Outputs:**
  - `X` (`INT`)
  - `Y` (`INT`)
  - `Z` (`INT`)
  - `Is Tile` (`BOOLEAN`)
  - `Extent X` (`INT`)
  - `Extent Y` (`INT`)
  - `Extent Z` (`INT`)


### Voxelize Grid — `GeometryNodeGridVoxelize`
- **Notes:** The Voxelize Grid node converts all active tiles in a sparse voxel grid into fully populated voxel regions, removing sparseness. In voxel-based grids such as signed distance fields (SDF) or fog volumes, inactive areas are often stored as tiles—compact representations that save memory by not allocating individual voxel values. This node expands those tiles into explicit voxels, making every voxel within an active tile directly accessible and editable. This can be useful before performing operations that require dense voxel data, such as sampling, filtering, or arithmetic operations that depend on neighboring voxel values.
- **Inputs:**
  - `Grid` (`FLOAT`)
- **Outputs:**
  - `Grid` (`FLOAT`)
