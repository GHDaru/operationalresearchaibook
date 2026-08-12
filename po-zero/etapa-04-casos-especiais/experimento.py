"""Gera resultados.json — a procedência de todo número do capítulo 10.

Cinco casos, e o quinto é o que dá sentido aos outros quatro:

  1. **Vértice degenerado** — a montadora com um contrato que limita o total
     montado a 10, coincidindo com o limite de CPUs. O empate no teste da razão
     aparece, e o quadro final tem uma básica valendo zero.
  2. **Mais de um plano ótimo** — a mesma montadora com lucro (100, 200), que
     deixa o objetivo paralelo à restrição de memória.
  3. **Sem teto** — a montadora sem restrição de recurso: o caso do capítulo 07.
  4. **Sem plano** — a montadora com um compromisso impossível: o do capítulo 09.
  5. **O giro** — a instância clássica de ciclagem, resolvida **duas vezes**:
     com a regra que o capítulo 09 ensina e com a de Bland.

O quinto caso é um **experimento controlado**: o modelo é o mesmo, muda só a
regra de pivoteamento. O que sobrevive à troca é do modelo; o que some era do
método. É a tese do capítulo, e ela é medida aqui.

    cd po-zero/etapa-04-casos-especiais && python experimento.py
"""

from __future__ import annotations

import json
import platform
from fractions import Fraction as F
from pathlib import Path

import pulp

from vereditos import Restricao, analisar

AQUI = Path(__file__).parent

# A montadora dos capítulos 07 a 09: 10 CPUs, 12 pentes, lucros 100 e 150.
CPU = lambda: Restricao([F(1), F(1)], "<=", F(10), "CPUs: x1 + x2 <= 10")
MEM = lambda: Restricao([F(1), F(2)], "<=", F(12), "pentes: x1 + 2x2 <= 12")

# A instância clássica de ciclagem. Sobre a atribuição, ver ADR 0008: os
# primeiros exemplos são creditados a Hoffman e a Wolfe (fonte de 1955, lida);
# a instância que o ensino faz circular é atribuída a Beale (1955), e este
# handbook NÃO afirma que a forma primal abaixo apareça literalmente ali.
CICLO_LUCROS = [F(3, 4), F(-150), F(1, 50), F(-6)]
def CICLO_RESTRICOES():
    return [
        Restricao([F(1, 4), F(-60), F(-1, 25), F(9)], "<=", F(0), "face 1"),
        Restricao([F(1, 2), F(-90), F(-1, 50), F(3)], "<=", F(0), "face 2"),
        Restricao([F(0), F(0), F(1), F(0)], "<=", F(1), "x3 <= 1"),
    ]


def por_solver(lucros, restricoes) -> dict:
    p = pulp.LpProblem("caso", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(len(lucros))]
    p += pulp.lpSum(float(c) * v for c, v in zip(lucros, x))
    for r in restricoes:
        e = pulp.lpSum(float(a) * v for a, v in zip(r.coefs, x))
        p += (e <= float(r.b)) if r.sinal == "<=" else (e >= float(r.b)) if r.sinal == ">=" else (e == float(r.b))
    st = pulp.LpStatus[p.solve(pulp.HiGHS(msg=False))]
    if st != "Optimal":
        return {"status": st}
    return {"status": st, "ponto": [round(v.value(), 6) for v in x], "valor": round(pulp.value(p.objective), 6)}


def main() -> None:
    casos = {}

    casos["1_vertice_degenerado"] = analisar(
        "vertice_degenerado",
        "Montadora com um contrato que limita o total montado a 10 — exatamente o que as CPUs já "
        "limitavam. A restrição é redundante e passa pelo vértice ótimo.",
        [100, 150],
        [CPU(), MEM(), Restricao([F(1), F(1)], "<=", F(10), "contrato: x1 + x2 <= 10")],
    )

    casos["2_multiplos_otimos"] = analisar(
        "multiplos_otimos",
        "A mesma montadora com lucro (100, 200): o objetivo fica paralelo à restrição de memória, "
        "e o último contato da reta de iso-lucro é um lado inteiro, não um ponto.",
        [100, 200],
        [CPU(), MEM()],
    )
    # Os dois extremos do segmento ótimo, avaliados à mão para o capítulo poder
    # dizer que rendem o mesmo. É conta de uma linha; não precisa de solver.
    casos["2_multiplos_otimos"]["extremos_do_segmento"] = [
        {"ponto": [0, 6], "valor": 100 * 0 + 200 * 6},
        {"ponto": [8, 2], "valor": 100 * 8 + 200 * 2},
    ]

    casos["3_sem_teto"] = analisar(
        "sem_teto",
        "A montadora sem nenhuma restrição de recurso — o primeiro estágio do capítulo 07. "
        "Nenhuma razão positiva no teste da razão: dá para andar para sempre.",
        [100, 150],
        [],
    )

    casos["4_sem_plano"] = analisar(
        "sem_plano",
        "A montadora com 8 unidades do Tipo 2 já vendidas: exigiriam 16 pentes e só há 12. "
        "A variável artificial sobra na base com valor positivo.",
        [100, 150],
        [CPU(), MEM(), Restricao([F(0), F(1)], ">=", F(8), "compromisso: x2 >= 8")],
    )

    # O experimento controlado: mesmo modelo, duas regras.
    casos["5_giro_dantzig"] = analisar(
        "giro_dantzig",
        "A instância clássica de ciclagem, com a regra que o capítulo 09 ensina (custo reduzido "
        "mais negativo; desempate da saída pela linha de menor índice).",
        CICLO_LUCROS, CICLO_RESTRICOES(), regra="dantzig", limite=40,
    )
    casos["5_giro_bland"] = analisar(
        "giro_bland",
        "A MESMA instância, mudando só a regra de pivoteamento: Bland — menor índice na entrada "
        "e, entre as de menor razão, a variável básica de menor índice.",
        CICLO_LUCROS, CICLO_RESTRICOES(), regra="bland", limite=40,
    )

    # "Bland é mais lenta" é afirmação sobre desempenho, e afirmação sobre
    # desempenho exige medição (Princípio III). Aqui ela é medida: as mesmas
    # instâncias, as duas regras, contando pivôs.
    custo_da_garantia = []
    for rot, lucros, rest in [
        ("montadora", [100, 150], [CPU(), MEM()]),
        ("vertice_degenerado", [100, 150], [CPU(), MEM(), Restricao([F(1), F(1)], "<=", F(10), "contrato")]),
        ("multiplos_otimos", [100, 200], [CPU(), MEM()]),
        ("sem_plano", [100, 150], [CPU(), MEM(), Restricao([F(0), F(1)], ">=", F(8), "compromisso")]),
    ]:
        d = analisar(rot, "", lucros, rest, regra="dantzig")
        b = analisar(rot, "", lucros, rest, regra="bland")
        com_solucao = d["status"] == "otimo" and b["status"] == "otimo"
        custo_da_garantia.append({
            "instancia": rot,
            "pivos_dantzig": d["pivos"],
            "pivos_bland": b["pivos"],
            "mesmo_veredito": d["status"] == b["status"],
            # `None == None` é verdade vazia: sem solução, não há valor nem ponto
            # a comparar, e dizer "sim" na tabela publicada seria enganoso.
            "mesmo_valor": (d["valor"] == b["valor"]) if com_solucao else None,
            # A pergunta que faltava, e cuja ausência deixou a prosa afirmar
            # "Bland nunca muda a resposta" — o que é FALSO quando há mais de um
            # plano ótimo. Apontado pela revisão independente da rodada 006.
            "mesmo_ponto": (d["ponto"] == b["ponto"]) if com_solucao else None,
        })

    # O solver de mercado como testemunha independente nos casos com resposta.
    conferencia = {
        "1_vertice_degenerado": por_solver([100, 150], [CPU(), MEM(), Restricao([F(1), F(1)], "<=", F(10), "")]),
        "2_multiplos_otimos": por_solver([100, 200], [CPU(), MEM()]),
        "3_sem_teto": por_solver([100, 150], []),
        "4_sem_plano": por_solver([100, 150], [CPU(), MEM(), Restricao([F(0), F(1)], ">=", F(8), "")]),
        "5_giro": por_solver(CICLO_LUCROS, CICLO_RESTRICOES()),
    }

    resultados = {
        "casos": casos,
        "conferencia_com_solver": conferencia,
        "custo_da_garantia": {
            "descricao": "Pivôs sob as duas regras nas instâncias que NÃO ciclam. Mede o preço de trocar Dantzig por Bland.",
            "medicoes": custo_da_garantia,
        },
        "tese_do_capitulo": {
            "enunciado": "O que é do modelo sobrevive à troca do método; o que some quando se troca o método era do método.",
            "evidencia": {
                "mesma_instancia_duas_regras": "5_giro_dantzig vs 5_giro_bland",
                "ciclo_com_dantzig": bool(casos["5_giro_dantzig"]["ciclo"]),
                "ciclo_com_bland": bool(casos["5_giro_bland"]["ciclo"]),
                "empates_persistem_no_modelo_degenerado": len(casos["1_vertice_degenerado"]["empates_no_teste_da_razao"]) > 0,
            },
        },
        "ambiente": {
            "python": platform.python_version(),
            "pulp": pulp.__version__,
            "solver": "HiGHS (via highspy)",
            "aritmetica": "exata (fractions.Fraction)",
            "determinismo": "sem aleatoriedade: nenhuma semente a declarar",
        },
    }

    (AQUI / "resultados.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    for m in custo_da_garantia:
        print(f"custo da garantia · {m['instancia']:20s} dantzig={m['pivos_dantzig']} bland={m['pivos_bland']} veredito={m['mesmo_veredito']} valor={m['mesmo_valor']} ponto={m['mesmo_ponto']}")
    for nome, c in casos.items():
        extra = ""
        if c["ciclo"]:
            extra = f" · CICLO período {c['ciclo']['periodo']} (base {c['ciclo']['base_repetida']} repetiu na iteração {c['ciclo']['repetiu_em']})"
        elif c["vertice"]["degenerado"]:
            extra = f" · vértice DEGENERADO (básicas em zero: {c['vertice']['basicas_em_zero']})"
        if c["otimo"] and c["otimo"]["multiplos_otimos"]:
            extra += f" · MAIS DE UM ÓTIMO (custo reduzido zero em {c['otimo']['colunas_com_custo_reduzido_zero']})"
        print(f"{nome:24s} [{c['regra']:7s}] {c['status']:20s} pivôs={c['pivos']:3d} ponto={c['ponto']}{extra}")


if __name__ == "__main__":
    main()
