"""Dump the identity facts of every node type creatable in a Geometry Nodes tree.

Node identity -- socket names, identifiers, types and RNA classes, tooltips,
writable RNA properties and their enum values -- is read from a running Blender
rather than maintained by hand. One dump per Blender version feeds
``tools/diff_node_dumps.py``, which computes the cross-version differences that
cannot be introspected from a single install.

Run inside Blender. ``--factory-startup`` is required: user add-ons register
extra node types and would change the set of creatable classes.

    blender -b --factory-startup --python tools/introspect_nodes.py -- \\
        --output docs/node-dumps/gn-5.2.0.json

The script also runs against the PyPI ``bpy`` wheel, where there is no ``--``
separator:

    python tools/introspect_nodes.py --output docs/node-dumps/gn-5.0.1.json

Run by plain CPython with ``--blender`` or ``--discover`` it becomes a launcher
instead, re-invoking itself inside each Blender it is given or finds:

    python tools/introspect_nodes.py --discover
    python tools/introspect_nodes.py --blender /path/to/Blender -o out.json

``--discover`` walks ``BLENDER_VERSIONS_ROOT`` (default ``~/blender_vers``) for
``*/blender-<version>-*/`` builds and takes the version from the directory name,
so no Blender path is written into this file. That layout is the maintainer's
evidence environment, not a product assumption -- see
``docs/node-dumps/README.md``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:  # Absent when this file is run as a launcher by plain CPython.
    import bpy
except ModuleNotFoundError:  # pragma: no cover - depends on the interpreter
    bpy = None

TREE_TYPE = "GeometryNodeTree"

DEFAULT_VERSIONS_ROOT = "~/blender_vers"
DEFAULT_OUTPUT_DIR = "docs/node-dumps"

# ``blender-5.1.2-macos-arm64+stable.ec6e62d40fa9`` -> ``5.1.2``. Anything not
# named ``blender-<version>-`` is a different application (upbge, bforartists)
# and is skipped rather than guessed at.
_BUILD_DIR_RE = re.compile(r"^blender-(\d+\.\d+(?:\.\d+)?)-")

# Where the executable sits inside an extracted build, per platform.
_EXECUTABLE_SUFFIXES = (
    ("Blender.app", "Contents", "MacOS", "Blender"),
    ("blender",),
    ("blender.exe",),
)

# Node properties that describe the editor presentation of a single node
# instance rather than the node type. ``bl_*`` is excluded separately: its
# ``bl_icon`` enum alone inflates a single node record to about 17 KB.
UI_PROPERTIES = frozenset(
    {
        "name",
        "label",
        "location",
        "location_absolute",
        "width",
        "height",
        "color",
        "select",
        "mute",
        "hide",
        "parent",
        "show_options",
        "show_preview",
        "show_texture",
        "use_custom_color",
        "warning_propagation",
    }
)


def _script_args(argv: list[str]) -> list[str]:
    """Return the arguments meant for this script.

    Blender passes its own arguments first and separates ours with ``--``.
    Under the ``bpy`` wheel the script is invoked directly and there is no
    separator.
    """
    if "--" in argv:
        return argv[argv.index("--") + 1 :]
    return argv[1:]


def parse_build_version(directory_name: str) -> str | None:
    """Return the Blender version encoded in an extracted build's directory name."""
    match = _BUILD_DIR_RE.match(directory_name)
    return match.group(1) if match else None


def version_sort_key(version: str) -> tuple[int, ...]:
    """Order versions numerically so 5.10 sorts after 5.2, not before it."""
    return tuple(int(part) for part in version.split("."))


def _executable_in(build_dir: Path) -> Path | None:
    for suffix in _EXECUTABLE_SUFFIXES:
        candidate = build_dir.joinpath(*suffix)
        if candidate.is_file():
            return candidate
    return None


def _channel_rank(channel: Path) -> tuple[int, str]:
    """Sort ``stable`` ahead of every other channel, then alphabetically."""
    return (0 if channel.name == "stable" else 1, channel.name)


def discover_blenders(root: str | Path) -> list[tuple[str, Path]]:
    """Find ``(version, executable)`` pairs under a versions root.

    The root holds one directory per channel (``stable``, ``daily``, ...), each
    containing extracted builds named ``blender-<version>-<platform>+<tag>``.
    When two channels carry the same version, ``stable`` wins: a dump is
    evidence, and a released build is the one worth citing.
    """
    root = Path(root).expanduser()
    found: dict[str, Path] = {}
    if not root.is_dir():
        return []
    for channel in sorted((p for p in root.iterdir() if p.is_dir()), key=_channel_rank):
        for build in sorted(p for p in channel.iterdir() if p.is_dir()):
            version = parse_build_version(build.name)
            if version is None or version in found:
                continue
            executable = _executable_in(build)
            if executable is not None:
                found[version] = executable
    return [(v, found[v]) for v in sorted(found, key=version_sort_key)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="introspect_nodes.py",
        description="Dump Geometry Nodes node-type identity facts as JSON.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="path of the JSON dump to write (required when dumping)",
    )
    parser.add_argument(
        "--no-props",
        dest="props",
        action="store_false",
        help="omit writable RNA properties and enum values",
    )
    launcher = parser.add_argument_group(
        "launcher mode",
        "Run this file with plain CPython to drive one or more Blender installs.",
    )
    launcher.add_argument(
        "--blender",
        action="append",
        default=[],
        metavar="PATH",
        help="a Blender executable to dump; repeatable",
    )
    launcher.add_argument(
        "--discover",
        action="store_true",
        help=f"find builds under $BLENDER_VERSIONS_ROOT (default {DEFAULT_VERSIONS_ROOT})",
    )
    launcher.add_argument(
        "--versions-root",
        default=None,
        help="override $BLENDER_VERSIONS_ROOT for --discover",
    )
    launcher.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"where discovered dumps are written as gn-<version>.json (default {DEFAULT_OUTPUT_DIR})",
    )
    launcher.add_argument(
        "--dry-run",
        action="store_true",
        help="list what would be dumped and exit",
    )
    return parser.parse_args(_script_args(argv))


def node_classes() -> list[str]:
    """Return the names of every ``bpy.types.Node`` subclass, sorted."""
    names = []
    for name in sorted(dir(bpy.types)):
        candidate = getattr(bpy.types, name)
        try:
            if isinstance(candidate, type) and issubclass(candidate, bpy.types.Node):
                names.append(name)
        except TypeError:
            continue
    return names


def read_properties(node) -> dict[str, object]:
    """Return the writable, type-level RNA properties of ``node``."""
    props: dict[str, object] = {}
    for prop in node.bl_rna.properties:
        if prop.is_readonly or prop.identifier in UI_PROPERTIES:
            continue
        if prop.identifier.startswith("bl_"):
            continue
        if prop.type == "ENUM":
            try:
                props[prop.identifier] = [item.identifier for item in prop.enum_items]
            except Exception:
                # Dynamic enums are populated from context and have no static
                # item list outside the UI.
                props[prop.identifier] = "ENUM"
        elif prop.type in ("BOOLEAN", "INT", "FLOAT", "STRING"):
            props[prop.identifier] = prop.type
    return props


def read_socket(socket) -> list[str]:
    """Return ``[name, identifier, type, rna_class]`` for one socket.

    ``socket.type`` is coarse: a 3D and a 2D vector both read ``VECTOR``. The
    RNA class name separates them (``NodeSocketVector`` vs
    ``NodeSocketVector2D``), and that distinction is a real compatibility risk
    -- feeding three components into a 2D socket silently drops one.
    """
    return [socket.name, socket.identifier, socket.type, socket.bl_rna.identifier]


def read_node(node, with_props: bool) -> dict[str, object]:
    record: dict[str, object] = {
        "label": node.bl_label,
        "desc": node.bl_rna.description,
        "in": [read_socket(s) for s in node.inputs],
        "out": [read_socket(s) for s in node.outputs],
    }
    if with_props:
        props = read_properties(node)
        if props:
            record["props"] = props
    return record


def introspect(with_props: bool = True) -> tuple[dict[str, dict], list[str]]:
    """Instantiate every node type in a throwaway tree and read it back.

    Types that cannot live in a Geometry Nodes tree raise on ``nodes.new()``
    and are reported as skipped.
    """
    tree = bpy.data.node_groups.new("__introspect_probe", TREE_TYPE)
    records: dict[str, dict] = {}
    skipped: list[str] = []
    try:
        for class_name in node_classes():
            try:
                node = tree.nodes.new(class_name)
            except Exception:
                skipped.append(class_name)
                continue
            try:
                records[class_name] = read_node(node, with_props)
            except Exception as exc:  # pragma: no cover - depends on Blender build
                skipped.append(f"{class_name} (read failed: {exc})")
            finally:
                tree.nodes.remove(node)
    finally:
        bpy.data.node_groups.remove(tree)
    return records, skipped


def read_experimental() -> dict[str, bool]:
    """Return the boolean experimental preferences and their factory defaults.

    ``nodes.new()`` succeeds for node types whose feature is still behind an
    experimental preference, so the creatable set alone reports a node as
    available when the user cannot reach it. Verified on 5.1.2: turning
    ``use_geometry_nodes_lists`` and ``use_geometry_bundle`` on leaves the
    creatable set byte-identical at 333 types. Which flag gates which node is
    not exposed through RNA -- recording the flags is what makes the gate
    visible at all.

    Read under ``--factory-startup``, so these are the defaults a user starts
    from, not one machine's saved preferences.
    """
    experimental = bpy.context.preferences.experimental
    flags: dict[str, bool] = {}
    for prop in experimental.bl_rna.properties:
        if prop.identifier == "rna_type" or prop.type != "BOOLEAN":
            continue
        flags[prop.identifier] = bool(getattr(experimental, prop.identifier))
    return flags


def build_dump(records: dict[str, dict]) -> dict[str, object]:
    return {
        "blender": bpy.app.version_string,
        "tree_type": TREE_TYPE,
        "experimental": read_experimental(),
        "nodes": records,
    }


def _run_one(executable: Path, output: str, with_props: bool) -> int:
    """Dump one install by re-invoking this file inside it."""
    command = [
        str(executable),
        "-b",
        "--factory-startup",
        "--python",
        str(Path(__file__).resolve()),
        "--",
        "--output",
        output,
    ]
    if not with_props:
        command.append("--no-props")
    return subprocess.call(command)


def _launch(args: argparse.Namespace) -> int:
    """Drive the dump across explicitly named or discovered Blender installs."""
    targets: list[tuple[str | None, Path]] = [(None, Path(p)) for p in args.blender]
    if args.discover:
        root = args.versions_root or os.environ.get(
            "BLENDER_VERSIONS_ROOT", DEFAULT_VERSIONS_ROOT
        )
        discovered = discover_blenders(root)
        if not discovered:
            print(f"no Blender builds found under {root}", file=sys.stderr)
            return 1
        targets += discovered

    if args.output is not None and len(targets) > 1:
        print("--output takes a single target; use --output-dir instead", file=sys.stderr)
        return 2

    failures = 0
    for version, executable in targets:
        if args.output is not None:
            output = args.output
        elif version is None:
            print(
                f"--blender {executable} needs --output: the version is only known "
                "from a discovered directory name",
                file=sys.stderr,
            )
            failures += 1
            continue
        else:
            output = str(Path(args.output_dir) / f"gn-{version}.json")

        print(f"{version or '?':>8}  {executable} -> {output}")
        if args.dry_run:
            continue
        if not executable.is_file():
            print(f"  not an executable: {executable}", file=sys.stderr)
            failures += 1
            continue
        if _run_one(executable, output, args.props) != 0:
            print(f"  failed: {executable}", file=sys.stderr)
            failures += 1
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv if argv is None else argv)

    if args.blender or args.discover:
        return _launch(args)

    if bpy is None:
        print(
            "no bpy in this interpreter: run this file inside Blender, against "
            "the PyPI bpy wheel, or pass --blender/--discover to launch it",
            file=sys.stderr,
        )
        return 2
    if args.output is None:
        print("--output is required when dumping", file=sys.stderr)
        return 2

    records, skipped = introspect(with_props=args.props)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(build_dump(records), handle, indent=0, sort_keys=True)
        handle.write("\n")
    print(
        f"\n[[DUMP]] version={bpy.app.version_string} "
        f"nodes={len(records)} skipped={len(skipped)} out={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
