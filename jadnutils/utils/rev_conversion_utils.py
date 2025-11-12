from jadnutils.utils.jadn_utils import get_field_by_data, get_type, get_field_from_struct, get_children, get_options, get_true_type_def, get_parent
from jadnutils.utils.consts import CORE_TYPES, PRIMITIVE_TYPES, STRUCTURED_TYPES

def compact_to_verbose(jadn_types, json_obj, type_def):
    """
    Convert compact JSON object to verbose representation using the JADN Schema.
    Call and store get_real_type_order in jadn_types before passing in jadn_types
    """

    if not type_def:
        return json_obj

    if isinstance(json_obj, dict):
        result = {}

        # Handle enumerated fields 
        curr_type = get_type(type_def)
        try:
            if curr_type == "Enumerated":
                for key, value in json_obj.items():
                    field_type_def = get_jadn_type_by_name(jadn_types, curr_type)
                    verbose_value = compact_to_verbose(jadn_types, value, field_type_def)
                    if verbose_value is not None:
                        result[key] = verbose_value
                return result
        except Exception as e:
            raise ValueError(f"Type Definition {type_def} is not valid for Enumerated type. {e}")
        
        try:
            # Make sure type_def[4] exists
            if len(type_def) < 5:
                type_def.append([])
            for idx, (field_num, field_name, field_type, _, _) in enumerate(type_def[4]):
                field_value = json_obj.get(field_name)
                if field_value is not None:
                    field_type_def = get_jadn_type_by_name(jadn_types, field_type)
                    verbose_value = compact_to_verbose(jadn_types, field_value, field_type_def)
                    if verbose_value is not None:
                        result[field_name] = verbose_value
        except Exception as e:
            raise ValueError(f"Type Definition {type_def} has insufficient fields to enumerate. {e}")
                    
        if result == {} and json_obj:
            key = list(json_obj.keys())[0]
            next_type = jadn_types[1]
            next_jadn_types = jadn_types[1:]

            try:
                # Determine if current type def should be kept. If current type_def children match json_obj keys, keep type
                curr_keys = set(json_obj[key].keys()) if isinstance(json_obj[key], dict) else json_obj[key]
                expected_keys = set(child[1] for child in get_children(type_def))

                # Other case: check if keys match expected keys from type definition
                curr_key_type = get_jadn_type_by_name(jadn_types, key)
                curr_key_keys = set(child[1] for child in get_children(curr_key_type)) if curr_key_type else set()
            except Exception as e:
                raise ValueError(f"Error determining keys for type definition {type_def}. {e}")

            keep_type = (curr_keys == expected_keys) or (curr_key_keys == expected_keys and curr_key_keys != set() and expected_keys != set())

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
            idx = 0
            for child in children:
                key = child[1]
                field_type = child[2]
                value = json_obj[idx] if idx < len(json_obj) else None

                # Get options to determine if field is ID type
                true_curr_type = get_true_type_def(jadn_types, child)
                options = get_options(true_curr_type)
                isID = True if any(opt for opt in options if opt == "=") else False

                if value is not None and isinstance(value, get_python_type(jadn_types, child, isID)):
                    # Case: field_type has been converted to ArrayOf in JADN types
                    new_type = get_jadn_type_by_name(jadn_types, key)
                    if new_type and get_type(new_type) == "ArrayOf":
                        child = new_type
                        field_type = "ArrayOf"
                    if valid_children_length(jadn_types, child, value): #valid_children_length(jadn_types, type_def, json_obj):
                        idx += 1
                        field_type_def = get_jadn_type_by_name(jadn_types, field_type)
                        field_type_def = get_jadn_type_by_name(jadn_types, key) if not field_type_def else field_type_def # use key if field_type not found
                        verbose_value = compact_to_verbose(jadn_types, value, field_type_def)
                        if verbose_value is not None:
                            result[key] = verbose_value
            return result
        elif curr_type == "ArrayOf":
            # Handle ArrayOf
            verbose_value = []
            instances = json_obj
            for inst in instances:
                curr_options = get_options(type_def)
                val_type = next((opt for opt in curr_options if opt.startswith("*")), None)
                val_type_def = get_jadn_type_by_name(jadn_types, val_type.lstrip('*'))
                item = compact_to_verbose(jadn_types, inst, val_type_def)
                if item is not None:
                    verbose_value.append(item)
            return verbose_value
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

def valid_children_length(jadn_types, type_def, json_obj):
    """
    Check if number of children in type def matches numbers of keys in json_obj
    """
    if not type_def or not json_obj:
        return False
    
    true_type_def = get_true_type_def(jadn_types, type_def)
    true_type_type = get_type(true_type_def)

    keys = json_obj.keys() if isinstance(json_obj, dict) else json_obj if isinstance(json_obj, list) else [json_obj]

    # Handle ArrayOf
    if true_type_type == "ArrayOf":
        true_type_type = get_options(true_type_def)[0].lstrip('*')
        if true_type_type and true_type_type in PRIMITIVE_TYPES and len(keys) > 1:
            # if key type is a primitive and more than 1 key is given, return False. Not the type
            return False
    
    true_type_children = get_children(true_type_def) if true_type_type in STRUCTURED_TYPES else [] # Enum and Choice children should not all be counted
    required_children = [child for child in true_type_children if '[0' not in get_options(child)]

    req_len = len(required_children)
    keys_len = len(keys)

    return req_len <= keys_len

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

def get_python_type(jadn_types, field, id = False):
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
        "Enumerated": int if id else str,
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

    # Check for multiplicity
    if true_type in PRIMITIVE_TYPES:
        options = get_options(field)
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

    return type_mapping.get(true_type, object)