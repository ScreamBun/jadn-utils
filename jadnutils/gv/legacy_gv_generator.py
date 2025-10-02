
from jadnutils.utils.consts import PRIMITIVE_TYPES, CoreType, Fields, TypeName, TypeOptions
from jadnutils.utils.jadn_utils import jadn2typestr


class LegacyGvGenerator:
    def __init__(self, schema: dict, style: dict = None):
        self.schema = schema
        self.style = style if style is not None else self.get_style()

    def generate(self, *args, **kwargs):

        gv = {}
        gv.update(self.style)
        
        assert self.src['format'] in {'graphviz'}
        assert self.src['detail'] in {'conceptual', 'logical', 'information'}
        
        fmt = {
            'graphviz': {
                'comment': '#',
                'start': 'digraph G {',
                'end': '}',
                'header': gv['header']['graphviz']
            }
        }[gv['format']]

        text = ''
        for k, v in self.schema.get('meta', {}).items():
            text += f"{fmt['comment']} {k}: {v}\n"
        text += f"\n{fmt['start']}\n  " + '\n  '.join(fmt['header']) + '\n\n'

        hide_types = [] if gv['attributes'] else (*PRIMITIVE_TYPES, 'Enumerated')
        nodes = {tdef[TypeName]: k for k, tdef in enumerate(self.schema['types']) if tdef[CoreType] not in hide_types}
        
        edges = ''
        for td in self.schema['types']:
            if (td[TypeName]) in nodes:
                bt = f' : {jadn2typestr(td[CoreType], td[TypeOptions])}' if gv['detail'] == 'information' else ''
                if td[CoreType] in PRIMITIVE_TYPES:
                    text += self.node_leaf(gv, nodes, td, bt)
                else:
                    text += self.node_start(gv, nodes, td, bt)
                    edges += self.edge_type(td)
                    for fd in td[Fields]:
                        text += self.node_field(td, fd)
                        edges += self.edge_field(td, fd)
                    text += self.node_end()
                    
        return text + edges + fmt['end']
    
    def node_leaf(gv, nodes, td, bt) -> str:
        """
        Return Leaf Type Definition in selected diagram format
        """

        tn = td[TypeName]
        return {
            'graphviz': f'n{nodes[tn]} [label=<<b>{tn}{bt}</b>>, '
                        f'shape=ellipse, style=filled, fillcolor={gv["attr_color"]}]\n\n',
        }[gv['format']]

    def node_start(gv, nodes, td, bt) -> str:
        """
        Return start of Compound Type Definition in selected diagram format
        """
        # nodes and s are available in caller scope
        tn = td[TypeName]
        color = f'fillcolor={gv["attr_color"]}, ' if td[CoreType] == 'Enumerated' else ''
        hr = '<hr/>' if gv['detail'] in {'logical', 'information'} and td[Fields] else ''
        return {
            'plantuml': f'class "{tn}{bt}" as n{nodes[tn]}\n',
            'graphviz': f'n{nodes[tn]} [{color}label=<<table cellborder="0" cellpadding="1" cellspacing="0">\n'
                        f'<tr><td cellpadding="4"><b>  {tn}{bt}  </b></td></tr>{hr}\n'
        }[gv['format']]

    def node_field(td, fd) -> str:
        """
        Return Field Definition in selected diagram format
        """
        # nodes and s are available in caller scope
        if s['detail'] == 'conceptual':
            return ''
        elif s['detail'] == 'logical':
            fval = fd[FieldName]
        elif s['detail'] == 'information':
            fl = '{field} ' if s['format'] == 'plantuml' else ''    # override PlantUML parsing parens as methods
            fname, fdef, fmult, fdesc = jadn2fielddef(fd, td)
            fdef += '' if fmult == '1' else ' [' + fmult + ']'
            fval = f'{fd[FieldID]} {fname}' + ('' if td[CoreType] == 'Enumerated' else f' : {fl}{fdef}')
        return {
            'plantuml': f'  n{nodes[td[TypeName]]} : {fval}\n',
            'graphviz': f'  <tr><td align="left">  {fval}  </td></tr>\n'
        }[s['format']]

    def node_end() -> str:
        """
        Return end of Compound Type Definition
        """
        # nodes and s are available in caller scope
        return {
            'plantuml': '\n',
            'graphviz': '</table>>]\n\n'
        }[s['format']]

    def edge_type(td) -> str:
        """
        Return graph edges from type options in selected diagram format
        """
        topts = topts_s2d(td[TypeOptions])
        k, v = topts.get('ktype', None), topts.get('vtype', None)
        edge = edge_field(td, [0, 'key', k, [], '']) if k else ''
        edge += edge_field(td, [0, 'value', v, [], '']) if v else ''
        return edge

    def edge_field(td, fd) -> str:
        """
        Return graph edges from fields in selected diagram format
        """
        # Normalize edge label for diagram format
        def ename(edge_label: str) -> str:
            return edge_label.replace('-', '_')

        # nodes and s are available in caller scope
        if td[CoreType] == 'Enumerated':
            return ''
        fopts, ftopts = ftopts_s2d(fd[FieldOptions], fd[FieldType])
        fieldtype = ftopts['vtype'] if fd[FieldType] in {'ArrayOf', 'MapOf'} else fd[FieldType]
        if fieldtype in nodes:
            mult_f = multiplicity_str(fopts)
            mult_r = '1'
            if s['format'] == 'plantuml':
                rel = ('.' if 'link_horizontal' in s else '..') if 'link' in fopts else '--'
                elabel = ' : ' + fd[FieldName] if s['edge_label'] else ''
                mult = f'"{mult_r}" {rel}> "{mult_f}"' if s['edge_mult'] else f'{rel}>'
                return f'  n{nodes[td[TypeName]]} {mult} n{nodes[fieldtype]}{elabel}\n'
            elif s['format'] == 'graphviz':
                edge = [f'label={ename(fd[FieldName])}'] if s['edge_label'] else []
                edge += ['style="dashed"'] if 'link' in fopts else []
                edge += [f'headlabel="{mult_f}", taillabel="{mult_r}"'] if s['edge_mult'] else []
                edge_label = f' [{", ".join(edge)}]' if edge else ''
                return f'  n{nodes[td[TypeName]]} -> n{nodes[fieldtype]}{edge_label}\n'
        return ''    

    def get_style() -> dict:
        # Return default generation options and style attributes
        return {
            'format': 'plantuml',       # diagram format: graphviz, plantuml
            'detail': 'conceptual',     # Level of detail: conceptual, logical, information
            'links': True,              # Show link edges (dashed)
            'link_horizontal': True,    # Use e-w links vs. n-s containers
            'edge_label': True,         # Show field name on edges
            'edge_mult': True,          # Show multiplicity on edges
            'attributes': False,        # Show node attributes connected to entities (ellipse)
            'attr_color': 'palegreen',  # Attribute ellipse fill color
            'enums': 10,                # Show Enumerated items with max count (0: none)
            'header': {
                'plantuml': [
                    '\' !theme spacelab',
                    'hide empty members',
                    'hide circle'
                ],
                'graphviz': [
                    'graph [fontname=Arial, fontsize=12];',
                    'node [fontname=Arial, fontsize=8, shape=plain, style=filled, fillcolor=lightskyblue1];',
                    'edge [fontname=Arial, fontsize=7, arrowsize=0.5, labelangle=45.0, labeldistance=0.9];',
                    'bgcolor="transparent";'
                ]
            }
        }