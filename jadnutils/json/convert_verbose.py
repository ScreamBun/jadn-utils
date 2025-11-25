from jadnutils.utils.rev_conversion_utils import get_real_type_order
from jadnutils.utils.rev_conversion_utils import get_jadn_type_by_name
from jadnutils.utils.jadn_utils import get_options
from jadnutils.utils.jadn_utils import get_children
from jadnutils.utils.jadn_utils import get_inherited_fields
from jadnutils.utils.jadn_utils import has_key_link
from jadnutils.utils.jadn_utils import get_key_from_link
from jadnutils.utils.jadn_utils import get_type
from jadnutils.utils.rev_conversion_utils import reconcile_children
from jadnutils.utils.jadn_utils import get_true_type_def
from jadnutils.utils.rev_conversion_utils import get_python_type
from jadnutils.utils.rev_conversion_utils import valid_children_length
from jadnutils.utils.jadn_utils import handle_mapof_enum_key
from jadnutils.utils.consts import OPTION_ID, COMPACT_CONST, CONCISE_CONST

def convert_to_verbose(jadn_schema, json_obj, convert_from, root=None):
    """
    Converts a Compact or Concise JSON Object to a Verbose JSON representation
    """
    try:
        if not jadn_schema or not json_obj:
            raise ValueError("JADN Schema and JSON Object are required for conversion")

        if not convert_from in ['compact', 'concise']:
            raise ValueError("convert_from must be either 'compact' or 'concise'")

        jadn_types = jadn_schema.get('types', {})
        root_name = jadn_schema.get('meta', {}).get('roots', [None])[0] if root is None else root

        try:
            root_def = get_jadn_type_by_name(jadn_types, root_name)
        except Exception as e:
            raise ValueError("Root type definition not found in JADN schema: " + str(e))

        ordered_types = get_real_type_order(jadn_types, [], root_def)

        verbose_json = {}
        if convert_from == COMPACT_CONST:
            verbose_json = compact_to_verbose(jadn_types, json_obj, root_def)
            return verbose_json
        else:  # convert_from == CONCISE_CONST
            pass

        return verbose_json
    except Exception as e:
        raise ValueError("Error converting to verbose JSON: " + str(e))

def compact_to_verbose(jadn_types, json_obj, type_def):
    """
    Convert compact JSON object to verbose representation using the JADN Schema.
    Call and store get_real_type_order in jadn_types before passing in jadn_types
    """

    if not type_def:
        return json_obj

    # Handle inherited fields at top level
    options = get_options(type_def)
    has_inherited_fields = True if options and any(opt for opt in options if opt.startswith(OPTION_ID["extends"]) or opt.startswith(OPTION_ID["restricts"])) else False
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
                if field_opts and any(opt for opt in field_opts if opt == OPTION_ID["link"]):
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
                elif value is None:
                    idx += 1
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