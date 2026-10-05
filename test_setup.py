#!/usr/bin/env python
"""Script de teste para validar a configuração do projeto."""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_config():
    """Testa se as variáveis de configuração estão corretas."""
    print("🧪 Testando configuração...")

    try:
        from cinedata.config import MODELO_LLM, DB_PATH, OPENROUTER_API_KEY

        print(f"✅ MODELO_LLM: {MODELO_LLM}")
        print(f"✅ DB_PATH: {DB_PATH}")
        print(f"✅ OPENROUTER_API_KEY: {'*' * 10}...{OPENROUTER_API_KEY[-4:] if OPENROUTER_API_KEY else 'NÃO CONFIGURADA'}")

        # Validar DB
        db_path = Path(DB_PATH)
        if not db_path.exists():
            print(f"❌ Banco de dados não encontrado: {DB_PATH}")
            return False

        print(f"✅ Banco de dados encontrado: {db_path.stat().st_size / (1024**2):.2f} MB")
        return True

    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return False


def test_database():
    """Testa a conexão com o banco de dados."""
    print("\n🧪 Testando conexão com banco de dados...")

    try:
        from cinedata.database import DatabaseManager
        from cinedata.config import DB_PATH

        db = DatabaseManager(DB_PATH)
        db.connect()

        # Testar query simples
        result = db.execute_query("SELECT COUNT(*) as total FROM dim_movies;")
        total_movies = result[0]["total"]

        print(f"✅ Conexão bem-sucedida!")
        print(f"✅ Total de filmes: {total_movies}")

        # Contar outras tabelas
        tables = ["dim_genres", "dim_people", "dim_companies", "fact_movies_performance"]
        for table in tables:
            result = db.execute_query(f"SELECT COUNT(*) as total FROM {table};")
            count = result[0]["total"]
            print(f"✅ {table}: {count} registros")

        db.close()
        return True

    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return False


def test_schema():
    """Testa a recuperação do schema."""
    print("\n🧪 Testando recuperação do schema...")

    try:
        from cinedata.database import DatabaseManager
        from cinedata.config import DB_PATH

        db = DatabaseManager(DB_PATH)
        db.connect()

        schema = db.get_schema()
        lines = len(schema.split("\n"))

        print(f"✅ Schema recuperado com sucesso!")
        print(f"✅ Total de linhas de documentação: {lines}")

        db.close()
        return True

    except Exception as e:
        print(f"❌ Erro ao recuperar schema: {e}")
        return False


def main():
    """Executa todos os testes."""
    print("=" * 80)
    print("🎬 CineData Analytics - Validação de Setup")
    print("=" * 80)

    all_passed = True

    all_passed &= test_config()
    all_passed &= test_database()
    all_passed &= test_schema()

    print("\n" + "=" * 80)
    if all_passed:
        print("✅ Todas as validações passaram!")
        print("   Você pode executar: uv run src/cinedata/cli.py")
    else:
        print("❌ Algumas validações falharam. Verifique os erros acima.")
    print("=" * 80)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
