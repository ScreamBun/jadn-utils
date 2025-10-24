import re
from jadnutils.gv.gv_generator import GvGenerator


def make_schema():
    return {
        'meta': {'roots': ['Album']},
        'types': [
            # use '{2' and '}5' so get_min_max_length() produces '{2..5}'
            ['Album', 'Record', [], '', [['id', 'id', 'String', ['{2', '}5']]]],
            ['String', 'String', [], '', []]
        ]
    }


def extract_label(src, node_name='Album'):
    m = re.search(r"""%s\s*\[label=(?P<label><.*?>>)\s*(?P<attrs>[^\]]*)\]""" % node_name, src, re.S)
    assert m, 'node not found'
    return m.group('label')


def test_len_shown_only_in_informational():
    schema = make_schema()
    g = GvGenerator(schema, {'detail': GvGenerator.INFORMATIONAL})
    src = g.generate()
    label = extract_label(src)
    # length {2..5} should be present in informational mode
    assert '{2..5}' in label


def test_len_hidden_in_logical_and_conceptual():
    schema = make_schema()
    g = GvGenerator(schema, {'detail': GvGenerator.LOGICAL})
    src = g.generate()
    label = extract_label(src)
    # logical: no length
    assert '{2..5}' not in label

    g = GvGenerator(schema, {'detail': GvGenerator.CONCEPTUAL})
    src = g.generate()
    label = extract_label(src)
    # conceptual: no length
    assert '{2..5}' not in label
