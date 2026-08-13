"""O relatório de sensibilidade, e a demonstração de que o preço pode ser ambíguo.

A segunda metade da etapa 05 — uma etapa por PARTE ([ADR 0013](../../adr/0013-o-que-e-a-v0.md),
D3). O `dual.py` ancora o capítulo 12; este ancora o 13.

DUAS COISAS SÃO MEDIDAS AQUI, e a segunda é a que o capítulo existe para ensinar.

1. **O relatório de sensibilidade**, em formato próprio do handbook. Por decisão
   registrada na [ADR 0014](../../adr/0014-relatorio-de-sensibilidade-e-a-faixa-medida.md)
   (D1), o handbook **não reproduz o layout de nenhum fornecedor**: o Princípio IV
   proíbe que um objetivo declarado dependa de produto licenciado. O que o
   capítulo faz é rotular explicitamente a distinção que o relatório comercial
   funde — faixa de **coeficiente** (quanto o PLANO aguenta) e faixa de **lado
   direito** (até onde o PREÇO vale) usam as mesmas palavras e autorizam coisas
   diferentes.

2. **O preço-sombra ambíguo em vértice degenerado.** Aqui não basta afirmar que
   "o número fica ambíguo", que foi o que o capítulo 10 pôde dizer. Aqui se
   EXIBE: a mesma instância, o mesmo ótimo, e dois conjuntos de preços
   diferentes, ambos válidos — a diferença sendo apenas a ORDEM em que as
   restrições foram digitadas.

Rode com: python3 sensibilidade.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "etapa-03-simplex"))
from quadro import Restricao, resolver, fmt  # noqa: E402

from dual import faixa_de_custo, faixa_de_validade, montadora, precos_sombra  # noqa: E402

AQUI = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. O relatório


def relatorio(lucros, restricoes, produtos) -> dict:
    """As duas metades do relatório, com a autorização de cada faixa explícita.

    A coluna `autoriza` não é enfeite: é o campo que o relatório comercial não
    tem, e a ausência dele é o que produz o erro caro. As duas famílias de faixa
    respondem a perguntas diferentes, e a resposta errada custa dinheiro.
    """
    r = resolver(lucros, restricoes)
    assert r["status"] == "otimo", r["status"]
    precos = precos_sombra(lucros, restricoes)["precos"]

    linhas_var = []
    for j, rotulo in enumerate(produtos):
        c = faixa_de_custo(lucros, restricoes, j, f"x{j+1}")
        linhas_var.append({
            "produto": rotulo,
            "produzir": r["ponto"][j],
            "lucro_unitario": fmt(lucros[j]),
            "lucro_pode_cair_ate": c["pode_cair_ate"],
            "lucro_pode_subir_ate": c["pode_subir_ate"],
            "autoriza": "dentro desta faixa, o PLANO não muda — só o lucro total",
        })

    linhas_restr = []
    for i, restr in enumerate(restricoes):
        f = faixa_de_validade(lucros, restricoes, i)
        linhas_restr.append({
            "recurso": restr.rotulo,
            "estoque": fmt(restr.b),
            "usado": fmt(sum(restr.coefs[j] * F(r["ponto"][j]) for j in range(len(lucros)))),
            "preco_sombra": precos[restr.rotulo],
            "estoque_pode_cair_ate": f["pode_cair_ate"],
            "estoque_pode_subir_ate": f["pode_subir_ate"],
            "autoriza": "dentro desta faixa, o PREÇO vale — fora dela, não",
        })

    return {"valor": r["valor"], "variaveis": linhas_var, "restricoes": linhas_restr}


def imprimir_relatorio(rel: dict) -> str:
    largura = 96
    L = ["RELATÓRIO DE SENSIBILIDADE — formato do handbook (ADR 0014, D1)",
         "=" * largura,
         f"lucro do plano: {rel['valor']}", "",
         "PRODUTOS — até onde o lucro unitário pode variar sem mudar O PLANO",
         "-" * largura,
         f"{'produto':<22}{'produzir':>10}{'lucro':>9}{'pode cair até':>16}{'pode subir até':>16}"]
    for v in rel["variaveis"]:
        L.append(f"{v['produto']:<22}{v['produzir']:>10}{v['lucro_unitario']:>9}"
                 f"{v['lucro_pode_cair_ate']:>16}{v['lucro_pode_subir_ate']:>16}")
    L += ["", "RECURSOS — até onde o estoque pode variar com O PREÇO ainda valendo",
          "-" * largura,
          f"{'recurso':<32}{'estoque':>9}{'usado':>8}{'preço':>8}{'pode cair até':>16}{'pode subir até':>16}"]
    for c in rel["restricoes"]:
        L.append(f"{c['recurso']:<32}{c['estoque']:>9}{c['usado']:>8}{c['preco_sombra']:>8}"
                 f"{c['estoque_pode_cair_ate']:>16}{c['estoque_pode_subir_ate']:>16}")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# 2. A ambiguidade


def montadora_com_bancada() -> tuple[list[F], list[Restricao]]:
    """A montadora mais uma restrição que passa pelo MESMO vértice ótimo.

    A bancada de teste comporta 8 unidades por dia, e o plano ótimo já produz
    exatamente 8 do Tipo 1. A restrição, portanto, **não muda nada** — e é
    justamente por não mudar nada que ela produz o fenômeno: três restrições
    passando por um ponto que, no plano, precisa de duas.

    É o caso que o capítulo 10 anunciou e não pôde exibir.
    """
    lucros, restricoes, _ = montadora()
    return lucros, restricoes + [Restricao([F(1), F(0)], "<=", F(8), "horas de bancada")]


def precos_na_ordem(lucros, restricoes, ordem: list[int]) -> dict:
    """Os preços lidos do quadro final com as restrições digitadas nesta ordem.

    Nenhum truque de solver: a mesma implementação, o mesmo critério de entrada e
    de saída. Só muda em que linha cada restrição foi escrita — que é uma decisão
    de digitação, não de modelagem.
    """
    permutadas = [restricoes[i] for i in ordem]
    r = resolver(lucros, permutadas)
    p = precos_sombra(lucros, permutadas)
    return {
        "ponto": r["ponto"],
        "valor": r["valor"],
        "base": sorted(r["iteracoes"][-1].base),
        "precos": p["precos"],
    }


def dual_viavel(lucros, restricoes, y: list[F]) -> dict:
    """`y` é solução viável do dual, e quanto ela custa?

    Dual de max c'x s.a. Ax <= b, x >= 0  é  min b'y s.a. A'y >= c, y >= 0.

    Serve de árbitro: se dois vetores diferentes passam aqui E custam o mesmo que
    o primal, então os dois são preços legítimos, e a pergunta "qual é O preço"
    não tem resposta — que é a tese do capítulo 13.
    """
    n = len(lucros)
    ok_sinal = all(v >= 0 for v in y)
    folgas = [sum(restricoes[i].coefs[j] * y[i] for i in range(len(restricoes))) - lucros[j]
              for j in range(n)]
    return {
        "y": [fmt(v) for v in y],
        "viavel": ok_sinal and all(f >= 0 for f in folgas),
        "custo": fmt(sum(restricoes[i].b * y[i] for i in range(len(restricoes)))),
    }


def derivadas(lucros, restricoes, i: int) -> dict:
    """Quanto vale MESMO uma unidade a mais do recurso `i` — medido, não lido.

    O preço-sombra é uma derivada, e em vértice degenerado a derivada pela
    esquerda e pela direita **não coincidem**. Quando isso acontece, os dois
    números do quadro estão certos e a PERGUNTA é que está mal feita.
    """
    def z(delta: F):
        alt = [Restricao(list(r.coefs), r.sinal, r.b + (delta if k == i else 0), r.rotulo)
               for k, r in enumerate(restricoes)]
        s = resolver(lucros, alt)
        return F(s["valor"]) if s["status"] == "otimo" else None

    z0, menos, mais = z(F(0)), z(F(-1)), z(F(1))
    return {
        "recurso": restricoes[i].rotulo,
        "z_menos_um": fmt(menos), "z": fmt(z0), "z_mais_um": fmt(mais),
        "derivada_pela_esquerda": fmt(z0 - menos),
        "derivada_pela_direita": fmt(mais - z0),
        "coincidem": (z0 - menos) == (mais - z0),
    }


if __name__ == "__main__":
    lucros, restricoes, ficha = montadora()
    produtos = [ficha["produtos"][p]["rotulo"] for p in ficha["produtos"]]

    rel = relatorio(lucros, restricoes, produtos)
    print(imprimir_relatorio(rel))
    print()

    print("=" * 96)
    print("O PREÇO AMBÍGUO — mesma instância, mesma implementação, só muda a ORDEM das restrições")
    print("=" * 96)
    lucros_b, restr_b = montadora_com_bancada()
    leituras = {
        "CPU, pente, bancada": precos_na_ordem(lucros_b, restr_b, [0, 1, 2]),
        "bancada, pente, CPU": precos_na_ordem(lucros_b, restr_b, [2, 1, 0]),
    }
    for nome, r in leituras.items():
        print(f"  ordem {nome:<22} ponto {r['ponto']}  valor {r['valor']}")
        print(f"        preços: {r['precos']}")

    # O árbitro: os dois vetores são soluções duais viáveis e custam o mesmo?
    print()
    print("  os dois vetores, conferidos como soluções do DUAL:")
    candidatos = [[F(50), F(50), F(0)], [F(0), F(75), F(25)], [F(25), F(125, 2), F(25, 2)]]
    checagens = [dual_viavel(lucros_b, restr_b, y) for y in candidatos]
    for c in checagens:
        print(f"    y = {str(c['y']):<30} viável: {c['viavel']}   b'y = {c['custo']}")

    print()
    print("  quanto vale mesmo uma CPU a mais, medido dos dois lados:")
    d = derivadas(lucros_b, restr_b, 0)
    print(f"    z(9) = {d['z_menos_um']} · z(10) = {d['z']} · z(11) = {d['z_mais_um']}")
    print(f"    pela esquerda: {d['derivada_pela_esquerda']} · pela direita: {d['derivada_pela_direita']}"
          f" · coincidem: {d['coincidem']}")

    saida = {"relatorio": rel, "leituras": leituras,
             "duais_conferidos": checagens, "derivadas_cpu": d}
    (AQUI / "resultados-sensibilidade.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # A etapa só entrega se a demonstração de fato demonstrar. Se os três vetores
    # não forem duais viáveis com o mesmo custo, não há ambiguidade a ensinar — e
    # o capítulo 13 não pode ser escrito com este exemplo.
    if not all(c["viavel"] and F(c["custo"]) == F(rel["valor"]) for c in checagens):
        raise SystemExit("✗ os preços alternativos NÃO são todos duais viáveis de mesmo custo")
    if d["coincidem"]:
        raise SystemExit("✗ as derivadas coincidem — este vértice não demonstra ambiguidade")
