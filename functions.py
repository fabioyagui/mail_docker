import urllib.parse
import re
import os

def load_template(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None


def extract_placeholders(template):
    return set(re.findall(r'\{(\w+)\}', template))

def format_template(template, data):
    return template.format(**data)

import urllib.parse

def create_mailto_link(to, cc, subject):
    # Definição dos parâmetros
    params = {
        "cc": cc,
        "subject": subject
    }
    # Codificação dos parâmetros para a URL
    query_string = urllib.parse.urlencode(params)
    # Substituir '+' por '%20' para garantir a correta exibição de espaços
    query_string = query_string.replace('+', '%20')
    return f"mailto:{to}?{query_string}"

def load_placeholder_data(placeholder_name, base_dir='data'):
    file_path = os.path.join(base_dir, f'{placeholder_name}.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def load_translation(template_name):
    # Define o caminho base para a pasta 'translations'
    translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
    
    # Forma o nome do arquivo de tradução
    translation_file = f"{template_name}_translated.txt"
    translation_path = os.path.join(translations_dir, translation_file)

    # Tenta abrir o arquivo de tradução
    try:
        with open(translation_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Translation file not found at path: {translation_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the translation file: {e}")
        return None

def parse_css(css_content):
    if css_content is None:
        return {}

    css_dict = {}
    for line in css_content.split('\n'):
        if ':' in line:
            prop, value = line.split(':', 1)
            css_dict[prop.strip()] = value.strip()

    return css_dict


# Adicione a função load_css para carregar o conteúdo CSS do arquivo
def load_css(css_filename):
    css_path = os.path.join(os.getcwd(), 'css', css_filename)
    try:
        with open(css_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"CSS file not found at path: {css_path}")
        return None
