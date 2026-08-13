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


def _quadro_final(lucros, restricoes):
    """O quadro final, com o índice de cada coluna de folga.

    Serve às duas faixas. Vale só para o caso deste capítulo — todas as
    restrições `<=`, folgas na base inicial — que é justamente quando as
    colunas de folga do quadro final SÃO a inversa da base, $B^{-1}$.
    """
    r = resolver(lucros, restricoes)
    assert r["status"] == "otimo", r["status"]
    f = r["iteracoes"][-1]
    col_folga = [f.colunas.index(f"f{i+1}") for i in range(len(restricoes))]
    return f, col_folga


def faixa_de_validade(lucros, restricoes, indice: int) -> dict:
    """Até onde o estoque do componente `indice` pode variar sem mudar a BASE.

    Enquanto a base não muda, o preço-sombra vale e o plano muda de forma
    previsível. Sair da faixa é o erro clássico de leitura que o capítulo 13
    ensina a não cometer — e o capítulo 10 já avisou que em vértice degenerado a
    faixa fica ambígua.

    ---------------------------------------------------------------------------
    ESTA FUNÇÃO JÁ ESTEVE ERRADA, e o erro chegou a texto de capítulo.

    A primeira versão varria o lado direito de meio em meio e reportava o último
    valor em que a base do quadro final ainda era a mesma. O defeito é
    estrutural, não de precisão: a varredura mede EM QUE BASE O SIMPLEX
    ATERRISSA, e não PARA QUE LADO DIREITO A BASE CONTINUA ÓTIMA. Na fronteira
    o vértice fica degenerado e o método pode aterrissar em outra base
    equivalente — então a varredura lê "mudou" um passo antes da fronteira real
    e **subestima sempre**. Publicou 13/2 onde o certo é 6, e 39/2 onde o certo
    é 20. O teto 12 saiu certo por sorte de desempate, o que é pior: um método
    que erra um lado e acerta o outro sem avisar não é medição.

    O método correto é álgebra, e cabe no quadro que o leitor já tem. Com todas
    as restrições `<=`, as colunas de folga do quadro final são $B^{-1}$. Somar
    $\\Delta$ ao estoque $i$ desloca as básicas por $\\Delta$ vezes a coluna $i$
    de $B^{-1}$, e a base continua viável enquanto todas seguirem $\\ge 0$:

        x_B + Δ·(B⁻¹ e_i) ≥ 0

    Isso dá a fronteira EXATA, em fração, sem passo e sem resolver de novo.
    ---------------------------------------------------------------------------
    """
    f, col_folga = _quadro_final(lucros, restricoes)
    b0 = restricoes[indice].b
    d = [linha[col_folga[indice]] for linha in f.corpo]   # coluna i de B⁻¹
    xb = list(f.lado_direito)

    inf, sup = None, None                                  # None = sem limite
    for r, dr in enumerate(d):
        if dr == 0:
            continue
        limite = -xb[r] / dr                               # Δ em que a básica r zera
        if dr > 0:
            inf = limite if inf is None else max(inf, limite)
        else:
            sup = limite if sup is None else min(sup, limite)

    return {
        "componente": restricoes[indice].rotulo,
        "estoque_atual": fmt(b0),
        "pode_cair_ate": fmt(b0 + inf) if inf is not None else "sem limite",
        "pode_subir_ate": fmt(b0 + sup) if sup is not None else "sem limite",
        "base_de_referencia": sorted(f.base),
    }


def faixa_de_custo(lucros, restricoes, j: int, nome: str) -> dict:
    """Quanto o lucro unitário do produto `j` pode variar sem mudar o PLANO.

    A outra metade do relatório de sensibilidade, e a que responde à pergunta do
    comercial: *"até onde eu posso baixar o preço deste produto antes de valer
    a pena produzir outra coisa?"*.

    Método, para uma variável BÁSICA na linha `r`: somar $\\delta$ ao seu lucro
    desloca a linha $z$ em $\\delta \\cdot a_{rk}$ em cada coluna não básica `k`.
    A otimalidade exige que todo custo reduzido siga $\\ge 0$:

        (z_k - c_k) + δ·a_rk ≥ 0   para toda coluna k fora da base

    Para uma variável FORA da base é uma desigualdade só — ela entra na base
    quando o próprio custo reduzido dela zera.

    É varredura da LINHA do quadro, não do modelo: nenhum problema é resolvido
    de novo, e o resultado é exato.
    """
    f, _ = _quadro_final(lucros, restricoes)
    col = f.colunas.index(nome)
    c0 = lucros[j]

    # `Iteracao.base` guarda NOMES de coluna, não índices — comparar índice com
    # essa lista dá sempre falso, e a função inteira devolveria "fora da base"
    # para todo mundo, em silêncio. Foi o que aconteceu na primeira execução.
    inf, sup = None, None
    if nome in f.base:
        r = f.base.index(nome)
        for k, coluna in enumerate(f.colunas):
            if coluna in f.base:
                continue
            a = f.corpo[r][k]
            if a == 0:
                continue
            limite = -f.linha_z[k].n / a
            if a > 0:
                inf = limite if inf is None else max(inf, limite)
            else:
                sup = limite if sup is None else min(sup, limite)
    else:
        sup = f.linha_z[col].n                             # sobe até o custo reduzido zerar

    return {
        "produto": nome,
        "lucro_atual": fmt(c0),
        "pode_cair_ate": fmt(c0 + inf) if inf is not None else "sem limite",
        "pode_subir_ate": fmt(c0 + sup) if sup is not None else "sem limite",
        "na_base": nome in f.base,
    }


def confere_faixa(lucros, restricoes, indice: int, faixa: dict) -> dict:
    """A conferência INDEPENDENTE da faixa, e é ela que fecha o buraco.

    A álgebra acima é uma derivação; se ela estiver errada, ela erra em silêncio,
    do mesmo jeito que a varredura errava. Então a fronteira é conferida por um
    caminho que não usa $B^{-1}$ nenhum: resolve-se o problema DE NOVO, com o
    estoque posto exatamente na fronteira e um pouco além dela, e verifica-se se
    o preço-sombra ainda prevê o valor ótimo.

      - NA fronteira, o preço tem de acertar:  z(b) = z(b₀) + y_i·(b − b₀)
      - ALÉM dela, o preço tem de ERRAR.

    Se o preço acerta além da fronteira, a faixa está curta demais. Se erra na
    fronteira, está longa demais. Os dois casos falham a etapa.
    """
    y = F(precos_sombra(lucros, restricoes)["precos"][restricoes[indice].rotulo])
    z0 = F(resolver(lucros, restricoes)["valor"])
    b0 = restricoes[indice].b

    def z_em(b: F):
        alt = [Restricao(list(r.coefs), r.sinal, b if i == indice else r.b, r.rotulo)
               for i, r in enumerate(restricoes)]
        r = resolver(lucros, alt)
        return F(r["valor"]) if r["status"] == "otimo" else None

    def preve(b: F) -> bool:
        z = z_em(b)
        return z is not None and z == z0 + y * (b - b0)

    fora = F(1, 4)                                          # um passo pequeno além
    saida = {"componente": restricoes[indice].rotulo}
    for lado, chave in (("piso", "pode_cair_ate"), ("teto", "pode_subir_ate")):
        if faixa[chave] == "sem limite":
            saida[lado] = "sem limite"
            continue
        fronteira = F(faixa[chave])
        alem = fronteira - fora if lado == "piso" else fronteira + fora
        saida[lado] = {
            "fronteira": fmt(fronteira),
            "preco_acerta_na_fronteira": preve(fronteira),
            "preco_erra_alem": not preve(alem),
        }
    return saida


if __name__ == "__main__":
    lucros, restricoes, ficha = montadora()

    primal = precos_sombra(lucros, restricoes)
    dual = dual_explicito(lucros, restricoes)
    faixas = [faixa_de_validade(lucros, restricoes, i) for i in range(len(restricoes))]
    conferencias = [confere_faixa(lucros, restricoes, i, faixas[i]) for i in range(len(restricoes))]
    produtos = [ficha["produtos"][p]["rotulo"] for p in ficha["produtos"]]
    custos = [faixa_de_custo(lucros, restricoes, j, f"x{j+1}") for j in range(len(lucros))]
    for c, rotulo in zip(custos, produtos):
        c["rotulo"] = rotulo

    # As faixas só entram no livro se as duas conferências fecharem: o preço tem
    # de acertar NA fronteira e errar ALÉM dela. É a verificação que a versão
    # por varredura não tinha — e que teria barrado os números errados.
    faixas_conferem = all(
        lado == "sem limite" or (lado["preco_acerta_na_fronteira"] and lado["preco_erra_alem"])
        for c in conferencias for lado in (c["piso"], c["teto"])
    )

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
        "faixas_conferidas": conferencias,
        "faixas_conferem": faixas_conferem,
        "faixas_de_custo": custos,
    }
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"instância: {saida['instancia']}")
    print(f"primal   : ponto {primal['ponto']}  valor {primal['valor']}")
    print(f"preços   : {primal['precos']}")
    print(f"dual     : y = {dual['y']}  valor {dual['valor_dual']}  ({dual['pivos']} pivôs)")
    print(f"dualidade forte confere: {confere}")
    print()
    print("faixa do ESTOQUE — até onde o preço-sombra vale")
    for f in faixas:
        print(f"  {f['componente']}: hoje {f['estoque_atual']} · "
              f"faixa [{f['pode_cair_ate']}, {f['pode_subir_ate']}]")
    print(f"faixas conferidas por caminho independente: {faixas_conferem}")
    print()
    print("faixa do LUCRO UNITÁRIO — até onde o plano continua o mesmo")
    for c in custos:
        print(f"  {c['rotulo']}: hoje {c['lucro_atual']} · "
              f"faixa [{c['pode_cair_ate']}, {c['pode_subir_ate']}]")

    if not confere:
        raise SystemExit("✗ dualidade forte NÃO confere — o capítulo 12 não pode ser escrito")
    if not faixas_conferem:
        raise SystemExit("✗ alguma faixa NÃO confere pelo caminho independente — não publique o número")
