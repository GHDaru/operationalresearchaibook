"""O capítulo 38 e a sua bateria têm de bater com a medição.

Este arquivo carrega uma responsabilidade extra, e ela está declarada no
`verifica-otimos.mjs`: os números do `cap38.exB` **não podem** ser conferidos
pelo portão de ótimo do livro, porque a região do exercício é uma UNIÃO e o
portão só sabe enumerar vértices de interseções de semiespaços — ele é, por
construção, uma máquina de conjuntos convexos. Um exercício sobre não
convexidade é exatamente o que ele não alcança.

Então a conferência acontece aqui, e a isenção lá aponta para cá. Nenhum número
do handbook fica sem dono.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

import pytest

from convexidade import (busca_local, lucro, melhor_da_grade, regiao_convexa,
                         regiao_disjuntiva, teste_do_ponto_medio)

RAIZ = Path(__file__).resolve().parents[2]
CAPITULO = RAIZ / "livro/capitulos/38-convexidade.md"


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def exercicios():
    return {e["id"]: e for e in json.loads((RAIZ / "livro/exercicios.json").read_text(encoding="utf-8"))}


def test_a_regiao_de_pl_nao_tem_contraexemplo(texto):
    r = teste_do_ponto_medio(regiao_convexa, "montadora")
    assert r["contraexemplo"] is None
    assert r["pares_testados"] == 12561
    assert "pares testados: 12561" in texto


def test_a_regiao_disjuntiva_tem_contraexemplo(texto):
    r = teste_do_ponto_medio(regiao_disjuntiva, "disjuntiva")
    c = r["contraexemplo"]
    assert c is not None
    assert (c["a"], c["b"], c["meio"]) == (["0", "8"], ["6", "0"], ["3", "4"])
    assert "contraexemplo: ['0', '8'] e ['6', '0'] estão dentro · meio ['3', '4'] está FORA" in texto


def test_a_assimetria_do_teste(texto):
    """15 pares refutam; 12.561 não provam. É a tese metodológica do capítulo."""
    convexa = teste_do_ponto_medio(regiao_convexa, "a")
    disjuntiva = teste_do_ponto_medio(regiao_disjuntiva, "b")
    assert disjuntiva["pares_testados"] < convexa["pares_testados"] / 100
    assert disjuntiva["pares_testados"] == 15
    assert "15" in texto and "12.561" in texto


def test_o_otimo_local_que_nao_e_global(texto, exercicios):
    """Os dois números do capítulo E da rubrica do cap38.exB, refeitos do zero."""
    a = busca_local(regiao_disjuntiva, (F(0), F(8)))
    b = busca_local(regiao_disjuntiva, (F(6), F(0)))
    assert (a["parou_em"], a["lucro"]) == (["2", "8"], "22")
    assert (b["parou_em"], b["lucro"]) == (["10", "0"], "30")
    assert melhor_da_grade(regiao_disjuntiva) == {"ponto": ["10", "0"], "lucro": "30"}

    assert "partindo de ['0', '8']: para em ['2', '8'] com lucro 22" in texto

    # A rubrica do exercício depende destes mesmos números — e é o único lugar
    # onde eles são conferidos, porque o portão de ótimo do livro não alcança
    # região não convexa.
    rubrica = " ".join([exercicios["cap38.exB"]["resposta_guia"],
                        *exercicios["cap38.exB"]["criterios"]])
    assert "(2,8)" in rubrica.replace("$", "").replace(" ", "")
    assert exercicios["cap38.exB"]["enunciado"].count("22") >= 1
    assert exercicios["cap38.exB"]["enunciado"].count("30") >= 1


def test_o_ponto_de_parada_e_mesmo_um_otimo_local():
    """A afirmação central do exercício B: em (2,8) NENHUM vizinho é melhor.

    Sem isto, o exercício estaria acusando a busca de ter errado — e a lição
    inteira depende de ela não ter errado.
    """
    passo = F(1, 2)
    atual = (F(2), F(8))
    vizinhos = [(atual[0] + dx, atual[1] + dy)
                for dx in (-passo, F(0), passo) for dy in (-passo, F(0), passo)
                if (dx, dy) != (F(0), F(0))]
    melhores = [v for v in vizinhos if regiao_disjuntiva(*v) and lucro(v) > lucro(atual)]
    assert melhores == [], f"(2,8) não é ótimo local — há vizinho melhor: {melhores}"


def test_a_isencao_no_portao_aponta_para_ca():
    """O portão de ótimo isenta os três exercícios do 38; a isenção tem de existir.

    Se alguém tirar a isenção sem trazer os números para um modelo conferível, o
    build fica vermelho — e é o que se quer. Se alguém tirar ESTE teste, a
    isenção lá vira um buraco silencioso, e é isso que esta asserção impede.
    """
    portao = (RAIZ / "publicar/verifica-otimos.mjs").read_text(encoding="utf-8")
    for id_ in ("cap38.exA", "cap38.exB", "cap38.exC"):
        assert f'"{id_}"' in portao, f"{id_} deixou de estar isento — traga o modelo ou reponha a isenção"
    assert "etapa-06-convexidade" in portao, "a isenção precisa apontar para onde a conferência acontece"
