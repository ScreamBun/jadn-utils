from jadnutils.utils.options import CHOICE_OPTIONS, TYPE_OPTIONS

def get_type_opts(opts):
    opts_found = []
    for opt in opts:
        if (
            isinstance(opt, str)
            and opt in TYPE_OPTIONS
            and (opt.isalpha() or opt == "=")
            and opt != "C"
        ):
            opts_found.append(TYPE_OPTIONS[opt]['name'])
    return ', '.join(opts_found)

def get_combine(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('C'):
            if len(opt) > 1:
                key = opt[1]
                return CHOICE_OPTIONS.get(key)
    return ''

def get_extends(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('e'):
            return opt[1:]
    return ''

def get_restricts(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('r'):
            return opt[1:]
    return ''

def get_enumerated(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('#'):
            return opt[1:]
    return ''

def get_pointer(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('>'):
            return opt[1:]
    return ''

def get_format(opts):
    for opt in opts:
        if isinstance(opt, str) and opt.startswith('/'):
            return opt[1:]
    return ''

def get_min_max_length(opts):
    min_length = ''
    max_length = ''
    
    for opt in opts:
        if isinstance(opt, str):
            if opt.startswith("{"):
                num = opt[1:]
                min_length = num if num.isdigit() else "1"
            elif opt.startswith("}"):
                num = opt[1:]
                max_length = num if num.isdigit() else "*"
                
    if min_length == '' and max_length == '':
        return ''
        
    if max_length is '':
        max_length = "*"
        
    return f"{{{min_length}..{max_length}}}"
    
def get_min_max_occurs(opts):
    min_occurs = ''
    max_occurs = ''
    
    for opt in opts:
        if isinstance(opt, str):
            if opt.startswith("["):
                num = opt[1:]
                min_occurs = num if num.isdigit() else "1"
            elif opt.startswith("]"):
                num = opt[1:]
                max_occurs = num if num.isdigit() else "*"
                
    if min_occurs == '' and max_occurs == '':
        return ''
    
    if max_occurs is '':
        max_occurs = "*"
        
    return f"[{min_occurs}..{max_occurs}]"

def build_choice_label(name, fields, opts, bgcolor):
    type_opts = get_type_opts(opts)
    combine_opt = get_combine(opts)
    combine_str = f'(Combine {combine_opt})' if combine_opt else ''
    
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}</b>: Choice {type_opts} {combine_str}</td></tr>
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
    if pointer_type is not '':
        pointer_str = f'(pointing to {pointer_type})'
        
    enumerated_str = ''
    if enumerated_type is not '':
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
    format_opt = get_format(opts)
    label = f'''<
    <table cellborder="0" cellpadding="1" cellspacing="1" bgcolor="{bgcolor}">
    <tr><td cellpadding="4"><b>{name}</b>: {type_label} {min_max_len} {type_opts} {format_opt}</td></tr>
    <hr/>
    '''
    for field in fields:
        field_min_max_occurs = get_min_max_occurs(field[3])
        label += f'<tr><td align="left">{field[0]} {field[1]}: {field[2]} {field_min_max_occurs}</td></tr>\n'
    label += "</table>>"
    return label
