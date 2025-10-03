import pandas as pd
from graphviz import Digraph

class GvGenerator:

    def __init__(self, schema: dict, style: dict = None):
        self.schema = schema
        self.style = style if style is not None else self.get_style()

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

        # Add nodes for each type
        for _, row in types_df.iterrows():
            if row["type"] == "Record":
                fields = row["fields"]
                label = f'''<
                <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="lightskyblue1">
                <tr><td cellpadding="4"><b>{row['name']} : Record</b></td></tr>
                <hr/>
                '''
                for field in fields:
                    # field: [num, name, type, opts, desc]
                    label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
                label += "</table>>"
                dot.node(row["name"], label=label, shape="none")
            else:
                dot.node(row["name"], label=row["name"])

        # Track primitive types referenced
        primitive_types = set()

        # Add inheritance edges for types whose base is a primitive
        for _, row in types_df.iterrows():
            if row["type"] in ["String", "Integer", "Binary"]:
                dot.edge(row["name"], row["type"], label="is a")
                primitive_types.add(row["type"])

        # Add nodes for primitive types if referenced
        for ptype in primitive_types:
            dot.node(ptype, label=ptype, shape="box", style="dashed")


        # Add edges for Record types
        for _, row in types_df.iterrows():
            if row["type"] == "Record":
                for field in row["fields"]:
                    # field[2] is the referenced type
                    dot.edge(row["name"], field[2], label=field[1])

        # Map types
        for _, row in types_df.iterrows():
            if row["type"] == "Map":
                fields = row["fields"]
                if fields:
                    label = f'''<
                    <table cellborder="0" cellpadding="0" cellspacing="1" bgcolor="plum">
                    <tr><td cellpadding="4"><b>{row['name']} : Map</b></td></tr>
                    <hr/>
                    '''
                    for field in fields:
                        # field: [num, name, type, opts, desc]
                        label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
                    label += "</table>>"
                    dot.node(row["name"], label=label, shape="none")
                    
        # Array types
        for _, row in types_df.iterrows():
            if row["type"] == "Array":
                fields = row["fields"]
                if fields:
                    label = f'''<
                    <table cellborder="0" cellpadding="0" cellspacing="1" bgcolor="MediumAquamarine">
                    <tr><td cellpadding="4"><b>{row['name']} : Map</b></td></tr>
                    <hr/>
                    '''
                    for field in fields:
                        # field: [num, name, type, opts, desc]
                        label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
                    label += "</table>>"
                    dot.node(row["name"], label=label, shape="none")                   

        # Enumerated types
        for _, row in types_df.iterrows():
            if row["type"] == "Enumerated":
                enum_items = row["fields"]
                if enum_items:
                    label = f'''<
                    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="palegreen">
                    <tr><td cellpadding="4"><b>{row['name']} : Enumerated</b></td></tr>
                    <hr/>
                    '''
                    for item in enum_items:
                        # item: [num, name, ...]
                        label += f'<tr><td align="left">{item[0]} {item[1]}</td></tr>\n'
                    label += "</table>>"
                    dot.node(row["name"], label=label, shape="none")
                    
        # Choice types
        for _, row in types_df.iterrows():
            if row["type"] == "Choice":
                fields = row["fields"]
                if fields:
                    label = f'''<
                    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="lightyellow">
                    <tr><td cellpadding="4"><b>{row['name']} : Choice</b></td></tr>
                    <hr/>
                    '''
                    for field in fields:
                        # field: [num, name, type, opts, desc]
                        label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
                    label += "</table>>"
                    dot.node(row["name"], label=label, shape="none")

        # MapOf types: relabel node to show key/value types
        for _, row in types_df.iterrows():
            if row["type"] == "MapOf":
                opts = row["opts"]
                key_type = None
                value_type = None
                for opt in opts:
                    if isinstance(opt, str) and opt.startswith("+"):
                        key_type = opt[1:]
                    elif isinstance(opt, str) and opt.startswith("*"):
                        value_type = opt[1:]
                label = f'''<
                <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="SandyBrown">
                <tr><td><b>{row["name"]}: MapOf({key_type if key_type else "?"}, {value_type if value_type else "?"})</b></td></tr>
                </table>>'''
                dot.node(row["name"], label=label, shape="none")
                
        # ArrayOf types
        for _, row in types_df.iterrows():
            if row["type"] == "ArrayOf":
                opts = row["opts"]
                key_type = None
                value_type = None
                for opt in opts:
                    if isinstance(opt, str) and opt.startswith("*"):
                        value_type = opt[1:]
                label = f'''<
                <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="LightSkyBlue">
                <tr><td><b>{row["name"]}: ArrayOf({key_type if key_type else "?"}, {value_type if value_type else "?"})</b></td></tr>
                </table>>'''
                dot.node(row["name"], label=label, shape="none")          

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