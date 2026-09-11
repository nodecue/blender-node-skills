---
title: Node-Group and Asset Reuse
description: "How to decide whether an existing node group answers the request, how to look without mutating the project, and what to check on a candidate before wiring it."
last_verified: "2026-09-02"
---

# Reuse: existing node groups and assets

**Read this only when** the request might already be answered by a node group that
exists — an assembly, a named effect the user expects Blender to have, a repeat of
something the file already does. An ordinary build does not need it.

There is no inventory here. What a library holds is read at runtime; a shipped list goes
stale, and this one already has: a version that was documented as carrying three bundled
Geometry Nodes files turned out to carry four.

## An intent's answer may not be a node

Enumerating node types is the reliable way to find a node, and it cannot find what is not
a node type. Every asset node group reads back as `GeometryNodeGroup`, so there is no
identifier to search for. When an enumeration returns a node whose *name* fits but whose
*sockets* do not answer the request, look for an asset before concluding the feature is
missing. The closest-named built-in node is not evidence that it is the answer.

## Search order

1. **Node groups already in the current `.blend`.** Free, and the user's own vocabulary.
2. **Blender's bundled asset libraries.** Blender's own datafiles — no permission needed
   to read them. Whether they contain anything general-purpose is a version fact:
   `versions.md`.
3. **The user's configured asset libraries.** Theirs, and only the ones they configured.

`scripts/inspect_assets.py` walks this: `libraries` → `files` → `groups` → `inspect`.
Discovery is read-only. Deep inspection loads temporarily and removes what it loaded.

## Access policy

Only Blender's bundled asset root and the paths in the user's configured asset libraries
are readable. A path outside every configured root is refused, and the refusal names the
allowed roots — ask the user to name or authorize that path rather than reaching for it.
Never scan above a configured root, and never reach the network.

Reading a library is not the same as changing the project. Inspection is safe in Explain
mode; **appending or linking a group into the working file is a Build/Edit mutation** and
belongs to the caller, not to inspection.

## Deciding whether to look at all

Inspecting costs a few calls. It is worth it when the request names something composite
("scatter", "array", "cloth", "tube along a curve"), when the user's own file already
contains groups with related names, or when a first enumeration produced a node whose
sockets do not match the request. It is not worth it for a two-node operation you can
already name.

## What to check on a candidate

Read these off the group as it exists in the running Blender, not off any description:

- **Semantic fit.** What the group is *for*, from its interface and asset description —
  not from its name. A name is a hint; the interface is the claim.
- **The interface as it is now.** Names, identifiers, socket types, panels, defaults.
  Interface socket names are **not unique**: a bundled dynamics group exposes two inputs
  both named `Gravity`. Resolve by identifier.
- **Dependencies, measured per asset.** Loading one group brings in whatever it depends
  on, and the weight is a property of that asset rather than of the library. Measured on
  one install: one essentials group brought in a single extra group; one dynamics group
  brought in 45; one third-party group brought in 22 datablocks including objects and
  meshes. Read the number, do not assume it.
- **Output semantics.** What component type comes out, and whether it is instanced or
  real. A group that returns instances changes what the rest of your graph may do.

## Reuse or rebuild

The question is not how many nodes the group contains. It is whether you can explain what
you wired and why.

- A group whose interface you can read in one pass and whose purpose matches the request
  is worth using, however many nodes are inside it — the implementation cost is the part
  you avoid.
- A group with panels and a wide interface is a sub-product with its own UI. Every input
  is a decision you either make deliberately or leave at a default you have not inspected.
  Use it when the request covers most of what it does; build when the request uses one
  corner of it.
- A group you cannot explain is not reusable even if it works. You will have to describe
  the result to the user.

## When to ask instead of choosing

Present candidates rather than picking silently when two or more fit the intent, when the
best fit lives in the user's own library rather than the bundled one, or when reuse would
change the shape of the result (instances instead of real geometry, a different component
type). A library a user collected for exploration is a set of candidates to put in front
of them; one kept for efficiency invites reuse.

## Link or append

- **Append** when the group should travel with the file, when the user may edit it, or
  when the source library may move.
- **Link** when the source is a library the user maintains deliberately and expects
  updates from. Linking makes the file depend on that path.

Say which one you did and what came in with it.

## After loading

Read the group node's sockets back from the running Blender before wiring anything. The
interface you get is the one in this version's file — not the one in any table, including
one you read a moment ago from a different version.

## Recording what you learned

When a reused group turns out to have a verified project-specific meaning — what it is
for in this project, an external dependency it needs, an interface subtlety that cost you
a repair — that belongs in the project's `NODECUE.md`, with the Blender version and the
group identity that make it checkable. Not the interface itself: that is read live every
time.
