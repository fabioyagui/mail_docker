import streamlit as st

# Estilo para o texto do template de tradução
def translation_text_style():
    return {
        "color": "#000",  # Cor do texto preto
        "font-size": "16px",  # Tamanho da fonte
        # Adicione outros estilos conforme necessário
    }

# Função para exibir o conteúdo do template de tradução com estilo
def styled_translation_content(translation_content):
    # Carregar o estilo do texto do template de tradução
    text_style = translation_text_style()

    # Container para o conteúdo do template de tradução com estilo personalizado
    with st.container():
        st.text("Template Translation:")
        st.write(translation_content, style=text_style)
