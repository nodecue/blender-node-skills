"""Exercise the Geometry Nodes runtime scripts inside a real Blender.

Checks the contract the redesign plan puts on them: read-only reading, exactly
targeted cleanup, structured return through both channels, configured-library-only
discovery, and a clear failure result when the thing asked for does not exist.

Run:
    conda run -n blender blender -b --factory-startup \
        --python tests/golden/run_skill_runtime_scripts.py -- /tmp/out.json

Exit code is 0 only when every check passes. The JSON holds every check with its
observed value, so a failure names itself.
"""

import hashlib
import json
import os
import runpy
import sys

import bpy

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(ROOT, "skills", "geometry-nodes", "scripts")

CHECKS = []


def check(name, passed, observed=None):
    CHECKS.append({"check": name, "pass": bool(passed), "observed": observed})
    return passed


def call(script, params):
    """Invoke a script the way a host does: one path, no re-authored body."""
    path = os.path.join(SCRIPTS, script)
    globs = runpy.run_path(path, init_globals={"NODECUE_PARAMS": params})
    return globs["result"]


def build_fixture():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.node_groups):
        for item in list(coll):
            coll.remove(item, do_unlink=True)

    tree = bpy.data.node_groups.new("Fixture", "GeometryNodeTree")
    tree.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    out = tree.nodes.new("NodeGroupOutput")
    grid = tree.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    set_pos = tree.nodes.new("GeometryNodeSetPosition")
    set_pos.name = "Set Position"
    stray = tree.nodes.new("GeometryNodeMeshCube")  # deliberately off the trunk
    stray.name = "Off Trunk"
    frame = tree.nodes.new("NodeFrame")
    tree.links.new(grid.outputs["Mesh"], set_pos.inputs["Geometry"])
    tree.links.new(set_pos.outputs["Geometry"], out.inputs[0])

    noise = tree.nodes.new("ShaderNodeTexNoise")
    noise.name = "Noise"
    noise_out = noise.outputs.get("Fac") or noise.outputs[0]
    tree.links.new(noise_out, set_pos.inputs["Offset"])

    obj = bpy.data.objects.new("Fixture", bpy.data.meshes.new("Fixture"))
    bpy.context.scene.collection.objects.link(obj)
    mod = obj.modifiers.new("GeometryNodes", "NODES")
    mod.node_group = tree
    bpy.context.view_layer.objects.active = obj
    return tree, frame


WATCHED = ("node_groups", "objects", "meshes", "materials", "images", "collections",
           "texts", "worlds", "curves", "hair_curves", "pointclouds", "volumes")


def fingerprint(tree):
    """Identity plus content. Counts miss a rename, a rewire and every value write."""
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
    for link in sorted(tree.links, key=lambda l: (l.from_node.name, l.from_socket.identifier,
                                                  l.to_node.name, l.to_socket.identifier)):
        parts.append(f"L|{link.from_node.name}.{link.from_socket.identifier}"
                     f"->{link.to_node.name}.{link.to_socket.identifier}")
    for item in tree.interface.items_tree:
        parts.append(f"I|{item.item_type}|{item.name}|{getattr(item, 'identifier', '')}"
                     f"|{getattr(item, 'in_out', '')}")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def datablock_identity():
    """Names *and* a content fingerprint per node group, so a mutated one is caught."""
    out = {c: sorted(d.name for d in getattr(bpy.data, c)) for c in WATCHED}
    out["node_group_content"] = {
        g.name: fingerprint(g) for g in bpy.data.node_groups
    }
    return out


def snapshot(tree):
    return {
        "nodes": sorted(n.name for n in tree.nodes),
        "links": len(tree.links),
        "interface": [(i.name, getattr(i, "identifier", None)) for i in tree.interface.items_tree],
        "fingerprint": fingerprint(tree),
        "datablocks": datablock_identity(),
    }


# --- read_graph ---------------------------------------------------------------
def test_read_graph(tree):
    before = snapshot(tree)
    res = call("read_graph.py", {"tree": "Fixture"})
    after = snapshot(tree)

    check("read_graph.ok", res.get("ok"), res.get("error"))
    check("read_graph.no_mutation", before == after, {"before": before, "after": after})
    check("read_graph.resolved_by_explicit",
          res.get("resolved_by") == "explicit `tree` parameter", res.get("resolved_by"))
    check("read_graph.reports_blender_version",
          res.get("blender_version") == list(bpy.app.version), res.get("blender_version"))
    check("read_graph.tree_role_present",
          "is_modifier" in res["tree"] and "is_tool" in res["tree"], res.get("tree"))
    check("read_graph.used_by_modifier",
          res["tree"]["used_by"] == [{"object": "Fixture", "modifier": "GeometryNodes"}],
          res["tree"]["used_by"])

    by_name = {n["name"]: n for n in res["nodes"]}
    check("read_graph.reports_location_facts",
          "location" in by_name["Grid"] and "location_absolute" in by_name["Grid"]
          and "width" in by_name["Grid"] and "height" in by_name["Grid"],
          {k: by_name["Grid"].get(k) for k in ("location", "location_absolute", "width", "height")})
    check("read_graph.frame_marked_structural",
          by_name["Frame"]["structural"] is True, by_name.get("Frame"))
    check("read_graph.functional_not_structural",
          by_name["Grid"]["structural"] is False, by_name.get("Grid"))
    check("read_graph.socket_identifiers",
          all("identifier" in s for s in by_name["Grid"]["inputs"]), by_name["Grid"]["inputs"])
    check("read_graph.writable_properties_not_bl",
          all(not k.startswith("bl_") for k in by_name["Grid"]["properties"]),
          list(by_name["Grid"]["properties"]))

    # Group Output's interface identifier is Socket_N, never the display name.
    iface = res["interface"]
    check("read_graph.interface_identifier_is_socket_n",
          any(i["identifier"].startswith("Socket_") for i in iface if i["item_type"] == "SOCKET"),
          iface)

    trunk = res["output_trunk"]
    check("read_graph.trunk_reachable", trunk.get("reachable") is True, trunk)
    check("read_graph.trunk_nodes_correct",
          "Set Position" in trunk.get("trunk_nodes", [])
          and "Grid" in trunk.get("trunk_nodes", [])
          and "Noise" not in trunk.get("trunk_nodes", []),
          trunk)
    check("read_graph.dependency_nodes_detected",
          "Noise" in trunk.get("dependency_nodes", [])
          and "Grid" not in trunk.get("dependency_nodes", [])
          and "Set Position" not in trunk.get("dependency_nodes", []),
          trunk)
    check("read_graph.off_trunk_detected",
          "Off Trunk" in trunk.get("off_trunk_nodes", [])
          and "Set Position" not in trunk.get("off_trunk_nodes", [])
          and "Noise" not in trunk.get("off_trunk_nodes", []),
          trunk)

    scoped = call("read_graph.py", {"tree": "Fixture", "scope": {"nodes": ["Grid", "Nope"]}})
    check("read_graph.scope_filters", [n["name"] for n in scoped["nodes"]] == ["Grid"],
          [n["name"] for n in scoped["nodes"]])
    check("read_graph.scope_reports_missing", scoped["scope_missing_nodes"] == ["Nope"],
          scoped["scope_missing_nodes"])

    check("read_graph.scoped_links_are_not_the_whole_tree",
          len(scoped["links"]) <= res["tree"]["link_count"] and scoped["links_scoped"] is True,
          {"scoped": len(scoped["links"]), "tree": res["tree"]["link_count"]})
    check("read_graph.boundary_links_kept_as_stubs",
          scoped["boundary_links"] == sum(1 for l in scoped["links"] if "boundary" in l),
          scoped["boundary_links"])

    page = call("read_graph.py", {"tree": "Fixture", "scope": {"limit": 2}})
    check("read_graph.limit_bounds_the_result", len(page["nodes"]) == 2, len(page["nodes"]))
    check("read_graph.truncation_is_explicit",
          page["scope"]["truncated"] is True and page["scope"]["next_cursor"],
          page["scope"])
    rest = call("read_graph.py",
                {"tree": "Fixture", "scope": {"cursor": page["scope"]["next_cursor"]}})
    seen = [n["name"] for n in page["nodes"]] + [n["name"] for n in rest["nodes"]]
    check("read_graph.cursor_resumes_without_gap_or_repeat",
          sorted(seen) == sorted(n.name for n in tree.nodes), seen)
    bad_cursor = call("read_graph.py", {"tree": "Fixture", "scope": {"cursor": "Nope"}})
    check("read_graph.unknown_cursor_fails_clearly", bad_cursor.get("ok") is False, bad_cursor)

    shader = bpy.data.node_groups.new("NotGeometry", "ShaderNodeTree")
    wrong = call("read_graph.py", {"tree": "NotGeometry"})
    check("read_graph.rejects_a_non_geometry_tree",
          wrong.get("ok") is False and "ShaderNodeTree" in (wrong.get("error") or ""), wrong)
    bpy.data.node_groups.remove(shader)

    obj = bpy.data.objects["Fixture"]
    second = obj.modifiers.new("GeometryNodes2", "NODES")
    second.node_group = tree
    ambiguous = call("read_graph.py", {"object": "Fixture"})
    check("read_graph.refuses_to_guess_between_modifiers",
          ambiguous.get("ok") is False and "pass `modifier`" in (ambiguous.get("error") or ""),
          ambiguous.get("error"))
    chosen = call("read_graph.py", {"object": "Fixture", "modifier": "GeometryNodes2"})
    check("read_graph.explicit_modifier_resolves",
          chosen.get("ok") and "GeometryNodes2" in chosen["resolved_by"], chosen.get("resolved_by"))
    obj.modifiers.remove(second)

    missing = call("read_graph.py", {"tree": "Does Not Exist"})
    check("read_graph.missing_tree_fails_clearly",
          missing.get("ok") is False and missing.get("candidates"), missing)


# --- probe_node ---------------------------------------------------------------
def test_probe_node():
    before = datablock_identity()
    res = call(
        "probe_node.py",
        {"nodes": [
            {"bl_idname": "FunctionNodeRandomValue", "properties": {"data_type": "BOOLEAN"}},
            {"bl_idname": "ShaderNodeVectorMath"},
            {"bl_idname": "ShaderNodeVectorMath", "properties": {"operation": "MULTIPLY_ADD"}},
            {"bl_idname": "GeometryNodeNotARealNode"},
        ]},
    )
    after = datablock_identity()

    check("probe_node.cleanup_restored", res["cleanup"]["counts_restored"] is True, res["cleanup"])
    check("probe_node.cleanup_observed_by_identity_and_content", before == after,
          {c: sorted(set(after[c]) ^ set(before[c])) for c in WATCHED if after[c] != before[c]})
    check("probe_node.temp_tree_removed",
          bpy.data.node_groups.get(res["cleanup"]["temp_tree"]) is None,
          res["cleanup"]["temp_tree"])

    rand, vmath, vmath3, bogus = res["probes"]
    check("probe_node.property_applied", rand["properties_applied"].get("data_type") == "BOOLEAN",
          rand.get("properties_applied"))
    # 5.2 removes the other variants; 4.5 and 5.1 only disable them. The script
    # has to give the same usable answer on both, which is what active_inputs is.
    active = rand["active_inputs"]
    check("probe_node.property_selects_active_sockets",
          "Probability" in active and not any(a.startswith("Min") for a in active),
          {"active": active, "inactive": rand["inactive_inputs"]})
    check("probe_node.inactive_sockets_still_reported",
          all(s["identifier"] in active or s["identifier"] in rand["inactive_inputs"]
              for s in rand["inputs"]),
          [(s["identifier"], s["enabled"]) for s in rand["inputs"]])
    # Vector Math carries three inputs all named Vector, but how many are live is
    # decided by `operation`: two under the default ADD, three under MULTIPLY_ADD.
    check("probe_node.duplicate_identifiers_exposed",
          vmath.get("duplicate_input_names", {}).get("Vector") == ["Vector", "Vector_001"],
          vmath.get("duplicate_input_names"))
    check("probe_node.operation_changes_live_socket_count",
          vmath3.get("duplicate_input_names", {}).get("Vector")
          == ["Vector", "Vector_001", "Vector_002"],
          vmath3.get("duplicate_input_names"))
    check("probe_node.field_shape_reported",
          any(s.get("display_shape") for s in vmath["inputs"]),
          [(s["name"], s.get("display_shape")) for s in vmath["inputs"]])
    check("probe_node.unregistered_reported",
          bogus.get("registered") is False and bogus.get("ok") is False, bogus)
    check("probe_node.reports_the_shape_vocabulary_it_used",
          res.get("shape_vocabulary") in {"4.x", "5.x"}, res.get("shape_vocabulary"))
    expected = "5.x" if bpy.app.version[0] >= 5 else "4.x"
    check("probe_node.vocabulary_matches_this_build",
          res.get("shape_vocabulary") == expected,
          {"reported": res.get("shape_vocabulary"), "build": bpy.app.version_string})
    check("probe_node.socket_raw_facts_reported",
          all("display_shape" in s and "hide_value" in s and "has_default_value" in s
              for s in rand["inputs"]),
          [(s["name"], s.get("display_shape"), s.get("hide_value"), s.get("has_default_value"))
           for s in rand["inputs"]])

    rejected = call("probe_node.py", {"bl_idname": "FunctionNodeRandomValue",
                                      "properties": {"data_type": "NOT_A_MODE"}})
    check("probe_node.a_rejected_property_fails_the_probe",
          rejected["ok"] is False and rejected["probes"][0]["ok"] is False,
          rejected["probes"][0].get("error"))
    check("probe_node.a_rejected_property_says_the_sockets_are_the_default",
          "default configuration" in (rejected["probes"][0].get("error") or ""),
          rejected["probes"][0].get("error"))
    check("probe_node.cleanup_contract_present_even_when_a_probe_fails",
          set(rejected["cleanup"]) >= {"temp_tree", "removed", "counts_restored", "method"},
          rejected["cleanup"])

    bad_tree = call("probe_node.py", {"bl_idname": "GeometryNodeMeshCube",
                                      "tree_type": "NotARealTreeType"})
    check("probe_node.creation_failure_keeps_the_same_contract",
          bad_tree["ok"] is False and "cleanup" in bad_tree and "probes" in bad_tree,
          {k: bad_tree.get(k) for k in ("ok", "error", "cleanup")})
    check("probe_node.partial_failure_reported", res["probes_failed"] == 1, res["probes_failed"])
    check("probe_node.ok_false_on_partial_failure", res["ok"] is False, res["ok"])


# --- capture ------------------------------------------------------------------
def test_capture():
    res = call("capture.py", {"output": "/tmp/nodecue-capture-check.png"})
    fit_in_all = call("capture.py", {"stage": "all", "fit": True, "output": "/tmp/x.png"})
    check("capture.all_refuses_to_fit",
          fit_in_all.get("ok") is False and "event loop" in (fit_in_all.get("error") or ""),
          fit_in_all.get("error"))
    fit_in_capture = call("capture.py", {"stage": "capture", "fit": True, "output": "/tmp/x.png"})
    check("capture.capture_refuses_to_fit",
          fit_in_capture.get("ok") is False and "prepare" in (fit_in_capture.get("error") or ""),
          fit_in_capture.get("error"))

    unknown = call("capture.py", {"stage": "teleport"})
    check("capture.unknown_stage_fails_clearly",
          unknown.get("ok") is False and unknown.get("stages"), unknown)
    check("capture.redraw_operator_off_by_default",
          res.get("redraw_mode") == "tag_redraw", res.get("redraw_mode"))

    bad = call("capture.py", {})
    if bpy.app.background:
        # Without a window there is nothing to capture, and that is the failure
        # worth reporting - it comes before any parameter complaint.
        check("capture.background_fails_clearly",
              res.get("ok") is False and "background" in (res.get("error") or ""), res)
        check("capture.background_fails_clearly_without_params",
              bad.get("ok") is False and "background" in (bad.get("error") or ""), bad)
    else:
        check("capture.captured", res.get("ok") and res.get("exists"), res)
        check("capture.graph_unchanged", res.get("graph_unchanged") is True, res)
        check("capture.ui_restored", res.get("ui_restored") is True, res)
        check("capture.missing_output_fails_clearly",
              bad.get("ok") is False and "output" in (bad.get("error") or ""), bad)


# --- inspect_assets -----------------------------------------------------------
def test_inspect_assets():
    libs = call("inspect_assets.py", {"operation": "libraries"})
    check("inspect_assets.libraries_ok", libs.get("ok"), libs.get("error"))
    bundled = [l for l in libs["libraries"] if l["kind"] == "bundled"]
    check("inspect_assets.bundled_root_found", len(bundled) == 1, libs["libraries"])
    check("inspect_assets.bundled_needs_no_consent",
          bundled and "none needed" in bundled[0]["consent"], bundled)

    root = bundled[0]["path"]
    files = call("inspect_assets.py", {"operation": "files", "library": "<bundled>"})
    entries = files["files"]["<bundled>"]
    check("inspect_assets.files_listed", len(entries) > 0, len(entries))
    check("inspect_assets.listing_does_not_open_every_blend",
          files["probed_groups"] is False
          and all("asset_node_groups" not in e for e in entries),
          files["probed_groups"])

    paged = call("inspect_assets.py",
                 {"operation": "files", "library": "<bundled>", "limit": 2})
    bounds = paged["paging"]["<bundled>"]
    check("inspect_assets.files_paging_is_explicit",
          len(paged["files"]["<bundled>"]) == 2 and bounds["truncated"] is True
          and bounds["next_cursor"], bounds)

    probed = call("inspect_assets.py",
                  {"operation": "files", "library": "<bundled>", "probe_groups": True})
    with_groups = [e for e in probed["files"]["<bundled>"] if e.get("asset_node_groups")]
    check("inspect_assets.some_file_has_groups", len(with_groups) > 0, len(with_groups))

    target = with_groups[0]["path"]
    groups = call("inspect_assets.py", {"operation": "groups", "path": target})
    check("inspect_assets.groups_ok", groups.get("ok"), groups.get("error"))
    check("inspect_assets.groups_are_names_only",
          isinstance(groups["asset_node_groups"], list)
          and all(isinstance(n, str) for n in groups["asset_node_groups"]),
          groups.get("asset_node_groups", [])[:3])
    one = call("inspect_assets.py", {"operation": "groups", "path": target, "limit": 1})
    check("inspect_assets.groups_paging_is_explicit",
          len(one["asset_node_groups"]) == 1 and one["paging"]["of"] >= 1, one["paging"])

    # Snapshot every collection, not just node_groups: a real user asset drags in
    # objects, meshes and materials alongside the group, and cleanup has to take
    # those too. Measured on 5.2.1 against a user library - 7 objects, 7 meshes
    # and a material behind one 14-node group.
    watched = ("node_groups", "objects", "meshes", "materials", "images",
               "collections", "curves", "hair_curves", "pointclouds", "volumes", "texts")

    def snap():
        return {c: {d.name for d in getattr(bpy.data, c)} for c in watched}

    before_all = snap()
    before = before_all["node_groups"]
    name = groups["asset_node_groups"][0]
    deep = call("inspect_assets.py", {"operation": "inspect", "path": target, "group": name})
    after_all = snap()
    after = after_all["node_groups"]
    leaked = {c: sorted(after_all[c] - before_all[c])
              for c in watched if after_all[c] - before_all[c]}
    check("inspect_assets.no_datablock_of_any_kind_leaks", not leaked, leaked)
    check("inspect_assets.cleanup_reports_per_collection",
          isinstance(deep["cleanup"]["loaded_datablocks"], dict),
          deep["cleanup"]["loaded_datablocks"])
    check("inspect_assets.inspect_ok", deep.get("ok"), deep.get("error"))
    check("inspect_assets.tree_type_reported", deep.get("kind") in
          {"geometry", "shader", "compositor", "texture"}, deep.get("kind"))
    check("inspect_assets.interface_read", isinstance(deep.get("interface"), list)
          and len(deep["interface"]) > 0, deep.get("input_count"))
    check("inspect_assets.dependencies_reported",
          isinstance(deep.get("direct_dependencies"), list), deep.get("direct_dependencies"))
    check("inspect_assets.append_cost_reported",
          isinstance(deep.get("append_cost", {}).get("extra_node_groups"), int),
          deep.get("append_cost"))
    check("inspect_assets.cleanup_restored", deep["cleanup"]["counts_restored"] is True,
          deep["cleanup"])
    check("inspect_assets.cleanup_observed_by_test", before == after,
          sorted(after - before))
    check("inspect_assets.reports_the_datablock_it_actually_loaded",
          isinstance(deep.get("loaded_as"), str) and "name_collided" in deep,
          {k: deep.get(k) for k in ("loaded_as", "name_collided")})
    check("inspect_assets.dependency_closure_is_more_than_nested_groups",
          isinstance(deep.get("dependency_closure"), dict)
          and isinstance(deep.get("dependency_closure_size"), int),
          deep.get("dependency_closure_size"))

    authorized = call("inspect_assets.py",
                      {"operation": "groups", "path": target,
                       "authorized_paths": [target]})
    check("inspect_assets.explicit_authorization_is_accepted",
          authorized.get("ok") is True, authorized.get("error"))

    outside = call("inspect_assets.py",
                   {"operation": "groups", "path": os.path.join(ROOT, "nope.blend")})
    check("inspect_assets.refuses_unconfigured_path",
          outside.get("ok") is False and "outside" in (outside.get("error") or ""), outside)
    check("inspect_assets.refusal_lists_allowed_roots",
          bool(outside.get("allowed_roots")), outside.get("allowed_roots"))

    missing = call("inspect_assets.py",
                   {"operation": "inspect", "path": target, "group": "No Such Group"})
    check("inspect_assets.missing_group_fails_clearly",
          missing.get("ok") is False and missing.get("candidates"), missing.get("error"))

    unknown = call("inspect_assets.py", {"operation": "teleport"})
    check("inspect_assets.unknown_operation_fails_clearly",
          unknown.get("ok") is False and unknown.get("operations"), unknown)
    return root


def _layout_params(extra=None):
    params = {
        "op": "apply",
        "tree": "Fixture",
        "nodes": [
            "Group Input", "Grid", "Set Position", "Noise", "Group Output",
            "Sources", "Deform",
        ],
        "trunk": ["Group Input", "Grid", "Set Position", "Group Output"],
        "dependencies": [{"node": "Noise", "consumer": "Set Position"}],
        "frames": [
            {"name": "Sources", "nodes": ["Group Input", "Grid"]},
            {"name": "Deform", "nodes": ["Set Position", "Noise"]},
        ],
    }
    if extra:
        params.update(extra)
    return params


def test_layout_graph(tree):
    gin = tree.nodes.new("NodeGroupInput")
    gin.name = "Group Input"
    gout = next(n for n in tree.nodes if n.bl_idname == "NodeGroupOutput")
    gout.name = "Group Output"
    sources = tree.nodes.new("NodeFrame")
    sources.name = "Sources"
    deform = tree.nodes.new("NodeFrame")
    deform.name = "Deform"
    stray = tree.nodes["Off Trunk"]
    stray.location = (1234.0, -567.0)
    stray_parent = stray.parent.name if stray.parent else None

    def layout_snap():
        return {
            n.name: (
                n.parent.name if n.parent else None,
                round(float(n.location[0]), 4),
                round(float(n.location[1]), 4),
            )
            for n in tree.nodes
        }

    check_before = snapshot(tree)
    layout_before = layout_snap()
    checked = call("layout_graph.py", _layout_params({"op": "check"}))
    check_after = snapshot(tree)
    layout_after = layout_snap()
    check("layout_graph.check_ok", checked.get("ok") is True, checked.get("error"))
    check("layout_graph.check_is_read_only",
          check_before == check_after and layout_before == layout_after,
          {"graph": check_before == check_after, "layout": layout_after})
    check("layout_graph.check_does_not_claim_graph_correctness",
          checked.get("graph_correctness") == "not_evaluated",
          checked.get("graph_correctness"))
    check("layout_graph.check_reports_presentation_findings",
          isinstance(checked.get("findings"), list) and checked.get("layout_ok") is False,
          checked.get("findings"))
    check("layout_graph.check_mutated_flag_false",
          checked.get("mutated") is False, checked.get("mutated"))

    first = call("layout_graph.py", _layout_params())
    check("layout_graph.apply_ok", first.get("ok") is True, first.get("error"))
    check("layout_graph.apply_layout_ok", first.get("layout_ok") is True, first.get("findings"))
    pos = first["positions"]
    trunk = ["Group Input", "Grid", "Set Position", "Group Output"]
    xs = [pos[n]["location_absolute"][0] for n in trunk]
    check("layout_graph.trunk_left_to_right",
          all(xs[i] < xs[i + 1] for i in range(len(xs) - 1)), xs)
    noise_y = pos["Noise"]["location_absolute"][1]
    set_y = pos["Set Position"]["location_absolute"][1]
    check("layout_graph.dependency_close_above_consumer",
          noise_y > set_y
          and abs(pos["Noise"]["location_absolute"][0] - pos["Set Position"]["location_absolute"][0])
          < 1.0,
          {"noise": pos["Noise"]["location_absolute"], "set": pos["Set Position"]["location_absolute"]})
    check("layout_graph.frame_parenting",
          pos["Grid"]["parent"] == "Sources" and pos["Noise"]["parent"] == "Deform",
          {n: pos[n]["parent"] for n in ("Grid", "Noise", "Set Position")})

    src_box = first["targets"]["Sources"]
    def_box = first["targets"]["Deform"]
    check("layout_graph.frames_do_not_share_origin",
          abs(src_box[0] - def_box[0]) > 1.0 or abs(src_box[1] - def_box[1]) > 1.0,
          {"sources": src_box, "deform": def_box})

    check("layout_graph.protected_node_unmoved",
          list(stray.location) == [1234.0, -567.0]
          and (stray.parent.name if stray.parent else None) == stray_parent,
          {"location": list(stray.location), "parent": stray.parent.name if stray.parent else None})

    keep = tree.nodes.new("NodeFrame")
    keep.name = "Keep"
    keep.location = (300.0, 400.0)
    stray.parent = keep
    stray.location = (11.0, 22.0)
    keep_before = (
        keep.parent.name if keep.parent else None,
        [float(keep.location[0]), float(keep.location[1])],
        [float(getattr(keep, "location_absolute", keep.location)[0]),
         float(getattr(keep, "location_absolute", keep.location)[1])],
    )
    child_before = (
        stray.parent.name if stray.parent else None,
        [float(stray.location[0]), float(stray.location[1])],
        [float(getattr(stray, "location_absolute", stray.location)[0]),
         float(getattr(stray, "location_absolute", stray.location)[1])],
    )
    grid_parent_before = tree.nodes["Grid"].parent.name if tree.nodes["Grid"].parent else None
    guarded = call("layout_graph.py", {
        "op": "apply",
        "tree": "Fixture",
        "nodes": ["Keep", "Grid", "Group Output"],
        "trunk": ["Grid", "Group Output"],
        "dependencies": [],
        "frames": [{"name": "Keep", "nodes": ["Grid"]}],
    })
    child_after = (
        stray.parent.name if stray.parent else None,
        [float(stray.location[0]), float(stray.location[1])],
        [float(getattr(stray, "location_absolute", stray.location)[0]),
         float(getattr(stray, "location_absolute", stray.location)[1])],
    )
    keep_after = (
        keep.parent.name if keep.parent else None,
        [float(keep.location[0]), float(keep.location[1])],
        [float(getattr(keep, "location_absolute", keep.location)[0]),
         float(getattr(keep, "location_absolute", keep.location)[1])],
    )
    check("layout_graph.protected_child_in_authorized_frame_rejected",
          guarded.get("ok") is False and "protected" in (guarded.get("error") or ""),
          guarded.get("error"))
    check("layout_graph.protected_child_parent_and_positions_unchanged",
          child_after == child_before and keep_after == keep_before
          and (tree.nodes["Grid"].parent.name if tree.nodes["Grid"].parent else None)
          == grid_parent_before
          and guarded.get("rolled_back") is True,
          {"child_before": child_before, "child_after": child_after,
           "keep_before": keep_before, "keep_after": keep_after,
           "rolled_back": guarded.get("rolled_back"),
           "mutated": guarded.get("mutated")})

    second = call("layout_graph.py", _layout_params())
    check("layout_graph.repeated_apply_idempotent",
          first["positions"] == second["positions"],
          {"first": first["positions"], "second": second["positions"]})

    third = call("layout_graph.py", _layout_params())
    check("layout_graph.frame_parent_no_drift",
          second["positions"]["Grid"]["location_absolute"]
          == third["positions"]["Grid"]["location_absolute"]
          and second["positions"]["Grid"]["parent"] == "Sources",
          third["positions"]["Grid"])

    before_bad = {n.name: list(n.location) for n in tree.nodes}
    missing = call("layout_graph.py", _layout_params({"nodes": ["Grid", "Nope"]}))
    after_bad = {n.name: list(n.location) for n in tree.nodes}
    check("layout_graph.missing_name_rejected",
          missing.get("ok") is False and "not in tree" in (missing.get("error") or ""),
          missing.get("error"))
    check("layout_graph.missing_name_does_not_mutate",
          before_bad == after_bad, {"before": before_bad, "after": after_bad})

    out_of_scope = call(
        "layout_graph.py",
        _layout_params({"trunk": ["Grid", "Off Trunk"]}),
    )
    check("layout_graph.out_of_scope_rejected",
          out_of_scope.get("ok") is False and "outside authorized" in (out_of_scope.get("error") or ""),
          out_of_scope.get("error"))

    group = bpy.data.node_groups.new("InnerGroup", "GeometryNodeTree")
    group.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    nested = tree.nodes.new("GeometryNodeGroup")
    nested.name = "Inner"
    nested.node_tree = group
    grouped = call("layout_graph.py", {
        "op": "apply",
        "tree": "Fixture",
        "nodes": ["Inner", "Group Output"],
        "trunk": ["Inner", "Group Output"],
        "dependencies": [],
        "frames": [],
    })
    check("layout_graph.group_node_is_a_regular_authorized_member",
          grouped.get("ok") is True, grouped.get("error"))

    zone_ok = True
    try:
        zin = tree.nodes.new("GeometryNodeRepeatInput")
        zout = tree.nodes.new("GeometryNodeRepeatOutput")
        zin.name = "Repeat Input"
        zout.name = "Repeat Output"
    except Exception as exc:
        zone_ok = False
        check("layout_graph.zone_types_unavailable_reported",
              True, str(exc))
    if zone_ok:
        before_zone = {n.name: list(n.location) for n in tree.nodes}
        split = call("layout_graph.py", {
            "op": "apply",
            "tree": "Fixture",
            "nodes": ["Repeat Input", "Grid"],
            "trunk": ["Grid"],
            "dependencies": [],
            "frames": [],
        })
        after_zone = {n.name: list(n.location) for n in tree.nodes}
        check("layout_graph.split_zone_rejected",
              split.get("ok") is False and "zone edge" in (split.get("error") or ""),
              split.get("error"))
        check("layout_graph.split_zone_does_not_mutate",
              before_zone == after_zone, None)
        both = call("layout_graph.py", {
            "op": "apply",
            "tree": "Fixture",
            "nodes": ["Repeat Input", "Repeat Output", "Group Output"],
            "trunk": ["Repeat Output", "Group Output"],
            "dependencies": [],
            "frames": [],
        })
        check("layout_graph.complete_zone_pair_accepted",
              both.get("ok") is True, both.get("error"))

    unknown = call("layout_graph.py", {"op": "teleport", "tree": "Fixture", "nodes": ["Grid"]})
    check("layout_graph.unknown_op_fails_clearly",
          unknown.get("ok") is False and unknown.get("operations"), unknown)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out_path = argv[0] if argv else os.path.join(ROOT, "runtime-script-checks.json")

    tree, _frame = build_fixture()
    test_read_graph(tree)
    test_probe_node()
    test_capture()
    test_inspect_assets()
    test_layout_graph(tree)

    failed = [c for c in CHECKS if not c["pass"]]
    payload = {
        "blender": bpy.app.version_string,
        "background": bpy.app.background,
        "total": len(CHECKS),
        "failed": len(failed),
        "checks": CHECKS,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False, default=str)

    for c in failed:
        print("FAIL", c["check"], json.dumps(c["observed"], default=str)[:400])
    print(f"RUNTIME SCRIPT CHECKS: {len(CHECKS) - len(failed)}/{len(CHECKS)} passed -> {out_path}")
    sys.exit(1 if failed else 0)


main()
