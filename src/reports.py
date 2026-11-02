from io import BytesIO
import pandas as pd
from src.analytics import indicators, grouped, monthly

def br_number(value):
    return f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def observations(df):
    if df.empty:
        return ['Nenhuma venda no recorte selecionado.']
    kpi = indicators(df)
    leader = grouped(df, 'Categoria').iloc[0]
    notes = [f"Categoria com maior receita: {leader['Categoria']} (R$ {br_number(leader['Receita'])}).",
             f"Margem de lucro: {br_number(100*kpi['Lucro estimado']/kpi['Receita total'])}%." if kpi['Receita total'] else 'Margem não calculada: receita igual a zero.']
    months = monthly(df)
    if len(months) >= 2:
        delta = months.iloc[-1]['Variação receita (%)']
        notes.append(f'Variação entre os dois últimos meses do recorte: {br_number(delta)}%.' if pd.notna(delta) else 'Variação mensal indisponível: base anterior igual a zero.')
    return notes

def safe_export(df):
    """Neutraliza fórmulas em textos de arquivos importados ao exportar."""
    result = df.copy()
    for col in result.select_dtypes(include=['object', 'string']).columns:
        result[col] = result[col].map(lambda x: "'" + x if isinstance(x, str) and x.lstrip().startswith(('=', '+', '-', '@')) else x)
    return result

def csv_bytes(df):
    return safe_export(df).to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')

def excel_bytes(tables):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for name, df in tables.items():
            safe_export(df).to_excel(writer, sheet_name=name[:31], index=False)
    return buffer.getvalue()

def report_tables(df, context='Todos os dados'):
    return {'Indicadores': pd.DataFrame(indicators(df).items(), columns=['Indicador', 'Valor']),
            'Mensal': monthly(df), 'Categorias': grouped(df, 'Categoria'),
            'Regiões': grouped(df, 'Região'), 'Produtos': grouped(df, 'Produto'),
            'Observações': pd.DataFrame({'Observação': observations(df)}),
            'Recorte': pd.DataFrame({'Filtros': [context], 'Gerado em UTC': [pd.Timestamp.now(tz='UTC').isoformat()]}),
            'Vendas': df}
