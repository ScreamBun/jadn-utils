# PlantUML Generator for JADN Schemas

## Overview

The `PumlGenerator` class provides PlantUML diagram generation from JADN schemas using pandas DataFrames, following the same patterns established by `GvGenerator`. This creates a complementary visualization option that targets different use cases.

## Key Features

✅ **Complete Implementation**
- ✅ Pandas DataFrame processing (same as GvGenerator)
- ✅ Three detail levels (conceptual, logical, informational)
- ✅ Style configuration system with defaults
- ✅ HTML escaping and defensive programming
- ✅ Comprehensive test coverage (22 tests passing)
- ✅ Support for all JADN types (Record, Map, Array, Choice, Enumerated, ArrayOf, MapOf)
- ✅ Relationship generation with show_links control
- ✅ PlantUML themes and stereotypes
- ✅ Root type annotations
- ✅ Multiplicity display
- ✅ Container type information

## Architecture

```
PumlGenerator
├── __init__(schema, style)           # Initialize with schema and style options
├── generate() -> str                 # Generate PlantUML source code
├── save(filename)                    # Save to .puml file
├── _escape_name()                    # Handle special characters in names
├── _get_class_stereotype()           # Get UML stereotypes for types
├── _build_class_declaration()        # Create class/entity/interface declarations
├── _build_field_list()               # Build field attributes for classes
├── _build_enumerated_items()         # Build enumeration values
├── _build_relationships()            # Create relationships between classes
└── _get_container_info()             # Extract ArrayOf/MapOf container details
```

## Style Configuration

The generator supports comprehensive styling through `STYLE_DEFAULT`:

```python
STYLE_DEFAULT = {
    'detail': 'conceptual',           # conceptual|logical|informational  
    'show_links': True,               # Include relationships
    'show_fields': True,              # Show field details
    'show_multiplicity': True,        # Show [0..1], [1..*] notation
    'class_style': 'class',           # class|entity|interface
    'relationship_style': '--',       # Arrow style for relationships
    'show_primitive_types': False,    # Include primitive type relationships
    'group_by_package': True,         # Future: package grouping
    'theme': None,                    # PlantUML theme name
    'title': None,                    # Diagram title
    'note_position': 'right'          # Root type note position
}
```

## Type Representations

| JADN Type | PlantUML Representation | Stereotype |
|-----------|------------------------|------------|
| Record | `class Name <<record>>` | `<<record>>` |
| Map | `class Name <<map>>` | `<<map>>` |
| Array | `class Name <<array>>` | `<<array>>` |
| Choice | `class/interface Name <<choice>>` | `<<choice>>` |
| Enumerated | `class Name <<enumeration>>` | `<<enumeration>>` |
| ArrayOf | `class Name <<arrayOf>>` | `<<arrayOf>>` |
| MapOf | `class Name <<mapOf>>` | `<<mapOf>>` |

## Testing

Comprehensive test suite with 22 test cases covering:

- ✅ Initialization and style handling
- ✅ Name escaping for special characters  
- ✅ Class declaration building
- ✅ Field list generation at all detail levels
- ✅ Enumeration item handling
- ✅ Container type information extraction
- ✅ Relationship generation
- ✅ Theme and root type handling
- ✅ File saving functionality
- ✅ Edge cases and defensive programming
- ✅ None field handling (defensive programming)

## Examples Generated

1. **E-commerce system examples** (`examples/puml_examples.py`)
   - Conceptual, logical, detailed, and no-links variants
   - Demonstrates themes, styling, and different use cases

2. **Generator comparison** (`examples/generator_comparison.py`)  
   - Side-by-side comparison with GvGenerator
   - Feature analysis and complementary use cases
   - Generated comparison files for same schema

## Integration with Existing Codebase

The PlantUML generator follows established patterns:
- Same pandas DataFrame processing approach
- Compatible style configuration system  
- Similar defensive programming patterns (`.get()`, `or []`)
- Consistent detail level concepts
- Parallel file structure in `jadnutils/gv/`

## Usage Examples

```python
from jadnutils.gv.puml_generator import PumlGenerator

# Basic usage
generator = PumlGenerator(schema)
puml_source = generator.generate()

# With custom styling
style = {
    'detail': PumlGenerator.INFORMATIONAL,
    'theme': 'blueprint',
    'class_style': 'entity',
    'show_multiplicity': True
}
generator = PumlGenerator(schema, style)
generator.save('output/schema.puml')
```

## Output and Viewing

Generated PlantUML can be viewed via:
1. Online PlantUML server (immediate preview)
2. VS Code PlantUML extension (local editing)
3. Local PlantUML installation (batch processing)
4. Documentation systems (GitLab, GitHub, etc.)

## Complementary to Graphviz

| Use Case | Graphviz | PlantUML |
|----------|----------|----------|
| Technical documentation | ✅ Precise control | ○ Standard UML |
| Architectural diagrams | ○ Manual styling | ✅ Built-in themes |
| Direct rendering | ✅ Native support | ○ External tools |
| UML compliance | ○ Custom approach | ✅ Standard syntax |
| Layout control | ✅ Fine-grained | ○ Automatic |
| Integration | ✅ SVG/PNG direct | ✅ Doc systems |

## Files Added

```
jadnutils/gv/puml_generator.py          # Main generator class
jadnutils/gv/tests/test_puml_generator.py  # Comprehensive tests  
examples/puml_examples.py               # Usage examples
examples/generator_comparison.py        # Comparison with Graphviz
output/ecommerce_*.puml                 # Generated examples
output/comparison_*.puml                # Comparison outputs
```

## Documentation

- ✅ Comprehensive README section added
- ✅ Usage examples and style guide
- ✅ Feature comparison with GvGenerator
- ✅ Integration instructions
- ✅ Viewing and output options

## Summary

The PlantUML generator successfully extends the JADN utilities with a complementary visualization option that:

1. **Maintains consistency** with existing patterns and architecture
2. **Provides UML-compliant** class diagram generation  
3. **Supports comprehensive styling** through familiar configuration
4. **Handles all JADN types** with appropriate PlantUML representations
5. **Includes robust testing** with 100% test pass rate
6. **Offers practical examples** showing real-world usage
7. **Integrates seamlessly** with existing codebase patterns

The implementation delivers a production-ready PlantUML generation capability that complements the existing Graphviz generator while targeting different visualization needs and workflows.