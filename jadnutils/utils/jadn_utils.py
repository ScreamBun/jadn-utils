from jadnutils.utils.consts import SELECTOR_TYPES, STRUCTURED_TYPES


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