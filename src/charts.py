import plotly.express as px
from math import ceil
from src.analytics import grouped, monthly

COLORS = ['#17324D', '#31734E', '#648674', '#5A768C', '#A5CDB3']

def chart(df, kind):
    if kind == 'Evolução mensal':
        fig = px.line(monthly(df), x='Mês', y=['Receita', 'Lucro'], markers=True, color_discrete_sequence=COLORS)
        fig.update_yaxes(title='Valor (R$)')
        table = monthly(df)
        ticks = table.iloc[::max(1, ceil(len(table) / 6))]
        fig.update_xaxes(tickmode='array', tickvals=ticks['Mês'], ticktext=ticks['Mês'].dt.strftime('%m/%Y') if not ticks.empty else [])
        fig.update_traces(hovertemplate='%{x|%m/%Y}<br>Valor: R$ %{y:,.2f}<extra>%{fullData.name}</extra>')
    elif kind == 'Categorias':
        fig = px.bar(grouped(df, 'Categoria'), x='Categoria', y='Receita', color='Categoria', color_discrete_sequence=COLORS)
    elif kind == 'Participação regional':
        fig = px.pie(grouped(df, 'Região'), names='Região', values='Receita', hole=.6, color_discrete_sequence=COLORS)
    elif kind == 'Dispersão':
        fig = px.scatter(df, x='Receita', y='Lucro', color='Categoria', hover_data=['Produto', 'Quantidade'], color_discrete_sequence=COLORS)
    else:
        fig = px.bar(grouped(df, 'Produto').head(10).sort_values('Receita'), x='Receita', y='Produto', orientation='h', color_discrete_sequence=COLORS)
    fig.update_layout(template='plotly_white', colorway=COLORS, paper_bgcolor='rgba(0,0,0,0)',
                      font_color='#17324D', plot_bgcolor='#F3F5F4', margin=dict(l=10, r=10, t=20, b=10), legend_title_text='',
                      separators=',.', legend=dict(orientation='h', yanchor='bottom', y=1.02, x=0))
    if kind != 'Participação regional':
        fig.update_yaxes(tickformat=',.0f')
        if kind not in ['Evolução mensal', 'Categorias']:
            fig.update_xaxes(tickformat=',.0f')
    return fig
