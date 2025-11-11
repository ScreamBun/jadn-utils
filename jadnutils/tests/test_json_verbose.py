import os
import sys
import json

from jadnutils.utils.rev_conversion_utils import compact_to_verbose, get_real_type_order
from jadnutils.utils.rev_conversion_utils import get_jadn_type_by_name
sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
from music_lib_compact_data import j_data
from music_lib import j_schema
from music_lib_data import j_data as verbose_j_data

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

def test_compact_to_verbose_4():
    jadn_schema = {
        "meta": {
            "roots": ["Person"],
            "package": "https://www.test"
        },
        "types": [
            ["Person", "Map", [], "", [
                [1, "name", "String", [], ""],
                [2, "address", "Address", [], ""],
                [3, "house_info", "House-Info", [], ""]
            ]],
            ["Address", "Record", [], "", [
                [1, "street_address", "String", [], ""],
                [2, "city", "String", [], ""],
                [3, "state", "String", [], ""],
                [4, "zip_code", "Integer", ["w00000", "x99999"], ""]
            ]],
            ["House-Info", "Map", [], "", [
                [1, "purchase_amount", "Integer", [], ""],
                [2, "date_purchased", "String", ["/date"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    expected_json = {
        "Person": {
            "name": "Test Person",
            "address": {
                "street_address": "12345",
                "city": "Columbia",
                "state": "Maryland",
                "zip_code": 11111
            },
            "house_info": {
                "purchase_amount": 100000,
                "date_purchased": "2023-01-01"
            }
        }
    }

    nested_json = {"Person": {"name": "Test Person", "address": ["12345", "Columbia", "Maryland", 11111], "house_info": {"purchase_amount": 100000, "date_purchased": "2023-01-01"}}}
    verbose_json = compact_to_verbose(ordered_types, nested_json, root_def)

    assert verbose_json == expected_json

def test_compact_to_verbose_5():
    jadn_schema = {
        "meta": {
            "roots": ["States"],
            "package": "https://www.test"
        },
        "types": [
            ["States", "Array", [], "", [
                [1, "state", "State", [], ""],
                [2, "state2", "State", [], ""]
            ]],
            ["State", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "state", "String", [], ""],
                [3, "latitude", "String", [], ""],
                [4, "longitude", "String", [], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    expected_json = [
        {
            "name": "St. Louis",
            "state": "Missouri",
            "latitude": "38.627003",
            "longitude": "-90.199402"
        },
        {
            "name": "Seattle",
            "state": "Washington",
            "latitude": "47.60621",
            "longitude": "-122.33207"
        }
    ]

    nested_json = [["St. Louis", "Missouri", "38.627003", "-90.199402"],["Seattle", "Washington", "47.60621", "-122.33207"]]

    assert compact_to_verbose(ordered_types, nested_json, root_def) == expected_json

def test_compact_music_lib_to_verbose():
    json_data = j_data
    jadn_types = j_schema.get("types", {})
    root_name = j_schema.get("meta", {}).get("roots", [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)
    verbose_output = compact_to_verbose(ordered_types, json_data, root_def)
    write_verbose_output(verbose_output, "music-library-verbose.json")
    assert verbose_output == verbose_j_data

# Sandbox generated data
def test_arrayof():
    jadn_schema = {
    "meta": {
        "roots": ["ArrayOf-Name"]
    },
    "types": [
        ["ArrayOf-Name", "ArrayOf", ["*Record-Name"], "", []],
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "String", [], ""],
            [2, "field_value_2", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    compact_json = {
    "ArrayOf-Name": [
        ["1", "2"],
        ["3", "4"]
    ]
    }

    expected_json = {
    "ArrayOf-Name": [{
        "field_value_1": "1",
        "field_value_2": "2"
        }, {
        "field_value_1": "3",
        "field_value_2": "4"
        }]
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == expected_json

def test_choice_enumerated():
    jadn_schema = {
    "meta": {
        "roots": ["Choice-Name"]
    },
    "types": [
        ["Choice-Name", "Choice", [], "", [
            [1, "field_value_1", "Enumerated-Name", [], ""],
            [2, "field_value_2", "Enumerated-Name-1", [], ""]
        ]],
        ["Enumerated-Name", "Enumerated", [], "", [
            [1, "choice_a", ""],
            [2, "choice_b", ""]
        ]],
        ["Enumerated-Name-1", "Enumerated", [], "", [
            [1, "choice_c", ""],
            [2, "choice_d", ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    compact_json = {
    "Choice-Name": {
        "field_value_1": "choice_b"
    }
    }

    expected_json = {
    "Choice-Name": {
        "field_value_1": "choice_b"
    }
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == expected_json

def test_enum_derived():
    jadn_schema = {
    "meta": {
        "roots": ["Map-Name"],
        "package": "https://www.test"
    },
    "types": [
        ["Map-Name", "Map", [], "", [
            [1, "field_value_1", "Enumerated-Name", [], ""],
            [2, "field_value_2", "Enumerated-Name-1", [], ""]
        ]],
        ["Enumerated-Name", "Enumerated", [], "", [
            [1, "selection_1", ""]
        ]],
        ["Enumerated-Name-1", "Enumerated", ["#Enumerated-Name"], "", []]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    compact_json = {
    "Map-Name": {
        "field_value_1": "selection_1",
        "field_value_2": "selection_1"
    }
    }

    expected_json = {
    "Map-Name": {
        "field_value_1": "selection_1",
        "field_value_2": "selection_1"
    }
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == expected_json