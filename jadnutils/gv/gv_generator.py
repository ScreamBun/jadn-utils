import pandas as pd
from graphviz import Digraph

class GvGenerator:

    def __init__(self, schema: dict, style: dict = None):
        self.schema = schema
        self.style = style if style is not None else self.get_style()
        
    def build_primitive_nodes(self, types_df, dot):
        primitive_types = set()
        # Add inheritance edges for types whose base is a primitive
        for _, row in types_df.iterrows():
            if row["type"] in ["String", "Integer", "Binary"]:
                dot.edge(row["name"], row["type"], label="is a")
                primitive_types.add(row["type"])
        # Add nodes for primitive types if referenced
        for ptype in primitive_types:
            dot.node(ptype, label=ptype, shape="box", style="dashed")        
        
    def build_table_node(self, row, type_label, dot, bgcolor="lightskyblue1", shape="none"):
        fields = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']} : {type_label}</b></td></tr>
        <hr/>
        '''
        for field in fields:
            label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
        label += "</table>>"
        dot.node(row["name"], label=label, shape=shape)
    
    def build_arrayof_node(self, row, dot, bgcolor="LightSkyBlue", shape="none"):
        opts = row["opts"]
        key_type = None
        value_type = None
        for opt in opts:
            if isinstance(opt, str) and opt.startswith("*"):
                value_type = opt[1:]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td><b>{row["name"]}: ArrayOf({key_type if key_type else "?"}, {value_type if value_type else "?"})</b></td></tr>
        </table>>'''
        dot.node(row["name"], label=label, shape=shape)
    
    def build_mapof_node(self, row, dot, bgcolor="SandyBrown", shape="none"):
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
    
    def build_enum_node(self, row, dot, bgcolor="palegreen", shape="none"):
        enum_items = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']} : Enumerated</b></td></tr>
        <hr/>
        '''
        for item in enum_items:
            label += f'<tr><td align="left">{item[0]} {item[1]}</td></tr>\n'
        label += "</table>>"
        dot.node(row["name"], label=label, shape=shape)

    def build_choice_node(self, row, dot, bgcolor="lightyellow", shape="none"):
        fields = row["fields"]
        label = f'''<
        <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
        <tr><td cellpadding="4"><b>{row['name']} : Choice</b></td></tr>
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
        self.build_primitive_nodes(types_df, dot)
                    
        for _, row in types_df.iterrows():
            if row["type"] == "Record":
                self.build_table_node(row, "Record", dot, bgcolor="lightskyblue1", shape="none")
            elif row["type"] == "Map":
                self.build_table_node(row, "Map", dot, bgcolor="plum", shape="none")
            elif row["type"] == "Array":
                self.build_table_node(row, "Array", dot, bgcolor="MediumAquamarine", shape="none")
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
                dot.node(row["name"], label=f'{row["name"]}: {row["type"]}', shape="ellipse")        

        # Add edges for Record types
        for _, row in types_df.iterrows():
            if row["type"] == "Record":
                for field in row["fields"]:
                    # field[2] is the referenced type
                    dot.edge(row["name"], field[2], label=field[1])

        # Add logic for Array types: link to element type
        for _, row in types_df.iterrows():
            if row["type"] == "Array":
                opts = row["opts"]
                element_type = None
                # Usually, the first item in opts is the element type
                if opts and isinstance(opts[0], str):
                    # Remove any leading * or other marker
                    element_type = opts[0].lstrip("*")
                if element_type:
                    dot.edge(row["name"], element_type, label="element")

        # Add logic for ArrayOf types: link to element type
        for _, row in types_df.iterrows():
            if row["type"] == "ArrayOf":
                opts = row["opts"]
                element_type = None
                # Usually, the first item in opts is the element type
                if opts and isinstance(opts[0], str):
                    # Remove any leading * or other marker
                    element_type = opts[0].lstrip("*")
                if element_type:
                    dot.edge(row["name"], element_type, label="element")

        # Highlight root nodes
        for root in roots:
            # dot.node(root, color="red", style="filled")
            dot.node(root)

        return dot.source