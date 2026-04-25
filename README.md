# Football Player Performance Analysis

## Descrição
Este projeto analisa o desempenho de jogadores de futebol profissional europeu usando dados do European Soccer Database (Kaggle). O foco é identificar jogadores eficientes, entender a evolução temporal, analisar atributos influenciadores e definir o perfil ideal de jogador.

## Dados
- Dataset: European Soccer Database (temporadas 2008-2016)
- Inclui: +25.000 partidas, +10.000 jogadores, atributos do FIFA, odds de apostas, etc.

## Objetivos da Análise
- Quem são os jogadores mais eficientes?
- Como a evolução acontece ao longo do tempo?
- Quais atributos influenciam o desempenho?
- Qual é o perfil ideal de jogador?

## Estrutura do Projeto
- `data/raw/`: Dados brutos (database.sqlite)
- `data/processed/`: Dados processados para dashboards
- `notebooks/`: Notebooks de análise e exploração
- `dashboards/`: Dashboards em Streamlit e Power BI
- `reports/`: Relatórios e insights
- `src/`: Código fonte adicional
- `sql/`: Consultas SQL

## Como Usar
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute o notebook principal: `notebooks/analysis/analysis_pipeline.ipynb`
3. Para dashboards: Acesse `dashboards/streamlit/` ou abra arquivos Power BI

## Dashboards
- **Streamlit**: Dashboard interativo em Python
- **Power BI**: Visualizações avançadas

## Insights Principais
- Jogadores elite (>85 rating) se destacam em reações, passe curto e controle de bola
- Idade ideal: 28-32 anos
- Atributos chave: reações, visão, drible

## Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.