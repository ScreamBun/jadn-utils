import sys
sys.path.insert(0, '/home/matt/workspace/jadn-utils')
from jadnutils.gv.gv_generator import GvGenerator
from jadnutils.tests.test_data.music_lib import j_schema
import os
import subprocess

out_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(out_dir, exist_ok=True)
out_gv = os.path.join(out_dir, 'sample.gv')
out_png = os.path.join(out_dir, 'sample.png')

g = GvGenerator(j_schema)
dot_src = g.generate()
with open(out_gv, 'w') as f:
    f.write(dot_src)
print('Wrote', out_gv)
try:
    subprocess.run(['dot', '-Tpng', out_gv, '-o', out_png], check=True)
    print('Wrote', out_png)
except Exception as e:
    print('Rendering failed:', e)
