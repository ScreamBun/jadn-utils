from jadnutils.utils.options import TYPE_OPTIONS

def get_type_opts(opts):
    """
    Extract option names from opts using TYPE_OPTIONS, return as comma-delimited string.
    Args:
        opts (list): List of option strings.
    Returns:
        str: Comma-delimited option names.
    """
    opts_found = []
    for opt in opts:
        if isinstance(opt, str) and opt in TYPE_OPTIONS and (opt.isalpha() or opt == "="):
            opts_found.append(TYPE_OPTIONS[opt]['name'])
    return ', '.join(opts_found)

def get_extends(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('e'):
            return opt[1:]
    return None

def get_restricts(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('r'):
            return opt[1:]
    return None

def get_enumerated(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('#'):
            return opt[1:]
    return None

def get_pointer(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('>'):
            return opt[1:]
    return None

def get_min_max_length(opts):
    minLength = None
    maxLength = None
    
    for opt in opts:
        if isinstance(opt, str):
            if opt.startswith("{"):
                num = opt[1:]
                minLength = num if num.isdigit() else "0"
            elif opt.startswith("}"):
                num = opt[1:]
                maxLength = num if num.isdigit() else "*"
                
    if minLength is None:
        minLength = "0"
        
    if maxLength is None:
        maxLength = "*"
        
    return f"{{{minLength}..{maxLength}}}"
    # return f"{minLength}..{maxLength}"

def build_choice_label(name, fields, opts, bgcolor):
    type_opts = get_type_opts(opts)
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}</b>: Choice {type_opts}</td></tr>
    <hr/>
    '''
    for field in fields:
        label += f'<tr><td align="left">{field[0]} {field[1]} : {field[2]}</td></tr>\n'
    label += "</table>>"
    return label

def build_enum_label(name, enum_items, opts, bgcolor):
    type_opts = get_type_opts(opts)
    pointer_type = get_pointer(opts)
    enumerated_type = get_enumerated(opts)
    
    pointer_str = ''
    if pointer_type is not None:
        pointer_str = f'(pointing to {pointer_type})'
        
    enumerated_str = ''
    if enumerated_type is not None:
        enumerated_str = f'(enumerated by {enumerated_type})'        
    
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}</b>: Enumerated {type_opts} {pointer_str} {enumerated_str}</td></tr>
    '''
    
    if not pointer_type and not enumerated_type:
        label += "<hr/>\n"
        for item in enum_items:
            label += f'<tr><td align="left">{item[0]} {item[1]}</td></tr>\n'
    label += "</table>>\n"
        
    return label

def build_mapof_label(name, key_type, value_type, opts, bgcolor):
    min_max_len = get_min_max_length(opts)
    type_opts = get_type_opts(opts)    
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}</b>: MapOf({key_type if key_type else "?"}, {value_type if value_type else "?"}) {min_max_len} {type_opts}</td></tr>
    </table>>'''
    return label

def extract_mapof_types(opts=None):
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
    if opts is None:
        opts = []
    value_type = None
    for opt in opts:
        if isinstance(opt, str) and opt.startswith("*"):
            value_type = opt[1:]
    return value_type

def build_arrayof_label(name, value_type, opts, bgcolor):
    min_max_len = get_min_max_length(opts)
    type_opts = get_type_opts(opts)
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}</b>: ArrayOf({value_type if value_type else "?"}) {min_max_len} {type_opts}</td></tr>
    </table>>'''
    return label

# Used by record, map, array
def build_basic_label(name, type_label, opts, bgcolor, fields = []):
    min_max_len = get_min_max_length(opts)
    type_opts = get_type_opts(opts)
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}</b>: {type_label} {min_max_len} {type_opts}</td></tr>
    <hr/>
    '''
    for field in fields:
        label += f'<tr><td align="left">{field[0]} {field[1]}: {field[2]}</td></tr>\n'
    label += "</table>>"
    return label
