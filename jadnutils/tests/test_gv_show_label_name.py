import re

from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.tests.helpers import find_edge_attr_block, parse_edge_attrs


def make_simple_schema():
    # Two types: A has a field referencing B (non-primitive)
    return {
        'meta': {'roots': ['A']},
        'types': [
            ['A', 'Record', [], 'A record', [['f1', 'field1', 'B', []]]],
            ['B', 'Record', [], 'B record', []]
        ]
    }


def test_show_label_name_off_and_on():
    schema = make_simple_schema()

    # show_label_name = False -> edges should not contain a label= attribute
    g_off = GvGenerator(schema, {'show_label_name': False})
    src_off = g_off.generate()
    # Inspect the specific edge A -> B attributes and assert label not present
    attrs_block_off = find_edge_attr_block(src_off, 'A', 'B')
    assert attrs_block_off is not None
    attrs_off = parse_edge_attrs(attrs_block_off)
    assert 'label' not in attrs_off

    # show_label_name = True -> edges should contain label=attributes for our field
    g_on = GvGenerator(schema, {'show_label_name': True})
    src_on = g_on.generate()
    attrs_block_on = find_edge_attr_block(src_on, 'A', 'B')
    assert attrs_block_on is not None
    attrs_on = parse_edge_attrs(attrs_block_on)
    assert 'label' in attrs_on
