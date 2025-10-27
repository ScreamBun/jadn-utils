import re

from jadnutils.gv.gv_generator import GvGenerator


def test_table_border_removed_for_ellipse():
    schema = {
        'meta': {'roots': ['Album']},
        'types': [
            ['Album', 'Record', [], '', [['id', 'id', 'String', []]]],
            ['String', 'String', [], '', []]
        ]
    }

    # Force Record to render as ellipse for this test
    gv = GvGenerator(schema, style={'per_type_attrs': {'Record': {'shape': GvGenerator.NODE_SHAPE_ELLIPSE, 'fillcolor': GvGenerator.COLOR_LIGHTSKYBLUE}}})
    src = gv.generate()

    # Extract the Album node label block and attributes
    m = re.search(r"Album\s*\[label=(?P<label><.*?>>)\s*(?P<attrs>[^\]]*)\]", src, re.S)
    assert m, "Could not locate Album node in generated DOT"

    label = m.group('label')
    attrs = m.group('attrs')

    # When shape is ellipse, the TABLE should be borderless and not have a bgcolor
    assert 'border="0"' in label, 'TABLE should include border="0" when rendered inside an ellipse'
    assert 'bgcolor="' not in label, 'TABLE should not include a bgcolor when node uses node-level fill'

    # Node attributes should include shape=ellipse and a fillcolor
    assert 'shape=ellipse' in attrs, f'Expected shape=ellipse in node attrs, got: {attrs}'
    assert 'fillcolor=' in attrs, f'Expected fillcolor in node attrs, got: {attrs}'
