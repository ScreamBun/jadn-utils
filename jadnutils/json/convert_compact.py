from jadnutils.utils.conversion_utils import serialize_as_compact, validate_json

def convert_to_compact(jadn_schema, json_obj):
    """
    Converts a Verbose JSON Object to a Compact JSON representation
    """
    try:
        # Validate initial JSON Object
        valid = validate_json(json_obj)
        if not valid:
            raise ValueError("Invalid JSON Object", json_obj)

        jadn_types = jadn_schema.get('types', {})
        compact_json = serialize_as_compact(jadn_types, json_obj)

        # Validate Compact JSON Object
        valid_compact = validate_json(compact_json)
        if not valid_compact:
            raise ValueError("Invalid Compact JSON Object", compact_json)

        return compact_json
    except Exception as e:
        raise ValueError("Error converting to compact JSON: " + str(e))