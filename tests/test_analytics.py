import pandas as pd
import pytest
from src.data_generator import generate_sales
from src.analytics import indicators, filter_sales, grouped, monthly
from src.reports import report_tables, excel_bytes, csv_bytes, observations
from io import BytesIO

def test_generator_reproducible_and_finances():
    df = generate_sales()
    pd.testing.assert_frame_equal(df, generate_sales())
    assert len(df) >= 2000 and df['ID da venda'].is_unique
    assert (df.Receita == (df.Quantidade * df['Preço unitário']).round(2)).all()
    assert (df.Lucro == (df.Receita - df['Custo total']).round(2)).all()

def test_known_indicators():
    df = pd.DataFrame({'Receita': [100., 300.], 'Lucro': [20., 90.]})
    assert indicators(df) == {'Receita total': 400., 'Quantidade de vendas': 2, 'Ticket médio': 200., 'Lucro estimado': 110.}
    assert all(v == 0 for v in indicators(df.iloc[:0]).values())

def test_filters_and_totals():
    df = generate_sales()
    result = filter_sales(df, '2024-01-01', '2024-01-31', ['Sul'], ['Tecnologia'])
    assert not result.empty
    assert result.Data.between('2024-01-01', '2024-01-31').all()
    assert result['Região'].eq('Sul').all()
    assert result.Categoria.eq('Tecnologia').all()
    assert filter_sales(df, regions=[]).empty
    assert grouped(df, 'Categoria').Receita.sum() == pytest.approx(df.Receita.sum())
    assert monthly(df).Receita.sum() == pytest.approx(df.Receita.sum())

def test_monthly_zero_baseline():
    df = generate_sales(2)
    df['Data'] = pd.to_datetime(['2024-01-01', '2024-03-01'])
    table = monthly(df)
    assert len(table) == 3
    assert table.iloc[1].Receita == 0
    assert pd.isna(table.iloc[2]['Variação receita (%)'])

def test_report_roundtrip():
    df = generate_sales(20)
    tables = report_tables(df, 'Teste Sul')
    exported = pd.read_excel(BytesIO(excel_bytes(tables)), sheet_name=None)
    assert set(exported) == set(tables)
    assert len(exported['Vendas']) == 20
    assert exported['Indicadores'].iloc[0].Valor == pytest.approx(df.Receita.sum())
    assert len(pd.read_csv(BytesIO(csv_bytes(df)), sep=';', decimal=',')) == 20
    assert observations(df.iloc[:0]) == ['Nenhuma venda no recorte selecionado.']

def test_export_formula_neutralized():
    df = pd.DataFrame({'Produto': ['=1+1', ' @SUM(A1)', 'Normal']})
    result = pd.read_excel(BytesIO(excel_bytes({'Dados': df})))
    assert result.iloc[0, 0] == "'=1+1"
