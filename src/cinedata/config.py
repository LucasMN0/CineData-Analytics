"""Configuração da aplicação."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretórios
PROJECT_DIR = Path(__file__).parent.parent.parent
DB_PATH = os.getenv("DB_PATH", str(PROJECT_DIR / "cinerocket.db"))

# Modelo LLM - Remove prefixo openrouter: se presente
_modelo_raw = os.getenv("MODELO_LLM", "openrouter:openrouter/free")
MODELO_LLM = _modelo_raw.split(":")[-1] if ":" in _modelo_raw else _modelo_raw

# API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY não está configurada no .env")

# Validar banco
if not Path(DB_PATH).exists():
    raise FileNotFoundError(f"Banco de dados não encontrado: {DB_PATH}")

print(f"✓ Config carregada - Modelo: {MODELO_LLM}")
