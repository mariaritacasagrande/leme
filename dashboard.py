"""
Dashboard de Monetização - Minutagem e Hashtags
Foco: Identificar criadores monetizáveis por minutagem
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from social_media_scraper import SocialMediaScraper

st.set_page_config(
    page_title="Dashboard Monetização",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    .stMetric {background-color: #f0f2f6; padding: 10px; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)


def create_dashboard(data):
    """Dashboard focado em monetização por minutagem"""
    df = pd.DataFrame(data)
    
    st.title("💰 Dashboard de Monetização")
    st.markdown("**Análise de minutagem para identificar conteúdo monetizável**")
    st.markdown("---")
    
    # SIDEBAR: Filtros
    st.sidebar.header("⚙️ Filtros")
    
    # Filtro de minutagem mínima
    min_minutos = st.sidebar.number_input(
        "Minutagem mínima (minutos)",
        min_value=0,
        max_value=60,
        value=1,
        help="Vídeos acima deste tempo são monetizáveis"
    )
    
    min_segundos = min_minutos * 60
    
    # Filtro por plataforma
    plataformas_selecionadas = st.sidebar.multiselect(
        "Plataformas",
        options=df['plataforma'].unique(),
        default=df['plataforma'].unique()
    )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['duracao_segundos'] >= min_segundos) &
        (df['plataforma'].isin(plataformas_selecionadas))
    ]
    
    # MÉTRICAS PRINCIPAIS
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_videos = len(df_filtrado)
        st.metric("Vídeos Monetizáveis", total_videos)
    
    with col2:
        criadores_unicos = df_filtrado['perfil'].nunique()
        st.metric("Criadores Únicos", criadores_unicos)
    
    with col3:
        duracao_media = df_filtrado['duracao_segundos'].mean()
        min_media = int(duracao_media // 60)
        seg_media = int(duracao_media % 60)
        st.metric("Minutagem Média", f"{min_media}:{seg_media:02d}")
    
    with col4:
        # Percentual de vídeos monetizáveis
        perc_monetizavel = (len(df_filtrado) / len(df)) * 100 if len(df) > 0 else 0
        st.metric("% Monetizável", f"{perc_monetizavel:.1f}%")
    
    st.markdown("---")
    
    # TABS POR PLATAFORMA
    tabs = st.tabs([f"📱 {plat}" for plat in df['plataforma'].unique()])
    
    for i, plataforma in enumerate(df['plataforma'].unique()):
        with tabs[i]:
            df_plat = df_filtrado[df_filtrado['plataforma'] == plataforma]
            
            if len(df_plat) == 0:
                st.warning(f"Nenhum vídeo monetizável no {plataforma} com os filtros atuais")
                continue
            
            # Métricas da plataforma
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(f"Vídeos {plataforma}", len(df_plat))
            
            with col2:
                st.metric(f"Criadores {plataforma}", df_plat['perfil'].nunique())
            
            with col3:
                duracao_media_plat = df_plat['duracao_segundos'].mean()
                min_p = int(duracao_media_plat // 60)
                seg_p = int(duracao_media_plat % 60)
                st.metric(f"Minutagem Média", f"{min_p}:{seg_p:02d}")
            
            st.markdown("#### 📊 Distribuição de Minutagem")
            
            # Gráfico de minutagem
            df_plat_sorted = df_plat.sort_values('duracao_segundos', ascending=False).copy()
            df_plat_sorted['duracao_minutos'] = df_plat_sorted['duracao_segundos'] / 60
            
            fig = px.bar(
                df_plat_sorted,
                x=df_plat_sorted.index,
                y='duracao_minutos',
                hover_data=['perfil', 'titulo', 'duracao_formatada'],
                labels={'duracao_minutos': 'Duração (minutos)', 'index': 'Vídeo'},
                color='duracao_minutos',
                color_continuous_scale='Viridis'
            )
            
            # Linha de corte de monetização
            fig.add_hline(
                y=min_minutos, 
                line_dash="dash", 
                line_color="red",
                annotation_text=f"Mínimo Monetizável: {min_minutos} min"
            )
            
            fig.update_layout(
                showlegend=False,
                height=300,
                xaxis_title="",
                xaxis={'visible': False}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📋 Vídeos Detalhados")
            
            # Preparar dados para exibição
            df_display = df_plat_sorted[[
                'perfil', 'titulo', 'duracao_formatada', 
                'likes', 'comentarios', 'data_publicacao', 'url'
            ]].copy()
            
            df_display.columns = [
                'Criador', 'Título', 'Duração', 
                'Likes', 'Comentários', 'Data', 'URL'
            ]
            
            # Adicionar indicador de monetização
            df_display.insert(0, '💰', '✅')
            
            st.dataframe(
                df_display,
                use_container_width=True,
                height=400,
                column_config={
                    "URL": st.column_config.LinkColumn("Link", width="small")
                }
            )
            
            # Top criadores por minutagem média
            st.markdown("#### 🏆 Top Criadores por Minutagem Média")
            
            criadores_plat = df_plat.groupby('perfil').agg({
                'duracao_segundos': ['mean', 'count'],
                'titulo': 'first'
            }).round(0)
            
            criadores_plat.columns = ['duracao_media_seg', 'num_videos', 'exemplo']
            criadores_plat['duracao_media'] = criadores_plat['duracao_media_seg'].apply(
                lambda x: f"{int(x//60)}:{int(x%60):02d}"
            )
            
            criadores_plat = criadores_plat.sort_values('duracao_media_seg', ascending=False)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(
                    criadores_plat[['num_videos', 'duracao_media']],
                    use_container_width=True,
                    column_config={
                        'num_videos': 'Nº Vídeos',
                        'duracao_media': 'Minutagem Média'
                    }
                )
            
            with col2:
                # Gráfico de pizza
                fig_criadores = px.pie(
                    values=criadores_plat['num_videos'].values,
                    names=criadores_plat.index,
                    title=f"Distribuição de Vídeos"
                )
                fig_criadores.update_layout(height=300)
                st.plotly_chart(fig_criadores, use_container_width=True)
    
    st.markdown("---")
    
    # ANÁLISE COMPARATIVA
    st.subheader("📊 Comparação Entre Plataformas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Comparação de minutagem média
        plat_stats = df_filtrado.groupby('plataforma').agg({
            'duracao_segundos': 'mean',
            'perfil': 'count'
        }).round(0)
        
        plat_stats.columns = ['duracao_media_seg', 'total_videos']
        plat_stats['duracao_formatada'] = plat_stats['duracao_media_seg'].apply(
            lambda x: f"{int(x//60)}:{int(x%60):02d}"
        )
        
        st.markdown("**Minutagem Média por Plataforma:**")
        st.dataframe(
            plat_stats[['total_videos', 'duracao_formatada']],
            column_config={
                'total_videos': 'Total Vídeos',
                'duracao_formatada': 'Duração Média'
            }
        )
    
    with col2:
        # Gráfico de barras
        fig_comp = px.bar(
            x=plat_stats.index,
            y=plat_stats['duracao_media_seg'] / 60,
            labels={'x': 'Plataforma', 'y': 'Duração Média (minutos)'},
            color=plat_stats['duracao_media_seg'] / 60,
            color_continuous_scale='Viridis'
        )
        fig_comp.update_layout(showlegend=False, height=250)
        st.plotly_chart(fig_comp, use_container_width=True)
    
    st.markdown("---")
    
    # BUSCAR CRIADOR ESPECÍFICO
    st.subheader("🔍 Buscar Criador")
    
    criador_busca = st.text_input(
        "Digite o nome do criador/canal",
        placeholder="Ex: DoctorRamani"
    )
    
    if criador_busca:
        df_criador = df[df['perfil'].str.contains(criador_busca, case=False, na=False)]
        
        if len(df_criador) > 0:
            st.success(f"✅ Encontrados {len(df_criador)} vídeos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Vídeos", len(df_criador))
            
            with col2:
                duracao_criador = df_criador['duracao_segundos'].mean()
                min_c = int(duracao_criador // 60)
                seg_c = int(duracao_criador % 60)
                st.metric("Minutagem Média", f"{min_c}:{seg_c:02d}")
            
            with col3:
                monetizaveis = len(df_criador[df_criador['duracao_segundos'] >= min_segundos])
                st.metric("Vídeos Monetizáveis", monetizaveis)
            
            df_criador_display = df_criador[[
                'plataforma', 'titulo', 'duracao_formatada', 
                'likes', 'comentarios', 'data_publicacao', 'url'
            ]].copy()
            
            df_criador_display.columns = [
                'Plataforma', 'Título', 'Duração',
                'Likes', 'Comentários', 'Data', 'URL'
            ]
            
            # Marcar monetizáveis
            df_criador_display.insert(
                0, 
                '💰', 
                df_criador['duracao_segundos'].apply(lambda x: '✅' if x >= min_segundos else '❌')
            )
            
            st.dataframe(
                df_criador_display,
                use_container_width=True,
                column_config={
                    "URL": st.column_config.LinkColumn("Link")
                }
            )
        else:
            st.warning("❌ Nenhum vídeo encontrado para este criador")


def main():
    st.sidebar.title("💰 Monetização")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Menu",
        ["📊 Dashboard", "🔄 Coletar Dados", "ℹ️ Info"]
    )
    
    if menu == "🔄 Coletar Dados":
        st.title("🔄 Coletar Dados")
        
        with st.form("coleta_form"):
            hashtag = st.text_input(
                "Hashtag para buscar",
                placeholder="Ex: lovebombing, tecnologia",
                help="Digite sem o símbolo #"
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
            with st.spinner("Coletando dados..."):
                try:
                    scraper = SocialMediaScraper()
                    
                    if youtube_api_key:
                        scraper.configure_apis(youtube_key=youtube_api_key)
                    
                    data = scraper.search_all_platforms(hashtag, max_results)
                    
                    st.session_state['data'] = data
                    st.session_state['hashtag'] = hashtag
                    
                    filename = scraper.export_to_excel(f"dados_{hashtag}.xlsx")
                    
                    st.success(f"✅ {len(data)} posts coletados!")
                    
                    with open(filename, 'rb') as f:
                        st.download_button(
                            label="📥 Download Excel",
                            data=f,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    st.info("👉 Vá para 'Dashboard' para ver a análise")
                    
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
        
        elif submit:
            st.warning("⚠️ Digite uma hashtag")
    
    elif menu == "📊 Dashboard":
        if 'data' in st.session_state and st.session_state['data']:
            hashtag = st.session_state.get('hashtag', 'desconhecida')
            st.sidebar.success(f"✅ Hashtag: #{hashtag}")
            create_dashboard(st.session_state['data'])
        else:
            st.info("""
            ### 📊 Nenhum dado carregado
            
            1. Vá em "Coletar Dados"
            2. Digite a hashtag
            3. Cole YouTube API Key (ou deixe em branco para dados de exemplo)
            4. Clique "Iniciar Coleta"
            5. Retorne aqui
            
            Ou carregue um Excel existente:
            """)
            
            uploaded_file = st.file_uploader("Carregar Excel", type=['xlsx'])
            
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.session_state['data'] = df.to_dict('records')
                    st.success("✅ Arquivo carregado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    
    else:  # Info
        st.title("ℹ️ Sobre o Dashboard")
        
        st.markdown("""
        ## 💰 Dashboard de Monetização
        
        ### 🎯 O que este dashboard faz:
        
        **Identifica conteúdo monetizável por minutagem:**
        
        - Define **minutagem mínima** para monetização (ex: 1 min)
        - Mostra quais vídeos **passam** deste limite
        - Filtra vídeos **monetizáveis por plataforma**
        - Lista todos os **criadores que usam a hashtag**
        
        ### 📊 Análise por Plataforma:
        
        **Abas separadas** para cada plataforma:
        - YouTube
        - Instagram  
        - TikTok
        
        Em cada aba você vê:
        - Quantos vídeos são monetizáveis
        - Minutagem média
        - Distribuição de duração
        - Lista detalhada de todos os vídeos
        - Top criadores por minutagem
        
        ### 💰 Como funciona a monetização:
        
        **Requisitos típicos:**
        - YouTube: geralmente >1 minuto
        - Instagram Reels: geralmente >60 segundos
        - TikTok: geralmente >1 minuto
        
        O dashboard mostra:
        - ✅ Vídeos que passam do mínimo
        - ❌ Vídeos abaixo do mínimo
        - Percentual de conteúdo monetizável
        
        ### 🔍 Busca por Criador:
        
        Digite o nome de qualquer criador para ver:
        - Todos os vídeos dele
        - Quais são monetizáveis
        - Minutagem média
        - Performance individual
        
        ### 📋 Dados Detalhados:
        
        Para cada vídeo você vê:
        - Criador/Canal
        - Título completo
        - **Duração (minutagem)**
        - Likes e comentários
        - Data de publicação
        - Link direto
        
        ### ⚙️ Filtros:
        
        - **Minutagem mínima**: Ajuste conforme necessário
        - **Plataformas**: Selecione quais ver
        
        ### 🎯 Casos de uso:
        
        1. **Identificar criadores monetizáveis**
           - Filtrar por minutagem mínima
           - Ver quais criadores cumprem requisito
        
        2. **Analisar performance por plataforma**
           - Comparar YouTube vs Instagram vs TikTok
           - Ver onde o conteúdo é mais longo
        
        3. **Buscar criadores específicos**
           - Verificar se usam a hashtag
           - Ver minutagem dos vídeos deles
        
        4. **Comparar plataformas**
           - Qual tem vídeos mais longos?
           - Qual tem mais criadores?
        """)


if __name__ == "__main__":
    main()