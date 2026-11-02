import streamlit as st
from src.ui import setup

setup('Sobre o projeto', 'Métricas Gestão e Dados • portfólio de análise de dados')
st.markdown('''
### Dados que ajudam a entender resultados
Plataforma local para importar vendas, verificar qualidade, explorar indicadores e exportar relatórios, sem APIs ou banco externo.

### Como utilizar
1. Explore a demonstração com 2.400 vendas sintéticas de 2024 e 2025.
2. Importe CSV ou XLSX e mapeie os oito campos obrigatórios.
3. Na página Limpeza, gere uma prévia, corrija os valores e valide a cópia.
4. Ajuste período, região e categoria nas páginas de análise.
5. Exporte tabelas ou o relatório completo.

### Etapas de ETL
**Extração:** CSV com UTF-8 ou Windows-1252, separador detectado automaticamente; Excel com seleção de aba.
**Transformação:** mapeamento, conversão explícita de datas e números, revisão de nulos e duplicatas, validação e recálculo financeiro.
**Carga:** DataFrame mantido na sessão do Streamlit. Os uploads não são gravados pela aplicação em disco.

### Indicadores
- Receita = quantidade × preço unitário, arredondada por venda a centavos.
- Custo total = quantidade × custo unitário, arredondado a centavos.
- Lucro estimado = receita − custo total. Não inclui despesas operacionais ou impostos.
- Quantidade de vendas = número de linhas com ID único; unidades vendidas são somadas separadamente nas tabelas.
- Ticket médio = receita total ÷ quantidade de vendas; zero em recortes vazios.
- Variação mensal = (receita atual ÷ anterior − 1) × 100; indisponível com base zero.

### Tecnologias e competências
Python 3.11+, Streamlit, Pandas, NumPy, Plotly, OpenPyXL e Pytest.
O projeto demonstra ETL, qualidade de dados, agregações, visualização, comunicação de indicadores,
testes automatizados e organização de código para Git/GitHub.

### Convenções de dados
Uma linha corresponde a uma venda, com ID único. Quantidade deve ser inteira e positiva;
preço e custo devem ser finitos e não negativos. Nulos obrigatórios impedem ativação.
Datas brasileiras usam dia/mês/ano. Números com vírgula usam formato brasileiro.
Valores financeiros enviados são recalculados de forma explícita ao ativar a base.
''')
