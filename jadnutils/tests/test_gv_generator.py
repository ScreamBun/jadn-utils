import os
import re
import sys

from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.utils.utils import write_gv_to_output
from jadnutils.tests.test_data.music_lib import j_schema
from jadnutils.tests.test_data.generic_schema import generic_schema

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_data')))

def test_generic_data():
    
    gv_gen = GvGenerator(generic_schema, {})
    gv_source = gv_gen.generate()

    # Basic checks
    assert isinstance(gv_source, str)
    assert 'digraph' in gv_source or 'graph' in gv_source
    # Check that all types are present as nodes
    for t in generic_schema['types']:
        assert re.search(r'"?' + re.escape(t[0]) + r'"?\s*\[', gv_source) or re.search(r'\b' + re.escape(t[0]) + r'\b', gv_source)
    # Check that root nodes are highlighted
    for root in generic_schema['meta']['roots']:
        assert root in gv_source    
        
    filename = "test_generic_schema"
    svg_path = write_gv_to_output(gv_source, filename, remove_source=True)
    assert os.path.exists(svg_path)  

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