# 🎬 CineData Analytics

Agente IA para realizar consultas e análises sobre o catálogo de filmes do banco de dados **CineRocket** usando **PydanticAI** e modelos LLM via OpenRouter.

## 📊 O que é?

CineData Analytics é um assistente inteligente que permite análises avançadas sobre dados de filmes, atores, produtoras, gêneros e performance de bilheteria através de conversas em linguagem natural.

Você pode fazer perguntas como:
- "Quais foram os 10 filmes com maior receita em R$?"
- "Qual ator participou de mais filmes nos últimos 5 anos?"
- "Qual é a receita média por gênero?"
- "Quais filmes têm maior divergência entre avaliações IMDb e TMDb?"

## 🏗️ Arquitetura

```
┌─────────────────┐
│  Usuário (CLI)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Agente PydanticAI             │
│  (system_prompt + tools)        │
└────────┬────────────────────────┘
         │
         ├─► query_db()    → Executa SQL customizado
         ├─► get_schema()  → Schema do banco para referência
         └─► find_movie()  → Busca filmes por título
         │
         ▼
┌──────────────────────────────────┐
│  DatabaseManager (SQLite)        │
│  Database: cinerocket.db (555MB) │
└──────────────────────────────────┘
```

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes)

### 1. Instalação

```bash
# Clonar o repositório
git clone <seu-repo>
cd cinedata-analytics

# Instalar dependências
uv sync
```

### 2. Executar

```bash
# Via CLI interativa
uv run src/cinedata/cli.py
```

**Nota:** O projeto já inclui a chave OpenRouter API no `.env` configurada para modelos gratuitos (`openrouter/free`), permitindo testes imediatos sem configuração adicional.

## 📚 Estrutura do Projeto

```
cinedata-analytics/
├── src/cinedata/
│   ├── __init__.py        # Pacote
│   ├── __main__.py        # Entry point
│   ├── config.py          # Variáveis de ambiente
│   ├── database.py        # Gerenciador SQLite
│   ├── agent.py           # Agente PydanticAI com tools
│   └── cli.py             # Interface interativa
├── tests/
│   ├── __init__.py
│   └── test_database.py   # Testes unitários
├── cinerocket.db          # Banco de dados (555MB)
├── pyproject.toml         # Dependências
├── .env                   # Configuração (com chave pré-configurada)
├── .gitignore
└── README.md
```

## 🛠️ Componentes Principais

### `config.py`
Carrega e valida todas as variáveis de ambiente:
- `OPENROUTER_API_KEY`: Chave da API OpenRouter
- `MODELO_LLM`: Modelo LLM a ser utilizado
- `DB_PATH`: Caminho para o banco de dados SQLite

### `database.py`
Classe `DatabaseManager` que gerencia:
- Conexões com SQLite
- Execução de queries SQL
- Recuperação do schema do banco
- Tratamento de erros

### `agent.py`
Agente PydanticAI com:
- System prompt configurado para análises de cinema
- Tool: `query_db()` - executa SQL customizado
- Tool: `get_schema()` - referência das tabelas e campos
- Tool: `find_movie()` - busca filmes por título
- Modelo de resposta estruturado (`AnalysisResult`) com answer, data_points e query_used
- Modelo: `openrouter/free` (seleção automática de modelo gratuito)

### `cli.py`
Interface interativa que:
- Apresenta loop principal assíncrono
- Aceita perguntas do usuário
- Exibe respostas do agente formatadas
- Mostra queries SQL e dados utilizados

## 📊 Base de Dados

O banco de dados **cinerocket.db** contém:

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `dim_movies` | 95,645 | Dimensão de filmes |
| `dim_genres` | 19 | Dimensão de gêneros |
| `dim_people` | 424,656 | Dimensão de pessoas (atores/diretores) |
| `dim_companies` | 45,941 | Dimensão de produtoras |
| `fact_movies_performance` | 95,645 | Fatos de performance (receita, orçamento, notas) |
| `dim_reviews` | 40,267 | Dimensão de avaliações |
| `movie_reviews` | 43,666 | Reviews individuais |
| `bridge_movie_genre` | 121,521 | Relacionamento filme-gênero |
| `bridge_movie_person` | 745,450 | Relacionamento filme-pessoa |
| `bridge_movie_company` | 116,326 | Relacionamento filme-empresa |

## 🎯 Exemplos de Uso

### CLI Interativa
```bash
$ uv run src/cinedata/cli.py

================================================================================
🎬 CineData Analytics
================================================================================

Pergunte sobre filmes, atores, bilheteria, etc.
Tipo 'sair' para encerrar.

📊 Pergunta: Qual o top 10 filmes com maior número de bilheteria?

🔍 Buscando dados...

💬 Resposta:
────────────────────────────────────────────────────────────────────────────────
Os 10 filmes com maior bilheteria são:
1. Avatar (2009) – US$ 2,923,706,026
2. Avatar: The Way of Water (2022) – US$ 2,320,250,281
[...]
────────────────────────────────────────────────────────────────────────────────

📈 Dados utilizados:
  • {'titulo': 'Avatar', 'receita_usd': 2923706026}
  [...]

🔨 Query utilizada:
   SELECT titulo, receita_usd FROM ... ORDER BY receita_usd DESC LIMIT 10

📊 Pergunta: sair

👋 Até logo!
```

## 🔄 Fluxo de Execução

1. **Usuário faz pergunta** via CLI interativa
2. **Agente recebe pergunta** com system prompt de análise de cinema
3. **Agente decide qual tool usar**:
   - Se precisa do schema → `get_schema()`
   - Se precisa de dados específicos → `query_db(sql)`
   - Se é uma busca por título → `find_movie(title)`
4. **DatabaseManager executa query** no SQLite (cinerocket.db)
5. **Agente processa resultado** e estrutura resposta em AnalysisResult
6. **CLI exibe resultado formatado** com resposta, dados e query utilizada

## 🚨 Troubleshooting

### Erro: "OPENROUTER_API_KEY não configurada"
- Verifique se o arquivo `.env` existe no diretório do projeto
- A chave já vem pré-configurada para uso com modelos gratuitos

### Erro: "Banco de dados não encontrado"
- Verifique se `cinerocket.db` existe no diretório raiz do projeto
- Tamanho esperado: ~555MB

### Rate limit do OpenRouter (erro 429)
- A API gratuita permite 20 requisições por minuto
- Aguarde ~1 minuto antes de fazer novas perguntas, ou
- Use uma chave com plano pago editando `.env` e `MODELO_LLM`

### Modelo LLM não reconhecido
- O padrão é `openrouter/free` que seleciona automaticamente modelos gratuitos disponíveis
- Para especificar um modelo, edite `MODELO_LLM` no `.env`

## 📝 Características Técnicas

- **Modelo LLM:** openrouter/free (seleção automática de modelo gratuito)
- **Framework:** PydanticAI com tool use
- **Provider API:** OpenRouter (com fallback para modelos gratuitos)
- **Python:** 3.12+
- **Database:** SQLite3 com 1.4M+ registros em 11 tabelas
- **Async:** CLI interativa com execução assíncrona

## 🔐 Configuração de Segurança

- ✅ O `.env` já vem configurado com uma chave de teste em conta secundária (sem pagamento)
- ℹ️ A chave é pública pois o projeto é educacional e não contém dados sensíveis
- 🔒 Para produção: crie uma chave paga e atualize o `.env`

## 📄 Licença

MIT © 2026 CineData Team

---

**Desenvolvido para RocketLab GenAI Challenge**
