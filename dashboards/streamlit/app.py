import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Football Player Performance Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Função para carregar dados
@st.cache_data
def load_data():
    """Carrega todos os dados necessários para o dashboard"""
    data_dir = Path(__file__).parent.parent.parent / 'data' / 'processed'

    try:
        # Dados principais
        player_evolution = pd.read_csv(data_dir / 'player_evolution_final.csv')
        top_players = pd.read_csv(data_dir / 'top_players_growth.csv')
        rating_trends = pd.read_csv(data_dir / 'rating_trends_by_year.csv')
        attributes_corr = pd.read_csv(data_dir / 'top_attributes_correlation.csv')

        return player_evolution, top_players, rating_trends, attributes_corr

    except FileNotFoundError as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.error("Certifique-se de que os arquivos CSV foram exportados corretamente.")
        return None, None, None, None

# Carregar dados
player_evolution, top_players, rating_trends, attributes_corr = load_data()

# Verificar se dados foram carregados
if player_evolution is None:
    st.stop()

# Sidebar para navegação
st.sidebar.title("⚽ Football Analytics Dashboard")
st.sidebar.markdown("---")

# Seleção de página
page = st.sidebar.radio(
    "Navegação",
    ["🏠 Visão Geral", "👤 Análise por Jogador", "📈 Tendências Temporais",
     "🎯 Análise de Atributos", "⭐ Top Performers"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Sobre:** Dashboard interativo para análise de desempenho de jogadores de futebol baseado em dados do FIFA.")

# Conteúdo principal baseado na página selecionada
if page == "🏠 Visão Geral":
    st.title("🏠 Visão Geral - Football Player Performance")

    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_players = len(top_players)
        st.metric("Total de Jogadores", f"{total_players:,}")

    with col2:
        avg_rating = player_evolution['overall_rating'].mean()
        st.metric("Rating Médio Geral", f"{avg_rating:.1f}")

    with col3:
        max_growth = top_players['rating_growth'].max()
        st.metric("Maior Crescimento", f"{max_growth:.1f}")

    with col4:
        elite_count = len(player_evolution[player_evolution['overall_rating'] > 85])
        st.metric("Jogadores Elite (>85)", f"{elite_count:,}")

    st.markdown("---")

    # Gráficos principais
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribuição de Rating")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(player_evolution['overall_rating'], bins=30, kde=True, ax=ax)
        ax.set_title("Distribuição de Overall Rating", fontsize=14, fontweight='bold')
        ax.set_xlabel("Overall Rating")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

    with col2:
        st.subheader("📈 Evolução do Rating Médio")
        fig = px.line(rating_trends, x='year', y='overall_rating',
                     title="Tendência de Rating Médio por Ano",
                     markers=True, line_shape='linear')
        fig.update_layout(xaxis_title="Ano", yaxis_title="Rating Médio")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Top 5 atributos mais importantes
    st.subheader("🎯 Top 5 Atributos Determinantes")
    top_5_attrs = attributes_corr.head(5)

    fig = px.bar(top_5_attrs, x='correlation', y='attribute',
                title="Atributos Mais Correlacionados com Overall Rating",
                orientation='h', color='correlation',
                color_continuous_scale='viridis')
    fig.update_layout(xaxis_title="Correlação", yaxis_title="Atributo")
    st.plotly_chart(fig, use_container_width=True)

elif page == "👤 Análise por Jogador":
    st.title("👤 Análise por Jogador")

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        # Selecionar jogador
        players_list = sorted(player_evolution['player_name'].unique())
        selected_player = st.selectbox("Selecione um Jogador:", players_list)

    with col2:
        # Filtro de ano
        years = sorted(player_evolution['year'].unique())
        selected_years = st.multiselect("Anos:", years, default=years)

    # Filtrar dados do jogador selecionado
    player_data = player_evolution[
        (player_evolution['player_name'] == selected_player) &
        (player_evolution['year'].isin(selected_years))
    ].sort_values('year')

    if not player_data.empty:
        # Informações do jogador
        st.subheader(f"📊 Perfil de {selected_player}")

        # Métricas do jogador
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            current_rating = player_data['overall_rating'].iloc[-1]
            st.metric("Rating Atual", f"{current_rating:.1f}")

        with col2:
            avg_rating = player_data['overall_rating'].mean()
            st.metric("Rating Médio", f"{avg_rating:.1f}")

        with col3:
            growth = player_data['rating_growth'].iloc[0] if len(player_data) > 0 else 0
            st.metric("Crescimento Total", f"{growth:.1f}")

        with col4:
            age = player_data['age_at_rating'].iloc[-1]
            st.metric("Idade Atual", f"{age:.0f}")

        st.markdown("---")

        # Gráfico de evolução do rating
        st.subheader("📈 Evolução do Rating ao Longo do Tempo")
        fig = px.line(player_data, x='year', y='overall_rating',
                     title=f"Evolução de Rating - {selected_player}",
                     markers=True, line_shape='linear')
        fig.update_layout(xaxis_title="Ano", yaxis_title="Overall Rating")
        st.plotly_chart(fig, use_container_width=True)

        # Atributos técnicos atuais
        st.subheader("🎯 Atributos Técnicos Atuais")
        current_attrs = player_data.iloc[-1]

        # Selecionar atributos técnicos (excluindo colunas não técnicas)
        tech_columns = [col for col in player_data.columns if col not in
                       ['player_api_id', 'player_name', 'year', 'month', 'age_at_rating', 'rating_growth']]

        # Criar dataframe para visualização
        attrs_df = pd.DataFrame({
            'Atributo': tech_columns,
            'Valor': current_attrs[tech_columns]
        })

        fig = px.bar(attrs_df, x='Atributo', y='Valor',
                     title=f"Atributos Técnicos - {selected_player}",
                     color='Valor', color_continuous_scale='blues')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Nenhum dado encontrado para o jogador e anos selecionados.")

elif page == "📈 Tendências Temporais":
    st.title("📈 Tendências Temporais")

    st.subheader("📊 Evolução Geral do Rating por Ano")

    # Gráfico de linha principal
    fig = px.line(rating_trends, x='year', y='overall_rating',
                 title="Evolução do Rating Médio dos Jogadores (2008-2016)",
                 markers=True, line_shape='spline')
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Rating Médio",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Estatísticas por ano
    st.subheader("📈 Estatísticas Anuais Detalhadas")

    # Preparar dados para tabela
    stats_by_year = player_evolution.groupby('year').agg({
        'overall_rating': ['mean', 'std', 'min', 'max', 'count']
    }).round(2)

    stats_by_year.columns = ['Média', 'Desvio Padrão', 'Mínimo', 'Máximo', 'Nº Jogadores']
    stats_by_year = stats_by_year.reset_index()

    st.dataframe(stats_by_year, use_container_width=True)

    # Distribuição por ano
    st.subheader("📊 Distribuição de Rating por Ano")

    fig = px.box(player_evolution, x='year', y='overall_rating',
                title="Distribuição de Rating por Ano",
                points="outliers")
    fig.update_layout(xaxis_title="Ano", yaxis_title="Overall Rating")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Análise de Atributos":
    st.title("🎯 Análise de Atributos")

    # Correlações
    st.subheader("📊 Top 10 Atributos Correlacionados com Overall Rating")

    fig = px.bar(attributes_corr, x='correlation', y='attribute',
                title="Correlação dos Atributos com Overall Rating",
                orientation='h', color='correlation',
                color_continuous_scale='plasma')
    fig.update_layout(xaxis_title="Coeficiente de Correlação", yaxis_title="Atributo")
    st.plotly_chart(fig, use_container_width=True)

    # Scatter plot interativo
    st.subheader("🔍 Relação entre Atributos e Rating")

    col1, col2 = st.columns(2)

    with col1:
        x_attr = st.selectbox("Atributo X:", attributes_corr['attribute'].tolist(),
                             index=0, key='x_attr')

    with col2:
        y_attr = st.selectbox("Atributo Y:", attributes_corr['attribute'].tolist(),
                             index=1, key='y_attr')

    # Amostra dos dados para performance
    sample_data = player_evolution.sample(min(5000, len(player_evolution)), random_state=42)

    fig = px.scatter(sample_data, x=x_attr, y=y_attr,
                    color='overall_rating', size='overall_rating',
                    title=f"Relação entre {x_attr} e {y_attr}",
                    color_continuous_scale='viridis',
                    opacity=0.6)
    fig.update_layout(xaxis_title=x_attr, yaxis_title=y_attr)
    st.plotly_chart(fig, use_container_width=True)

    # Perfil Elite vs Geral
    st.subheader("⭐ Comparação: Jogadores Elite vs. Média Geral")

    # Calcular médias
    elite = player_evolution[player_evolution['overall_rating'] > 85]
    geral = player_evolution[player_evolution['overall_rating'] <= 85]

    elite_means = elite[attributes_corr['attribute'].head(5)].mean()
    geral_means = geral[attributes_corr['attribute'].head(5)].mean()

    comp_df = pd.DataFrame({
        'Atributo': attributes_corr['attribute'].head(5),
        'Elite (>85)': elite_means.values,
        'Média Geral': geral_means.values
    })

    comp_melted = comp_df.melt(id_vars='Atributo', var_name='Grupo', value_name='Média')

    fig = px.bar(comp_melted, x='Atributo', y='Média', color='Grupo',
                title="Comparação de Atributos: Elite vs. Geral",
                barmode='group', color_discrete_sequence=['gold', 'silver'])
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

elif page == "⭐ Top Performers":
    st.title("⭐ Top Performers")

    # Top 10 jogadores por crescimento
    st.subheader("🚀 Top 10 Jogadores com Maior Crescimento de Rating")

    top_10_growth = top_players.nlargest(10, 'rating_growth')

    # Tabela
    st.dataframe(top_10_growth[['player_name', 'rating_growth']],
                use_container_width=True)

    # Gráfico
    fig = px.bar(top_10_growth, x='rating_growth', y='player_name',
                title="Top 10 Jogadores por Crescimento de Rating",
                orientation='h', color='rating_growth',
                color_continuous_scale='greens')
    fig.update_layout(xaxis_title="Crescimento de Rating", yaxis_title="Jogador")
    st.plotly_chart(fig, use_container_width=True)

    # Distribuição de crescimento
    st.subheader("📊 Distribuição do Crescimento de Rating")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(top_players['rating_growth'], bins=30, kde=True, ax=ax, color='skyblue')
    ax.set_title("Distribuição do Crescimento de Rating dos Jogadores", fontsize=14, fontweight='bold')
    ax.set_xlabel("Crescimento de Rating")
    ax.set_ylabel("Frequência")
    ax.axvline(top_players['rating_growth'].mean(), color='red', linestyle='--',
               label=f'Média: {top_players["rating_growth"].mean():.2f}')
    ax.legend()
    st.pyplot(fig)

    # Estatísticas de crescimento
    st.subheader("📈 Estatísticas de Crescimento")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Crescimento Médio", f"{top_players['rating_growth'].mean():.2f}")

    with col2:
        st.metric("Crescimento Máximo", f"{top_players['rating_growth'].max():.2f}")

    with col3:
        st.metric("Crescimento Mínimo", f"{top_players['rating_growth'].min():.2f}")

    with col4:
        st.metric("Mediana", f"{top_players['rating_growth'].median():.2f}")

# Footer
st.markdown("---")
st.markdown("*Dashboard criado com Streamlit | Dados: European Soccer Database (Kaggle)*")