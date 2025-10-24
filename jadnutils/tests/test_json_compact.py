import os
import sys
import json
from jadnutils.utils.conversion_utils import strip_keys
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
def test_strip_keys():
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

    assert strip_keys(jadn_types, nested_json) == expected_json

def test_strip_keys_2():
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

    assert strip_keys(jadn_types, nested_json) == expected_json

def test_strip_keys_3():
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

    assert strip_keys(jadn_types, nested_json) == expected_json

def test_strip_keys_4():
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
    compact_json = strip_keys(jadn_types, nested_json)

    assert compact_json == expected_json