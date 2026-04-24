# Football Player Performance Dashboard

Dashboard interativo em Streamlit para análise de desempenho de jogadores de futebol baseado nos dados do European Soccer Database.

## 📊 Funcionalidades

### 🏠 Visão Geral
- KPIs principais (total de jogadores, rating médio, maior crescimento, jogadores elite)
- Distribuição de rating dos jogadores
- Evolução temporal do rating médio
- Top 5 atributos mais determinantes

### 👤 Análise por Jogador
- Seleção interativa de jogadores
- Filtros por período (anos)
- Evolução individual do rating ao longo do tempo
- Perfil completo de atributos técnicos

### 📈 Tendências Temporais
- Evolução do rating médio por ano (2008-2016)
- Estatísticas anuais detalhadas
- Distribuição de rating por ano

### 🎯 Análise de Atributos
- Correlação dos atributos com overall rating
- Scatter plots interativos entre atributos
- Comparação Elite vs. Média Geral

### ⭐ Top Performers
- Ranking dos 10 jogadores com maior crescimento
- Distribuição estatística do crescimento
- Métricas de performance

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Dados exportados do notebook de análise

### Instalação e Execução

#### Opção 1: Script Automático (Windows)
```bash
# Execute o script de inicialização
run_dashboard.bat
```

#### Opção 2: Comando Manual
1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar o dashboard:**
   ```bash
   streamlit run app.py
   ```

3. **Acessar no navegador:**
   - O Streamlit abrirá automaticamente em `http://localhost:8501`

### 📁 Estrutura dos Dados

O dashboard utiliza 4 arquivos CSV da pasta `../../data/processed/`:

- `player_evolution_final.csv` - Base principal com histórico completo
- `top_players_growth.csv` - Ranking de crescimento dos jogadores
- `rating_trends_by_year.csv` - Tendências temporais
- `top_attributes_correlation.csv` - Correlações de atributos

## 🎨 Tecnologias Utilizadas

- **Streamlit** - Framework web para dashboards
- **Plotly** - Gráficos interativos
- **Pandas** - Manipulação de dados
- **Matplotlib/Seaborn** - Visualizações estáticas
- **NumPy** - Computações numéricas

## 📈 Insights Principais

- **Evolução Temporal**: Tendência geral de melhoria no rating médio dos jogadores
- **Atributos Críticos**: Reactions, ball_control e vision são os mais determinantes
- **Perfil Elite**: Jogadores acima de 85 têm diferenças significativas em atributos técnicos
- **Crescimento**: Alguns jogadores mostram evolução excepcional ao longo da carreira

## 🤝 Contribuição

Para melhorias ou correções:
1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.