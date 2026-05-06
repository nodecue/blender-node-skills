## Core Patterns

Reusable multi-node composition patterns that cannot be derived from individual node rules.

### Field & Attribute
- [`capture-then-propagate.md`](capture-then-propagate.md): Freeze field values with Capture Attribute before geometry changes to prevent re-evaluation.
- [`material-attribute-handoff.md`](material-attribute-handoff.md): Preserve material decisions or numeric masks through geometry.
- [`index-normalized-shaping.md`](index-normalized-shaping.md): Shape per-element values along a sequence using Index normalization + Float Curve + Map Range.

### Vector Math
- [`normal-projection-removal.md`](normal-projection-removal.md): Remove normal component from a vector via dot product → scale → subtract. For surface-preserving deformation.
- [`surface-displacement.md`](surface-displacement.md): Move geometry with Set Position using verified vector and field drivers.

### Instancing
- [`density-controlled-scatter.md`](density-controlled-scatter.md): Control surface scatter with boolean or float density fields.

### Representation Conversion
- [`points-to-volume-to-mesh.md`](points-to-volume-to-mesh.md): Convert point cloud → volume → mesh for organic blob shapes.

### Control Flow (Repeat Zones)
- [`repeat-zone-iterative-smoothing.md`](repeat-zone-iterative-smoothing.md): Multi-pass smoothing/relaxation using Repeat Zone with Blur Attribute or manual averaging.
- [`repeat-zone-selection-expansion.md`](repeat-zone-selection-expansion.md): Grow boolean selection outward by N rings via Repeat Zone + domain hopping.
