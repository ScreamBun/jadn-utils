import pandas as pd
from graphviz import Digraph

from jadnutils.gv.utils.gv_utils import build_basic_label, build_arrayof_label, extract_arrayof_value_type, extract_mapof_types, build_mapof_label, build_enum_label, build_choice_label, get_extends, get_restricts

class GvGenerator:

    basic_types = ["Record", "Map", "Array"]
    primitive_types = ["String", "Integer", "Binary", "Boolean", "Number"]

    def __init__(self, schema: dict, style: dict = None):
        self.schema = schema
        self.style = style if style is not None else self.get_style()
    
    # Basic is used for record, map and array    
    def build_basic_node(self, row, dot, type_label="Record", bgcolor="LightSkyBlue", shape="none"):
        fields = row["fields"]
        opts = row.get("opts", [])
        label = build_basic_label(row['name'], type_label, opts, bgcolor, fields)
        
        dot.node(row["name"], label=label, shape=shape)
            
    def build_basic_edges(self, row, dot):
        fields = row["fields"]
        opts = row.get("opts", [])
        
        for field in fields:
            if field[2] not in self.primitive_types:
                dot.edge(row["name"], field[2], label=field[1])
           
        extends = get_extends(opts)    
        if extends is not None:
            dot.edge(row["name"], extends, label="extends", style="dashed")
                
        restricts = get_restricts(opts)    
        if restricts is not None:       
            dot.edge(restricts, row["name"], label="restricts", style="dashed")                                             
                    
    def build_arrayof_node(self, row, dot, bgcolor="LightSkyBlue", shape="none"):
        opts = row.get("opts", [])
        value_type = extract_arrayof_value_type(opts) 
        label = build_arrayof_label(row["name"], value_type, opts, bgcolor)
        
        dot.node(row["name"], label=label, shape=shape)
            
    def build_arrayof_edges(self, row, dot):
        opts = row.get("opts", [])
        value_type = extract_arrayof_value_type(opts) 
        
        if value_type and not value_type in self.primitive_types:
            dot.edge(row["name"], value_type, label="element")            
    
    def build_mapof_node(self, row, dot, bgcolor="LightSkyBlue", shape="none"):
        opts = row["opts"]
        key_type, value_type = extract_mapof_types(opts)
        label = build_mapof_label(row["name"], key_type, value_type, opts, bgcolor)
        
        dot.node(row["name"], label=label, shape=shape)
            
    def build_mapof_edges(self, row, dot):
        opts = row["opts"]
        key_type, value_type = extract_mapof_types(opts)
        
        if key_type and not (hasattr(self, "primitives") and key_type in self.primitive_types):
            dot.edge(row["name"], key_type, label="key")
        if value_type and not (hasattr(self, "primitives") and value_type in self.primitive_types):
            dot.edge(row["name"], value_type, label="value")            

    def build_choice_node(self, row, dot, bgcolor="palegreen", shape="none"):
        opts = row["opts"]
        fields = row["fields"]
        label = build_choice_label(row["name"], fields, opts, bgcolor)
        
        dot.node(row["name"], label=label, shape=shape)
                
    def build_choice_edges(self, row, dot):
        opts = row["opts"]
        fields = row["fields"]
        
        for field in fields:
            if field[2] not in self.primitive_types:
                dot.edge(row["name"], field[2], label=field[1])                      
                
    def build_enum_node(self, row, dot, bgcolor="palegreen", shape="none"):
        opts = row["opts"]
        enum_items = row["fields"]
        label = build_enum_label(row["name"], enum_items, opts, bgcolor)
        dot.node(row["name"], label=label, shape=shape)                

    def generate(self, *args, **kwargs):
        schema = self.schema
        types = schema.get("types", [])
        meta = schema.get("meta", {})
        roots = meta.get("roots", [])

        # Convert types to DataFrame
        types_df = pd.DataFrame(types, columns=["name", "type", "opts", "desc", "fields"])

        dot = Digraph(comment="JADN Schema")
        dot.graph_attr.update({
            "fontname": "Arial",
            "fontsize": "12",
            "bgcolor": "white"
            # "bgcolor": "transparent"
        })
        dot.node_attr.update({
            "fontname": "Arial",
            "fontsize": "8",
            "shape": "plain",
            # "style": "filled",
            # "fillcolor": "lightskyblue1"
        })
        dot.edge_attr.update({
            "fontname": "Arial",
            "fontsize": "7",
            "arrowsize": "0.5",
            "labelangle": "45.0",
            "labeldistance": "0.9"
        })
                    
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