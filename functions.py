import urllib.parse
import pyperclip
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
        return None  # Retorna None se o arquivo não for encontrado