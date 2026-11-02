import pandas as pd
import pytest
from src.data_cleaning import clean_data, quality_table, numeric_value
from src.data_generator import generate_sales
from src.data_loader import prepare_sales

@pytest.mark.parametrize('value,expected', [('R$ 1.234,56', 1234.56), ('1234.56', 1234.56), (10, 10), ('1,25', 1.25)])
def test_numbers(value, expected):
    assert numeric_value(value) == expected

def test_copy_duplicates_dates_and_nulls():
    source = pd.DataFrame({'Data': ['31/01/2024', '31/01/2024', 'inválida', '2024-02-01'], 'Quantidade': ['2', '2', 'erro', '3']})
    original = source.copy(deep=True)
    clean = clean_data(source)
    pd.testing.assert_frame_equal(source, original)
    assert len(clean) == 3
    assert clean.Data.iloc[0] == pd.Timestamp('2024-01-31')
    assert clean.Data.iloc[2] == pd.Timestamp('2024-02-01')
    assert clean.Data.isna().sum() == 1
    assert quality_table(clean).Nulos.sum() == 2

@pytest.mark.parametrize('column,value', [('Quantidade', -1), ('Quantidade', 1.5), ('Preço unitário', 'inf'), ('Data', 'ruim'), ('Categoria', ' '), ('Custo unitário', None)])
def test_invalid_sales_rejected(column, value):
    df = generate_sales(4).astype({column: 'object'})
    df.loc[0, column] = value
    with pytest.raises(ValueError, match='inválido'):
        prepare_sales(df)

def test_recalculate_and_duplicate_id():
    df = generate_sales(4)
    df['Receita'] = 1
    assert prepare_sales(df).Receita.iloc[0] != 1
    df.loc[1, 'ID da venda'] = df.loc[0, 'ID da venda']
    with pytest.raises(ValueError, match='IDs'):
        prepare_sales(df)

def test_timezone_dates_and_empty_base():
    df = generate_sales(2)
    df['Data'] = ['2024-01-31T23:30:00-03:00', '01/02/2024']
    ready = prepare_sales(df)
    assert ready.Data.iloc[0] == pd.Timestamp('2024-01-31')
    assert ready.Data.iloc[1] == pd.Timestamp('2024-02-01')
    with pytest.raises(ValueError, match='pelo menos'):
        prepare_sales(df.iloc[:0])
