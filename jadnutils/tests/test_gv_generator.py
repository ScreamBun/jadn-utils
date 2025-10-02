import os
import re
import sys

from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.utils.utils import write_gv_to_output
from jadnutils.tests.test_data.music_lib import j_schema

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_data')))


# def test_basic_gen():
    
#     j_schema = {}
#     style = {}
#     gv_gen = GvGenerator(j_schema, style)

#     gv_source = gv_gen.generate({})
#     assert isinstance(gv_source, str)
#     assert "digraph" in gv_source or "graph" in gv_source  # basic Graphviz check

#     filename = "test_gv_basic_2"
#     svg_path = write_gv_to_output(gv_source, filename, remove_source=True)
#     assert os.path.exists(svg_path)

#     with open(svg_path, "r", encoding="utf-8") as f:
#         svg_content = f.read()
#     assert "<svg" in svg_content
#     assert "</svg>" in svg_content

def test_gv_generator_music_lib():
    
    gv_gen = GvGenerator(j_schema, {})
    gv_source = gv_gen.generate()

    # Basic checks
    assert isinstance(gv_source, str)
    assert 'digraph' in gv_source or 'graph' in gv_source
    # Check that all types are present as nodes
    for t in j_schema['types']:
        assert re.search(r'"?' + re.escape(t[0]) + r'"?\s*\[', gv_source) or re.search(r'\b' + re.escape(t[0]) + r'\b', gv_source)
    # Check that root nodes are highlighted
    for root in j_schema['meta']['roots']:
        assert root in gv_source    
        
    filename = "test_music_gv"
    svg_path = write_gv_to_output(gv_source, filename, remove_source=True)
    assert os.path.exists(svg_path)        