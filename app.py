import streamlit as st
import urllib.parse
import pyperclip

def load_template(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None  # Se o arquivo não for encontrado, retorna None

def format_template(template, manager, ticket, engineer):
    # Substitui as variáveis no template
    formatted_template = template.format(manager=manager, ticket=ticket, engineer=engineer)
    return formatted_template

def create_mailto_link(to, cc, subject, body):
    # Codifica componentes da URL
    params = {
        "to": to,
        "cc": cc,
        "subject": subject,
        "body": body
    }
    # Cria a string de consulta com múltiplos campos
    query_string = urllib.parse.urlencode(params, safe=',')
    # Substitui '+' por '%20' para corrigir o problema de espaçamento na URL
    query_string = query_string.replace('+', '%20')
    return f"mailto:{to}?{query_string}"

def main():
    st.title('Templates for Tasks')

    # Carrega a lista de engenheiros do arquivo
    try:
        with open('data/engineers.txt', 'r', encoding='utf-8') as file:
            engineers = file.read().splitlines()
        if not engineers:
            st.error("Engineer list is empty. Please check your 'engineers.txt' file.")
            return
    except FileNotFoundError:
        st.error("Engineers file not found. Please ensure the file exists.")
        return

    # Seleção do engenheiro
    engineer = st.selectbox("Choose an engineer:", engineers)
    
    # Mapeamento de nomes de arquivos para nomes amigáveis
    template_options = {
        "New PC Request": "templates/new_pc.txt",
        "Incident": "templates/incident.txt",
        "Other Template": "templates/other_template.txt"
    }

    # Seleção do template
    template_name = st.selectbox("Choose your template:", list(template_options.keys()))
    template_path = template_options[template_name]
    template_content = load_template(template_path)

    if not template_content:
        st.error("Template file not found. Please check the file path.")
        return

    # Entradas do usuário
    manager = st.text_input("Manager's Name:")
    ticket = st.text_input(f"{template_name} Ticket Number:")
    recipient_email = st.text_input("Recipient Email:")

    # CC emails sempre fixos
    cc_emails = "team1@example.com,team2@example.com,team3@example.com"

    # Botão para preparar e copiar o e-mail
    if st.button("Prepare E-mail"):
        if manager and ticket and recipient_email:
            # Formatação do Assunto
            subject_template = load_template(template_path.replace('.txt', '_subject.txt')) # Carrega o template de assunto correspondente
            subject = format_template(subject_template, manager, ticket, engineer) if subject_template else f"{template_name} | {ticket}"  # Se não houver template de assunto, usa um padrão
            subject = subject.replace('%20', ' ')  # Corrige o sinal "+" e o caractere "|" no assunto

            # Copiar corpo do e-mail para a área de transferência
            body = format_template(template_content, manager, ticket, engineer)
            pyperclip.copy(body)

            # Link para abrir e-mail no cliente de e-mail padrão
            mailto_link = create_mailto_link(recipient_email, cc_emails, subject, '')  # Corrigido para não incluir o corpo do e-mail
            st.markdown(f'[Open in Email Client]({mailto_link})', unsafe_allow_html=True)
            st.success("E-mail prepared. Body text copied to clipboard.")
        else:
            st.error("Please fill all the fields.")

if __name__ == "__main__":
    main()
