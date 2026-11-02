from io import BytesIO
from pathlib import Path
import pandas as pd
import numpy as np
from src.data_cleaning import clean_data

REQUIRED = ['ID da venda', 'Data', 'Produto', 'Categoria', 'Região', 'Quantidade', 'Preço unitário', 'Custo unitário']
MAX_BYTES = 20 * 1024 * 1024

def validate_file(name, content):
    if Path(name).suffix.lower() not in {'.csv', '.xlsx'}:
        raise ValueError('Envie um arquivo CSV ou XLSX.')
    if not content or len(content) > MAX_BYTES:
        raise ValueError('O arquivo deve ter conteúdo e no máximo 20 MB.')

def excel_sheets(content):
    try:
        return pd.ExcelFile(BytesIO(content), engine='openpyxl').sheet_names
    except Exception as exc:
        raise ValueError('Não foi possível abrir o Excel. Verifique se está íntegro e sem senha.') from exc

def load_file(name, content, sheet_name=0):
    validate_file(name, content)
    try:
        if name.lower().endswith('.xlsx'):
            df = pd.read_excel(BytesIO(content), sheet_name=sheet_name, engine='openpyxl')
        else:
            try:
                text = content.decode('utf-8-sig')
            except UnicodeDecodeError:
                text = content.decode('cp1252')
            from io import StringIO
            df = pd.read_csv(StringIO(text), sep=None, engine='python')
        if df.empty or df.columns.duplicated().any():
            raise ValueError('A planilha deve ter registros e nomes de colunas únicos.')
        return df
    except Exception as exc:
        raise ValueError(f'Falha na leitura: {exc}') from exc

def map_columns(df, mapping):
    if set(mapping) != set(REQUIRED) or len(set(mapping.values())) != len(REQUIRED):
        raise ValueError('Selecione uma coluna diferente para cada campo obrigatório.')
    if any(value not in df.columns for value in mapping.values()):
        raise ValueError('Uma coluna selecionada não existe na planilha.')
    return df[list(mapping.values())].rename(columns={v: k for k, v in mapping.items()}).copy()

def prepare_sales(df):
    if df.empty:
        raise ValueError('A base deve conter pelo menos uma venda válida.')
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError('Colunas ausentes: ' + ', '.join(sorted(missing)))
    result = clean_data(df, remove_duplicates=False)
    invalid = result[REQUIRED].isna().any(axis=1)
    for col in ['Produto', 'Categoria', 'Região', 'ID da venda']:
        invalid |= result[col].astype(str).str.strip().eq('')
    invalid |= (result[['Quantidade', 'Preço unitário', 'Custo unitário']] < 0).any(axis=1)
    invalid |= result['Quantidade'].le(0) | result['Quantidade'].mod(1).ne(0)
    if invalid.any():
        raise ValueError(f'{int(invalid.sum())} registro(s) inválido(s). Corrija nulos, datas, quantidades inteiras positivas e valores não negativos na página Limpeza.')
    result['ID da venda'] = result['ID da venda'].astype(str).str.strip()
    if result['ID da venda'].duplicated().any():
        raise ValueError('IDs de venda repetidos. Cada linha deve representar uma venda única.')
    for col in ['Produto', 'Categoria', 'Região']:
        result[col] = result[col].astype(str).str.strip()
    result['Receita'] = (result['Quantidade'] * result['Preço unitário']).round(2)
    result['Custo total'] = (result['Quantidade'] * result['Custo unitário']).round(2)
    result['Lucro'] = (result['Receita'] - result['Custo total']).round(2)
    if not np.isfinite(result[['Receita', 'Custo total', 'Lucro']].to_numpy(dtype=float)).all():
        raise ValueError('Valores financeiros excedem o limite numérico. Revise os valores importados.')
    return result
