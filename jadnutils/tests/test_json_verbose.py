from jadnutils.utils.rev_conversion_utils import compact_to_verbose

def test_compact_to_verbose():
    jadn_schema = {
        "types": [
            ["Record-Name", "Record", [], "", [
                [1, "string_field", "String", [], ""],
                [2, "int_field", "Integer", [], ""],
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})
    
    nested_json = ["test", 1]

    expected_json = {
        "string_field": "test",
        "int_field": 1
    }

    assert compact_to_verbose(jadn_types, nested_json) == expected_json

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

def test_compact_to_verbose_complex():
    jadn_schema = {
        "types": [
            ["Map-Name", "Map", [], "", [
                [1, "key_field", "String", [], ""],
                [2, "value_field", "Record", [], "", [
                    [1, "inner_string", "String", [], ""],
                    [2, "inner_int", "Integer", [], ""],
                ]],
            ]]
        ]
    }
    jadn_types = jadn_schema.get('types', {})

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

    assert compact_to_verbose(jadn_types, nested_json) == expected_json