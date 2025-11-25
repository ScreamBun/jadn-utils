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
        "dob": "-1990-07",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "dob": "-1982-06"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", 646804800, 79546],
        ["Alice", "B239-5921-348", 391752000, None]
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
        ["Alice", "B239-5921-348", 76651200, None]
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
        ["Alice", "B239-5921-348", 22500, None]
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
        ["Alice", "B239-5921-348", 15, None]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_gyear():
    jadn_schema = {
        "types": [
            ["People", "Array", [], "", [
                [1, "bob", "Person", [], ""],
                [2, "alice", "Person", [], ""]
            ]],
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "String", [], ""],
                [3, "dob", "String", ["/gYear"], ""],
                [4, "weight", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = [{
        "name": "Bob",
        "id": "K193-3498-234",
        "dob": "-1990",
        "weight": 79546
        }, {
        "name": "Alice",
        "id": "B239-5921-348",
        "dob": "-1982"
    }]
    
    expected_json = [
        ["Bob", "K193-3498-234", 631170000, 79546],
        ["Alice", "B239-5921-348", 378709200, None]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_formats():
    jadn_schema = {
    "meta": {
        "package": "https://www.test.com",
        "roots": ["Decimal-Integer", "Binary-Fmt", "Integer-Fmts", "String-Fmts"]
    },
    "types": [
        ["Decimal-Integer", "Record", [], "", [
            [1, "u64", "Integer", ["/u64"], ""],
            [2, "i64", "Integer", ["/i64"], ""],
            [3, "non_negative_integer", "Integer", ["/nonNegativeInteger"], ""],
            [4, "negative_integer", "Integer", ["/negativeInteger"], ""],
            [5, "non_positive_integer", "Integer", ["/nonPositiveInteger"], ""],
            [6, "positive_integer", "Integer", ["/positiveInteger"], ""],
            [7, "unsigned_short", "Integer", ["/u16"], ""]
        ]],
        ["Binary-Fmt", "Record", [], "", [
            [1, "lower_x", "Binary", ["/x", "[0"], ""],
            [2, "upper_x", "Binary", ["/X", "[0"], ""],
            [3, "base64", "Binary", ["/b64", "[0"], ""]
        ]],
        ["Integer-Fmts", "Record", [], "", [
            [1, "int_date_time", "Integer", ["/date-time"], ""],
            [2, "string_date_time", "String", ["/date-time"], ""],
            [3, "int_date", "Integer", ["/date"], ""],
            [4, "string_date", "String", ["/date"], ""],
            [5, "time", "Integer", ["/time"], ""],
            [6, "string_time", "String", ["/time"], ""],
            [7, "g_year_month", "Integer", ["/gYearMonth"], ""],
            [8, "g_year", "Integer", ["/gYear"], ""],
            [9, "g_month_day", "Integer", ["/gMonthDay"], ""],
            [10, "duration_test", "Integer", ["/duration"], ""],
            [11, "day_time_duration", "Integer", ["/dayTimeDuration"], ""],
            [12, "year_month_duration", "Integer", ["/yearMonthDuration"], ""]
        ]],
        ["String-Fmts", "Record", [], "", [
            [1, "normalized_string", "String", ["/normalizedString"], ""],
            [2, "token", "String", ["/token"], ""],
            [3, "language", "String", ["/language"], ""],
            [4, "name", "String", ["/name"], ""],
            [5, "any_uri", "String", ["/anyUri"], ""],
            [6, "qname", "String", ["/QName"], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = {
    "int_date_time": 1761664474,
    "string_date_time": "2023-01-01T00:00+03:00",
    "int_date": 1761664474,
    "string_date": "2023-01-01",
    "time": 1761664474,
    "string_time": "12:00:00",
    "g_year_month": "-1000-05",
    "g_year": 1999,
    "g_month_day": "--04-12Z",
    "duration_test": 1,
    "day_time_duration": "PT30M",
    "year_month_duration": "P17M"
    }

    expected_json = [
        1761664474, "2023-01-01T00:00+03:00", 1761664474, "2023-01-01", 1761664474, "12:00:00", -30599838238, 1999, 71902800, 1, 1800, 17
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

    nested_json_binary = {
        "lower_x": "ABCD",
        "upper_x": "ABCD",
        "base64": "ABCD"
    }

    expected_json_binary = [
        '41424344',
        '41424344',
        '001083'
    ]

    assert serialize_as_concise(jadn_types, nested_json_binary) == expected_json_binary

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
        ["Bob", "K193-3498-234", '3139322e3136382e312e313030', 79546],
        ["Alice", "B239-5921-348", '31302e302e302e31', None]
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
        ["Bob", "K193-3498-234", '323030313a306462383a383561333a303030303a303030303a386132653a303337303a37333334', 79546],
        ["Alice", "B239-5921-348", '666538303a3a31', None]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_ipv4net():
    jadn_schema =  { 
        "types": [
            ["Array-Name", "Array", ["/ipv4-net", "{1", "}2"], "", [
                [1, "ipv4_addr", "Binary", ["/ipv4-addr", "{1"], "IPv4 address as defined in [[RFC0791]](#rfc0791)"],
                [2, "prefix_length", "Integer", ["{0", "}32", "[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = {
        "Array-Name": "127.0.0.1/1"
    }
    
    expected_json = {
        'Array-Name': '3132372e302e302e312f31'
    }

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_binary():
    """
    Test /x, /X, /base64Binary, /b64
    """
    jadn_schema = {
        "types": [
            ["DataRecord", "Record", [], "", [
                [1, "dataHex", "String", ["/x"], ""],
                [2, "dataBase64", "String", ["/base64Binary"], ""],
                [3, "dataBin", "String", ["/b64"], ""],
                [4, "dataXUpper", "String", ["/X"], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = {
        "dataHex": "4d616e",
        "dataBase64": "TWFu",
        "dataBin": "TWFu",
        "dataXUpper": "4D616E"
    }
    
    expected_json = [
        '346436313665',
        '4d616e',
        '4d616e',
        '344436313645'
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

def test_concise_serialize_enumerated_id():
    jadn_schema = {
    "meta": {
        "roots": ["Enumerated-Name"]
    },
    "types": [
        ["Enumerated-Name", "Enumerated", ["="], "", [
            [1, "field_1", ""],
            [2, "field_2", ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = {
    "Enumerated-Name": 1
    }

    expected_json = 1

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_choice():
    jadn_schema = {
        "types": [
            ["ChoiceType", "Choice", [], "", [
                [1, "optionA", "String", [], ""],
                [2, "optionB", "Integer", [], ""]
            ]],
            ["Item", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "choiceField", "ChoiceType", [], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = {
        "name": "Gadget",
        "choiceField": {
            "optionB": 42
        }
    }
    
    expected_json = [
        "Gadget",
        {2: 42}
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_choice_id():
    jadn_schema = {
    "meta": {
        "roots": ["Choice-Name"]
    },
    "types": [
        ["Choice-Name", "Choice", ["="], "", [
            [1, "field_value_1", "String", [], ""],
            [2, "field_value_2", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = {
        "1": "test"
    }

    expected_json = {
        1: "test"
    }

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_map():
    jadn_schema = {
        "types": [
            ["MapType", "Map", [], "", [
                [1, "key1", "String", [], ""],
                [2, "key2", "Integer", [], ""]
            ]],
            ["Item", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "mapField", "MapType", [], ""]
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = {
        "name": "Container",
        "mapField": {
            "key1": "value1",
            "key2": 100
        }
    }
    
    expected_json = [
        "Container",
        {
            1: "value1",
            2: 100
        }
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_map_id():
    jadn_schema = {
    "meta": {
        "roots": ["Map-Name"]
    },
    "types": [
        ["Map-Name", "Map", ["="], "", [
            [1, "field_1", "String", [], ""],
            [2, "field_2", "String", [], ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = {
    "field_1": "value1",
    "field_2": "value2"
    }

    expected_json = {
        1: "value1",
        2: "value2"
    }

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_complex():
    jadn_schema = {
    "meta": {
        "package": "https://www.test",
        "roots": ["Parent-Record"]
    },
    "types": [
        ["Parent-Record", "Record", [], "", [
            [1, "choice", "Choice", [], ""],
            [2, "map", "Map", [], ""],
            [3, "enumerated", "Enumerated", [], ""]
        ]],
        ["Choice", "Choice", [], "", [
            [1, "option_a", "String", [], ""],
            [2, "option_b", "String", [], ""]
        ]],
        ["Map", "Map", [], "", [
            [1, "field_1", "String", [], ""],
            [2, "field_2", "String", [], ""]
        ]],
        ["Enumerated", "Enumerated", [], "", [
            [1, "selection_1", ""],
            [2, "selection_2", ""],
            [3, "selection_3", ""]
        ]]
    ]
    }
    jadn_types = jadn_schema.get('types', {})

    nested_json = {
        "choice": {
        "option_a": "a"
        },
        "map": {
        "field_1": "1",
        "field_2": "2"
        },
        "enumerated": "selection_2"
    }

    expected_json = [
        {1: "a"},
        {
            1: "1",
            2: "2"
        },
        2
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_issue_field_disappearing():
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
            [1, "string_choice_2", "String", ["N"], ""],
            [2, "integer_choice_2", "Integer", [], ""]
        ]],
        ["Choice-Regular", "Choice", [], "", [
            [1, "string_choice", "String", [], ""],
            [2, "integer_choice", "String", [], ""]
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

    nested_json = {
        "field_value_1": "1",
        "field_value_2": "2"
    }
    expected_json = {
        1: ["1", "2"]
    }
    assert serialize_as_concise(jadn_types, nested_json) == expected_json

    nested_json = {
        "choice_combine": "a",
        "choice_regular": {
            "string_choice": "b"
        },
        "choice_combine_complex": {
            "field_value_1": "c",
            "field_value_2": "d"
        }
    }

    expected_json = [
        "a",
        {1: 'b'},
        ["c", "d"]
    ]

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_inheritance_extend():
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

    assert serialize_as_concise(jadn_types, nested_json) == expected_json

def test_concise_serialize_inheritance_restrict():
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

    assert serialize_as_concise(jadn_types, nested_json) == expected_json
    
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
    assert serialize_as_concise(jadn_types, nested_json) == expected_json

    nested_json = {
    "Restrict-2": {
        "abstract_1": "1",
        "abstract_2": "2",
        "abstract_3": "3",
        "abstract_4": "4",
        "extend_4": "5",
        "extend_5": "6"
    }
    }

    expected_json = {"Restrict-2": ["1", "2", "3", "4", "5", "6"]}
    assert serialize_as_concise(jadn_types, nested_json) == expected_json