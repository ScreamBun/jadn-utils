from jadnutils.utils.jadn_utils import get_field_by_data, get_type, get_field_from_struct, get_children, get_options, get_true_type_def, get_parent
from jadnutils.utils.consts import CORE_TYPES, PRIMITIVE_TYPES
# def compact_to_verbose(jadn_types, json_obj):
#     """
#     Convert compact JSON object to verbose representation.
#     Ex: [1, 2] => {"a": 1, "b": 2}
#     """
#     if isinstance(json_obj, list):
#         field = get_field_from_compact_data(jadn_types, json_obj)
#         type = get_type(field)
#         if type == "Record":
#             children = get_children(field)
#             result = {}
#             for i, child in enumerate(children):
#                 key = child[1]
#                 value = json_obj[i] if i < len(json_obj) else None
#                 result[key] = compact_to_verbose(jadn_types, value)
#             return result
#         else:
#             return [compact_to_verbose(jadn_types, value) for value in json_obj]
#     elif isinstance(json_obj, dict):
#         return {key: compact_to_verbose(jadn_types, value) for key, value in json_obj.items()}
#     else:
#         return json_obj

def compact_to_verbose(jadn_types, json_obj, type_def):
    """
    Convert compact JSON object to verbose representation using the JADN Schema.
    Call and store get_real_type_order in jadn_types before passing in jadn_types
    """

    if not type_def:
        return json_obj

    next_type_def = jadn_types[1] if len(jadn_types) > 1 else None
    next_jadn_types = jadn_types[1:] if len(jadn_types) > 1 else []

    if isinstance(json_obj, dict):
        return {key: compact_to_verbose(next_jadn_types, value, next_type_def) for key, value in json_obj.items()}
    if isinstance(json_obj, list):
        curr_type = get_type(type_def)
        if curr_type == "Record":
            children = get_children(type_def)
            result = {}
            for i, child in enumerate(children):
                # See if parent matches
                parent_field = get_parent(jadn_types, child)
                if parent_field and parent_field[0] != type_def[0]:
                    type_def = parent_field
                key = child[1]
                value = json_obj[i] if i < len(json_obj) else None
                result[key] = compact_to_verbose(jadn_types, value, type_def)
            return result
        else:
            return [compact_to_verbose(next_jadn_types, value, next_type_def) for value in json_obj]
    else:
        return json_obj

def get_real_type_order(jadn_types, visited, type_def):
    """
    Returns a flat list of type definitions in the order they are encountered,
    starting from the root type.
    """
    if type_def[0] in visited:
        return []
    visited.append(type_def[0])
    result = [type_def]
    for field in get_children(type_def):
        child_type_name = get_type(field)
        child_type_def = get_jadn_type_by_name(jadn_types, child_type_name)
        if child_type_def:
            result += get_real_type_order(jadn_types, visited, child_type_def)
    return result

def make_jadn_frequency_map(jadn_types):
    """
    Create a frequency map of JADN types used in the schema.
    """
    freq_map = {}
    for jadn_type in jadn_types:
        type_name = jadn_type[0]
        freq_map[type_name] = freq_map.get(type_name, 0) + 1
    return freq_map

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
        "Float": float,
        "Boolean": bool,
        "Record": dict,
        "Enumerated": str,
        "Choice": dict,
        "Map": dict,
        "Array": list,
    }

    true_type = get_type(field)
    if true_type not in type_mapping:
        true_type = get_type(get_true_type_def(jadn_types, field))

    if true_type not in type_mapping:
        return None

    return type_mapping.get(true_type, object)