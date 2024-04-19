import streamlit as st
from functions import load_template, format_template, create_mailto_link, extract_placeholders
from data_manager import load_engineers, load_placeholder_data
import pyperclip

def main():
    st.title('Templates for Tasks')

    # Carregar a lista de engenheiros e criar um menu suspenso para seleção
    engineer_choices = load_engineers('data/engineers.txt')
    if not engineer_choices:
        st.error("Engineer list is empty. Please check your 'engineers.txt' file.")
        return

    selected_engineer = st.selectbox("Choose an engineer:", engineer_choices)

    # Selecionar o template
    template_options = {
        "New PC Request": "templates/new_pc.txt",
        "Bring Laptop to TechHub": "templates/incident.txt",
        "Quotation": "templates/quotation.txt",
        "PC Send": "templates/pc_send.txt",
        "Hardware Reclaim": "templates/pc_return.txt"
    }
    template_name = st.selectbox("Choose your template:", list(template_options.keys()))
    template_content = load_template(template_options[template_name])

    if not template_content:
        st.error("Template file not found. Please check the file path.")
        return

    # Solicitar campos obrigatórios
    manager = st.text_input("Manager's Name:")
    recipient_email = st.text_input("Recipient Email:")
    

    # Extrair os placeholders do template selecionado
    placeholders = extract_placeholders(template_content)
    data = {'recipient_email': recipient_email, 'manager': manager, 'engineer': selected_engineer, 'ticket': None, 'new_user': None}

    # Verificar se 'ticket' e 'new_user' devem ser solicitados com base no template selecionado
    if template_name == "Bring Laptop to TechHub" and 'ticket' in placeholders:
        data['ticket'] = st.text_input("Ticket:")
    elif template_name == "PC Send":
        if 'new_user' in placeholders:
            data['new_user'] = st.text_input("New User:")
        if 'ticket' in placeholders:
            data['ticket'] = st.text_input("Ticket:")
    elif template_name == "New PC Request":
        if 'new_user' in placeholders:
            data['new_user'] = st.text_input("New User:")
        if 'ticket' in placeholders:
            data['ticket'] = st.text_input("Ticket:")
    elif template_name == "Hardware Reclaim":
        if 'new_user' in placeholders:
            data['new_user'] = st.text_input("New User:")
        if 'ticket' in placeholders:
            data['ticket'] = st.text_input("Ticket:")

    # Restante dos campos do formulário
    for placeholder in placeholders - {'manager', 'engineer', 'recipient_email', 'day', 'month', 'yobi', 'period', 'ticket', 'new_user'}:
        data[placeholder] = st.text_input(f"{placeholder.title()}:")

    # Solicitar datas em uma única linha
    cols = st.columns(4)
    if 'day' in placeholders:
        with cols[0]:
            day = st.selectbox("Day:", load_placeholder_data('day'))
        data['day'] = day
    if 'month' in placeholders:
        with cols[1]:
            month = st.selectbox("Month:", load_placeholder_data('month'))
        data['month'] = month
    if 'yobi' in placeholders:
        with cols[2]:
            yobi = st.selectbox("Yobi:", load_placeholder_data('yobi'))
        data['yobi'] = yobi
    if 'period' in placeholders:
        with cols[3]:
            period = st.selectbox("Period:", load_placeholder_data('period'))
        data['period'] = period

    cc_emails = " "

    if st.button("Prepare E-mail"):
        # Verifica se todos os campos relevantes estão preenchidos corretamente.
        if all((value or '').strip() for value in data.values() if value is not None):
            # Mapeamento de assuntos de e-mail
            subject_map = {
                "New PC Request": f"New PC Request || {data.get('ticket', 'No Ticket')}",
                "Bring Laptop to TechHub": f"{data.get('incident_description', 'No Description')} || {data.get('ticket', 'No Ticket')}",
                "Quotation": "HPラップトップ修理のPO番号作成について",
                "PC Send": "PCを発送させていただきました",
                "Hardware Reclaim": f"Hardware Reclaim || {data.get('ticket', 'No Ticket')}"
            }
            
            # Seleciona o assunto correto baseado no template escolhido
            subject = subject_map.get(template_name, "Default Subject")

            # Formata o corpo do e-mail usando o template carregado
            body = format_template(template_content, data)
            try:
                # Tenta copiar o corpo do e-mail para a área de transferência
                pyperclip.copy(body)
                st.success("E-mail prepared and body text copied to clipboard.")
            except Exception as e:
                st.error(f"Failed to copy to clipboard. {e}")
            
            # Cria o link 'mailto' para abrir o cliente de e-mail
            mailto_link = create_mailto_link(recipient_email, cc_emails, subject)
            st.markdown(f'[Open in Email Client]({mailto_link})', unsafe_allow_html=True)
        else:
            st.error("Please fill all the fields.")

if __name__ == "__main__":
    main()
