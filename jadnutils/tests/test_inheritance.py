import os
import sys
import json
from jadnutils.utils.jadn_utils import get_inherited_fields, get_type_by_name, get_children

def test_get_inherited_fields():
    j_schema = {
        "types": [
            ["Common-Items", "Array", [], "", [
                [1, "common_1", "Integer", ["[0"]],
                [2, "common_2", "Integer", ["[0"]],
                [3, "common_3", "Integer", ["[0"]],
            ]],            
            ["Root-Test", "Array", ["eCommon-Items"], "", [
                [111, "item_1", "String", [], ""],
                [222, "item_2", "String", ["[0"], ""],
                [333, "item_3", "String", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = j_schema.get("types", [])

    root_field = get_type_by_name(jadn_types, "Root-Test")
    root_children = get_children(root_field)
    root_children = get_inherited_fields(jadn_types, root_field, root_children)
    assert root_children == [
        [1, "common_1", "Integer", ["[0"]],
        [2, "common_2", "Integer", ["[0"]],
        [3, "common_3", "Integer", ["[0"]],
        [111, "item_1", "String", [], ''],
        [222, "item_2", "String", ["[0"], ''],
        [333, "item_3", "String", ["[0"], '']
    ]

def test_get_inherited_fields_extend_overwrite():
    j_schema = {
        "types": [
            ["Common-Items", "Array", [], "", [
                [1, "common_1", "Integer", ["[0"]],
                [2, "common_2", "Integer", ["[0"]],
                [3, "common_3", "Integer", ["[0"]],
            ]],            
            ["Root-Test", "Array", ["eCommon-Items"], "", [
                [1, "common_1_edited", "Integer", ["[0", "w0"], ""]
            ]]
        ]
    }
    jadn_types = j_schema.get("types", [])

    root_field = get_type_by_name(jadn_types, "Root-Test")
    root_children = get_children(root_field)
    root_children = get_inherited_fields(jadn_types, root_field, root_children)
    assert root_children == [
        [1, "common_1_edited", "Integer", ["[0", "w0"], ""],
        [2, "common_2", "Integer", ["[0"]],
        [3, "common_3", "Integer", ["[0"]]
    ]

def test_get_inherited_fields_restrict_overwrite():
    j_schema = {
        "types": [
            ["Common-Items", "Array", [], "", [
                [1, "common_1", "Integer", ["[0"]],
                [2, "common_2", "Integer", ["[0"]],
                [3, "common_3", "Integer", ["[0"]],
            ]],            
            ["Root-Test", "Array", ["rCommon-Items"], "", [
                [1, "common_1_edited", "Integer", ["[0", "w0"], ""],
                [4, "common_4", "Integer", ["[0"], ""]
            ]]
        ]
    }
    jadn_types = j_schema.get("types", [])

    root_field = get_type_by_name(jadn_types, "Root-Test")
    root_children = get_children(root_field)
    root_children = get_inherited_fields(jadn_types, root_field, root_children)
    assert root_children == [
        [1, "common_1_edited", "Integer", ["[0", "w0"], ""],
        [2, "common_2", "Integer", ["[0"]],
        [3, "common_3", "Integer", ["[0"]]
    ]