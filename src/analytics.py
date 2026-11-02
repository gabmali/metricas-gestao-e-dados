import pandas as pd

def filter_sales(df, start=None, end=None, regions=None, categories=None):
    mask = pd.Series(True, index=df.index)
    if start is not None:
        mask &= df['Data'] >= pd.Timestamp(start)
    if end is not None:
        mask &= df['Data'].dt.normalize() <= pd.Timestamp(end).normalize()
    if regions is not None:
        mask &= df['Região'].isin(regions)
    if categories is not None:
        mask &= df['Categoria'].isin(categories)
    return df.loc[mask].copy()

def indicators(df):
    revenue = float(df['Receita'].sum())
    count = len(df)
    return {'Receita total': revenue, 'Quantidade de vendas': count,
            'Ticket médio': revenue / count if count else 0.0,
            'Lucro estimado': float(df['Lucro'].sum())}

def grouped(df, column):
    return df.groupby(column, as_index=False, dropna=False)[['Receita', 'Custo total', 'Lucro', 'Quantidade']].sum().sort_values('Receita', ascending=False)

def monthly(df):
    if df.empty:
        return pd.DataFrame(columns=['Mês', 'Receita', 'Custo total', 'Lucro', 'Quantidade', 'Variação receita (%)'])
    data = df.set_index('Data')[['Receita', 'Custo total', 'Lucro', 'Quantidade']].resample('MS').sum()
    data['Variação receita (%)'] = data['Receita'].pct_change(fill_method=None).where(data['Receita'].shift().ne(0)) * 100
    data.index.name = 'Mês'
    return data.reset_index()
