"""Generate three graphs (informational, logical, conceptual) and write SVGs to output/ for visual comparison."""
from jadnutils.gv.gv_generator import GvGenerator
import os

schema = {
    'meta': {'roots': ['Album']},
    'types': [
        ['Album', 'Record', [], '', [['id', 'id', 'String', ['[1]', ']5']], ['title', 'title', 'String', []]]],
        ['String', 'String', [], '', []]
    ]
}

out = 'output'
os.makedirs(out, exist_ok=True)

modes = [
    ('informational', GvGenerator.INFORMATIONAL),
    ('logical', GvGenerator.LOGICAL),
    ('conceptual', GvGenerator.CONCEPTUAL),
]

for name, mode in modes:
    g = GvGenerator(schema, {'detail': mode, 'graph_attr': {'label': name}})
    src = g.generate()
    path = os.path.join(out, f'gv_detail_{name}.gv')
    with open(path, 'w') as f:
        f.write(src)
    print('Wrote', path)
print('Done')
