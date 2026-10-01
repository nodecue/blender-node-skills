"""Deterministic Geometry Nodes layout for an explicit authorized node set.

The caller supplies authorized names, trunk order, dependency-to-consumer pairs,
and frame groups. This script does not infer semantic grouping and does not
evaluate whether the graph result is correct.

    blender -b --python scripts/layout_graph.py -- '{
        "op": "check",
        "tree": "Geometry Nodes",
        "nodes": ["Grid", "Set Position", "Group Output"],
        "trunk": ["Grid", "Set Position", "Group Output"],
        "dependencies": [{"node": "Noise", "consumer": "Set Position"}],
        "frames": [{"name": "Sources", "nodes": ["Grid"]}]
    }'

    import runpy
    result = runpy.run_path(SCRIPT, init_globals={"NODECUE_PARAMS": params})["result"]

Parameters:
    op              "check" (read-only) or "apply" (move authorized nodes)
    tree/object/modifier  same tree resolution as read_graph.py
    nodes           required list of authorized node names (exact Blender names)
    trunk           ordered geometry-trunk names (subset of nodes)
    dependencies    [{"node": str, "consumer": str}, ...]
    frames          [{"name": str, "nodes": [str, ...]}, ...]
                    Frame nodes named here must exist and be authorized.

`check` returns structured presentation findings and never writes.
`apply` snapshots every node's parent and local location, writes parent-relative
locations from a stable absolute model, then readbacks. If a protected node
moved, it restores parent and local location in parent-safe order. Missing,
duplicate, or out-of-scope names fail with no partial mutation. Zone input/output
pairs must both be in scope or both out; a split pair is rejected.
"""

import json
import sys

import bpy

_FALLBACK_W = 140.0
_FALLBACK_H = 100.0
_GAP_X = 80.0
_GAP_Y = 60.0
_FRAME_PAD = 30.0
_ORIGIN_X = 0.0
_ORIGIN_Y = 0.0
_EPS = 0.51
# Protected-node identity: layout matching uses _EPS; scope safety does not.
_PROTECTED_EPS = 1e-5

_ZONE_PAIRS = (
    ("GeometryNodeRepeatInput", "GeometryNodeRepeatOutput"),
    ("GeometryNodeSimulationInput", "GeometryNodeSimulationOutput"),
    ("GeometryNodeForeachGeometryElementInput",
     "GeometryNodeForeachGeometryElementOutput"),
)

def _resolve(params):
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
            return (
                None,
                f"{obj.name!r} has {len(mods)} NODES modifiers; pass `modifier` to choose",
                [f"{obj.name}/{m.name} -> {m.node_group.name}" for m in mods],
            )

    trees = [g.name for g in bpy.data.node_groups if g.bl_idname == "GeometryNodeTree"]
    return None, "no unambiguous tree", candidates + trees


def _abs_location(node):
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


def _size(node):
    dims = getattr(node, "dimensions", None)
    if dims is not None and float(dims[0]) > 1.0 and float(dims[1]) > 1.0:
        return float(dims[0]), float(dims[1])
    w = float(getattr(node, "width", 0.0) or 0.0)
    h = float(getattr(node, "height", 0.0) or 0.0)
    if w < 1.0:
        w = _FALLBACK_W
    if h < 1.0:
        h = _FALLBACK_H
    return w, h


def _snapshot_layout(tree):
    out = {}
    for node in tree.nodes:
        out[node.name] = {
            "parent": node.parent.name if node.parent else None,
            "location": [float(node.location[0]), float(node.location[1])],
            "location_absolute": _abs_location(node),
        }
    return out


def _fail(error, **extra):
    payload = {
        "ok": False,
        "blender": bpy.app.version_string,
        "error": error,
        "graph_correctness": "not_evaluated",
    }
    payload.update(extra)
    return payload


def _authorize(tree, params):
    raw = params.get("nodes")
    if not raw or not isinstance(raw, list):
        return None, _fail(
            "pass `nodes` as an explicit list of authorized node names",
            candidates=[n.name for n in tree.nodes],
        )
    names = list(raw)
    seen = {}
    dups = []
    for n in names:
        if n in seen:
            dups.append(n)
        seen[n] = True
    if dups:
        return None, _fail(
            f"duplicate authorized names: {sorted(set(dups))}",
            mutated=False,
        )
    missing = [n for n in names if tree.nodes.get(n) is None]
    if missing:
        return None, _fail(
            f"authorized names not in tree: {missing}",
            candidates=[n.name for n in tree.nodes],
            mutated=False,
        )
    authorized = set(names)

    trunk = params.get("trunk") or []
    if not isinstance(trunk, list):
        return None, _fail("`trunk` must be a list of node names", mutated=False)
    extra = [n for n in trunk if n not in authorized]
    if extra:
        return None, _fail(
            f"trunk names outside authorized scope: {extra}",
            mutated=False,
        )

    deps = params.get("dependencies") or []
    if not isinstance(deps, list):
        return None, _fail("`dependencies` must be a list of {node, consumer}", mutated=False)
    for i, rec in enumerate(deps):
        if not isinstance(rec, dict) or "node" not in rec or "consumer" not in rec:
            return None, _fail(
                f"dependencies[{i}] must be {{'node': str, 'consumer': str}}",
                mutated=False,
            )
        for key in ("node", "consumer"):
            if rec[key] not in authorized:
                return None, _fail(
                    f"dependency {key} {rec[key]!r} is outside authorized scope",
                    mutated=False,
                )

    frames = params.get("frames") or []
    if not isinstance(frames, list):
        return None, _fail("`frames` must be a list of {name, nodes}", mutated=False)
    frame_members = {}
    for i, rec in enumerate(frames):
        if not isinstance(rec, dict) or "name" not in rec or "nodes" not in rec:
            return None, _fail(
                f"frames[{i}] must be {{'name': str, 'nodes': [str, ...]}}",
                mutated=False,
            )
        fname = rec["name"]
        if fname not in authorized:
            return None, _fail(
                f"frame {fname!r} is outside authorized scope",
                mutated=False,
            )
        frame_node = tree.nodes.get(fname)
        if frame_node is None or frame_node.bl_idname != "NodeFrame":
            return None, _fail(
                f"{fname!r} is not a NodeFrame",
                mutated=False,
            )
        members = list(rec["nodes"])
        for m in members:
            if m not in authorized:
                return None, _fail(
                    f"frame member {m!r} is outside authorized scope",
                    mutated=False,
                )
            if m == fname:
                return None, _fail("a frame cannot list itself as a member", mutated=False)
            if m in frame_members:
                return None, _fail(
                    f"{m!r} is listed in more than one frame",
                    mutated=False,
                )
            frame_members[m] = fname

    zone_error = _zone_scope_error(tree, authorized)
    if zone_error:
        return None, _fail(zone_error, mutated=False)

    spec = {
        "authorized": authorized,
        "ordered": names,
        "trunk": list(trunk),
        "dependencies": deps,
        "frames": frames,
        "frame_members": frame_members,
    }
    return spec, None


def _zone_scope_error(tree, authorized):
    by_id = {}
    for node in tree.nodes:
        by_id.setdefault(node.bl_idname, []).append(node.name)
    for a, b in _ZONE_PAIRS:
        a_names = [n for n in by_id.get(a, []) if n in authorized]
        b_names = [n for n in by_id.get(b, []) if n in authorized]
        if bool(a_names) != bool(b_names):
            return (
                f"zone edge split: {a} {a_names} and {b} {b_names} must both be "
                "inside authorized scope or both outside"
            )
    return None


def _plan_positions(tree, spec):
    """Stable absolute positions from caller order, never set/dict accident."""
    sizes = {name: _size(tree.nodes[name]) for name in spec["ordered"]}
    abs_pos = {}
    cursor_x = _ORIGIN_X
    trunk_y = _ORIGIN_Y
    for name in spec["trunk"]:
        w, h = sizes[name]
        abs_pos[name] = [cursor_x, trunk_y]
        cursor_x += w + _GAP_X

    consumer_index = {}
    for rec in spec["dependencies"]:
        consumer_index.setdefault(rec["consumer"], []).append(rec["node"])

    for consumer, producers in consumer_index.items():
        if consumer not in abs_pos:
            w, h = sizes[consumer]
            abs_pos[consumer] = [cursor_x, trunk_y]
            cursor_x += w + _GAP_X
        cx, cy = abs_pos[consumer]
        _, ch = sizes[consumer]
        stack_y = cy + ch + _GAP_Y
        for prod in producers:
            pw, ph = sizes[prod]
            abs_pos[prod] = [cx, stack_y]
            stack_y += ph + _GAP_Y

    rest_x = cursor_x
    rest_y = trunk_y - (_FALLBACK_H + _GAP_Y)
    for name in spec["ordered"]:
        node = tree.nodes[name]
        if name in abs_pos:
            continue
        if node.bl_idname == "NodeFrame":
            continue
        abs_pos[name] = [rest_x, rest_y]
        w, _h = sizes[name]
        rest_x += w + _GAP_X

    frame_abs = {}
    frame_boxes = {}
    for rec in spec["frames"]:
        fname = rec["name"]
        members = rec["nodes"]
        if not members:
            frame_abs[fname] = [_ORIGIN_X, _ORIGIN_Y]
            frame_boxes[fname] = [_ORIGIN_X, _ORIGIN_Y, _ORIGIN_X + _FRAME_PAD, _ORIGIN_Y + _FRAME_PAD]
            continue
        xs, ys, x2s, y2s = [], [], [], []
        for m in members:
            if m not in abs_pos:
                continue
            x, y = abs_pos[m]
            w, h = sizes[m]
            xs.append(x)
            ys.append(y)
            x2s.append(x + w)
            y2s.append(y + h)
        min_x = min(xs) - _FRAME_PAD
        min_y = min(ys) - _FRAME_PAD
        max_x = max(x2s) + _FRAME_PAD
        max_y = max(y2s) + _FRAME_PAD
        frame_abs[fname] = [min_x, min_y]
        frame_boxes[fname] = [min_x, min_y, max_x, max_y]
        abs_pos[fname] = [min_x, min_y]

    parent_of = dict(spec["frame_members"])
    relative = {}
    for name, abs_xy in abs_pos.items():
        parent = parent_of.get(name)
        if parent and parent in abs_pos:
            px, py = abs_pos[parent]
            relative[name] = [abs_xy[0] - px, abs_xy[1] - py]
        else:
            relative[name] = list(abs_xy)

    return {
        "absolute": abs_pos,
        "relative": relative,
        "parent_of": parent_of,
        "sizes": sizes,
        "frame_boxes": frame_boxes,
    }


def _boxes_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def _node_box(name, plan):
    x, y = plan["absolute"][name]
    w, h = plan["sizes"][name]
    return [x, y, x + w, y + h]


def _findings(tree, spec, plan):
    findings = []
    trunk = spec["trunk"]
    for i in range(len(trunk) - 1):
        a, b = trunk[i], trunk[i + 1]
        if a not in plan["absolute"] or b not in plan["absolute"]:
            continue
        ax = plan["absolute"][a][0]
        bx = plan["absolute"][b][0]
        aw = plan["sizes"][a][0]
        if bx + _EPS < ax + aw:
            findings.append({
                "kind": "trunk_not_left_to_right",
                "lane": "presentation",
                "nodes": [a, b],
                "observed": {"from_x": ax, "to_x": bx},
            })

    for rec in spec["dependencies"]:
        n, c = rec["node"], rec["consumer"]
        if n not in plan["absolute"] or c not in plan["absolute"]:
            continue
        nx, ny = plan["absolute"][n]
        cx, cy = plan["absolute"][c]
        dist = ((nx - cx) ** 2 + (ny - cy) ** 2) ** 0.5
        limit = plan["sizes"][c][0] + plan["sizes"][n][0] + 4 * _GAP_X
        if dist > limit:
            findings.append({
                "kind": "dependency_far_from_consumer",
                "lane": "presentation",
                "node": n,
                "consumer": c,
                "distance": dist,
            })

    names = [n for n in spec["ordered"] if n in plan["absolute"]
             and tree.nodes[n].bl_idname != "NodeFrame"]
    for i, a in enumerate(names):
        ba = _node_box(a, plan)
        for b in names[i + 1:]:
            bb = _node_box(b, plan)
            if _boxes_overlap(ba, bb):
                findings.append({
                    "kind": "node_overlap",
                    "lane": "presentation",
                    "nodes": [a, b],
                })

    items = list(plan["frame_boxes"].items())
    for i, (fa, ba) in enumerate(items):
        for fb, bb in items[i + 1:]:
            if _boxes_overlap(ba, bb):
                findings.append({
                    "kind": "frame_overlap",
                    "lane": "presentation",
                    "frames": [fa, fb],
                })

    for name in spec["ordered"]:
        if name not in plan["absolute"]:
            continue
        node = tree.nodes[name]
        obs = _abs_location(node)
        exp = plan["absolute"][name]
        if abs(obs[0] - exp[0]) > _EPS or abs(obs[1] - exp[1]) > _EPS:
            findings.append({
                "kind": "position_mismatch",
                "lane": "presentation",
                "node": name,
                "expected_absolute": exp,
                "observed_absolute": obs,
            })
        expected_parent = spec["frame_members"].get(name)
        actual_parent = node.parent.name if node.parent else None
        if expected_parent != actual_parent and name in spec["frame_members"]:
            findings.append({
                "kind": "parent_mismatch",
                "lane": "presentation",
                "node": name,
                "expected_parent": expected_parent,
                "observed_parent": actual_parent,
            })
    return findings


def _apply_plan(tree, spec, plan):
    for rec in spec["frames"]:
        fname = rec["name"]
        frame = tree.nodes[fname]
        for m in rec["nodes"]:
            tree.nodes[m].parent = frame
    for name, rel in plan["relative"].items():
        node = tree.nodes[name]
        node.location = (rel[0], rel[1])


def _same_xy(a, b, eps):
    return abs(a[0] - b[0]) <= eps and abs(a[1] - b[1]) <= eps


def _layout_equal(a, b, eps):
    if set(a) != set(b):
        return False
    for name, rec in a.items():
        now = b[name]
        if now["parent"] != rec["parent"]:
            return False
        if not _same_xy(rec["location"], now["location"], eps):
            return False
        if not _same_xy(rec["location_absolute"], now["location_absolute"], eps):
            return False
    return True


def _parent_depth(name, snapshot):
    depth = 0
    seen = set()
    parent = snapshot.get(name, {}).get("parent")
    while parent:
        if parent in seen:
            break
        seen.add(parent)
        depth += 1
        parent = snapshot.get(parent, {}).get("parent")
    return depth


def _rollback_layout(tree, snapshot):
    """Restore parent and local location for every snapshotted node still present.

    Unparent deepest-first, then reparent and write local location ancestor-first,
    so nested frames cannot leave a half-applied parent graph.
    """
    existing = []
    for name in snapshot:
        node = tree.nodes.get(name)
        if node is not None:
            existing.append(name)

    for name in sorted(existing, key=lambda n: -_parent_depth(n, snapshot)):
        tree.nodes[name].parent = None

    for name in sorted(existing, key=lambda n: _parent_depth(n, snapshot)):
        rec = snapshot[name]
        node = tree.nodes[name]
        pname = rec["parent"]
        node.parent = tree.nodes.get(pname) if pname else None
        loc = rec["location"]
        node.location = (loc[0], loc[1])


def _protected_ok(before, after, authorized):
    for name, rec in before.items():
        if name in authorized:
            continue
        now = after.get(name)
        if now is None:
            return False, f"protected node {name!r} disappeared"
        if now["parent"] != rec["parent"]:
            return False, f"protected node {name!r} parent changed"
        for key in ("location", "location_absolute"):
            if not _same_xy(rec[key], now[key], _PROTECTED_EPS):
                return False, f"protected node {name!r} {key} changed"
    return True, None


def _positions_payload(tree, spec):
    out = {}
    for name in spec["ordered"]:
        node = tree.nodes[name]
        out[name] = {
            "parent": node.parent.name if node.parent else None,
            "location": [float(node.location[0]), float(node.location[1])],
            "location_absolute": _abs_location(node),
            "width": _size(node)[0],
            "height": _size(node)[1],
        }
    return out


def run(params=None):
    params = params or {}
    op = params.get("op") or params.get("operation")
    if op not in {"check", "apply"}:
        return _fail(
            "pass op as 'check' (read-only) or 'apply' (authorized mutation)",
            operations=["check", "apply"],
        )

    tree, how, candidates = _resolve(params)
    if tree is None:
        return _fail(how, candidates=candidates)

    spec, err = _authorize(tree, params)
    if err is not None:
        return err

    before = _snapshot_layout(tree)
    plan = _plan_positions(tree, spec)

    if op == "check":
        findings = _findings(tree, spec, plan)
        after = _snapshot_layout(tree)
        mutated = before != after
        return {
            "ok": True,
            "blender": bpy.app.version_string,
            "operation": "check",
            "resolved_by": how,
            "mutated": mutated,
            "layout_ok": not findings,
            "findings": findings,
            "graph_correctness": "not_evaluated",
            "positions": _positions_payload(tree, spec),
            "targets": plan["absolute"],
        }

    _apply_plan(tree, spec, plan)
    after = _snapshot_layout(tree)
    ok_prot, prot_err = _protected_ok(before, after, spec["authorized"])
    if not ok_prot:
        _rollback_layout(tree, before)
        restored = _snapshot_layout(tree)
        rolled_back = _layout_equal(before, restored, _PROTECTED_EPS)
        return _fail(
            prot_err,
            mutated=not rolled_back,
            rolled_back=rolled_back,
            graph_correctness="not_evaluated",
        )

    findings = _findings(tree, spec, plan)
    return {
        "ok": True,
        "blender": bpy.app.version_string,
        "operation": "apply",
        "resolved_by": how,
        "mutated": True,
        "layout_ok": not findings,
        "findings": findings,
        "graph_correctness": "not_evaluated",
        "positions": _positions_payload(tree, spec),
        "targets": plan["absolute"],
        "protected_unchanged": True,
    }


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
