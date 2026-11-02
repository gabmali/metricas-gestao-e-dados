import streamlit as st
from src.ui import setup, filtered, metrics
from src.reports import report_tables, observations, csv_bytes, excel_bytes

setup('Relatórios', 'Resultados verificáveis e exportações para compartilhar')
df, context = filtered()
metrics(df)
st.subheader('Principais resultados')
for note in observations(df):
    st.write('• ' + note)
st.caption('Observações descritivas por regras matemáticas, sem inferência causal. A comparação mensal usa os dois últimos meses observados; podem ser parciais.')
tables = report_tables(df, context)
for name in ['Mensal', 'Categorias', 'Regiões', 'Produtos']:
    with st.expander(name):
        st.dataframe(tables[name], hide_index=True, width='stretch')
st.download_button('Exportar relatório completo em Excel', excel_bytes(tables), 'relatorio_metricas_gestao_e_dados.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', type='primary')
choice = st.selectbox('Tabela para exportação CSV', list(tables))
st.download_button('Exportar tabela em CSV', csv_bytes(tables[choice]), f'relatorio_{choice}.csv', 'text/csv')
