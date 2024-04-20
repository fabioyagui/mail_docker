import os

def load_placeholder_data(placeholder_name, base_dir='data'):
    """Carrega o conteúdo do arquivo de placeholder especificado e retorna como uma lista."""
    file_path = os.path.join(base_dir, f'{placeholder_name}.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Usando rstrip() para remover espaços em branco no final de cada linha
            return [line.rstrip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def load_engineers(file_path):
    """Carrega uma lista de engenheiros de um arquivo de texto."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            engineers = [line.strip() for line in file if line.strip()]
            return engineers
    except FileNotFoundError:
        return []  # Retorna uma lista vazia se o arquivo não for encontrado
