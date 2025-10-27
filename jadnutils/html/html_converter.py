import pandas as pd
import json

from jadnutils.utils.conversion_utils import build_types_html, get_theme_css
from jadnutils.utils.jadn_utils import get_title

class HtmlConverter:
    jadn_data: dict = {}
    
    def __init__(self, jadn_data):
        self.jadn_data = jadn_data

    def jadn_to_html(self, **kwargs):
        """
        Convert JADN JSON data to an HTML representation.
        :param json_data: JADN JSON data as a string or dictionary
        :param run_validation: Whether to validate the JSON data (default: True)
        :return: HTML string representing the JADN schema
        """
        
        run_validation = kwargs.get('run_validation', True)
        if run_validation:
            data = json.loads(self.jadn_data)
        else:
            data = self.jadn_data
        
        html_title = get_title(data)

        if isinstance(data, dict):
            meta = data.get('meta', None)
            types = data.get('types', None)
        else:
            meta = None
            types = None


        html_meta = ''
        html_config = ''
        
        if meta:
            meta_copy = dict(meta)  # avoid mutating original
            config = meta_copy.pop('config', None)
            if meta_copy:
                df_meta = pd.DataFrame([meta_copy]).transpose().reset_index()
                df_meta['index'] = df_meta['index'].apply(lambda x: x.title() if isinstance(x, str) else x)
                df_meta.columns = ["Field", "Value"]
                html_meta = df_meta.to_html(index=False, classes="no-border", header=False)
            if config is not None:
                if isinstance(config, dict):
                    df_config = pd.DataFrame([config]).transpose().reset_index()
                    df_config.columns = ["Config Field", "Value"]
                    html_config = df_config.to_html(index=False, classes="no-border", header=False)

        html_root_types = ''
        html_types = ''
        
        if types:
            
            root_types = meta['roots']
            root_type_defs = [t for t in types if t[0] in root_types]
            
            html_root_types = build_types_html(root_type_defs)
            # Remove root types from types to avoid duplication
            types = [t for t in types if t[0] not in root_types]
            
            html_types += build_types_html(types) # Multiple tables

        theme_css = get_theme_css()

        config_section = ''
        if html_config:
            config_section = (
                '<h4>Config</h4>\n'
                '<div id="config">\n'
                f'{html_config}\n'
                '</div>\n'
            )

        html = (
            '<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '<meta charset="UTF-8">\n'
            f'<title>{html_title}</title>\n'
            f'<style>\n{theme_css}\n</style>\n'
            '</head>\n'
                '<body>\n'
                    '<div id="schema">\n'
                        f'<h2>{html_title}</h2>\n'
                        '<h3>Meta</h3>\n'
                        '<div id="meta">\n'
                            f'{html_meta}\n'
                        '</div>\n'
                        f'{config_section}'
                        '<h3>Types</h3>\n'
                        '<div class="types">\n'
                            f'{html_root_types}\n'
                        '</div>\n'
                        '<div class="types">\n'
                            f'{html_types}\n'
                        '</div>\n'             
                    '</div>\n'
                '</body>\n'
            '</html>'
        )
        
        return html