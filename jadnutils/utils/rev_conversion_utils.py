from jadnutils.utils.jadn_utils import get_type, get_children, get_options, get_true_type_def
from jadnutils.utils.consts import PRIMITIVE_TYPES, STRUCTURED_TYPES, OPTION_ID

def reconcile_children(type_def):
    """
    Reconcile type definition children to ensure it has all necessary components.
    """
    if not type_def:
        raise ValueError("Type definition is None or empty.")

    if len(type_def) < 5:
        type_def.append([])

    try:
        for idx, child in enumerate(type_def[4]):
            type_def[4][idx] = reconcile_field_def(child)
    except Exception as e:
        raise ValueError(f"Error reconciling children for type definition {type_def}. {e}")

    return type_def

def reconcile_field_def(field_def):
    """
    Reconcile field definition to ensure it has all necessary components.
    """
    if not field_def:
        raise ValueError("Field definition is None or empty.")

    if len(field_def) < 4:
        field_def.append([])
    if len(field_def) < 5:
        field_def.append("")

    return field_def

def valid_children_length(jadn_types, type_def, json_obj):
    """
    Check if number of children in type def matches numbers of keys in json_obj
    """
    if type_def is None or json_obj is None:
        return False
    
    try:
        true_type_def = get_true_type_def(jadn_types, type_def)
        true_type_type = get_type(true_type_def)

        keys = json_obj.keys() if isinstance(json_obj, dict) else json_obj if isinstance(json_obj, list) else [json_obj]

        # Handle ArrayOf
        if true_type_type == "ArrayOf":
            true_type_type = get_options(true_type_def)[0].lstrip('*')
            if true_type_type and len(keys) > 1:
                # if key instances are not all of key type that type, not correct type
                return all(isinstance(k, get_python_type(jadn_types, type_def, direct_type=true_type_type, value=k)) for k in keys)
        
        true_type_children = get_children(true_type_def) if true_type_type in STRUCTURED_TYPES else [] # Enum and Choice children should not all be counted
        required_children = [child for child in true_type_children if '[0' not in get_options(child)]

        req_len = len(required_children)
        keys_len = len(keys)
    except Exception as e:
        raise ValueError(f"Error comparing children for type definition {type_def} and {json_obj}. {e}")

    return req_len <= keys_len

def get_real_type_order(jadn_types, visited, type_def):
    """
    Returns a flat list of type definitions in the order they are encountered,
    starting from the root type.
    """
    try:
        if not type_def or type_def[0] in visited:
            return []
        visited.append(type_def[0])
        result = [type_def]

        children = get_children(type_def)
        options = get_options(type_def)
        curr_type = get_type(type_def)

        # Case: children
        if children and len(children) > 0:
            for field in children:
                child_type_name = get_type(field)
                child_type_def = get_jadn_type_by_name(jadn_types, child_type_name)
                if child_type_def:
                    result += get_real_type_order(jadn_types, visited, child_type_def)
        # Case: ArrayOf
        elif curr_type == "ArrayOf" and len(options) > 0:
            array_of_type_name = options[0].lstrip('*')
            array_of_type_def = get_jadn_type_by_name(jadn_types, array_of_type_name)
            if array_of_type_def:
                result += get_real_type_order(jadn_types, visited, array_of_type_def)
        # Case: MapOf
        elif curr_type == "MapOf" and len(options) > 1:
            key_name = next(opt for opt in options if opt.startswith('+')).lstrip('+')
            value_name = next(opt for opt in options if opt.startswith('*')).lstrip('*')
            key_type_def = get_jadn_type_by_name(jadn_types, key_name)
            value_type_def = get_jadn_type_by_name(jadn_types, value_name)
            if key_type_def:
                result += get_real_type_order(jadn_types, visited, key_type_def)
            if value_type_def:
                result += get_real_type_order(jadn_types, visited, value_type_def)
        
        # Case: Inheritance
        parent = [opt for opt in options if opt.startswith(OPTION_ID["extends"]) or opt.startswith(OPTION_ID["restricts"])]
        if len(parent) > 0:
            parent_name = parent[0][1:] if parent else None
            parent_type_def = get_jadn_type_by_name(jadn_types, parent_name)
            if parent_type_def:
                result += get_real_type_order(jadn_types, visited, parent_type_def)
        return result
    except Exception as e:
        raise ValueError(f"Error determining real type order for type definition {type_def}. {e}")

def get_jadn_type_by_name(jadn_types, name):
    """
    Retrieve a JADN Type by providing a type name
    """
    if not name or not jadn_types:
        return None

    for jadn_type in jadn_types:
        if jadn_type[0] == name:
            return jadn_type

    return None

def get_python_type(jadn_types, field, id = False, direct_type = None, value = None):
    """
    Map JADN types to Python types.
    """
    type_mapping = {
        "String": str,
        "Integer": int,
        "Number": float,
        "Boolean": bool,
        "Binary": str,
        "Record": list, # Compact changes records to lists
        "Enumerated": int if id else str,
        "Choice": dict,
        "Map": dict,
        "Array": list,
        "MapOf": dict,
        "ArrayOf": list,
    }

    options = get_options(field)

    # Skip all the logic, just want to get the python equivalent of a JADN Type
    if direct_type:
        return type_mapping.get(direct_type, object)

    true_type = get_type(field)
    true_options = options
    true_children = get_children(field)
    if true_type not in type_mapping:
        true_type_def = get_true_type_def(jadn_types, field)
        true_type = get_type(true_type_def)
        true_options = get_options(true_type_def)
        true_children = get_children(true_type_def)

    if true_type not in type_mapping:
        return None

    # Check for multiplicity
    if true_type in PRIMITIVE_TYPES:
        if options:
            # If any item in options includes '[#' or ']#' += '[0', return true
            multiplicities = [opt for opt in options if opt.startswith('[') or opt.startswith(']')]
            if multiplicities:
                min_mult = [mult.lstrip('[') for mult in multiplicities if mult.startswith('[')]
                min_mult = min_mult[0] if min_mult else None

                max_mult = [mult.lstrip(']') for mult in multiplicities if mult.startswith(']')]
                max_mult = max_mult[0] if max_mult else None

                if (min_mult and min_mult != '0') or (max_mult and max_mult != '1'):
                    jadn_types.append([field[1], "ArrayOf", ['*' + true_type], "", []])
                    return list

    # Handle untagged choices
    if value and true_type == "Choice" and any(opt for opt in true_options if opt == "CO" or opt == "CA" or opt == "CX"):
        for child in true_children:
            if isinstance(value, get_python_type(jadn_types, child, value=value)):
                new_type = get_type(child)
                return type_mapping.get(new_type, object)

    # Handle tagID choices
    if value and true_type == "Choice":
        merged_opts = options + true_options
        tagid_opt = next((opt for opt in merged_opts if opt.startswith(OPTION_ID["tagid"])), None)
        if tagid_opt:
            tagid = tagid_opt.lstrip(OPTION_ID["tagid"])
            if tagid.isdigit():
                tagid = int(tagid)
            else:
                raise ValueError(f"Invalid tag ID option '{tagid}' in field {field}.")
            return type(value)

    try:
        return type_mapping.get(true_type, object)
    except Exception as e:
        raise ValueError(f"Error determining Python type for field {field}. {e}")