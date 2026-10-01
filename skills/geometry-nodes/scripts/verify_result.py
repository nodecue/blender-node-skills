"""Measure what a Geometry Nodes modifier actually produces. Build/Edit check.

A graph that reads back correctly can still store constants, zeros, or nothing
at all, and a node group with no user is dropped when the file is saved. This
script evaluates the group and reports values, not wiring:

- per named attribute: domain, data type, element count, min / max (vector and
  colour attributes by length), distinct values, and the fraction that is zero;
- per geometry component: element counts;
- whether the group survives a save (it has a user or a fake user).

Two ways to get geometry, usable together:

    object      evaluate an existing object's NODES modifier as it stands.
                Read-only: nothing is created or changed.
    samples     temporary hosts built for this call, each carrying a modifier
                with the group at its interface defaults:
                "cube", "uv_sphere", "monkey", "grid", "plane", "cylinder".
                This creates data, so it is a write: Build/Edit only. Exactly
                what was created is removed again and the counts are reported.

A value that should vary but does not is the failure this exists to catch. An
attribute is reported `constant` when every element of one evaluation holds
the same value; `findings` adds ATTRIBUTE_CONSTANT_EVERYWHERE when that holds
for every evaluated geometry, ATTRIBUTE_ALL_ZERO when every element is zero,
and ATTRIBUTE_MISSING for an expected name that no component carries. Whether
a constant is wrong depends on the request; the script reports, it does not
judge intent.

    # a host Python channel
    import runpy
    g = runpy.run_path(SCRIPT, init_globals={"NODECUE_PARAMS": {
        "tree": "My Group", "samples": ["cube", "uv_sphere"],
        "attributes": ["edge_distance"]}})
    result = g["result"]

    # Blender CLI
    blender -b file.blend --python scripts/verify_result.py -- '{"tree": "My Group"}'

Parameters:
    tree         node group name (required unless `object` is given)
    object       object whose NODES modifier to evaluate as it stands
    modifier     which NODES modifier on `object`, when it has several
    samples      list of sample shape names (see above); default none
    attributes   names to report; default every non-internal attribute that is
                 not a built-in (position, UV maps and similar are skipped)
    max_elements values read per attribute, default 200000

Unknown parameters are rejected. Never uses `bpy.ops.outliner.orphans_purge`.
"""

import json
import math
import sys

import bmesh
import bpy

_PARAMS = {"tree", "object", "modifier", "samples", "attributes", "max_elements"}
_SHAPES = ("cube", "uv_sphere", "monkey", "grid", "plane", "cylinder")
_BUILTIN = {
    "position", "radius", "id", "material_index", "sharp_face", "sharp_edge",
    "crease_edge", "crease_vert", "bevel_weight_edge", "bevel_weight_vert",
    "UVMap", "uv_map", "resolution", "cyclic", "curve_type", "normal_mode",
    "handle_left", "handle_right", "handle_type_left", "handle_type_right",
    "nurbs_order", "nurbs_weight", "knots_mode", "tilt", "instance_transform",
    ".reference_index",
}
_WATCHED = ("objects", "meshes", "node_groups")
_EPS = 1e-6


def _counts():
    return {name: len(getattr(bpy.data, name)) for name in _WATCHED}


def _sample_mesh(shape):
    bm = bmesh.new()
    if shape == "cube":
        bmesh.ops.create_cube(bm, size=2.0)
    elif shape == "uv_sphere":
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    elif shape == "monkey":
        bmesh.ops.create_monkey(bm)
    elif shape == "grid":
        bmesh.ops.create_grid(bm, x_segments=10, y_segments=10, size=1.0)
    elif shape == "plane":
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1.0)
    elif shape == "cylinder":
        bmesh.ops.create_cone(bm, cap_ends=True, segments=32,
                              radius1=1.0, radius2=1.0, depth=2.0)
    me = bpy.data.meshes.new(f"NodeCue verify {shape}")
    bm.to_mesh(me)
    bm.free()
    return me


def _values(attr, limit):
    """Scalar view of each element: the value, or the length of a vector."""
    data = attr.data
    n = min(len(data), limit)
    out = []
    for i in range(n):
        item = data[i]
        for key in ("value", "vector", "color"):
            if hasattr(item, key):
                v = getattr(item, key)
                break
        else:
            return None
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, (bool, int, float)):
            out.append(float(v))
        else:
            out.append(math.sqrt(sum(float(c) * float(c) for c in v)))
    return out


def _attr_stats(attr, limit):
    rec = {"domain": attr.domain, "data_type": attr.data_type, "count": len(attr.data)}
    vals = _values(attr, limit)
    if vals is None or not vals:
        rec["constant"] = None
        return rec
    if isinstance(vals[0], str):
        distinct = len(set(vals))
        rec.update(distinct=distinct, constant=distinct == 1)
        return rec
    distinct = len({round(v, 5) for v in vals})
    rec.update(
        min=round(min(vals), 6),
        max=round(max(vals), 6),
        distinct=distinct,
        constant=distinct == 1,
        zero_fraction=round(sum(1 for v in vals if abs(v) < _EPS) / len(vals), 4),
    )
    if len(attr.data) > len(vals):
        rec["sampled"] = len(vals)
    return rec


def _components(geometry):
    comps = {}
    mesh = geometry.mesh
    if mesh is not None:
        comps["mesh"] = (mesh, {"points": len(mesh.vertices), "edges": len(mesh.edges),
                                "faces": len(mesh.polygons)})
    cloud = geometry.pointcloud
    if cloud is not None:
        comps["pointcloud"] = (cloud, {"points": len(cloud.points)})
    curves = geometry.curves
    if curves is not None:
        comps["curves"] = (curves, {"points": len(curves.points),
                                    "curves": len(curves.curves)})
    inst = geometry.instances_pointcloud()
    if inst is not None:
        comps["instances"] = (inst, {"instances": len(inst.points)})
    return comps


def _measure(obj, wanted, limit):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    out = {"components": {}, "attributes": {}}
    # The component data lives only as long as this GeometrySet does.
    geometry = evaluated.evaluated_geometry()
    for kind, (data, counts) in _components(geometry).items():
        out["components"][kind] = counts
        for attr in data.attributes:
            name = attr.name
            if wanted is not None:
                if name not in wanted:
                    continue
            elif name.startswith(".") or name in _BUILTIN:
                continue
            key = name if kind == "mesh" else f"{kind}:{name}"
            out["attributes"][key] = _attr_stats(attr, limit)
    return out


def _modifier(obj, wanted):
    mods = [m for m in obj.modifiers if m.type == "NODES" and m.node_group]
    if wanted:
        mods = [m for m in mods if m.name == wanted]
    return mods


def _findings(tree, evaluations, wanted):
    findings = []
    if tree is not None and tree.users == 0 and not tree.use_fake_user:
        findings.append({
            "code": "GROUP_NOT_SAVED",
            "severity": "error",
            "message": "the group has no user and no fake user; saving drops it. "
                       "Set use_fake_user or keep it on a modifier, then re-check.",
        })
    if not evaluations:
        return findings
    seen = {}
    for ev in evaluations:
        for name, rec in ev["attributes"].items():
            seen.setdefault(name.split(":")[-1], []).append(rec)
    for name in sorted(wanted or []):
        if name not in seen:
            findings.append({"code": "ATTRIBUTE_MISSING", "severity": "error",
                             "attribute": name})
    for name, recs in sorted(seen.items()):
        if all(r.get("zero_fraction") == 1.0 for r in recs):
            findings.append({"code": "ATTRIBUTE_ALL_ZERO", "severity": "warning",
                             "attribute": name})
        elif all(r.get("constant") for r in recs) and any(r["count"] > 1 for r in recs):
            findings.append({"code": "ATTRIBUTE_CONSTANT_EVERYWHERE", "severity": "warning",
                             "attribute": name,
                             "values": sorted({r.get("min") for r in recs}, key=str)})
    for ev in evaluations:
        if not any(any(v for v in c.values()) for c in ev["components"].values()):
            findings.append({"code": "GEOMETRY_EMPTY", "severity": "warning",
                             "source": ev["source"]})
    return findings


def run(params=None):
    params = params or {}
    unknown = sorted(set(params) - _PARAMS)
    if unknown:
        return {"ok": False, "error": f"unknown parameter(s) {unknown}",
                "accepted": sorted(_PARAMS)}
    samples = params.get("samples") or []
    bad = [s for s in samples if s not in _SHAPES]
    if bad:
        return {"ok": False, "error": f"unknown sample shape(s) {bad}",
                "shapes": list(_SHAPES)}
    wanted = params.get("attributes")
    wanted = set(wanted) if wanted else None
    limit = int(params.get("max_elements", 200000))

    tree = None
    evaluations = []
    obj_name = params.get("object")
    if obj_name:
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            return {"ok": False, "error": f"object {obj_name!r} not found",
                    "candidates": [o.name for o in bpy.data.objects][:50]}
        mods = _modifier(obj, params.get("modifier"))
        if len(mods) != 1:
            return {"ok": False,
                    "error": f"{obj.name!r} has {len(mods)} matching NODES modifiers; "
                             "pass `modifier` to choose",
                    "candidates": [m.name for m in _modifier(obj, None)]}
        tree = mods[0].node_group
        ev = _measure(obj, wanted, limit)
        ev["source"] = f"object:{obj.name}/{mods[0].name}"
        evaluations.append(ev)

    name = params.get("tree")
    if name:
        named = bpy.data.node_groups.get(name)
        if named is None or named.bl_idname != "GeometryNodeTree":
            return {"ok": False, "error": f"no GeometryNodeTree named {name!r}",
                    "candidates": [g.name for g in bpy.data.node_groups
                                   if g.bl_idname == "GeometryNodeTree"]}
        if tree is not None and tree is not named:
            return {"ok": False,
                    "error": f"`object` uses {tree.name!r}, not {name!r}"}
        tree = named
    if tree is None:
        return {"ok": False, "error": "pass `tree` or `object`"}
    if samples and not getattr(tree, "is_modifier", True):
        return {"ok": False,
                "error": f"{tree.name!r} is not a modifier group; a tool is verified "
                         "on the mesh it edited, not on sample hosts"}

    cleanup = None
    if samples:
        before = _counts()
        created_objects, created_meshes = [], []
        users_before = tree.users
        try:
            for shape in samples:
                me = _sample_mesh(shape)
                created_meshes.append(me.name)
                ob = bpy.data.objects.new(f"NodeCue verify {shape}", me)
                created_objects.append(ob)
                bpy.context.scene.collection.objects.link(ob)
                ob.modifiers.new("NodeCue verify", "NODES").node_group = tree
            for shape, ob in zip(samples, created_objects):
                ev = _measure(ob, wanted, limit)
                ev["source"] = f"sample:{shape}"
                evaluations.append(ev)
        finally:
            for ob in created_objects:
                bpy.data.objects.remove(ob, do_unlink=True)
            # Removing an object can free its mesh with it; look each one up by
            # the name it was created under rather than holding a dead reference.
            for mesh_name in created_meshes:
                me = bpy.data.meshes.get(mesh_name)
                if me is not None:
                    bpy.data.meshes.remove(me, do_unlink=True)
        after = _counts()
        leaked = {k: [before[k], after[k]] for k in before if before[k] != after[k]}
        cleanup = {"counts_restored": not leaked, "changed_counts": leaked,
                   "group_users_restored": tree.users == users_before,
                   "method": "targeted remove of the sample objects and meshes"}

    persistence = {"users": tree.users, "use_fake_user": tree.use_fake_user,
                   "survives_save": tree.users > 0 or tree.use_fake_user}
    findings = _findings(tree, evaluations, wanted)
    payload = {
        "ok": not any(f["severity"] == "error" for f in findings),
        "blender": bpy.app.version_string,
        "tree": tree.name,
        "persistence": persistence,
        "evaluations": evaluations,
        "findings": findings,
    }
    if cleanup is not None:
        payload["cleanup"] = cleanup
    return payload


def _emit(payload):
    print(json.dumps(payload, ensure_ascii=False, default=str, separators=(",", ":")))
    return payload


def _argv_params():
    if "--" not in sys.argv:
        return {}
    rest = sys.argv[sys.argv.index("--") + 1:]
    return json.loads(rest[0]) if rest else {}


if __name__ == "__main__":
    result = _emit(run(_argv_params()))
elif "NODECUE_PARAMS" in globals():
    result = run(NODECUE_PARAMS)  # noqa: F821  - injected by the host
