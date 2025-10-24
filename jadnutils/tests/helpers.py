import re


def parse_edge_attrs(edge_attr_str: str) -> dict:
    """Parse a Graphviz edge attribute list (contents inside [...]) into a dict.

    Example input: 'label=field1 headlabel=1 taillabel=1'
    Returns: {'label': 'field1', 'headlabel': '1', 'taillabel': '1'}

    Notes:
    - Handles unquoted and quoted values ("value" or value).
    - Returns values as raw strings (no un-escaping beyond stripping surrounding quotes).
    """
    attrs = {}
    if edge_attr_str is None:
        return attrs

    # Regex to match key=value where value may be quoted or unquoted. Allows hyphens/underscores in keys.
    token_re = re.compile(r"(?P<key>[A-Za-z_][-A-Za-z0-9_]*)\s*=\s*(?:\"(?P<qval>.*?)\"|(?P<val>[^\s,]+))")
    for m in token_re.finditer(edge_attr_str):
        key = m.group('key')
        val = m.group('qval') if m.group('qval') is not None else m.group('val')
        attrs[key] = val

    return attrs


def find_edge_attr_block(dot_source: str, tail: str, head: str) -> str | None:
    """Return the attribute block string for the first matching edge `tail -> head` or None.

    Example match: A -> B [label=field1 taillabel=1]
    Returns the content inside the brackets: 'label=field1 taillabel=1'
    """
    m = re.search(rf"{re.escape(tail)}\s*->\s*{re.escape(head)}\s*\[([^\]]*)\]", dot_source)
    if not m:
        return None
    return m.group(1)
