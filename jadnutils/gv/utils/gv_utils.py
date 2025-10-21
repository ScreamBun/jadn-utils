from jadnutils.utils.options import CHOICE_OPTIONS, FIELD_OPTIONS, TYPE_OPTIONS

# Need to add:
# - edge headlabels and taillabels for field options
# - display options
# - css styling options 


def append_fields_to_label(label, fields):
    """
    Appends field rows to the label for each field in fields.
    Returns the updated label string.
    """
    for field in fields:
        field_id = safe_get_field_item(field, 0)
        field_name = safe_get_field_item(field, 1)
        field_type = safe_get_field_item(field, 2)
        field_opts = safe_get_field_item(field, 3)
        type_opts = get_type_opts(field_opts)
        field_flag_opts = get_field_opts(field_opts)
        field_min_max_occurs = get_min_max_occurs(field_opts)
        field_min_max_length = get_min_max_length(field_opts)
        field_min_max_inclusive = get_min_max_inclusive(field_opts)
        field_min_max_exclusive = get_min_max_exclusive(field_opts)
        field_format_opt = get_format(field_opts)
        opts_str = array_to_comma_str(type_opts, field_flag_opts, field_format_opt)
        label += f'<tr><td align="left">{field_id} {field_name}: {field_type} {field_min_max_occurs} {field_min_max_length} {field_min_max_inclusive} {field_min_max_exclusive} {opts_str}</td></tr>\n'
    return label

def safe_get_field_item(field, idx):
    """
    Safely get item at index `idx` from `field` (list/tuple). Returns [] if not available.
    """
    if isinstance(field, (list, tuple)) and len(field) > idx:
        return field[idx]
    return []

def array_to_comma_str(arr, extra_list=None, *extra):
    """
    Converts an array of strings to a comma-delimited string.
    Appends any additional strings provided as arguments, and a second list if given.
    Returns an empty string if input is not a list/tuple or is empty.
    """
    items = []
    if isinstance(arr, (list, tuple)):
        items.extend(str(item) for item in arr)
    if extra_list and isinstance(extra_list, (list, tuple)):
        items.extend(str(item) for item in extra_list)
    items.extend(str(e) for e in extra if e)
    return ', '.join(items)

def get_type_opts(opts):
    opts_found = []
    for opt in opts:
        if (
            isinstance(opt, str)
            and opt in TYPE_OPTIONS
            and (opt.isalpha() or opt == "=")
            and opt != "C"
            and opt != "w"
            and opt != "x"
            and opt != "y"
            and opt != "z"
        ):
            opts_found.append(TYPE_OPTIONS[opt]['name'])
    return opts_found

def get_field_opts(opts):
    opts_found = []
    for opt in opts:
        if (
            isinstance(opt, str)
            and opt in FIELD_OPTIONS
            and (opt.isalpha() or opt == "<")
        ):
            opts_found.append(FIELD_OPTIONS[opt]['name'])
    return opts_found

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

# w, x
def get_min_max_inclusive(opts):
    min = ''
    max = ''
    
    for opt in opts:
        if isinstance(opt, str):
            if opt.startswith("w"):
                num = opt[1:]
                min = num if num.isdigit() else "1"
            elif opt.startswith("x"):
                num = opt[1:]
                max = num if num.isdigit() else "*"
                
    # If neither bound present, return empty
    if min == '' and max == '':
        return ''

    parts = []
    if min:
        parts.append(f"&gt;={min}")
    if max:
        parts.append(f"&lt;={max}")

    return "{" + " and ".join(parts) + "}"

# y, z
def get_min_max_exclusive(opts):
    min = ''
    max = ''
    
    for opt in opts:
        if isinstance(opt, str):
            if opt.startswith("y"):
                num = opt[1:]
                min = num if num.isdigit() else "1"
            elif opt.startswith("z"):
                num = opt[1:]
                max = num if num.isdigit() else "*"
                
    # If neither bound present, return empty
    if min == '' and max == '':
        return ''

    parts = []
    if min:
        parts.append(f"&gt;{min}")
    if max:
        parts.append(f"&lt;{max}")

    # Join with ' and ' when both present
    return "{" + " and ".join(parts) + "}"

def get_multiplicity_label(opts):
    """
    Return the best multiplicity string for the given opts.
    Priority: exclusive -> inclusive -> occurs -> length.
    Returns '' when no multiplicity found.
    """
    if not opts:
        return ''
    for fn in (get_min_max_exclusive, get_min_max_inclusive, get_min_max_occurs, get_min_max_length):
        try:
            s = fn(opts)
        except Exception:
            s = ''
        if s:
            return s
    return ''

def build_choice_label(name, fields, opts, bgcolor):
    type_opts = get_type_opts(opts)
    combine_opt = get_combine(opts)
    combine_str = f'Combine {combine_opt}' if combine_opt else ''
    opts_str = array_to_comma_str(type_opts, combine_str)
    
    label = f'''<
    <table cellborder="0" cellpadding="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}:</b> Choice</td></tr>
    '''
    
    if opts_str:
        label += f'<tr><td>Options: {opts_str}</td></tr>\n'
        
    if fields:
        label += '<hr/>'
        label = append_fields_to_label(label, fields)
        
    label += "</table>>"
    
    return label

def build_enumerated_label(name, enum_items, opts, bgcolor):
    type_opts = get_type_opts(opts)
    pointer_type = get_pointer(opts)
    enumerated_type = get_enumerated(opts)
    
    pointer_str = ''
    if pointer_type is not '':
        pointer_str = f'pointing to {pointer_type}'
        
    enumerated_str = ''
    if enumerated_type is not '':
        enumerated_str = f'enumerated by {enumerated_type}'
        
    opts_str = array_to_comma_str(type_opts, pointer_str, enumerated_str)        
    
    label = f'''<
    <table cellborder="0" cellpadding="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}:</b> Enumerated</td></tr>
    '''
    
    if opts_str:
        label += f'<tr><td>Options: {opts_str}</td></tr>\n'    
    
    if not pointer_type and not enumerated_type:
        label += "<hr/>\n"
        for item in enum_items:
            label += f'<tr><td align="left">{item[0]} {item[1]}</td></tr>\n'
    label += "</table>>\n"
        
    return label

def build_mapof_label(name, key_type, value_type, opts, bgcolor):
    min_max_len = get_min_max_length(opts)
    type_opts = get_type_opts(opts)
    opts_str = array_to_comma_str(type_opts)
    
    label = f'''<
    <table cellborder="0" cellpadding="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}:</b> MapOf({key_type if key_type else "?"}, {value_type if value_type else "?"}) {min_max_len}</td></tr>
    '''
    
    if opts_str:
        label += f'<tr><td>Options: {opts_str}</td></tr>\n'        
        
    label += "</table>>\n"
    
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
    opts_str = array_to_comma_str(type_opts)
    
    label = f'''<
    <table cellborder="0" cellpadding="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}:</b> ArrayOf({value_type if value_type else "?"}) {min_max_len}</td></tr>
    '''
    
    if opts_str:
        label += f'<tr><td>Options: {opts_str}</td></tr>\n'      
        
    label += "</table>>\n"        
    
    return label

# Used by record, map, array
def build_basic_label(name, type_label, opts, bgcolor, fields = []):
    min_max_len = get_min_max_length(opts)
    type_opts = get_type_opts(opts)
    format_opt = get_format(opts)
    opts_str = array_to_comma_str(type_opts, format_opt)
    
    label = f'''<
    <table cellborder="0" cellpadding="1" bgcolor="{bgcolor}">
    <tr><td><b>{name}:</b> {type_label} {min_max_len}</td></tr>
    '''
    
    if opts_str:
        label += f'<tr><td>Options: {opts_str}</td></tr>\n'
        
    if fields:
        label += '<hr/>'
        label = append_fields_to_label(label, fields)
        
    label += "</table>>"
    
    return label
