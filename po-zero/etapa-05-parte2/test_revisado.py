"""O capítulo 11 tem de bater com a medição — inclusive nos resultados NEGATIVOS.

Um teste que só protege resultados favoráveis é um teste que ajuda a maquiar. Os
dois negativos desta etapa — a forma revisada perdendo em duas instâncias, e o
limiar de estagnação nunca sendo atingido — estão asseverados aqui exatamente
como os positivos. Se um dia a implementação mudar e a revisada passar a ganhar
sempre, este arquivo fica **vermelho**, e é o que se quer: o capítulo teria de
ser reescrito, não silenciosamente corrigido.
"""

from __future__ import annotations

import random
from fractions import Fraction as F
from pathlib import Path

import pytest

from revisado import (INSTANCIAS, LIMIAR_ESTAGNACAO, SEMENTE, fracao_contra_float,
                      gerar, medir, perfil_de_estagnacao)

CAPITULO = Path(__file__).resolve().parents[2] / "livro/capitulos/11-simplex-revisado.md"


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def linhas():
    rng = random.Random(SEMENTE)
    out = []
    for rotulo, m, n, dens in INSTANCIAS:
        c, A, b, realizada = gerar(m, n, dens, rng)
        out.append(medir(rotulo, c, A, b, realizada))
    return {r["instancia"]: r for r in out}


def test_as_tres_garantias_da_medicao(linhas):
    """Sem elas, resultado inesperado vira suspeita de bug — e a lição se perde."""
    for r in linhas.values():
        assert r["concordam"], f"{r['instancia']}: divergiu do oráculo da etapa 03"
        assert r["mesma_trajetoria_de_pivo"], f"{r['instancia']}: trajetórias de pivô diferentes"


def test_as_razoes_publicadas(linhas, texto):
    esperado = {"pequena densa": 1.265, "pequena esparsa": 0.935, "média densa": 1.87,
                "média esparsa": 1.341, "magra densa": 2.956, "magra esparsa": 0.746}
    for nome, razao in esperado.items():
        assert linhas[nome]["razao_quadro_sobre_revisada"] == razao
        assert str(razao) in texto, f"o capítulo não publica a razão de {nome}"


def test_o_ganho_cresce_com_n_sobre_m_nas_densas(linhas):
    """A tendência que o capítulo afirma, conferida em vez de contada."""
    densas = ["pequena densa", "média densa", "magra densa"]
    razoes = [linhas[d]["razao_quadro_sobre_revisada"] for d in densas]
    nm = [linhas[d]["n"] / linhas[d]["m"] for d in densas]
    assert nm == sorted(nm), "as densas não estão em ordem crescente de n/m"
    assert razoes == sorted(razoes), "o ganho não cresce com n/m — a afirmação do capítulo caiu"


def test_o_resultado_negativo_da_forma_revisada(linhas):
    """A revisada PERDE em duas instâncias. É resultado, e é protegido como tal."""
    perdedoras = [n for n, r in linhas.items() if r["razao_quadro_sobre_revisada"] < 1]
    assert set(perdedoras) == {"pequena esparsa", "magra esparsa"}


def test_o_preenchimento_explica(linhas):
    """A explicação medida: onde o quadro preenche muito, a revisada ganha."""
    esparsas = ["média esparsa", "magra esparsa"]
    fill = {n: linhas[n]["preenchimento"] for n in esparsas}
    assert fill["média esparsa"] > fill["magra esparsa"]
    assert linhas["média esparsa"]["razao_quadro_sobre_revisada"] > 1
    assert linhas["magra esparsa"]["razao_quadro_sobre_revisada"] < 1


def test_nenhuma_instancia_estagna_pelo_limiar_declarado(texto):
    """O SEGUNDO negativo, e o mais delicado.

    Se algum dia uma destas passar a estagnar, este teste fica vermelho — e a
    seção do capítulo que publica o negativo terá de ser reescrita. É o oposto de
    baixar o limiar até caber: aqui o limiar é constante e o resultado é o que
    varia.
    """
    assert LIMIAR_ESTAGNACAO == 3
    rng2 = random.Random(SEMENTE + 1)
    c2, A2, b2, _ = gerar(12, 60, 0.30, rng2)
    aleatoria = perfil_de_estagnacao(c2, A2, b2)
    degenerada = perfil_de_estagnacao(
        [2, 3], [[1, 1], [1, 2], [1, 0], [0, 1], [3, 2]], [4, 6, 2, 2, 10])

    assert aleatoria["veredito"] == "lentidão"
    assert aleatoria["iteracoes"] == 30
    assert not aleatoria["estagna_pelo_limiar"]
    assert not degenerada["estagna_pelo_limiar"]
    assert not aleatoria["base_repetiu"] and not degenerada["base_repetiu"]
    assert "VEREDITO: lentidão" in texto
    assert "limiar não foi baixado" in texto or "não foi baixado" in texto


def test_float_nao_mudou_o_veredito(texto):
    """O terceiro negativo. E a asserção que importa é a da BASE, não a do valor."""
    rng2 = random.Random(SEMENTE + 1)
    c2, A2, b2, _ = gerar(12, 60, 0.30, rng2)
    n = fracao_contra_float(c2, A2, b2)
    assert n["valor_exato"] == "965935/486"
    assert n["mesma_base"]
    assert not n["veredito_mudou"]
    assert n["erro_relativo"] < 1e-15
    assert "965935/486" in texto


def test_a_ponte_declara_que_ninguem_inverte(texto):
    """Critério A16 da spec 008: a caixa que fecha a ponte tem de existir."""
    assert "solver nenhum faz" in texto
    assert "notação, não instrução" in texto
