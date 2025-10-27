import os
import json
import pandas as pd
from jadnutils.utils.jadn_utils import get_field_by_data, get_type

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
def serialize_as_compact(jadn_types, json_obj):
	"""
	Recursively strip keys from JSON objects, returning only values.
	Example: {"a": 1, "b": 2} => [1, 2]
	"""
	if isinstance(json_obj, dict): # {a:1, b:2}
		field = get_field_by_data(jadn_types, json_obj)
		type = get_type(field)
		if type == "Record":
			return [serialize_as_compact(jadn_types, value) for value in json_obj.values()]
		else:
			return {key: serialize_as_compact(jadn_types, value) for key, value in json_obj.items()}
	elif isinstance(json_obj, list): # [{a:1, b:2}]
		return [serialize_as_compact(jadn_types, item) for item in json_obj]
	else: # value base case
		return json_obj

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
