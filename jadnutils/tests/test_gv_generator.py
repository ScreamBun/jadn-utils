import os
import re
import sys

from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.utils.utils import write_gv_to_output
from jadnutils.tests.test_data.ap_hunt import ap_hunt_schema
from jadnutils.tests.test_data.oc2_101 import oc2_101_schema
from jadnutils.tests.test_data.music_lib import j_schema
from jadnutils.tests.test_data.generic_schema import generic_schema
from jadnutils.tests.test_data.unresolved_schema import unresolved_schema

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
    
    
def test_unresolved_schema():
    
    gv_gen = GvGenerator(unresolved_schema, {})
    gv_source = gv_gen.generate()

    # Basic checks
    assert isinstance(gv_source, str)
    assert 'digraph' in gv_source or 'graph' in gv_source
    # Check that all types are present as nodes
    for t in unresolved_schema['types']:
        assert re.search(r'"?' + re.escape(t[0]) + r'"?\s*\[', gv_source) or re.search(r'\b' + re.escape(t[0]) + r'\b', gv_source)
    # Check that root nodes are highlighted
    for root in unresolved_schema['meta']['roots']:
        assert root in gv_source    
        
    filename = "test_unresolved_schema"
    svg_path = write_gv_to_output(gv_source, filename, remove_source=True)
    assert os.path.exists(svg_path)
    
def test_gv_generator_oc2_101():
    
    gv_gen = GvGenerator(oc2_101_schema, {})
    gv_source = gv_gen.generate()

    # Basic checks
    assert isinstance(gv_source, str)
    assert 'digraph' in gv_source or 'graph' in gv_source
    # Check that all types are present as nodes
    for t in oc2_101_schema['types']:
        assert re.search(r'"?' + re.escape(t[0]) + r'"?\s*\[', gv_source) or re.search(r'\b' + re.escape(t[0]) + r'\b', gv_source)
    # Check that root nodes are highlighted
    for root in oc2_101_schema['meta']['roots']:
        assert root in gv_source    
        
    filename = "test_oc2_101_gv"
    try:
        svg_path = write_gv_to_output(gv_source, filename, remove_source=True)
    except Exception as e:
        assert False, f"write_gv_to_output failed: {e}"
        
    assert os.path.exists(svg_path)    
    
def test_gv_generator_oc2_110():
    
    gv_gen = GvGenerator(oc2_101_schema, {})
    gv_source = gv_gen.generate()

    # Basic checks
    assert isinstance(gv_source, str)
    assert 'digraph' in gv_source or 'graph' in gv_source
    # Check that all types are present as nodes
    for t in oc2_101_schema['types']:
        assert re.search(r'"?' + re.escape(t[0]) + r'"?\s*\[', gv_source) or re.search(r'\b' + re.escape(t[0]) + r'\b', gv_source)
    # Check that root nodes are highlighted
    for root in oc2_101_schema['meta']['roots']:
        assert root in gv_source    
        
    filename = "test_oc2_110_gv"
    try:
        svg_path = write_gv_to_output(gv_source, filename, remove_source=True)
    except Exception as e:
        assert False, f"write_gv_to_output failed: {e}"
        
    assert os.path.exists(svg_path)
    
def test_gv_generator_ap_hunt():
    
    gv_gen = GvGenerator(ap_hunt_schema, {})
    gv_source = gv_gen.generate()

    # Basic checks
    assert isinstance(gv_source, str)
    assert 'digraph' in gv_source or 'graph' in gv_source
    # Check that all types are present as nodes
    for t in ap_hunt_schema['types']:
        assert re.search(r'"?' + re.escape(t[0]) + r'"?\s*\[', gv_source) or re.search(r'\b' + re.escape(t[0]) + r'\b', gv_source)
    # Check that root nodes are highlighted
    for root in ap_hunt_schema['meta']['roots']:
        assert root in gv_source    
        
    filename = "ap_hunt_schema"
    try:
        svg_path = write_gv_to_output(gv_source, filename, remove_source=True)
    except Exception as e:
        assert False, f"write_gv_to_output failed: {e}"
        
    assert os.path.exists(svg_path)      