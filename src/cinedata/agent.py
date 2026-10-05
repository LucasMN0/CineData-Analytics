"""Agente de análise de filmes com PydanticAI."""

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic import BaseModel
from typing import Optional

try:
    from .config import MODELO_LLM
    from .database import db_manager
except ImportError:
    from config import MODELO_LLM
    from database import db_manager


class AnalysisResult(BaseModel):
    """Resposta do agente."""
    answer: str
    data_points: Optional[list] = None
    query_used: Optional[str] = None


# Setup do modelo
# OpenRouterModel obtém API key de OPENROUTER_API_KEY (variável de ambiente)
model = OpenRouterModel(MODELO_LLM)

# Agente principal
system_prompt = """Você é um analista de dados especializado em cinema.

Seu trabalho é responder perguntas sobre filmes, atores, produtoras e bilheteria.

Quando receber uma pergunta:
1. Entenda o que está sendo pedido
2. Crie uma query SQL para buscar os dados
3. Execute a query usando as ferramentas
4. Estruture a resposta com números e explicações claras"""

agent = Agent(
    model=model,
    output_type=AnalysisResult,
    system_prompt=system_prompt,
    retries=3,
)


@agent.tool
def query_db(ctx: RunContext, sql: str) -> str:
    """Executa uma query SQL no banco CineRocket."""
    try:
        results = db_manager.execute_query(sql)

        if not results:
            return "Nenhum resultado encontrado."

        # Retorna até 10 resultados
        output = "\n".join([str(row) for row in results[:10]])
        if len(results) > 10:
            output += f"\n... e mais {len(results) - 10} registros"

        return output
    except Exception as e:
        return f"Erro na query: {e}"


@agent.tool
def get_schema(ctx: RunContext) -> str:
    """Retorna as tabelas disponíveis no banco."""
    tables = [
        "dim_movies (sk_movie_id, titulo, ano_lancamento, duracao, etc)",
        "dim_genres (sk_genre_id, nome)",
        "dim_people (sk_people_id, nome, profissao)",
        "dim_companies (sk_company_id, nome)",
        "fact_movies_performance (sk_fact_id, sk_movie_id, receita_total, etc)",
        "dim_reviews (sk_review_id, rating, texto)",
        "movie_reviews (sk_movie_id, sk_review_id)",
        "bridge_movie_genre, bridge_movie_person, bridge_movie_company (relacionamentos)"
    ]
    return "Tabelas disponíveis:\n" + "\n".join(f"- {t}" for t in tables)


@agent.tool
def find_movie(ctx: RunContext, title: str) -> str:
    """Busca filmes por título (útil para encontrar IDs)."""
    sql = f"""
    SELECT sk_movie_id, titulo, ano_lancamento
    FROM dim_movies
    WHERE titulo LIKE '%{title}%'
    LIMIT 5
    """
    return query_db(ctx, sql)


async def analyze(question: str) -> AnalysisResult:
    """Processa pergunta e retorna análise com dados."""
    result = await agent.run(question)
    return result.output
