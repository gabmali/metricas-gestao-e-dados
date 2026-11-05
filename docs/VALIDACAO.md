# Validação local

- Ambiente: Windows, Python 3.12.14, dependências em `requirements-lock.txt`.
- `python -m pytest`: 36 testes aprovados na revisão final de interface.
- `python -m pip check`: nenhuma dependência incompatível.
- Inicialização: `python -m streamlit run app.py --server.headless=true --server.address=127.0.0.1 --server.port=8502`.
- Saúde HTTP: `GET /_stcore/health` retornou `200`, conteúdo `ok`.
- Dashboard inspecionado no navegador; captura em `screenshots/visao-geral.jpg`.
- Testes de interface: seis páginas, filtro vazio e tratamento/ativação de uma cópia importada via Streamlit AppTest.
- CSV, Excel, seleção de aba e exportações validados por testes automatizados. Upload de Excel, seleção da aba Vendas, ativação da base e confirmação da limpeza também exercitados pelo navegador.
- Git inicializado localmente na branch `main`. Nenhum envio para GitHub ou deploy realizado.

No ambiente de desenvolvimento, testes de interface e servidor precisaram de execução fora do isolamento de rede para habilitar os servidores locais internos do Streamlit. Python padrão do terminal era 3.7; o projeto usa o Python 3.12 do ambiente virtual.

## Revisão de interface e responsividade

- Cartões de indicadores com grade responsiva, texto integral e quebra de linha quando necessário, sem reticências.
- Verificação no navegador Chromium integrado nas larguras de 390, 870 e 1440 pixels. Não houve rolagem horizontal global nas verificações de cartões e gráficos; as tabelas mantêm rolagem interna para suas colunas.
- Gráficos em colunas que se empilham quando o espaço disponível diminui; legendas horizontais e rótulos de datas numéricos em português brasileiro.
- Filtros de datas com campos DD/MM/AAAA e mensagens em português para datas inválidas e períodos invertidos.
- Textos visíveis de importação, tipos de dados, valores monetários e observações revisados. Barras de ferramentas nativas com comandos em inglês ocultadas; download continua disponível pelos botões da aplicação.
- Alguns nomes internos de acessibilidade dos componentes Streamlit, como abrir/fechar a barra lateral, continuam definidos pelo framework em inglês. A verificação não inclui leitores de tela, outros navegadores ou dispositivos físicos.
- Limpeza agora atualiza imediatamente a base ativa, contagem de registros, nulos e duplicatas após ativação, preservando o original. Teste de regressão automatizado adicionado e confirmação também verificada no navegador com 30 vendas tratadas.
- Base tratada reimportada do relatório completo após reinicialização do servidor. Os totais continuam em 30 vendas e R$ 81.150,00 de receita.
- Capturas: `screenshots/qa-390.jpg`, `screenshots/qa-870.jpg`, `screenshots/qa-1440.jpg`.
- Menu lateral móvel verificado abrindo e fechando os filtros. Evidência final em `screenshots/qa-final-celular.jpg`.
- O limite padrão de 3 segundos do AppTest causou duas expirações em uma rodada concorrente com o navegador. Os testes de interface agora usam limite de 30 segundos; a última execução completa terminou com 36 testes aprovados em 18,25 segundos.
- A instância auxiliar de QA foi encerrada; a aplicação principal permanece disponível em http://127.0.0.1:8501.

## Atualização de cores

Paleta alterada para verde claro, cinza claro e azul escuro. Contrastes calculados: azul escuro sobre verde claro 11,56:1; rótulos verde-escuros sobre verde claro 8,25:1; legendas sobre cinza claro 6,64:1; branco sobre azul escuro 13,13:1. São verificações desses pares de cores, não uma auditoria integral de acessibilidade. Tema conferido no navegador com os dados tratados. Após a alteração, 36 testes passaram em 18,92 segundos.

## QA após mudança de marca — 02/11/2026

- Marca atual: Métricas Gestão e Dados. Verificados menu compartilhado, títulos das páginas, Sobre e nome do relatório Excel.
- Suíte completa: 36 testes aprovados em 17,55 segundos.
- Acrescentadas verificações da nova marca e ausência da marca anterior no menu das seis páginas. Os 11 testes de interface passaram novamente em 17,67 segundos após essa alteração.
- `python -m pip check`: nenhuma dependência incompatível.
- Busca em src, pages, app.py e configuração: nenhuma referência à marca DataVision.
- O bloqueio da execução anterior foi resolvido executando AppTest com acesso aos servidores internos locais do Streamlit fora do isolamento. Não foi necessário alterar a lógica da aplicação.
- Arquivos já importados ou exportados anteriormente preservam seu nome original; novos relatórios usam relatorio_metricas_gestao_e_dados.xlsx.

## Versão GitHub Pages

- Aplicação estática em web/ com seis páginas, paleta preservada, dados processados no navegador e bibliotecas locais.
- Oito testes Node aprovados: datas, números, limpeza sem mutação, validação, filtros, consolidação mensal, 2.400 vendas e exportação/reimportação Excel.
- Navegador: importação da aba Vendas_para_limpar, remoção de 3 duplicatas, correção dos sete campos e ativação de 30 vendas.
- Edição corrigida para registrar valores ao digitar; quantidade zero rejeitada e cópia corrigida aceita.
- Recorte Tecnologia/Sul: 3 vendas, receita R$ 1.200, ticket R$ 400 e lucro R$ 480.
- Excel baixado pela interface e aberto com OpenPyXL: oito abas, indicadores do recorte corretos e três vendas.
- Dados importados ficam apenas na memória da aba; recarregar descarta a sessão.

- Responsividade da versão estática conferida no Chromium integrado em 1440 e 390 pixels; largura dos componentes sem overflow global. A publicação GitHub Pages concluiu com sucesso e o endereço público retornou HTTP 200 sem autenticação.
