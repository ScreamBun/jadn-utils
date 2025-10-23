import pandas as pd
from graphviz import Digraph

from jadnutils.gv.utils.gv_utils import build_basic_label, build_arrayof_label, extract_arrayof_value_type, extract_mapof_types, build_mapof_label, build_enumerated_label, build_choice_label, get_extends, get_restricts, get_pointer, get_enumerated, get_multiplicity_label, safe_get_field_item

class GvGenerator:

    CONCEPTUAL = 'conceptual'
    LOGICAL = 'logical'
    INFORMATION = 'information'
    GRAPH_DETAIL_OPTS = {CONCEPTUAL, LOGICAL, INFORMATION}
    
    COLOR_LIGHTSKYBLUE = 'LightSkyBlue'
    COLOR_PALEGREEN = 'Palegreen'
    
    NODE_SHAPE_NONE = 'none'
    NODE_SHAPE_PLAIN = 'plain' # rectangle
    NODE_SHAPE_ELLIPSE = 'ellipse'

    basic_types = ["Record", "Map", "Array"]
    primitive_types = ["String", "Integer", "Binary", "Boolean", "Number"]
    schema: dict = {}
    style: dict = {}

    def __init__(self, schema: dict, style: dict = None):
        self.schema = schema
        
        base_style = self.get_style()
        if style is None or style == {}:
            self.style = base_style
        else:
            # shallow merge: keys in provided style override defaults
            merged = {**base_style, **style}
            # support nested label.spacer_height: prefer style['label']['spacer_height']
            label_block = merged.get('label', {})
            if isinstance(label_block, dict) and 'spacer_height' in label_block:
                merged['label_spacer_height'] = label_block['spacer_height']
            # legacy: if 'label_spacer_height' provided directly, keep it
            self.style = merged
        
    def get_style(self) -> dict:
        return {
            'detail': self.CONCEPTUAL,  # Level of detail: conceptual, logical, information
            'show_links': True,         # Show link edges (dashed)
            'show_edge_label': True,    # Show field name on edges
            'show_edge_mult': True,     # Show multiplicity on edges
            # 'show_attributes': False,   # Show node attributes connected to entities (ellipse)
            'enums_allowed': 10,        # Show Enumerated items with max count (0: none)
            
            'graph_comment': 'JADN Schema',
            'graph_format': 'svg',  
            'graph_engine': 'dot',
            'label_spacer_height': 4,
            'link_horizontal': False,
            
            'graph_attr' : {
                'fontname': 'Arial',
                'fontsize': '12',
                'bgcolor': 'white',
                # 'bgcolor': 'transparent'
            },
            'node_attr' : {
                'fontname': 'Arial',
                'fontsize': '8',
                'shape': 'plain',
                # 'style': 'filled',
                # 'fillcolor': 'lightskyblue1'
            },
            
            'edge_attr' : {
                'fontname': 'Arial',
                'fontsize': '7',
                'arrowsize': '0.5',
                # labelangle/labeldistance removed for consistent headlabel/taillabel rendering
            },
            
            'per_type_attrs': {
                'Record': {
                    'fillcolor': self.COLOR_LIGHTSKYBLUE,
                    'shape': self.NODE_SHAPE_PLAIN
                },
                'Map': {
                    'fillcolor': self.COLOR_LIGHTSKYBLUE,
                    'shape': self.NODE_SHAPE_PLAIN
                },
                'Array': {
                    'fillcolor': self.COLOR_LIGHTSKYBLUE,
                    'shape': self.NODE_SHAPE_PLAIN
                },
                'Choice': {
                    'fillcolor': self.COLOR_LIGHTSKYBLUE,
                    'shape': self.NODE_SHAPE_PLAIN
                },
                'Enumerated': {
                    'fillcolor': self.COLOR_PALEGREEN,
                    'shape': self.NODE_SHAPE_PLAIN
                },
                'Integer': {
                    'fillcolor': self.COLOR_PALEGREEN,
                    'shape': self.NODE_SHAPE_ELLIPSE
                },
                'String': {
                    'fillcolor': self.COLOR_PALEGREEN,
                    'shape': self.NODE_SHAPE_ELLIPSE
                },
                'Binary': {    
                    'fillcolor': self.COLOR_PALEGREEN,
                    'shape': self.NODE_SHAPE_ELLIPSE
                },
                'Boolean': {
                    'fillcolor': self.COLOR_PALEGREEN,
                    'shape': self.NODE_SHAPE_ELLIPSE
                },
                'Number': {
                    'fillcolor': self.COLOR_PALEGREEN,
                    'shape': self.NODE_SHAPE_ELLIPSE
                }
            }
            
        }        
    
    def init_diagraph(self) -> Digraph:
        dot = Digraph(comment=self.style.get('graph_comment', 'JADN Schema'),
                      format=self.style.get('graph_format', 'svg'),
                      engine=self.style.get('graph_engine', 'dot'))
        
        # Apply graph attributes, and set rankdir when link_horizontal is requested
        graph_attr = {**self.style.get('graph_attr', {})}
        
        # Resolve link_horizontal preference: top-level style key wins, otherwise graph_attr may contain it
        link_horizontal = self.style.get('link_horizontal', self.style.get('graph_attr', {}).get('link_horizontal', False))
        
        # Remove any internal-only flags that shouldn't be passed to graphviz
        # (graphviz attribute values must be strings; booleans like link_horizontal
        # would raise when graphviz tries to quote them)
        graph_attr.pop('link_horizontal', None)

        if link_horizontal:
            # left-to-right layout (east-west links)
            graph_attr.setdefault('rankdir', 'LR')
            # Use spline routing for smoother, angled edges that avoid crossing node centers
            # and increase node/rank separation so edges attach outside node perimeters.
            graph_attr.setdefault('splines', 'spline')
            # spacing values chosen to give room for labels and to route lines outside node shapes
            graph_attr.setdefault('nodesep', '0.6')
            graph_attr.setdefault('ranksep', '1.0')

        dot.graph_attr.update(graph_attr)
        dot.node_attr.update(self.style.get('node_attr', {}))
        dot.edge_attr.update({**self.style.get('edge_attr', {})})

        return dot

    # Basic is used for record, map and array    
    def build_basic_node(self, row, dot, type_label="Record"):
        fields = row["fields"]
        opts = row.get("opts", [])
        # get per-type fillcolor from style, fallback to LightSkyBlue
        per_type = self.style.get('per_type_attrs', {})
        bgcolor = per_type.get(type_label, {}).get('fillcolor', self.COLOR_LIGHTSKYBLUE)
        # honor per-type shape if present, otherwise default to plain
        node_shape = per_type.get(type_label, {}).get('shape', self.NODE_SHAPE_PLAIN)

        # If the shape is plain/none, keep the table background; otherwise make the table transparent
        include_table_bg = node_shape in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE)
        spacer_height = self.style.get('label_spacer_height', None)
        label = build_basic_label(row['name'], type_label, opts, bgcolor, fields, include_table_bg, spacer_height)

        node_attrs = {'shape': node_shape}
        if node_shape not in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE):
            # put the color on the node itself so the ellipse is filled
            node_attrs['style'] = 'filled'
            node_attrs['fillcolor'] = bgcolor

        dot.node(row["name"], label=label, **node_attrs)

    def _edge(self, dot: Digraph, tail: str, head: str, **attrs):
        """Internal helper to create an edge. When link_horizontal is enabled
        attach edges to east/west ports to keep links flowing left-to-right.
        """
        link_horizontal = self.style.get('link_horizontal', self.style.get('graph_attr', {}).get('link_horizontal', False))
        if link_horizontal:
            # Spread outgoing edges from the same tail node across multiple
            # compass points so they don't all converge on a single point.
            # If caller already provided explicit ports, respect them.
            if 'tailport' not in attrs:
                # rotation list of east-side ports (right side) to distribute tails
                tail_ports = ['e', 'ne', 'se', 'n', 's']
                # initialize counter store if needed
                if not hasattr(self, '_edge_port_counters') or self._edge_port_counters is None:
                    self._edge_port_counters = {}
                count = self._edge_port_counters.get(tail, 0)
                attrs['tailport'] = tail_ports[count % len(tail_ports)]
                # increment counter for next outgoing edge from this tail
                self._edge_port_counters[tail] = count + 1
            if 'headport' not in attrs:
                # rotate incoming ports for the head node as well to avoid label collisions
                head_ports = ['w', 'nw', 'sw', 'n', 's']
                if not hasattr(self, '_edge_head_counters') or self._edge_head_counters is None:
                    self._edge_head_counters = {}
                hcount = self._edge_head_counters.get(head, 0)
                attrs['headport'] = head_ports[hcount % len(head_ports)]
                self._edge_head_counters[head] = hcount + 1
        dot.edge(tail, head, **attrs)
            
    def build_basic_edges(self, row, dot):
        fields = row["fields"]
        opts = row.get("opts", [])
        
        for field in fields:
            if field[2] not in self.primitive_types:
                field_opts = safe_get_field_item(field, 3)
                mult = get_multiplicity_label(field_opts)
                if mult:
                    self._edge(dot, row["name"], field[2], label=field[1], headlabel=mult, taillabel="1")
                else:
                    self._edge(dot, row["name"], field[2], label=field[1], taillabel="1")
           
        extends = get_extends(opts)    
        if extends != '':
            self._edge(dot, row["name"], extends, label="extends", style="dashed", taillabel="1")
                
        restricts = get_restricts(opts)    
        if restricts != '':       
            self._edge(dot, restricts, row["name"], label="restricts", style="dashed", taillabel="1")                                             
                    
    def build_arrayof_node(self, row, dot):
        opts = row.get("opts", [])
        value_type = extract_arrayof_value_type(opts)
        per_type = self.style.get('per_type_attrs', {})
        bgcolor = per_type.get('Array', {}).get('fillcolor', self.COLOR_LIGHTSKYBLUE)
        node_shape = per_type.get('Array', {}).get('shape', self.NODE_SHAPE_PLAIN)
        include_table_bg = node_shape in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE)
        spacer_height = self.style.get('label_spacer_height', None)
        label = build_arrayof_label(row["name"], value_type, opts, bgcolor, include_table_bg, spacer_height)

        node_attrs = {'shape': node_shape}
        if node_shape not in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE):
            node_attrs['style'] = 'filled'
            node_attrs['fillcolor'] = bgcolor

        dot.node(row["name"], label=label, **node_attrs)
            
    def build_arrayof_edges(self, row, dot):
        opts = row.get("opts", [])
        value_type = extract_arrayof_value_type(opts) 
        
        if value_type and not value_type in self.primitive_types:
            mult = get_multiplicity_label(opts)
            if mult:
                self._edge(dot, row["name"], value_type, label="element", headlabel=mult, taillabel="1")
            else:
                self._edge(dot, row["name"], value_type, label="element", taillabel="1")            
    
    def build_mapof_node(self, row, dot):
        opts = row["opts"]
        key_type, value_type = extract_mapof_types(opts)
        per_type = self.style.get('per_type_attrs', {})
        bgcolor = per_type.get('Map', {}).get('fillcolor', self.COLOR_LIGHTSKYBLUE)
        node_shape = per_type.get('Map', {}).get('shape', self.NODE_SHAPE_PLAIN)
        include_table_bg = node_shape in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE)
        spacer_height = self.style.get('label_spacer_height', None)
        label = build_mapof_label(row["name"], key_type, value_type, opts, bgcolor, include_table_bg, spacer_height)

        node_attrs = {'shape': node_shape}
        if node_shape not in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE):
            node_attrs['style'] = 'filled'
            node_attrs['fillcolor'] = bgcolor

        dot.node(row["name"], label=label, **node_attrs)
            
    def build_mapof_edges(self, row, dot):
        opts = row["opts"]
        key_type, value_type = extract_mapof_types(opts)
        
        mult = get_multiplicity_label(opts)
        if (key_type not in self.primitive_types):
            if mult:
                self._edge(dot, row["name"], key_type, label="key", headlabel=mult, taillabel="1")
            else:
                self._edge(dot, row["name"], key_type, label="key", taillabel="1")
            
        if (value_type not in self.primitive_types):
            if mult:
                self._edge(dot, row["name"], value_type, label="value", headlabel=mult, taillabel="1")
            else:
                self._edge(dot, row["name"], value_type, label="value", taillabel="1")            

    def build_choice_node(self, row, dot):
        opts = row["opts"]
        fields = row["fields"]
        per_type = self.style.get('per_type_attrs', {})
        bgcolor = per_type.get('Choice', {}).get('fillcolor', self.COLOR_LIGHTSKYBLUE)
        node_shape = per_type.get('Choice', {}).get('shape', self.NODE_SHAPE_PLAIN)
        include_table_bg = node_shape in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE)
        spacer_height = self.style.get('label_spacer_height', None)
        label = build_choice_label(row["name"], fields, opts, bgcolor, include_table_bg, spacer_height)

        node_attrs = {'shape': node_shape}
        if node_shape not in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE):
            node_attrs['style'] = 'filled'
            node_attrs['fillcolor'] = bgcolor

        dot.node(row["name"], label=label, **node_attrs)
                
    def build_choice_edges(self, row, dot):
        opts = row["opts"]
        fields = row["fields"]
        
        for field in fields:
            if field[2] not in self.primitive_types:
                field_opts = safe_get_field_item(field, 3)
                mult = get_multiplicity_label(field_opts)
                if mult:
                    self._edge(dot, row["name"], field[2], label=field[1], headlabel=mult, taillabel="1")
                else:
                    self._edge(dot, row["name"], field[2], label=field[1], taillabel="1")                      
                
    def build_enum_node(self, row, dot):
        opts = row["opts"]
        enum_items = row["fields"]
        per_type = self.style.get('per_type_attrs', {})
        bgcolor = per_type.get('Enumerated', {}).get('fillcolor', self.COLOR_PALEGREEN)
        node_shape = per_type.get('Enumerated', {}).get('shape', self.NODE_SHAPE_PLAIN)
        include_table_bg = node_shape in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE)
        spacer_height = self.style.get('label_spacer_height', None)
        label = build_enumerated_label(row["name"], enum_items, opts, bgcolor, include_table_bg, spacer_height)

        node_attrs = {'shape': node_shape}
        if node_shape not in (self.NODE_SHAPE_PLAIN, self.NODE_SHAPE_NONE):
            node_attrs['style'] = 'filled'
            node_attrs['fillcolor'] = bgcolor

        dot.node(row["name"], label=label, **node_attrs)

        pointer = get_pointer(opts)
        if pointer != '':       
            self._edge(dot, row["name"], pointer, label="pointer", style="dashed", taillabel="1")
            
        enumerated = get_enumerated(opts)
        if enumerated != '':       
            self._edge(dot, row["name"], enumerated, label="enumerated", style="dashed", taillabel="1")                                

    def generate(self, *args, **kwargs):
        schema = self.schema
        types = schema.get("types", [])
        meta = schema.get("meta", {})
        roots = meta.get("roots", [])
        # Convert types to DataFrame
        types_df = pd.DataFrame(types, columns=["name", "type", "opts", "desc", "fields"])

        # Reset any per-generate edge port counters so attachment distribution
        # is deterministic for each generated graph.
        self._edge_port_counters = {}
        self._edge_head_counters = {}

        dot = self.init_diagraph()

        # Build Nodes
        for root in roots:
            dot.node(root)

        for _, row in types_df.iterrows():
            if row["type"] in self.basic_types:
                self.build_basic_node(row, dot, type_label=row["type"])
            elif row["type"] == "Enumerated":
                self.build_enum_node(row, dot)
            elif row["type"] == "Choice":
                self.build_choice_node(row, dot)
            elif row["type"] == "ArrayOf":
                self.build_arrayof_node(row, dot)
            elif row["type"] == "MapOf":
                self.build_mapof_node(row, dot)
            else:
                dot.node(row["name"], label=f'{row["name"]}: {row["type"]}', shape="ellipse", style="filled", fillcolor="palegreen")

        # Build Edges
        for _, row in types_df.iterrows():
            if row["type"] in self.basic_types:
                self.build_basic_edges(row, dot)
            elif row["type"] == "Choice":
                self.build_choice_edges(row, dot)
            elif row["type"] == "ArrayOf":
                self.build_arrayof_edges(row, dot)
            elif row["type"] == "MapOf":
                self.build_mapof_edges(row, dot)
            else:
                pass

        return dot.source