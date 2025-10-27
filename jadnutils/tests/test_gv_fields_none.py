from jadnutils.gv.gv_generator import GvGenerator


def test_type_with_fields_none_does_not_crash():
    # Schema where a type explicitly sets fields to None
    schema = {
        'meta': {'roots': []},
        'types': [
            ['TNone', 'Record', [], '', None]
        ]
    }

    gv = GvGenerator(schema, {})
    # Should not raise; should return a DOT source string containing the type name
    src = gv.generate()
    assert isinstance(src, str)
    assert 'TNone' in src
