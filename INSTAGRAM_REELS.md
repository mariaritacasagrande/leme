# 📸 Instagram: Coleta de Reels com Duração

## 🎯 O Que o Sistema Coleta no Instagram

### ✅ APENAS REELS (Vídeos)
O sistema foi configurado para coletar **exclusivamente Reels do Instagram**, que são vídeos curtos semelhantes aos do TikTok.

**NÃO coletamos:**
- ❌ Posts de imagem estáticos
- ❌ Carrosséis de fotos
- ❌ Stories (são efêmeros)

**SIM coletamos:**
- ✅ Reels (vídeos de 15-90 segundos)
- ✅ Todos com duração completa
- ✅ Métricas de engajamento

---

## ⏱️ Duração dos Reels

### Características dos Reels do Instagram:
- **Duração mínima**: 15 segundos
- **Duração máxima**: 90 segundos (1:30)
- **Típico**: Entre 20-60 segundos
- **SEMPRE incluída** nos dados coletados

### Formato da Duração:
```
Duração em segundos: 45
Duração formatada: 00:45

Duração em segundos: 75
Duração formatada: 01:15
```

---

## 📊 Dados Coletados por Reel

Cada Reel do Instagram contém:

```
┌────────────────────┬──────────────────────────┐
│ Campo              │ Exemplo                  │
├────────────────────┼──────────────────────────┤
│ Plataforma         │ Instagram                │
│ Hashtag            │ fitness                  │
│ Perfil             │ @influencer_tech         │
│ Título             │ Reel sobre fitness #5    │
│ Video ID           │ ig_reel_4                │
│ Likes              │ 12,345                   │
│ Comentários        │ 567                      │
│ Visualizações      │ 89,012                   │
│ Salvamentos        │ 1,234                    │
│ Duração (segundos) │ 45                       │
│ Duração (formato)  │ 00:45                    │
│ Data Publicação    │ 2024-12-01               │
│ URL                │ instagram.com/reel/...   │
└────────────────────┴──────────────────────────┘
```

---

## 🔍 Por Que Apenas Reels?

### Razões Técnicas:
1. **Duração mensurável**: Reels são vídeos, têm tempo definido
2. **Comparabilidade**: Podemos comparar com YouTube e TikTok
3. **Tendência do mercado**: Instagram está focando em Reels
4. **API limitada**: Acesso facilitado a vídeos vs. posts estáticos

### Razões de Negócio:
1. **Engajamento**: Reels têm maior alcance que posts estáticos
2. **Formato viral**: Conteúdo mais compartilhável
3. **Algoritmo favorece**: Instagram prioriza Reels no feed
4. **Análise consistente**: Todos os dados têm métricas similares

---

## 📈 Como o Instagram Aparece no Excel

### Aba "Instagram" (Exemplo Real):
```
Hashtag  | Perfil            | Título           | Likes  | Coment | Salv  | Duração | URL
---------|-------------------|------------------|--------|--------|-------|---------|------------------
fitness  | @influencer_tech  | Reel treino casa | 12,345 |   567  | 1,234 |  00:45  | instagram.com/...
fitness  | @creator_digital  | Reel cardio      | 8,976  |   234  |   876 |  00:30  | instagram.com/...
fitness  | @brand_inovacao   | Reel yoga        | 15,432 |   789  | 2,456 |  01:15  | instagram.com/...
```

**Todos os Reels têm:**
- ✅ Duração em segundos
- ✅ Duração formatada (MM:SS)
- ✅ Número de salvamentos (métrica exclusiva do Instagram)

---

## 🎬 Comparação: Reels vs TikTok vs YouTube Shorts

| Característica      | Instagram Reels | TikTok         | YouTube Shorts |
|---------------------|-----------------|----------------|----------------|
| **Duração Típica**  | 15-90 segundos  | 15-180 segundos| 15-60 segundos |
| **Salvamentos**     | ✅ Sim          | ✅ Sim         | ❌ Não         |
| **Formato**         | Vertical 9:16   | Vertical 9:16  | Vertical 9:16  |
| **Algoritmo**       | Alto alcance    | Alto alcance   | Médio alcance  |
| **API Disponível**  | ⚠️ Restrita     | ⚠️ Beta        | ✅ Sim         |

---

## 📊 Estatísticas Típicas de Reels

### Engajamento Médio (dados de exemplo):
```
Likes médios: 8.000 - 15.000 por Reel
Comentários médios: 200 - 500 por Reel
Salvamentos médios: 500 - 2.000 por Reel
Taxa de engajamento: 2-5% (muito bom)
```

### Durações Mais Performáticas:
```
30-45 segundos: ⭐⭐⭐⭐⭐ (Melhor retenção)
15-30 segundos: ⭐⭐⭐⭐ (Bom para viralização)
45-60 segundos: ⭐⭐⭐ (Conteúdo mais profundo)
60-90 segundos: ⭐⭐ (Menor retenção)
```

---

## 🔧 Como Funciona a Coleta (Técnico)

### Fluxo de Coleta:
```python
1. Sistema busca hashtag no Instagram
   └─> Filtra apenas conteúdo tipo "REEL"

2. Para cada Reel encontrado:
   ├─> Extrai perfil do criador
   ├─> Conta likes, comentários, salvamentos
   ├─> Obtém duração do vídeo
   └─> Salva URL do Reel

3. Valida dados:
   ├─> Duração sempre > 0
   ├─> Formato de duração válido
   └─> Todas métricas presentes

4. Exporta para Excel:
   └─> Aba "Instagram" com apenas Reels
```

### Código de Exemplo:
```python
from social_media_scraper import SocialMediaScraper

scraper = SocialMediaScraper()

# Buscar Reels com hashtag específica
reels = scraper.search_instagram("marketing", max_results=20)

# Verificar que todos têm duração
for reel in reels:
    print(f"Reel: {reel['titulo']}")
    print(f"Duração: {reel['duracao_formatada']}")
    print(f"Salvamentos: {reel['salvamentos']}")
    print("---")
```

---

## ⚠️ Importante Saber

### Limitações da API do Instagram:
1. **Requer conta Business/Creator**
   - Não funciona com conta pessoal padrão
   
2. **Processo de aprovação**
   - Precisa criar app no Facebook Developers
   - Solicitar permissões específicas
   
3. **Rate Limits rigorosos**
   - Limite de requisições por hora
   - Recomendado: usar com moderação

4. **Dados públicos apenas**
   - Não acessa contas privadas
   - Apenas Reels públicos com a hashtag

### Modo de Demonstração:
Sem API configurada, o sistema usa **dados de exemplo realistas** que simulam Reels reais do Instagram, todos com duração incluída.

---

## 💡 Dicas de Análise

### Perguntas que Você Pode Responder:

1. **Qual duração de Reel performa melhor?**
   ```
   Filtre por faixa de duração e compare likes médios
   ```

2. **Qual horário é melhor para postar?**
   ```
   Agrupe por hora de publicação (data_publicacao)
   ```

3. **Salvamentos indicam qualidade?**
   ```
   Compare taxa salvamentos/likes entre Reels
   ```

4. **Qual tipo de conteúdo viraliza mais?**
   ```
   Analise títulos dos Reels com mais engajamento
   ```

---

## ✅ Checklist de Validação

Ao receber os dados, verifique:

- [ ] Todos os registros do Instagram são Reels
- [ ] Todos têm duração > 0 segundos
- [ ] Duração está formatada (MM:SS)
- [ ] Salvamentos estão incluídos
- [ ] URLs apontam para /reel/ (não /p/)
- [ ] Métricas de engajamento presentes

---

## 🎯 Casos de Uso

### Marketing Digital:
```
"Quero saber qual duração de Reel gera mais salvamentos"
└─> Analise coluna salvamentos vs duracao_segundos
```

### Criadores de Conteúdo:
```
"Preciso entender qual estilo de Reel engaja mais"
└─> Compare likes/comentários por perfil similar ao seu
```

### Agências:
```
"Cliente quer comparar performance em todas as plataformas"
└─> Use aba "Resumo por Plataforma" para comparar Instagram vs outras
```

### Pesquisa de Mercado:
```
"Analisar tendências de conteúdo na minha indústria"
└─> Colete múltiplas hashtags e identifique padrões
```

---

## 📚 Recursos Adicionais

- [Documentação Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Melhores Práticas para Reels](https://business.instagram.com/reels)
- [Métricas do Instagram Insights](https://help.instagram.com/insights)

---

**Resumo**: O sistema coleta **apenas Reels** do Instagram, garantindo que **100% dos dados** incluem duração, salvamentos e métricas completas de engajamento! 📸✨
