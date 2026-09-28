"""Read a Geometry Nodes tree. Read-only — safe in Explain mode.

Returns the running Blender's answer for node identities, socket identifiers,
writable properties, links, the group interface, and whether a geometry trunk
actually reaches the active Group Output. It makes no repair decisions and
writes nothing.

Three ways to invoke the same file, none of which re-author its body:

    # 1. Blender CLI
    blender -b --python scripts/read_graph.py -- '{"tree": "Geometry Nodes"}'

    # 2. a host Python channel that captures stdout and/or a `result` variable
    import runpy
    g = runpy.run_path(SCRIPT, init_globals={"NODECUE_PARAMS": {"tree": "Geometry Nodes"}})
    result = g["result"]

    # 3. import and call
    runpy.run_path(SCRIPT)["run"]({"tree": "Geometry Nodes"})

Parameters (all optional):
    tree            node group name to read; skips resolution entirely, and is
                    rejected if it names something that is not a GeometryNodeTree
    object          object whose NODES modifier holds the tree
    modifier        which NODES modifier, by name. Required when the object has
                    more than one: the script refuses to guess
    scope           {"nodes": [names], "selected_only": bool, "limit": int,
                     "cursor": "<node name>", "links": bool, "interface": bool,
                     "properties": bool}

Scoping and `limit` never drop a link silently. Links that cross the scope
boundary come back marked `boundary`, and the result carries `scope.truncated`
plus `scope.next_cursor` so a caller knows there is more and where to resume.

The result always carries `ok`. On failure it carries `error` and, where it can,
`candidates` so the caller can ask a narrower question rather than guess.
"""

import json
import sys

import bpy

# Node appearance and layout. Writable, and never what a graph means.
_SKIP_PROPS = {
    "name", "label", "location", "location_absolute", "width", "height",
    "color", "use_custom_color", "mute", "hide", "select", "show_options",
    "show_preview", "show_texture", "parent", "warning_propagation",
}
_STRUCTURAL = {"NodeFrame", "NodeReroute"}


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


def _jsonable(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bpy.types.ID):
        return {"id_name": value.name, "id_type": type(value).__name__}
    try:
        return [_jsonable(v) for v in value]
    except TypeError:
        return str(value)


def _writable_properties(node):
    out = {}
    for prop in node.bl_rna.properties:
        ident = prop.identifier
        if prop.is_readonly or ident.startswith("bl_") or ident in _SKIP_PROPS:
            continue
        try:
            value = getattr(node, ident)
        except Exception as exc:  # a property that cannot be read is data too
            out[ident] = {"error": f"{type(exc).__name__}: {exc}"}
            continue
        rec = {"value": _jsonable(value), "rna_type": prop.type}
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
        "is_linked": sock.is_linked,
    }
    if hasattr(sock, "hide_value"):
        rec["hide_value"] = bool(sock.hide_value)
    shape = getattr(sock, "display_shape", None)
    if shape:
        rec["display_shape"] = shape
    has_def = hasattr(sock, "default_value")
    rec["has_default_value"] = has_def
    if has_def and not sock.is_linked:
        rec["default_value"] = _jsonable(sock.default_value)
    return rec


def _location_absolute(node):
    """Editor-space origin. Prefer RNA; otherwise walk parent-relative locations."""
    abs_loc = getattr(node, "location_absolute", None)
    if abs_loc is not None:
        return [float(abs_loc[0]), float(abs_loc[1])]
    x, y = float(node.location[0]), float(node.location[1])
    parent = node.parent
    while parent is not None:
        x += float(parent.location[0])
        y += float(parent.location[1])
        parent = parent.parent
    return [x, y]


def _node(node, want_properties=True):
    rec = {
        "name": node.name,
        "bl_idname": node.bl_idname,
        "label": node.label,
        "structural": node.bl_idname in _STRUCTURAL,
        "parent": node.parent.name if node.parent else None,
        "location": [float(node.location[0]), float(node.location[1])],
        "location_absolute": _location_absolute(node),
        "width": float(getattr(node, "width", 0.0) or 0.0),
        "height": float(getattr(node, "height", 0.0) or 0.0),
        "mute": node.mute,
        "select": node.select,
        "inputs": [_socket(s) for s in node.inputs],
        "outputs": [_socket(s) for s in node.outputs],
    }
    dims = getattr(node, "dimensions", None)
    if dims is not None:
        rec["dimensions"] = [float(dims[0]), float(dims[1])]
    if want_properties:
        rec["properties"] = _writable_properties(node)
    if node.bl_idname == "GeometryNodeGroup" and node.node_tree:
        rec["node_tree"] = node.node_tree.name
    return rec


def _interface(tree):
    items = []
    for item in tree.interface.items_tree:
        rec = {
            "item_type": item.item_type,
            "name": item.name,
            "identifier": getattr(item, "identifier", None),
            "in_out": getattr(item, "in_out", None),
            "parent": item.parent.name if getattr(item, "parent", None) else None,
        }
        if item.item_type == "SOCKET":
            rec["socket_type"] = item.socket_type
            if hasattr(item, "default_value"):
                rec["default_value"] = _jsonable(item.default_value)
        items.append(rec)
    return items


def _trunk(tree):
    """Is there an observable geometry path to the active Group Output?"""
    outputs = [n for n in tree.nodes if n.bl_idname == "NodeGroupOutput"]
    active = next((n for n in outputs if n.is_active_output), None) or (
        outputs[0] if outputs else None
    )
    if active is None:
        return {"group_output": None, "reachable": False,
                "reason": "no NodeGroupOutput in this tree"}

    geometry_in = [s for s in active.inputs if s.type == "GEOMETRY"]
    seeds = [s for s in geometry_in if s.is_linked]
    if not seeds:
        return {
            "group_output": active.name,
            "reachable": False,
            "reason": "no geometry socket on the active Group Output is linked",
            "geometry_inputs": [s.identifier for s in geometry_in],
        }

    # 1. Geometry trunk: follow ONLY geometry data flow to active Group Output
    trunk_set, frontier, trunk = set(), [s for s in seeds], []
    visited_socks = set()
    while frontier:
        sock = frontier.pop()
        if sock in visited_socks:
            continue
        visited_socks.add(sock)
        for link in sock.links:
            node = link.from_node
            if node.bl_idname in _STRUCTURAL:
                for inp in node.inputs:
                    if inp.type == "GEOMETRY" and inp.is_linked:
                        frontier.append(inp)
                continue
            if node.name not in trunk_set and node.bl_idname != "NodeGroupOutput":
                trunk_set.add(node.name)
                trunk.append(node.name)
            for inp in node.inputs:
                if inp.type == "GEOMETRY" and inp.is_linked:
                    frontier.append(inp)

    # 2. Dependency nodes: field/control contributors feeding trunk nodes
    dep_set, dep_frontier, dep_nodes = set(), [], []
    visited_dep_socks = set()
    for node_name in trunk:
        node = tree.nodes.get(node_name)
        if not node:
            continue
        for inp in node.inputs:
            if inp.type != "GEOMETRY" and inp.is_linked:
                dep_frontier.append(inp)

    while dep_frontier:
        sock = dep_frontier.pop()
        if sock in visited_dep_socks:
            continue
        visited_dep_socks.add(sock)
        for link in sock.links:
            node = link.from_node
            if node.name in trunk_set or node.bl_idname == "NodeGroupOutput":
                continue
            if node.bl_idname not in _STRUCTURAL and node.name not in dep_set:
                dep_set.add(node.name)
                dep_nodes.append(node.name)
            for inp in node.inputs:
                if inp.is_linked:
                    dep_frontier.append(inp)

    functional = [
        n.name for n in tree.nodes
        if n.bl_idname not in _STRUCTURAL and n.bl_idname != "NodeGroupOutput"
    ]
    return {
        "group_output": active.name,
        "reachable": True,
        "trunk_nodes": trunk,
        "dependency_nodes": dep_nodes,
        "off_trunk_nodes": [n for n in functional if n not in trunk_set and n not in dep_set],
    }


def _resolve(params):
    """Resolve one tree, and say which rule resolved it.

    The active modifier is the last rule, not the first: a user editing a nested
    group inside the node editor is not editing the modifier's top-level tree.
    """
    candidates = []

    name = params.get("tree")
    if name:
        tree = bpy.data.node_groups.get(name)
        if tree is None:
            return None, "named tree not found", [g.name for g in bpy.data.node_groups]
        if tree.bl_idname != "GeometryNodeTree":
            return (
                None,
                f"{name!r} is a {tree.bl_idname}, not a GeometryNodeTree",
                [g.name for g in bpy.data.node_groups if g.bl_idname == "GeometryNodeTree"],
            )
        return tree, "explicit `tree` parameter", None

    # The editor's edit_tree is what the user is actually looking at, nested
    # groups included. bpy.context has no area in a background channel, so walk
    # the window manager instead of relying on context.space_data.
    for wm in bpy.data.window_managers:
        for win in wm.windows:
            for area in win.screen.areas:
                if area.type != "NODE_EDITOR":
                    continue
                space = area.spaces.active
                if getattr(space, "tree_type", None) != "GeometryNodeTree":
                    continue
                edit = getattr(space, "edit_tree", None)
                if edit is not None:
                    return edit, "node editor edit_tree", None
                candidates.append(f"node editor with no tree open ({win.screen.name})")

    obj_name = params.get("object")
    obj = bpy.data.objects.get(obj_name) if obj_name else None
    if obj_name and obj is None:
        return None, f"object {obj_name!r} not found", [o.name for o in bpy.data.objects]
    if obj is None:
        obj = getattr(bpy.context, "object", None) or getattr(
            bpy.context.view_layer.objects, "active", None
        )
    if obj is not None:
        mods = [m for m in obj.modifiers if m.type == "NODES" and m.node_group]
        wanted = params.get("modifier")
        if wanted:
            chosen = next((m for m in mods if m.name == wanted), None)
            if chosen is None:
                return (
                    None,
                    f"no NODES modifier named {wanted!r} on {obj.name!r}",
                    [m.name for m in mods],
                )
            return (
                chosen.node_group,
                f"explicit `modifier` {chosen.name!r} on {obj.name!r}",
                None,
            )
        if len(mods) == 1:
            return mods[0].node_group, f"sole NODES modifier on {obj.name!r}", None
        if len(mods) > 1:
            # Guessing which of several the user meant is how a read ends up
            # describing a different graph than the one on screen.
            return (
                None,
                f"{obj.name!r} has {len(mods)} NODES modifiers; pass `modifier` to choose",
                [f"{obj.name}/{m.name} -> {m.node_group.name}" for m in mods],
            )

    trees = [g.name for g in bpy.data.node_groups if g.bl_idname == "GeometryNodeTree"]
    return None, "no unambiguous tree", candidates + trees


def _link_record(link, in_scope):
    """One link. Outside the node scope it is kept as a stub, never dropped.

    A scoped read that silently omits the links crossing its own boundary is
    unreadable: the nodes look unconnected. The stub keeps the edge and says
    which end left the scope.
    """
    rec = {
        "from_node": link.from_node.name,
        "from_socket": link.from_socket.name,
        "from_identifier": link.from_socket.identifier,
        "to_node": link.to_node.name,
        "to_socket": link.to_socket.name,
        "to_identifier": link.to_socket.identifier,
        "is_valid": link.is_valid,
        "is_muted": link.is_muted,
    }
    inside_from = link.from_node.name in in_scope
    inside_to = link.to_node.name in in_scope
    if not (inside_from and inside_to):
        rec["boundary"] = "from" if inside_to else "to" if inside_from else "both"
    return rec


def run(params=None):
    params = params or {}
    scope = params.get("scope") or {}
    vocabulary = shape_vocabulary()

    tree, how, candidates = _resolve(params)
    if tree is None:
        return {
            "ok": False,
            "blender": bpy.app.version_string,
            "error": how,
            "candidates": candidates,
            "hint": "pass {'tree': '<node group name>'} to read one directly",
        }

    selected = list(tree.nodes)
    if scope.get("selected_only"):
        selected = [n for n in selected if n.select]
    wanted = scope.get("nodes")
    if wanted:
        wanted = set(wanted)
        selected = [n for n in selected if n.name in wanted]
        missing = sorted(wanted - {n.name for n in selected})
    else:
        missing = []
    scoped = bool(scope.get("selected_only") or wanted)

    # Explicit bounds. A cursor is the name of the node to resume at, so it stays
    # valid across calls in a way an index does not.
    limit = scope.get("limit")
    cursor = scope.get("cursor")
    truncated = False
    next_cursor = None
    ordered = selected
    if cursor is not None:
        names = [n.name for n in ordered]
        if cursor not in names:
            return {
                "ok": False,
                "blender": bpy.app.version_string,
                "error": f"cursor {cursor!r} is not a node in this scope",
                "candidates": names[:50],
            }
        ordered = ordered[names.index(cursor):]
    if limit is not None:
        limit = int(limit)
        if limit < 1:
            return {"ok": False, "blender": bpy.app.version_string,
                    "error": "scope.limit must be at least 1"}
        if len(ordered) > limit:
            truncated = True
            next_cursor = ordered[limit].name
            ordered = ordered[:limit]

    in_scope = {n.name for n in ordered}

    users = [
        {"object": ob.name, "modifier": m.name}
        for ob in bpy.data.objects
        for m in ob.modifiers
        if m.type == "NODES" and m.node_group is tree
    ]

    payload = {
        "ok": True,
        "blender": bpy.app.version_string,
        "blender_version": list(bpy.app.version),
        "shape_vocabulary": vocabulary,
        "resolved_by": how,
        "tree": {
            "name": tree.name,
            "bl_idname": tree.bl_idname,
            "is_modifier": getattr(tree, "is_modifier", None),
            "is_tool": getattr(tree, "is_tool", None),
            "used_by": users,
            "node_count": len(tree.nodes),
            "link_count": len(tree.links),
        },
        "active_node": tree.nodes.active.name if tree.nodes.active else None,
        "selected_nodes": [n.name for n in tree.nodes
                           if n.select and n.bl_idname not in _STRUCTURAL],
        "selected_structural": [n.name for n in tree.nodes
                                if n.select and n.bl_idname in _STRUCTURAL],
        "nodes": [_node(n, scope.get("properties", True)) for n in ordered],
        "scope_missing_nodes": missing,
        "scope": {
            "scoped": scoped,
            "returned": len(ordered),
            "of": len(selected),
            "limit": limit,
            "cursor": cursor,
            "truncated": truncated,
            "next_cursor": next_cursor,
        },
        "output_trunk": _trunk(tree),
    }
    if scope.get("links", True):
        if scoped or truncated:
            # Only links that touch the scope, with the crossing ones marked.
            links = [l for l in tree.links
                     if l.from_node.name in in_scope or l.to_node.name in in_scope]
        else:
            links = list(tree.links)
        payload["links"] = [_link_record(l, in_scope) for l in links]
        payload["links_scoped"] = scoped or truncated
        payload["boundary_links"] = sum(1 for r in payload["links"] if "boundary" in r)
    if scope.get("interface", True):
        payload["interface"] = _interface(tree)
    return payload


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
