import hashlib
import streamlit as st
from src.ui import setup
from src.data_loader import REQUIRED, validate_file, excel_sheets, load_file, map_columns, prepare_sales

setup('Importação de dados', 'CSV ou Excel • até 20 MB • processamento apenas nesta sessão')
st.info('Cada linha deve representar uma venda única. Receita, custo total e lucro serão recalculados a partir da quantidade e dos valores unitários. Datas: DD/MM/AAAA ou ISO. Decimais: ponto ou vírgula brasileira.')
upload = st.file_uploader('Escolha sua planilha', type=['csv', 'xlsx'], key=f"upload_{st.session_state.get('upload_revision', 0)}")
if upload:
    if st.button('Selecionar outro arquivo'):
        st.session_state.upload_revision = st.session_state.get('upload_revision', 0) + 1
        st.rerun()
    try:
        content = upload.getvalue()
        validate_file(upload.name, content)
        sheet = st.selectbox('Aba do Excel', excel_sheets(content)) if upload.name.lower().endswith('.xlsx') else 0
        df = load_file(upload.name, content, sheet)
        st.subheader('Prévia do arquivo')
        st.dataframe(df.head(50), hide_index=True, width='stretch')
        st.caption(f'{len(df)} linhas · {len(df.columns)} colunas · prévia limitada a 50 linhas')
        st.subheader('Mapear colunas obrigatórias')
        mapping = {}
        identity = hashlib.sha256(content).hexdigest()[:12] + str(sheet)
        for field in REQUIRED:
            choices = list(df.columns)
            mapping[field] = st.selectbox(field, choices, index=choices.index(field) if field in choices else None, key=f'{identity}_{field}', placeholder='Selecione a coluna')
        if st.button('Confirmar mapeamento e preparar dados', type='primary'):
            mapped = map_columns(df, mapping)
            st.session_state.raw_data = df.copy(deep=True)
            st.session_state.working_data = mapped.copy(deep=True)
            st.session_state.editor_revision = st.session_state.get('editor_revision', 0) + 1
            st.session_state.pop('clean_preview', None)
            st.session_state.import_name = upload.name
            st.success('Cópia de trabalho criada. O arquivo original foi preservado na sessão.')
            try:
                ready = prepare_sales(mapped)
                st.session_state.sales = ready
                st.session_state.source = upload.name
                st.session_state.flash_message = 'Base validada e ativada nos painéis.'
                st.rerun()
            except ValueError as exc:
                st.warning(str(exc))
                st.page_link('pages/2_Limpeza.py', label='Abrir limpeza de dados')
    except ValueError as exc:
        st.error(str(exc))
