import os
import sys
import json

from jadnutils.utils.rev_conversion_utils import compact_to_verbose, get_real_type_order
from jadnutils.utils.rev_conversion_utils import get_jadn_type_by_name
sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
from music_lib_compact_data import j_data
from music_lib import j_schema

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))

def write_verbose_output(verbose_output, filename):
    """
    Write compact JSON output to a file in the output directory and print it.
    """
    output_dir = "output"
    output_path = os.path.join(output_dir, filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(verbose_output))
    print(verbose_output)

def test_get_real_type_order():
    jadn_schema = {
        "meta": {"roots": ["TypeB"]},
        "types": [
            ["TypeA", "Record", [], "", [
                [1, "field1", "TypeC", [], ""]
            ]],
            ["TypeB", "Record", [], "", [
                [1, "subfield1", "TypeA", [], ""],
            ]],
            ["TypeC", "Map", [], "", [
                [1, "mapfield1", "String", [], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    
    expected_order = [
        ["TypeB", "Record", [], "", [
            [1, "subfield1", "TypeA", [], ""],
        ]],
        ["TypeA", "Record", [], "", [
            [1, "field1", "TypeC", [], ""]
        ]],
        ["TypeC", "Map", [], "", [
            [1, "mapfield1", "String", [], ""]
        ]]
    ]
    assert get_real_type_order(jadn_types, [], root_def) == expected_order

def test_compact_to_verbose():
    jadn_schema = {
        "meta": {"roots": ["Record-Name"]},
        "types": [
            ["Record-Name", "Record", [], "", [
                [1, "string_field", "String", [], ""],
                [2, "int_field", "Integer", [], ""],
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)
    
    nested_json = ["test", 1]

    expected_json = {
        "string_field": "test",
        "int_field": 1
    }

    assert compact_to_verbose(ordered_types, nested_json, root_def) == expected_json

def test_compact_to_verbose_complex():
    jadn_schema = {
        "meta": {"roots": ["Map-Name"]},
        "types": [
            ["Map-Name", "Map", [], "", [
                [1, "key_field", "String", [], ""],
                [2, "value_field", "Record-Name", [], ""],
            ]],
            ["Record-Name", "Record", [], "", [
                [1, "inner_string", "String", [], ""],
                [2, "inner_int", "Integer", [], ""],
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    nested_json = {
        "key_field": "test",
        "value_field": ["inner1", 10]
    }

    expected_json = {
        "key_field": "test",
        "value_field": {
            "inner_string": "inner1",
            "inner_int": 10
        }
    }

    assert compact_to_verbose(ordered_types, nested_json, root_def) == expected_json

def test_compact_to_verbose_dupe_children():
    jadn_schema = {
        "meta": {"roots": ["Map-Name"]},
        "types": [
            ["Map-Name", "Map", [], "", [
                [1, "key_field", "String", [], ""],
                [2, "value_field", "Record-Name", [], ""],
                [3, "value_field_2", "Record-Name-2", [], ""],
            ]],
            ["Record-Name-2", "Record", [], "", [
                [1, "inner_string_2", "String", [], ""],
                [2, "inner_int_2", "Integer", [], ""],
            ]],
            ["Record-Name", "Record", [], "", [
                [1, "inner_string", "String", [], ""],
                [2, "inner_int", "Integer", [], ""],
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    nested_json = {
        "key_field": "test",
        "value_field": ["inner1", 10],
        "value_field_2": ["inner2", 20]
    }

    expected_json = {
        "key_field": "test",
        "value_field": {
            "inner_string": "inner1",
            "inner_int": 10
        },
        "value_field_2": {
            "inner_string_2": "inner2",
            "inner_int_2": 20
        }
    }

    assert compact_to_verbose(ordered_types, nested_json, root_def) == expected_json

def test_compact_to_verbose_reverse():
    jadn_schema = {
        "types": [
            ["Record-Name", "Record", [], "", [
                [1, "string_field", "String", [], ""],
                [2, "int_field", "Integer", [], ""],
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [1, "test"]

    expected_json = {
        "string_field": "test",
        "int_field": 1
    }

    assert compact_to_verbose(jadn_types, nested_json) == expected_json

def test_compact_to_verbose_convert():
    json_data = j_data
    verbose_output = compact_to_verbose(j_schema.get("types", {}), json_data)
    write_verbose_output(verbose_output, "music-library-verbose.json")
    assert verbose_output