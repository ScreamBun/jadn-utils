from jadnutils.utils.conversion_utils import validate_json
import os
import sys
import json as _json

from jadnutils.html.html_converter import HtmlConverter

sys.path.append(os.path.join(os.path.dirname(__file__), "test_data"))
from jadnutils.utils.utils import write_to_output
from jadnutils.tests.test_data.music_lib import j_schema

    
def test_music_lib_to_html():
    json_data = j_schema
    
    # Validate the JSON data before conversion
    validate_json(json_data)
    
    converter = HtmlConverter(json_data)
    
    html_output = converter.jadn_to_html(run_validation=False)
    write_to_output(html_output, "test_jadn_to_html_music_lib.html")
    
    assert "<table" in html_output
    assert '<style>' in html_output
    assert '<title>Music Library</title>' in html_output
    assert '<div id="meta">' in html_output
    assert '<h3>Types</h3>' in html_output
    assert '<div class="types">' in html_output