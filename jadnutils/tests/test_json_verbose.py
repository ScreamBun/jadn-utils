import os
import sys
import json

from jadnutils.utils.rev_conversion_utils import compact_to_verbose, get_real_type_order
from jadnutils.utils.rev_conversion_utils import get_jadn_type_by_name
from jadnutils.json.convert_verbose import convert_to_verbose
sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))

from music_lib_compact_data import j_data
from music_lib import j_schema
from music_lib_data import j_data as verbose_j_data

from schema_classes import j_schema as schema_classes_schema
from schema_classes_data import j_data as schema_classes_data
from schema_classes_compact_data import j_data as schema_classes_compact_j_data

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))

def test_convert_verbose():
    jadn_schema = j_schema
    json_obj = j_data
    convert_from = 'compact'
    root = 'Library'

    verbose_output = convert_to_verbose(jadn_schema, json_obj, convert_from, root)
    assert verbose_output == verbose_j_data

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

def test_mapof_list():
    jadn_schema =  {
    "meta": {
        "roots": ["MapOf-Name"]
    },
    "types": [
        ["MapOf-Name", "MapOf", ["+Integer", "*Record-Name", "q"], "", []],
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

    verbose_json = {
    "MapOf-Name": [1, {
        "field_value_1": "a",
        "field_value_2": "b"
        }, 2, {
        "field_value_1": "c",
        "field_value_2": "d"
        }, 3, {
        "field_value_1": "e",
        "field_value_2": "f"
        }]
    }

    compact_json = {"MapOf-Name": [1, ["a", "b"], 2, ["c", "d"], 3, ["e", "f"]]}

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_mapof_dict():
    jadn_schema = {
    "meta": {
        "roots": ["MapOf-Name"]
    },
    "types": [
        ["MapOf-Name", "MapOf", ["*Record-Name", "+String", "q"], "", []],
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

    verbose_json = {
    "MapOf-Name": {
        "a": {
        "field_value_1": "1",
        "field_value_2": "2"
        },
        "b": {
        "field_value_1": "3",
        "field_value_2": "4"
        },
        "c": {
        "field_value_1": "5",
        "field_value_2": "6"
        }
    }
    }

    compact_json = {
    "MapOf-Name": {
        "a": ["1", "2"],
        "b": ["3", "4"],
        "c": ["5", "6"]
    }
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_mapof_within_list():
    jadn_schema = {
    "meta": {
        "roots": ["Array-Name"]
    },
    "types": [
        ["MapOf-Name", "MapOf", ["*Record-Name", "+String", "q"], "", []],
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "String", [], ""],
            [2, "field_value_2", "String", [], ""]
        ]],
        ["Array-Name", "Array", [], "", [
            [1, "field_value_1", "MapOf-Name", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Array-Name": [{
        "a": {
            "field_value_1": "1",
            "field_value_2": "2"
        },
        "b": {
            "field_value_1": "3",
            "field_value_2": "4"
        }
        }]
    }

    compact_json = {
    "Array-Name": [{
        "a": ["1", "2"],
        "b": ["3", "4"]
        }]
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

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

def test_choice_combine():
    jadn_schema = {
    "meta": {
        "title": "JADN Schema Start Up Template",
        "package": "http://JADN-Schema-Start-Up-Template-URI",
        "roots": ["Choices", "Choice-Regular", "Choice-Combine", "Choice-Combine-Complex"]
    },
    "types": [
        ["Choices", "Record", [], "", [
            [1, "choice_combine", "Choice-Combine", [], ""],
            [2, "choice_regular", "Choice-Regular", [], ""],
            [3, "choice_combine_complex", "Choice-Combine-Complex", [], ""]
        ]],
        ["Choice-Combine", "Choice", ["CO"], "", [
            [1, "string_choice", "String", ["N"], ""],
            [2, "integer_choice", "Integer", [], ""]
        ]],
        ["Choice-Regular", "Choice", [], "", [
            [1, "string_choice_2", "String", [], ""],
            [2, "integer_choice_2", "String", [], ""]
        ]],
        ["Choice-Combine-Complex", "Choice", ["CO"], "", [
            [1, "field_value_1", "Basic-Record", [], ""],
            [2, "field_value_2", "String", ["N"], ""]
        ]],
        ["Basic-Record", "Record", [], "", [
            [1, "field_value_1", "String", [], ""],
            [2, "field_value_2", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0] # Choices
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Choices": {
        "choice_combine": "string_a",
        "choice_regular": {
        "string_choice_2": "string_b"
        },
        "choice_combine_complex": {
        "field_value_1": "c",
        "field_value_2": "d"
        }
    }
    }

    compact_json = {
    "Choices": ["string_a", {
        "string_choice_2": "string_b"
        }, {
        "field_value_1": "c",
        "field_value_2": "d"
        }]
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

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

def test_multiplicities():
    jadn_schema = {
    "meta": {
        "package": "https://www.test.com",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "strict_range", "String", ["[1", "]3"], ""],
            [2, "negative_one", "String", ["]-1"], ""],
            [3, "negative_two", "String", ["]-2"], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Record-Name": {
        "strict_range": ["a", "b"],
        "negative_one": ["c", "d"],
        "negative_two": ["e", "f"]
    }
    }

    compact_json = {
    "Record-Name": [
        ["a", "b"],
        ["c", "d"],
        ["e", "f"]
    ]
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_inheritance_extends():
    jadn_schema = {
    "meta": {
        "roots": ["Child-Name"]
    },
    "types": [
        ["Parent-Name", "Record", [], "", [
            [1, "parent_field", "String", [], ""]
        ]],
        ["Child-Name", "Record", ["eParent-Name"], "", [
            [2, "child_field", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    compact_json = {
    "Child-Name": ["parent_value", "child_value"]
    }

    expected_json = {
    "Child-Name": {
        "parent_field": "parent_value",
        "child_field": "child_value"
    }
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == expected_json

def test_inheritance_restricts():
    jadn_schema = {
    "meta": {
        "roots": ["Child-Name"]
    },
    "types": [
        ["Parent-Name", "Record", [], "", [
            [1, "parent_field", "String", [], ""],
            [2, "common_field", "String", [], ""]
        ]],
        ["Child-Name", "Record", ["rParent-Name"], "", [
            [1, "common_field", "String", [], ""],
            [2, "child_field", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    compact_json = {
    "Child-Name": ["common_value", "child_value"]
    }

    expected_json = {
    "Child-Name": {
        "common_field": "common_value",
        "child_field": "child_value"
    }
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == expected_json

def test_inheritance_complex():
    jadn_schema = {
    "meta": {
        "package": "https://www.test.com",
        "roots": ["Abstract-Object", "Extend-1", "Restrict-1", "Extend-2", "Extend-3", "Restrict-2", "Extend-4"]
    },
    "types": [
        ["Abstract-Object", "Record", ["a"], "This is an abstract record.", [
            [1, "abstract_1", "String", ["[0"], ""],
            [2, "abstract_2", "String", ["[0"], ""],
            [3, "abstract_3", "String", ["[0"], ""],
            [4, "abstract_4", "String", ["[0"], ""]
        ]],
        ["Extend-1", "Record", ["eAbstract-Object"], "Should contain abstract_1 through abstract_4 and extend_1", [
            [5, "extend_1", "String", ["[0"], ""]
        ]],
        ["Restrict-1", "Record", ["rAbstract-Object"], "Should contain abstract_1 through abstract_4", []],
        ["Extend-2", "Record", ["eExtend-1"], "Should contain abstract_1 through abstract_4 and extend_1, extend_2", [
            [6, "extend_2", "String", ["[0"], ""]
        ]],
        ["Extend-3", "Record", ["eRestrict-1"], "Should contain abstract_1 through abstract_4 and extend_4, extend_5", [
            [7, "extend_4", "String", [], ""],
            [8, "extend_5", "String", [], ""]
        ]],
        ["Restrict-2", "Record", ["rExtend-3"], "Should contain abstract_1 through abstract_4 and extend_4, extend_5", []],
        ["Extend-4", "Record", ["eRestrict-2"], "Should contain abstract_1 through abstract_4 and extend_4 through extend_7", [
            [9, "extend_6", "String", ["[0"], ""],
            [10, "extend_7", "String", ["[0"], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_names = jadn_schema.get('meta', {}).get('roots', [None])[6] # Extend-4
    root_def = get_jadn_type_by_name(jadn_types, root_names)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Extend-4": {
        "abstract_1": "a",
        "abstract_2": "b",
        "abstract_3": "c",
        "abstract_4": "d",
        "extend_4": "e",
        "extend_5": "f",
        "extend_6": "g",
        "extend_7": "h"
    }
    }

    compact_json = {"Extend-4": ["a", "b", "c", "d", "e", "f", "g", "h"]}

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_key_link():
    jadn_schema = {
    "meta": {
        "title": "JADN Schema Start Up Template",
        "package": "http://JADN-Schema-Start-Up-Template-URI",
        "roots": ["Person", "Organization"]
    },
    "types": [
        ["Person", "Record", [], "", [
            [1, "id", "Integer", ["K"], ""],
            [2, "name", "String"],
            [3, "mother", "Person", ["L"]],
            [4, "father", "Person", ["L"]],
            [5, "siblings", "Person", ["L", "[0", "]-2"]],
            [6, "employer", "Organization", ["L", "[0"], ""]
        ]],
        ["Organization", "Record", [], "", [
            [1, "name", "String"],
            [2, "weird_key", "Comp-Key", ["K"], ""],
            [3, "ceo", "Person", ["L"]]
        ]],
        ["Comp-Key", "Array", [], "", [
            [1, "alphabetical_part", "String", ["{2", "}2"]],
            [2, "numeric", "Integer", ["w3", "x3"], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Person": {
        "id": 5,
        "name": "Name",
        "mother": 1,
        "father": 1,
        "siblings": [1],
        "employer": ["aa", 3]
    }
    }

    compact_json = {"Person": [5, "Name", 1, 1, [1], ["aa", 3]]}

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_tag_id():
    jadn_schema = {
    "meta": {
        "package": "https://www.tagid.com",
        "title": "TagID Test",
        "roots": ["Root-Test"]
    },
    "types": [
        ["Root-Test", "Record", ["q"], "", [
            [1, "type_name", "String", [], ""],
            [2, "selected_type", "Selected-Type", [], ""],
            [3, "fields", "JADN-Type", ["&2"], ""]
        ]],
        ["Selected-Type", "Enumerated", ["#JADN-Type"], "", [
            [1, "string", "Array-Empty", [], ""],
            [2, "record", "Array-Fields", [], ""],
            [3, "enum", "Array-Items", [], ""]
        ]],
        ["JADN-Type", "Choice", [], "", [
            [1, "string", "Array-Empty", [], ""],
            [2, "record", "Array-Fields", [], ""],
            [3, "enum", "Array-Items", [], ""]
        ]],
        ["Array-Items", "Array", [], "", [
            [1, "field_value_1", "String", [], ""],
            [2, "field_value_2", "String", [], ""]
        ]],
        ["Array-Fields", "Array", [], "", [
            [1, "field_value_a", "String", [], ""],
            [2, "field_value_b", "String", [], ""]
        ]],
        ["Array-Empty", "Array", [], "", []]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Root-Test": {
        "type_name": "Type-Name",
        "selected_type": "record",
        "fields": ["a", "b"]
    }
    }

    compact_json = {"Root-Test": ["Type-Name", "record", ["a", "b"]]}

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_map_id():
    jadn_schema = {
    "meta": {
        "roots": ["Map-Name"]
    },
    "types": [
        ["Map-Name", "Map", ["="], "", [
            [1, "field_value_1", "String", [], ""],
            [2, "field_value_2", "String", [], ""],
            [3, "field_value_3", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Map-Name": {
        "1": "a",
        "2": "b",
        "3": "c"
    }
    }

    compact_json = {
    "Map-Name": {
        "1": "a",
        "2": "b",
        "3": "c"
    }
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_choice_id():
    jadn_schema = {
    "meta": {
        "roots": ["Choice-Name"]
    },
    "types": [
        ["Choice-Name", "Choice", ["="], "", [
            [1, "field_value_1", "String", [], ""],
            [2, "field_value_2", "String", [], ""],
            [3, "field_value_3", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)
 
    verbose_json = {
    "Choice-Name": {
        "2": "b"
    }
    }

    compact_json = {
    "Choice-Name": {
        "2": "b"
    }
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

def test_enum_id():
    jadn_schema = {
    "meta": {
        "roots": ["Enum-Name"]
    },
    "types": [
        ["Enum-Name", "Enumerated", ["="], "", [
            [1, "choice_a", ""],
            [2, "choice_b", ""],
            [3, "choice_c", ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
    "Enum-Name": 1
    }

    compact_json = {
    "Enum-Name": 1
    }

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

# TODO: Fix after discussion on optional fields with customer
def test_optional_fields():
    jadn_schema = {
    "meta": {
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "req_1", "String", [], ""],
            [2, "req_2", "String", [], ""],
            [3, "opt_1", "String", ["[0"], ""],
            [4, "req_3", "String", [], ""],
            [5, "opt_2", "String", ["[0"], ""],
            [6, "opt_3", "String", ["[0"], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})
    root_name = jadn_schema.get('meta', {}).get('roots', [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)

    verbose_json = {
        "Record-Name": {
            "req_1": "a",
            "req_2": "b",
            "req_3": "c",
            "opt_2": "d"
        }
    }

    compact_json = {"Record-Name": ["a", "b", "c", "d"]}

    test = compact_to_verbose(ordered_types, compact_json, root_def)

    assert compact_to_verbose(ordered_types, compact_json, root_def) == verbose_json

########## TEST EXAMPLE SCHEMAS
def test_schema_classes():
    json_data_compact = schema_classes_compact_j_data
    json_data_expected = schema_classes_data
    jadn_schema = schema_classes_schema

    jadn_types = jadn_schema.get("types", {})
    root_name = jadn_schema.get("meta", {}).get("roots", [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)
    verbose_output = compact_to_verbose(ordered_types, json_data_compact, root_def)
    write_verbose_output(verbose_output, "schema-classes-verbose.json")
    assert verbose_output == json_data_expected

def test_compact_music_lib_to_verbose():
    json_data = j_data
    jadn_types = j_schema.get("types", {})
    root_name = j_schema.get("meta", {}).get("roots", [None])[0]
    root_def = get_jadn_type_by_name(jadn_types, root_name)
    ordered_types = get_real_type_order(jadn_types, [], root_def)
    verbose_output = compact_to_verbose(ordered_types, json_data, root_def)
    write_verbose_output(verbose_output, "music-library-verbose.json")
    assert verbose_output == verbose_j_data