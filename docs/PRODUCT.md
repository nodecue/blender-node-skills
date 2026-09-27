# PRODUCT

Stable product core. Change rarely. Live direction belongs in `CURRENT.md`, not here.

## One-liner

NodeCue is a Geometry Nodes skill (plus a thin plugin) that lets agents build, edit, and explain Blender node graphs using exact live node and socket identities.

## For whom / when

Agents and operators who need to construct or teach Geometry Nodes graphs against a running Blender, without guessing node names, sockets, or legal property values from stale docs.

## Core experience

- Decide whether the task is build, edit, or explain, then follow the skill’s judgment loop.
- Use version routing and live introspection so the graph matches the Blender that is actually open.
- Get graphs that verify, plus teaching structure that names real nodes and sockets.

## Non-negotiables

1. Live Blender is the authority for current node, socket, property, and RNA identity and legal values.
2. Product knowledge and workflow live in the Geometry Nodes skill; the plugin only provides installation, environment, and entry points.
3. Geometry Nodes is the shipped runtime. Retired add-on and sidecar runtimes stay retired.

## Explicitly not

- A dump of local manuals, private corpora, session transcripts, or machine paths into the public repo.
- A second copy of skill workflow inside the plugin.
- A shipped Shader or Compositor skill.
- Input-reference reconstruction or automatic evaluated-output QA as shipped features.
- A product that depends on Jev, find_nodes, or any unshipped ranking experiment.

## Success looks like

A new agent can open this repository, follow the skill, talk to live Blender, and produce or explain a Geometry Nodes graph whose identities match that Blender — without needing another checkout or chat history.
