"""
Exemplo de Uso Simples - Sistema de Coleta de Redes Sociais

Este script demonstra como usar o sistema de forma básica
"""

from social_media_scraper import SocialMediaScraper
from datetime import datetime

def exemplo_basico():
    """Exemplo básico de coleta de dados"""
    print("="*60)
    print("EXEMPLO BÁSICO - Coleta de Dados de Redes Sociais")
    print("="*60 + "\n")
    
    # Criar instância do scraper
    scraper = SocialMediaScraper()
    
    # Configurar API do YouTube (opcional)
    # scraper.configure_apis(youtube_key="SUA_API_KEY_AQUI")
    
    # Definir hashtag para buscar
    hashtag = "tecnologia"
    
    print(f"🔍 Buscando posts com hashtag: #{hashtag}\n")
    
    # Coletar dados de todas as plataformas
    dados = scraper.search_all_platforms(hashtag, max_results_per_platform=20)
    
    # Exibir resumo
    print("\n" + "="*60)
    print("RESUMO DOS DADOS COLETADOS")
    print("="*60)
    
    print(f"\n📊 Total de posts coletados: {len(dados)}")
    
    # Estatísticas por plataforma
    from collections import Counter
    plataformas = Counter([d['plataforma'] for d in dados])
    
    print("\n📱 Posts por plataforma:")
    for plataforma, count in plataformas.items():
        print(f"   - {plataforma}: {count} posts")
    
    # Estatísticas de engajamento
    total_likes = sum(d['likes'] for d in dados)
    total_comentarios = sum(d['comentarios'] for d in dados)
    
    print(f"\n❤️  Total de likes: {total_likes:,}")
    print(f"💬 Total de comentários: {total_comentarios:,}")
    print(f"📊 Média de likes por post: {total_likes // len(dados):,}")
    
    # Exportar para Excel
    print("\n📄 Exportando dados para Excel...")
    filename = scraper.export_to_excel(f"dados_{hashtag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    
    print(f"\n✅ Processo concluído!")
    print(f"📁 Arquivo gerado: {filename}")
    print("\n" + "="*60)
    
    return dados, filename


def exemplo_youtube_apenas():
    """Exemplo coletando apenas do YouTube"""
    print("\n" + "="*60)
    print("EXEMPLO - YouTube Apenas")
    print("="*60 + "\n")
    
    scraper = SocialMediaScraper()
    
    # Buscar apenas no YouTube
    hashtag = "python"
    print(f"🔍 Buscando vídeos do YouTube com hashtag: #{hashtag}\n")
    
    dados_youtube = scraper.search_youtube(hashtag, max_results=15)
    
    # Mostrar top 5 vídeos por likes
    print("\n🏆 Top 5 vídeos por likes:")
    dados_ordenados = sorted(dados_youtube, key=lambda x: x['likes'], reverse=True)[:5]
    
    for i, video in enumerate(dados_ordenados, 1):
        print(f"\n{i}. {video['titulo']}")
        print(f"   Canal: {video['perfil']}")
        print(f"   Likes: {video['likes']:,}")
        print(f"   Comentários: {video['comentarios']:,}")
        print(f"   Duração: {video['duracao_formatada']}")
    
    return dados_youtube


def exemplo_com_estatisticas():
    """Exemplo mostrando estatísticas detalhadas"""
    print("\n" + "="*60)
    print("EXEMPLO - Estatísticas Detalhadas")
    print("="*60 + "\n")
    
    scraper = SocialMediaScraper()
    hashtag = "marketing"
    
    # Coletar dados
    scraper.search_all_platforms(hashtag, max_results_per_platform=25)
    
    # Obter estatísticas
    stats = scraper.get_statistics()
    
    print("📊 ESTATÍSTICAS GERAIS:\n")
    print(f"Total de posts: {stats['total_posts']}")
    print(f"Total de likes: {stats['total_likes']:,}")
    print(f"Total de comentários: {stats['total_comentarios']:,}")
    print(f"Média de likes por post: {stats['media_likes']:.0f}")
    print(f"Média de comentários por post: {stats['media_comentarios']:.0f}")
    print(f"Perfis únicos: {stats['perfis_unicos']}")
    
    # Converter duração média para formato legível
    duracao_segundos = int(stats['duracao_media_segundos'])
    minutos = duracao_segundos // 60
    segundos = duracao_segundos % 60
    print(f"Duração média dos vídeos: {minutos}m {segundos}s")
    
    print("\n📱 Posts por plataforma:")
    for plataforma, count in stats['por_plataforma'].items():
        print(f"   - {plataforma}: {count} posts")
    
    # Exportar
    scraper.export_to_excel(f"estatisticas_{hashtag}.xlsx")
    
    return stats


def exemplo_comparacao_hashtags():
    """Exemplo comparando múltiplas hashtags"""
    print("\n" + "="*60)
    print("EXEMPLO - Comparação de Hashtags")
    print("="*60 + "\n")
    
    scraper = SocialMediaScraper()
    hashtags = ["tecnologia", "inovacao", "digital"]
    
    resultados = {}
    
    for hashtag in hashtags:
        print(f"\n🔍 Analisando #{hashtag}...")
        scraper.search_all_platforms(hashtag, max_results_per_platform=15)
        resultados[hashtag] = scraper.get_statistics()
    
    # Comparação
    print("\n" + "="*60)
    print("COMPARAÇÃO DE HASHTAGS")
    print("="*60 + "\n")
    
    print(f"{'Hashtag':<15} {'Posts':<10} {'Likes':<15} {'Comentários':<15}")
    print("-" * 60)
    
    for hashtag, stats in resultados.items():
        print(f"#{hashtag:<14} {stats['total_posts']:<10} {stats['total_likes']:<15,} {stats['total_comentarios']:<15,}")
    
    return resultados


def menu_principal():
    """Menu interativo para escolher exemplos"""
    print("\n" + "="*70)
    print(" "*15 + "🚀 SISTEMA DE COLETA DE REDES SOCIAIS")
    print("="*70)
    
    print("\nEscolha um exemplo para executar:\n")
    print("1. Exemplo Básico (coleta de todas as plataformas)")
    print("2. Exemplo YouTube Apenas")
    print("3. Exemplo com Estatísticas Detalhadas")
    print("4. Exemplo Comparação de Hashtags")
    print("5. Sair")
    
    escolha = input("\nDigite o número da opção desejada: ")
    
    print("\n")
    
    if escolha == "1":
        exemplo_basico()
    elif escolha == "2":
        exemplo_youtube_apenas()
    elif escolha == "3":
        exemplo_com_estatisticas()
    elif escolha == "4":
        exemplo_comparacao_hashtags()
    elif escolha == "5":
        print("👋 Até logo!")
        return
    else:
        print("⚠️  Opção inválida!")
        return
    
    # Perguntar se quer executar outro exemplo
    print("\n" + "="*70)
    continuar = input("\nDeseja executar outro exemplo? (s/n): ")
    
    if continuar.lower() == 's':
        menu_principal()


if __name__ == "__main__":
    # Menu interativo
    menu_principal()
