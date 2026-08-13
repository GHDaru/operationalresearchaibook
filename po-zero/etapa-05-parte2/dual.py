"""O dual da montadora, em aritmética exata — a medição da Parte II.

Uma etapa por PARTE, não por capítulo ([ADR 0013](../../adr/0013-o-que-e-a-v0.md),
D3). Esta ancora dois capítulos de uma vez:

  - capítulo 12 (Dualidade): o dual da montadora, os preços com nome e unidade,
    e a dualidade forte conferida — não afirmada;
  - capítulo 13 (Sensibilidade): até onde cada estoque pode variar antes de o
    plano ótimo mudar.

REGRA QUE ESTA ETAPA CUMPRE: capítulo v0 não publica número que não saiba
regenerar. Todo número dos capítulos 12 e 13 sai daqui.

Aritmética exata (`Fraction`) de propósito: o capítulo 11 vai mostrar o que o
ponto flutuante faz com isso, e a comparação só é honesta se o lado exato for
exato de verdade.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "etapa-03-simplex"))
from quadro import Restricao, resolver, fmt  # noqa: E402

AQUI = Path(__file__).parent
INSTANCIA = AQUI.parent / "etapa-01-formulacao" / "instancias" / "montadora.json"


def montadora() -> tuple[list[F], list[Restricao], dict]:
    """A instância-fio, lida do arquivo — nunca redigitada aqui.

    É a mesma que atravessa os capítulos 07 a 10. Reusá-la é decisão editorial
    (o leitor não reaprende cenário) e decisão de engenharia (um número muda num
    lugar só)."""
    d = json.loads(INSTANCIA.read_text(encoding="utf-8"))
    produtos = list(d["produtos"])
    componentes = list(d["componentes"])
    lucros = [F(d["produtos"][p]["lucro_reais"]) for p in produtos]
    restricoes = [
        Restricao(
            [F(d["produtos"][p]["lista_de_materiais"].get(c, 0)) for p in produtos],
            "<=",
            F(d["componentes"][c]["estoque"]),
            d["componentes"][c]["rotulo"],
        )
        for c in componentes
    ]
    return lucros, restricoes, d


def precos_sombra(lucros, restricoes) -> dict:
    """Os preços-sombra, lidos do quadro final: são a linha `z` sob as folgas.

    Não é truque de implementação — é o TEOREMA. O custo reduzido da variável de
    folga da restrição i é exatamente o preço da restrição i, e é isso que o
    capítulo 12 ensina a enxergar no quadro que o leitor já sabe montar.
    """
    r = resolver(lucros, restricoes)
    final = r["iteracoes"][-1]
    precos = {}
    for j, col in enumerate(final.colunas):
        if col.startswith("f"):
            i = int(col[1:]) - 1
            # linha_z guarda (m, n) — a parte simbólica de M e a numérica.
            precos[restricoes[i].rotulo] = fmt(final.linha_z[j].n)
    return {"status": r["status"], "valor": r["valor"], "ponto": r["ponto"], "precos": precos}


def dual_explicito(lucros, restricoes) -> dict:
    """Resolve o DUAL como um problema próprio, e confere a dualidade forte.

    Por que isto existe em vez de só ler o quadro: ler o preço no quadro primal
    é conveniente e circular — usa o mesmo cálculo para produzir e para conferir.
    Montar o dual como problema separado e chegar ao MESMO valor ótimo é a
    verificação independente. Se os dois divergirem, o capítulo 12 está errado.

    Dual de  max c'x s.a Ax <= b, x >= 0
    é        min b'y s.a A'y >= c, y >= 0.

    O `quadro.resolver` maximiza, então minimizamos maximizando o negativo — e
    as restrições `>=` entram com variável artificial e big-M, que é a máquina
    que o capítulo 09 construiu.
    """
    m = len(restricoes)
    n = len(lucros)
    b = [r.b for r in restricoes]
    # A' : uma restrição do dual por variável do primal
    dual_restr = [
        Restricao([restricoes[i].coefs[j] for i in range(m)], ">=", lucros[j], f"custo de x{j+1}")
        for j in range(n)
    ]
    r = resolver([-x for x in b], dual_restr, nomes=[f"y{i+1}" for i in range(m)])
    # `resolver` devolve `valor` já formatado como TEXTO. Voltar a fração antes
    # de negar — comparar texto com fração daria falso negativo na dualidade
    # forte, que é a única verificação que esta etapa existe para fazer.
    valor = -F(r["valor"]) if r["status"] == "otimo" else None
    return {"status": r["status"], "valor_dual": fmt(valor) if valor is not None else None,
            "y": r["ponto"], "pivos": r["pivos"]}


def faixa_de_validade(lucros, restricoes, indice: int) -> dict:
    """Até onde o estoque do componente `indice` pode variar sem mudar a BASE.

    Enquanto a base não muda, o preço-sombra vale e o plano muda de forma
    previsível. Sair da faixa é o erro clássico de leitura que o capítulo 13
    ensina a não cometer — e o capítulo 10 já avisou que em vértice degenerado a
    faixa fica ambígua.

    Método: varre o lado direito por passos exatos e registra onde a BASE do
    quadro final deixa de ser a mesma. Busca direta, não fórmula — o capítulo
    ensina a ideia, e a etapa mostra a fronteira sem exigir álgebra de
    sensibilidade que o leitor v0 ainda não tem.
    """
    base0 = tuple(sorted(resolver(lucros, restricoes)["iteracoes"][-1].base))
    b0 = restricoes[indice].b

    def base_com(delta: F):
        alt = [Restricao(list(r.coefs), r.sinal, r.b + (delta if i == indice else 0), r.rotulo)
               for i, r in enumerate(restricoes)]
        r = resolver(lucros, alt)
        if r["status"] != "otimo":
            return None
        return tuple(sorted(r["iteracoes"][-1].base)), r["valor"]

    passo = F(1, 2)
    def limite(sentido: int):
        d, ultimo = passo * sentido, F(0)
        while abs(d) <= 40:
            res = base_com(d)
            if res is None or res[0] != base0:
                return ultimo
            ultimo = d
            d += passo * sentido
        return ultimo

    return {
        "componente": restricoes[indice].rotulo,
        "estoque_atual": fmt(b0),
        "pode_cair_ate": fmt(b0 + limite(-1)),
        "pode_subir_ate": fmt(b0 + limite(+1)),
        "base_de_referencia": list(base0),
    }


if __name__ == "__main__":
    lucros, restricoes, ficha = montadora()

    primal = precos_sombra(lucros, restricoes)
    dual = dual_explicito(lucros, restricoes)
    faixas = [faixa_de_validade(lucros, restricoes, i) for i in range(len(restricoes))]

    # A VERIFICAÇÃO QUE IMPORTA: dualidade forte. Os dois problemas, resolvidos
    # separadamente, têm de chegar ao mesmo valor. Se não chegarem, não é o
    # capítulo que está errado — é esta etapa, e o capítulo não pode ser escrito.
    # Comparação em FRAÇÃO, não em texto: "1100" e "1100/1" são o mesmo número
    # e textos diferentes.
    confere = (dual["valor_dual"] is not None
               and F(primal["valor"]) == F(dual["valor_dual"]))

    saida = {
        "instancia": ficha["ficha"]["nome"],
        "primal": primal,
        "dual": dual,
        "dualidade_forte_confere": confere,
        "faixas_de_validade": faixas,
    }
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"instância: {saida['instancia']}")
    print(f"primal   : ponto {primal['ponto']}  valor {primal['valor']}")
    print(f"preços   : {primal['precos']}")
    print(f"dual     : y = {dual['y']}  valor {dual['valor_dual']}  ({dual['pivos']} pivôs)")
    print(f"dualidade forte confere: {confere}")
    print()
    for f in faixas:
        print(f"  {f['componente']}: hoje {f['estoque_atual']} · "
              f"faixa [{f['pode_cair_ate']}, {f['pode_subir_ate']}]")
    if not confere:
        raise SystemExit("✗ dualidade forte NÃO confere — o capítulo 12 não pode ser escrito")
