import os
import sys
import json
from jadnutils.utils.conversion_utils import serialize_as_compact
from jadnutils.json.convert_compact import convert_to_compact

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
from music_lib_data import j_data
from music_lib import j_schema

def write_compact_output(compact_output, filename):
    """
    Write compact JSON output to a file in the output directory and print it.
    """
    output_dir = "output"
    output_path = os.path.join(output_dir, filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(compact_output))
    print(compact_output)

### TEST CONVERT TO COMPACT FUNCTION
def test_convert_to_compact():
    json_data = j_data
    compact_json = convert_to_compact(j_schema, json_data)
    write_compact_output(compact_json, "music-library-compact.json")
    assert compact_json

#### TEST STRIP KEYS UTIL
def test_compact_serialize():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "dob", "String", [], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "dob": "the 4th of July 1990",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "dob": "the 27th of June 1982"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", "the 4th of July 1990", 79546],
        ["Alice", "B239-5921-348", "the 27th of June 1982"]
    ]

    assert serialize_as_compact(jadn_types, nested_json) == expected_json

def test_compact_serialize_2():
    jadn_schema = {
        "types": [
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "elevation", "Integer", [], ""],
                [3, "location", "Array", [], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = { 
        'name': 'Hamilton',
        'elevation': 20,
        'location': [32.2912, -64.7864] 
    }

    expected_json = ['Hamilton', 20, [32.2912, -64.7864]]

    assert serialize_as_compact(jadn_types, nested_json) == expected_json

def test_compact_serialize_3():
    jadn_schema = {
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

    nested_json = [
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

    expected_json = [["St. Louis", "Missouri", "38.627003", "-90.199402"],["Seattle", "Washington", "47.60621", "-122.33207"]]

    assert serialize_as_compact(jadn_types, nested_json) == expected_json

def test_compact_serialize_4():
    """
    Test case where example is NOT all records
    """
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

    nested_json = {
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

    expected_json = {"Person": {"name": "Test Person", "address": ["12345", "Columbia", "Maryland", 11111], "house_info": {"purchase_amount": 100000, "date_purchased": "2023-01-01"}}}
    compact_json = serialize_as_compact(jadn_types, nested_json)

    assert compact_json == expected_json

def test_compact_serialize_inheritance_extend():
    jadn_schema = {"types": [
        ["Abstract-Record", "Record", ["a"], "This is an abstract record.", [
            [1, "value_1", "String", ["[0"], ""],
            [2, "value_2", "Integer", ["[0"], ""],
            [3, "value_3", "String", ["[0"], ""]
        ]],
        ["Restrict-Record", "Record", ["rAbstract-Record"], "", []],
        ["Extend-Record", "Record", ["eAbstract-Record"], "", [
            [4, "value_4", "String", [], ""],
            [5, "value_5", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = {
    "Extend-Record": {
        "value_1": "1",
        "value_2": 2,
        "value_3": "3",
        "value_4": "4",
        "value_5": "5"
    }
    }

    expected_json = {"Extend-Record": ["1", 2, "3", "4", "5"]}

    assert serialize_as_compact(jadn_types, nested_json) == expected_json

def test_compact_serialize_inheritance_restrict():
    jadn_schema = {"types": [
        ["Abstract-Record", "Record", ["a"], "This is an abstract record.", [
            [1, "value_1", "String", ["[0"], ""],
            [2, "value_2", "Integer", ["[0"], ""],
            [3, "value_3", "String", ["[0"], ""]
        ]],
        ["Restrict-Record", "Record", ["rAbstract-Record"], "", []],
        ["Extend-Record", "Record", ["eAbstract-Record"], "", [
            [4, "value_4", "String", [], ""],
            [5, "value_5", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = {
    "Restrict-Record": {
        "value_1": "1",
        "value_2": 2,
        "value_3": "3"
    }
    }

    expected_json = {"Restrict-Record": ["1", 2, "3"]}

    assert serialize_as_compact(jadn_types, nested_json) == expected_json

def test_concise_serialize_inheritance_recursive():
    jadn_schema = {
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

    nested_json = {
    "Extend-2": {
        "abstract_1": "1",
        "abstract_2": "2",
        "abstract_3": "3",
        "abstract_4": "4",
        "extend_1": "5",
        "extend_2": "6"
    }
    }

    expected_json = {"Extend-2": ["1", "2", "3", "4", "5", "6"]}
    assert serialize_as_compact(jadn_types, nested_json) == expected_json