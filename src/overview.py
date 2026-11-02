import streamlit as st
from src.ui import setup, filtered, metrics
from src.charts import chart

setup('Visão geral', 'Seu negócio em perspectiva • indicadores e resultados do período')
df, _ = filtered()
metrics(df)
if df.empty:
    st.info('Nenhuma venda encontrada. Ajuste os filtros na barra lateral.')
else:
    st.subheader('Evolução do negócio')
    st.plotly_chart(chart(df, 'Evolução mensal'), width='stretch', config={'displayModeBar': False, 'scrollZoom': False})
    left, right = st.columns(2)
    with left:
        st.subheader('Receita por categoria')
        st.plotly_chart(chart(df, 'Categorias'), width='stretch', config={'displayModeBar': False, 'scrollZoom': False})
    with right:
        st.subheader('Produtos em destaque')
        st.plotly_chart(chart(df, 'Ranking'), width='stretch', config={'displayModeBar': False, 'scrollZoom': False})
    with st.expander('Explorar registros do período'):
        st.dataframe(df, hide_index=True, width='stretch')
