import pandas as pd
import subprocess
import tempfile
import os
import base64
import zlib
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Union, Tuple


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
        'group_by_package': True,
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
    
    @classmethod
    def get_theme_info(cls, theme_name: str) -> Dict[str, str]:
        """
        Get information about a specific theme.
        
        Args:
            theme_name: Name of the theme to get info about
            
        Returns:
            Dict with theme information including name, description, and category
        """
        theme_descriptions = {
            'amiga': {'description': 'White on blue theme based on Amiga Workbench 1.x', 'category': 'retro'},
            'aws-orange': {'description': 'Amazon Web Services colors', 'category': 'professional'},
            'black-knight': {'description': 'Dark theme representing the black knight', 'category': 'dark'},
            'bluegray': {'description': 'Blue-gray theme', 'category': 'minimalist'},
            'blueprint': {'description': 'White on blue based on blueprint reproduction process', 'category': 'retro'},
            'carbon-gray': {'description': 'Gray palette from Carbon Design System', 'category': 'professional'},
            'cerulean': {'description': 'Bootstrap cerulean theme', 'category': 'bootstrap'},
            'cloudscape-design': {'description': 'Cloudscape design colors', 'category': 'professional'},
            'crt-amber': {'description': 'Orange on black theme based on monochrome CRT monitors', 'category': 'retro'},
            'cyborg': {'description': 'Bootstrap cyborg theme', 'category': 'bootstrap'},
            'hacker': {'description': 'Jekyll hacker theme (green on dark)', 'category': 'dark'},
            'lightgray': {'description': 'Light gray theme', 'category': 'minimalist'},
            'mars': {'description': 'Mars theme from future-architect/puml-themes', 'category': 'colorful'},
            'materia': {'description': 'Bootstrap materia theme', 'category': 'bootstrap'},
            'metal': {'description': 'Silver/metallic theme', 'category': 'minimalist'},
            'mimeograph': {'description': 'Purple on gray based on mimeograph reproduction', 'category': 'retro'},
            'minty': {'description': 'Bootstrap minty theme', 'category': 'bootstrap'},
            'mono': {'description': 'Monochrome theme with monospaced font', 'category': 'minimalist'},
            '_none_': {'description': 'Empty theme (no styling)', 'category': 'minimalist'},
            'plain': {'description': 'Simple black on white with blue hyperlinks', 'category': 'minimalist'},
            'reddress-darkblue': {'description': 'Dark blue variant from Red Dress themes', 'category': 'dark'},
            'reddress-lightblue': {'description': 'Light blue variant from Red Dress themes', 'category': 'professional'},
            'sandstone': {'description': 'Bootstrap sandstone theme', 'category': 'bootstrap'},
            'silver': {'description': 'Silver/gray theme', 'category': 'minimalist'},
            'sketchy': {'description': 'Bootstrap sketchy theme (hand-drawn style)', 'category': 'bootstrap'},
            'spacelab': {'description': 'Bootstrap spacelab theme', 'category': 'bootstrap'},
            'sunlust': {'description': 'Solarized-inspired theme', 'category': 'colorful'},
            'superhero': {'description': 'Bootstrap superhero theme (dark with bright accents)', 'category': 'dark'},
            'toy': {'description': 'Toy theme from future-architect/puml-themes', 'category': 'colorful'},
            'united': {'description': 'Bootstrap united theme', 'category': 'bootstrap'},
            'vibrant': {'description': 'Vibrant colors theme', 'category': 'colorful'}
        }
        
        if theme_name not in cls.AVAILABLE_THEMES:
            return {
                'name': theme_name,
                'description': 'Unknown theme',
                'category': 'unknown',
                'available': False
            }
        
        info = theme_descriptions.get(theme_name, {'description': 'No description available', 'category': 'other'})
        return {
            'name': theme_name,
            'description': info['description'],
            'category': info['category'],
            'available': True
        }
    
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

    def generate(self, output_format: str = 'raw') -> Union[str, bytes]:
        """
        Generate PlantUML output in the specified format.
        
        Args:
            output_format: Output format - 'raw', 'png', 'svg', 'pdf', 'eps', 'txt'
        
        Returns:
            str for 'raw' format, bytes for image formats
        """
        # Generate PlantUML source code
        puml_source = self._generate_source()
        
        if output_format.lower() == 'raw':
            return puml_source
        else:
            return self._render_to_format(puml_source, output_format)
    
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

    def _render_to_format(self, puml_source: str, output_format: str) -> bytes:
        """
        Render PlantUML source to specified format.
        
        Args:
            puml_source: PlantUML source code
            output_format: Target format (png, svg, pdf, eps, txt)
        
        Returns:
            bytes: Rendered output
        """
        format_map = {
            'png': '-tpng',
            'svg': '-tsvg', 
            'pdf': '-tpdf',
            'eps': '-teps',
            'txt': '-ttxt'
        }
        
        if output_format.lower() not in format_map:
            raise ValueError(f"Unsupported format: {output_format}")
        
        # Try local PlantUML first
        try:
            plantuml_cmd = self._find_plantuml_command()
            format_flag = format_map[output_format.lower()]
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as f:
                f.write(puml_source)
                temp_puml = f.name
            
            try:
                # Run PlantUML using pipe mode for better compatibility
                cmd = [plantuml_cmd, format_flag, '-pipe']
                result = subprocess.run(
                    cmd, 
                    input=puml_source.encode('utf-8'),
                    capture_output=True,
                    check=True
                )
                return result.stdout
            finally:
                os.unlink(temp_puml)
                
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Fallback to web service for supported formats
            web_formats = {'png', 'svg', 'txt'}
            if output_format.lower() in web_formats:
                return self._render_via_web_service(puml_source, output_format)
            else:
                raise RuntimeError(
                    f"Local PlantUML required for {output_format} format. "
                    f"Web service only supports: {', '.join(web_formats)}"
                )
    
    def _find_plantuml_command(self) -> str:
        """
        Find available PlantUML command.
        
        Returns:
            str: PlantUML command to use
        
        Raises:
            FileNotFoundError: If no PlantUML installation is found
        """
        # Try different common PlantUML commands
        commands = [
            'plantuml',  # System-wide installation
            'java -jar plantuml.jar',  # JAR file in current directory
            '/usr/local/bin/plantuml',  # Common installation path
            '/opt/plantuml/plantuml.jar',  # Another common path
        ]
        
        for cmd in commands:
            try:
                # Test if command is available
                if cmd.startswith('java -jar'):
                    # For Java commands, check if the jar exists
                    jar_path = cmd.split()[-1]
                    if os.path.exists(jar_path):
                        return cmd
                else:
                    # For direct commands, test execution
                    subprocess.run([cmd.split()[0], '-version'], 
                                 capture_output=True, check=True, timeout=5)
                    return cmd
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        raise FileNotFoundError("PlantUML not found. Install PlantUML or provide path to plantuml.jar")

    def _render_via_web_service(self, puml_source: str, output_format: str, 
                               server: str = "http://www.plantuml.com/plantuml") -> bytes:
        """
        Render PlantUML using web service (fallback when local PlantUML not available).
        
        Args:
            puml_source: PlantUML source code
            output_format: Target format (png, svg, txt)
            server: PlantUML server URL
        
        Returns:
            bytes: Rendered output
        """
        # PlantUML web service encoding
        compressed = zlib.compress(puml_source.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('ascii')
        
        # Convert to PlantUML URL encoding
        encoded = encoded.replace('+', '-').replace('/', '_')
        
        format_map = {
            'png': 'png',
            'svg': 'svg', 
            'txt': 'txt'
        }
        
        if output_format.lower() not in format_map:
            raise ValueError(f"Web service only supports: {list(format_map.keys())}")
        
        url_format = format_map[output_format.lower()]
        url = f"{server}/{url_format}/{encoded}"
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return response.read()
        except Exception as e:
            raise RuntimeError(f"Web service rendering failed: {e}")

    def generate_url(self, server: str = "http://www.plantuml.com/plantuml", 
                     output_format: str = 'png') -> str:
        """
        Generate a URL for viewing the PlantUML diagram online.
        
        Args:
            server: PlantUML server URL
            output_format: Format for the URL (png, svg, txt)
        
        Returns:
            str: URL to view the diagram
        """
        puml_source = self._generate_source()
        
        # PlantUML web service encoding
        compressed = zlib.compress(puml_source.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('ascii')
        encoded = encoded.replace('+', '-').replace('/', '_')
        
        format_map = {
            'png': 'png',
            'svg': 'svg',
            'txt': 'txt'
        }
        
        url_format = format_map.get(output_format.lower(), 'png')
        return f"{server}/{url_format}/{encoded}"

    def save(self, filename: str, output_format: str = None) -> None:
        """
        Save the generated PlantUML to a file.
        
        Args:
            filename: Output filename
            output_format: Output format ('raw', 'png', 'svg', 'pdf', 'eps', 'txt').
                          If None, infers from filename extension.
        """
        # Infer format from filename if not specified
        if output_format is None:
            ext = os.path.splitext(filename)[1].lower()
            format_map = {
                '.puml': 'raw',
                '.plantuml': 'raw', 
                '.png': 'png',
                '.svg': 'svg',
                '.pdf': 'pdf',
                '.eps': 'eps',
                '.txt': 'txt'
            }
            output_format = format_map.get(ext, 'raw')
        
        # Generate content
        content = self.generate(output_format)
        
        # Write to file
        if output_format == 'raw':
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open(filename, 'wb') as f:
                f.write(content)