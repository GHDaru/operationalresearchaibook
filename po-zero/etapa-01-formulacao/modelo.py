"""Etapa 01 — Formulação: o modelo de mix de produção, e o modelo errado ao lado.

Duas formulações do MESMO problema, com a mesma região viável e objetivos
diferentes:

  modelo_margem(...)  — o correto: maximiza margem de contribuição.
  modelo_receita(...) — o erro de abertura do capítulo: maximiza receita.

Ter os dois lado a lado é o ponto pedagógico da etapa. O erro não é de
aritmética nem de solver: os dois modelos rodam, os dois devolvem "ótimo", e só
um responde à pergunta que a marcenaria fez.
"""

from __future__ import annotations

import json
from pathlib import Path

import pulp


def carregar(caminho: str | Path) -> dict:
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def _variaveis(dados: dict) -> dict[str, pulp.LpVariable]:
    """As variáveis de decisão: quantas unidades de cada produto fabricar no mês.

    Contínuas de propósito — um capítulo sobre formulação linear não introduz
    integralidade. O que isso custa está na seção "quando não serve".
    """
    return {
        nome: pulp.LpVariable(f"x_{nome}", lowBound=0, cat="Continuous")
        for nome in dados["produtos"]
    }


def _restricoes(prob: pulp.LpProblem, x: dict, dados: dict) -> None:
    """As restrições, com unidades coerentes dos dois lados.

    Recurso: (h/unid) x (unid/mês) = h/mês, contra h/mês disponíveis.
    Demanda: unid/mês contra unid/mês.
    """
    for recurso, disponivel in dados["recursos"].items():
        prob += (
            pulp.lpSum(dados["produtos"][p][recurso] * x[p] for p in x) <= disponivel,
            f"recurso_{recurso}",
        )
    for produto, teto in dados.get("demanda_maxima", {}).items():
        prob += (x[produto] <= teto, f"demanda_{produto}")


def modelo_margem(dados: dict) -> tuple[pulp.LpProblem, dict]:
    """O modelo correto: o que sobra por unidade, e não o que entra por unidade."""
    prob = pulp.LpProblem("mix_producao_margem", pulp.LpMaximize)
    x = _variaveis(dados)
    prob += pulp.lpSum(dados["produtos"][p]["margem_reais"] * x[p] for p in x), "margem_total"
    _restricoes(prob, x, dados)
    return prob, x


def modelo_receita(dados: dict) -> tuple[pulp.LpProblem, dict]:
    """O modelo ERRADO do capítulo: maximiza receita.

    Mesmas restrições, mesma região viável. Só o objetivo muda — e é o objetivo
    que decide o que a fábrica vai produzir.
    """
    prob = pulp.LpProblem("mix_producao_receita", pulp.LpMaximize)
    x = _variaveis(dados)
    prob += pulp.lpSum(dados["produtos"][p]["preco_reais"] * x[p] for p in x), "receita_total"
    _restricoes(prob, x, dados)
    return prob, x


def resolver(prob: pulp.LpProblem, x: dict, dados: dict) -> dict:
    """Resolve com HiGHS (aberto, sem licença) e devolve o que o capítulo cita."""
    prob.solve(pulp.HiGHS(msg=False))
    plano = {p: round(v.value(), 6) for p, v in x.items()}
    margem = sum(dados["produtos"][p]["margem_reais"] * q for p, q in plano.items())
    receita = sum(dados["produtos"][p]["preco_reais"] * q for p, q in plano.items())
    uso = {
        r: round(sum(dados["produtos"][p][r] * q for p, q in plano.items()), 6)
        for r in dados["recursos"]
    }
    return {
        "status": pulp.LpStatus[prob.status],
        "plano": plano,
        "margem_total_reais": round(margem, 2),
        "receita_total_reais": round(receita, 2),
        "uso_dos_recursos": uso,
        "folga_dos_recursos": {
            r: round(dados["recursos"][r] - uso[r], 6) for r in dados["recursos"]
        },
    }
