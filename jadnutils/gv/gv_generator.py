import pandas as pd
from graphviz import Digraph

class GvGenerator:

    primitives = ["String", "Integer", "Binary", "Boolean", "Number"]

    def __init__(self, schema: dict, style: dict = None):
        self.schema = schema
        self.style = style if style is not None else self.get_style()
        
    def build_primitive_edge(self, node_name, primitive_type, dot, label="is a"):
        """
        Create an edge from node_name to a primitive type.
        Args:
            node_name (str): The name of the node.
            primitive_type (str): The primitive type to link to.
            dot (Digraph): The graphviz Digraph object.
            label (str): The label for the edge (default: "is a").
        """
        dot.edge(node_name, primitive_type, label=label)        
        
    # TODO: Move these into a separate file/class
    def build_primitive_nodes(self, types_df, dot):
        primitive_types = set()
        # Add inheritance edges for types whose base is a primitive
        for _, row in types_df.iterrows():
            if row["type"] in self.primitives:
                dot.edge(row["name"], row["type"], label="is a")
                primitive_types.add(row["type"])
        # Add nodes for primitive types if referenced
        # for ptype in primitive_types:
        #     dot.node(ptype, label=ptype, shape="ellipse", style="filled", fillcolor="palegreen")        
        
    def build_record_node(self, row, type_label, dot, bgcolor="LightSkyBlue", shape="none"):
        fields = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']}: {type_label}</b></td></tr>
        <hr/>
        '''
        for field in fields:
            label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
        label += "</table>>"
        dot.node(row["name"], label=label, shape=shape)
        
        for field in fields:
            # if referenced type build connection edges
            if field[2] not in self.primitives:
                dot.edge(row["name"], field[2], label=field[1])     
                
    def build_map_node(self, row, type_label, dot, bgcolor="LightSkyBlue", shape="none"):
        fields = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']}: {type_label}</b></td></tr>
        <hr/>
        '''
        for field in fields:
            label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
        label += "</table>>"
        dot.node(row["name"], label=label, shape=shape)
        
        for field in fields:
            # if referenced type build connection edges
            if field[2] not in self.primitives:
                dot.edge(row["name"], field[2], label=field[1])                  
                
    def build_array_node(self, row, type_label, dot, bgcolor="LightSkyBlue", shape="none"):
        fields = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']}: {type_label}</b></td></tr>
        <hr/>
        '''
        for field in fields:
            label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
        label += "</table>>"
        dot.node(row["name"], label=label, shape=shape)
        
        for field in fields:
            # if referenced type build connection edges
            if field[2] not in self.primitives:
                dot.edge(row["name"], field[2], label=field[1])                                  
                    
    def build_arrayof_node(self, row, dot, bgcolor="LightSkyBlue", shape="none"):
        opts = row["opts"]
        value_type = None
        
        for opt in opts:
            if isinstance(opt, str) and opt.startswith("*"):
                value_type = opt[1:]
                
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td><b>{row["name"]}: ArrayOf({value_type if value_type else "?"})</b></td></tr>
        </table>>'''
        
        dot.node(row["name"], label=label, shape=shape)
        
        if value_type and not (hasattr(self, "primitives") and value_type in self.primitives):
            dot.edge(row["name"], value_type, label="element")        
    
    def build_mapof_node(self, row, dot, bgcolor="LightSkyBlue", shape="none"):
        opts = row["opts"]
        key_type = None
        value_type = None
        
        for opt in opts:
            if isinstance(opt, str) and opt.startswith("+"):
                key_type = opt[1:]
            elif isinstance(opt, str) and opt.startswith("*"):
                value_type = opt[1:]
                
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td><b>{row["name"]}: MapOf({key_type if key_type else "?"}, {value_type if value_type else "?"})</b></td></tr>
        </table>>'''
        
        dot.node(row["name"], label=label, shape=shape)
        
        if key_type and not (hasattr(self, "primitives") and key_type in self.primitives):
            dot.edge(row["name"], key_type, label="key")
        if value_type and not (hasattr(self, "primitives") and value_type in self.primitives):
            dot.edge(row["name"], value_type, label="value")          
    
    def build_enum_node(self, row, dot, bgcolor="palegreen", shape="none"):
        enum_items = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']}: Enumerated</b></td></tr>
        <hr/>
        '''
        for item in enum_items:
            label += f'<tr><td align="left">{item[0]} {item[1]}</td></tr>\n'
        label += "</table>>"
        dot.node(row["name"], label=label, shape=shape)

    # TODO: Choice could have ref types as well
    def build_choice_node(self, row, dot, bgcolor="palegreen", shape="none"):
        fields = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']}: Choice</b></td></tr>
        <hr/>
        '''
        for field in fields:
            label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
        label += "</table>>"
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

        # Build primitive type nodes and edges
        # self.build_primitive_nodes(types_df, dot)
                    
        for _, row in types_df.iterrows():
            if row["type"] == "Record":
                self.build_record_node(row, "Record", dot, shape="none")
            elif row["type"] == "Map":
                self.build_map_node(row, "Map", dot, shape="none")
            elif row["type"] == "Array":
                self.build_array_node(row, "Array", dot, shape="none")
            elif row["type"] == "Enumerated":
                self.build_enum_node(row, dot)
            elif row["type"] == "Choice":
                self.build_choice_node(row, dot)
            elif row["type"] == "ArrayOf":
                self.build_arrayof_node(row, dot)
            elif row["type"] == "MapOf":
                self.build_mapof_node(row, dot)
            else:
                # For other types, just create a simple node
                dot.node(row["name"], label=f'{row["name"]}: {row["type"]}', shape="ellipse", style="filled", fillcolor="palegreen")        

        # Add logic for Array types: link to element type, skip if primitive
        # for _, row in types_df.iterrows():
        #     if row["type"] == "Array":
        #         opts = row["opts"]
        #         element_type = None
        #         # Usually, the first item in opts is the element type
        #         if opts and isinstance(opts[0], str):
        #             # Remove any leading * or other marker
        #             element_type = opts[0].lstrip("*")
        #         if element_type and not (hasattr(self, "primitives") and element_type in self.primitives):
        #             dot.edge(row["name"], element_type, label="element")

        # Add logic for ArrayOf types: link to element type, skip if primitive
        # for _, row in types_df.iterrows():
        #     if row["type"] == "ArrayOf":
        #         opts = row["opts"]
        #         element_type = None
        #         # Usually, the first item in opts is the element type
        #         if opts and isinstance(opts[0], str):
        #             # Remove any leading * or other marker
        #             element_type = opts[0].lstrip("*")
        #         if element_type and not (hasattr(self, "primitives") and element_type in self.primitives):
        #             dot.edge(row["name"], element_type, label="element")
                    
        # Add logic for MapOf types: link to key and value types, skip if primitive
        # for _, row in types_df.iterrows():
        #     if row["type"] == "MapOf":
        #         opts = row["opts"]
        #         key_type = None
        #         value_type = None
        #         for opt in opts:
        #             if isinstance(opt, str) and opt.startswith("+"):
        #                 key_type = opt[1:]
        #             elif isinstance(opt, str) and opt.startswith("*"):
        #                 value_type = opt[1:]
        #         if key_type and not (hasattr(self, "primitives") and key_type in self.primitives):
        #             dot.edge(row["name"], key_type, label="key")
        #         if value_type and not (hasattr(self, "primitives") and value_type in self.primitives):
        #             dot.edge(row["name"], value_type, label="value")                    

        # Highlight root nodes
        for root in roots:
            dot.node(root)

        return dot.source