"""Interface de linha de comando para o agente."""

import asyncio
import sys
from pathlib import Path

# Garantir que consegue importar do src/cinedata
sys.path.insert(0, str(Path(__file__).parent))

try:
    from .agent import analyze
except ImportError:
    from agent import analyze


async def main():
    """Loop principal da CLI."""
    print("\n" + "=" * 80)
    print("🎬 CineData Analytics")
    print("=" * 80)
    print("\nPergunte sobre filmes, atores, bilheteria, etc.")
    print("Tipo 'sair' para encerrar.\n")

    while True:
        try:
            prompt = input("📊 Pergunta: ").strip()

            if prompt.lower() in ["sair", "exit", "quit"]:
                print("\n👋 Até logo!\n")
                break

            if not prompt:
                continue

            print("\n🔍 Buscando dados...\n")

            result = await analyze(prompt)

            print("💬 Resposta:")
            print("-" * 80)
            print(result.answer)

            if result.data_points:
                print("\n📈 Dados utilizados:")
                for ponto in result.data_points:
                    print(f"  • {ponto}")

            if result.query_used:
                print(f"\n🔨 Query utilizada:")
                print(f"   {result.query_used}")

            print("-" * 80 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 Tchau!\n")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
