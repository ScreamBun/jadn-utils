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

        # Add nodes for each type
        for _, row in types_df.iterrows():
            dot.node(row["name"], label=row["name"])

        # Add edges for Record types
        for _, row in types_df.iterrows():
            if row["type"] == "Record":
                for field in row["fields"]:
                    # field[2] is the referenced type
                    dot.edge(row["name"], field[2], label=field[1])

        # Highlight root nodes
        for root in roots:
            dot.node(root, color="red", style="filled")

        return dot.source