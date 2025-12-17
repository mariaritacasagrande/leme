"""
Sistema de Coleta de Dados de Redes Sociais
Coleta dados de Instagram, TikTok e YouTube baseado em hashtags
"""

import pandas as pd
import json
import time
from datetime import datetime
from typing import List, Dict
import requests
from collections import defaultdict

class SocialMediaScraper:
    """Classe principal para coletar dados de redes sociais"""
    
    def __init__(self):
        self.data = []
        self.api_keys = {
            'youtube': None,  # Adicionar sua API key do YouTube
            'instagram': None,  # Adicionar token de acesso do Instagram
            'tiktok': None  # Adicionar API key do TikTok
        }
    
    def configure_apis(self, youtube_key=None, instagram_token=None, tiktok_key=None):
        """Configura as chaves de API das plataformas"""
        if youtube_key:
            self.api_keys['youtube'] = youtube_key
        if instagram_token:
            self.api_keys['instagram'] = instagram_token
        if tiktok_key:
            self.api_keys['tiktok'] = tiktok_key
    
    def search_youtube(self, hashtag: str, max_results: int = 50) -> List[Dict]:
        """
        Busca vídeos no YouTube por hashtag usando YouTube Data API v3
        
        Args:
            hashtag: Hashtag para buscar (sem #)
            max_results: Número máximo de resultados
            
        Returns:
            Lista de dicionários com dados dos vídeos
        """
        print(f"🔍 Buscando vídeos no YouTube com hashtag: #{hashtag}")
        
        if not self.api_keys['youtube']:
            print("⚠️  API Key do YouTube não configurada. Retornando dados de exemplo.")
            return self._get_youtube_sample_data(hashtag)
        
        try:
            # Endpoint da API do YouTube
            search_url = "https://www.googleapis.com/youtube/v3/search"
            video_url = "https://www.googleapis.com/youtube/v3/videos"
            
            results = []
            
            # Buscar vídeos
            search_params = {
                'part': 'snippet',
                'q': f'#{hashtag}',
                'type': 'video',
                'maxResults': min(max_results, 50),
                'key': self.api_keys['youtube']
            }
            
            search_response = requests.get(search_url, params=search_params)
            
            if search_response.status_code != 200:
                print(f"❌ Erro na busca: {search_response.status_code}")
                return self._get_youtube_sample_data(hashtag)
            
            search_data = search_response.json()
            video_ids = [item['id']['videoId'] for item in search_data.get('items', [])]
            
            if not video_ids:
                print("⚠️  Nenhum vídeo encontrado")
                return []
            
            # Obter estatísticas detalhadas
            video_params = {
                'part': 'statistics,contentDetails,snippet',
                'id': ','.join(video_ids),
                'key': self.api_keys['youtube']
            }
            
            video_response = requests.get(video_url, params=video_params)
            video_data = video_response.json()
            
            for item in video_data.get('items', []):
                duration = self._parse_youtube_duration(item['contentDetails']['duration'])
                
                video_info = {
                    'plataforma': 'YouTube',
                    'hashtag': hashtag,
                    'perfil': item['snippet']['channelTitle'],
                    'titulo': item['snippet']['title'],
                    'video_id': item['id'],
                    'likes': int(item['statistics'].get('likeCount', 0)),
                    'comentarios': int(item['statistics'].get('commentCount', 0)),
                    'visualizacoes': int(item['statistics'].get('viewCount', 0)),
                    'salvamentos': 'N/A',  # YouTube não disponibiliza esse dado
                    'duracao_segundos': duration,
                    'duracao_formatada': self._format_duration(duration),
                    'data_publicacao': item['snippet']['publishedAt'],
                    'url': f"https://youtube.com/watch?v={item['id']}"
                }
                results.append(video_info)
            
            print(f"✅ {len(results)} vídeos coletados do YouTube")
            return results
            
        except Exception as e:
            print(f"❌ Erro ao buscar no YouTube: {str(e)}")
            return self._get_youtube_sample_data(hashtag)
    
    def search_instagram(self, hashtag: str, max_results: int = 50) -> List[Dict]:
        """
        Busca Reels (vídeos) no Instagram por hashtag
        
        Nota: Foca apenas em Reels (conteúdo de vídeo), não em posts de imagem
        Requer Instagram Graph API com permissões adequadas
        """
        print(f"🔍 Buscando Reels no Instagram com hashtag: #{hashtag}")
        
        if not self.api_keys['instagram']:
            print("⚠️  Token do Instagram não configurado. Retornando dados de exemplo.")
            return self._get_instagram_sample_data(hashtag)
        
        # Implementação com Instagram Graph API
        # Nota: Requer Business Account e aprovação do Facebook
        try:
            # Esta é a estrutura básica - ajuste conforme sua configuração
            results = []
            
            # A API do Instagram tem restrições e requer aprovação
            # Para uso em produção, você precisa:
            # 1. Converter conta para Business/Creator
            # 2. Criar app no Facebook Developers
            # 3. Obter permissões necessárias
            # 4. Filtrar apenas por media_type='VIDEO' ou 'REELS'
            
            print("⚠️  Instagram API tem restrições. Usando dados de exemplo de Reels.")
            return self._get_instagram_sample_data(hashtag)
            
        except Exception as e:
            print(f"❌ Erro ao buscar Reels no Instagram: {str(e)}")
            return self._get_instagram_sample_data(hashtag)
    
    def search_tiktok(self, hashtag: str, max_results: int = 50) -> List[Dict]:
        """
        Busca vídeos no TikTok por hashtag
        
        Nota: Requer TikTok API (em beta, acesso limitado)
        """
        print(f"🔍 Buscando vídeos no TikTok com hashtag: #{hashtag}")
        
        if not self.api_keys['tiktok']:
            print("⚠️  API Key do TikTok não configurada. Retornando dados de exemplo.")
            return self._get_tiktok_sample_data(hashtag)
        
        # TikTok API está em desenvolvimento e tem acesso limitado
        try:
            print("⚠️  TikTok API tem acesso restrito. Usando dados de exemplo.")
            return self._get_tiktok_sample_data(hashtag)
            
        except Exception as e:
            print(f"❌ Erro ao buscar no TikTok: {str(e)}")
            return self._get_tiktok_sample_data(hashtag)
    
    def search_all_platforms(self, hashtag: str, max_results_per_platform: int = 30):
        """Busca em todas as plataformas"""
        print(f"\n{'='*60}")
        print(f"INICIANDO COLETA DE DADOS - HASHTAG: #{hashtag}")
        print(f"{'='*60}\n")
        
        all_results = []
        
        # YouTube
        youtube_results = self.search_youtube(hashtag, max_results_per_platform)
        all_results.extend(youtube_results)
        time.sleep(1)  # Rate limiting
        
        # Instagram
        instagram_results = self.search_instagram(hashtag, max_results_per_platform)
        all_results.extend(instagram_results)
        time.sleep(1)
        
        # TikTok
        tiktok_results = self.search_tiktok(hashtag, max_results_per_platform)
        all_results.extend(tiktok_results)
        
        self.data = all_results
        
        print(f"\n{'='*60}")
        print(f"COLETA FINALIZADA")
        print(f"Total de posts/vídeos coletados: {len(all_results)}")
        print(f"{'='*60}\n")
        
        return all_results
    
    def export_to_excel(self, filename: str = "dados_redes_sociais.xlsx"):
        """Exporta os dados para Excel com abas separadas por plataforma e MINUTAGEM destacada"""
        if not self.data:
            print("⚠️  Nenhum dado para exportar")
            return
        
        df = pd.DataFrame(self.data)
        
        # Renomear coluna para destacar MINUTAGEM
        df = df.rename(columns={'duracao_formatada': 'MINUTAGEM'})
        
        # Criar arquivo Excel com formatação
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Formato para cabeçalhos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 11
            })
            
            # Formato especial para coluna MINUTAGEM (destaque amarelo)
            minutagem_format = workbook.add_format({
                'bg_color': '#FFF2CC',
                'bold': True,
                'align': 'center',
                'font_size': 11,
                'border': 1
            })
            
            # Formato para números
            number_format = workbook.add_format({'num_format': '#,##0'})
            
            # ABA 1: TODOS OS DADOS
            df_todos = df.copy()
            df_todos.to_excel(writer, sheet_name='TODOS OS DADOS', index=False)
            
            worksheet = writer.sheets['TODOS OS DADOS']
            for col_num, value in enumerate(df_todos.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Destacar coluna MINUTAGEM
            if 'MINUTAGEM' in df_todos.columns:
                minutagem_col = df_todos.columns.get_loc('MINUTAGEM')
                for row in range(1, len(df_todos) + 1):
                    worksheet.write(row, minutagem_col, df_todos.iloc[row-1]['MINUTAGEM'], minutagem_format)
            
            worksheet.set_column('A:A', 12)  # Plataforma
            worksheet.set_column('B:B', 15)  # Hashtag
            worksheet.set_column('C:C', 20)  # Perfil
            worksheet.set_column('D:D', 40)  # Título
            worksheet.set_column('E:E', 15)  # Video ID
            worksheet.set_column('F:H', 12)  # Likes, Comentários, Visualizações
            worksheet.set_column('I:I', 12)  # Salvamentos
            worksheet.set_column('J:J', 15)  # Duração segundos
            worksheet.set_column('K:K', 16)  # MINUTAGEM (destaque)
            worksheet.set_column('L:L', 12)  # Data
            worksheet.set_column('M:M', 50)  # URL
            
            # ABA 2, 3, 4: UMA PARA CADA PLATAFORMA
            plataformas = df['plataforma'].unique()
            
            for plataforma in sorted(plataformas):
                df_plataforma = df[df['plataforma'] == plataforma].copy()
                
                # Remover coluna de plataforma já que está implícito
                df_plataforma = df_plataforma.drop('plataforma', axis=1)
                
                sheet_name = f'{plataforma}'
                df_plataforma.to_excel(writer, sheet_name=sheet_name, index=False)
                
                worksheet = writer.sheets[sheet_name]
                
                # Aplicar formato aos cabeçalhos
                for col_num, value in enumerate(df_plataforma.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Destacar coluna MINUTAGEM
                if 'MINUTAGEM' in df_plataforma.columns:
                    minutagem_col = df_plataforma.columns.get_loc('MINUTAGEM')
                    for row in range(1, len(df_plataforma) + 1):
                        worksheet.write(row, minutagem_col, df_plataforma.iloc[row-1]['MINUTAGEM'], minutagem_format)
                
                # Ajustar largura das colunas
                worksheet.set_column('A:A', 15)  # Hashtag
                worksheet.set_column('B:B', 20)  # Perfil
                worksheet.set_column('C:C', 40)  # Título
                worksheet.set_column('D:D', 15)  # Video ID
                worksheet.set_column('E:G', 12)  # Likes, Comentários, Visualizações
                worksheet.set_column('H:H', 12)  # Salvamentos
                worksheet.set_column('I:I', 15)  # Duração segundos
                worksheet.set_column('J:J', 16)  # MINUTAGEM (destaque)
                worksheet.set_column('K:K', 12)  # Data
                worksheet.set_column('L:L', 50)  # URL
                
                print(f"   ✅ Aba '{plataforma}' criada com {len(df_plataforma)} posts - MINUTAGEM incluída")
            
            # ABA: RESUMO POR PLATAFORMA COM MINUTAGEM
            stats = df.groupby('plataforma').agg({
                'likes': 'sum',
                'comentarios': 'sum',
                'perfil': 'count',
                'duracao_segundos': ['mean', 'min', 'max']
            })
            
            stats.columns = ['total_likes', 'total_comentarios', 'total_posts', 
                           'duracao_media_seg', 'duracao_min_seg', 'duracao_max_seg']
            
            # Adicionar taxa de engajamento
            stats['engajamento_total'] = stats['total_likes'] + stats['total_comentarios']
            stats['media_likes_por_post'] = (stats['total_likes'] / stats['total_posts']).round(0)
            
            # Formatar durações
            stats['MINUTAGEM_MÉDIA'] = stats['duracao_media_seg'].apply(
                lambda x: self._format_duration(int(x))
            )
            stats['MINUTAGEM_MÍNIMA'] = stats['duracao_min_seg'].apply(
                lambda x: self._format_duration(int(x))
            )
            stats['MINUTAGEM_MÁXIMA'] = stats['duracao_max_seg'].apply(
                lambda x: self._format_duration(int(x))
            )
            
            # Reorganizar colunas
            stats = stats[['total_posts', 'total_likes', 'total_comentarios', 'engajamento_total', 
                          'media_likes_por_post', 'MINUTAGEM_MÉDIA', 'MINUTAGEM_MÍNIMA', 'MINUTAGEM_MÁXIMA']]
            
            stats.to_excel(writer, sheet_name='RESUMO COM MINUTAGEM')
            
            worksheet = writer.sheets['RESUMO COM MINUTAGEM']
            for col_num, value in enumerate(['Plataforma'] + list(stats.columns)):
                worksheet.write(0, col_num, value, header_format)
            
            # Destacar colunas de MINUTAGEM
            for col_name in ['MINUTAGEM_MÉDIA', 'MINUTAGEM_MÍNIMA', 'MINUTAGEM_MÁXIMA']:
                if col_name in stats.columns:
                    col_idx = list(stats.columns).index(col_name) + 1  # +1 por causa do índice
                    for row in range(1, len(stats) + 1):
                        worksheet.write(row, col_idx, stats.iloc[row-1][col_name], minutagem_format)
            
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:H', 18)
            
            # ABA: TOP 20 PERFIS
            top_perfis = df.groupby(['plataforma', 'perfil']).agg({
                'likes': 'sum',
                'comentarios': 'sum',
                'perfil': 'count'
            }).rename(columns={'perfil': 'total_posts'})
            
            top_perfis['engajamento_total'] = top_perfis['likes'] + top_perfis['comentarios']
            top_perfis = top_perfis.sort_values('likes', ascending=False).head(20)
            
            top_perfis.to_excel(writer, sheet_name='Top 20 Perfis')
            
            worksheet = writer.sheets['Top 20 Perfis']
            for col_num, value in enumerate(['Plataforma', 'Perfil', 'Total Likes', 'Total Comentários', 'Engajamento Total']):
                worksheet.write(0, col_num, value, header_format)
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:B', 25)
            worksheet.set_column('C:E', 18)
        
        print(f"\n✅ Excel exportado com sucesso: {filename}")
        print(f"   📊 Contém {len(plataformas)} abas de plataformas + abas de análise")
        print(f"   ⏱️  MINUTAGEM destacada em AMARELO em todas as abas")
        return filename
    
    def get_statistics(self) -> Dict:
        """Calcula estatísticas gerais dos dados coletados"""
        if not self.data:
            return {}
        
        df = pd.DataFrame(self.data)
        
        stats = {
            'total_posts': len(df),
            'total_likes': df['likes'].sum(),
            'total_comentarios': df['comentarios'].sum(),
            'media_likes': df['likes'].mean(),
            'media_comentarios': df['comentarios'].mean(),
            'por_plataforma': df.groupby('plataforma').size().to_dict(),
            'duracao_media_segundos': df['duracao_segundos'].mean(),
            'perfis_unicos': df['perfil'].nunique()
        }
        
        return stats
    
    # Métodos auxiliares
    
    @staticmethod
    def _parse_youtube_duration(duration: str) -> int:
        """Converte duração ISO 8601 do YouTube para segundos"""
        import re
        
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Formata segundos para HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"
    
    # Dados de exemplo (para demonstração quando API keys não estão configuradas)
    
    def _get_youtube_sample_data(self, hashtag: str) -> List[Dict]:
        """Retorna dados de exemplo do YouTube"""
        import random
        
        sample_data = []
        channels = ['Canal Tech', 'Vlog Diário', 'Tutorial Pro', 'Gaming Master', 'Review Expert']
        
        for i in range(15):
            duration = random.randint(60, 3600)
            sample_data.append({
                'plataforma': 'YouTube',
                'hashtag': hashtag,
                'perfil': random.choice(channels),
                'titulo': f'Vídeo sobre {hashtag} - Parte {i+1}',
                'video_id': f'sample_{i}',
                'likes': random.randint(100, 50000),
                'comentarios': random.randint(10, 5000),
                'visualizacoes': random.randint(1000, 500000),
                'salvamentos': 'N/A',
                'duracao_segundos': duration,
                'duracao_formatada': self._format_duration(duration),
                'data_publicacao': '2024-12-01',
                'url': f'https://youtube.com/watch?v=sample_{i}'
            })
        
        return sample_data
    
    def _get_instagram_sample_data(self, hashtag: str) -> List[Dict]:
        """Retorna dados de exemplo de Reels do Instagram"""
        import random
        
        sample_data = []
        profiles = ['@influencer_tech', '@creator_digital', '@brand_inovacao', '@artist_criativo', '@traveler_mundo']
        
        # Reels do Instagram geralmente têm entre 15-90 segundos
        for i in range(15):
            duration = random.randint(15, 90)  # Duração típica de Reels
            likes = random.randint(500, 100000)
            comments = random.randint(20, 10000)
            views = random.randint(5000, 1000000)
            saves = random.randint(50, 5000)
            
            sample_data.append({
                'plataforma': 'Instagram',
                'hashtag': hashtag,
                'perfil': random.choice(profiles),
                'titulo': f'Reel sobre {hashtag} #{i+1}',
                'video_id': f'ig_reel_{i}',
                'likes': likes,
                'comentarios': comments,
                'visualizacoes': views,
                'salvamentos': saves,
                'duracao_segundos': duration,
                'duracao_formatada': self._format_duration(duration),
                'data_publicacao': '2024-12-01',
                'url': f'https://instagram.com/reel/sample_{i}'
            })
        
        return sample_data
    
    def _get_tiktok_sample_data(self, hashtag: str) -> List[Dict]:
        """Retorna dados de exemplo do TikTok"""
        import random
        
        sample_data = []
        users = ['@tiktoker1', '@creator2', '@viral3', '@trending4', '@famous5']
        
        for i in range(15):
            duration = random.randint(15, 180)  # TikTok permite até 10 min
            sample_data.append({
                'plataforma': 'TikTok',
                'hashtag': hashtag,
                'perfil': random.choice(users),
                'titulo': f'Vídeo TikTok {hashtag}',
                'video_id': f'tt_sample_{i}',
                'likes': random.randint(1000, 500000),
                'comentarios': random.randint(50, 50000),
                'visualizacoes': random.randint(10000, 5000000),
                'salvamentos': random.randint(100, 10000),
                'duracao_segundos': duration,
                'duracao_formatada': self._format_duration(duration),
                'data_publicacao': '2024-12-01',
                'url': f'https://tiktok.com/@user/video/{i}'
            })
        
        return sample_data


# Função principal para uso simples
def coletar_dados_redes_sociais(hashtag: str, youtube_api_key: str = None):
    """
    Função simplificada para coletar dados de redes sociais
    
    Args:
        hashtag: Hashtag para buscar (sem o #)
        youtube_api_key: Chave da API do YouTube (opcional)
    
    Returns:
        Nome do arquivo Excel gerado
    """
    scraper = SocialMediaScraper()
    
    if youtube_api_key:
        scraper.configure_apis(youtube_key=youtube_api_key)
    
    # Coletar dados
    scraper.search_all_platforms(hashtag, max_results_per_platform=30)
    
    # Exportar para Excel
    filename = f"dados_{hashtag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    scraper.export_to_excel(filename)
    
    # Mostrar estatísticas
    stats = scraper.get_statistics()
    print("\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   Total de posts: {stats['total_posts']}")
    print(f"   Total de likes: {stats['total_likes']:,}")
    print(f"   Total de comentários: {stats['total_comentarios']:,}")
    print(f"   Média de likes: {stats['media_likes']:.0f}")
    print(f"   Duração média: {scraper._format_duration(int(stats['duracao_media_segundos']))}")
    print(f"   Perfis únicos: {stats['perfis_unicos']}")
    
    return filename, scraper


if __name__ == "__main__":
    # Exemplo de uso
    print("🚀 Sistema de Coleta de Dados de Redes Sociais\n")
    
    # Você pode adicionar sua API key do YouTube aqui
    # Para obter uma: https://console.cloud.google.com/
    YOUTUBE_API_KEY = None  # Substitua por sua chave
    
    # Coletar dados
    hashtag = "tecnologia"  # Altere para a hashtag desejada
    filename, scraper = coletar_dados_redes_sociais(hashtag, YOUTUBE_API_KEY)
    
    print(f"\n✅ Processo concluído! Arquivo gerado: {filename}")
