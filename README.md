# jadn-validation

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

These settings are applied per-graph and are carried through to all label
builders so fields, options, and enumerated items are shown or hidden
consistently.

