TYPE_OPTIONS = {
    '=': {'id': 61, 'unicode': '0x3d', 'name': 'id', 'type': 'Boolean', 'description': 'Enumerated type and Choice/Map/Record keys are ID not Name'},
    '*': {'id': 42, 'unicode': '0x2a', 'name': 'valueType', 'type': 'String', 'description': 'Value type for ArrayOf and MapOf'},
    '+': {'id': 43, 'unicode': '0x2b', 'name': 'keyType', 'type': 'String', 'description': 'Key type for MapOf'},
    '#': {'id': 35, 'unicode': '0x23', 'name': 'enum', 'type': 'String', 'description': 'enumeration derived from Array/Choice/Map/Record type'},
    '>': {'id': 62, 'unicode': '0x3e', 'name': 'pointer', 'type': 'String', 'description': 'enumeration of pointers derived from Array/Choice/Map/Record type'},
    '%': {'id': 37, 'unicode': '0x25', 'name': 'pattern', 'type': 'String', 'description': 'regular expression that a string must match'},
    'w': {'id': 119, 'unicode': '0x77', 'name': 'minExclusive', 'type': None, 'description': 'minimum numeric/string value, excluding bound'},
    'x': {'id': 120, 'unicode': '0x78', 'name': 'maxExclusive', 'type': None, 'description': 'maximum numeric/string value, excluding bound'},
    'y': {'id': 121, 'unicode': '0x79', 'name': 'minInclusive', 'type': None, 'description': 'minimum numeric/string value'},
    'z': {'id': 122, 'unicode': '0x7a', 'name': 'maxInclusive', 'type': None, 'description': 'maximum numeric/string value'},
    'u': {'id': 117, 'unicode': '0x75', 'name': 'default', 'type': None, 'description': 'Default value'},
    'v': {'id': 118, 'unicode': '0x76', 'name': 'const', 'type': None, 'description': 'Constant value'},
    '{': {'id': 123, 'unicode': '0x7b', 'name': 'minLength', 'type': 'Integer', 'description': 'minimum byte or text string length, collection item count'},
    '}': {'id': 125, 'unicode': '0x7d', 'name': 'maxLength', 'type': 'Integer', 'description': 'maximum byte or text string length, collection item count'},
    'q': {'id': 113, 'unicode': '0x71', 'name': 'unique', 'type': 'Boolean', 'description': 'ArrayOf instance must not contain duplicates'},
    's': {'id': 115, 'unicode': '0x73', 'name': 'set', 'type': 'Boolean', 'description': 'ArrayOf instance is unordered and unique (set)'},
    'b': {'id': 98, 'unicode': '0x62', 'name': 'unordered', 'type': 'Boolean', 'description': 'ArrayOf instance is unordered and not unique (bag)'},
    'o': {'id': 111, 'unicode': '0x6f', 'name': 'sequence', 'type': 'Boolean', 'description': 'Map, MapOr or Record instance is ordered and unique (ordered set)'},
    '0': {'id': 48, 'unicode': '0x30', 'name': 'nillable', 'type': 'Boolean', 'description': 'Instance may have no value, represented by nil, null, None, etc.'},
    'C': {'id': 67, 'unicode': '0x43', 'name': 'combine', 'type': 'String', 'description': 'Choice instance is a logical combination (anyOf, allOf, oneOf)'},
    '/': {'id': 47, 'unicode': '0x2f', 'name': 'format', 'type': 'String', 'description': 'semantic validation keyword, may affect serialization'},
    'E': {'id': 69, 'unicode': '0x45', 'name': 'scale', 'type': 'Integer', 'description': 'fixed point scale factor n, serialized int = value * 10^n'},
    'a': {'id': 97, 'unicode': '0x61', 'name': 'abstract', 'type': 'Boolean', 'description': 'Inheritance: abstract, non-instantiatable'},
    'r': {'id': 114, 'unicode': '0x72', 'name': 'restricts', 'type': 'String', 'description': 'Inheritance: restriction - subset of referenced type'},
    'e': {'id': 101, 'unicode': '0x65', 'name': 'extends', 'type': 'String', 'description': 'Inheritance: extension - superset of referenced type'},
    'f': {'id': 102, 'unicode': '0x66', 'name': 'final', 'type': 'Boolean', 'description': 'Inheritance: final - cannot have subtype'},
    'A': {'id': 65, 'unicode': '0x41', 'name': 'attr', 'type': 'Boolean', 'description': 'Value may be serialized as an XML attribute'}
}

FIELD_OPTIONS = {
    '[': {'id': 91, 'unicode': '0x5b', 'name': 'minOccurs', 'type': 'Integer', 'description': 'min cardinality, default = 1, 0 = field is optional'},
    ']': {'id': 93, 'unicode': '0x5d', 'name': 'maxOccurs', 'type': 'Integer', 'description': 'max cardinality, default = 1, <0 = inherited or none, not 1 = array'},
    '&': {'id': 38, 'unicode': '0x26', 'name': 'tagId', 'type': 'Integer', 'description': 'field that specifies the type of this field'},
    '<': {'id': 60, 'unicode': '0x3c', 'name': 'dir', 'type': 'Boolean', 'description': 'pointer enumeration treats field as a collection'},
    'K': {'id': 75, 'unicode': '0x4b', 'name': 'key', 'type': 'Boolean', 'description': 'field is the primary key for TypeName'},
    'L': {'id': 76, 'unicode': '0x4c', 'name': 'link', 'type': 'Boolean', 'description': 'field is a link (foreign key) to an instance of FieldType'}
    # 'N': {'id': 78, 'unicode': '0x4e', 'name': 'not', 'type': 'Boolean', 'description': 'field is not an instance of FieldType, use Choice(anyOf)'}
}