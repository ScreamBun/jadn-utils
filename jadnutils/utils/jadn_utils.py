from typing import Union
from jadnutils.utils.consts import MAX_DEFAULT, MAX_UNLIMITED, OPTION_ID, OPTION_TYPES, SELECTOR_TYPES, STRUCTURED_TYPES, TYPE_OPTIONS


def get_title(data):
    """
    Get the title from data['meta']['title'], or return 'JADN Schema' if missing.
    """
    try:
        return data.get('meta', {}).get('title', 'JADN Schema')
    except Exception:
        return 'JADN Schema'

def get_type(field):
    """
    Get the type from a field definition.
    """
    if not isinstance(field, list):
        return None
    if isinstance(field[0], str):
        return field[1]
    elif isinstance(field[1], str):
        return field[2]
    else:
        return None

def get_children(field):
    """
    Get the children from a field definition.
    """
    if not isinstance(field, list):
        raise ValueError("Field definition must be a list: ", field)
    if isinstance(field[0], str) and len(field) > 4:
        return field[4]
    else:
        return []

def get_options(field):
    """
    Get the options from a field definition.
    """
    if not isinstance(field, list):
        raise ValueError("Field definition must be a list: ", field)
    if isinstance(field[0], str):
        return field[2]
    elif isinstance(field[1], str) and len(field) > 3:
        return field[3]
    else:
        return []

def get_options(field):
    """
    Get the options from a field definition.
    """
    if not isinstance(field, list):
        raise ValueError("Field definition must be a list: ", field)
    if isinstance(field[0], str):
        return field[2]
    elif isinstance(field[1], str) and len(field) > 3:
        return field[3]
    else:
        return []

def get_field_by_name(jadn_types, name):
    """
    Retrieve a field definition by its name from jadn_types
    """
    for type_def in jadn_types:
        if type_def[0] == name:
            return type_def
    return None

def get_field_by_data(jadn_types, data):
    """
    Retrive a field definition by its data from jadn_types
    """
    if isinstance(data, dict):
        field_names = set(data.keys())
    elif isinstance(data, list):
        field_names = [get_field_by_data(jadn_types, item) for item in data]
    else:
        return None

    for jadn_type in jadn_types:
        found = True
        children = get_children(jadn_type)
        if not children:
            continue
        for field in children:
            if field[1] not in field_names and ("[0" not in get_options(field)):
                found = False
                break
        if found:
            return jadn_type
    return None

def get_field_from_struct(struct_field, value):
    """
    Retrieve a field definition from a structured type by its value
    """
    if not is_structure(struct_field) and not is_selector(struct_field):
        raise ValueError("Struct field definition must be a list: ", struct_field)
    children = get_children(struct_field)
    for field in children:
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
