#!/usr/bin/env python3
from pathlib import Path
from subprocess import run
from jadnutils.gv.gv_generator import GvGenerator

OUT = Path('output')
OUT.mkdir(exist_ok=True)

schema = {
    'meta': {'roots': ['Album']},
    'types': [
        ['Album', 'Record', [], '', [['id','id','String',[]], ['tracks','tracks','Array', ['*Track']]]],
        ['Track', 'Record', [], '', [['title','title','String',[]]]],
        ['String', 'String', [], '', []]
    ]
}

for spacer in (2, 6, 12):
    style = {'label_spacer_height': spacer}
    gv = GvGenerator(schema, style=style)
    src = gv.generate()
    gvfile = OUT / f'sample_spacer_{spacer}.gv'
    svgfile = OUT / f'sample_spacer_{spacer}.svg'
    gvfile.write_text(src)
    print(f'Wrote {gvfile}')

    # Try to render using dot if it's available
    cmd = ['dot', '-Tsvg', str(gvfile), '-o', str(svgfile)]
    try:
        r = run(cmd, check=False)
        if r.returncode == 0:
            print(f'Rendered {svgfile}')
        else:
            print(f'Could not render {svgfile}; dot returned {r.returncode}. You can render manually:')
            print('  dot -Tsvg {inp} -o {outp}'.format(inp=gvfile, outp=svgfile))
    except FileNotFoundError:
        print('dot (Graphviz) not found in PATH. To render the GV files to SVG install graphviz and run:')
        print('  dot -Tsvg output/sample_spacer_<n>.gv -o output/sample_spacer_<n>.svg')

print('Done')
