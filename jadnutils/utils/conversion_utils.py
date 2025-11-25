import os
import json
import pandas as pd
from jadnutils.utils.jadn_utils import get_field_by_data, get_inherited_fields, get_type, get_field_from_struct, get_children, get_options, get_true_type_def
from jadnutils.utils.consts import CONCISE_IGNORE_FORMATS
from jadnutils.utils.rev_conversion_utils import get_python_type

############### HTML Convert Utils ###############
def build_type_summary_html(name, type_val, options, description):
	"""
	Build HTML table for type, options, and description, including a heading for the name.
	Args:
		name (str): The type name (for heading and anchor)
		type_val (str): The type name (for table)
		options (str): Options string
		description (str): Description string
	Returns:
		str: HTML table with heading
	"""
	df = pd.DataFrame([[type_val, options, description]], columns=["Name", "Options", "Description"])
	return f"<h4 id='{name}'>{name}</h4>" + df.to_html(index=False, escape=False)

def build_types_html(types):
	"""
	Build HTML for all non-compound types in a single table.
	Args:
		types (list): List of JADN type definitions.
	Returns:
		str: HTML table for non-compound types.
	"""
	html = ''
	primitive_like_kinds = {"String", "Boolean", "Integer", "Number", "Binary", "ArrayOf", "MapOf"}
	compound_type_kinds = {"Record", "Array", "Map", "Choice"}
	enum_type_kinds = {"Enumerated"}
  
	for t in types:
     
		is_enum = False
		fields = []
  
		if len(t) > 1 and t[1] in primitive_like_kinds:
			name = t[0] if len(t) > 0 else ''
			type = t[1]
			options = t[2] if len(t) > 2 else ''
			description = t[3] if len(t) > 3 else ''
   
		elif len(t) > 1 and t[1] in compound_type_kinds:
			name = t[0] if len(t) > 0 else ''
			type = t[1] if len(t) > 1 else ''
			options = t[2] if len(t) > 2 else ''
			description = t[3] if len(t) > 3 else ''
			fields = t[4] if len(t) > 4 else []
   
		elif len(t) > 1 and t[1] in enum_type_kinds:
			is_enum = True
			name = t[0] if len(t) > 0 else ''
			type = t[1] if len(t) > 1 else ''
			options = t[2] if len(t) > 2 else ''
			description = t[3] if len(t) > 3 else ''
			fields = t[4] if len(t) > 4 else []
		else:
			# Unknown type format, skip
			print(f"Skipping unknown type format: {t}")
			continue
   
		if fields and len(fields) > 0:
	
			if is_enum:
				normalized_fields = [(list(f) + ["", "", ""])[:3] for f in fields]
				df_fields = pd.DataFrame(normalized_fields, columns=["Id", "Value", "Description"])
			else:
				normalized_fields = []
				for f in fields:
					row = (list(f) + ["", "", "", ""])[:4]
					type_val = row[2]
					if type_val not in {"String", "Integer", "Boolean", "Number", "Binary"} and type_val:
						row[2] = f'<a href="#{type_val}">{type_val}</a>'
					normalized_fields.append(row)
				df_fields = pd.DataFrame(normalized_fields, columns=["Id", "Name", "Type", "Description"])
    
			fields_html = df_fields.to_html(index=False, escape=False)
   
			html += build_type_summary_html(name, type, options, description)
			html += f"""
					</br><div>{fields_html}</div>
					"""   
		else:
			html += build_type_summary_html(name, type, options, description)
   
	return html

def get_theme_css():
	"""
	Reads and returns the contents of theme.css from the support directory.
	Returns:
		str: CSS content or empty string if not found.
	"""

	support_dir = os.path.join(os.path.dirname(__file__), '..', 'support')
	theme_path = os.path.join(support_dir, 'theme.css')
	try:
		with open(theme_path, 'r', encoding='utf-8') as f:
			return f.read()
	except Exception:
		return ''

############### JSON Convert Utils ###############
def insert_null_values(jadn_types, field, children, json_vals):
	"""
	Insert null values for missing fields in json_obj based on children definitions.
	"""

	if not field or not children:
		return json_vals

	# Check for inherited fields
	inherited_fields = get_inherited_fields(jadn_types, field, children)
	if inherited_fields and isinstance(inherited_fields, list):
		children = inherited_fields

	if not children or not isinstance(children, list):
		return json_vals

	if isinstance(json_vals, list):
		for idx, child in enumerate(children):
			json_val = json_vals[idx] if idx < len(json_vals) else None

			if json_val is None:
				json_vals.insert(idx, None)
				continue
		
			if isinstance(json_val, get_python_type(jadn_types, child)):
				continue

			json_vals.insert(idx, None)
	elif isinstance(json_vals, dict):
		for child in children:
			if len(child) > 1:
				field_name = child[1]
				if field_name not in json_vals:
					json_vals[field_name] = None

	return json_vals

def serialize_as_compact(jadn_types, json_obj):
	"""
	Serialize JSON object to compact representation.
	Example: {"a": 1, "b": 2} => [1, 2]
	"""
	field = get_field_by_data(jadn_types, json_obj)
	type_def = get_true_type_def(jadn_types, field)
	children = get_children(type_def)
	type = get_type(type_def)
	if isinstance(json_obj, dict): # {a:1, b:2}
		if type == "Record":
			new_json_obj = insert_null_values(jadn_types, field, children, list(json_obj.values()))
			return [serialize_as_compact(jadn_types, value) for value in new_json_obj]
		else:
			new_json_obj = insert_null_values(jadn_types, field, children, json_obj)
			return {key: serialize_as_compact(jadn_types, value) for key, value in new_json_obj.items()}
	elif isinstance(json_obj, list): # [{a:1, b:2}]
		new_json_obj = insert_null_values(jadn_types, field, children, json_obj)
		return [serialize_as_compact(jadn_types, item) for item in new_json_obj]
	else: # value base case
		return json_obj

def serialize_as_concise(jadn_types, json_obj):
	"""
	Serialize JSON object to concise representation.
	Special serializations: enumeration returns id only, choice returns field ID, map returns field ID, record returns values.
	"""
	if isinstance(json_obj, dict):
		field = get_field_by_data(jadn_types, json_obj)
		type = get_type(field)
		children = get_children(field)
		if children and isinstance(children, list) and len(children) > 0 and not isinstance(children[0], list):
			children = [children] # Ensure children is the correct shape
		type_options_dict = {field[0]: get_options(field)} if field else {}
		type_options = get_options(field)
		field_options_dict = {child[1]: get_options(child) for child in children} if children else {}
		convert_format_value(type_options_dict, json_obj)
		convert_format_value(field_options_dict, json_obj)

		if type == "Record":
			return [serialize_as_concise(jadn_types, value) for value in json_obj.values()]
		elif type == "Enumerated":
			hasID = "=" in type_options
			enum_field = get_field_from_struct(field, list(json_obj.values())[0], id = hasID)
			return enum_field[0] if enum_field else None
		elif type == "Choice":
			hasID = "=" in type_options
			isCombine = "CO" in type_options or "CA" in type_options or "CX" in type_options
			choice_field = get_field_from_struct(field, list(json_obj.keys())[0], id = hasID)
			if isCombine:
				idx = jadn_types.index(field)
				field[1] = get_type(get_true_type_def(jadn_types, choice_field))
				field[4] = choice_field
				jadn_types[idx] = field
				return {choice_field[0] : serialize_as_concise(jadn_types, json_obj)}
			return {choice_field[0] : serialize_as_concise(jadn_types, json_obj.get(str(choice_field[0])) if hasID or isCombine else json_obj.get(choice_field[1]))} if choice_field else None
		elif type == "Map":
			map_field = get_field_from_struct(field, list(json_obj.keys())[0])
			if map_field:
				map_children = get_children(map_field)
				result = {}
				for key, value in json_obj.items():
					key_field = get_field_from_struct(field,  key)
					if key_field:
						result[key_field[0]] = serialize_as_concise(jadn_types, value)
				return result
			return {}
		else:
			return {key: serialize_as_concise(jadn_types, value) for key, value in json_obj.items()}
	elif isinstance(json_obj, list):
		return [serialize_as_concise(jadn_types, item) for item in json_obj]
	else:
		field = get_field_by_data(jadn_types, json_obj)
		if field and get_type(field) == "Enumerated":
			return serialize_as_concise(jadn_types, {field[0]: json_obj})
		return json_obj

def convert_format_value(format_dict, json_obj):
	"""
	Convert value based on format.
	"""
	if not isinstance(json_obj, dict):
		return

	if not isinstance(format_dict, dict):
		return

	for key, value in json_obj.items():
		for name, formats in format_dict.items():
			for format in formats:
				if format and name == key:
					converter = CONCISE_IGNORE_FORMATS[format] if format in CONCISE_IGNORE_FORMATS else None
					if converter:
						json_obj[key] = converter(value)

############### JSON Validate Utils ###############
def validate_json(data):
	"""
	Validate if the input is a valid JSON string or object.
	Returns the loaded object if valid, raises ValueError if not.
	"""
	if isinstance(data, str):
		try:
			return json.loads(data)
		except Exception as e:
			raise ValueError(f"Invalid JSON string: {e}")
	elif isinstance(data, dict) or isinstance(data, list):
		# Already a valid JSON-serializable object
		return data
	else:
		raise ValueError("Input is not a valid JSON string or object.")
