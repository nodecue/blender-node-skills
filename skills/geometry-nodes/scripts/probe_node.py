"""Ask the running Blender what a node actually is. Build/Edit only.

Probing creates a node, so it creates Blender data — that is a write, and it does
not belong in Explain mode. Everything it creates lives in a uniquely named
temporary tree that is removed again, and the result says whether the removal
restored the counts it started from.

The reason this exists: a socket list is not a node. A mode/type property often
*replaces* the sockets rather than adding to them, so the sockets you read
depend on the properties you set first. This script sets them in the order you
give and reads back afterwards.

    # Blender CLI
    blender -b --python scripts/probe_node.py -- \
        '{"nodes": [{"bl_idname": "FunctionNodeRandomValue",
                     "properties": {"data_type": "BOOLEAN"}}]}'

    # a host Python channel
    import runpy
    g = runpy.run_path(SCRIPT, init_globals={"NODECUE_PARAMS": {...}})
    result = g["result"]

Parameters:
    bl_idname    a single node type, shorthand for nodes=[{...}]
    properties   property assignments for that single node
    nodes        [{"bl_idname": str, "properties": {...}, "label": str}]
    tree_type    default "GeometryNodeTree"

Never uses `bpy.ops.outliner.orphans_purge`: a broad purge would take the user's
unrelated unused datablocks with it.
"""

import json
import sys
import uuid

import bpy

_SKIP_PROPS = {
    "name", "label", "location", "location_absolute", "width", "height",
    "color", "use_custom_color", "mute", "hide", "select", "show_options",
    "show_preview", "show_texture", "parent", "warning_propagation",
}


def shape_vocabulary():
    """Which vocabulary this build draws with, from its own registered enum.

    `LINE` is registered only in the 5.x vocabulary, so the enum answers this
    without a version comparison - and keeps answering it correctly if a future
    build changes the shapes again.
    """
    try:
        items = {
            item.identifier
            for item in bpy.types.NodeSocket.bl_rna.properties["display_shape"].enum_items
        }
    except Exception:
        items = set()
    if not items:
        return "5.x" if bpy.app.version[0] >= 5 else "4.x"
    return "5.x" if "LINE" in items else "4.x"


# Collections a node create could plausibly grow. Counted before and after so
# cleanup can be reported rather than assumed.
_WATCHED = (
    "node_groups", "objects", "meshes", "materials", "images", "texts",
    "collections", "worlds",
)


def _jsonable(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bpy.types.ID):
        return {"id_name": value.name, "id_type": type(value).__name__}
    try:
        return [_jsonable(v) for v in value]
    except TypeError:
        return str(value)


def _counts():
    return {name: len(getattr(bpy.data, name)) for name in _WATCHED}


def _properties(node):
    out = {}
    for prop in node.bl_rna.properties:
        ident = prop.identifier
        if prop.is_readonly or ident.startswith("bl_") or ident in _SKIP_PROPS:
            continue
        rec = {"rna_type": prop.type}
        try:
            rec["value"] = _jsonable(getattr(node, ident))
        except Exception as exc:
            rec["error"] = f"{type(exc).__name__}: {exc}"
        if prop.type == "ENUM":
            items = [i.identifier for i in prop.enum_items]
            if not items:
                items = [i.identifier for i in getattr(prop, "enum_items_static", [])]
            rec["enum_items"] = items
        out[ident] = rec
    return out


def _socket(sock):
    rec = {
        "name": sock.name,
        "identifier": sock.identifier,
        "type": sock.type,
        "enabled": sock.enabled,
        "hide": sock.hide,
    }
    if hasattr(sock, "hide_value"):
        rec["hide_value"] = bool(sock.hide_value)
    shape = getattr(sock, "display_shape", None)
    if shape:
        rec["display_shape"] = shape
    has_def = hasattr(sock, "default_value")
    rec["has_default_value"] = has_def
    if has_def:
        rec["default_value"] = _jsonable(sock.default_value)
    # A menu socket takes a string whose legal values live on the socket, not in
    # any list this skill could ship.
    items = getattr(getattr(sock, "bl_rna", None), "properties", {})
    prop = items.get("default_value") if hasattr(items, "get") else None
    if prop is not None and prop.type == "ENUM":
        rec["menu_items"] = [i.identifier for i in prop.enum_items]
    return rec


def _probe_one(tree, spec):
    bl_idname = spec.get("bl_idname")
    if not bl_idname:
        return {"ok": False, "error": "spec has no bl_idname"}

    try:
        node = tree.nodes.new(bl_idname)
    except Exception as exc:
        # Not registered on this Blender is a real answer, not a crash.
        return {
            "ok": False,
            "bl_idname": bl_idname,
            "registered": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    applied, rejected = {}, {}
    for key, value in (spec.get("properties") or {}).items():
        try:
            setattr(node, key, value)
            applied[key] = _jsonable(getattr(node, key))
        except Exception as exc:
            rejected[key] = f"{type(exc).__name__}: {exc}"

    # A rejected property means the sockets below describe the node's default
    # mode, not the one that was asked for. Reporting them as the answer would be
    # worse than reporting nothing, so the probe fails.
    rec = {
        "ok": not rejected,
        "bl_idname": bl_idname,
        "registered": True,
        "created_as": node.name,
        "label": node.bl_label,
        "properties_applied": applied,
        "properties_rejected": rejected,
        # Read after the writes, never before: the properties decide the sockets.
        "properties": _properties(node),
        "inputs": [_socket(s) for s in node.inputs],
        "outputs": [_socket(s) for s in node.outputs],
        # A mode/type property removes the other variants outright on 5.2, but on
        # 4.5 and 5.1 it only disables them: they stay in node.inputs, keep their
        # names, and wiring to one silently does nothing. Wire from these.
        "active_inputs": [s.identifier for s in node.inputs if s.enabled],
        "active_outputs": [s.identifier for s in node.outputs if s.enabled],
        "inactive_inputs": [s.identifier for s in node.inputs if not s.enabled],
    }
    if rejected:
        rec["error"] = (
            "requested properties were not applied, so these sockets are the node's "
            f"default configuration and not the requested one: {sorted(rejected)}"
        )
    active = [s for s in node.inputs if s.enabled]
    names = [s.name for s in active]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        rec["duplicate_input_names"] = {
            name: [s.identifier for s in active if s.name == name] for name in dupes
        }
    tree.nodes.remove(node)
    return rec


def run(params=None):
    params = params or {}
    specs = params.get("nodes")
    if not specs:
        if not params.get("bl_idname"):
            return {"ok": False, "error": "pass `bl_idname` or `nodes`"}
        specs = [{"bl_idname": params["bl_idname"], "properties": params.get("properties")}]

    tree_type = params.get("tree_type", "GeometryNodeTree")
    vocabulary = shape_vocabulary()
    before = _counts()
    tree_name = "NodeCue probe %s" % uuid.uuid4().hex[:8]

    try:
        tree = bpy.data.node_groups.new(tree_name, tree_type)
    except Exception as exc:
        # Same shape of answer as a successful run, so a caller never has to
        # branch on whether `cleanup` is present.
        after = _counts()
        return {
            "ok": False,
            "blender": bpy.app.version_string,
            "blender_version": list(bpy.app.version),
            "shape_vocabulary": vocabulary,
            "probes": [],
            "probes_failed": len(specs),
            "error": f"could not create a {tree_type}: {type(exc).__name__}: {exc}",
            "cleanup": {
                "temp_tree": None,
                "removed": False,
                "counts_restored": before == after,
                "changed_counts": {k: [before[k], after[k]]
                                   for k in before if before[k] != after[k]},
                "method": "nothing was created; nothing to remove",
            },
        }

    probes, failed = [], 0
    try:
        for spec in specs:
            rec = _probe_one(tree, spec)
            failed += 0 if rec.get("ok") else 1
            probes.append(rec)
    finally:
        # Targeted removal of exactly the datablock this call created.
        removed = False
        existing = bpy.data.node_groups.get(tree.name)
        if existing is not None:
            bpy.data.node_groups.remove(existing)
            removed = True
        after = _counts()

    leaked = {k: [before[k], after[k]] for k in before if before[k] != after[k]}
    return {
        "ok": failed == 0,
        "blender": bpy.app.version_string,
        "blender_version": list(bpy.app.version),
        "shape_vocabulary": vocabulary,
        "probes": probes,
        "probes_failed": failed,
        "cleanup": {
            "temp_tree": tree_name,
            "removed": removed,
            "counts_restored": not leaked,
            "changed_counts": leaked,
            "method": "targeted remove; never orphans_purge",
        },
    }


def _emit(payload):
    print(json.dumps(payload, ensure_ascii=False, default=str))
    return payload


def _argv_params():
    if "--" not in sys.argv:
        return {}
    rest = sys.argv[sys.argv.index("--") + 1:]
    return json.loads(rest[0]) if rest else {}


if __name__ == "__main__":
    result = _emit(run(_argv_params()))
elif "NODECUE_PARAMS" in globals():
    result = _emit(run(NODECUE_PARAMS))  # noqa: F821  - injected by the host
