"""Find out what node groups are already available before rebuilding one.

Read-only discovery by default. It enumerates Blender's own bundled asset
libraries and the libraries the user has configured, lists the node groups in a
selected file, and — only when asked — loads one group temporarily to read its
real interface, dependencies and asset metadata, then removes exactly what it
loaded.

Two boundaries are enforced here rather than left to judgement:

* Only Blender's bundled asset root and the paths in
  `preferences.filepaths.asset_libraries` are readable. Anything else is
  refused with the list of allowed roots, so the user can name or authorize a
  path rather than have one guessed for them.
* Nothing is appended into the working file. Bringing a group in for real is a
  Build/Edit mutation and belongs to the caller, not to this script.

No network access.

    blender -b --python scripts/inspect_assets.py -- '{"operation": "libraries"}'
    blender -b --python scripts/inspect_assets.py -- \
        '{"operation": "inspect", "path": "...blend", "group": "Smooth by Angle"}'

Parameters:
    operation   "libraries" (default) | "files" | "groups" | "inspect"
    library     library name, for "files"
    path        .blend path, for "groups" and "inspect"
    group       node group name, for "inspect"
"""

import json
import os
import sys

import bpy

_WATCHED = ("node_groups", "images", "materials", "objects", "meshes", "texts",
            "collections", "curves", "hair_curves", "pointclouds", "volumes")
# Objects before their data, so mesh and curve datablocks drop to zero users and
# remove cleanly. Node groups late: a loaded object may still reference one.
_REMOVE_ORDER = ("objects", "collections", "meshes", "curves", "hair_curves",
                 "pointclouds", "volumes", "node_groups", "materials", "images",
                 "texts")
_TREE_LABEL = {
    "GeometryNodeTree": "geometry",
    "ShaderNodeTree": "shader",
    "CompositorNodeTree": "compositor",
    "TextureNodeTree": "texture",
}


def _counts():
    return {name: len(getattr(bpy.data, name)) for name in _WATCHED}


def _jsonable(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bpy.types.ID):
        return {"id_name": value.name, "id_type": type(value).__name__}
    try:
        return [_jsonable(v) for v in value]
    except TypeError:
        return str(value)


def _bundled_root():
    try:
        return bpy.utils.system_resource("DATAFILES", path="assets")
    except Exception:
        return None


def _roots(params=None):
    """Every directory or file this script is allowed to read, and why.

    Configured libraries are the default. A path outside them is readable only
    when the user named it in this conversation and the caller passes it in
    `authorized_paths` - one file, or one bounded directory. Nothing is inferred.
    """
    params = params or {}
    roots = []
    bundled = _bundled_root()
    if bundled and os.path.isdir(bundled):
        roots.append(
            {
                "name": "<bundled>",
                "path": bundled,
                "kind": "bundled",
                "consent": "none needed - Blender's own datafiles",
            }
        )
    for lib in bpy.context.preferences.filepaths.asset_libraries:
        path = bpy.path.abspath(lib.path) if lib.path else ""
        roots.append(
            {
                "name": lib.name,
                "path": path,
                "kind": "user",
                "exists": bool(path) and os.path.isdir(path),
                "consent": "configured by the user in this Blender",
            }
        )
    for entry in params.get("authorized_paths") or []:
        raw = entry if isinstance(entry, str) else entry.get("path")
        if not raw:
            continue
        path = os.path.realpath(bpy.path.abspath(raw))
        roots.append(
            {
                "name": f"<authorized:{os.path.basename(path)}>",
                "path": path,
                "kind": "authorized-file" if os.path.isfile(path) else "authorized-directory",
                "exists": os.path.exists(path),
                "consent": "named by the user in this conversation",
            }
        )
    return roots


def _authorized(path, roots):
    """Containment decided on canonical paths, on both sides.

    Resolving only the root leaves a symlinked file inside a library able to point
    anywhere; resolving both and comparing is what closes that.
    """
    real = os.path.realpath(path)
    for root in roots:
        if not root.get("path"):
            continue
        base = os.path.realpath(root["path"])
        if real == base:
            return root
        if os.path.isdir(base) and real.startswith(base + os.sep):
            return root
    return None


def _blend_files(root_path, roots):
    """Every .blend under a root, each re-checked after resolving its own path.

    A file inside an authorized directory can still be a symlink out of it. The
    walk finds candidates; `_authorized` on the *resolved* path decides.
    """
    base = os.path.realpath(root_path)
    if os.path.isfile(base):
        return [base] if base.endswith(".blend") else []
    found, refused = [], []
    for dirpath, dirnames, filenames in os.walk(base, followlinks=False):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in sorted(filenames):
            if not name.endswith(".blend"):
                continue
            candidate = os.path.join(dirpath, name)
            real = os.path.realpath(candidate)
            if _authorized(real, roots) is None:
                refused.append({"path": candidate, "resolves_to": real})
                continue
            found.append(real)
    return sorted(set(found)), refused


def _page(items, params, key="cursor"):
    """Explicit bounds. The cursor is the next item itself, not an index."""
    limit = params.get("limit")
    cursor = params.get(key)
    if cursor is not None:
        items = [i for i in items if i >= cursor]
    truncated, next_cursor = False, None
    if limit is not None:
        limit = int(limit)
        if len(items) > limit:
            truncated = True
            next_cursor = items[limit]
            items = items[:limit]
    return items, {"limit": limit, "cursor": cursor,
                   "truncated": truncated, "next_cursor": next_cursor}


def _asset_group_names(path):
    with bpy.data.libraries.load(path, link=False, assets_only=True) as (src, _dst):
        return sorted(src.node_groups)


def _op_libraries(params):
    """List the roots. Counting files walks; it never opens a .blend."""
    roots = _roots(params)
    out = []
    for root in roots:
        rec = dict(root)
        path = root.get("path")
        if path and (os.path.isdir(path) or os.path.isfile(path)):
            files, refused = _blend_files(path, roots)
            rec["blend_files"] = len(files)
            if refused:
                rec["refused_symlinks"] = refused
        else:
            rec["blend_files"] = 0
            rec["error"] = "path is not readable"
        out.append(rec)
    return {"ok": True, "libraries": out,
            "note": "file counts are a directory walk; no .blend was opened"}


def _op_files(params):
    roots = _roots()
    name = params.get("library")
    chosen = [r for r in roots if name in (None, r["name"])]
    if name and not chosen:
        return {
            "ok": False,
            "error": f"no configured library named {name!r}",
            "candidates": [r["name"] for r in roots],
        }
    # Opening every .blend to report a count is what makes this unusable on a large
    # library, so it is opt-in and paged.
    probe = bool(params.get("probe_groups"))
    out, paging, refused_all = {}, {}, {}
    for root in chosen:
        path = root.get("path")
        if not path or not (os.path.isdir(path) or os.path.isfile(path)):
            continue
        files, refused = _blend_files(path, roots)
        page, bounds = _page(files, params)
        entries = []
        for blend in page:
            rec = {"path": blend}
            if probe:
                try:
                    rec["asset_node_groups"] = len(_asset_group_names(blend))
                except Exception as exc:
                    rec["error"] = f"{type(exc).__name__}: {exc}"
            entries.append(rec)
        out[root["name"]] = entries
        paging[root["name"]] = {**bounds, "of": len(files)}
        if refused:
            refused_all[root["name"]] = refused
    payload = {"ok": True, "files": out, "paging": paging, "probed_groups": probe}
    if refused_all:
        payload["refused_symlinks"] = refused_all
    return payload


def _op_groups(params):
    roots = _roots(params)
    path = params.get("path")
    if not path:
        return {"ok": False, "error": "pass `path` to a .blend inside a configured library"}
    path = bpy.path.abspath(path)
    root = _authorized(path, roots)
    if root is None:
        return {
            "ok": False,
            "error": "path is outside every configured asset library",
            "path": path,
            "allowed_roots": [r["path"] for r in roots],
            "hint": "ask the user to name or authorize this path",
        }
    if not os.path.isfile(path):
        return {"ok": False, "error": f"no such file: {path}"}
    try:
        names = _asset_group_names(path)
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}", "path": path}
    page, bounds = _page(names, params)
    return {
        "ok": True,
        "path": path,
        "library": root["name"],
        "asset_node_groups": page,
        "paging": {**bounds, "of": len(names)},
        "note": "names only - a group's tree type and interface need operation='inspect'",
    }


def _op_inspect(params):
    roots = _roots(params)
    path, group = params.get("path"), params.get("group")
    if not path or not group:
        return {"ok": False, "error": "pass both `path` and `group`"}
    path = os.path.realpath(bpy.path.abspath(path))
    root = _authorized(path, roots)
    if root is None:
        return {
            "ok": False,
            "error": "path is outside every configured asset library",
            "path": path,
            "allowed_roots": [r["path"] for r in roots],
            "hint": "ask the user to name the file, then pass it in authorized_paths",
        }

    # A real user asset drags in more than node groups. Loading one group out of a
    # third-party library brought in 7 objects, 7 meshes and a material alongside
    # the 7 node groups, measured on 5.2.1 against a user library. Snapshot every
    # watched collection by name, not just node_groups, or the leftovers land in
    # the user's file.
    before_counts = _counts()
    before_names = {c: {d.name for d in getattr(bpy.data, c)} for c in _WATCHED}
    payload = {"ok": False, "path": path, "library": root["name"], "group": group}

    try:
        with bpy.data.libraries.load(path, link=False, assets_only=True) as (src, dst):
            if group not in src.node_groups:
                payload["error"] = f"no asset node group named {group!r} in this file"
                payload["candidates"] = sorted(src.node_groups)
                return payload
            dst.node_groups = [group]

        # Use the datablock the load handed back, never a name lookup. Blender
        # suffixes a colliding name, so `bpy.data.node_groups.get(group)` returns
        # the user's own group of that name and this would report on the wrong one.
        loaded = next((g for g in dst.node_groups if g is not None), None)
        if loaded is None:
            payload["error"] = "the group did not appear after loading"
            return payload
        payload["loaded_as"] = loaded.name
        payload["name_collided"] = loaded.name != group

        interface = []
        for item in loaded.interface.items_tree:
            rec = {
                "item_type": item.item_type,
                "name": item.name,
                "identifier": getattr(item, "identifier", None),
                "in_out": getattr(item, "in_out", None),
                "panel": item.parent.name if getattr(item, "parent", None) else None,
            }
            if item.item_type == "SOCKET":
                rec["socket_type"] = item.socket_type
                if hasattr(item, "default_value"):
                    rec["default_value"] = _jsonable(item.default_value)
            interface.append(rec)

        inputs = [i for i in interface if i.get("in_out") == "INPUT"]
        names = [i["name"] for i in inputs]
        duplicates = sorted({n for n in names if names.count(n) > 1})

        meta = None
        if loaded.asset_data:
            meta = {
                "description": loaded.asset_data.description,
                "author": loaded.asset_data.author,
                "catalog_id": loaded.asset_data.catalog_simple_name,
                "tags": [t.name for t in loaded.asset_data.tags],
            }

        payload.update(
            {
                "ok": True,
                "tree_type": loaded.bl_idname,
                "kind": _TREE_LABEL.get(loaded.bl_idname, loaded.bl_idname),
                "node_count": len(loaded.nodes),
                "interface": interface,
                "input_count": len(inputs),
                "panels": sorted({i["panel"] for i in interface if i.get("panel")}),
                "duplicate_input_names": duplicates,
                "direct_dependencies": sorted(
                    {n.node_tree.name for n in loaded.nodes
                     if getattr(n, "node_tree", None) is not None}
                ),
                "asset_metadata": meta,
            }
        )
    except Exception as exc:
        payload["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        # Remove exactly what this call brought in - the named group and every
        # dependency that came with it, in every collection, not only node groups.
        # Objects go first so their mesh data drops to zero users. Never a broad
        # orphan purge: that would take the user's unrelated unused data too.
        # The closure this load actually created, per collection, by identity.
        # Nested node groups are only part of it: an asset can bring objects,
        # meshes and materials that no node references.
        pulled_in = {
            c: sorted({d.name for d in getattr(bpy.data, c)} - before_names[c])
            for c in _WATCHED
        }
        payload["dependency_closure"] = {
            c: [{"name": n, "type": c} for n in v] for c, v in pulled_in.items() if v
        }
        payload["dependency_closure_size"] = sum(len(v) for v in pulled_in.values())
        for coll in _REMOVE_ORDER:
            for name in pulled_in.get(coll, []):
                existing = getattr(bpy.data, coll).get(name)
                if existing is not None:
                    try:
                        getattr(bpy.data, coll).remove(existing, do_unlink=True)
                    except Exception as exc:
                        payload.setdefault("cleanup_errors", {})[f"{coll}/{name}"] = (
                            f"{type(exc).__name__}: {exc}"
                        )
        after_counts = _counts()
        residual = {
            k: [before_counts[k], after_counts[k]]
            for k in before_counts
            if before_counts[k] != after_counts[k]
        }
        groups_pulled = pulled_in.get("node_groups", [])
        payload["cleanup"] = {
            "loaded_datablocks": {c: v for c, v in pulled_in.items() if v},
            "loaded_count": sum(len(v) for v in pulled_in.values()),
            "counts_restored": not residual,
            "residual_counts": residual,
            "method": "targeted remove of every datablock this call loaded; never orphans_purge",
        }
        payload["append_cost"] = {
            "extra_node_groups": max(len(groups_pulled) - 1, 0),
            "other_datablocks": {c: len(v) for c, v in pulled_in.items()
                                 if v and c != "node_groups"},
            "note": "dependency weight is per asset, not a property of the library; "
                    "an asset can bring objects and meshes, not only node groups",
        }
    return payload


_OPERATIONS = {
    "libraries": _op_libraries,
    "files": _op_files,
    "groups": _op_groups,
    "inspect": _op_inspect,
}


def run(params=None):
    params = params or {}
    op = params.get("operation", "libraries")
    fn = _OPERATIONS.get(op)
    if fn is None:
        return {"ok": False, "error": f"unknown operation {op!r}",
                "operations": sorted(_OPERATIONS)}
    payload = fn(params)
    payload["operation"] = op
    payload["blender"] = bpy.app.version_string
    payload["blender_version"] = list(bpy.app.version)
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
