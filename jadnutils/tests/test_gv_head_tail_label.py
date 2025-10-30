from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.tests.helpers import find_edge_attr_block, parse_edge_attrs


def make_simple_schema():
    return {
        'meta': {'roots': ['A']},
        'types': [
            # include a multiplicity option on the field so headlabel would normally be present
            ['A', 'Record', [], '', [['f1', 'field1', 'B', ['[1', ']3']]]],
            ['B', 'Record', [], '', []]
        ]
    }


def test_show_headlabel_and_taillabel_flags():
    schema = make_simple_schema()

    # Both head and tail labels off: neither appears
    g = GvGenerator(schema, {'show_headlabel': False, 'show_taillabel': False})
    src = g.generate()
    block = find_edge_attr_block(src, 'A', 'B')
    assert block is not None
    attrs = parse_edge_attrs(block)
    assert 'headlabel' not in attrs
    assert 'taillabel' not in attrs

    # Head on, tail off
    g = GvGenerator(schema, {'show_headlabel': True, 'show_taillabel': False})
    src = g.generate()
    block = find_edge_attr_block(src, 'A', 'B')
    assert block is not None
    attrs = parse_edge_attrs(block)
    assert 'headlabel' in attrs
    assert 'taillabel' not in attrs

    # Head off, tail on
    g = GvGenerator(schema, {'show_headlabel': False, 'show_taillabel': True})
    src = g.generate()
    block = find_edge_attr_block(src, 'A', 'B')
    assert block is not None
    attrs = parse_edge_attrs(block)
    assert 'headlabel' not in attrs
    assert 'taillabel' in attrs
