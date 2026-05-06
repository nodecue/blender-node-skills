---
id: workflow-id-here
name: Human-readable Workflow Name
description: "One-line: what this workflow achieves."
category: instancing | deformation | generation | conversion | branching
tags: tag1, tag2
---

## Workflow Name

**Intent:** What problem does this solve, in plain language.

## Evidence

- `rules/example.md`: exact `Node Name — bl_idname` entries or readback artifact that verifies this pattern.

## Signature

- **In:** `param_name` (SOCKET_TYPE/geometry_subtype) — what it expects
- **Out:** `param_name` (SOCKET_TYPE/geometry_subtype) — what it produces
- **Params:** `param_name` (TYPE) — user-controllable values

## Data Flow

```
source ─[TYPE]─→ Node A ─[TYPE]─→ Node B ─[TYPE]─→ result
                                     ↑
field_source ─[TYPE]─────────────  Socket Name
```

## Core Chain

1. `Node Name — bl_idname`
   - `Input Socket` ← source description
   - `Output Socket` → where it goes
2. `Node Name — bl_idname`
   - `Input Socket` ← step N output
   - key property: `property_name` = `VALUE`

## Field Drivers (optional)

Describe optional field extensions that add variation or control.
- **Pattern name**: `Producer.Output` → optional shaping → `Consumer.Socket`

## Composes With

- → [other-workflow-id] for downstream use case
- [upstream-workflow-id] → can replace a step in this workflow

## Common Mistakes

- Mistake description and why it happens
