"""Gera resultados.json — a procedência de todo número do capítulo 08.

Percorre as três etapas da narrativa do capítulo e, em cada uma, faz duas coisas:

  1. **enumera os vértices à mão** (`enumera.py`), como o leitor faz no papel;
  2. **confere com o HiGHS**, para provar que a enumeração não mentiu.

As duas concordarem é o ponto: o capítulo afirma que o ótimo está num vértice e,
neste caso pequeno, isso é verificável em vez de aceito.

    cd po-zero/etapa-02-metodo-grafico && python experimento.py
"""

from __future__ import annotations

import json
import platform
from pathlib import Path

import pulp

from enumera import Restricao, resolver

AQUI = Path(__file__).parent

LUCRO = (100.0, 150.0)          # Tipo 1, Tipo 2
CPU = Restricao(1, 1, 10, "CPUs: x1 + x2 <= 10")
MEM = Restricao(1, 2, 12, "pentes de 16 GB: x1 + 2x2 <= 12")


def por_solver(restricoes: list[Restricao]) -> dict:
    p = pulp.LpProblem("grafico", pulp.LpMaximize)
    x1 = pulp.LpVariable("x1", lowBound=0)
    x2 = pulp.LpVariable("x2", lowBound=0)
    p += LUCRO[0] * x1 + LUCRO[1] * x2
    for r in restricoes:
        p += r.a1 * x1 + r.a2 * x2 <= r.b
    st = pulp.LpStatus[p.solve(pulp.HiGHS(msg=False))]
    if st != "Optimal":
        return {"status": st}
    return {"status": st, "ponto": [round(x1.value(), 6), round(x2.value(), 6)],
            "lucro": round(pulp.value(p.objective), 6)}


def main() -> None:
    etapas = {}

    # Etapa 1 — nenhuma restrição além da não-negatividade.
    etapas["1_sem_restricao"] = {
        "descricao": "Só a não-negatividade. A região é infinita e o lucro não tem teto.",
        "solver": por_solver([]),
        "licao": "Sistema sem restrição não é sistema modelável. Toda restrição real vem depois desta constatação.",
    }

    # Etapa 2 — só a CPU.
    e2 = resolver([CPU], LUCRO)
    etapas["2_so_cpu"] = {
        "descricao": "10 CPUs, memória infinita.",
        "enumeracao": e2,
        "solver": por_solver([CPU]),
        "licao": "A intuição acerta (todo Tipo 2), mas não sabe provar. A prova é: são só três vértices, e um deles ganha.",
    }

    # Etapa 3 — CPU e memória.
    e3 = resolver([CPU, MEM], LUCRO)
    etapas["3_cpu_e_memoria"] = {
        "descricao": "10 CPUs e 12 pentes de 16 GB.",
        "enumeracao": e3,
        "solver": por_solver([CPU, MEM]),
        "licao": "O vértice ótimo da etapa 2 sai da região viável. Restrição nova nunca aumenta a região.",
    }

    # O ponto narrativo do capítulo: o ótimo anterior deixa de ser viável.
    otimo_anterior = tuple(e2["otimo"]["ponto"])
    ainda_viavel = MEM.satisfeita(otimo_anterior)
    etapas["3_cpu_e_memoria"]["o_que_aconteceu_com_o_otimo_anterior"] = {
        "ponto": list(otimo_anterior),
        "continua_viavel": ainda_viavel,
        "violou": None if ainda_viavel else MEM.rotulo,
        "quanto_faltou_de_pente": round(MEM.a1 * otimo_anterior[0] + MEM.a2 * otimo_anterior[1] - MEM.b, 6),
    }

    # A reta de iso-lucro no ótimo, e a direção de crescimento.
    otimo = e3["otimo"]
    etapas["3_cpu_e_memoria"]["iso_lucro_no_otimo"] = {
        "equacao": f"{LUCRO[0]:.0f}*x1 + {LUCRO[1]:.0f}*x2 = {otimo['lucro']:.0f}",
        "gradiente": list(LUCRO),
        "observacao": "O gradiente é perpendicular à reta de iso-lucro e aponta para onde o lucro cresce.",
    }

    # As duas heurísticas gulosas do capítulo anterior, agora vistas na geometria.
    etapas["3_cpu_e_memoria"]["heuristicas_gulosas"] = {
        "por_cpu": {"escolhe": "Tipo 2", "razao": [LUCRO[0] / 1, LUCRO[1] / 1], "plano": [0, 6], "lucro": 900.0},
        "por_pente": {"escolhe": "Tipo 1", "razao": [LUCRO[0] / 1, LUCRO[1] / 2], "plano": [10, 0], "lucro": 1000.0},
        "observacao": "As duas apontam para vértices diferentes, e nenhum dos dois é o ótimo.",
    }

    saida = {
        "instancia": "montagem de computadores (MRP inverso) — a mesma da etapa 01",
        "versoes": {"python": platform.python_version(), "pulp": pulp.__version__,
                    "solver": "HiGHS (via PuLP)", "sistema": platform.system()},
        "determinismo": "sem aleatoriedade — nenhuma semente é usada",
        "lucro_unitario": {"tipo1": LUCRO[0], "tipo2": LUCRO[1]},
        "etapas": etapas,
    }
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("resultados.json gerado")
    for nome, et in etapas.items():
        print(f"\n{nome}: {et['descricao']}")
        if "enumeracao" in et:
            for c in et["enumeracao"]["candidatos"]:
                marca = "✓" if c["viavel"] else "✗"
                extra = f"lucro R$ {c['lucro']:.0f}" if c["viavel"] else f"violou {', '.join(c['violou'])}"
                print(f"   {marca} ({c['ponto'][0]:g}, {c['ponto'][1]:g})  de [{' ∩ '.join(c['das_restricoes'])}]  {extra}")
            o = et["enumeracao"]["otimo"]
            print(f"   → ótimo por enumeração: ({o['ponto'][0]:g}, {o['ponto'][1]:g}) com R$ {o['lucro']:.0f}")
        print(f"   → solver: {et['solver']}")


if __name__ == "__main__":
    main()
