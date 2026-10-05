"""Ponto de entrada para executar o CLI."""

import asyncio
import sys
from pathlib import Path

# Adicionar parent directory ao path para imports relativos
sys.path.insert(0, str(Path(__file__).parent))

try:
    from .cli import main
except ImportError:
    from cli import main

if __name__ == "__main__":
    asyncio.run(main())
