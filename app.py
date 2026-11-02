import streamlit as st

navigation = st.navigation([
    st.Page('src/overview.py', title='Visão geral', icon='📊', default=True),
    st.Page('pages/1_Importacao.py', title='Importação de dados', icon='📥'),
    st.Page('pages/2_Limpeza.py', title='Limpeza de dados', icon='🧹'),
    st.Page('pages/3_Analises.py', title='Análises', icon='📈'),
    st.Page('pages/4_Relatorios.py', title='Relatórios', icon='📋'),
    st.Page('pages/5_Sobre.py', title='Sobre o projeto', icon='ℹ️'),
])
navigation.run()
