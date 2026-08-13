"""A distância entre o pior caso e a instância que você tem na mão.

O capítulo 05 faz uma afirmação incômoda: *"NP-difícil" e "pior caso
exponencial" são afirmações sobre a CLASSE, não sobre a sua instância* — e
usar a teoria para decidir não tentar é pular uma medição.

Este módulo mede as duas pontas dessa distância, em aritmética exata:

  1. **O pior caso existe e é construído.** O cubo de Klee–Minty faz o Simplex
     com a regra de Dantzig visitar todos os 2ⁿ vértices. Isso já estava medido
     na etapa 03, e aqui é reaproveitado — não reimplementado.

  2. **A instância aleatória não chega perto dele.** Mesmo tamanho, mesma
     estrutura de `≤`, e o número de pivôs cresce devagar.

E mede, de quebra, uma terceira coisa que **contraria a leitura fácil** da
literatura de análise suavizada, e por isso vale mais do que as outras duas:
perturbar levemente o cubo **não** o desmancha. Ver `perturba` para o detalhe e
para o que a medição NÃO autoriza concluir.

Tudo em `Fraction`. Nenhum ponto flutuante decide nada aqui — pela mesma razão
das outras etapas: um pivô a mais por erro de arredondamento seria indistinguível
de um pivô a mais por estrutura, e é exatamente a estrutura que está sendo medida.
"""

from __future__ import annotations

import random
import sys
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# O Simplex e o cubo vêm da etapa 03. Reimplementar qualquer um dos dois criaria
# uma segunda fonte da verdade para números que o livro já publicou — que é a
# classe de defeito que a ADR 0016 proíbe nos cadernos, e que não tem por que
# ser tolerada entre etapas.
sys.path.insert(0, str(RAIZ / "po-zero/etapa-03-simplex"))

from experimento import klee_minty  # noqa: E402
from quadro import Restricao, resolver  # noqa: E402

LIMITE = 20_000
SEMENTE_BASE = 20260813


def _copia(rs: list[Restricao]) -> list[Restricao]:
    """`resolver` normaliza restrições no lugar — devolver cópia evita surpresa."""
    return [Restricao(list(r.coefs), r.sinal, r.b, r.rotulo) for r in rs]


def pivos(lucros: list[F], restricoes: list[Restricao]) -> dict:
    r = resolver(lucros, _copia(restricoes), limite=LIMITE)
    return {"status": r["status"], "pivos": len(r["iteracoes"]) - 1}


def pior_caso(n: int) -> dict:
    """O cubo de Klee–Minty puro: 2ⁿ vértices, 2ⁿ−1 pivôs com a regra de Dantzig."""
    lucros, rs = klee_minty(n)
    m = pivos(lucros, rs)
    return {"n": n, "vertices": 2 ** n, "esperado": 2 ** n - 1, **m}


def perturba(n: int, magnitude: F, semente: int) -> dict:
    """O mesmo cubo com a MATRIZ perturbada — e o resultado que surpreende.

    A leitura fácil da análise suavizada (Spielman & Teng, 2004, na bibliografia)
    é que "o pior caso é frágil": bastaria mexer um pouco na entrada para o
    Simplex voltar a ser rápido. **A medição não sustenta essa leitura na forma
    ingênua.** Com perturbação relativa de 1% ou de 0,1%, o cubo continua
    custando exatamente 2ⁿ−1 pivôs — nada muda.

    O que a medição NÃO autoriza concluir: que o resultado de 2004 esteja errado.
    Ele é assintótico, em ESPERANÇA, sob perturbação gaussiana e com uma regra de
    pivoteamento específica — nenhuma dessas três condições vale aqui. O que a
    medição autoriza é uma advertência editorial: a frase "o pior caso é frágil"
    não descreve o que acontece quando alguém mexe 1% numa instância ruim.

    A degradação é **gradual e cara**: só em perturbações grandes o caminho
    encurta, e "grande" aqui significa mudar a instância a ponto de ela ser
    outra instância.

    O MODELO DE PERTURBAÇÃO, DECLARADO — porque ele é load-bearing.

    A perturbação é **multiplicativa, relativa, entrada a entrada, e preserva o
    padrão de zeros** da matriz triangular do cubo: cada coeficiente não nulo
    vira `c · (1 + δ)`, com `δ` uniforme em `[-magnitude, +magnitude]`. Quem
    reproduzir isto com ruído **aditivo denso** obtém outro resultado e concluirá
    que o handbook errou — e não terá errado: preencher os zeros do cubo com
    valores da ordem dos não nulos não é uma perturbação pequena, porque as
    variáveis do cubo chegam a 10ⁿ. Calibrando o preenchimento para que cada
    restrição mude no máximo 1% **no vértice ótimo**, que é a única definição
    invariante de "pequeno", o resultado volta a ser o mesmo.

    DUAS SEMENTES NÃO SÃO UMA MEDIÇÃO, E VINTE TAMBÉM NÃO ERAM.

    A tabela publicada no capítulo 05 nasceu de **um sorteio por magnitude**. A
    primeira revisão apontou a assimetria — a tabela vizinha declarava "20
    amostras por tamanho", esta declarava nada — e a correção foi para 20. A
    revisão da medição mostrou que 20 ainda era pouco **para o que a tabela
    publicava**: mínimo e máximo são estatísticas de ordem e se mexem muito com
    o tamanho da amostra (o máximo de 50% vai de 47 para 63 ao passar de 20 para
    200 sementes), enquanto **mediana e fração de caminhos intactos** ficam
    parados. Daí o desenho atual: 200 sementes, e a tabela publica só o que
    estabiliza.
    """
    rnd = random.Random(semente)
    lucros, rs = klee_minty(n)
    pert = []
    for r in rs:
        coefs = [
            c * (1 + magnitude * F(rnd.randint(-1000, 1000), 1000)) if c != 0 else c
            for c in r.coefs
        ]
        pert.append(Restricao(coefs, r.sinal, r.b, r.rotulo))
    return {"n": n, "magnitude": str(magnitude), "semente": semente, **pivos(lucros, pert)}


AMOSTRAS_PERTURBACAO = 200
AMOSTRAS_ALEATORIAS = 200
# O eixo em que o teorema de 2004 vive é o crescimento em n, e a tabela principal
# olha um n só. Esta varredura é curta de propósito — serve para dizer a direção,
# não para medir a taxa.
TAMANHOS_VARREDURA = (4, 5, 6, 7, 8)
AMOSTRAS_VARREDURA = 25


@lru_cache(maxsize=None)
def perfil_de_perturbacao(n: int, magnitude: F, amostras: int = AMOSTRAS_PERTURBACAO) -> dict:
    """A distribuição de pivôs sob perturbação, e não um sorteio dela.

    Devolve mediana e — o número que o capítulo publica — **em quantas das
    amostras o caminho ficou exatamente igual ao do cubo puro**. É essa fração
    que separa "não muda nada" de "quase nunca muda".

    Mínimo e máximo saem no dicionário para inspeção, e **não são publicados**:
    são estatísticas de ordem, e por isso se movem com o tamanho da amostra
    mesmo quando a distribuição não mudou. Publicar extremo de amostra pequena é
    a mesma classe de defeito que publicar um sorteio.

    Em cache porque a suíte pede o mesmo perfil várias vezes, e 200 sementes por
    magnitude não é barato.
    """
    puro = 2 ** n - 1
    contagens = sorted(
        perturba(n, magnitude, SEMENTE_BASE + 7000 + s)["pivos"] for s in range(amostras)
    )
    meio = len(contagens) // 2
    mediana = (contagens[meio] if len(contagens) % 2
               else F(contagens[meio - 1] + contagens[meio], 2))
    return {
        "n": n,
        "magnitude": str(magnitude),
        "amostras": amostras,
        "minimo": contagens[0],
        "mediana": str(mediana),
        "maximo": contagens[-1],
        "intactas": sum(1 for c in contagens if c == puro),
        "puro": puro,
    }


@lru_cache(maxsize=None)
def varredura_em_n(magnitude: F, amostras: int = AMOSTRAS_VARREDURA) -> list[dict]:
    """A fração de caminhos intactos conforme o cubo cresce.

    É o eixo que a tabela principal não olha, e é justamente o eixo em que a
    análise suavizada faz a sua afirmação. Medir aqui não confirma o teorema —
    a construção e a regra de pivoteamento são outras —, mas impede o capítulo
    de dizer que "não muda nada" a partir de um único tamanho.
    """
    saida = []
    for n in TAMANHOS_VARREDURA:
        puro = 2 ** n - 1
        intactas = sum(
            perturba(n, magnitude, SEMENTE_BASE + 9000 + s)["pivos"] == puro
            for s in range(amostras)
        )
        saida.append({"n": n, "magnitude": str(magnitude), "amostras": amostras,
                      "intactas": intactas, "puro": puro})
    return saida


def instancia_aleatoria(n: int, m: int, semente: int) -> tuple[list[F], list[Restricao]]:
    """Uma instância de PL do mesmo tamanho do cubo, e sem nenhuma malícia.

    Coeficientes inteiros pequenos, todos `≤`, lado direito positivo: a origem é
    sempre viável e a base de folgas serve de partida, então não há *big-M* no
    caminho — o número de pivôs mede o caminho, e não a partida.
    """
    rnd = random.Random(semente)
    lucros = [F(rnd.randint(1, 20)) for _ in range(n)]
    rs = [
        Restricao([F(rnd.randint(0, 9)) for _ in range(n)], "<=", F(rnd.randint(50, 200)), f"r{i+1}")
        for i in range(m)
    ]
    return lucros, rs


@lru_cache(maxsize=None)
def perfil_aleatorio(n: int, amostras: int = AMOSTRAS_ALEATORIAS) -> dict:
    """Distribuição de pivôs em `amostras` instâncias aleatórias de tamanho n×n.

    O **máximo** desta tabela é publicado, ao contrário do da tabela de
    perturbação, e a diferença tem razão: aqui ele é o argumento. Dizer que a
    PIOR de 200 instâncias custou 19 pivôs, onde o cubo do mesmo tamanho custa
    mais de um milhão, é mais forte do que dizer que a mediana custou 7. Com 20
    amostras esse máximo era 12 e não significava quase nada — extremo de amostra
    pequena é ruído; extremo de amostra grande é evidência.
    """
    contagens = []
    for s in range(amostras):
        lucros, rs = instancia_aleatoria(n, n, SEMENTE_BASE + 1000 * n + s)
        r = pivos(lucros, rs)
        if r["status"] != "otimo":
            raise AssertionError(f"instância aleatória n={n} semente={s} deu {r['status']}")
        contagens.append(r["pivos"])
    contagens.sort()
    meio = len(contagens) // 2
    mediana = (
        contagens[meio]
        if len(contagens) % 2
        else F(contagens[meio - 1] + contagens[meio], 2)
    )
    return {
        "n": n,
        "amostras": amostras,
        "minimo": contagens[0],
        "mediana": str(mediana),
        "maximo": contagens[-1],
        "pior_caso_construido": 2 ** n - 1,
    }


AQUI = Path(__file__).resolve().parent
TAMANHOS_ALEATORIOS = (5, 10, 15, 20)
MAGNITUDES = (F(1, 1000), F(1, 100), F(1, 10), F(1, 4), F(1, 2))

if __name__ == "__main__":
    import json

    piores = [pior_caso(n) for n in range(2, 8)]
    print("O PIOR CASO, CONSTRUÍDO — cubo de Klee–Minty, regra de Dantzig")
    print("=" * 82)
    for p in piores:
        ok = "✓" if p["pivos"] == p["esperado"] else "✗"
        print(f"  n={p['n']}  vértices={p['vertices']:>4}  pivôs={p['pivos']:>4}  "
              f"(2^n−1 = {p['esperado']}) {ok}")
    print()

    N_PERT = 6
    perts = [perfil_de_perturbacao(N_PERT, mag) for mag in MAGNITUDES]
    print(f"O MESMO CUBO PERTURBADO (n={N_PERT}) — e o resultado que contraria a leitura fácil")
    print(f"{AMOSTRAS_PERTURBACAO} sementes por magnitude; o cubo puro custa {2 ** N_PERT - 1} pivôs")
    print("=" * 82)
    for p in perts:
        print(f"  perturbação de {p['magnitude']:>6}: mediana {p['mediana']:>4} pivôs   "
              f"caminhos intactos: {p['intactas']}/{p['amostras']}"
              f"   (mín {p['minimo']}, máx {p['maximo']} — extremos de amostra, NÃO publicados)")
    print()

    varreduras = {str(mag): varredura_em_n(mag) for mag in (F(1, 100), F(1, 10))}
    print("O EIXO QUE A TABELA ACIMA NÃO OLHA — caminhos intactos conforme o cubo cresce")
    print("=" * 82)
    for mag, linhas in varreduras.items():
        marcas = "  ".join(f"n={l['n']}: {l['intactas']}/{l['amostras']}" for l in linhas)
        print(f"  perturbação de {mag:>6}: {marcas}")
    print()

    perfis = [perfil_aleatorio(n) for n in TAMANHOS_ALEATORIOS]
    print(f"A INSTÂNCIA ALEATÓRIA — mesmo tamanho, nenhuma malícia, {AMOSTRAS_ALEATORIAS} amostras cada")
    print("=" * 82)
    for p in perfis:
        print(f"  n=m={p['n']:>2}  pivôs: mediana {p['mediana']:>4} · máx {p['maximo']:>3} · "
              f"({p['amostras']} amostras)   contra o cubo de Klee–Minty do mesmo tamanho: {p['pior_caso_construido']}")
    print()

    saida = {
        "pior_caso_do_cubo": piores,
        "pior_caso_perturbado": {"n": N_PERT, "amostras": AMOSTRAS_PERTURBACAO, "medicoes": perts},
        "varredura_em_n": varreduras,
        "instancias_aleatorias": perfis,
        "versoes": {"python": sys.version.split()[0], "aritmetica": "fractions.Fraction (exata)"},
        "semente_base": SEMENTE_BASE,
    }
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"resultados.json gravado em {AQUI}")
