unresolved_schema = {
  "meta": {
    "package": "http://example.fake",
    "roots": ["One-Of", "Any-Of", "All-Of", "Test"], 
    "namespaces": {"ls": "www.example.fake"}
  },
  "types": [
    ["One-Of", "Choice", ["CX"], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", [], ""]
      ]],
    ["All-Of", "Choice", ["CA"], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", ["%[a-z]"], ""]
      ]],
    ["Any-Of", "Choice", ["CO"], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "String", ["%[a-z]"], ""]
      ]],    
      ["Test", "Record", [], "", [
        [1, "field_value_1", "ls:OpenC2-Command", [], ""],
        [2, "field_value_2", "ls:OpenC2-Response", [], ""]
      ]]
  ]
} 