from jadnutils.gv.gv_generator import GvGenerator


def test_enums_allowed_truncation():
    # Schema with a single Enumerated type containing three items
    schema = {
        'meta': {'roots': []},
        'types': [
            ['E', 'Enumerated', [], '', [
                [1, 'a', ''],
                [2, 'b', ''],
                [3, 'c', '']
            ]]
        ]
    }

    # When enums_allowed is 1, only the first item should be shown and
    # a summary row should indicate the remaining count.
    gv = GvGenerator(schema, {'enums_allowed': 1, 'detail': 'informational'})
    src = gv.generate()
    assert '1 a' in src
    assert '2 b' not in src
    assert '3 c' not in src
    assert '... and 2 more' in src


def test_enums_allowed_none_shows_all():
    schema = {
        'meta': {'roots': []},
        'types': [
            ['E', 'Enumerated', [], '', [
                [1, 'a', ''],
                [2, 'b', ''],
                [3, 'c', '']
            ]]
        ]
    }

    # When enums_allowed is None (or omitted) all items should be shown
    gv = GvGenerator(schema, {'enums_allowed': None, 'detail': 'informational'})
    src = gv.generate()
    assert '1 a' in src
    assert '2 b' in src
    assert '3 c' in src
    assert '... and' not in src
