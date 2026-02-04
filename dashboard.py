"""
Dashboard Unificado - API ou Upload de URLs
YouTube, Instagram, TikTok: Busca por hashtag OU upload de planilha
"""

import streamlit as st
import pandas as pd
import subprocess
import json
import time
from datetime import datetime
from social_media_scraper import SocialMediaScraper

st.set_page_config(
    page_title="Dashboard Completo",
    page_icon="📊",
    layout="wide"
)


def extrair_duracao_url(url):
    """Extrai duração usando yt-dlp (sem API)"""
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-playlist', '--no-warnings', url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            duracao_seg = data.get('duration', 0)
            
            if duracao_seg:
                horas = int(duracao_seg // 3600)
                minutos = int((duracao_seg % 3600) // 60)
                segundos = int(duracao_seg % 60)
                
                if horas > 0:
                    duracao_fmt = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
                else:
                    duracao_fmt = f"{minutos:02d}:{segundos:02d}"
                
                # Extrair título se disponível
                titulo = data.get('title', 'Sem título')
                criador = data.get('uploader', data.get('channel', 'Desconhecido'))
                
                return {
                    'segundos': duracao_seg,
                    'formatada': duracao_fmt,
                    'titulo': titulo,
                    'criador': criador,
                    'status': 'ok'
                }
        
        return {'segundos': 0, 'formatada': 'Erro', 'status': 'erro'}
    
    except Exception as e:
        return {'segundos': 0, 'formatada': 'Erro', 'status': f'erro: {str(e)}'}


def processar_upload(df, coluna_url, tempo_minimo_seg):
    """Processa planilha de URLs e extrai minutagem"""
    
    if coluna_url not in df.columns:
        st.error(f"❌ Coluna '{coluna_url}' não encontrada")
        return None
    
    # Criar colunas resultado
    df['Plataforma'] = ''
    df['Criador'] = ''
    df['Título'] = ''
    df['Duração (seg)'] = 0
    df['Duração'] = ''
    df['Status'] = ''
    df['Monetizável'] = ''
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total = len(df)
    sucesso = 0
    erro = 0
    
    for idx, row in df.iterrows():
        url = str(row[coluna_url]).strip()
        
        if pd.isna(url) or url == '' or url == 'nan':
            df.at[idx, 'Status'] = 'URL vazia'
            continue
        
        status_text.text(f"Processando {idx + 1}/{total}: {url[:50]}...")
        
        # Identificar plataforma
        if 'tiktok.com' in url.lower():
            plataforma = 'TikTok'
        elif 'instagram.com' in url.lower():
            plataforma = 'Instagram'
        elif 'youtube.com' in url.lower() or 'youtu.be' in url.lower():
            plataforma = 'YouTube'
        else:
            plataforma = 'Outra'
        
        df.at[idx, 'Plataforma'] = plataforma
        
        # Extrair duração
        resultado = extrair_duracao_url(url)
        
        df.at[idx, 'Duração (seg)'] = resultado['segundos']
        df.at[idx, 'Duração'] = resultado['formatada']
        df.at[idx, 'Status'] = resultado['status']
        
        if resultado['status'] == 'ok':
            df.at[idx, 'Criador'] = resultado.get('criador', 'Desconhecido')
            df.at[idx, 'Título'] = resultado.get('titulo', 'Sem título')
            df.at[idx, 'Monetizável'] = '✅' if resultado['segundos'] >= tempo_minimo_seg else '❌'
            sucesso += 1
        else:
            df.at[idx, 'Monetizável'] = '❌'
            erro += 1
        
        progress_bar.progress((idx + 1) / total)
        time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    
    st.success(f"✅ Concluído! Sucesso: {sucesso} | Erro: {erro}")
    
    return df


def tab_api(plataforma):
    """Tab para busca por API"""
    st.subheader(f"🔍 Busca por Hashtag - {plataforma}")
    
    with st.form(f"form_api_{plataforma}"):
        hashtag = st.text_input(
            "Hashtag",
            placeholder="Ex: tecnologia",
            key=f"hashtag_{plataforma}"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            tempo_minimo = st.number_input(
                "Minutagem mínima (minutos)",
                min_value=0.0,
                max_value=60.0,
                value=1.0,
                step=0.5,
                key=f"tempo_{plataforma}"
            )
        
        with col2:
            max_results = st.slider(
                "Máximo de resultados",
                10, 50, 20, 5,
                key=f"max_{plataforma}"
            )
        
        if plataforma == "YouTube":
            api_key = st.text_input(
                "YouTube API Key",
                type="password",
                help="Obtenha em console.cloud.google.com",
                key=f"key_{plataforma}"
            )
        else:
            api_key = None
            st.info(f"⚠️ API do {plataforma} não configurada. Dados de exemplo serão usados.")
        
        submit = st.form_submit_button("🚀 Buscar")
    
    if submit and hashtag:
        segundos_minimo = tempo_minimo * 60
        
        with st.spinner(f"Buscando no {plataforma}..."):
            try:
                scraper = SocialMediaScraper()
                
                if api_key:
                    scraper.configure_apis(youtube_key=api_key)
                
                # Buscar apenas na plataforma específica
                if plataforma == "YouTube":
                    data_raw = scraper.search_youtube(hashtag, max_results)
                elif plataforma == "Instagram":
                    data_raw = scraper.search_instagram(hashtag, max_results)
                else:  # TikTok
                    data_raw = scraper.search_tiktok(hashtag, max_results)
                
                # Filtrar por minutagem
                data_filtrada = [
                    video for video in data_raw 
                    if video['duracao_segundos'] >= segundos_minimo
                ]
                
                if len(data_filtrada) == 0:
                    st.warning(f"⚠️ Nenhum vídeo ≥ {tempo_minimo} min")
                    st.info(f"Total encontrado: {len(data_raw)}, todos abaixo de {tempo_minimo} min")
                else:
                    # Salvar nos session_state específicos da plataforma
                    st.session_state[f'data_{plataforma}'] = data_filtrada
                    st.session_state[f'hashtag_{plataforma}'] = hashtag
                    st.session_state[f'tempo_{plataforma}'] = tempo_minimo
                    
                    st.success(f"✅ {len(data_filtrada)} vídeos encontrados (≥ {tempo_minimo} min)")
                    
                    # Mostrar resultado
                    df = pd.DataFrame(data_filtrada)
                    
                    df_display = df[[
                        'perfil', 'titulo', 'duracao_formatada',
                        'likes', 'comentarios', 'data_publicacao', 'url'
                    ]].copy()
                    
                    df_display.columns = [
                        'Criador', 'Título', 'Duração',
                        'Likes', 'Comentários', 'Data', 'URL'
                    ]
                    
                    st.dataframe(df_display, use_container_width=True, height=400)
                    
                    # Download
                    scraper.data = data_filtrada
                    filename = f"dados_{plataforma}_{hashtag}_{tempo_minimo}min.xlsx"
                    scraper.export_to_excel(filename)
                    
                    with open(filename, 'rb') as f:
                        st.download_button(
                            "📥 Download Excel",
                            f,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_api_{plataforma}"
                        )
            
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    
    elif submit:
        st.warning("⚠️ Digite a hashtag")


def tab_upload(plataforma):
    """Tab para upload de URLs"""
    st.subheader(f"📤 Upload de URLs - {plataforma}")
    
    st.info(f"""
    **Como funciona:**
    1. Faça upload de Excel/CSV com URLs do {plataforma}
    2. Sistema extrai minutagem automaticamente (sem API)
    3. Download do arquivo atualizado
    """)
    
    uploaded = st.file_uploader(
        f"Upload planilha com URLs do {plataforma}",
        type=['xlsx', 'xls', 'csv'],
        key=f"upload_{plataforma}"
    )
    
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            st.success(f"✅ Arquivo carregado: {len(df)} linhas")
            
            with st.expander("👁️ Ver preview"):
                st.dataframe(df.head(10))
            
            col1, col2 = st.columns(2)
            
            with col1:
                coluna_url = st.selectbox(
                    "Coluna com URLs",
                    options=df.columns.tolist(),
                    key=f"coluna_{plataforma}"
                )
            
            with col2:
                tempo_minimo_upload = st.number_input(
                    "Minutagem mínima (minutos)",
                    min_value=0.0,
                    max_value=60.0,
                    value=1.0,
                    step=0.5,
                    key=f"tempo_upload_{plataforma}"
                )
            
            # Teste limitado
            limitar = st.checkbox(
                "Processar apenas primeiras linhas (teste)",
                value=False,
                key=f"limitar_{plataforma}"
            )
            
            if limitar:
                n_linhas = st.number_input(
                    "Quantas linhas?",
                    min_value=1,
                    max_value=len(df),
                    value=min(5, len(df)),
                    key=f"n_linhas_{plataforma}"
                )
                df_processar = df.head(n_linhas).copy()
            else:
                df_processar = df.copy()
            
            if st.button(f"⏱️ Extrair Minutagem", key=f"extrair_{plataforma}"):
                # Verificar yt-dlp
                try:
                    subprocess.run(['yt-dlp', '--version'], 
                                 capture_output=True, check=True)
                except:
                    st.error("""
                    ❌ **yt-dlp não está instalado!**
                    
                    Adicione ao requirements.txt:
                    ```
                    yt-dlp>=2024.3.10
                    ```
                    """)
                    return
                
                segundos_minimo = tempo_minimo_upload * 60
                
                st.info(f"Processando {len(df_processar)} URLs...")
                
                df_resultado = processar_upload(df_processar, coluna_url, segundos_minimo)
                
                if df_resultado is not None:
                    # Filtrar apenas monetizáveis
                    df_monetizavel = df_resultado[df_resultado['Monetizável'] == '✅']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Processado", len(df_resultado))
                    
                    with col2:
                        st.metric("✅ Monetizáveis", len(df_monetizavel))
                    
                    with col3:
                        perc = (len(df_monetizavel) / len(df_resultado) * 100) if len(df_resultado) > 0 else 0
                        st.metric("% Monetizável", f"{perc:.1f}%")
                    
                    st.markdown("---")
                    st.markdown("**Resultado:**")
                    
                    st.dataframe(
                        df_resultado,
                        use_container_width=True,
                        height=400
                    )
                    
                    # Download
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{plataforma}_minutagem_{timestamp}.xlsx"
                    df_resultado.to_excel(filename, index=False)
                    
                    with open(filename, 'rb') as f:
                        st.download_button(
                            "📥 Download Excel Atualizado",
                            f,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_upload_{plataforma}"
                        )
        
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")


def main():
    st.title("📊 Dashboard Completo - API ou Upload")
    st.markdown("**Escolha: Buscar por hashtag (API) OU Upload de URLs**")
    st.markdown("---")
    
    # Tabs principais por plataforma
    tab1, tab2, tab3 = st.tabs(["▶️ YouTube", "📸 Instagram", "🎵 TikTok"])
    
    with tab1:
        st.markdown("## YouTube")
        subtab1, subtab2 = st.tabs(["🔍 Busca por API", "📤 Upload URLs"])
        
        with subtab1:
            tab_api("YouTube")
        
        with subtab2:
            tab_upload("YouTube")
    
    with tab2:
        st.markdown("## Instagram")
        subtab1, subtab2 = st.tabs(["🔍 Busca por API", "📤 Upload URLs"])
        
        with subtab1:
            tab_api("Instagram")
        
        with subtab2:
            tab_upload("Instagram")
    
    with tab3:
        st.markdown("## TikTok")
        subtab1, subtab2 = st.tabs(["🔍 Busca por API", "📤 Upload URLs"])
        
        with subtab1:
            tab_api("TikTok")
        
        with subtab2:
            tab_upload("TikTok")
    
    # Sidebar info
    st.sidebar.title("ℹ️ Como Usar")
    st.sidebar.markdown("""
    ### Duas formas de coletar dados:
    
    **1. Busca por API (Hashtag)**
    - YouTube: Requer API Key
    - Instagram: Dados de exemplo
    - TikTok: Dados de exemplo
    - Define minutagem mínima
    - Busca e filtra automaticamente
    
    **2. Upload de URLs**
    - Faça upload de planilha
    - Sistema extrai minutagem (sem API)
    - Funciona com qualquer plataforma
    - Marca vídeos monetizáveis
    
    ---
    
    ### Para Upload funcionar:
    
    Adicione ao `requirements.txt`:
    ```
    yt-dlp>=2024.3.10
    ```
    """)


if __name__ == "__main__":
    main()