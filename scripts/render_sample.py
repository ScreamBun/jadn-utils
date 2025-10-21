import sys
sys.path.insert(0, '/home/matt/workspace/jadn-utils')
from jadnutils.gv.gv_generator import GvGenerator

schema = {
    "types": [
        ["A", "Record", [], "", [["id", "id", "B", ["[1", "]3"]]]],
        ["B", "Record", [], "", [["x", "x", "String", []]]]
    ],
    "meta": {"roots": ["A"]}
}

g = GvGenerator(schema, style={})
print(g.generate())
