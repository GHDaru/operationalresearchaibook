"""Etapa 01 — Formulação: do estoque para o modelo (MRP inverso).

O modelo NÃO é escrito à mão: ele é **montado a partir da lista de materiais**.
Isso é decisão pedagógica. O planejamento de necessidades de materiais (MRP)
clássico anda para a frente — da demanda para o componente. Aqui andamos para
trás: do componente que existe para o que dá para montar. A estrutura do modelo
é a mesma nos dois sentidos, e é a lista de materiais que a fornece.

Consequência prática: acrescentar um terceiro produto ou um terceiro componente
é editar o JSON, não o código. É assim que se percebe que a formulação tem
FORMA, e que a forma é o que o método explora.
"""

from __future__ import annotations

import json
from pathlib import Path

import pulp


def carregar(caminho: str | Path) -> dict:
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def montar(dados: dict, componentes_ativos: list[str] | None = None) -> tuple[pulp.LpProblem, dict]:
    """Monta o modelo a partir da lista de materiais.

    `componentes_ativos` é o que permite a narrativa em três etapas do capítulo:
    com `[]` nenhum componente limita (o modelo é ilimitado), com `["cpu"]` só a
    CPU limita, e com os dois o problema fica como na vida real.
    """
    ativos = list(dados["componentes"]) if componentes_ativos is None else componentes_ativos

    prob = pulp.LpProblem("mrp_inverso", pulp.LpMaximize)
    x = {p: pulp.LpVariable(f"x_{p}", lowBound=0, cat="Continuous") for p in dados["produtos"]}

    # Objetivo: lucro total. Uma medida só.
    prob += pulp.lpSum(dados["produtos"][p]["lucro_reais"] * x[p] for p in x), "lucro_total"

    # Uma restrição por componente em estoque. O coeficiente vem da lista de
    # materiais: quantas unidades daquele componente cada produto consome.
    for c in ativos:
        prob += (
            pulp.lpSum(dados["produtos"][p]["lista_de_materiais"].get(c, 0) * x[p] for p in x)
            <= dados["componentes"][c]["estoque"],
            f"estoque_{c}",
        )
    return prob, x


def resolver(prob: pulp.LpProblem, x: dict, dados: dict) -> dict:
    status = pulp.LpStatus[prob.solve(pulp.HiGHS(msg=False))]
    if status != "Optimal":
        # Ilimitado é RESULTADO, não erro. A etapa 1 do capítulo depende disso.
        return {"status": status, "plano": None, "lucro_total_reais": None}
    plano = {p: round(v.value(), 6) for p, v in x.items()}
    return {
        "status": status,
        "plano": plano,
        "lucro_total_reais": round(sum(dados["produtos"][p]["lucro_reais"] * q for p, q in plano.items()), 2),
        "uso_dos_componentes": {
            c: round(sum(dados["produtos"][p]["lista_de_materiais"].get(c, 0) * q for p, q in plano.items()), 6)
            for c in dados["componentes"]
        },
        "folga_dos_componentes": {
            c: round(dados["componentes"][c]["estoque"]
                     - sum(dados["produtos"][p]["lista_de_materiais"].get(c, 0) * q for p, q in plano.items()), 6)
            for c in dados["componentes"]
        },
    }


def avaliar(plano: dict, dados: dict) -> dict:
    """Avalia um plano QUALQUER — inclusive um que veio de regra de bolso."""
    lucro = sum(dados["produtos"][p]["lucro_reais"] * q for p, q in plano.items())
    uso = {c: sum(dados["produtos"][p]["lista_de_materiais"].get(c, 0) * q for p, q in plano.items())
           for c in dados["componentes"]}
    viavel = all(uso[c] <= dados["componentes"][c]["estoque"] + 1e-9 for c in uso)
    return {"plano": plano, "lucro_total_reais": round(lucro, 2), "viavel": viavel,
            "folga_dos_componentes": {c: round(dados["componentes"][c]["estoque"] - uso[c], 6) for c in uso}}


def regra_gulosa(dados: dict, por_componente: str) -> dict:
    """A heurística que o aluno inventa: 'faça o que paga mais por unidade de X'.

    Devolve o produto escolhido e o plano que ela produz — gastar o componente
    todo naquele produto. Existe para ser REFUTADA com número, e não no discurso.
    """
    razao = {
        p: dados["produtos"][p]["lucro_reais"] / dados["produtos"][p]["lista_de_materiais"][por_componente]
        for p in dados["produtos"]
    }
    escolhido = max(razao, key=razao.get)
    # Gasta o componente inteiro no escolhido, respeitando os demais componentes.
    limite = min(
        dados["componentes"][c]["estoque"] / dados["produtos"][escolhido]["lista_de_materiais"][c]
        for c in dados["componentes"]
        if dados["produtos"][escolhido]["lista_de_materiais"].get(c, 0) > 0
    )
    plano = {p: (limite if p == escolhido else 0.0) for p in dados["produtos"]}
    return {"criterio": f"lucro por {por_componente}", "razao": {p: round(r, 2) for p, r in razao.items()},
            "escolheu": escolhido, **avaliar(plano, dados)}
