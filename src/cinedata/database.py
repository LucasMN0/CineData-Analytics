"""Gerenciador de banco de dados SQLite."""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any

try:
    from .config import DB_PATH
except ImportError:
    from config import DB_PATH


class DatabaseManager:
    """Gerencia conexões e queries ao banco CineRocket."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Abre conexão com o banco."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def execute_query(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Executa uma query SELECT e retorna resultados."""
        if self.conn is None:
            self.connect()

        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise Exception(f"Erro na query: {str(e)}")

    def get_schema(self) -> str:
        """Retorna documentação do schema do banco."""
        if self.conn is None:
            self.connect()

        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        doc = "# Schema do Banco CineRocket\n\n"

        for (table_name,) in tables:
            if table_name == "alembic_version":
                continue

            doc += f"## {table_name}\n"
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            doc += "| Campo | Tipo | PK |\n"
            doc += "|-------|------|----|\n"

            for col in columns:
                _, name, col_type, notnull, _, pk = col
                pk_mark = "✓" if pk else ""
                doc += f"| {name} | {col_type} | {pk_mark} |\n"

            doc += "\n"

        return doc

    def close(self):
        """Fecha a conexão."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Instância global do gerenciador
db_manager = DatabaseManager()
