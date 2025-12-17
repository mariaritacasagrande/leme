# 📊 Sistema de Coleta e Análise de Redes Sociais

Sistema completo para coleta, análise e visualização de dados de redes sociais (Instagram, TikTok e YouTube) baseado em hashtags específicas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Funcionalidades

### Coleta de Dados
- ✅ Busca por hashtags específicas
- ✅ Suporte para YouTube, Instagram (Reels) e TikTok
- ✅ **Instagram**: Foca apenas em Reels (vídeos), não em posts de imagem
- ✅ Integração com APIs oficiais
- ✅ Dados de exemplo para testes (sem necessidade de API keys)

### Métricas Coletadas
- 👤 Nome do perfil/canal
- ❤️ Número de likes
- 💬 Número de comentários  
- 💾 Número de salvamentos (quando disponível)
- ⏱️ Duração do vídeo/conteúdo (minutagem completa)
- 📅 Data de publicação
- 🔗 URL do conteúdo original
- 👁️ Visualizações (quando disponível)

### Visualização e Exportação
- 📊 Dashboard interativo com gráficos
- 📈 Análise de engajamento por plataforma
- 📉 Comparação de perfis
- 📄 Exportação para Excel (.xlsx)
- 🎨 Gráficos interativos com Plotly
- 🔍 Filtros avançados de dados

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
# Se usando git
git clone <url-do-repositorio>
cd social-media-scraper

# Ou baixe e extraia o arquivo ZIP
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. (Opcional) Configure as API Keys

Para coleta de dados reais, você precisará de API keys:

#### YouTube Data API v3
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a "YouTube Data API v3"
4. Crie credenciais → API Key
5. Copie sua API key

#### Instagram Graph API
1. Converta sua conta para Business/Creator
2. Crie um app em [Facebook Developers](https://developers.facebook.com/)
3. Configure o Instagram Graph API
4. Obtenha um Access Token

#### TikTok API
⚠️ **Nota**: A API do TikTok está em beta e tem acesso muito limitado.

## 💻 Como Usar

### Método 1: Dashboard Interativo (Recomendado)

Execute o dashboard web interativo:

```bash
streamlit run dashboard.py
```

O dashboard abrirá automaticamente no seu navegador (http://localhost:8501)

**Funcionalidades do Dashboard:**
- 🔍 Coletar novos dados por hashtag
- 📊 Visualizar dados em gráficos interativos
- 📥 Download de dados em Excel
- 🔎 Filtros avançados
- 📈 Estatísticas em tempo real

### Método 2: Linha de Comando

Execute o script principal:

```bash
python social_media_scraper.py
```

Ou use o script de exemplos:

```bash
python exemplo_uso.py
```

### Método 3: Integração no seu código

```python
from social_media_scraper import SocialMediaScraper

# Criar instância
scraper = SocialMediaScraper()

# Configurar API (opcional)
scraper.configure_apis(youtube_key="SUA_API_KEY")

# Coletar dados
dados = scraper.search_all_platforms("tecnologia", max_results_per_platform=30)

# Exportar para Excel
scraper.export_to_excel("meus_dados.xlsx")

# Obter estatísticas
stats = scraper.get_statistics()
print(f"Total de posts: {stats['total_posts']}")
print(f"Total de likes: {stats['total_likes']:,}")
```

## 📊 Exemplos de Uso

### Exemplo 1: Coleta Básica

```python
from social_media_scraper import coletar_dados_redes_sociais

# Coletar dados de uma hashtag
filename, scraper = coletar_dados_redes_sociais("marketing")
```

### Exemplo 2: YouTube Apenas

```python
scraper = SocialMediaScraper()
dados_youtube = scraper.search_youtube("python", max_results=20)
```

### Exemplo 3: Com API Key

```python
scraper = SocialMediaScraper()
scraper.configure_apis(youtube_key="AIzaSy...")

dados = scraper.search_youtube("tecnologia", max_results=50)
scraper.export_to_excel("dados_youtube.xlsx")
```

### Exemplo 4: Análise Comparativa

```python
hashtags = ["tecnologia", "inovacao", "digital"]

for hashtag in hashtags:
    scraper = SocialMediaScraper()
    scraper.search_all_platforms(hashtag, max_results_per_platform=25)
    scraper.export_to_excel(f"analise_{hashtag}.xlsx")
```

## 📁 Estrutura dos Dados Exportados

O arquivo Excel gerado contém **múltiplas abas organizadas**:

### Aba 1: Todos os Dados
Consolidação de todas as informações coletadas de todas as plataformas

### Abas 2-4: YouTube, Instagram e TikTok (Separadas)
**Uma aba dedicada para cada plataforma** contendo apenas os posts daquela rede social:
- YouTube: Todos os vídeos do YouTube
- Instagram: Todos os posts do Instagram  
- TikTok: Todos os vídeos do TikTok

Cada aba contém:
- Hashtag pesquisada
- Nome do perfil
- Título do conteúdo
- Video ID
- Likes
- Comentários
- Visualizações
- Salvamentos (quando disponível)
- Duração (segundos e formatada MM:SS)
- Data de publicação
- URL do conteúdo

### Aba: Resumo por Plataforma
Estatísticas agregadas por rede social:
- Total de posts
- Total de likes
- Total de comentários
- Engajamento total
- Média de likes por post
- Média de comentários por post
- Duração média dos vídeos

### Aba: Top 20 Perfis
Ranking dos 20 perfis com maior engajamento:
- Plataforma
- Nome do perfil
- Total de likes
- Total de comentários
- Engajamento total

**Benefício**: Com as abas separadas, você pode analisar cada plataforma individualmente ou fazer comparações entre elas facilmente!

## 🎨 Dashboard - Visualizações Disponíveis

### Métricas Principais
- Total de posts coletados
- Total de likes
- Total de comentários
- Média de likes por post
- Duração média dos vídeos

### Gráficos
- 📊 Pizza: Distribuição por plataforma
- 📊 Barras: Engajamento por plataforma
- 📊 Barras Horizontais: Top 10 perfis
- 📊 Histograma: Distribuição de durações
- 📊 Scatter: Correlação likes vs comentários

### Filtros
- Por plataforma
- Por número mínimo de likes
- Por perfis específicos

## ⚙️ Configuração Avançada

### Rate Limiting

O sistema implementa delays entre requisições para evitar bloqueios:

```python
time.sleep(1)  # 1 segundo entre plataformas
```

### Customização de Resultados

```python
# Aumentar número de resultados
scraper.search_youtube("hashtag", max_results=50)

# Coletar de plataforma específica
dados = scraper.search_instagram("moda", max_results=30)
```

### Tratamento de Erros

O sistema possui tratamento robusto de erros:
- Retorna dados de exemplo se API falhar
- Logs informativos de cada etapa
- Continua execução mesmo com erros parciais

## 🔐 Limitações e Considerações

### Limitações Técnicas
- **YouTube**: 10.000 unidades/dia (gratuito)
- **Instagram**: Requer conta Business, rate limits rigorosos, coleta apenas Reels (vídeos com duração)
- **TikTok**: API em beta, acesso muito limitado

### Considerações Legais
- ⚠️ Sempre respeite os Termos de Serviço das plataformas
- ⚠️ Use APIs oficiais quando possível
- ⚠️ Não use para spam ou coleta massiva não autorizada
- ⚠️ Respeite a privacidade dos usuários

### Boas Práticas
- ✅ Implemente rate limiting adequado
- ✅ Armazene API keys de forma segura
- ✅ Não compartilhe suas credenciais
- ✅ Monitore seu uso de API
- ✅ Use dados coletados de forma ética

## 🐛 Solução de Problemas

### Erro: "API Key não configurada"
**Solução**: Configure sua API key ou use o modo de exemplo:
```python
scraper.configure_apis(youtube_key="SUA_KEY")
```

### Erro: "Module not found"
**Solução**: Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Quota exceeded" (YouTube)
**Solução**: Você atingiu o limite diário gratuito. Aguarde 24h ou solicite aumento de quota.

### Dashboard não abre
**Solução**: Verifique se o Streamlit está instalado:
```bash
pip install streamlit
streamlit run dashboard.py
```

## 📚 Estrutura de Arquivos

```
social-media-scraper/
│
├── social_media_scraper.py   # Classe principal de coleta
├── dashboard.py               # Dashboard interativo Streamlit
├── exemplo_uso.py             # Scripts de exemplo
├── requirements.txt           # Dependências do projeto
├── README.md                  # Este arquivo
│
└── dados/                     # Diretório de saída (criado automaticamente)
    ├── dados_*.xlsx          # Arquivos Excel gerados
    └── ...
```

## 🔄 Próximas Melhorias

- [ ] Suporte para Twitter/X
- [ ] Análise de sentimentos dos comentários
- [ ] Detecção de tendências
- [ ] Agendamento automático de coletas
- [ ] API REST para integração
- [ ] Exportação para outros formatos (CSV, JSON)
- [ ] Machine Learning para previsões

## 📝 Licença

Este projeto é fornecido "como está" para fins educacionais e de pesquisa.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 📧 Suporte

Para dúvidas e suporte:
- Abra uma issue no repositório
- Consulte a documentação das APIs oficiais
- Verifique os exemplos incluídos

## 🙏 Agradecimentos

- Google YouTube Data API
- Meta Instagram Graph API
- Streamlit Framework
- Comunidade Python

---

**Desenvolvido com ❤️ para análise de redes sociais**

⭐ Se este projeto foi útil, considere dar uma estrela!
