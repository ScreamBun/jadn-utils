from typing import Union
from jadnutils.utils.consts import MAX_DEFAULT, MAX_UNLIMITED, OPTION_ID, OPTION_TYPES, SELECTOR_TYPES, STRUCTURED_TYPES, TYPE_OPTIONS, CORE_TYPES


def get_title(data):
    """
    Get the title from data['meta']['title'], or return 'JADN Schema' if missing.
    """
    try:
        return data.get('meta', {}).get('title', 'JADN Schema')
    except Exception:
        return 'JADN Schema'

def get_type(j_type):
    """
    Get the type from a type definition.
    
    j_type is the type definition list
    """
    if not isinstance(j_type, list):
        return None
    if isinstance(j_type[0], str):
        return j_type[1]
    elif isinstance(j_type[1], str):
        return j_type[2]
    else:
        return None

def get_children(j_type):
    """
    Get the children from a j_type definition.
    
    j_type is the type definition list
    """
    if not isinstance(j_type, list):
        return None
    if isinstance(j_type[0], str) and len(j_type) > 4:
        return j_type[4]
    else:
        return []

def get_parent(jadn_types, field):
    """
    Get the parent type definition of a given field.
    """
    field_name = field[0] if isinstance(field[0], str) else field[1]
    for type_def in jadn_types:
        children = get_children(type_def)
        for child in children:
            if child[1] == field_name:
                return type_def
    return None

def get_options(type_or_field):
    """
    Get the options from a type or field definition.
    """
    if not isinstance(type_or_field, list):
        return None
    if isinstance(type_or_field[0], str):
        return type_or_field[2]
    elif isinstance(type_or_field[1], str) and len(type_or_field) > 3:
        return type_or_field[3]
    else:
        return []

def get_type_by_name(jadn_types, name):
    """
    Retrieve a type definition by its name from jadn_types
    
    jadn_types is the list of all JADN type definitions
    name is the name of the type definition to retrieve
    
    """
    for type_def in jadn_types:
        if type_def[0] == name:
            return type_def
    return None

def get_inherited_fields(jadn_types, j_type, j_fields):
    """
    Retrieve all inherited fields for a given type definition
    
    jadn_types is the list of all JADN type definitions
    j_type is the type definition to check for inheritance
    j_fields is the current list of fields to which inherited fields will be added
    
    """
    parent = [opt for opt in get_options(j_type) if opt.startswith('e') or opt.startswith('r')]

    if parent and isinstance(parent, list):
        clean_parent = parent[0][1:]
        opt = parent[0][0]

        parent_field = get_type_by_name(jadn_types, clean_parent)
        if parent_field:
            children = get_children(parent_field)

            if opt == 'e':  # extends
                for child in children:
                    idx = child[0]
                    if idx not in [f[0] for f in j_fields]:
                        # overwrite fields
                        j_fields.append(child)
            elif opt == 'r':  # restricts
                # Filter inherited fields so that new fields aren't added
                updated_fields = []
                for inherited_field in j_fields:
                    idx = inherited_field[0]
                    if idx in [f[0] for f in children]:
                        updated_fields.append(inherited_field)
                j_fields = sorted(updated_fields, key=lambda x: x[0])

                # Normal overwrite logic
                for child in children:
                    idx = child[0]
                    if idx not in [f[0] for f in j_fields]:
                        # overwrite fields
                        j_fields.append(child)

            grandparent = [opt for opt in get_options(parent_field) if opt.startswith('e') or opt.startswith('r')]

            if grandparent and isinstance(grandparent, list) and len(grandparent) > 0:
                j_fields.extend(get_inherited_fields(jadn_types, parent_field, j_fields))
   
    dedup = {}
    for f in j_fields:
        dedup[f[0]] = f
    return sorted(list(dedup.values()), key=lambda x: x[0])

def get_key_from_link(jadn_types, link_field):
    """
    Retrive the key field def given its parent
    """
    if not jadn_types or not link_field:
        raise ValueError("Error during key/link processing. One or more args is None.")
    
    parent = get_type(link_field)
    parent_type_def = get_type_by_name(jadn_types, parent)
    fields = get_children(parent_type_def) or []
    for field in fields:
        options = get_options(field)
        if options and any(opt for opt in options if opt == "K"):
            new_opts = [opt for opt in get_options(link_field) if opt != "K"]
            link_field[3] = new_opts
            link_field[2] = get_type(field)
            return link_field
    return link_field

def has_key_link(type_def):
    """
    Determine if a type definition has a key/link field
    """
    if not type_def:
        raise ValueError("Error during key/link processing. Type definition is None.")
    
    children = get_children(type_def)
    hasKey = False
    hasLink = False
    for field in children:
        options = get_options(field)
        if options and any(opt for opt in options if opt == "K"):
            hasKey = True
        if options and any(opt for opt in options if opt == "L"):
            hasLink = True
    if hasKey and hasLink:
        return True
    return False

def handle_mapof_enum_key(jadn_types, mapof_type_def, key_type_def, value_type):
    """
    A Mapof with an enum key becomes a Map with field names from the enum values and type of value type
    """
    if not jadn_types or not mapof_type_def or not key_type_def or not value_type:
        raise ValueError("Error during MapOf enum key processing. One or more args is None.")

    try:
        map_fields = []
        field_names = [child[1] for child in get_children(key_type_def)]
        for idx, name in enumerate(field_names):
            field_def = [idx, name, value_type, ["[0"], ""]
            map_fields.append(field_def)
        
        map_type_def = [mapof_type_def[0], "Map", [], mapof_type_def[3], map_fields]
        return map_type_def
    except Exception as e:
        raise ValueError(f"Error during MapOf enum key processing: {e}")

def get_field_by_data(jadn_types, data):
    """
    Retrive a field definition by its data from jadn_types
    """
    if isinstance(data, dict):
        field_names = set(data.keys())
        try:
            field_values = set(data.values())
        except TypeError as e:
            field_values = []
    elif isinstance(data, list):
        field_names = [get_field_by_data(jadn_types, item) for item in data]
    else:
        field_values = [data]
        field_names = []

    for jadn_type in jadn_types:
        found = True
        children = list(get_children(jadn_type) or [])
        handleInheritance = len([opt for opt in get_options(jadn_type) if opt.startswith('e') or opt.startswith('r')]) > 0
        if handleInheritance: 
            children = get_inherited_fields(jadn_types, jadn_type, children)
        if children and isinstance(children, list) and len(children) > 0 and not isinstance(children[0], list):
            children = [children]
        if not children:
            continue

        true_type_def = get_true_type_def(jadn_types, jadn_type)

        # Account for Enumerated
        if children and len(children) > 0 and isinstance(children[0], list) and len(children[0]) == 3 and len(field_values) == 1:
            if "=" in get_options(true_type_def): # Account for ID opt
                children_names = [child[0] for child in children]
            else:
                children_names = [child[1] for child in children]
            for val in field_values:
                if val in children_names:
                    return jadn_type

        # Account for Choice
        if get_type(true_type_def) == "Choice":
            if "=" in get_options(true_type_def): # Account for ID opt
                children_names = [str(child[0]) for child in children]
            else:
                children_names = [child[1] for child in children]
            for name in field_names:
                if name in children_names:
                    return jadn_type

        # Account for special ipvnet Array case
        if get_type(true_type_def) == "Array" and ("/ipv4-net" in get_options(true_type_def) or "/ipv6-net" in get_options(true_type_def)):
            if true_type_def[0] in field_names:
                return jadn_type
                
        found_count = 0
        opt_count = 0
        for field in children:
            if field[1] in field_names:
                found_count += 1
                if len(field) > 3 and "[0" in field[3]:
                    opt_count -= 1
            if len(field) > 3 and "[0" in field[3]:
                opt_count += 1
            if field[1] not in field_names and ("[0" not in get_options(field)):
                found = False
                break
        if found and found_count + opt_count == len(field_names) + opt_count:
            return jadn_type
    return None

def get_true_type_def(jadn_types, field):
    """
    Retrieve the true type of a JADN type definition, resolving any type references.
    """
    field_type = get_type(field)
    if field_type in CORE_TYPES:
        return field
    
    type_def = get_type_by_name(jadn_types, field_type)

    if not type_def:
        return field

    if get_type(type_def) in CORE_TYPES:
        return type_def
    
    return get_true_type(jadn_types, type_def)

def get_field_from_struct(struct_field, value, id = False):
    """
    Retrieve a field definition from a structured type by its value
    """
    if not get_type(struct_field) in STRUCTURED_TYPES and not get_type(struct_field) in SELECTOR_TYPES:
        raise ValueError("Struct field definition must be a list: ", struct_field)
    children = get_children(struct_field)
    for field in children:
        if id:
            if str(field[0]) == str(value):
                return field
        else:
            if field[1] == value:
                return field
    return None

def is_structure(cls) -> bool:
    """
    Determine if the definition is a structure type
    `Array`, `ArrayOf`, `Map`, `MapOf`, & `Record` are structure types
    :return: True/False if the definition is a structure type
    """
    for base in cls.__mro__:
        if base.__name__ in STRUCTURED_TYPES:
            return True
    return False

def is_selector(cls) -> bool:
    """
    Determine if the definition is a selector type
    `Enumerated` & `Choice` are selector types
    :return: True/False if the definition is a selector type
    """
    for base in cls.__mro__:
        if base.__name__ in SELECTOR_TYPES:
            return True
    return False

def jadn2typestr(tname: str, topts: list[OPTION_TYPES]) -> str:
    """
    Convert typename and options to string
    """
    # Handle ktype/vtype containing Enum options
    def _kvstr(optv: str) -> str:
        if optv[0] == OPTION_ID['enum']:
            return f'Enum[{optv[1:]}]'
        if optv[0] == OPTION_ID['pointer']:
            return f'Pointer[{optv[1:]}]'
        return optv

    # Length range (single-ended) - default is {0..*}
    # min/max Length: {}
    def _lrange(ops: dict) -> str:
        lo = ops.pop('minLength', 0)
        hi = ops.pop('maxLength', MAX_DEFAULT)
        hs = '*' if hi == MAX_DEFAULT else '.' if hi == MAX_UNLIMITED else str(hi)
        return f'{{{lo}..{hs}}}' if lo != 0 or hs != '*' else ''

    # Value range (double-ended) - default is [*..*]
    # min/max Inclusive: []
    # min/max Exclusive: ()
    def _vrange(ops: dict) -> str:
        lc = '(' if 'minExclusive' in ops else '['
        hc = ')' if 'maxExclusive' in ops else ']'
        lo = ops.pop('minInclusive', ops.pop('minExclusive', '*'))
        hi = ops.pop('maxInclusive', ops.pop('maxExclusive', '*'))
        return f'={lc}{lo}, {hi}{hc}' if lo != '*' or hi != '*' else ''

    opts = topts_s2d(topts, tname)
    txt = '#' if opts.pop('id', None) else ''   # SIDE EFFECT: remove known options from opts.
    if tname in ('ArrayOf', 'MapOf'):
        txt += f"({_kvstr(opts.pop('ktype'))}, " if tname == 'MapOf' else '('
        txt += f"{_kvstr(opts.pop('vtype'))})"

    if v := opts.pop('combine', None):
        txt += f"({ {'O': 'anyOf', 'A': 'allOf', 'X': 'oneOf'}[v]})"

    if v := opts.pop('enum', None):
        txt += f'(Enum[{v}])'

    if v := opts.pop('pointer', None):
        txt += f'(Pointer[{v}])'

    if v := opts.pop('pattern', None):
        txt += f'{{pattern="{v}"}}'

    if v := _vrange(opts):
        txt += v

    if v := _lrange(opts):
        txt += v

    if v := opts.pop('format', None):
        txt += f' /{v}'

    for opt in ('unique', 'set', 'unordered', 'sequence', 'abstract', 'final'):
        if o := opts.pop(opt, None):
            txt += (' ' + opt)

    for opt in ('extends', 'restricts'):
        if o := opts.pop(opt, None):
            txt += f" {opt}({o})"

    return f"{tname}{txt}{f' ?{opts}?' if opts else ''}"  # Flag unrecognized options

def topts_s2d(olist: Union[list[OPTION_TYPES], tuple[OPTION_TYPES, ...]], typename: str = None) -> dict:
    """
    Convert list of type definition option strings to options dictionary
    """
    ptype = {'Binary': bytes, 'Boolean': bool, 'Integer': int, 'Number': float, 'String': str}.get(typename, None)
    assert isinstance(olist, (list, tuple)), f'{olist} is not a list'
    topts = {o for o in olist if ord(o[0]) in TYPE_OPTIONS}
    if uopts := {*olist} - topts:
        raise(f"Unknown type options: {','.join(uopts)}")
    opts = {}
    for o in topts:
        k, v, _ = TYPE_OPTIONS[ord(o[0])]
        t = v if v else ptype
        if t is None:
            raise(f"Invalid type option for {typename}: {k}={o[1:]}")
        opts[k] = t(o[1:])
    return opts
