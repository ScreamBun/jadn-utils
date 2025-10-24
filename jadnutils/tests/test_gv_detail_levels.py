import re
from jadnutils.gv.gv_generator import GvGenerator


def make_schema():
    return {
        'meta': {'roots': ['Album']},
        'types': [
            ['Album', 'Record', [], '', [['id', 'id', 'String', ['[1]', ']5']]]],
            ['String', 'String', [], '', []]
        ]
    }


def extract_label(src, node_name='Album'):
    m = re.search(r"""%s\s*\[label=(?P<label><.*?>>)\s*(?P<attrs>[^\]]*)\]""" % node_name, src, re.S)
    assert m, 'node not found'
    return m.group('label')


def test_informational_detail_contains_full_fields():
    schema = make_schema()
    g = GvGenerator(schema, {'detail': GvGenerator.INFORMATIONAL})
    src = g.generate()
    label = extract_label(src)
    assert 'id id:' in label  # shows id, name and type
    assert 'String' in label


def test_logical_detail_shows_field_names_only():
    schema = make_schema()
    g = GvGenerator(schema, {'detail': GvGenerator.LOGICAL})
    src = g.generate()
    label = extract_label(src)
    assert 'id id:' not in label
    assert 'id' in label
    assert 'String' not in label


def test_conceptual_detail_shows_only_type_header():
    schema = make_schema()
    g = GvGenerator(schema, {'detail': GvGenerator.CONCEPTUAL})
    src = g.generate()
    label = extract_label(src)
    assert 'id' not in label
    assert 'String' not in label
    # should include Album: Record header
    assert 'Album:' in label
    assert 'Record' in label
