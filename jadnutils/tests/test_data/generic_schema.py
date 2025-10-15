generic_schema = {
  "meta": {
    "title": "JADN Schema Start Up Template",
    "package": "http://JADN-Schema-Start-Up-Template-URI",
    "roots": ["Schema"]
  },
  "types": [
    ["Schema", "Record", ["{1", "q", "f", "eRecord-Ext"], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", [], ""],
        [3, "field_value_3", "Enumerated-Name", [], ""],
        [4, "field_value_4", "Choice-Name", [], ""],
        [5, "field_value_5", "Map-Name", [], ""],
        [6, "field_value_6", "Array-Name", [], ""],
        [7, "field_value_7", "MapOf-Name", [], ""],
        [8, "field_value_8", "ArrayOf-Name", [], ""]
      ]],
    ["Enumerated-Name", "Enumerated", ["f"], "", [
        [1, "field_value_1", ""],
        [2, "field_value_2", ""]
      ]],
    ["Choice-Name", "Choice", ["a"], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", [], ""],
        [3, "field_value_3", "String-Name", [], ""]
      ]],
    ["Map-Name", "Map", ["{3", "}6", "="], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", [], ""]
      ]],
    ["Array-Name", "Array", ["{3", "}5", "a"], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String-Name", [], ""]
      ]],
    ["MapOf-Name", "MapOf", ["*String", "+Integer", "{1", "}4", "q"], "", []],
    ["ArrayOf-Name", "ArrayOf", ["*String", "{3", "}6", "s"], "", []],
    ["String-Name", "String", [], "", []],
    ["Record-Ext", "Record", [], "", [
        [1, "field_value_1", "Integer", [], ""]
      ]]
  ]
}