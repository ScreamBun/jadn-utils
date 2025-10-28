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

def test_concise_serialize_daytimeduration():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "dob", "String", ["/dayTimeDuration"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "dob": "P1DT12H30M45S",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "dob": "PT6H15M"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", 131445, 79546],
        ["Alice", "B239-5921-348", 22500]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_yearmonthduration():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "dob", "String", ["/yearMonthDuration"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "dob": "P2Y6M",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "dob": "P1Y3M"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", 30, 79546],
        ["Alice", "B239-5921-348", 15]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_ipv4addr():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "addr", "String", ["/ipv4-addr"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "addr": "192.168.1.100",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "addr": "10.0.0.1"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", b'192.168.1.100', 79546],
        ["Alice", "B239-5921-348", b'10.0.0.1']
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_ipv6addr():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "addr", "String", ["/ipv6-addr"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "addr": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "addr": "fe80::1"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", b'2001:0db8:85a3:0000:0000:8a2e:0370:7334', 79546],
        ["Alice", "B239-5921-348", b'fe80::1']
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_ipv4net():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "network", "Array", ["/ipv4-net"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "network": "192.168.1.0/24",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "network": "10.0.0.0/8"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", b'192.168.1.0/24', 79546],
        ["Alice", "B239-5921-348", b'10.0.0.0/8']
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_enumerated():
    jadn_schema = {
        "types": [
            ["ColorEnum", "Enumerated", [], "", [
                [1, "Red", ""],
                [2, "Green", ""],
                [3, "Blue", ""]
            ]],
            ["Item", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "color", "ColorEnum", [], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = {
        "name": "Ball",
        "color": "Red"
    }
    
    expected_json = [
        "Ball",
        1
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json