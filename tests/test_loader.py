from io import BytesIO
import pandas as pd
import pytest
from src.data_loader import load_file, validate_file, excel_sheets, map_columns, REQUIRED, MAX_BYTES
from src.data_generator import generate_sales

def test_csv_encodings_and_separator():
    df = generate_sales(5)
    for encoding in ['utf-8-sig', 'cp1252']:
        content = df.to_csv(index=False, sep=';', decimal=',').encode(encoding)
        loaded = load_file('vendas.csv', content)
        assert len(loaded) == 5 and 'Região' in loaded

def test_excel_select_sheet():
    data = BytesIO()
    with pd.ExcelWriter(data, engine='openpyxl') as writer:
        pd.DataFrame({'A': [1]}).to_excel(writer, sheet_name='Outra', index=False)
        generate_sales(7).to_excel(writer, sheet_name='Vendas', index=False)
    assert excel_sheets(data.getvalue()) == ['Outra', 'Vendas']
    assert len(load_file('dados.xlsx', data.getvalue(), 'Vendas')) == 7

@pytest.mark.parametrize('name,content', [('dados.txt', b'abc'), ('dados.csv', b''), ('dados.xlsx', b'corrompido')])
def test_bad_files(name, content):
    with pytest.raises(ValueError):
        load_file(name, content)

def test_size_and_mapping():
    with pytest.raises(ValueError):
        validate_file('dados.csv', b'0' * (MAX_BYTES + 1))
    df = generate_sales(3)
    result = map_columns(df, {col: col for col in REQUIRED})
    assert list(result.columns) == REQUIRED
    with pytest.raises(ValueError):
        map_columns(df, {col: 'Data' for col in REQUIRED})
