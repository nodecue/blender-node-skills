---
title: Diagnostics
description: "What to inspect next when the graph reads back correctly and the evaluated result is still wrong."
last_verified: "2026-09-02"
---

# When the graph is right and the result is not

**Read this only when** readback shows the nodes, links and values you intended, and the
evaluated result is still wrong or suspicious. If the graph itself is broken — a missing
link, an unset mode, a trunk that does not reach the output — that is a readback problem,
not this.

Each row is a pivot, not a repair: what to look at next, and the assumption that made
the result look right. Compute the correction from what you observe; none of these
carries a fixed value or a fixed fix.

| Observed signal | Inspect next | Do not assume |
|---|---|---|
| Geometry sits somewhere you did not intend — floating, sunk, offset | The evaluated bounds and origin of each source primitive, against the placement the request asks for | That a Geometry Nodes primitive is centred on its origin, or that it matches the object-mode operator of the same name |
| A per-part operation ran once, over everything | Whether the "parts" are instances, loose parts, or separate components | That loose parts or separate components are an evaluation boundary. Instances are the only one Geometry Nodes has |
| A value you typed into a socket has no effect | Whether that socket hides its value and reads the current one as its default | That a typed literal reaches a hidden-value socket. Wire it instead |
| A rotation or angle is off by a large factor | Whether the number was computed or copied out of a UI field | That the socket converts. Degrees exist only in the editor's draw layer; a field carries radians |
| A node fed one `Geometry` socket read the wrong part of a joined geometry | Which components carry the requested domain, then separate them explicitly | That join order or socket order decides which component is read |
| Something disappeared across a join | Component and element counts on both sides of the join | That every component type merges. One with no merge implementation is dropped, and nothing reports it |
| A per-element operation returned its input unchanged | Whether that domain has adjacency at all on that component type | That "unsupported" raises. It can return the input, which reads as the node running and doing nothing |
| A downstream node behaves as if a flag is false everywhere | Whether the attribute exists on that domain at all | That an absent attribute reads as "unset". Downstream it reads as false |
| An instanced result measures as unchanged | What the depsgraph reports about instances, rather than the evaluated mesh | That evaluated mesh data sees instances. It returns realized geometry only |
| A mode or data-type property is set and the sockets look wrong | Which sockets are currently enabled, not merely present | That a disabled socket is inert. On some versions the unused variants stay in the socket list under their old names |
