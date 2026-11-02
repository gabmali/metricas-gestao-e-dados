"""Vendas sintéticas reproduzíveis; nenhum dado pessoal real."""
from pathlib import Path
import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'vendas_ficticias.csv'

def generate_sales(n=2400, seed=42):
    rng = np.random.default_rng(seed)
    products = np.array(['Notebook', 'Monitor', 'Teclado', 'Mouse', 'Cadeira', 'Mesa', 'Luminária', 'Estante'])
    prices = np.array([3500, 1100, 180, 90, 850, 650, 120, 450])
    idx = rng.integers(0, len(products), n)
    df = pd.DataFrame({
        'ID da venda': [f'VD{i:05d}' for i in range(1, n+1)],
        'Data': pd.Timestamp('2024-01-01') + pd.to_timedelta(rng.integers(0, 731, n), unit='D'),
        'Produto': products[idx],
        'Categoria': np.where(idx < 4, 'Tecnologia', 'Escritório'),
        'Região': rng.choice(['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'], n),
        'Quantidade': rng.integers(1, 9, n),
        'Preço unitário': np.round(prices[idx] * rng.uniform(.9, 1.1, n), 2),
    })
    df['Custo unitário'] = (df['Preço unitário'] * rng.uniform(.5, .8, n)).round(2)
    df['Receita'] = (df['Quantidade'] * df['Preço unitário']).round(2)
    df['Custo total'] = (df['Quantidade'] * df['Custo unitário']).round(2)
    df['Lucro'] = (df['Receita'] - df['Custo total']).round(2)
    return df.sort_values('Data').reset_index(drop=True)

if __name__ == '__main__':
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    generate_sales().to_csv(DATA_PATH, index=False, date_format='%Y-%m-%d')
