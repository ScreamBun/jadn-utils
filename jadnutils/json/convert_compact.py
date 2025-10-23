from jadnutils.utils.conversion_utils import strip_keys, validate_json

def convert_to_compact(json_obj) -> list:
    """
    Converts a Verbose JSON Object to a Compact JSON representation
    """
    try:
        # Validate initial JSON Object
        valid = validate_json(json_obj)
        if not valid:
            print("Error: Invalid JSON Object\n", json_obj)

        compact_json = strip_keys(json_obj)

        # Validate Compact JSON Object
        valid_compact = validate_json(compact_json)
        if not valid_compact:
            print("Error: Invalid Compact JSON Object\n", compact_json)

        return compact_json
    except Exception as e:
        print(e)