from jadnutils.utils.jadn_utils import get_field_by_data, get_type, get_field_from_struct, get_children, get_options, get_true_type_def

def compact_to_verbose(jadn_types, json_obj):
    """
    Convert compact JSON object to verbose representation.
    Ex: [1, 2] => {"a": 1, "b": 2}
    """
    if isinstance(json_obj, list):
        field = get_field_from_compact_data(jadn_types, json_obj)
        type = get_type(field)
        if type == "Record":
            children = get_children(field)
            result = {}
            for i, child in enumerate(children):
                key = child[1]
                value = json_obj[i] if i < len(json_obj) else None
                result[key] = compact_to_verbose(jadn_types, value)
            return result
        else:
            return {compact_to_verbose(jadn_types, value) for value in json_obj}
        return result
    elif isinstance(json_obj, dict):
        return {key: compact_to_verbose(jadn_types, value) for key, value in json_obj.items()}
    else:
        return json_obj

def get_field_from_compact_data(jadn_types, data):
    """
    Helper function to get the field definition from compact data.
    """
    for field in jadn_types:
        type = get_type(field)
        if type == "Record":
            children = get_children(field)
            if len(children) == len(data):
                # Check if types of children match data
                match = True
                for i, child in enumerate(children):
                    child_type = get_type(child)
                    if not isinstance(data[i], get_python_type(child_type)):
                        match = False
                        break
                if match:
                    return field
    return None

def get_python_type(jadn_type):
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
    return type_mapping.get(jadn_type, object)