import os
import sys
import json
import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from jadnutils.utils.conversion_utils import (
    build_type_summary_html, build_types_html, get_theme_css,
    serialize_as_compact, serialize_as_concise, convert_format_value,
    validate_json
)

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))


class TestConversionUtils:
    """Test suite for conversion utility functions."""

    @pytest.fixture
    def sample_jadn_types(self):
        """Sample JADN types for testing."""
        return [
            ["Person", "Record", [], "A person", [
                [1, "name", "String", [], "Person's name"],
                [2, "age", "Integer", [], "Person's age"],
                [3, "email", "String", [], "Optional email"]
            ]],
            ["Status", "Enumerated", [], "Status values", [
                [1, "active", "Active status"],
                [2, "inactive", "Inactive status"]
            ]],
            ["Color", "String", ["/x"], "Hexadecimal color"],
            ["Company", "ArrayOf", ["{*Person"], "Array of persons"]
        ]

    def test_build_type_summary_html_basic(self):
        """Test build_type_summary_html with basic parameters."""
        name = "TestType"
        type_val = "String"
        options = "[0..10]"
        description = "A test type"
        
        result = build_type_summary_html(name, type_val, options, description)
        
        assert f"<h4 id='{name}'>{name}</h4>" in result
        assert type_val in result
        assert options in result
        assert description in result
        assert "<table" in result

    def test_build_type_summary_html_empty_values(self):
        """Test build_type_summary_html with empty values."""
        result = build_type_summary_html("", "", "", "")
        
        assert "<h4 id=''></h4>" in result
        assert "<table" in result

    def test_build_types_html_record_type(self, sample_jadn_types):
        """Test build_types_html with Record type."""
        record_types = [sample_jadn_types[0]]  # Person type
        result = build_types_html(record_types)
        
        assert "Person" in result
        assert "Record" in result
        assert "name" in result
        assert "age" in result
        assert "email" in result
        assert "<table" in result

    def test_build_types_html_enumerated_type(self, sample_jadn_types):
        """Test build_types_html with Enumerated type."""
        enum_types = [sample_jadn_types[1]]  # Status type
        result = build_types_html(enum_types)
        
        assert "Status" in result
        assert "Enumerated" in result
        assert "active" in result
        assert "inactive" in result
        assert "<table" in result

    def test_build_types_html_primitive_type(self, sample_jadn_types):
        """Test build_types_html with primitive type."""
        primitive_types = [sample_jadn_types[2]]  # Color type
        result = build_types_html(primitive_types)
        
        assert "Color" in result
        assert "String" in result
        assert "/x" in result

    def test_build_types_html_arrayof_type(self, sample_jadn_types):
        """Test build_types_html with ArrayOf type."""
        arrayof_types = [sample_jadn_types[3]]  # Company type
        result = build_types_html(arrayof_types)
        
        assert "Company" in result
        assert "ArrayOf" in result

    def test_build_types_html_unknown_type(self):
        """Test build_types_html with unknown type format."""
        unknown_types = [["Unknown"]]  # Invalid format
        result = build_types_html(unknown_types)
        
        # Should skip unknown types and return empty string
        assert result == ""

    def test_build_types_html_type_references(self, sample_jadn_types):
        """Test build_types_html creates proper type references."""
        # Add a type that references another type
        types_with_refs = [
            ["Employee", "Record", [], "An employee", [
                [1, "name", "String", [], "Name"],
                [2, "person", "Person", [], "Person details"]
            ]],
            sample_jadn_types[0]  # Person type
        ]
        result = build_types_html(types_with_refs)
        
        assert '<a href="#Person">Person</a>' in result

    @patch("builtins.open", new_callable=mock_open, read_data="body { color: red; }")
    def test_get_theme_css_success(self, mock_file):
        """Test get_theme_css when file exists."""
        result = get_theme_css()
        assert result == "body { color: red; }"

    @patch("builtins.open", side_effect=FileNotFoundError())
    def test_get_theme_css_file_not_found(self, mock_file):
        """Test get_theme_css when file doesn't exist."""
        result = get_theme_css()
        assert result == ""

    @patch("builtins.open", side_effect=Exception("Read error"))
    def test_get_theme_css_read_error(self, mock_file):
        """Test get_theme_css when file read fails."""
        result = get_theme_css()
        assert result == ""

    def test_serialize_as_compact_dict_record(self, sample_jadn_types):
        """Test serialize_as_compact with Record type dict."""
        json_obj = {"name": "John", "age": 30, "email": "john@example.com"}
        
        # Mock get_field_by_data to return Person type
        with patch('jadnutils.utils.conversion_utils.get_field_by_data') as mock_get_field:
            with patch('jadnutils.utils.conversion_utils.get_type') as mock_get_type:
                mock_get_field.return_value = sample_jadn_types[0]
                mock_get_type.return_value = "Record"
                
                result = serialize_as_compact(sample_jadn_types, json_obj)
                assert result == ["John", 30, "john@example.com"]

    def test_serialize_as_compact_dict_non_record(self, sample_jadn_types):
        """Test serialize_as_compact with non-Record type dict."""
        json_obj = {"key": "value"}
        
        with patch('jadnutils.utils.conversion_utils.get_field_by_data') as mock_get_field:
            with patch('jadnutils.utils.conversion_utils.get_type') as mock_get_type:
                mock_get_field.return_value = None
                mock_get_type.return_value = "Map"
                
                result = serialize_as_compact(sample_jadn_types, json_obj)
                assert result == {"key": "value"}

    def test_serialize_as_compact_list(self, sample_jadn_types):
        """Test serialize_as_compact with list."""
        json_obj = [{"name": "John"}, {"name": "Jane"}]
        
        with patch('jadnutils.utils.conversion_utils.get_field_by_data') as mock_get_field:
            with patch('jadnutils.utils.conversion_utils.get_type') as mock_get_type:
                mock_get_field.return_value = sample_jadn_types[0]
                mock_get_type.return_value = "Record"
                
                result = serialize_as_compact(sample_jadn_types, json_obj)
                assert result == [["John"], ["Jane"]]

    def test_serialize_as_compact_primitive(self, sample_jadn_types):
        """Test serialize_as_compact with primitive value."""
        result = serialize_as_compact(sample_jadn_types, "simple_string")
        assert result == "simple_string"
        
        result = serialize_as_compact(sample_jadn_types, 42)
        assert result == 42

    def test_serialize_as_concise_record(self, sample_jadn_types):
        """Test serialize_as_concise with Record type."""
        json_obj = {"name": "John", "age": 30}
        
        with patch('jadnutils.utils.conversion_utils.get_field_by_data') as mock_get_field:
            with patch('jadnutils.utils.conversion_utils.get_type') as mock_get_type:
                with patch('jadnutils.utils.conversion_utils.get_children') as mock_get_children:
                    with patch('jadnutils.utils.conversion_utils.get_options') as mock_get_options:
                        mock_get_field.return_value = sample_jadn_types[0]
                        mock_get_type.return_value = "Record"
                        mock_get_children.return_value = sample_jadn_types[0][4]
                        mock_get_options.return_value = []
                        
                        result = serialize_as_concise(sample_jadn_types, json_obj)
                        assert result == ["John", 30]

    def test_serialize_as_concise_enumerated(self, sample_jadn_types):
        """Test serialize_as_concise with Enumerated type."""
        json_obj = {"active": 1}
        
        with patch('jadnutils.utils.conversion_utils.get_field_by_data') as mock_get_field:
            with patch('jadnutils.utils.conversion_utils.get_type') as mock_get_type:
                with patch('jadnutils.utils.conversion_utils.get_children') as mock_get_children:
                    with patch('jadnutils.utils.conversion_utils.get_options') as mock_get_options:
                        with patch('jadnutils.utils.conversion_utils.get_field_from_struct') as mock_get_field_struct:
                            mock_get_field.return_value = sample_jadn_types[1]
                            mock_get_type.return_value = "Enumerated"
                            mock_get_children.return_value = sample_jadn_types[1][4]
                            mock_get_options.return_value = []
                            mock_get_field_struct.return_value = [1, "active", "Active status"]
                            
                            result = serialize_as_concise(sample_jadn_types, json_obj)
                            assert result == 1

    def test_serialize_as_concise_list(self, sample_jadn_types):
        """Test serialize_as_concise with list."""
        json_obj = ["item1", "item2"]
        result = serialize_as_concise(sample_jadn_types, json_obj)
        assert result == ["item1", "item2"]

    def test_serialize_as_concise_primitive(self, sample_jadn_types):
        """Test serialize_as_concise with primitive value."""
        result = serialize_as_concise(sample_jadn_types, "simple")
        assert result == "simple"

    def test_convert_format_value_with_format(self):
        """Test convert_format_value with format conversion."""
        format_dict = {"date_field": ["/gYear"]}
        json_obj = {"date_field": "2023", "other": "value"}
        
        # This function modifies json_obj in place
        convert_format_value(format_dict, json_obj)
        
        # Should have converted the date_field if converter exists
        assert "other" in json_obj
        assert "date_field" in json_obj

    def test_convert_format_value_no_format(self):
        """Test convert_format_value with no format."""
        format_dict = {}
        json_obj = {"field": "value"}
        original = json_obj.copy()
        
        convert_format_value(format_dict, json_obj)
        assert json_obj == original

    def test_convert_format_value_invalid_input(self):
        """Test convert_format_value with invalid inputs."""
        # Should handle non-dict json_obj gracefully
        convert_format_value({"key": ["format"]}, "not_a_dict")
        
        # Should handle non-dict format_dict gracefully
        json_obj = {"field": "value"}
        original = json_obj.copy()
        convert_format_value("not_a_dict", json_obj)
        assert json_obj == original

    def test_validate_json_string_valid(self):
        """Test validate_json with valid JSON string."""
        json_string = '{"name": "John", "age": 30}'
        result = validate_json(json_string)
        assert result == {"name": "John", "age": 30}

    def test_validate_json_string_invalid(self):
        """Test validate_json with invalid JSON string."""
        invalid_json = '{"name": "John", "age":}'
        with pytest.raises(ValueError, match="Invalid JSON string"):
            validate_json(invalid_json)

    def test_validate_json_dict(self):
        """Test validate_json with dict object."""
        data = {"name": "John", "age": 30}
        result = validate_json(data)
        assert result == data

    def test_validate_json_list(self):
        """Test validate_json with list object."""
        data = [1, 2, 3]
        result = validate_json(data)
        assert result == data

    def test_validate_json_invalid_type(self):
        """Test validate_json with invalid type."""
        with pytest.raises(ValueError, match="Input is not a valid JSON string or object"):
            validate_json(42)
        
        with pytest.raises(ValueError, match="Input is not a valid JSON string or object"):
            validate_json(None)


# Additional integration-style tests using test data if available
def test_integration_with_music_lib():
    """Test functions with music library data if available."""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
        from music_lib import j_schema
        from music_lib_data import j_data
        
        # Test serialize_as_compact with real data
        compact_result = serialize_as_compact(j_schema.get("types", []), j_data)
        assert compact_result is not None
        
        # Test serialize_as_concise with real data
        concise_result = serialize_as_concise(j_schema.get("types", []), j_data)
        assert concise_result is not None
        
        # Test validate_json with music lib data
        validated = validate_json(j_data)
        assert validated == j_data
        
    except ImportError:
        # Skip if music lib data is not available
        pytest.skip("music_lib test data not available")


if __name__ == "__main__":
    pytest.main([__file__])