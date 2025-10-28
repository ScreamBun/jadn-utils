#!/usr/bin/env python3
"""
Integration test showing how to use both GvGenerator and PumlGenerator
together for the same schema, demonstrating their complementary capabilities.
"""

from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.gv.puml_generator import PumlGenerator


def create_test_schema():
    """Create a simple test schema for comparison."""
    return {
        "meta": {
            "title": "Simple Schema Comparison",
            "module": "test_comparison",
            "version": "1.0",
            "roots": ["User"]
        },
        "types": [
            ["User", "Record", [], "User information", [
                [1, "id", "String", [], "User ID"],
                [2, "name", "String", [], "User name"],
                [3, "profile", "UserProfile", [], "User profile"],
                [4, "roles", "Role-List", ["[0..*]"], "User roles"]
            ]],
            ["UserProfile", "Record", [], "User profile details", [
                [1, "bio", "String", ["[0..1]"], "User biography"],
                [2, "avatar_url", "String", ["[0..1]"], "Avatar image URL"],
                [3, "preferences", "UserPreferences", [], "User preferences"]
            ]],
            ["UserPreferences", "Map", [], "User preference settings", [
                [1, "theme", "String", [], "UI theme"],
                [2, "notifications", "Boolean", [], "Enable notifications"],
                [3, "language", "Language", [], "Preferred language"]
            ]],
            ["Role", "Choice", [], "User role types", [
                [1, "admin", "AdminRole", [], "Administrator role"],
                [2, "user", "UserRole", [], "Regular user role"],
                [3, "guest", "GuestRole", [], "Guest role"]
            ]],
            ["AdminRole", "Record", [], "Administrator permissions", [
                [1, "permissions", "String-List", [], "Admin permissions"],
                [2, "level", "Integer", [], "Admin level"]
            ]],
            ["UserRole", "Record", [], "Regular user permissions", [
                [1, "can_edit_profile", "Boolean", [], "Can edit own profile"]
            ]],
            ["GuestRole", "Record", [], "Guest permissions", [
                [1, "session_timeout", "Integer", [], "Session timeout in minutes"]
            ]],
            # Container types
            ["Role-List", "ArrayOf", ["*Role"], "List of roles"],
            ["String-List", "ArrayOf", ["*String"], "List of strings"],
            # Enumerations
            ["Language", "Enumerated", [], "Supported languages", [
                [1, "en", "English"],
                [2, "es", "Spanish"],
                [3, "fr", "French"],
                [4, "de", "German"],
                [5, "ja", "Japanese"]
            ]]
        ]
    }


def compare_generators():
    """Generate both Graphviz and PlantUML outputs for comparison."""
    schema = create_test_schema()
    
    print("Schema Comparison: Graphviz vs PlantUML")
    print("=" * 60)
    
    # Test configurations
    test_styles = [
        ('conceptual', {'detail': 'conceptual'}),
        ('logical', {'detail': 'logical'}),
        ('informational', {'detail': 'informational'}),
        ('no_links', {'detail': 'logical', 'show_links': False})
    ]
    
    for style_name, style_config in test_styles:
        print(f"\n=== {style_name.upper()} COMPARISON ===")
        
        # Generate Graphviz DOT
        gv_generator = GvGenerator(schema, style_config.copy())
        gv_source = gv_generator.generate()
        
        # Generate PlantUML
        puml_generator = PumlGenerator(schema, style_config.copy())
        puml_source = puml_generator.generate()
        
        # Save both outputs
        gv_filename = f"output/comparison_{style_name}.gv"
        puml_filename = f"output/comparison_{style_name}.puml"
        
        with open(gv_filename, 'w') as f:
            f.write(gv_source)
        
        with open(puml_filename, 'w') as f:
            f.write(puml_source)
        
        print(f"Generated: {gv_filename}")
        print(f"Generated: {puml_filename}")
        
        # Show key differences
        print("\nKey Differences:")
        print(f"  Graphviz: {len(gv_source.splitlines())} lines, uses HTML-like labels in nodes")
        print(f"  PlantUML: {len(puml_source.splitlines())} lines, uses class syntax with stereotypes")
        
        # Count specific elements
        gv_nodes = gv_source.count(' [label=')
        gv_edges = gv_source.count(' -> ')
        puml_classes = puml_source.count('class ') + puml_source.count('entity ') + puml_source.count('interface ')
        puml_relations = puml_source.count(' -- ') + puml_source.count(' --> ')
        
        print(f"  Graphviz: {gv_nodes} nodes, {gv_edges} edges")
        print(f"  PlantUML: {puml_classes} classes, {puml_relations} relationships")


def demonstrate_complementary_use():
    """Show how the two generators complement each other."""
    schema = create_test_schema()
    
    print("\n" + "=" * 60)
    print("COMPLEMENTARY USE CASES")
    print("=" * 60)
    
    # Graphviz: Technical documentation with precise layout
    gv_technical = GvGenerator(schema, {
        'detail': GvGenerator.INFORMATIONAL,
        'enums_allowed': 3,
        'link_horizontal': True,
        'label': {'spacer_height': 6}
    })
    
    # PlantUML: Architectural overview with clean styling
    puml_architectural = PumlGenerator(schema, {
        'detail': PumlGenerator.LOGICAL,
        'theme': 'blueprint',
        'class_style': 'entity',
        'relationship_style': '-->'
    })
    
    print("\nGraphviz Use Case: Technical documentation")
    print("- Precise control over node positioning and edge routing")
    print("- HTML-like labels with customizable spacing")
    print("- SVG/PNG output for embedding in documentation")
    print("- Fine-grained control over visual styling")
    
    print("\nPlantUML Use Case: Architectural diagrams")
    print("- Clean, standardized UML class diagram syntax")
    print("- Built-in themes and professional styling")
    print("- Easy integration with documentation systems")
    print("- Automatic layout with minimal configuration")
    
    # Save specialized outputs
    gv_source = gv_technical.generate()
    with open("output/technical_detailed.gv", 'w') as f:
        f.write(gv_source)
    
    puml_architectural.save("output/architectural_overview.puml")
    
    print("\nGenerated:")
    print("- output/technical_detailed.gv (for precise technical docs)")
    print("- output/architectural_overview.puml (for architectural overview)")


def feature_comparison():
    """Compare specific features between the generators."""
    print("\n" + "=" * 60)
    print("FEATURE COMPARISON")
    print("=" * 60)
    
    features = [
        ("Detail Levels", "Both support conceptual/logical/informational", "✓", "✓"),
        ("Custom Styling", "Graphviz: graph/node/edge attrs, PlantUML: themes", "✓", "✓"),
        ("Field Multiplicity", "Both show [0..1], [1..*] notation", "✓", "✓"),
        ("Relationship Control", "Both support show_links toggle", "✓", "✓"),
        ("Container Types", "Both represent ArrayOf/MapOf", "✓", "✓"),
        ("Enumeration Truncation", "Graphviz: configurable, PlantUML: all/none", "✓", "○"),
        ("HTML-like Labels", "Graphviz: native, PlantUML: not applicable", "✓", "N/A"),
        ("UML Stereotypes", "Graphviz: custom, PlantUML: built-in", "○", "✓"),
        ("Themes", "Graphviz: manual styling, PlantUML: built-in themes", "○", "✓"),
        ("Layout Control", "Graphviz: precise, PlantUML: automatic", "✓", "○"),
        ("Output Formats", "Graphviz: SVG/PNG/PDF/etc, PlantUML: via tools", "✓", "○"),
        ("Integration", "Graphviz: direct rendering, PlantUML: external tools", "✓", "○")
    ]
    
    print(f"{'Feature':<20} {'Description':<45} {'Graphviz':<10} {'PlantUML':<10}")
    print("-" * 95)
    
    for feature, description, gv_support, puml_support in features:
        print(f"{feature:<20} {description:<45} {gv_support:<10} {puml_support:<10}")
    
    print("\nLegend: ✓ = Full Support, ○ = Partial Support, N/A = Not Applicable")


if __name__ == "__main__":
    import os
    
    # Ensure output directory exists
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Run comparisons
    compare_generators()
    demonstrate_complementary_use()
    feature_comparison()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Both generators process JADN schemas using pandas DataFrames and support")
    print("similar styling options, but target different use cases:")
    print("")
    print("• Use Graphviz for: Technical documentation, precise layouts, direct rendering")
    print("• Use PlantUML for: Architectural diagrams, UML compliance, theme consistency")
    print("")
    print("Generated comparison files in output/ directory.")
    print("View Graphviz: dot -Tsvg file.gv -o file.svg")
    print("View PlantUML: Use online viewer or install PlantUML locally")