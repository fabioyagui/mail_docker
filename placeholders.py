# placeholders.py
import streamlit as st

def display_placeholder_selections(data, placeholders):
    # Crie um dicionário para armazenar as seleções do usuário
    selections = {}
    
    # Crie uma linha única de seleção com quatro colunas
    cols = st.columns(4)
    
    with cols[0]:
        if 'day' in placeholders:
            day = data.get('day', [])
            selected_day = st.selectbox("Day:", day, key='day')
            selections['day'] = selected_day
    
    with cols[1]:
        if 'month' in placeholders:
            month = data.get('month', [])
            selected_month = st.selectbox("Month:", month, key='month')
            selections['month'] = selected_month
            
    with cols[2]:
        if 'yobi' in placeholders:
            yobi = data.get('yobi', [])
            selected_yobi = st.selectbox("Yobi:", yobi, key='yobi')
            selections['yobi'] = selected_yobi
            
    with cols[3]:
        if 'period' in placeholders:
            period = data.get('period', [])
            selected_period = st.selectbox("Period:", period, key='period')
            selections['period'] = selected_period

    return selections
