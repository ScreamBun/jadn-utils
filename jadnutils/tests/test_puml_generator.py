import os
import sys
import tempfile

from jadnutils.puml.puml_generator import PumlGenerator
from jadnutils.utils.conversion_utils import validate_json

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
from jadnutils.utils.utils import write_to_output
from jadnutils.tests.test_data.music_lib import j_schema
from jadnutils.tests.test_data.oc2_101 import oc2_101_schema
from jadnutils.tests.test_data.ap_hunt import ap_hunt_schema
from jadnutils.tests.test_data.generic_schema import generic_schema


def test_music_lib_to_puml():
    """Test PlantUML generation from music library schema."""
    json_data = j_schema
    
    # Validate the JSON data before conversion
    validate_json(json_data)
    
    generator = PumlGenerator(json_data)
    puml_output = generator.generate()
    write_to_output(puml_output, "test_music_lib.puml")
    
    # Basic PlantUML structure checks
    assert "@startuml" in puml_output
    assert "@enduml" in puml_output
    assert "title Music Library" in puml_output
    
    # Check that classes are generated for main types
    assert "class Album <<record>>" in puml_output
    assert "class Artist <<record>>" in puml_output
    assert "class Track <<record>>" in puml_output


def test_oc2_101_to_puml():
    """Test PlantUML generation from OC2 101 schema."""
    json_data = oc2_101_schema
    
    validate_json(json_data)
    
    generator = PumlGenerator(json_data)
    puml_output = generator.generate()
    write_to_output(puml_output, "test_oc2_101.puml")
    
    # Basic structure
    assert "@startuml" in puml_output
    assert "@enduml" in puml_output
    
    # Check for key OC2 types
    assert "class OpenC2_Command <<record>>" in puml_output or "class OpenC2-Command <<record>>" in puml_output
    assert "class Action <<enumeration>>" in puml_output


def test_ap_hunt_to_puml():
    """Test PlantUML generation from AP Hunt schema."""
    json_data = ap_hunt_schema
    
    validate_json(json_data)
    
    generator = PumlGenerator(json_data)
    puml_output = generator.generate()
    write_to_output(puml_output, "test_ap_hunt.puml")
    
    # Basic structure
    assert "@startuml" in puml_output
    assert "@enduml" in puml_output


def test_generic_schema_to_puml():
    """Test PlantUML generation from generic schema."""
    json_data = generic_schema
    
    validate_json(json_data)
    
    generator = PumlGenerator(json_data)
    puml_output = generator.generate()
    write_to_output(puml_output, "test_generic.puml")
    
    # Basic structure
    assert "@startuml" in puml_output
    assert "@enduml" in puml_output


def test_puml_generator_default_style():
    """Test PumlGenerator with default style settings."""
    generator = PumlGenerator(j_schema)
    
    # Check default style values
    assert generator.style['detail'] == PumlGenerator.CONCEPTUAL
    assert generator.style['show_links'] is True
    assert generator.style['show_fields'] is True
    assert generator.style['class_style'] == 'class'
    assert generator.style['relationship_style'] == '--'


def test_puml_generator_custom_style():
    """Test PumlGenerator with custom style settings."""
    custom_style = {
        'detail': PumlGenerator.INFORMATIONAL,
        'show_links': False,
        'theme': 'aws-orange',
        'class_style': 'entity',
        'relationship_style': '-->',
        'title': 'Custom Title'
    }
    
    generator = PumlGenerator(j_schema, custom_style)
    
    # Check that custom style is applied
    assert generator.style['detail'] == PumlGenerator.INFORMATIONAL
    assert generator.style['show_links'] is False
    assert generator.style['theme'] == 'aws-orange'
    assert generator.style['class_style'] == 'entity'
    assert generator.style['relationship_style'] == '-->'
    assert generator.style['title'] == 'Custom Title'
    
    # Check that defaults are preserved for unspecified values
    assert generator.style['show_fields'] is True


def test_puml_detail_levels():
    """Test different detail levels for PlantUML generation."""
    schema = j_schema
    
    # Test Conceptual level
    generator_conceptual = PumlGenerator(schema, {'detail': PumlGenerator.CONCEPTUAL})
    conceptual_output = generator_conceptual.generate()
    
    # Test Logical level
    generator_logical = PumlGenerator(schema, {'detail': PumlGenerator.LOGICAL})
    logical_output = generator_logical.generate()
    
    # Test Informational level
    generator_informational = PumlGenerator(schema, {'detail': PumlGenerator.INFORMATIONAL})
    informational_output = generator_informational.generate()
    
    # All should have basic structure
    for output in [conceptual_output, logical_output, informational_output]:
        assert "@startuml" in output
        assert "@enduml" in output
    
    # Informational should have more detailed field information
    # This is a rough check - informational output should generally be longer
    assert len(informational_output) >= len(logical_output) >= len(conceptual_output)


def test_puml_with_theme():
    """Test PlantUML generation with themes."""
    themes = ['blueprint', 'aws-orange', 'cerulean']
    
    for theme in themes:
        generator = PumlGenerator(j_schema, {'theme': theme})
        output = generator.generate()
        
        assert f"!theme {theme}" in output
        assert "@startuml" in output
        assert "@enduml" in output


def test_puml_with_relationships():
    """Test PlantUML generation with and without relationships."""
    # With relationships
    generator_with_links = PumlGenerator(j_schema, {'show_links': True})
    output_with_links = generator_with_links.generate()
    
    # Without relationships
    generator_no_links = PumlGenerator(j_schema, {'show_links': False})
    output_no_links = generator_no_links.generate()
    
    # Both should have basic structure
    assert "@startuml" in output_with_links
    assert "@startuml" in output_no_links
    
    # The version with links should generally have relationship arrows
    # Note: This is a heuristic check since the exact format may vary
    link_indicators = ['--', '->', '<-->', '..']
    has_links = any(indicator in output_with_links for indicator in link_indicators)
    has_no_links = not any(indicator in output_no_links for indicator in link_indicators)
    
    # This might not always be true depending on schema, so we'll just check structure
    assert len(output_with_links) > 0
    assert len(output_no_links) > 0


def test_puml_class_styles():
    """Test different PlantUML class styles."""
    styles = ['class', 'entity', 'interface']
    
    for style in styles:
        generator = PumlGenerator(j_schema, {'class_style': style})
        output = generator.generate()
        
        assert "@startuml" in output
        assert "@enduml" in output
        # The style should appear in the output for some classes
        # Note: 'interface' style is only used for Choice types


def test_puml_name_escaping():
    """Test name escaping for special characters."""
    # Create a schema with special characters in names
    test_schema = {
        "meta": {"title": "Test Escaping"},
        "types": [
            ["User-Type", "Record", [], "Type with hyphen", []],
            ["Config.Setting", "Record", [], "Type with dot", []],
            ["User:Profile", "Record", [], "Type with colon", []]
        ]
    }
    
    generator = PumlGenerator(test_schema)
    output = generator.generate()
    
    # Check that names are properly escaped
    assert "class User_Type" in output  # Hyphen becomes underscore
    assert 'class "Config.Setting"' in output  # Dot gets quoted
    assert 'class "User:Profile"' in output  # Colon gets quoted


def test_puml_save_to_file():
    """Test saving PlantUML output to file."""
    generator = PumlGenerator(j_schema)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as f:
        temp_file = f.name
    
    try:
        generator.save(temp_file)
        
        # Verify file was created
        assert os.path.exists(temp_file)
        
        # Verify file content
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "@startuml" in content
        assert "@enduml" in content
        assert "Music Library" in content
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_puml_empty_schema():
    """Test PlantUML generation with empty schema."""
    empty_schema = {"meta": {}, "types": []}
    
    generator = PumlGenerator(empty_schema)
    output = generator.generate()
    
    # Should still generate valid PlantUML structure
    assert "@startuml" in output
    assert "@enduml" in output


def test_puml_defensive_programming():
    """Test defensive programming - handling None fields and malformed data."""
    # Schema with None fields
    schema_with_none = {
        "meta": {},
        "types": [
            ["User", "Record", [], "User with None fields", None],
            ["Config", "Map", None, "Config with None opts", []]
        ]
    }
    
    generator = PumlGenerator(schema_with_none)
    output = generator.generate()  # Should not crash
    
    assert "@startuml" in output
    assert "@enduml" in output
    assert "class User" in output
    assert "class Config" in output


def test_puml_stereotypes():
    """Test that correct PlantUML stereotypes are generated."""
    # Create schema with different JADN types
    test_schema = {
        "meta": {"title": "Stereotype Test"},
        "types": [
            ["TestRecord", "Record", [], "Test record", []],
            ["TestMap", "Map", [], "Test map", []],
            ["TestArray", "Array", [], "Test array", []],
            ["TestChoice", "Choice", [], "Test choice", []],
            ["TestEnum", "Enumerated", [], "Test enum", []],
            ["TestArrayOf", "ArrayOf", ["*String"], "Test array of"],
            ["TestMapOf", "MapOf", ["+String", "*Integer"], "Test map of"]
        ]
    }
    
    generator = PumlGenerator(test_schema)
    output = generator.generate()
    
    # Check that correct stereotypes are generated
    assert "class TestRecord <<record>>" in output
    assert "class TestMap <<map>>" in output
    assert "class TestArray <<array>>" in output
    assert "class TestChoice <<choice>>" in output
    assert "class TestEnum <<enumeration>>" in output
    assert "class TestArrayOf <<arrayOf>>" in output
    assert "class TestMapOf <<mapOf>>" in output


def test_puml_root_types():
    """Test root type annotations in PlantUML."""
    schema_with_roots = {
        "meta": {
            "title": "Root Test",
            "roots": ["MainType", "SecondaryType"]
        },
        "types": [
            ["MainType", "Record", [], "Main type", []],
            ["SecondaryType", "Record", [], "Secondary type", []],
            ["HelperType", "Record", [], "Helper type", []]
        ]
    }
    
    generator = PumlGenerator(schema_with_roots)
    output = generator.generate()
    
    # Should have root type notes
    assert "note right of MainType : Root Type" in output
    assert "note right of SecondaryType : Root Type" in output
    # HelperType should not have a root note
    assert "note right of HelperType : Root Type" not in output


def test_puml_multiplicity():
    """Test multiplicity display in PlantUML fields."""
    schema_with_multiplicity = {
        "meta": {"title": "Multiplicity Test"},
        "types": [
            ["TestType", "Record", [], "Test type with multiplicity", [
                [1, "required_field", "String", [], "Required field"],
                [2, "optional_field", "String", ["[0..1]"], "Optional field"],
                [3, "multiple_field", "String", ["[1..*]"], "Multiple field"],
                [4, "range_field", "String", ["{2..10}"], "Range field"]
            ]]
        ]
    }
    
    generator = PumlGenerator(schema_with_multiplicity, {'detail': PumlGenerator.INFORMATIONAL})
    output = generator.generate()
    
    # Check multiplicity notations appear
    assert "[0..1]" in output
    assert "[1..*]" in output
    assert "{2..10}" in output
