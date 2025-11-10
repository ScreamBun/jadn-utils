import pandas as pd
from typing import List


class PumlGenerator:
    """
    PlantUML generator for JADN schemas using pandas DataFrames.
    Follows similar patterns to GvGenerator but outputs PlantUML syntax.
    """

    CONCEPTUAL = 'conceptual'
    LOGICAL = 'logical'
    INFORMATIONAL = 'informational'
    DETAIL_OPTS = {CONCEPTUAL, LOGICAL, INFORMATIONAL}

    # Available PlantUML themes
    AVAILABLE_THEMES = [
        'amiga', 'aws-orange', 'black-knight', 'bluegray', 'blueprint',
        'carbon-gray', 'cerulean', 'cloudscape-design', 'crt-amber', 'cyborg',
        'hacker', 'lightgray', 'mars', 'materia', 'metal', 'mimeograph',
        'minty', 'mono', '_none_', 'plain', 'reddress-darkblue',
        'reddress-lightblue', 'sandstone', 'silver', 'sketchy', 'spacelab',
        'sunlust', 'superhero', 'toy', 'united', 'vibrant'
    ]
    
    # PlantUML styling options
    STYLE_DEFAULT = {
        'detail': CONCEPTUAL,
        'show_links': True,
        'show_fields': True,
        'show_multiplicity': True,
        'class_style': 'class',  # 'class', 'entity', 'interface'
        'relationship_style': '--',  # '--', '->', '<->', etc.
        'show_primitive_types': False,
        'theme': 'aws-orange',  # PlantUML theme name
        'title': None,
        'note_position': 'right'  # 'left', 'right', 'top', 'bottom'
    }

    basic_types = ["Record", "Map", "Array"]
    primitive_types = ["String", "Integer", "Binary", "Boolean", "Number"]
    
    @classmethod
    def get_available_themes(cls) -> List[str]:
        """
        Get list of all available PlantUML themes.
        
        Returns:
            List[str]: List of theme names that can be used with the 'theme' style option
        """
        return cls.AVAILABLE_THEMES.copy()
    
    def __init__(self, schema: dict, style: dict = None):
        self.schema = schema
        
        # Merge style with defaults
        base_style = self.STYLE_DEFAULT.copy()
        if style:
            base_style.update(style)
        self.style = base_style

    def _escape_name(self, name: str) -> str:
        """Escape names for PlantUML compatibility."""
        if not name:
            return name
        # Replace problematic characters
        escaped = name.replace('-', '_').replace(' ', '_')
        # Wrap in quotes if it contains special characters
        if any(c in escaped for c in [':', '.', '/', '@']):
            return f'"{name}"'
        return escaped

    def _get_class_stereotype(self, type_name: str) -> str:
        """Get PlantUML stereotype for different JADN types."""
        stereotypes = {
            'Record': '<<record>>',
            'Map': '<<map>>',
            'Array': '<<array>>',
            'Choice': '<<choice>>',
            'Enumerated': '<<enumeration>>',
            'ArrayOf': '<<arrayOf>>',
            'MapOf': '<<mapOf>>'
        }
        return stereotypes.get(type_name, '')

    def _build_class_declaration(self, name: str, type_name: str, opts: List = None) -> str:
        """Build PlantUML class declaration."""
        escaped_name = self._escape_name(name)
        stereotype = self._get_class_stereotype(type_name)
        
        if self.style['class_style'] == 'entity':
            return f"entity {escaped_name} {stereotype}"
        elif self.style['class_style'] == 'interface' and type_name == 'Choice':
            return f"interface {escaped_name}"
        else:
            return f"class {escaped_name} {stereotype}"

    def _build_field_list(self, fields: List, detail: str) -> List[str]:
        """Build list of field strings for a class."""
        if not fields or detail == self.CONCEPTUAL:
            return []
        
        field_lines = []
        for field in fields:
            if len(field) < 3:
                continue
                
            field_id = field[0] if len(field) > 0 else ""
            field_name = field[1] if len(field) > 1 else ""
            field_type = field[2] if len(field) > 2 else ""
            field_opts = field[3] if len(field) > 3 else []
            
            if detail == self.LOGICAL:
                # Show just field names
                field_lines.append(f"  {field_name}")
            else:  # INFORMATIONAL
                # Show full field details
                multiplicity = self._get_multiplicity_from_opts(field_opts)
                mult_str = f" {multiplicity}" if multiplicity and self.style['show_multiplicity'] else ""
                field_lines.append(f"  {field_id} {field_name} : {field_type}{mult_str}")
                
        return field_lines

    def _get_multiplicity_from_opts(self, opts: List) -> str:
        """Extract multiplicity information from field options."""
        if not opts:
            return ""
        
        # Look for common multiplicity patterns
        for opt in opts:
            if isinstance(opt, str):
                if opt.startswith('[') and ']' in opt:
                    return opt
                elif opt.startswith('{') and '}' in opt:
                    return opt
        return ""

    def _build_enumerated_items(self, enum_items: List, detail: str) -> List[str]:
        """Build enumerated items for an enumeration class."""
        if not enum_items or detail == self.CONCEPTUAL:
            return []
            
        items = []
        for item in enum_items:
            if len(item) >= 2:
                value = item[0]
                name = item[1]
                if detail == self.LOGICAL:
                    items.append(f"  {name}")
                else:  # INFORMATIONAL
                    items.append(f"  {value} {name}")
        return items

    def _build_class_content(self, row) -> List[str]:
        """Build the complete content for a PlantUML class."""
        lines = []
        name = row.get('name', '')
        type_name = row.get('type', '')
        fields = row.get('fields', []) or []
        opts = row.get('opts', []) or []
        
        # Class declaration
        declaration = self._build_class_declaration(name, type_name, opts)
        lines.append(declaration + " {")
        
        detail = self.style.get('detail', self.CONCEPTUAL)
        
        if type_name == 'Enumerated':
            # Handle enumerated types
            enum_items = self._build_enumerated_items(fields, detail)
            lines.extend(enum_items)
        elif type_name in ['ArrayOf', 'MapOf']:
            # Handle container types - show what they contain
            if detail != self.CONCEPTUAL:
                container_info = self._get_container_info(type_name, opts)
                if container_info:
                    lines.append(f"  <<{container_info}>>")
        else:
            # Handle regular types with fields
            if self.style['show_fields']:
                field_lines = self._build_field_list(fields, detail)
                lines.extend(field_lines)
        
        lines.append("}")
        return lines

    def _get_container_info(self, type_name: str, opts: List) -> str:
        """Get container type information for ArrayOf/MapOf types."""
        if type_name == 'ArrayOf':
            for opt in opts:
                if isinstance(opt, str) and opt.startswith('*'):
                    return f"Array of {opt[1:]}"
        elif type_name == 'MapOf':
            key_type = None
            value_type = None
            for opt in opts:
                if isinstance(opt, str):
                    if opt.startswith('+'):
                        key_type = opt[1:]
                    elif opt.startswith('*'):
                        value_type = opt[1:]
            if key_type and value_type:
                return f"Map of {key_type} -> {value_type}"
        return ""

    def _build_relationships(self, types_df: pd.DataFrame) -> List[str]:
        """Build PlantUML relationships between classes."""
        relationships = []
        
        if not self.style['show_links']:
            return relationships
            
        rel_style = self.style['relationship_style']
        
        for _, row in types_df.iterrows():
            name = row.get('name', '')
            type_name = row.get('type', '')
            fields = row.get('fields', []) or []
            opts = row.get('opts', []) or []
            
            # Handle field relationships
            if type_name in self.basic_types or type_name == 'Choice':
                for field in fields:
                    if len(field) >= 3:
                        field_type = field[2]
                        if field_type not in self.primitive_types:
                            if not self.style['show_primitive_types'] or field_type not in self.primitive_types:
                                field_name = field[1] if len(field) > 1 else ""
                                relationships.append(f"{self._escape_name(name)} {rel_style} {self._escape_name(field_type)} : {field_name}")
            
            # Handle ArrayOf relationships
            elif type_name == 'ArrayOf':
                for opt in opts:
                    if isinstance(opt, str) and opt.startswith('*'):
                        element_type = opt[1:]
                        if element_type not in self.primitive_types:
                            relationships.append(f"{self._escape_name(name)} {rel_style} {self._escape_name(element_type)} : contains")
            
            # Handle MapOf relationships
            elif type_name == 'MapOf':
                key_type = None
                value_type = None
                for opt in opts:
                    if isinstance(opt, str):
                        if opt.startswith('+'):
                            key_type = opt[1:]
                        elif opt.startswith('*'):
                            value_type = opt[1:]
                
                if key_type and key_type not in self.primitive_types:
                    relationships.append(f"{self._escape_name(name)} {rel_style} {self._escape_name(key_type)} : key")
                if value_type and value_type not in self.primitive_types:
                    relationships.append(f"{self._escape_name(name)} {rel_style} {self._escape_name(value_type)} : value")
        
        return relationships

    def generate(self) -> str:
        """
        Generate PlantUML source code from the JADN schema.
        
        Returns:
            str: PlantUML source code
        """
        return self._generate_source()
    
    def _generate_source(self) -> str:
        """Generate PlantUML source code from the JADN schema."""
        lines = []
        
        # Start PlantUML
        lines.append("@startuml")
        
        # Add theme if specified
        if self.style.get('theme'):
            lines.append(f"!theme {self.style['theme']}")
        
        # Add title if specified
        title = self.style.get('title') or self.schema.get('meta', {}).get('title')
        if title:
            lines.append(f"title {title}")
        
        lines.append("")
        
        # Get schema data
        schema = self.schema
        types = schema.get("types", [])
        meta = schema.get("meta", {})
        roots = meta.get("roots", [])
        
        # Convert types to DataFrame
        types_df = pd.DataFrame(types, columns=["name", "type", "opts", "desc", "fields"])
        
        # Build classes
        for _, row in types_df.iterrows():
            class_lines = self._build_class_content(row)
            lines.extend(class_lines)
            lines.append("")
        
        # Build relationships
        relationships = self._build_relationships(types_df)
        if relationships:
            lines.append("' Relationships")
            lines.extend(relationships)
            lines.append("")
        
        # Mark root types with notes if any
        if roots:
            lines.append("' Root types")
            for root in roots:
                lines.append(f"note {self.style['note_position']} of {self._escape_name(root)} : Root Type")
            lines.append("")
        
        # End PlantUML
        lines.append("@enduml")
        
        return "\n".join(lines)

    def save(self, filename: str) -> None:
        """
        Save the generated PlantUML source to a file.
        
        Args:
            filename: Output filename (should end in .puml or .plantuml)
        """
        puml_source = self.generate()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(puml_source)