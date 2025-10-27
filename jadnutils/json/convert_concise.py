from jadnutils.utils.conversion_utils import serialize_as_concise, validate_json

def convert_to_concise(jadn_schema, json_obj):
    """
    Converts a Verbose JSON Object to a Concise JSON representation
    """
    try:
        # Validate initial JSON Object
        valid = validate_json(json_obj)
        if not valid:
            raise ValueError("Invalid JSON Object", json_obj)

        jadn_types = jadn_schema.get('types', {})
        concise_json = serialize_as_concise(jadn_types, json_obj)

        # Validate Concise JSON Object
        valid_concise = validate_json(concise_json)
        if not valid_concise:
            raise ValueError("Invalid Concise JSON Object", concise_json)

        return concise_json
    except Exception as e:
        raise ValueError("Error converting to concise JSON: " + str(e))