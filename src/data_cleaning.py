import numbers
import numpy as np
import pandas as pd

NUMERIC = ['Quantidade', 'Preço unitário', 'Custo unitário']

def numeric_value(value):
    """Aceita números, decimal com ponto e formato brasileiro com vírgula."""
    if isinstance(value, numbers.Number):
        return value
    value = str(value).strip().replace('R$', '').replace(' ', '').replace('\u00a0', '')
    if ',' in value:
        value = value.replace('.', '').replace(',', '.')
    return pd.to_numeric(value, errors='coerce')

def parse_dates(series):
    # ISO e datas brasileiras coexistem sem inferência ambígua de mês/dia.
    def parse(value):
        if pd.isna(value):
            return pd.NaT
        if isinstance(value, numbers.Number):
            return pd.NaT
        parsed = pd.to_datetime(value, errors='coerce', dayfirst=not (isinstance(value, str) and len(value) >= 10 and value[4] == '-'))
        if pd.isna(parsed):
            return pd.NaT
        # O modelo usa dias civis, sem horário ou fuso.
        return parsed.tz_localize(None).normalize()
    return pd.to_datetime(series.map(parse))

def quality_table(df):
    def type_label(dtype):
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return 'Data'
        if pd.api.types.is_integer_dtype(dtype):
            return 'Número inteiro'
        if pd.api.types.is_numeric_dtype(dtype):
            return 'Número decimal'
        return 'Texto ou valores mistos'
    return pd.DataFrame({'Coluna': df.columns, 'Tipo': [type_label(t) for t in df.dtypes],
                         'Nulos': df.isna().sum().values})

def clean_data(df, remove_duplicates=True, dates=True, numbers=True):
    result = df.copy(deep=True)
    if remove_duplicates:
        result = result.drop_duplicates()
    if dates and 'Data' in result:
        result['Data'] = parse_dates(result['Data'])
    if numbers:
        for col in NUMERIC:
            if col in result:
                result[col] = result[col].map(numeric_value).replace([np.inf, -np.inf], np.nan)
    return result.reset_index(drop=True)
