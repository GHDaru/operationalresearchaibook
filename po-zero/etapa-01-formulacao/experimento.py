"""Gera resultados.json — a procedência de todo número do capítulo 07.

Percorre a narrativa em três etapas do capítulo e, na última, refuta com número
as duas regras de bolso que o aluno naturalmente inventa.

    cd po-zero/etapa-01-formulacao && python experimento.py
"""

from __future__ import annotations

import json
import platform
from pathlib import Path

import pulp

from modelo import avaliar, carregar, montar, regra_gulosa, resolver

AQUI = Path(__file__).parent


def etapa(dados: dict, ativos: list[str]) -> dict:
    prob, x = montar(dados, ativos)
    return resolver(prob, x, dados)


def main() -> None:
    dados = carregar(AQUI / "instancias" / "montadora.json")

    e1 = etapa(dados, [])
    e2 = etapa(dados, ["cpu"])
    e3 = etapa(dados, ["cpu", "pente16"])

    # O ótimo da etapa 2 ainda vale quando a memória entra?
    plano_e2 = e2["plano"]
    e2_sob_e3 = avaliar(plano_e2, dados)

    gulosas = {
        "por_cpu": regra_gulosa(dados, "cpu"),
        "por_pente16": regra_gulosa(dados, "pente16"),
    }

    saida = {
        "instancia": "instancias/montadora.json",
        "versoes": {"python": platform.python_version(), "pulp": pulp.__version__,
                    "solver": "HiGHS (via PuLP)", "sistema": platform.system()},
        "determinismo": "sem aleatoriedade — nenhuma semente é usada",
        "etapa_1_sem_restricao": {
            "descricao": "Nenhum componente limita.",
            "resultado": e1,
            "licao": "Ilimitado. Um sistema sem restrição não é modelável — e a restrição não é burocracia do método, é o que torna a pergunta respondível.",
        },
        "etapa_2_so_cpu": {
            "descricao": "10 CPUs, memória infinita.",
            "resultado": e2,
            "licao": "A intuição acerta: só o produto que paga mais, porque cada máquina custa exatamente uma CPU. Mas ela não sabe provar.",
        },
        "etapa_3_cpu_e_memoria": {
            "descricao": "10 CPUs e 12 pentes de 16 GB.",
            "resultado": e3,
            "o_que_aconteceu_com_o_otimo_da_etapa_2": e2_sob_e3,
            "licao": "O ótimo anterior deixa de ser viável, e o novo ótimo é uma MISTURA — que nenhuma regra de bolso encontra.",
        },
        "regras_de_bolso_refutadas": {
            **gulosas,
            "observacao": "As duas apontam para produtos diferentes, e nenhuma das duas chega ao ótimo.",
            "quanto_cada_uma_perde_por_mes": {
                k: round(e3["lucro_total_reais"] - g["lucro_total_reais"], 2) for k, g in gulosas.items()
            },
        },
    }

    (AQUI / "resultados.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("resultados.json gerado\n")
    print(f"  etapa 1 (sem restrição) : {e1['status']}")
    print(f"  etapa 2 (só CPU)        : {e2['plano']} -> R$ {e2['lucro_total_reais']:.0f}")
    print(f"  etapa 3 (CPU + memória) : {e3['plano']} -> R$ {e3['lucro_total_reais']:.0f}")
    print(f"    o ótimo da etapa 2 ainda é viável? {e2_sob_e3['viavel']}"
          f"  (folga de pentes: {e2_sob_e3['folga_dos_componentes']['pente16']:g})")
    print("\n  regras de bolso:")
    for k, g in gulosas.items():
        print(f"    {k:12s} escolhe {g['escolheu']:6s} -> {g['plano']} = R$ {g['lucro_total_reais']:.0f}"
              f"  (perde R$ {e3['lucro_total_reais'] - g['lucro_total_reais']:.0f})")


if __name__ == "__main__":
    main()
