"""Screenshot the Geometry Nodes editor, then put the UI back the way it was.

A verification and delivery aid, not an image-reference feature. It changes UI
state only — which tree the editor shows, whether the area is maximized, where
the view is framed — and restores all of it, so a file saved afterwards keeps the
user's normal layout. It never changes graph contents, and it reports the node
and link counts around the capture so that claim is checkable.

Two facts decide the shape of this script.

**Blender does not redraw while idle**, so a screenshot otherwise returns the
last drawn frame, and the node editor is usually too short to be readable.

**`bpy.ops.wm.redraw_timer()` segfaults Blender.** Measured twice on 5.2.1: once
from Python running inside a Blender application timer, which is how an MCP-style
host executes submitted code, and once from a `--python` startup script. Both
crash in `redraw_timer_exec`. So this script never forces a redraw. It tags
areas and splits the work into stages, and Blender's own event loop does the
redrawing in between:

    capture.py {"stage": "prepare", "tree": "My Tree"}   # returns; Blender redraws
    capture.py {"stage": "capture", "output": "/abs/path/graph.png"}
    capture.py {"stage": "restore"}

`stage: "all"` does all three in one call. It is correct whenever the window has
already drawn what you want captured — after a host call that only read the graph,
say. It refuses `fit`, because framing has to be drawn before it can be captured
and one call has no event loop in it.

Parameters:
    stage       "all" (default) | "prepare" | "capture" | "restore"
    output      required for "capture"/"all"; absolute, or "//x.png" when saved
    overwrite   replace an existing output file (default false — it refuses)
    tree        node group to show; the previous one is restored
    maximize    maximize the editor for the capture (default true)
    fit         frame the whole graph. Only in `prepare`, and **off by default**.
                Blender exposes no way to put the user's pan and zoom back, so
                this changes state the script cannot restore. `SKILL.md` makes it
                a permission boundary: tell the user the framing will change and
                cannot be undone, get their agreement, then pass it — and report
                it afterwards. Everything else the script touches (shown tree,
                pin, maximize) is temporary and restored.

`graph_unchanged` compares a fingerprint over node identities, socket values,
links and the group interface — not a pair of counts, which miss a rename, a
rewire between the same two nodes, and every value write.

Between-stage state lives in `bpy.app.driver_namespace`, which is session-only
and is never written into the .blend.
"""

import hashlib
import json
import os
import sys

import bpy

_STATE_KEY = "nodecue_capture_state"


def _fingerprint(tree):
    """Stable identity plus content, not a pair of counts.

    Counts miss a rename, a rewired link between the same two nodes, and a value
    write - all of which are graph changes a capture must not have caused.
    """
    if tree is None:
        return None
    parts = []
    for node in sorted(tree.nodes, key=lambda n: n.name):
        parts.append(f"N|{node.name}|{node.bl_idname}|{node.label}|{int(node.mute)}")
        for side, sockets in (("i", node.inputs), ("o", node.outputs)):
            for sock in sockets:
                value = ""
                if hasattr(sock, "default_value") and not sock.is_linked:
                    try:
                        value = repr(list(sock.default_value))
                    except TypeError:
                        value = repr(sock.default_value)
                parts.append(f"S|{node.name}|{side}|{sock.identifier}|{sock.type}|{value}")
    for link in sorted(
        tree.links,
        key=lambda l: (l.from_node.name, l.from_socket.identifier,
                       l.to_node.name, l.to_socket.identifier),
    ):
        parts.append(
            f"L|{link.from_node.name}.{link.from_socket.identifier}"
            f"->{link.to_node.name}.{link.to_socket.identifier}|{int(link.is_muted)}"
        )
    for item in tree.interface.items_tree:
        parts.append(
            f"I|{item.item_type}|{item.name}|{getattr(item, 'identifier', '')}"
            f"|{getattr(item, 'in_out', '')}|{getattr(item, 'socket_type', '')}"
        )
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _state():
    return bpy.app.driver_namespace.setdefault(_STATE_KEY, {})


def _redraw():
    """Ask for a redraw. Never force one - wm.redraw_timer segfaults Blender."""
    for wm in bpy.data.window_managers:
        for win in wm.windows:
            for area in win.screen.areas:
                area.tag_redraw()
    return "tag_redraw"


def _find_editor():
    for wm in bpy.data.window_managers:
        for win in wm.windows:
            for area in win.screen.areas:
                if area.type != "NODE_EDITOR":
                    continue
                space = area.spaces.active
                if getattr(space, "tree_type", None) == "GeometryNodeTree":
                    return win, area, space
    return None, None, None


def _region(area):
    return next((r for r in area.regions if r.type == "WINDOW"), None)


def _resolve_output(raw, overwrite):
    if not raw:
        return None, "pass an `output` path for the capture"
    if raw.startswith("//") and not bpy.data.filepath:
        return None, "relative '//' output needs a saved .blend; pass an absolute path"
    path = bpy.path.abspath(raw)
    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        return None, f"output directory does not exist: {parent}"
    if os.path.exists(path) and not overwrite:
        return None, (
            f"{path} already exists; pass overwrite=true to replace it, or choose "
            "another path. A capture silently replacing a file is not a side effect "
            "anyone asked for."
        )
    return path, None


def _preflight(base):
    if bpy.app.background:
        base["error"] = "no window in background mode; run this in a Blender with a UI"
        return None
    win, area, space = _find_editor()
    if area is None:
        base["error"] = "no Geometry Nodes editor is open"
        base["hint"] = "open a Geometry Nodes editor, then run this again"
        return None
    return win, area, space


def _prepare(params, base):
    found = _preflight(base)
    if found is None:
        return base
    win, area, space = found
    state = _state()
    state.setdefault("original_tree", space.node_tree.name if space.node_tree else None)
    state.setdefault("original_pin", bool(getattr(space, "pin", False)))
    state.setdefault("was_fullscreen", bool(win.screen.show_fullscreen))

    wanted = params.get("tree")
    if wanted:
        tree = bpy.data.node_groups.get(wanted)
        if tree is None:
            base["error"] = f"node group {wanted!r} not found"
            base["candidates"] = [g.name for g in bpy.data.node_groups]
            return base
        # An unpinned Geometry Nodes editor follows the active object's modifier,
        # so an assignment here is undone by the next draw - and the capture then
        # shows a different tree than the one it reports. Pin, then assign.
        if hasattr(space, "pin"):
            space.pin = True
        space.node_tree = tree

    steps = ["show-tree" if wanted else "keep-tree"]
    if params.get("maximize", True) and not win.screen.show_fullscreen:
        with bpy.context.temp_override(window=win, area=area, region=_region(area)):
            bpy.ops.screen.screen_full_area()
        state["maximized_here"] = True
        steps.append("maximize")

    # Framing happens here, never in `capture`: the view has to be drawn before a
    # screenshot means anything, and only the event loop between two host calls
    # draws it.
    view_changed = False
    if params.get("fit", False):
        win, area, space = _find_editor()
        with bpy.context.temp_override(window=win, area=area, region=_region(area)):
            bpy.ops.node.view_all()
        view_changed = True
        state["view_changed"] = True
        steps.append("fit")

    steps.append(_redraw())
    shown = space.edit_tree or space.node_tree
    base.update({
        "ok": True,
        "stage": "prepare",
        "steps": steps,
        "showing": shown.name if shown else None,
        "graph_fingerprint": _fingerprint(shown),
        "view_changed": view_changed,
        "view_restorable": False,
        "next": "capture",
        "note": "let Blender's event loop run before capturing; that is the redraw",
    })
    if view_changed:
        base["view_note"] = (
            "the node view was reframed and Blender exposes no way to put it back; "
            "pass fit=false to leave the user's framing alone"
        )
    return base


def _capture(params, base):
    if params.get("fit"):
        base["error"] = (
            "fit belongs to `prepare`. Framing has to be drawn before it can be "
            "captured, and only Blender's event loop between two calls draws it."
        )
        return base
    path, err = _resolve_output(params.get("output"), params.get("overwrite", False))
    if err:
        base["error"] = err
        return base
    found = _preflight(base)
    if found is None:
        return base
    win, area, space = found

    shown = space.edit_tree or space.node_tree
    before = _fingerprint(shown)
    steps = []
    try:
        size = [area.width, area.height]
        with bpy.context.temp_override(window=win, area=area, region=_region(area)):
            bpy.ops.screen.screenshot_area(filepath=path)
        steps.append("capture")
    except Exception as exc:
        base["error"] = f"{type(exc).__name__}: {exc}"
        base["steps"] = steps
        return base

    after = _fingerprint(shown)
    base.update({
        "ok": os.path.exists(path),
        "stage": "capture",
        "output": path,
        "exists": os.path.exists(path),
        "bytes": os.path.getsize(path) if os.path.exists(path) else None,
        "area_size": size,
        "steps": steps,
        "graph_unchanged": before == after,
        "graph_fingerprint": after,
        "captured_tree": {
            "name": shown.name if shown else None,
            "is_modifier": getattr(shown, "is_modifier", None) if shown else None,
            "is_tool": getattr(shown, "is_tool", None) if shown else None,
            "node_count": len(shown.nodes) if shown else None,
            "link_count": len(shown.links) if shown else None,
        },
        "next": "restore",
    })
    return base


def _restore(params, base):
    if bpy.app.background:
        base["error"] = "no window in background mode"
        return base
    state = _state()
    steps, errors = [], {}

    if state.get("maximized_here"):
        win, area, _ = _find_editor()
        if win is not None and win.screen.show_fullscreen:
            try:
                with bpy.context.temp_override(window=win, area=area, region=_region(area)):
                    bpy.ops.screen.back_to_previous()
                steps.append("restore-layout")
            except Exception as exc:
                errors["layout"] = f"{type(exc).__name__}: {exc}"
        state.pop("maximized_here", None)

    if "original_tree" in state:
        _, _, space = _find_editor()
        if space is not None:
            name = state["original_tree"]
            space.node_tree = bpy.data.node_groups.get(name) if name else None
            if hasattr(space, "pin"):
                space.pin = state.get("original_pin", False)
            steps.append("restore-tree")
        state.pop("original_tree", None)
    state.pop("original_pin", None)

    view_changed = bool(state.pop("view_changed", False))
    state.pop("was_fullscreen", None)
    steps.append(_redraw())
    win, _, space = _find_editor()
    base.update({
        "ok": not errors,
        "stage": "restore",
        "steps": steps,
        # The tree and the layout are put back. The view is not, because Blender
        # exposes no way to; saying so is the honest half of this contract.
        "ui_restored": not errors,
        "view_changed": view_changed,
        "view_restored": False if view_changed else None,
        "still_fullscreen": bool(win.screen.show_fullscreen) if win else None,
        "graph_fingerprint": _fingerprint(space.edit_tree or space.node_tree)
        if space is not None else None,
    })
    if view_changed:
        base["view_note"] = "the node view framing was changed by `fit` and cannot be restored"
    if errors:
        base["restore_errors"] = errors
    return base


def _all(params, base):
    if params.get("fit"):
        base["error"] = (
            "stage='all' cannot fit: the event loop has to run between framing and "
            "the screenshot, and one call has no loop in it. Use prepare / capture / "
            "restore as three calls."
        )
        base["stages"] = ["prepare", "capture", "restore"]
        return base
    prepared = _prepare(params, dict(base))
    if not prepared.get("ok"):
        return prepared
    captured = _capture(params, dict(base))
    restored = _restore(params, dict(base))
    captured["stage"] = "all"
    captured["ok"] = bool(captured.get("ok")) and bool(restored.get("ok"))
    captured["steps"] = prepared["steps"] + captured.get("steps", []) + restored["steps"]
    captured["ui_restored"] = restored.get("ui_restored")
    if "restore_errors" in restored:
        captured["restore_errors"] = restored["restore_errors"]
    return captured


_STAGES = {"all": _all, "prepare": _prepare, "capture": _capture, "restore": _restore}


def run(params=None):
    params = params or {}
    stage = params.get("stage", "all")
    fn = _STAGES.get(stage)
    base = {"ok": False, "stage": stage, "blender": bpy.app.version_string}
    if fn is None:
        base["error"] = f"unknown stage {stage!r}"
        base["stages"] = sorted(_STAGES)
        return base
    payload = fn(params, base)
    payload["redraw_mode"] = "tag_redraw"
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
