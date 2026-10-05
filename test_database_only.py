#!/usr/bin/env python
"""Teste simplificado: apenas validação do banco de dados."""

import sys
import sqlite3
from pathlib import Path

def test_database():
    """Testa conexão direta ao banco de dados."""
    db_path = Path(__file__).parent / "../../Projeto/cinerocket-db/cinerocket (1).db"

    print("=" * 80)
    print("🎬 CineData Analytics - Teste do Banco de Dados")
    print("=" * 80)
    print(f"\n📍 Caminho do banco: {db_path}")

    # Verificar se arquivo existe
    if not db_path.exists():
        print(f"❌ Arquivo não encontrado!")
        print(f"   Procurando em: {db_path.absolute()}")
        return False

    print(f"✅ Arquivo encontrado: {db_path.stat().st_size / (1024**2):.2f} MB")

    try:
        # Conectar ao banco
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        print("✅ Conexão bem-sucedida ao SQLite")

        # Listar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()

        print(f"\n📊 Tabelas encontradas ({len(tables)}):")
        for table in tables:
            name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {name}")
            count = cursor.fetchone()[0]
            print(f"   • {name:<30} {count:>10} registros")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False


if __name__ == "__main__":
    success = test_database()
    print("\n" + "=" * 80)
    if success:
        print("✅ Banco de dados está acessível!")
    else:
        print("❌ Falha ao acessar banco de dados")
    print("=" * 80)
    sys.exit(0 if success else 1)
