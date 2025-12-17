# 🔑 Guia: Como Obter API Key do YouTube

Este guia passo a passo mostra como obter gratuitamente uma API key do YouTube para usar no sistema de coleta de dados.

## 📋 Pré-requisitos

- Conta Google ativa
- Navegador web

## 🚀 Passo a Passo

### 1. Acesse o Google Cloud Console

Vá para: https://console.cloud.google.com/

Faça login com sua conta Google.

### 2. Crie um Novo Projeto

1. No topo da página, clique no seletor de projetos
2. Clique em "NOVO PROJETO"
3. Dê um nome ao projeto (ex: "Social Media Scraper")
4. Clique em "Criar"
5. Aguarde alguns segundos até o projeto ser criado

### 3. Ative a YouTube Data API v3

1. No menu lateral esquerdo, vá em "APIs e Serviços" → "Biblioteca"
   - Ou acesse diretamente: https://console.cloud.google.com/apis/library

2. Na barra de busca, digite: "YouTube Data API v3"

3. Clique no resultado "YouTube Data API v3"

4. Clique no botão "ATIVAR"

5. Aguarde a ativação (leva alguns segundos)

### 4. Crie Credenciais (API Key)

1. Após ativar, você verá uma página pedindo para criar credenciais
   - Ou vá em "APIs e Serviços" → "Credenciais"

2. Clique em "+ CRIAR CREDENCIAIS" no topo

3. Selecione "Chave de API"

4. Uma janela aparecerá mostrando sua nova API key
   - Ela será algo como: `AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q`

5. **IMPORTANTE**: Copie e guarde essa chave em um lugar seguro!

### 5. (Opcional) Restringir a API Key

Por segurança, você pode restringir o uso da sua API key:

1. Clique em "RESTRINGIR CHAVE"

2. Em "Restrições de aplicativo":
   - Selecione "Endereços IP" se for usar apenas no seu computador
   - Ou "Referenciadores HTTP" se for usar em um site
   - Ou deixe "Nenhum" para testes

3. Em "Restrições de API":
   - Clique em "Restringir chave"
   - Marque apenas "YouTube Data API v3"

4. Clique em "SALVAR"

### 6. Teste sua API Key

Execute este código para testar:

```python
import requests

API_KEY = "SUA_API_KEY_AQUI"
url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=python&type=video&maxResults=1&key={API_KEY}"

response = requests.get(url)
if response.status_code == 200:
    print("✅ API Key funcionando!")
    print(f"Resultado: {response.json()}")
else:
    print(f"❌ Erro: {response.status_code}")
    print(response.text)
```

### 7. Configure no Sistema

Edite o arquivo `social_media_scraper.py` ou use diretamente:

```python
from social_media_scraper import SocialMediaScraper

scraper = SocialMediaScraper()
scraper.configure_apis(youtube_key="SUA_API_KEY_AQUI")

# Agora pode usar normalmente
dados = scraper.search_youtube("tecnologia", max_results=20)
```

Ou no dashboard interativo, cole a API key no campo apropriado.

## 📊 Limites da API Gratuita

### Quota Diária
- **10.000 unidades por dia** (gratuito)
- Cada busca consome aproximadamente 100 unidades
- Isso significa ~100 buscas por dia

### Consumo por Operação
- **Search** (busca): 100 unidades
- **Videos.list** (detalhes): 1 unidade por vídeo
- **Comentários**: 1 unidade

### Exemplo de Cálculo
Para buscar 30 vídeos com detalhes completos:
- 1 busca (search): 100 unidades
- 30 vídeos (details): 30 unidades
- **Total**: 130 unidades

Com 10.000 unidades/dia, você pode fazer aproximadamente 75 buscas completas por dia.

## ⚠️ Problemas Comuns

### Erro 403: "Quota exceeded"
**Causa**: Você atingiu o limite diário de 10.000 unidades

**Solução**:
- Aguarde até o próximo dia (reset às 00:00 PST)
- Ou solicite aumento de quota no Google Cloud Console

### Erro 400: "Bad Request"
**Causa**: Parâmetros inválidos na requisição

**Solução**:
- Verifique se a hashtag não tem caracteres especiais
- Use palavras-chave simples

### Erro 401: "Invalid API key"
**Causa**: API key incorreta ou não ativada

**Solução**:
- Verifique se copiou a key completa
- Confirme que ativou a YouTube Data API v3
- Aguarde alguns minutos após criar a key

## 🔒 Segurança da API Key

### ❌ NÃO FAÇA:
- Compartilhar sua API key publicamente
- Commitar a key em repositórios públicos no GitHub
- Usar a mesma key em produção e desenvolvimento
- Deixar a key no código-fonte sem proteção

### ✅ FAÇA:
- Use variáveis de ambiente
- Restrinja o uso da API key por IP ou domínio
- Monitore o uso no Google Cloud Console
- Revogue e recrie keys comprometidas

### Exemplo Seguro

Crie um arquivo `.env` (não commite no git):
```
YOUTUBE_API_KEY=AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q
```

Use no código:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')
```

## 📈 Aumentar a Quota

Se precisar de mais de 10.000 unidades/dia:

1. Acesse o Google Cloud Console
2. Vá em "APIs e Serviços" → "YouTube Data API v3"
3. Clique em "Quotas"
4. Clique em "SOLICITAR AUMENTO DE QUOTA"
5. Preencha o formulário explicando seu uso
6. Aguarde aprovação (pode levar alguns dias)

**Nota**: Aumentos de quota podem ter custo adicional.

## 💰 Custo

- **Gratuito**: 10.000 unidades/dia
- **Pago**: Após exceder, você será cobrado por unidade adicional
- **Preço**: Consulte a página oficial de preços do Google Cloud

## 📚 Recursos Adicionais

- [Documentação Oficial](https://developers.google.com/youtube/v3)
- [Referência da API](https://developers.google.com/youtube/v3/docs)
- [Calculadora de Quotas](https://developers.google.com/youtube/v3/determine_quota_cost)
- [Suporte do Google Cloud](https://cloud.google.com/support)

## 🎯 Próximos Passos

Agora que você tem sua API key:

1. ✅ Configure no sistema usando o método acima
2. ✅ Execute alguns testes com hashtags simples
3. ✅ Monitore seu uso de quota no console
4. ✅ Explore as funcionalidades do dashboard

---

**Dica**: Salve este guia para referência futura! A API key não expira, mas mantenha-a segura.
