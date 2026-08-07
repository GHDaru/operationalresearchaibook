"""Gera resultados.json — a procedência de TODO número citado no capítulo 07.

Roda em segundos, em CPU, sem licença paga:

    cd po-zero/etapa-01-formulacao && python experimento.py

O arquivo gerado é determinístico: rodar duas vezes produz bytes idênticos.
Não há aleatoriedade neste experimento, e por isso não há semente a declarar —
dizer isso é mais honesto do que gravar uma semente que não é usada.
"""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import pulp

from modelo import carregar, modelo_margem, modelo_receita, resolver

AQUI = Path(__file__).parent


def versoes() -> dict:
    """Sem isto, o número medido não é evidência (constituição, Princípio III)."""
    return {
        "python": platform.python_version(),
        "pulp": pulp.__version__,
        "solver": "HiGHS (via PuLP)",
        "sistema": platform.system(),
    }


def main() -> None:
    dados = carregar(AQUI / "instancias" / "moveis.json")

    prob_m, x_m = modelo_margem(dados)
    correto = resolver(prob_m, x_m, dados)

    prob_r, x_r = modelo_receita(dados)
    errado = resolver(prob_r, x_r, dados)

    # O custo do erro: quanto de margem se perde ao seguir o plano que
    # maximiza receita. É o número que abre o capítulo.
    perda = round(correto["margem_total_reais"] - errado["margem_total_reais"], 2)

    saida = {
        "instancia": "instancias/moveis.json",
        "versoes": versoes(),
        "determinismo": "sem aleatoriedade — nenhuma semente é usada",
        "modelo_correto_margem": correto,
        "modelo_errado_receita": errado,
        "custo_do_erro": {
            "margem_perdida_reais_por_mes": perda,
            "leitura": (
                "O modelo que maximiza receita é viável e ótimo — para a pergunta errada. "
                "Seguir o plano dele custa esta margem por mês."
            ),
        },
    }

    destino = AQUI / "resultados.json"
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"resultados.json gerado: {destino}")
    print(f"  correto (margem): {correto['plano']} -> R$ {correto['margem_total_reais']:.2f}")
    print(f"  errado (receita): {errado['plano']} -> margem R$ {errado['margem_total_reais']:.2f}")
    print(f"  custo do erro:    R$ {perda:.2f} por mês")
    return 0


if __name__ == "__main__":
    sys.exit(main())
