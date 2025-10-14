def build_choice_label(name, fields, bgcolor):
    """
    Build an HTML-like label for Choice Graphviz node.
    Args:
        name (str): Node name.
        fields (list): List of choice field tuples.
        bgcolor (str): Background color.
    Returns:
        str: HTML label string.
    """
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}: Choice</b></td></tr>
    <hr/>
    '''
    for field in fields:
        label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
    label += "</table>>"
    return label

def build_enum_label(name, enum_items, bgcolor):
    """
    Build an HTML-like label for Enumerated Graphviz node.
    Args:
        name (str): Node name.
        enum_items (list): List of enum item tuples.
        bgcolor (str): Background color.
    Returns:
        str: HTML label string.
    """
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}: Enumerated</b></td></tr>
    <hr/>
    '''
    for item in enum_items:
        label += f'<tr><td align="left">{item[0]} {item[1]}</td></tr>\n'
    label += "</table>>"
    return label

def build_mapof_label(name, key_type, value_type, bgcolor):
    """
    Build an HTML-like label for MapOf Graphviz node.
    Args:
        name (str): Node name.
        key_type (str): Key type for MapOf.
        value_type (str): Value type for MapOf.
        bgcolor (str): Background color.
    Returns:
        str: HTML label string.
    """
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}: MapOf({key_type if key_type else "?"}, {value_type if value_type else "?"})</b></td></tr>
    </table>>'''
    return label

def extract_mapof_types(opts=None):
    """
    Extract both key_type and value_type from MapOf opts.
    Args:
        opts (list): List of option strings.
    Returns:
        tuple: (key_type, value_type)
    """
    if opts is None:
        opts = []
    key_type = None
    value_type = None
    for opt in opts:
        if isinstance(opt, str):
            if opt.startswith("+"):
                key_type = opt[1:]
            elif opt.startswith("*"):
                value_type = opt[1:]
    return key_type, value_type

def extract_arrayof_value_type(opts=None):
    """
    Extract the value_type from ArrayOf opts.
    Args:
        opts (list): List of option strings.
    Returns:
        str or None: The value type if found, else None.
    """
    if opts is None:
        opts = []
    value_type = None
    for opt in opts:
        if isinstance(opt, str) and opt.startswith("*"):
            value_type = opt[1:]
    return value_type

def build_arrayof_label(name, value_type, bgcolor):
    """
    Build an HTML-like label for ArrayOf Graphviz node.
    Args:
        name (str): Node name.
        value_type (str): Value type for ArrayOf.
        bgcolor (str): Background color.
    Returns:
        str: HTML label string.
    """
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}: ArrayOf({value_type if value_type else "?"})</b></td></tr>
    </table>>'''
    return label

def build_table_label(name, type_label, bgcolor, fields = []):
    """
    Build an HTML-like label for Graphviz table node.
    Args:
        name (str): Node name.
        type_label (str): Type label.
        bgcolor (str): Background color.
    Returns:
        str: HTML label string.
    """
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}: {type_label}</b></td></tr>
    <hr/>
    '''
    for field in fields:
        label += f'<tr><td align="left">{field[0]} {field[1]}: {field[2]}</td></tr>\n'
    label += "</table>>"
    return label
