# 🚀 INÍCIO RÁPIDO - Sistema de Coleta de Redes Sociais

## ⚡ Começar em 3 Passos

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar o Dashboard
```bash
streamlit run dashboard.py
```

### 3️⃣ Coletar Dados
No dashboard que abrir:
1. Vá em "Coletar Novos Dados"
2. Digite uma hashtag (ex: "tecnologia")
3. Clique em "Iniciar Coleta"
4. Download o Excel gerado!

---

## 🎯 Métodos de Uso

### Opção A: Dashboard Web (Mais Fácil) ⭐
```bash
streamlit run dashboard.py
```
- Interface visual completa
- Gráficos interativos
- Download direto de Excel
- Não precisa programar

### Opção B: Script Python
```bash
python exemplo_uso.py
```
- Menu interativo no terminal
- 4 exemplos prontos
- Exporta Excel automaticamente

### Opção C: No Seu Código
```python
from social_media_scraper import coletar_dados_redes_sociais

# Coletar dados
filename, scraper = coletar_dados_redes_sociais("marketing")
```

---

## 📊 O Que Você Recebe

### Arquivo Excel com Múltiplas Abas:
1. **Todos os Dados**: Consolidação completa de todas as plataformas

2. **YouTube** (Aba separada): Todos os vídeos do YouTube
   - Perfil, Likes, Comentários, Duração, URL

3. **Instagram** (Aba separada): Todos os posts do Instagram
   - Perfil, Likes, Comentários, Salvamentos, Duração, URL

4. **TikTok** (Aba separada): Todos os vídeos do TikTok
   - Perfil, Likes, Comentários, Salvamentos, Duração, URL

5. **Resumo por Plataforma**: Estatísticas agregadas
   - Total de posts, likes, comentários por rede social

6. **Top 20 Perfis**: Ranking de perfis com mais engajamento

### Dados Coletados por Post:
- ✅ Nome do perfil
- ✅ Número de likes
- ✅ Número de comentários
- ✅ Salvamentos (Instagram/TikTok)
- ✅ **Duração completa do vídeo** (MM:SS)
- ✅ Data de publicação
- ✅ URL do post

---

## 🔑 Usar API do YouTube (Opcional)

**Sem API Key**: Sistema usa dados de exemplo (perfeito para testes)

**Com API Key** (dados reais):
1. Leia o arquivo `GUIA_API_YOUTUBE.md`
2. Obtenha sua key gratuita em 5 minutos
3. Configure no dashboard ou no código

```python
scraper.configure_apis(youtube_key="SUA_KEY_AQUI")
```

---

## 📁 Arquivos do Projeto

```
📂 Projeto
├── 📄 social_media_scraper.py  ← Motor principal
├── 📄 dashboard.py              ← Interface web
├── 📄 exemplo_uso.py            ← Exemplos práticos
├── 📄 requirements.txt          ← Dependências
├── 📘 README.md                 ← Documentação completa
├── 📘 GUIA_API_YOUTUBE.md       ← Como obter API key
└── 📘 INICIO_RAPIDO.md          ← Este arquivo
```

---

## 🎨 Preview do Dashboard

O dashboard mostra:
- 📊 5 Métricas principais (posts, likes, comentários, etc)
- 📈 Gráfico de pizza: distribuição por plataforma
- 📊 Gráfico de barras: engajamento por plataforma
- 🏆 Top 10 perfis por likes
- ⏱️ Distribuição de durações
- 💬 Scatter plot: likes vs comentários
- 📋 Tabela completa com filtros
- 📥 Download Excel

---

## ⚡ Exemplo Mais Simples

```python
# Use sem configuração alguma (dados de exemplo)
from social_media_scraper import coletar_dados_redes_sociais

coletar_dados_redes_sociais("tecnologia")
# Pronto! Excel criado automaticamente
```

---

## 🆘 Precisa de Ajuda?

1. **Erro ao instalar**: 
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Dashboard não abre**:
   ```bash
   pip install streamlit
   streamlit run dashboard.py
   ```

3. **Ver documentação completa**: Abra `README.md`

4. **Configurar YouTube API**: Abra `GUIA_API_YOUTUBE.md`

---

## 💡 Dica Final

Comece com o dashboard! É a forma mais fácil e visual de usar o sistema:
```bash
streamlit run dashboard.py
```

Depois explore os exemplos de código no `exemplo_uso.py` 🚀

---

**Pronto para começar? Execute `streamlit run dashboard.py` agora! 🎉**
