from jadnutils.utils.rev_conversion_utils import compact_to_verbose, get_real_type_order
from jadnutils.utils.rev_conversion_utils import get_jadn_type_by_name

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
        if convert_from == 'compact':
            verbose_json = compact_to_verbose(jadn_types, json_obj, root_def)
            return verbose_json
        else:  # convert_from == 'concise'
            pass

        return verbose_json
    except Exception as e:
        raise ValueError("Error converting to verbose JSON: " + str(e))