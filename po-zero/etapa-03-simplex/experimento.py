"""Gera resultados.json — a procedência de todo número do capítulo 09.

Faz quatro coisas, nesta ordem:

  1. **Mede a explosão combinatória** que justifica o Simplex existir. O número
     de bases de um modelo em forma padrão é C(n+m, m); a tabela mostra onde a
     força bruta morre. É contagem, não estimativa.
  2. **Roda o Simplex de quadro na montadora** — a mesma instância dos
     capítulos 07 e 08 — e guarda a sequência de vértices visitados.
  3. **Roda o Simplex de quadro na montadora com compromisso** (x2 >= 5), em
     que a origem não é viável e o *big-M* precisa entrar.
  4. **Confere as duas contra o HiGHS.** Concordarem é o ponto: o capítulo
     afirma que o quadro chega ao mesmo lugar do desenho, e aqui isso é
     verificado, não prometido.

Executa em CPU, com solver aberto:

    cd po-zero/etapa-03-simplex && python experimento.py
"""

from __future__ import annotations

import json
import platform
from fractions import Fraction as F
from math import comb
from pathlib import Path

import pulp

from quadro import Restricao, imprimir, resolver

AQUI = Path(__file__).parent
INSTANCIA = AQUI.parent / "etapa-01-formulacao" / "instancias" / "montadora.json"

# O compromisso não está na instância original: ele é a variação que este
# capítulo introduz para que a origem deixe de ser viável. Fica declarado aqui,
# no experimento, e não escondido no texto.
COMPROMISSO = 5


def do_arquivo() -> tuple[list[F], list[Restricao], dict]:
    """Lê a montadora do capítulo 07 — a instância não é redigitada aqui."""
    dados = json.loads(INSTANCIA.read_text(encoding="utf-8"))
    produtos = list(dados["produtos"])
    componentes = list(dados["componentes"])
    lucros = [F(dados["produtos"][p]["lucro_reais"]) for p in produtos]
    restricoes = [
        Restricao(
            [F(dados["produtos"][p]["lista_de_materiais"].get(c, 0)) for p in produtos],
            "<=",
            F(dados["componentes"][c]["estoque"]),
            dados["componentes"][c]["rotulo"],
        )
        for c in componentes
    ]
    return lucros, restricoes, dados


def por_solver(lucros: list[F], restricoes: list[Restricao]) -> dict:
    p = pulp.LpProblem("simplex", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(len(lucros))]
    p += pulp.lpSum(float(c) * v for c, v in zip(lucros, x))
    for r in restricoes:
        e = pulp.lpSum(float(a) * v for a, v in zip(r.coefs, x))
        p += (e <= float(r.b)) if r.sinal == "<=" else (e >= float(r.b)) if r.sinal == ">=" else (e == float(r.b))
    st = pulp.LpStatus[p.solve(pulp.HiGHS(msg=False))]
    if st != "Optimal":
        return {"status": st}
    return {
        "status": st,
        "ponto": [round(v.value(), 6) for v in x],
        "valor": round(pulp.value(p.objective), 6),
    }


def caso(nome: str, descricao: str, lucros: list[F], restricoes: list[Restricao]) -> dict:
    r = resolver(lucros, restricoes)
    solver = por_solver(lucros, restricoes)
    # Concordar não é só chegar ao mesmo ponto: é dar o mesmo veredito. Um caso
    # sem solução tem de ser reconhecido como tal pelos dois lados.
    EQUIVALENTE = {"otimo": "Optimal", "inviavel": "Infeasible", "ilimitado": "Unbounded"}
    concordam = EQUIVALENTE.get(r["status"]) == solver.get("status")
    if concordam and r["status"] == "otimo":
        concordam = r["ponto_float"] == solver["ponto"] and r["valor_float"] == solver["valor"]
    return {
        "descricao": descricao,
        "modelo": [
            {"coeficientes": [str(c) for c in x.coefs], "sinal": x.sinal, "b": str(x.b), "rotulo": x.rotulo}
            for x in restricoes
        ],
        "quadro": {
            "status": r["status"],
            "pivos": r["pivos"],
            "colunas": r["colunas"],
            "artificiais": r["artificiais"],
            "vertices_visitados": r["vertices"],
            "ponto": r["ponto"],
            "valor": r["valor"],
            "quadros": [imprimir(it) for it in r["iteracoes"]],
            "decisoes": [
                {"iteracao": it.numero, "base": it.base, "entra": it.entra, "sai": it.sai, "razoes": it.razoes}
                for it in r["iteracoes"]
            ],
        },
        "solver": solver,
        "concordam": concordam,
    }


def klee_minty(n: int) -> tuple[list[F], list[Restricao]]:
    """O cubo de Klee–Minty: o pior caso do Simplex, construído em vez de citado.

    É um cubo levemente entortado, com 2^n vértices. Com a regra de Dantzig — a
    que este capítulo ensina — o algoritmo passa por **todos** eles antes de
    parar. O capítulo afirma que o Simplex tem pior caso exponencial; aqui essa
    afirmação é medida, e não emprestada de uma fonte que este ambiente não
    consegue abrir.
    """
    lucros = [F(10) ** (n - j) for j in range(1, n + 1)]
    restricoes = []
    for i in range(1, n + 1):
        coefs = [F(2) * F(10) ** (i - j) for j in range(1, i)] + [F(1)] + [F(0)] * (n - i)
        restricoes.append(Restricao(coefs, "<=", F(100) ** (i - 1), f"cubo, face {i}"))
    return lucros, restricoes


def main() -> None:
    lucros, restricoes, dados = do_arquivo()

    # 1. Por que não dá para enumerar: o número de bases é C(n+m, m).
    combinatoria = [
        {"variaveis": n, "restricoes": m, "bases": comb(n + m, m)}
        for n, m in [(2, 2), (5, 5), (10, 10), (20, 20), (50, 50)]
    ]

    casos = {
        "montadora": caso(
            "montadora",
            "A instância dos capítulos 07 e 08: 10 CPUs e 12 pentes de 16 GB. Origem viável, base de folgas serve.",
            lucros,
            restricoes,
        ),
        "montadora_com_compromisso": caso(
            "montadora_com_compromisso",
            f"A mesma montadora com {COMPROMISSO} unidades do Tipo 2 já vendidas: x2 >= {COMPROMISSO}. A origem deixa de ser viável e o big-M precisa entrar.",
            lucros,
            restricoes + [Restricao([F(0), F(1)], ">=", F(COMPROMISSO), f"compromisso: x2 >= {COMPROMISSO}")],
        ),
        "compromisso_impossivel": caso(
            "compromisso_impossivel",
            "O mesmo compromisso, mas de 8 unidades: 8 do Tipo 2 exigiriam 16 pentes e só há 12. Não existe plano.",
            lucros,
            restricoes + [Restricao([F(0), F(1)], ">=", F(8), "compromisso: x2 >= 8")],
        ),
    }

    # O quadro final da montadora carrega, na linha z sob as folgas, o valor de
    # uma unidade a mais de cada recurso. O capítulo 12 vai chamar isso de
    # preço-sombra; aqui o número é só registrado, e conferido por reexecução.
    def com_estoque_extra(indice: int) -> float:
        extra = [Restricao(list(r.coefs), r.sinal, r.b + (1 if i == indice else 0), r.rotulo)
                 for i, r in enumerate(restricoes)]
        return por_solver(lucros, extra)["valor"]

    base_valor = casos["montadora"]["solver"]["valor"]
    ganho_por_unidade = [
        {"recurso": r.rotulo, "valor_de_uma_unidade_a_mais": round(com_estoque_extra(i) - base_valor, 6)}
        for i, r in enumerate(restricoes)
    ]

    # O pior caso, medido. Cada linha é uma execução de verdade.
    pior_caso = []
    for n in range(2, 8):
        lk, rk = klee_minty(n)
        r = resolver(lk, rk, limite=5000)
        pior_caso.append({
            "n": n,
            "vertices_do_cubo": 2 ** n,
            "pivos": r["pivos"],
            "confere_com_2n_menos_1": r["pivos"] == 2 ** n - 1,
            "status": r["status"],
        })

    resultados = {
        "instancia": {"arquivo": str(INSTANCIA.relative_to(AQUI.parent.parent)), "ficha": dados["ficha"]["nome"]},
        "combinatoria": combinatoria,
        "pior_caso_klee_minty": {
            "descricao": "Cubo de Klee–Minty com a regra de Dantzig (a que o capítulo ensina). O algoritmo visita todos os 2^n vértices.",
            "medicoes": pior_caso,
        },
        "casos": casos,
        "ganho_por_unidade_extra": ganho_por_unidade,
        "ambiente": {
            "python": platform.python_version(),
            "pulp": pulp.__version__,
            "solver": "HiGHS (via highspy)",
            "aritmetica_do_quadro": "exata (fractions.Fraction); big-M simbólico",
            "determinismo": "sem aleatoriedade: nenhuma semente a declarar",
        },
    }
    (AQUI / "resultados.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    for nome, c in casos.items():
        q = c["quadro"]
        print(f"{nome}: {q['status']} · {q['pivos']} pivô(s) · ponto {q['ponto']} · z = {q['valor']} · concorda com HiGHS: {c['concordam']}")
    print(f"bases a enumerar com 20 variáveis e 20 restrições: {combinatoria[3]['bases']:,}".replace(",", "."))
    for g in ganho_por_unidade:
        print(f"uma unidade a mais de {g['recurso']}: R$ {g['valor_de_uma_unidade_a_mais']:.2f}")
    pc = ", ".join(f"n={p['n']}: {p['pivos']}" for p in pior_caso)
    print(f"pior caso (Klee–Minty), pivôs: {pc} — todos iguais a 2^n-1: {all(p['confere_com_2n_menos_1'] for p in pior_caso)}")


if __name__ == "__main__":
    main()
