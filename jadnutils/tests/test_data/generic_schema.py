generic_schema = {
  "meta": {
    "title": "JADN Schema Start Up Template",
    "package": "http://JADN-Schema-Start-Up-Template-URI",
    "roots": ["Schema"]
  },
  "types": [
    ["Schema", "Record", ["{1", "f", "q"], "", [
        [1, "field_value_1", "String", ["w1", "x4"], ""],
        [2, "field_value_2", "String", [], ""],
        [3, "field_value_3", "Enumerated-Name", ["w1", "x4"], ""],
        [4, "field_value_4", "Choice-Name", ["w1", "x4"], ""],
        [5, "field_value_5", "Map-Name", ["w1", "x4"], ""],
        [6, "field_value_6", "Array-Name", ["w1", "x4"], ""],
        [7, "field_value_7", "MapOf-Name", ["w1", "x4"], ""],
        [8, "field_value_8", "ArrayOf-Name", ["w1", "x4"], ""]
      ]],
    ["Enumerated-Name", "Enumerated", [], "", [
        [1, "field_value_1", ""],
        [2, "field_value_2", ""]
      ]],
    ["Choice-Name", "Choice", [], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", [], ""]
      ]],
    ["Map-Name", "Map", [], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", [], ""]
      ]],
    ["Array-Name", "Array", [], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", [], ""]
      ]],
    ["MapOf-Name", "MapOf", ["+Integer", "*String"], "", []],
    ["ArrayOf-Name", "ArrayOf", ["*String"], "", []]
  ]
}