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
