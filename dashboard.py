"""
Dashboard Interativo para Análise de Redes Sociais
Visualização dos dados coletados com gráficos e tabelas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from social_media_scraper import SocialMediaScraper, coletar_dados_redes_sociais
import json

# Configuração da página
st.set_page_config(
    page_title="Dashboard Redes Sociais",
    page_icon="📊",
    layout="wide"
)

# Estilo customizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def create_dashboard(data):
    """Cria dashboard com visualizações dos dados"""
    df = pd.DataFrame(data)
    
    # Título
    st.title("📊 Dashboard de Análise de Redes Sociais")
    st.markdown("---")
    
    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total de Posts", len(df))
    
    with col2:
        st.metric("Total de Likes", f"{df['likes'].sum():,}")
    
    with col3:
        st.metric("Total de Comentários", f"{df['comentarios'].sum():,}")
    
    with col4:
        st.metric("Média de Likes", f"{df['likes'].mean():.0f}")
    
    with col5:
        duracao_media = df['duracao_segundos'].mean()
        minutos = int(duracao_media // 60)
        segundos = int(duracao_media % 60)
        st.metric("Duração Média", f"{minutos}m {segundos}s")
    
    st.markdown("---")
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📱 Distribuição por Plataforma")
        plataforma_counts = df['plataforma'].value_counts()
        fig_plataforma = px.pie(
            values=plataforma_counts.values,
            names=plataforma_counts.index,
            title="Número de Posts por Plataforma",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_plataforma, use_container_width=True)
    
    with col2:
        st.subheader("❤️ Engajamento por Plataforma")
        engagement = df.groupby('plataforma').agg({
            'likes': 'sum',
            'comentarios': 'sum'
        }).reset_index()
        
        fig_engagement = go.Figure(data=[
            go.Bar(name='Likes', x=engagement['plataforma'], y=engagement['likes']),
            go.Bar(name='Comentários', x=engagement['plataforma'], y=engagement['comentarios'])
        ])
        fig_engagement.update_layout(
            title="Likes e Comentários por Plataforma",
            barmode='group'
        )
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    # Gráficos adicionais
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Perfis por Likes")
        top_perfis = df.groupby('perfil')['likes'].sum().sort_values(ascending=False).head(10)
        fig_top = px.bar(
            x=top_perfis.values,
            y=top_perfis.index,
            orientation='h',
            title="Perfis com Mais Likes",
            labels={'x': 'Total de Likes', 'y': 'Perfil'},
            color=top_perfis.values,
            color_continuous_scale='Viridis'
        )
        fig_top.update_layout(showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.subheader("⏱️ Distribuição de Duração dos Vídeos")
        fig_duracao = px.histogram(
            df,
            x='duracao_segundos',
            nbins=30,
            title="Frequência por Duração (segundos)",
            labels={'duracao_segundos': 'Duração (segundos)', 'count': 'Quantidade'},
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig_duracao, use_container_width=True)
    
    # Scatter plot - Relação likes vs comentários
    st.markdown("---")
    st.subheader("💬 Relação entre Likes e Comentários")
    fig_scatter = px.scatter(
        df,
        x='likes',
        y='comentarios',
        color='plataforma',
        size='duracao_segundos',
        hover_data=['perfil', 'duracao_formatada'],
        title="Correlação Likes vs Comentários (tamanho = duração)",
        labels={'likes': 'Número de Likes', 'comentarios': 'Número de Comentários'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Tabela de dados
    st.markdown("---")
    st.subheader("📋 Dados Detalhados")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        plataforma_filter = st.multiselect(
            "Filtrar por Plataforma",
            options=df['plataforma'].unique(),
            default=df['plataforma'].unique()
        )
    
    with col2:
        min_likes = st.number_input("Likes Mínimos", min_value=0, value=0)
    
    with col3:
        perfis = st.multiselect(
            "Filtrar por Perfil",
            options=sorted(df['perfil'].unique()),
            default=[]
        )
    
    # Aplicar filtros
    df_filtered = df[df['plataforma'].isin(plataforma_filter)]
    df_filtered = df_filtered[df_filtered['likes'] >= min_likes]
    
    if perfis:
        df_filtered = df_filtered[df_filtered['perfil'].isin(perfis)]
    
    # Selecionar colunas para exibir
    display_columns = [
        'plataforma', 'perfil', 'titulo', 'likes', 'comentarios',
        'duracao_formatada', 'data_publicacao', 'url'
    ]
    
    # Renomear colunas para português
    column_rename = {
        'plataforma': 'Plataforma',
        'perfil': 'Perfil',
        'titulo': 'Título',
        'likes': 'Likes',
        'comentarios': 'Comentários',
        'duracao_formatada': 'Duração',
        'data_publicacao': 'Data',
        'url': 'URL'
    }
    
    df_display = df_filtered[display_columns].rename(columns=column_rename)
    
    # Mostrar tabela
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )
    
    # Estatísticas dos dados filtrados
    st.markdown("---")
    st.subheader("📈 Estatísticas dos Dados Filtrados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Posts Filtrados", len(df_filtered))
    
    with col2:
        st.metric("Total Likes", f"{df_filtered['likes'].sum():,}")
    
    with col3:
        st.metric("Taxa de Comentários", f"{(df_filtered['comentarios'].sum() / df_filtered['likes'].sum() * 100):.2f}%")
    
    with col4:
        st.metric("Perfis Únicos", df_filtered['perfil'].nunique())


def main():
    """Função principal do dashboard"""
    
    st.sidebar.title("🎯 Configurações")
    st.sidebar.markdown("---")
    
    # Opções do menu
    menu = st.sidebar.radio(
        "Menu",
        ["📊 Visualizar Dados Existentes", "🔍 Coletar Novos Dados", "ℹ️ Sobre"]
    )
    
    if menu == "🔍 Coletar Novos Dados":
        st.title("🔍 Coletar Dados de Redes Sociais")
        
        st.info("""
        ### 📌 Instruções para Coleta de Dados:
        
        **APIs Necessárias:**
        - **YouTube**: Obtenha uma API key em [Google Cloud Console](https://console.cloud.google.com/)
        - **Instagram**: Requer conta Business e app no Facebook Developers
        - **TikTok**: API em beta com acesso limitado
        
        **Nota**: Sem API keys configuradas, o sistema usará dados de exemplo para demonstração.
        """)
        
        st.markdown("---")
        
        # Formulário de coleta
        with st.form("coleta_form"):
            hashtag = st.text_input(
                "Hashtag para buscar",
                placeholder="Ex: tecnologia, marketing, viagem",
                help="Digite a hashtag sem o símbolo #"
            )
            
            youtube_api_key = st.text_input(
                "YouTube API Key (opcional)",
                type="password",
                help="Deixe em branco para usar dados de exemplo"
            )
            
            max_results = st.slider(
                "Máximo de resultados por plataforma",
                min_value=10,
                max_value=50,
                value=30,
                step=10
            )
            
            submit = st.form_submit_button("🚀 Iniciar Coleta")
        
        if submit and hashtag:
            with st.spinner("Coletando dados... Isso pode levar alguns minutos."):
                try:
                    scraper = SocialMediaScraper()
                    
                    if youtube_api_key:
                        scraper.configure_apis(youtube_key=youtube_api_key)
                    
                    # Coletar dados
                    data = scraper.search_all_platforms(hashtag, max_results)
                    
                    # Salvar em sessão
                    st.session_state['data'] = data
                    st.session_state['hashtag'] = hashtag
                    
                    # Exportar para Excel
                    filename = scraper.export_to_excel(f"dados_{hashtag}.xlsx")
                    
                    st.success(f"✅ Dados coletados com sucesso! {len(data)} posts encontrados.")
                    
                    # Botão de download
                    with open(filename, 'rb') as f:
                        st.download_button(
                            label="📥 Download Excel",
                            data=f,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    # Mostrar estatísticas
                    stats = scraper.get_statistics()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Posts", stats['total_posts'])
                    with col2:
                        st.metric("Total de Likes", f"{stats['total_likes']:,}")
                    with col3:
                        st.metric("Perfis Únicos", stats['perfis_unicos'])
                    
                    st.info("💡 Vá para 'Visualizar Dados Existentes' para ver o dashboard completo!")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao coletar dados: {str(e)}")
        
        elif submit:
            st.warning("⚠️ Por favor, digite uma hashtag para buscar.")
    
    elif menu == "📊 Visualizar Dados Existentes":
        if 'data' in st.session_state and st.session_state['data']:
            hashtag = st.session_state.get('hashtag', 'desconhecida')
            st.sidebar.success(f"✅ Dados carregados: #{hashtag}")
            create_dashboard(st.session_state['data'])
        else:
            st.info("""
            ### 📊 Nenhum dado carregado
            
            Para visualizar o dashboard:
            1. Vá para "Coletar Novos Dados"
            2. Insira uma hashtag e clique em "Iniciar Coleta"
            3. Retorne aqui para visualizar os resultados
            
            Ou carregue um arquivo Excel existente:
            """)
            
            uploaded_file = st.file_uploader(
                "Carregar arquivo Excel",
                type=['xlsx'],
                help="Carregue um arquivo Excel gerado anteriormente"
            )
            
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.session_state['data'] = df.to_dict('records')
                    st.session_state['hashtag'] = 'arquivo_carregado'
                    st.success("✅ Arquivo carregado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
    
    else:  # Sobre
        st.title("ℹ️ Sobre o Sistema")
        
        st.markdown("""
        ## 📊 Dashboard de Análise de Redes Sociais
        
        ### 🎯 Funcionalidades
        
        - **Coleta de Dados**: Busca posts/vídeos por hashtag em YouTube, Instagram e TikTok
        - **Análise Visual**: Gráficos interativos e métricas de engajamento
        - **Exportação**: Dados exportados em formato Excel
        - **Filtros**: Filtragem avançada de dados por múltiplos critérios
        
        ### 📈 Métricas Coletadas
        
        - Nome do perfil/canal
        - Número de likes
        - Número de comentários
        - Número de salvamentos (quando disponível)
        - Duração do vídeo (em minutos e segundos)
        - Data de publicação
        - URL do conteúdo
        
        ### 🔧 Tecnologias Utilizadas
        
        - **Python**: Linguagem principal
        - **Streamlit**: Framework para dashboard interativo
        - **Pandas**: Processamento e análise de dados
        - **Plotly**: Visualizações interativas
        - **XlsxWriter**: Exportação para Excel
        
        ### 🔐 APIs Suportadas
        
        1. **YouTube Data API v3**: API oficial do Google
        2. **Instagram Graph API**: Requer conta Business
        3. **TikTok API**: Em desenvolvimento (acesso limitado)
        
        ### ⚠️ Considerações Importantes
        
        - Sempre respeite os termos de serviço das plataformas
        - Use APIs oficiais quando possível
        - Implemente rate limiting para evitar bloqueios
        - Dados de exemplo são usados quando APIs não estão configuradas
        
        ### 📝 Como Obter API Keys
        
        **YouTube**:
        1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
        2. Crie um novo projeto
        3. Ative a YouTube Data API v3
        4. Crie credenciais (API Key)
        
        **Instagram**:
        1. Converta sua conta para Business/Creator
        2. Crie um app em [Facebook Developers](https://developers.facebook.com/)
        3. Solicite permissões necessárias
        4. Obtenha Access Token
        
        ### 👨‍💻 Desenvolvido com ❤️
        
        Sistema de análise de redes sociais para marketing digital e pesquisa de mercado.
        """)
        
        st.markdown("---")
        
        st.info("""
        💡 **Dica**: Para começar, vá para "Coletar Novos Dados" e insira uma hashtag relevante 
        para seu nicho ou área de interesse!
        """)


if __name__ == "__main__":
    main()
