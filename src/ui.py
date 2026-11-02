from pathlib import Path
import streamlit as st
import pandas as pd
from src.data_generator import generate_sales, DATA_PATH
from src.data_loader import prepare_sales
from src.analytics import filter_sales, indicators
from html import escape
from datetime import datetime

def setup(title, subtitle):
    st.set_page_config(page_title=f'{title} • Métricas Gestão e Dados', page_icon='📊', layout='wide')
    st.markdown('''<style>
    .block-container{padding-top:2rem;max-width:1500px}
    [data-testid="stAppViewContainer"], [data-testid="stHeader"]{background:#F3F5F4}
    [data-testid="stMetric"]{background:#E6F4EA;border:1px solid #BDD8C6;border-radius:14px;padding:18px}
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] p{font-size:clamp(1rem,1.35vw,1.65rem)!important;letter-spacing:-.03em}
    .dv-metrics{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:16px 0}
    .dv-card{background:#E6F4EA;border:1px solid #BDD8C6;border-top:4px solid #17324D;border-radius:14px;padding:20px;min-width:0;color:#17324D}
    .dv-card-label{font-size:14px;line-height:1.5;overflow-wrap:anywhere;color:#304C43}
    .dv-card-value{font-size:24px;font-weight:600;line-height:1.5;overflow-wrap:anywhere;color:#17324D}
    [data-testid="stSidebar"]{background:#EDF2EF}
    [data-testid="stSidebarNav"] a[aria-current="page"]{background:#D9EEDD;color:#17324D}
    [data-testid="stCaptionContainer"]{color:#465B55}
    button[kind="primary"]{background:#17324D!important;color:white!important;border-color:#17324D!important}
    button[kind="secondary"]{background:white;color:#17324D;border-color:#BDD8C6}
    button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #31734E!important;outline-offset:2px}
    [data-testid="stHorizontalBlock"]{flex-wrap:wrap}
    [data-testid="stHorizontalBlock"]>[data-testid="stColumn"]{flex:1 1 280px!important;min-width:min(100%,280px)!important}
    [data-testid="stElementToolbar"]{display:none!important}
    [data-testid="stFileUploaderDropzone"] button[kind="secondary"]>div{display:none!important}
    [data-testid="stFileUploaderDropzone"] button[kind="secondary"]::after{content:'Selecionar arquivo';font-size:14px}
    [data-testid="stFileChipDeleteBtn"], [data-testid="stFileUploaderDropzone"] button[aria-label="Add files"]{display:none!important}
    [data-testid="stFileUploaderDropzoneInstructions"]>div{display:none!important}
    [data-testid="stFileUploaderDropzoneInstructions"]::after{content:'Até 20 MB por arquivo • CSV ou XLSX';font-size:14px}
    @media(min-width:1450px){.dv-metrics{grid-template-columns:repeat(4,minmax(0,1fr))}}
    @media(max-width:600px){.dv-metrics{grid-template-columns:1fr}}
    @media(max-width:600px){.block-container{padding:1.5rem 1rem}h1{font-size:2rem!important}}
    h1,h2,h3{color:#17324D} [data-testid="stSidebar"]{border-right:1px solid #CCD8D0}
    </style>''', unsafe_allow_html=True)
    st.sidebar.markdown('## ◈ Métricas\n**Gestão e Dados**')
    st.sidebar.caption('Explore. Entenda. Decida.')
    if 'sales' not in st.session_state:
        demo = pd.read_csv(DATA_PATH) if DATA_PATH.exists() else generate_sales()
        st.session_state.sales = prepare_sales(demo)
        st.session_state.source = 'Demonstração • dados fictícios'
    st.sidebar.divider()
    st.sidebar.caption('BASE ATIVA')
    st.sidebar.write(st.session_state.source)
    st.sidebar.caption(f'{len(st.session_state.sales):,} vendas válidas'.replace(',', '.'))
    if st.sidebar.button('Restaurar demonstração', width='stretch'):
        st.session_state.sales = generate_sales()
        st.session_state.source = 'Demonstração • dados fictícios'
        for key in ['working_data', 'raw_data', 'clean_preview', 'import_name']:
            st.session_state.pop(key, None)
        st.rerun()
    st.title(title)
    st.caption(subtitle)
    if 'flash_message' in st.session_state:
        st.success(st.session_state.pop('flash_message'))

def filtered():
    df = st.session_state.sales
    st.sidebar.subheader('Filtros de análise')
    st.sidebar.caption('Período • dia/mês/ano')
    start = st.sidebar.text_input('Data inicial', value=df.Data.min().strftime('%d/%m/%Y'))
    end = st.sidebar.text_input('Data final', value=df.Data.max().strftime('%d/%m/%Y'))
    try:
        period = (datetime.strptime(start, '%d/%m/%Y').date(), datetime.strptime(end, '%d/%m/%Y').date())
    except ValueError:
        st.info('Digite datas válidas no formato DD/MM/AAAA e pressione Enter.')
        st.stop()
    if period[0] > period[1]:
        st.info('A data inicial deve ser anterior ou igual à data final.')
        st.stop()
    regions = st.sidebar.multiselect('Região', sorted(df['Região'].unique()), default=sorted(df['Região'].unique()))
    cats = st.sidebar.multiselect('Categoria', sorted(df['Categoria'].unique()), default=sorted(df['Categoria'].unique()))
    if len(period) != 2:
        st.info('Selecione a data inicial e a final.')
        st.stop()
    result = filter_sales(df, *period, regions, cats)
    context = f'{period[0]} a {period[1]} | Regiões: {", ".join(regions) or "nenhuma"} | Categorias: {", ".join(cats) or "nenhuma"}'
    label = 'venda' if len(result) == 1 else 'vendas'
    st.caption(f'{len(result):,} {label} no recorte · {period[0]:%d/%m/%Y} — {period[1]:%d/%m/%Y}'.replace(',', '.'))
    return result, context

def money(value):
    return 'R$ ' + f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def metrics(df):
    cards = []
    for name, value in indicators(df).items():
        display = f'{value:,}'.replace(',', '.') if name == 'Quantidade de vendas' else money(value)
        cards.append(f'<div class="dv-card"><div class="dv-card-label">{escape(name)}</div><div class="dv-card-value">{escape(display)}</div></div>')
    st.markdown('<section class="dv-metrics" aria-label="Indicadores de vendas">'+''.join(cards)+'</section>', unsafe_allow_html=True)
    st.caption('Cada linha representa uma venda. Lucro estimado = receita − custo dos produtos; não inclui impostos e despesas operacionais.')
