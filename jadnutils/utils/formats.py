# Ensure jsonschema prerequisite packages are installed, e.g., rfc3987 for uri/iri validation
FORMAT_JS_VALIDATE = {      # Semantic validation formats defined by JSON Schema 2019-09 Sec 7.3
    'date-time': 'String',
    'date': 'String',
    'time': 'String',
    'duration': 'String',
    # 'email': 'String',        # jsonschema package has deliberately buggy email - won't be fixed
    'idn-email': 'String',
    # 'hostname': 'String',     # jsonschema package needs bug fix
    'idn-hostname': 'String',
    'ipv4': 'String',           # doesn't allow netmask prefix length
    'ipv6': 'String',           # doesn't allow netmask prefix length
    'uri': 'String',
    'uri-reference': 'String',
    'iri': 'String',
    'iri-reference': 'String',
    # 'uuid': 'String',
    'uri-template': 'String',
    'json-pointer': 'String',
    'relative-json-pointer': 'String',
    'regex': 'String'
}

FORMAT_VALIDATE = {         # Semantic validation formats for information instances
    'email': 'String',          # Use this instead of jsonschema
    'hostname': 'String',       # Use this instead of jsonschema
    'eui': 'Binary',            # IEEE Extended Unique Identifier, 48 bits or 64 bits
    'uuid': 'Binary',           # Use this instead of jsonschema
    'tag-uuid': 'Array',        # Prefixed UUID, e.g., "action-b254a45e-d0d3-4e17-b65a-3002f86ee836"
    'ipv4-addr': 'Binary',      # IPv4 address as specified in RFC 791 Section 3.1
    'ipv6-addr': 'Binary',      # IPv6 address as specified in RFC 8200 Section 3
    'ipv4-net': 'Array',        # Binary IPv4 address and Integer prefix length, RFC 4632 Section 3.1
    'ipv6-net': 'Array',        # Binary IPv6 address and Integer prefix length, RFC 4291 Section 2.3
    'i#': 'Integer',            # #-bit signed integer, range [-2^(#-1) .. 2^(#-1)-1]
    'u#': 'Integer',            # #-bit field or unsigned integer, range = [0 .. 2^#-1]
    'f#': 'Number',             # #-bit float, significand and exponent ranges as defined in IEEE 754
}

FORMAT_SERIALIZE = {        # Data representation formats for one or more serializations
    'eui': 'Binary',            # IEEE EUI, 'hex-byte-colon' text representation, (e.g., 00:1B:44:11:3A:B7)
    'uuid': 'Binary',           # RFC 4122 UUID text representation, (e.g., e81415a7-4c8d-45cd-a658-6b51b7a8f45d)
    'tag-uuid': 'Array',        # UUID with prefixed tag, (e.g., action-e81415a7-4c8d-45cd-a658-6b51b7a8f45d)
    'ipv4-addr': 'Binary',      # IPv4 'dotted-quad' text representation, RFC 2673 Section 3.2
    'ipv6-addr': 'Binary',      # IPv6 text representation, RFC 4291 Section 2.2
    'ipv4-net': 'Array',        # IPv4 Network Address CIDR text string, RFC 4632 Section 3.1
    'ipv6-net': 'Array',        # IPv6 Network Address CIDR text string, RFC 4291 Section 2.3
    'b64': 'Binary',            # Base64url - RFC 4648 Section 5 (default text representation of Binary type)
    'x': 'Binary',              # Hex - base16 - lowercase out, case-folding in
    'X': 'Binary',              # Hex - RFC 4648 Section 8 - uppercase only
    'i#': 'Integer',            # n-bit signed integer, n should be 8*2^N (8, 16, 32, 64, ...)
    'u#': 'Integer',            # n-bit field or unsigned integer
    'f#': 'Number',             # n-bit IEEE 754 Float (16=half precision, 32=single, 64=double, 128=quad, ...)
}

VALID_FORMATS = {**FORMAT_JS_VALIDATE, **FORMAT_VALIDATE, **FORMAT_SERIALIZE}