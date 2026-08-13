"""O que muda quando você troca de ferramenta — medido, e não suposto.

O capítulo 06 é sobre solvers, linguagens de modelagem e dados. O risco de um
capítulo assim é virar folheto: "instale isto, escreva assim". Este módulo é o
que impede — ele mede **três coisas que o leitor precisa saber antes de confiar
numa saída**, e as três aparecem no capítulo com o número na frente.

  1. **Com múltiplos ótimos, a ferramenta escolhe o seu plano.** Mesmo modelo,
     mesmo valor ótimo, planos diferentes. Quem executa a resposta executa a
     escolha do solver, não a do modelo.

  2. **Nenhum solver devolve a fração.** Eles trabalham em ponto flutuante, e
     dois solvers reportam números diferentes de casas — sem nenhum estar
     errado. O modelo da ração tem ótimo em 780/17, que não tem representação
     decimal finita.

  3. **Os vereditos concordam.** Ótimo, ilimitado e inviável saem iguais nos
     dois solvers e no Simplex exato. É a boa notícia, e ela também é resultado.

A implementação didática — exata, em `Fraction` — vem da etapa 03, e é ela que
serve de referência. Essa é a regra das duas implementações do `po-zero`
aplicada a um capítulo de ferramenta: só dá para dizer que o solver arredondou
porque existe alguém, ao lado, que não arredondou.
"""

from __future__ import annotations

import platform
import sys
from fractions import Fraction as F
from pathlib import Path

import pulp

try:                                     # highspy é a implementação do solver HiGHS
    import highspy                       # e é dela que sai o `45.88235294117647`
except ImportError:                      # pragma: no cover
    highspy = None

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "po-zero/etapa-03-simplex"))

from quadro import Restricao, resolver  # noqa: E402

SOLVERS = ("HiGHS", "CBC")


def _solver(nome: str):
    return pulp.HiGHS(msg=False) if nome == "HiGHS" else pulp.PULP_CBC_CMD(msg=False)


def por_solver(coefs: list[F], restricoes: list[Restricao], nome: str, maximizar: bool = True,
               rotulos: list[str] | None = None) -> dict:
    """Resolve pelo solver, e devolve os valores **sem arredondar**.

    O `round` que as outras etapas usam é conveniência de exibição. Aqui ele
    seria o oposto do que se quer medir: o assunto é justamente quantas casas
    cada ferramenta entrega.
    """
    rotulos = rotulos or [f"x{i+1}" for i in range(len(coefs))]
    p = pulp.LpProblem("cap06", pulp.LpMaximize if maximizar else pulp.LpMinimize)
    x = [pulp.LpVariable(r, lowBound=0) for r in rotulos]
    p += pulp.lpSum(float(c) * v for c, v in zip(coefs, x))
    for r in restricoes:
        e = pulp.lpSum(float(a) * v for a, v in zip(r.coefs, x))
        if r.sinal == "<=":
            p += e <= float(r.b)
        elif r.sinal == ">=":
            p += e >= float(r.b)
        else:
            p += e == float(r.b)
    status = pulp.LpStatus[p.solve(_solver(nome))]
    if status != "Optimal":
        return {"solver": nome, "status": status}
    return {
        "solver": nome,
        "status": status,
        "ponto": [v.value() for v in x],
        "valor": pulp.value(p.objective),
    }


def _exato(coefs: list[F], restricoes: list[Restricao], maximizar: bool = True) -> dict:
    lucros = list(coefs) if maximizar else [-c for c in coefs]
    r = resolver(lucros, [Restricao(list(x.coefs), x.sinal, x.b, x.rotulo) for x in restricoes])
    if r["status"] != "otimo":
        return {"status": r["status"]}
    ponto = r["iteracoes"][-1].ponto
    valor = sum(c * p for c, p in zip(coefs, ponto))
    return {"status": "otimo", "ponto": [str(p) for p in ponto], "valor": str(valor)}


# --- 1. múltiplos ótimos: mesmo valor, plano diferente ---------------------
# max x + y  s.a.  x + y ≤ 10,  x ≤ 6,  y ≤ 8
# A face ótima é o segmento de (2,8) a (6,4): TODO ponto dele vale 10.
MULTIPLOS = (
    [F(1), F(1)],
    [
        Restricao([F(1), F(1)], "<=", F(10), "capacidade total"),
        Restricao([F(1), F(0)], "<=", F(6), "limite de A"),
        Restricao([F(0), F(1)], "<=", F(8), "limite de B"),
    ],
)

# --- 2. ótimo fracionário: a ração do capítulo 15 --------------------------
# min 3·milho + 5·farelo  s.a.  proteína ≥ 180,  gordura ≥ 24
# Ótimo exato: milho = 180/17, farelo = 48/17, custo = 780/17.
RACAO = (
    [F(3), F(5)],
    [
        Restricao([F(9), F(30)], ">=", F(180), "proteína (g)"),
        Restricao([F(2), F(1)], ">=", F(24), "gordura (g)"),
    ],
)

# --- 3. os vereditos que não são plano -------------------------------------
ILIMITADO = ([F(1), F(1)], [Restricao([F(1), F(-1)], "<=", F(2), "só uma parede")])
INVIAVEL = ([F(1)], [Restricao([F(1)], ">=", F(5), "piso"), Restricao([F(1)], "<=", F(2), "teto")])


def multiplos_otimos() -> dict:
    coefs, rs = MULTIPLOS
    return {
        "exato": _exato(coefs, rs),
        "solvers": [por_solver(coefs, rs, s, rotulos=["A", "B"]) for s in SOLVERS],
    }


def racao() -> dict:
    coefs, rs = RACAO
    saida = {
        "exato": _exato(coefs, rs, maximizar=False),
        "valor_exato_fracao": "780/17",
        "valor_exato_float": float(F(780, 17)),
        "solvers": [por_solver(coefs, rs, s, maximizar=False, rotulos=["milho", "farelo"])
                    for s in SOLVERS],
    }
    for s in saida["solvers"]:
        if s["status"] == "Optimal":
            s["erro_absoluto"] = abs(F(s["valor"]).limit_denominator(10 ** 15) - F(780, 17))
            s["erro_absoluto"] = float(s["erro_absoluto"])
            s["casas_reportadas"] = len(repr(s["valor"]).split(".")[-1])
    return saida


def vereditos() -> dict:
    saida = {}
    for nome, (coefs, rs) in (("ilimitado", ILIMITADO), ("inviavel", INVIAVEL)):
        exato = resolver(coefs, [Restricao(list(x.coefs), x.sinal, x.b, x.rotulo) for x in rs])
        saida[nome] = {
            "exato": exato["status"],
            "solvers": [por_solver(coefs, rs, s)["status"] for s in SOLVERS],
        }
    return saida


def versoes_dos_solvers() -> dict:
    """As versões que produziram os dígitos publicados no capítulo 06.

    Sem isto, a tabela de ponto flutuante publica `45.882352` e não diz de onde
    — o que é exatamente o que o capítulo proíbe duas seções acima. O CBC vem
    embutido no PuLP, então a versão dele é a do PuLP que o empacota; dizer isso
    é mais honesto do que inventar um número de versão para o binário.
    """
    return {
        "HiGHS": getattr(highspy, "__version__", None) or _versao_instalada("highspy"),
        "CBC": f"embutido no PuLP {pulp.__version__}",
    }


def _versao_instalada(pacote: str) -> str:
    from importlib.metadata import PackageNotFoundError, version
    try:
        return version(pacote)
    except PackageNotFoundError:         # pragma: no cover
        return "não instalado"


AQUI = Path(__file__).resolve().parent

if __name__ == "__main__":
    import json

    m, r, v = multiplos_otimos(), racao(), vereditos()

    print("1. MÚLTIPLOS ÓTIMOS — mesmo valor, plano diferente")
    print("=" * 82)
    print(f"  Simplex exato : A={m['exato']['ponto'][0]}, B={m['exato']['ponto'][1]}  "
          f"· valor {m['exato']['valor']}")
    for s in m["solvers"]:
        print(f"  {s['solver']:<13} : A={s['ponto'][0]}, B={s['ponto'][1]}  · valor {s['valor']}")
    print("  → o número do relatório é o mesmo; o plano que alguém vai EXECUTAR, não.")
    print()

    print("2. PONTO FLUTUANTE — a ração, cujo ótimo é 780/17")
    print("=" * 82)
    print(f"  exato : {r['exato']['valor']}  (= {r['valor_exato_float']})")
    for s in r["solvers"]:
        print(f"  {s['solver']:<6}: {s['valor']!r}  · erro {s['erro_absoluto']:.2e}")
    print("  → nenhum devolve a fração, e os dois discordam entre si nas casas.")
    print()

    print("3. VEREDITOS — a boa notícia")
    print("=" * 82)
    for nome, d in v.items():
        print(f"  {nome:<10}: exato={d['exato']:<12} solvers={d['solvers']}")
    print()

    saida = {
        "multiplos_otimos": m,
        "racao": r,
        "vereditos": v,
        # O capítulo 06 diz, em prosa: "ao publicar um número, diga a ferramenta e
        # a VERSÃO que o produziu". Este bloco gravava os NOMES dos solvers e
        # chamava isso de versões — o capítulo enunciava a regra e a violava no
        # mesmo diretório. Encontrado pela revisão da medição.
        "versoes": {
            "python": platform.python_version(),
            "pulp": pulp.__version__,
            "solvers": versoes_dos_solvers(),
        },
    }
    (AQUI / "resultados-ferramentas.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"resultados-ferramentas.json gravado em {AQUI}")
