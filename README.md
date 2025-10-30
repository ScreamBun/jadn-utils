# jadn-utils

## How to create the whl

1) From setup.py, update the version
2) Run: python setup.py bdist_wheel --universal
3) Under dist, locate: jadn_json-*-py2.py3-none-any.whl
4) Copy to the repo or project that requires this functionality
5) To add to the other project run: pip install jadn_json-*-py2.py3-none-any.whl

## Graphviz label spacing and previews

You can control the vertical spacing used where an HTML-like label would previously
use an `<hr/>`. Graphviz labels don't support CSS, so this project simulates padding
by inserting an empty table row with a fixed height.

- Per-graph: set `style['label']['spacer_height']` (preferred) or the legacy
 `style['label_spacer_height']` when creating a `GvGenerator`.

Example:

```py
g = GvGenerator(schema, style={'label': {'spacer_height': 8}})
```

Preview SVGs demonstrating different spacer heights are included in `docs/preview/`.
Files: `sample_spacer_2.svg`, `sample_spacer_6.svg`, `sample_spacer_12.svg`.

## Graphviz detail levels (labels)

The Graphviz generator supports three detail levels which control how much
information is included inside HTML-like node labels. Set the level via the
`detail` key in the `style` dict passed to `GvGenerator`.

-- `GvGenerator.INFORMATIONAL` (or `'informational'`) — full labels. Shows the
  type header, Options (if any), and full field rows (id, name, type, multiplicity, format, etc.).
-- `GvGenerator.LOGICAL` (or `'logical'`) — medium detail. Shows the type
  header and field names only. Options and field-level metadata are hidden.
-- `GvGenerator.CONCEPTUAL` (or `'conceptual'`) — minimal detail. Shows only
  the type header (no Options, no field rows).

Examples

```py
# informational (default)
g = GvGenerator(schema, style={'detail': GvGenerator.INFORMATIONAL})

# logical — show only field names
g = GvGenerator(schema, style={'detail': GvGenerator.LOGICAL})

# conceptual — show only the type header
g = GvGenerator(schema, style={'detail': GvGenerator.CONCEPTUAL})
```

## Available style keys

You can pass a `style` dict into `GvGenerator(schema, style=...)` to override
defaults for a graph. The most commonly-used keys are below (defaults are
provided by `GvGenerator.STYLE_DEFAULT`):

- `detail` (string) — one of `conceptual`, `logical`, or `informational`. Controls
  label verbosity (headers only, field names, or full field rows).
- `show_links` (bool) — whether dashed "link" edges (e.g., pointer/enumerated)
  are included in the graph.
- `show_label_name` (bool) — show or hide the main edge label (the field name).
  When false the `label` attribute is omitted from edges entirely.
- `show_headlabel` (bool) — show or hide the head multiplicity label on edges.
- `show_taillabel` (bool) — show or hide the tail multiplicity label on edges.
- `enums_allowed` (int | None) — maximum number of enumerated items to render
  inside an `Enumerated` node. `None` shows all, `0` shows none, an integer
  truncates the list and appends a "... and N more" summary row when items
  remain.
- `label_spacer_height` or `label.spacer_height` (int) — vertical spacer height
  used in place of an `<hr/>` inside HTML-like labels. Prefer the nested
  `label` block (e.g. `{'label': {'spacer_height': 8}}`) but the legacy
  `label_spacer_height` is still supported.
- `link_horizontal` (bool) — prefer left-to-right layout for edges. When true
  the generator uses LR `rankdir` and spreads edge ports around node compass
  points to improve label legibility.
- `graph_comment`, `graph_format`, `graph_engine` — low-level Graphviz
  settings passed to `graphviz.Digraph`.
- `graph_attr`, `node_attr`, `edge_attr` (dict) — maps of Graphviz attributes
  applied to the graph, nodes, and edges respectively (font, fontsize, arrowsize,
  etc.). These are merged into the Graphviz objects via `graph_attr.update(...)`.
- `per_type_attrs` (dict) — per-type visual overrides. Keys are type names
  (e.g. `Record`, `Enumerated`, `String`) and values are dicts that may contain
  `fillcolor` and `shape`. Use this to render primitive types as ellipses while
  keeping complex types as tables.

Example: change enumerated truncation and layout

```py
g = GvGenerator(schema, style={
    'enums_allowed': 5,
    'detail': GvGenerator.INFORMATIONAL,
    'link_horizontal': True,
    'per_type_attrs': {'String': {'shape': 'ellipse'}}
})
```

These settings are applied per-graph and are carried through to all label
builders so fields, options, and enumerated items are shown or hidden
consistently.
