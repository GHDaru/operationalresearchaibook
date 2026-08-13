"""Convexidade, medida — e o ótimo local que não é global, exibido.

Uma etapa por PARTE ([ADR 0013](../../adr/0013-o-que-e-a-v0.md), D3); esta ancora
o capítulo 38, que é antecipado de propósito porque ~40 capítulos vão apontar
para ele em vez de reexplicar.

DUAS COISAS SÃO MEDIDAS, e a segunda é a que justifica o capítulo existir cedo:

1. **O teste do ponto médio.** Um conjunto é convexo quando, para todo par de
   pontos dele, o segmento inteiro entre os dois também está dentro. Isso é
   testável: sorteie pares, tome o meio, veja se pertence. O teste **não prova**
   convexidade — nenhuma amostragem prova —, mas **refuta**: um único par cujo
   meio caia fora encerra a questão. Refutar é o que ele existe para fazer.

2. **O ótimo local que não é global.** Com a região não convexa, uma busca local
   honesta — que só aceita vizinho melhor e viável — **para num ponto pior** que
   o ótimo verdadeiro. É a frase "o solver achou o ótimo" perdendo o sentido, em
   número.

Aritmética exata (`Fraction`), grade de meio em meio: o resultado se regenera
igual em qualquer máquina, sem semente e sem ponto flutuante.

Rode com: python3 convexidade.py
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

AQUI = Path(__file__).parent
PASSO = F(1, 2)


# ---------------------------------------------------------------------------
# As duas regiões

def regiao_convexa(x1: F, x2: F) -> bool:
    """A montadora dos capítulos 07 a 13 — interseção de semiespaços.

    Toda região de Programação Linear é assim, e é POR ISSO que o Simplex pode
    parar no primeiro topo: num conjunto convexo com objetivo linear, ótimo local
    é ótimo global. O capítulo 09 usou esse fato a crédito.
    """
    return x1 >= 0 and x2 >= 0 and x1 + x2 <= 10 and x1 + 2 * x2 <= 12


def regiao_disjuntiva(x1: F, x2: F) -> bool:
    """"Compre do fornecedor A **ou** do fornecedor B" — e o 'ou' quebra tudo.

    A regra de negócio é banal: o contrato exige volume mínimo de um dos dois
    fornecedores, não dos dois. Nada aqui é exótico, e é esse o ponto — a
    não convexidade entra na modelagem pela porta da frente, escrita em
    português, sem ninguém notar.
    """
    return x1 >= 0 and x2 >= 0 and x1 + x2 <= 10 and (x1 >= 6 or x2 >= 8)


def grade(pertence) -> list[tuple[F, F]]:
    pontos = []
    n = int(12 / PASSO)
    for i in range(n + 1):
        for j in range(n + 1):
            p = (i * PASSO, j * PASSO)
            if pertence(*p):
                pontos.append(p)
    return pontos


def teste_do_ponto_medio(pertence, nome: str) -> dict:
    """Procura um contraexemplo: par de pontos cujo MEIO cai fora.

    Devolve o primeiro que encontrar. Ausência de contraexemplo é evidência de
    convexidade e **não é prova** — está dito no campo `veredito`.
    """
    pontos = grade(pertence)
    testados = 0
    for a, b in combinations(pontos, 2):
        testados += 1
        meio = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if not pertence(*meio):
            return {"conjunto": nome, "pares_testados": testados,
                    "contraexemplo": {"a": [str(a[0]), str(a[1])], "b": [str(b[0]), str(b[1])],
                                      "meio": [str(meio[0]), str(meio[1])]},
                    "veredito": "NÃO é convexo — o contraexemplo prova"}
    return {"conjunto": nome, "pares_testados": testados, "contraexemplo": None,
            "veredito": "nenhum contraexemplo em toda a grade — evidência de convexidade, não prova"}


# ---------------------------------------------------------------------------
# O ótimo local

def lucro(p) -> F:
    return 3 * p[0] + 2 * p[1]


def busca_local(pertence, partida: tuple[F, F]) -> dict:
    """Sobe enquanto houver vizinho viável melhor. Honesta e comum.

    É o esqueleto de quase toda heurística: olhe em volta, vá para o melhor
    vizinho, pare quando ninguém em volta for melhor. Em região convexa com
    objetivo linear isso encontra o ótimo global. Fora dela, encontra o topo do
    morro em que você começou.
    """
    atual, passos = partida, 0
    while True:
        vizinhos = [(atual[0] + dx, atual[1] + dy)
                    for dx in (-PASSO, F(0), PASSO) for dy in (-PASSO, F(0), PASSO)
                    if (dx, dy) != (F(0), F(0))]
        melhores = [v for v in vizinhos if pertence(*v) and lucro(v) > lucro(atual)]
        if not melhores:
            return {"partida": [str(partida[0]), str(partida[1])],
                    "parou_em": [str(atual[0]), str(atual[1])],
                    "lucro": str(lucro(atual)), "passos": passos}
        atual = max(melhores, key=lucro)
        passos += 1


def melhor_da_grade(pertence) -> dict:
    p = max(grade(pertence), key=lucro)
    return {"ponto": [str(p[0]), str(p[1])], "lucro": str(lucro(p))}


if __name__ == "__main__":
    convexa = teste_do_ponto_medio(regiao_convexa, "região da montadora (Programação Linear)")
    disjuntiva = teste_do_ponto_medio(regiao_disjuntiva, "região com 'fornecedor A OU fornecedor B'")

    print("TESTE DO PONTO MÉDIO")
    print("=" * 78)
    for r in (convexa, disjuntiva):
        print(f"  {r['conjunto']}")
        print(f"    pares testados: {r['pares_testados']}")
        if r["contraexemplo"]:
            c = r["contraexemplo"]
            print(f"    contraexemplo: {c['a']} e {c['b']} estão dentro · meio {c['meio']} está FORA")
        print(f"    {r['veredito']}")
    print()

    print("O ÓTIMO LOCAL QUE NÃO É GLOBAL — max 3x₁ + 2x₂ na região disjuntiva")
    print("=" * 78)
    global_ = melhor_da_grade(regiao_disjuntiva)
    partidas = [(F(0), F(8)), (F(6), F(0))]
    corridas = [busca_local(regiao_disjuntiva, p) for p in partidas]
    for c in corridas:
        print(f"  partindo de {c['partida']}: para em {c['parou_em']} com lucro {c['lucro']}"
              f" ({c['passos']} passos)")
    print(f"  melhor de toda a região: {global_['ponto']} com lucro {global_['lucro']}")

    prejuizo = F(global_["lucro"]) - min(F(c["lucro"]) for c in corridas)
    print(f"  diferença entre a pior parada e o ótimo: {prejuizo}")

    saida = {"ponto_medio": [convexa, disjuntiva],
             "busca_local": corridas, "melhor_global": global_, "diferenca": str(prejuizo)}
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # A etapa só entrega se as duas medições de fato demonstrarem o que o
    # capítulo 38 vai afirmar. Sem contraexemplo na região disjuntiva não há
    # não convexidade a ensinar; sem divergência entre as buscas não há
    # armadilha a mostrar.
    if convexa["contraexemplo"] is not None:
        raise SystemExit("✗ achou contraexemplo numa região de PL — ou o teste ou a região está errada")
    if disjuntiva["contraexemplo"] is None:
        raise SystemExit("✗ nenhum contraexemplo na região disjuntiva — ela não demonstra nada")
    if len({c["lucro"] for c in corridas}) < 2:
        raise SystemExit("✗ as duas buscas pararam no mesmo lucro — não há ótimo local a exibir")
