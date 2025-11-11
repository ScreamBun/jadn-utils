from jadnutils.utils.jadn_utils import get_field_by_data, get_type, get_field_from_struct, get_children, get_options, get_true_type_def, get_parent
from jadnutils.utils.consts import CORE_TYPES

def compact_to_verbose(jadn_types, json_obj, type_def):
    """
    Convert compact JSON object to verbose representation using the JADN Schema.
    Call and store get_real_type_order in jadn_types before passing in jadn_types
    """

    if not type_def:
        return json_obj

    if isinstance(json_obj, dict):
        result = {}
        for idx, (field_num, field_name, field_type, _, _) in enumerate(type_def[4]):
            field_value = json_obj.get(field_name)
            if field_value is not None:
                field_type_def = get_jadn_type_by_name(jadn_types, field_type)
                verbose_value = compact_to_verbose(jadn_types, field_value, field_type_def)
                if verbose_value is not None:
                    result[field_name] = verbose_value
                    
        if result == {} and json_obj:
            key = list(json_obj.keys())[0]
            next_type = jadn_types[1]
            next_jadn_types = jadn_types[1:]

            # Determine if current type def should be kept. If current type_def children match json_obj keys, keep type
            curr_keys = set(json_obj[key].keys()) if isinstance(json_obj[key], dict) else json_obj[key]
            expected_keys = set(child[1] for child in get_children(type_def))
            keep_type = curr_keys == expected_keys

            # Handle ArrayOf
            curr_type = get_type(type_def)
            if curr_type == "ArrayOf":
                verbose_value = []
                instances = json_obj[key]
                for inst in instances:
                    curr_options = get_options(type_def)
                    val_type = next((opt for opt in curr_options if opt.startswith("*")), None)
                    val_type_def = get_jadn_type_by_name(jadn_types, val_type.lstrip('*'))
                    item = compact_to_verbose(jadn_types, inst, val_type_def)
                    if item is not None:
                        verbose_value.append(item)
                result[key] = verbose_value
                return result

            if keep_type:
                verbose_value = compact_to_verbose(jadn_types, json_obj[key], type_def)
            else:
                verbose_value = compact_to_verbose(next_jadn_types, json_obj[key], next_type)
            if verbose_value is not None:
                result[key] = verbose_value
        return result

    if isinstance(json_obj, list):
        curr_type = get_type(type_def)
        if curr_type == "Record":
            children = get_children(type_def)
            result = {}
            for i, child in enumerate(children):
                key = child[1]
                field_type = child[2]
                value = json_obj[i] if i < len(json_obj) else None
                if value is not None:
                    field_type_def = get_jadn_type_by_name(jadn_types, field_type)
                    verbose_value = compact_to_verbose(jadn_types, value, field_type_def)
                    if verbose_value is not None:
                        result[key] = verbose_value
            return result
        else:
            # Determine if current type def should be kept. If current type_def children match json_obj keys, keep type
            curr_keys = json_obj
            expected_keys = list(child[1] for child in get_children(type_def))
            keep_type = curr_keys == expected_keys

            if keep_type:
                return [compact_to_verbose(jadn_types, value, type_def) for value in json_obj if value is not None]
            else:
                next_type = jadn_types[1]
                next_jadn_types = jadn_types[1:]
                return [compact_to_verbose(next_jadn_types, value, next_type) for value in json_obj if value is not None]

    return json_obj

def get_real_type_order(jadn_types, visited, type_def):
    """
    Returns a flat list of type definitions in the order they are encountered,
    starting from the root type.
    """
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
        key_name = options[0].lstrip('+')
        value_name = options[1].lstrip('*')
        key_type_def = get_jadn_type_by_name(jadn_types, key_name)
        value_type_def = get_jadn_type_by_name(jadn_types, value_name)
        if key_type_def:
            result += get_real_type_order(jadn_types, visited, key_type_def)
        if value_type_def:
            result += get_real_type_order(jadn_types, visited, value_type_def)
    return result

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

def get_field_from_compact_data(jadn_types, data):
    """
    Helper function to get the field definition from compact data.
    """
    for field in jadn_types:
        type = get_type(field)
        if type == "Record":
            children = get_children(field)
            if valid_children_length(children, data): # Need length checker with optional consideration
                # Check if types of children match data
                match = True
                for i, child in enumerate(children):
                    child_type = get_type(child)
                    if not isinstance(data[i], get_python_type(jadn_types, child)):
                        match = False
                        break
                if match:
                    return field
    return None

def valid_children_length(children_array, data_array):
    """
    Check if the lengths of the children array and data array are equal,
    considering optional fields.
    """
    if not children_array or not data_array:
        return False
    
    children_required_count = len([child for child in children_array if '[0' not in get_options(child)])
    data_count = len(data_array)

    return children_required_count <= data_count

def get_python_type(jadn_types, field):
    """
    Map JADN types to Python types.
    """
    type_mapping = {
        "String": str,
        "Integer": int,
        "Number": float,
        "Boolean": bool,
        "Binary": bytes,
        "Record": list, # Compact changes records to lists
        "Enumerated": str,
        "Choice": dict,
        "Map": dict,
        "Array": list,
        "MapOf": dict,
        "ArrayOf": list,
    }

    true_type = get_type(field)
    if true_type not in type_mapping:
        true_type = get_type(get_true_type_def(jadn_types, field))

    if true_type not in type_mapping:
        return None

    return type_mapping.get(true_type, object)