---
id: points-to-volume-to-mesh
name: Points to Volume to Mesh
description: "Generate organic blobby mesh from a point cloud via volume intermediate."
category: generation
tags: points, volume, mesh, organic, blob, moss, coral, rock
blender_support: "5.0+"
blender_verified: 5.1.1
status: stable
---

## Points to Volume to Mesh

**Intent:** Create an organic, amorphous solid mesh from scattered points. By converting points to a volume (voxel grid) and back to mesh, nearby points merge into smooth blobby shapes. Useful for moss, coral, rock formations, cloud shapes, biological growths.

## Evidence

- `rules/point.md`: `GeometryNodePointsToVolume`, `GeometryNodeDistributePointsOnFaces`
- `rules/volume-operations.md`: `GeometryNodeVolumeToMesh`
- `rules/mesh-operations.md`: `GeometryNodeSubdivisionSurface`
- `rules/utilities-misc.md`: `FunctionNodeRandomValue`
- `rules/utilities-misc.md`: `GeometryNodeJoinGeometry`

## Signature

- **In:** `points` (GEOMETRY/point cloud) — source points, typically from Distribute Points on Faces
- **Out:** `blob_mesh` (GEOMETRY/mesh) — organic solid mesh
- **Params:** `radius` (FLOAT) — per-point volume radius, `voxel_amount` (INT) — resolution

## Data Flow

```
points ─[GEOMETRY]─→ Points to Volume ─[GEOMETRY/volume]─→ Volume to Mesh ─[GEOMETRY/mesh]─→ Subdivision Surface ─→ blob_mesh
                          ↑                                      ↑
                    radius (per-point)                    voxel_amount (shared)
```

## Core Chain

1. `Points to Volume — GeometryNodePointsToVolume`
   - `Points` ← input point cloud
   - `Radius` ← base radius (optionally randomized via Random Value for natural irregularity)
   - `Voxel Amount` ← resolution control
   - Output: volume geometry
2. `Volume to Mesh — GeometryNodeVolumeToMesh`
   - `Volume` ← step 1 output
   - `Voxel Amount` ← same resolution value as step 1 for consistent detail
   - Output: mesh geometry
3. `Subdivision Surface — GeometryNodeSubdivisionSurface` (optional)
   - `Mesh` ← step 2 output
   - `Level` ← 1 or 2 for smoothing
   - Output: smoothed organic mesh

## Key Properties

- Use the same `Voxel Amount` for both Points to Volume and Volume to Mesh to keep resolution consistent
- Randomizing radius per point (via Random Value with min/max bounds) gives natural irregularity

## Downstream Usage

- → Set Material for organic material assignment
- → Distribute Points on Faces again for secondary scatter (e.g. moss strands on moss blobs)
- → Join Geometry with original mesh

## Composes With

- [density-controlled-scatter](density-controlled-scatter.md) upstream when the source points should be controlled by a surface density field.
- [stitching-archetype](stitching-archetype.md) downstream when the blob mesh should be joined with other generated geometry.

## Common Mistakes

- Voxel Amount too low — blobby shapes lose detail and merge into a single lump
- Voxel Amount too high — slow performance, mesh becomes too detailed
- Forgetting that this is a representation conversion: point attributes are lost after volume stage
