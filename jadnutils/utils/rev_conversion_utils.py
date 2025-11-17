from jadnutils.utils.jadn_utils import get_type, get_children, get_options, get_true_type_def, get_inherited_fields, get_key_from_link, has_key_link, handle_mapof_enum_key
from jadnutils.utils.consts import PRIMITIVE_TYPES, STRUCTURED_TYPES

def compact_to_verbose(jadn_types, json_obj, type_def):
    """
    Convert compact JSON object to verbose representation using the JADN Schema.
    Call and store get_real_type_order in jadn_types before passing in jadn_types
    """

    if not type_def:
        return json_obj

    # Handle inherited fields at top level
    options = get_options(type_def)
    has_inherited_fields = True if options and any(opt for opt in options if opt.startswith('e') or opt.startswith('r')) else False
    if has_inherited_fields:
        existing_children = get_children(type_def)
        inherited_fields = get_inherited_fields(jadn_types, type_def, existing_children)
        if len(type_def) < 5:
            type_def.append(inherited_fields)
        else:
            type_def[4] = inherited_fields

    # Handle key link
    if has_key_link(type_def):
        if len(type_def) > 4 and isinstance(type_def[4], list):
            for idx, field in enumerate(type_def[4]):
                field_opts = get_options(field)
                if field_opts and any(opt for opt in field_opts if opt == "L"):
                    type_def[4][idx] = get_key_from_link(jadn_types, field)

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
            type_def[4] = reconcile_children(type_def)[4]
            for idx, (field_num, field_name, field_type, _, _) in enumerate(type_def[4]):
                # Check for ID
                hasID = True if len([opt for opt in options if opt == "="]) > 0 else False
                field_value = json_obj.get(field_name) if not hasID else json_obj.get(str(field_num))
                if field_value is not None:
                    field_type_def = get_jadn_type_by_name(jadn_types, field_type)
                    verbose_value = compact_to_verbose(jadn_types, field_value, field_type_def)
                    if verbose_value is not None:
                        if hasID:
                            result[str(field_num)] = verbose_value
                        else:
                            result[field_name] = verbose_value
        except Exception as e:
            raise ValueError(f"Type Definition {type_def} has insufficient fields to enumerate. {e}")
                    
        if result == {} and json_obj:
            try:
                key = list(json_obj.keys())[0]
                next_type = jadn_types[1] if len(jadn_types) > 1 else type_def
                next_jadn_types = jadn_types[1:] if len(jadn_types) > 1 else jadn_types

                # Determine if current type def should be kept. If current type_def children match json_obj keys, keep type
                curr_keys = set(json_obj[key].keys()) if isinstance(json_obj[key], dict) else json_obj[key]
                expected_keys = set(child[1] for child in get_children(type_def))

                # Other case: check if keys match expected keys from type definition
                curr_key_type = get_jadn_type_by_name(jadn_types, key)
                curr_key_keys = set(child[1] for child in get_children(curr_key_type)) if curr_key_type else set()
            except Exception as e:
                raise ValueError(f"Error determining keys for type definition {type_def}. {e}")

            keep_type = (curr_keys == expected_keys) or (curr_key_keys == expected_keys and curr_key_keys != set() and expected_keys != set())
            curr_type = get_type(type_def)

            # Handle ArrayOf
            try:
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
            except Exception as e:
                raise ValueError(f"Error processing ArrayOf type for type definition {type_def}. {e}")

            # Handle MapOf
            try:
                if curr_type == "MapOf":
                    key_type = next((opt for opt in options if opt.startswith("+")), None)
                    key_type_def = get_jadn_type_by_name(jadn_types, key_type.lstrip('+'))
                    value_type = next((opt for opt in options if opt.startswith("*")), None)
                    value_type_def = get_jadn_type_by_name(jadn_types, value_type.lstrip('*'))

                    true_key_type = get_type(get_true_type_def(jadn_types, key_type_def)) if key_type_def else key_type.lstrip('+')

                    # handle mapof with enum key type
                    if true_key_type == "Enumerated":
                        map_field = handle_mapof_enum_key(jadn_types, type_def, key_type_def, value_type)
                        type_def = map_field
                        # Replace type def in jadn_types
                        for idx, tdef in enumerate(jadn_types):
                            if tdef[0] == type_def[0]:
                                jadn_types[idx] = type_def
                                break
                        return compact_to_verbose(jadn_types, json_obj, type_def)

                    verbose_value = {} if true_key_type == "String" else []
                    if isinstance(verbose_value, dict):
                        if not isinstance(json_obj[key], dict):
                            for k, v in json_obj.items():
                                comp_key = compact_to_verbose(jadn_types, k, key_type_def)
                                comp_value = compact_to_verbose(jadn_types, v, value_type_def)
                                if true_key_type == "String":
                                    verbose_value[comp_key] = comp_value
                                else:
                                    verbose_value.append({comp_key: comp_value})
                                result.update(verbose_value)
                        else:
                            for k, v in json_obj[key].items():
                                comp_key = compact_to_verbose(jadn_types, k, key_type_def)
                                comp_value = compact_to_verbose(jadn_types, v, value_type_def)
                                if true_key_type == "String":
                                    verbose_value[comp_key] = comp_value
                                else:
                                    verbose_value.append({comp_key: comp_value})
                                result[key] = verbose_value
                    else:
                        for idx, item in enumerate(json_obj[key]):
                            if (idx % 2) == 0: #Even index starts at 0, keys
                                comp_key = compact_to_verbose(jadn_types, item, key_type_def)
                                verbose_value.append(comp_key)
                            else: # Odd index, values
                                comp_value = compact_to_verbose(jadn_types, item, value_type_def)
                                verbose_value.append(comp_value)
                        result[key] = verbose_value
                    return result
            except Exception as e:
                raise ValueError(f"Error processing MapOf type for type definition {type_def}. {e}")

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

                if value is not None and isinstance(value, get_python_type(jadn_types, child, isID, value=value)):
                    # Case: field_type has been converted to ArrayOf in JADN types
                    new_type = get_jadn_type_by_name(jadn_types, key)
                    if new_type and get_type(new_type) == "ArrayOf":
                        child = new_type
                        field_type = "ArrayOf"
                    if valid_children_length(jadn_types, child, value):
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
        parent = [opt for opt in options if opt.startswith('e') or opt.startswith('r')]
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
        tagid_opt = next((opt for opt in merged_opts if opt.startswith('&')), None)
        if tagid_opt:
            tagid = tagid_opt.lstrip('&')
            if tagid.isdigit():
                tagid = int(tagid)
            else:
                raise ValueError(f"Invalid tag ID option '{tagid}' in field {field}.")
            return type(value)

    try:
        return type_mapping.get(true_type, object)
    except Exception as e:
        raise ValueError(f"Error determining Python type for field {field}. {e}")