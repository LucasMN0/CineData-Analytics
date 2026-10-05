"""Testes para o módulo database usando SQLite direto."""

import sqlite3
from pathlib import Path


def get_db_path():
    """Retorna o caminho do banco de dados."""
    return Path(__file__).parent.parent / "../../Projeto/cinerocket-db/cinerocket (1).db"


def test_database_connection():
    """Testa conexão com banco de dados."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM dim_movies;")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] > 0

    conn.close()
    print("✅ test_database_connection passou")


def test_database_tables():
    """Testa se todas as tabelas esperadas existem."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    expected_tables = {
        "dim_movies", "dim_genres", "dim_people", "dim_companies",
        "fact_movies_performance", "dim_reviews", "movie_reviews",
        "bridge_movie_genre", "bridge_movie_person", "bridge_movie_company"
    }

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = {row[0] for row in cursor.fetchall()}

    for table in expected_tables:
        assert table in existing_tables, f"Tabela {table} não encontrada"

    conn.close()
    print("✅ test_database_tables passou")


def test_database_query_with_params():
    """Testa query com parâmetros."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM dim_movies WHERE ano_lancamento = ?",
        (2020,)
    )
    result = cursor.fetchone()
    assert result is not None

    conn.close()
    print("✅ test_database_query_with_params passou")


if __name__ == "__main__":
    test_database_connection()
    test_database_tables()
    test_database_query_with_params()
    print("\n✅ Todos os testes passaram!")
