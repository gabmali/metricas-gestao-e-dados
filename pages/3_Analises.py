import streamlit as st
from src.ui import setup, filtered
from src.charts import chart
from src.analytics import monthly, grouped

setup('Análises', 'Explore tendências, composição e relações entre receita e lucro')
df, _ = filtered()
if df.empty:
    st.info('Nenhuma venda no recorte selecionado.')
else:
    for row in [('Evolução mensal', 'Categorias'), ('Participação regional', 'Dispersão')]:
        for container, name in zip(st.columns(2), row):
            with container:
                st.subheader(name)
                st.plotly_chart(chart(df, name), width='stretch', config={'displayModeBar': False, 'scrollZoom': False})
    st.subheader('Top 10 produtos por receita')
    st.plotly_chart(chart(df, 'Ranking'), width='stretch', config={'displayModeBar': False, 'scrollZoom': False})
    st.subheader('Desempenho regional')
    st.dataframe(grouped(df, 'Região'), hide_index=True, width='stretch')
    st.subheader('Comparações mensais')
    st.caption('Meses sem vendas dentro do intervalo observado recebem zero. Os meses inicial e final podem ser parciais conforme o filtro.')
    st.dataframe(monthly(df), hide_index=True, width='stretch')
