import streamlit as st
from src.ui import setup
from src.data_cleaning import quality_table, clean_data
from src.data_loader import prepare_sales
from src.reports import csv_bytes, excel_bytes

setup('Limpeza de dados', 'Inspecione, trate e revise uma cópia antes de atualizar o dashboard')
if 'working_data' not in st.session_state:
    st.session_state.working_data = st.session_state.sales.copy(deep=True)
df = st.session_state.working_data
st.metric('Linhas duplicadas completas', int(df.duplicated().sum()))
st.dataframe(quality_table(df), hide_index=True, width='stretch')
a = st.checkbox('Remover linhas duplicadas completas', value=True)
b = st.checkbox('Padronizar datas (inválidas tornam-se nulas)', value=True)
c = st.checkbox('Converter campos numéricos (inválidos tornam-se nulos)', value=True)
if st.button('Gerar prévia de tratamento', type='primary'):
    st.session_state.clean_preview = clean_data(df, a, b, c)
if 'clean_preview' in st.session_state:
    preview = st.session_state.clean_preview
    st.subheader('Prévia da cópia tratada')
    st.caption('Edite a cópia abaixo. As alterações são usadas na exportação e ativação.')
    edited = st.data_editor(preview, num_rows='dynamic', hide_index=True, width='stretch', key=f"clean_editor_{st.session_state.get('editor_revision', 0)}")
    st.caption(f'{len(edited)} linhas · {int(edited.isna().sum().sum())} células nulas · {int(edited.duplicated().sum())} duplicatas completas na cópia atual.')
    left, right = st.columns(2)
    left.download_button('Baixar CSV tratado', csv_bytes(edited), 'dados_tratados.csv', 'text/csv')
    right.download_button('Baixar Excel tratado', excel_bytes({'Dados tratados': edited}), 'dados_tratados.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if st.button('Validar e usar cópia tratada no dashboard'):
        try:
            ready = prepare_sales(edited)
            st.session_state.sales = ready
            st.session_state.source = st.session_state.get('import_name', 'Demonstração') + ' • tratada'
            st.session_state.working_data = ready.copy(deep=True)
            st.session_state.clean_preview = ready.copy(deep=True)
            st.session_state.editor_revision = st.session_state.get('editor_revision', 0) + 1
            st.session_state.flash_message = 'Cópia validada e ativada. O original permanece preservado.'
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
else:
    st.dataframe(df.head(100), hide_index=True, width='stretch')
