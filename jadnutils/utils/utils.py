import os

import graphviz


def write_to_output(data, filename):
    """
    Write data to a file in the output directory and print it.
    """
    output_dir = "output"
    output_path = os.path.join(output_dir, filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(data)
        
    print(data)
    

def write_gv_to_output(gv_data, filename='gv_output.svg', auto_view=False, remove_source=False):
    """
    Write gv data to a file in the output directory and print it.
    If remove_source is True, delete the raw source file after SVG is rendered.
    """
    graph = graphviz.Source(gv_data)
    graph.format = 'svg'
    # Remove .svg from filename if present, graphviz adds it automatically
    if filename.endswith('.svg'):
        filename = filename[:-4]
    output_path = os.path.join('output', filename)
    svg_path = graph.render(output_path, view=auto_view)
    if remove_source and os.path.exists(output_path):
        os.remove(output_path)
    return svg_path
