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

## PlantUML Generator

The `PumlGenerator` class creates PlantUML class diagrams from JADN schemas, using pandas DataFrames for data processing. It follows similar patterns to `GvGenerator` but outputs PlantUML syntax instead of Graphviz DOT format.

### Basic Usage

```py
from jadnutils.puml.puml_generator import PumlGenerator

# Load your JADN schema
schema = {...}

# Generate PlantUML with default settings
generator = PumlGenerator(schema)
puml_source = generator.generate()

# Save to file
generator.save("output/schema.puml")
```

### PNG and Image Output

The PlantUML generator supports multiple output formats including PNG, SVG, and other image formats:

```py
# Generate PNG image (uses web service fallback)
png_data = generator.generate(output_format='png')
with open('schema.png', 'wb') as f:
    f.write(png_data)

# Generate SVG image
svg_data = generator.generate(output_format='svg')
with open('schema.svg', 'wb') as f:
    f.write(svg_data)

# Auto-detect format from file extension
generator.save('schema.png')  # Automatically generates PNG
generator.save('schema.svg')  # Automatically generates SVG
generator.save('schema.puml') # Saves PlantUML source

# Generate URL for online viewing
url = generator.generate_url(output_format='png')
print(f"View online: {url}")
```

**Supported formats:**
- `'raw'` (default) — PlantUML source code
- `'png'` — PNG image format
- `'svg'` — SVG vector format  
- `'pdf'` — PDF format (requires local PlantUML)
- `'eps'` — EPS format (requires local PlantUML)
- `'txt'` — ASCII art format

**Rendering methods:**
1. **Web service** (automatic fallback) — Uses PlantUML.com for PNG, SVG, TXT formats
2. **Local PlantUML** — Requires PlantUML installation for all formats including PDF, EPS

### PlantUML Detail Levels

The PlantUML generator supports three detail levels similar to the Graphviz generator:

- `PumlGenerator.CONCEPTUAL` (or `'conceptual'`) — shows only class names with stereotypes, no field details
- `PumlGenerator.LOGICAL` (or `'logical'`) — shows class names and field names only
- `PumlGenerator.INFORMATIONAL` (or `'informational'`) — shows full field details with IDs, types, and multiplicity

### PlantUML Style Options

You can customize PlantUML generation with these style options (defaults in `PumlGenerator.STYLE_DEFAULT`):

- `detail` (string) — detail level: `conceptual`, `logical`, or `informational`
- `show_links` (bool) — whether to include relationships between classes
- `show_fields` (bool) — whether to show field details inside classes
- `show_multiplicity` (bool) — whether to show multiplicity info (e.g., `[0..1]`, `[1..*]`)
- `class_style` (string) — PlantUML class type: `class`, `entity`, or `interface`
- `relationship_style` (string) — relationship arrow style: `--`, `-->`, `<-->`, etc.
- `show_primitive_types` (bool) — whether to include relationships to primitive types
- `group_by_package` (bool) — whether to group related types in packages
- `theme` (string) — PlantUML theme name (default: `aws-orange`)
- `title` (string) — diagram title (uses schema meta title if not specified)
- `note_position` (string) — position for root type notes: `left`, `right`, `top`, `bottom`

### Available Themes

The PlantUML generator includes 31 built-in themes. You can get the complete list and theme information programmatically:

```py
# Get all available themes
themes = PumlGenerator.get_available_themes()
print(f"Available themes: {themes}")

# Get information about a specific theme
info = PumlGenerator.get_theme_info('aws-orange')
print(f"Theme: {info['name']} ({info['category']})")
print(f"Description: {info['description']}")
```

**Theme Categories:**
- **Professional**: `aws-orange` (default), `carbon-gray`, `cloudscape-design`, `reddress-lightblue`
- **Bootstrap**: `cerulean`, `cyborg`, `materia`, `minty`, `sandstone`, `sketchy`, `spacelab`, `united`
- **Dark**: `black-knight`, `hacker`, `reddress-darkblue`, `superhero`
- **Colorful**: `mars`, `sunlust`, `toy`, `vibrant`
- **Minimalist**: `bluegray`, `lightgray`, `metal`, `mono`, `plain`, `silver`
- **Retro**: `amiga`, `blueprint`, `crt-amber`, `mimeograph`

**Theme Examples:**
```py
# Professional AWS theme (default)
generator = PumlGenerator(schema, {'theme': 'aws-orange'})

# Dark theme for presentations
generator = PumlGenerator(schema, {'theme': 'superhero'})

# Classic blueprint style
generator = PumlGenerator(schema, {'theme': 'blueprint'})

# Vibrant colors
generator = PumlGenerator(schema, {'theme': 'vibrant'})
```

### Example Configurations

```py
# Conceptual diagram with theme
conceptual_style = {
    'detail': PumlGenerator.CONCEPTUAL,
    'show_links': True,
    'theme': 'blueprint',
    'title': 'System Overview'
}

# Detailed diagram with full information
detailed_style = {
    'detail': PumlGenerator.INFORMATIONAL,
    'show_multiplicity': True,
    'relationship_style': '-->',
    'class_style': 'entity'
}

# Types-only diagram without relationships
types_only_style = {
    'detail': PumlGenerator.LOGICAL,
    'show_links': False,
    'class_style': 'interface',
    'theme': 'cerulean'
}

generator = PumlGenerator(schema, detailed_style)
```

### Type Representations

The PlantUML generator represents JADN types as follows:

- **Record** → `class` with `<<record>>` stereotype, fields shown as attributes
- **Map** → `class` with `<<map>>` stereotype
- **Array** → `class` with `<<array>>` stereotype
- **Choice** → `class` or `interface` with `<<choice>>` stereotype, options shown as attributes
- **Enumerated** → `class` with `<<enumeration>>` stereotype, values shown as attributes
- **ArrayOf** → `class` with `<<arrayOf>>` stereotype and container info
- **MapOf** → `class` with `<<mapOf>>` stereotype and key/value type info

### Relationships

When `show_links` is enabled, the generator creates relationships for:

- Field references between types
- ArrayOf container-to-element relationships
- MapOf container-to-key/value relationships
- Choice option relationships

### Output and Viewing

Generated PlantUML can be viewed and rendered in multiple ways:

#### Direct Image Generation
```py
# Generate PNG directly (no PlantUML installation required)
png_data = generator.generate(output_format='png')
with open('diagram.png', 'wb') as f:
    f.write(png_data)

# Generate online viewing URL
url = generator.generate_url(output_format='png')
# Opens diagram in web browser at plantuml.com
```

#### Traditional PlantUML Viewing
1. **Online PlantUML Server**: [http://www.plantuml.com/plantuml/uml/](http://www.plantuml.com/plantuml/uml/)
2. **VS Code PlantUML Extension**: Install the PlantUML extension for inline preview
3. **Local PlantUML**: Install PlantUML locally and generate images with `java -jar plantuml.jar *.puml`
4. **PlantUML Web Server**: Run your own PlantUML server instance

The new PNG generation provides immediate image output without requiring local PlantUML installation.

### Complete Example

```py
from jadnutils.puml.puml_generator import PumlGenerator

schema = {
    "meta": {"title": "User Management", "roots": ["User"]},
    "types": [
        ["User", "Record", [], "User information", [
            [1, "id", "String", [], "User ID"],
            [2, "name", "String", [], "User name"],
            [3, "status", "UserStatus", [], "User status"]
        ]],
        ["UserStatus", "Enumerated", [], "User status values", [
            [1, "active", "Active user"],
            [2, "inactive", "Inactive user"]
        ]]
    ]
}

# Generate different views
styles = {
    'overview': {'detail': 'conceptual', 'theme': 'blueprint'},
    'detailed': {'detail': 'informational', 'show_multiplicity': True},
    'types_only': {'show_links': False, 'class_style': 'entity'}
}

```py
for name, style in styles.items():
    generator = PumlGenerator(schema, style)
    generator.save(f"output/user_management_{name}.puml")
```
```

````
