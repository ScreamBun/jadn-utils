import re
from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.tests.test_data.music_lib import j_schema


def _find_node_attrs(dot_src: str, node_name: str) -> str:
    # Find the first occurrence of node_name, then return the content between the
    # following '[' and the matching ']' (simple first-']' after '[' as attributes
    # won't contain nested square brackets in our DOT output).
    # Anchor to the start of a line to match the node definition precisely.
    pattern = rf'^\s*"?{re.escape(node_name)}"?\s*\[(.*?)\]\s*$'
    m = re.search(pattern, dot_src, flags=re.DOTALL | re.MULTILINE)
    return m.group(1) if m else ''


def test_per_type_node_attributes():
    g = GvGenerator(j_schema)
    dot = g.generate()

    # Album is a Record type in music_lib; expect a bgcolor in label or fillcolor and shape possibly plain
    album_attrs = _find_node_attrs(dot, 'Album')
    assert album_attrs, 'Album node not found in DOT'
    assert ('LightSkyBlue' in album_attrs) or ('BGCOLOR="LightSkyBlue"' in album_attrs) or ('fillcolor="LightSkyBlue"' in album_attrs)
    # Accept plain/none or ellipse depending on current per-type configuration
    assert (
        ('shape=plain' in album_attrs) or ('shape="plain"' in album_attrs)
        or ('shape=none' in album_attrs) or ('shape=ellipse' in album_attrs)
    )

    # Image-Format is an Enumerated type (should show Palegreen)
    img_attrs = _find_node_attrs(dot, 'Image-Format')
    assert img_attrs, 'Image-Format node not found in DOT'
    assert ('Palegreen' in img_attrs) or ('BGCOLOR="Palegreen"' in img_attrs) or ('fillcolor="Palegreen"' in img_attrs)
