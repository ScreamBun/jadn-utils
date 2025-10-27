import os
import sys
import json
from jadnutils.utils.conversion_utils import serialize_as_concise
from jadnutils.json.convert_concise import convert_to_concise

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
from music_lib_data import j_data
from music_lib import j_schema

def write_concise_output(concise_output, filename):
    """
    Write concise JSON output to a file in the output directory and print it.
    """
    output_dir = "output"
    output_path = os.path.join(output_dir, filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(concise_output))
    print(concise_output)

### TEST CONVERT TO COMPACT FUNCTION
def test_convert_to_compact():
    json_data = j_data
    concise_json = convert_to_concise(j_schema, json_data)
    write_concise_output(concise_json, "music-library-concise.json")
    assert concise_json

#### TEST STRIP KEYS UTIL
def test_concise_serialize_gyearmonth():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "dob", "String", ["/gYearMonth"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "dob": "-1999-07",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "dob": "-1982-06"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", 930801600, 79546],
        ["Alice", "B239-5921-348", 391752000]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_gmonthday():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "dob", "String", ["/gMonthDay"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "dob": "--07-07",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "dob": "--06-06"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", 79329600, 79546],
        ["Alice", "B239-5921-348", 76651200]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json
