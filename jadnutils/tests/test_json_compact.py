import os
import sys
import json
from jadnutils.utils.conversion_utils import strip_keys
from jadnutils.json.convert_compact import convert_to_compact

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
from music_lib_data import j_data

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
    compact_json = convert_to_compact(json_data)
    write_compact_output(compact_json, "music-library-compact.json")
    assert compact_json

#### TEST STRIP KEYS UTIL
def test_strip_keys():
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

    assert strip_keys(nested_json) == expected_json

def test_strip_keys_2():
    nested_json = { 
        'name': 'Hamilton',
        'elevation': 20,
        'location': [32.2912, -64.7864] 
    }

    expected_json = ['Hamilton', 20, [32.2912, -64.7864]]

    assert strip_keys(nested_json) == expected_json

def test_strip_keys_3():
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

    assert strip_keys(nested_json) == expected_json