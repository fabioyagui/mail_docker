import streamlit as st
from functions import parse_css, load_css, load_template, format_template, create_mailto_link, extract_placeholders, load_translation
from data_manager import load_placeholder_data
import pyperclip
import os

# Carregar o conteúdo do CSS
css_content = load_css('styles.css')

# Aplicar o estilo CSS
st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

def main():
    st.markdown('<h1 style="text-align: center;">メールマスター</h1>', unsafe_allow_html=True)

    # Permitir que o usuário digite o nome de um engenheiro
    selected_engineer = st.text_input("Type the engineer's name:")

    # Checagem básica para garantir que um nome foi inserido
    if not selected_engineer.strip():
        st.markdown('<p style="background-color: #008080; color: #ffffff; padding: 15px; border-radius: 10px; font-size: 20px; text-align: center; display: flex; align-items: center; justify-content: center;">Welcome, please enter an engineer\'s name.</p>', unsafe_allow_html=True)
        return


    # Selecionar o template

    template_options = {
        "Bring Laptop to us": "templates/incident.txt",
        "Please more information": "templates/more_info.txt",
        "PC Send": "templates/pc_send.txt",
        "Hardware Reclaim": "templates/received_ticket.txt",
        "Status Update": "templates/status_update.txt",
        "Ticket done": "templates/ticket_done.txt",
        "Thank you for your time": "templates/time_thanks.txt"
    }
    template_name = st.selectbox("Choose your template:", list(template_options.keys()))
    template_filename = template_options[template_name]
    template_content = load_template(template_filename)

    # Remova a extensão '.txt' para obter o nome base do template para a tradução
    base_template_name = os.path.splitext(template_filename)[0]
    translation_content = load_translation(base_template_name)
    # Agora, a verificação de erro deve ser atualizada para refletir que estamos carregando um arquivo de tradução específico
    if not template_content:
        st.error("Template file not found. Please check the file paths.")
    elif not translation_content:
        st.error(f"Translation for {base_template_name} not found. Please check the file paths.")
    else:
        # Carregar o estilo CSS
        css_content = load_css('styles.css')
        # Converter o conteúdo CSS em um dicionário
        css_dict = parse_css(css_content)
        
        # Exibir a tradução na tela com o estilo
        with st.container():
            st.text("Template Translation:")
            st.markdown(f'<div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px; border: 3px solid #0078d4; font-size: 16px; color: #444;">{translation_content}</div>', unsafe_allow_html=True)

    # Solicitar campos obrigatórios
    manager = st.text_input("User's Name:")
    recipient_email = st.text_input("Recipient Email:")


    
        # Extrair os placeholders do template selecionado
    placeholders = extract_placeholders(template_content)
    data = {'recipient_email': recipient_email, 'manager': manager, 'engineer': selected_engineer, 'ticket': None, 'new_user': None}

    # Verificar se 'ticket' e 'new_user' devem ser solicitados com base no template selecionado
    if template_name == "Bring Laptop to us" and 'ticket' in placeholders:
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
    elif template_name == "Status Update":
        if 'new_user' in placeholders:
            data['new_user'] = st.text_input("New User:")
        if 'ticket' in placeholders:
            data['ticket'] = st.text_input("Ticket:")
    elif template_name == "Ticket done":
        if 'new_user' in placeholders:
            data['new_user'] = st.text_input("New User:")
        if 'ticket' in placeholders:
            data['ticket'] = st.text_input("Ticket:")
    elif template_name == "Thank you for your time":
        if 'new_user' in placeholders:
            data['new_user'] = st.text_input("New User:")
        if 'ticket' in placeholders:
            data['ticket'] = st.text_input("Ticket:")
    elif template_name == "Please more information":
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


    cc_emails = " "  # Suponha que não haja CCs inicialmente

    if st.button("Prepare E-mail"):
        # Verifica se todos os campos relevantes estão preenchidos corretamente.
        if all((value or '').strip() for value in data.values() if value is not None):
            # Mapeamento de assuntos de e-mail
            subject_map = {
                "New PC Request": f"新しいPCのリクエスト || チケット番号: {data.get('ticket', 'No Ticket')}",
                "Bring Laptop to us": f"{data.get('incident_description', 'No Description')} || チケット番号: {data.get('ticket', 'No Ticket')}",
                "Please more information": f"追加情報をお願いします || チケット番号: {data.get('ticket', 'No Ticket')}",
                "PC Send": f"PCを発送しました || チケット番号: {data.get('ticket', 'No Ticket')}",
                "Hardware Reclaim": f"ハードウェアの回収 || チケット番号: {data.get('ticket', 'No Ticket')}",
                "Status Update": f"ステータス更新 || チケット番号: {data.get('ticket', 'No Ticket')}",
                "Ticket done": f"チケット処理完了 || チケット番号: {data.get('ticket', 'No Ticket')}",
                "Thank you for your time": f"お時間をいただきありがとうございます || チケット番号: {data.get('ticket', 'No Ticket')}"
            }
            
            subject = subject_map.get(template_name, "Default Subject")

            body = format_template(template_content, data)
            try:
                pyperclip.copy(body)
                st.success("E-mail prepared and body text copied to clipboard.")
            except Exception as e:
                st.error(f"Failed to copy to clipboard. {e}")
            
            mailto_link = create_mailto_link(recipient_email, cc_emails, subject)
            st.markdown(f'[Open in Email Client]({mailto_link})', unsafe_allow_html=True)
        else:
            st.error("Please fill all the fields.")

if __name__ == "__main__":
    main()
