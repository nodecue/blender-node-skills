"""Dump the two live facts `references/nodes.tsv` needs that the identity dumps lack.

`docs/node-dumps/gn-*.json` carries names, identifiers, socket types and writable
properties. It does not carry:

1. **field socket display shapes**, per socket. Nothing in the identity record
   encodes them, and they are the only mechanical source for Field capability.
   They are maintainer evidence only: the published TSV carries no Field column,
   and `scripts/probe_node.py` answers the live question.
2. **the Add menu a node lives in** — Blender's own categorisation, defined in
   `bl_ui.node_add_menu_geometry` as `self.node_operator(layout, "<bl_idname>")`
   calls. Reading it is what makes `nodes.tsv.category` mechanical rather than
   invented.

This writes a separate evidence file rather than extending `introspect_nodes.py`,
so the existing per-version dumps and their diffs stay byte-stable.

Run once per install:

    blender -b --factory-startup --python tools/dump_tsv_evidence.py -- out.json

The menu is read by parsing the module's own source with `ast`, not by drawing it.
A `draw` body can branch on context; the AST sees every branch, which is what a
routing index wants, and it needs no window.
"""

import ast
import inspect
import json
import sys
import textwrap

import bpy

TREE_TYPE = "GeometryNodeTree"
# The virtual socket on Group Input/Output is a UI affordance, not an interface.
SKIP_IDENTIFIERS = {"__extend__"}


def node_classes():
    names = []
    for name in sorted(dir(bpy.types)):
        candidate = getattr(bpy.types, name)
        try:
            if isinstance(candidate, type) and issubclass(candidate, bpy.types.Node):
                names.append(name)
        except TypeError:
            continue
    return names


def _sockets(sockets):
    out = {}
    for sock in sockets:
        if sock.identifier in SKIP_IDENTIFIERS:
            continue
        out[sock.identifier] = getattr(sock, "display_shape", None)
    return out


def field_shapes():
    """Create every node type once and record each socket's display shape."""
    tree = bpy.data.node_groups.new("__tsv_evidence_probe", TREE_TYPE)
    records, skipped = {}, []
    try:
        for class_name in node_classes():
            try:
                node = tree.nodes.new(class_name)
            except Exception:
                skipped.append(class_name)
                continue
            try:
                # Shapes only. Rolling them up per node is the unstable abstraction
                # the plan forbids: capability is per socket and moves with the
                # node's mode, so the comparison happens per socket downstream.
                records[class_name] = {
                    "in": _sockets(node.inputs),
                    "out": _sockets(node.outputs),
                }
            except Exception as exc:  # a node that cannot be read is data too
                skipped.append(f"{class_name} (read failed: {exc})")
            finally:
                tree.nodes.remove(node)
    finally:
        bpy.data.node_groups.remove(tree)
    return records, skipped


def _first_string_arg(call):
    """The bl_idname is always the first positional string.

    Later positional strings are something else - `node_operator_enum(layout,
    "FunctionNodeBooleanMath", "operation")` passes a property name, and taking
    every string turns `operation` into a node.
    """
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            return arg.value
        if isinstance(arg, ast.Name) and arg.id == "layout":
            continue
    return None


def _string_args(call):
    return [a.value for a in call.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]


def menu_structure():
    """Read `bl_ui.node_add_menu_geometry` as source, not as a drawn menu."""
    try:
        import bl_ui.node_add_menu_geometry as module
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}, {}

    menus = {}
    for name in dir(module):
        cls = getattr(module, name)
        if not (isinstance(cls, type) and hasattr(cls, "draw")):
            continue
        try:
            source = inspect.getsource(cls.draw)
        except (OSError, TypeError):
            continue
        try:
            tree = ast.parse(textwrap.dedent(source))
        except SyntaxError:
            continue

        nodes, submenus = [], []
        for call in (n for n in ast.walk(tree) if isinstance(n, ast.Call)):
            func = call.func
            attr = func.attr if isinstance(func, ast.Attribute) else None
            if attr is None:
                continue
            if attr.startswith("node_operator") or attr == "add_node_type":
                first = _first_string_arg(call)
                if first:
                    nodes.append(first)
            elif attr == "menu":
                submenus += [s for s in _string_args(call) if s.startswith("NODE_MT_")]
        if nodes or submenus:
            menus[name] = {
                "label": getattr(cls, "bl_label", None),
                # Blender's own fully-qualified category, e.g. "Curve/Read". The
                # bl_label alone is ambiguous: Mesh, Curve and Volume all have a
                # submenu labelled "Primitives".
                "menu_path": getattr(cls, "menu_path", None),
                "nodes": nodes,
                "submenus": submenus,
            }
    return menus, _paths(menus)


def _paths(menus):
    """Category per bl_idname, from each menu's own `menu_path`.

    Falls back to `bl_label` only when a build predates `menu_path`; the fallback
    is recorded as such so the generator can report it instead of trusting it.
    """
    paths = {}
    for rec in menus.values():
        category = rec.get("menu_path") or rec.get("label")
        source = "menu_path" if rec.get("menu_path") else "bl_label"
        if not category:
            continue
        for bl_idname in rec["nodes"]:
            paths.setdefault(bl_idname, {})[category] = source
    return {
        k: [{"category": c, "source": s} for c, s in sorted(v.items())]
        for k, v in sorted(paths.items())
    }


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out_path = argv[0] if argv else "tsv-evidence.json"

    shapes, skipped = field_shapes()
    menus, paths = menu_structure()

    payload = {
        "blender": bpy.app.version_string,
        "version": list(bpy.app.version),
        "tree_type": TREE_TYPE,
        "creatable": len(shapes),
        "skipped": len(skipped),
        "field_shapes": shapes,
        "menu_paths": paths,
        "menu_structure": menus if isinstance(menus, dict) else {},
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False, sort_keys=True)
    covered = sum(1 for b in shapes if b in paths)
    print(f"WROTE {out_path}  creatable={len(shapes)}  in_menu={covered}  "
          f"menu_only={len(set(paths) - set(shapes))}")


main()
