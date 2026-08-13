"""O capítulo 13 tem de bater com a medição — mesma disciplina do `test_dual.py`.

A regra que este arquivo cumpre está na [ADR 0014](../../adr/0014-relatorio-de-sensibilidade-e-a-faixa-medida.md),
D3: número no livro tem dono, e o dono é um teste. Não existe número publicado
neste handbook que só o autor confira.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path

import pytest

from dual import montadora
from sensibilidade import (derivadas, dual_viavel, montadora_com_bancada,
                           precos_na_ordem, relatorio)

CAPITULO = Path(__file__).resolve().parents[2] / "livro/capitulos/13-sensibilidade.md"


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rel():
    lucros, restricoes, ficha = montadora()
    produtos = [ficha["produtos"][p]["rotulo"] for p in ficha["produtos"]]
    return relatorio(lucros, restricoes, produtos)


def test_relatorio_publicado_bate_com_o_medido(rel, texto):
    """Cada célula do relatório impresso no capítulo sai da medição."""
    esperado_var = {"Tipo 1 (16 GB)": ("8", "100", "75", "150"),
                    "Tipo 2 (32 GB)": ("2", "150", "100", "200")}
    for v in rel["variaveis"]:
        assert (v["produzir"], v["lucro_unitario"],
                v["lucro_pode_cair_ate"], v["lucro_pode_subir_ate"]) == esperado_var[v["produto"]]

    esperado_res = {"CPUs": ("10", "10", "50", "6", "12"),
                    "pentes de memória de 16 GB": ("12", "12", "50", "10", "20")}
    for c in rel["restricoes"]:
        assert (c["estoque"], c["usado"], c["preco_sombra"],
                c["estoque_pode_cair_ate"], c["estoque_pode_subir_ate"]) == esperado_res[c["recurso"]]

    # E o bloco impresso no capítulo contém as linhas, com os números na ordem.
    for linha in ("Tipo 1 (16 GB)                 8      100              75             150",
                  "Tipo 2 (32 GB)                 2      150             100             200",
                  "CPUs                                   10      10      50               6              12"):
        assert linha in texto, f"o capítulo não publica a linha medida:\n{linha}"


def test_as_duas_leituras_do_vertice_degenerado():
    """Mesma implementação, ordem diferente, preços diferentes — e todos válidos."""
    lucros, restricoes = montadora_com_bancada()
    a = precos_na_ordem(lucros, restricoes, [0, 1, 2])
    b = precos_na_ordem(lucros, restricoes, [2, 1, 0])

    # O plano e o lucro NÃO podem mudar: se mudassem, o exemplo não seria de
    # ambiguidade de preço — seria de modelo diferente.
    assert a["ponto"] == b["ponto"] == ["8", "2"]
    assert a["valor"] == b["valor"] == "1100"
    assert a["precos"] != b["precos"], "sem divergência não há o que demonstrar"
    assert a["precos"]["CPUs"] == "50" and b["precos"]["CPUs"] == "0"


def test_os_precos_alternativos_sao_todos_duais_viaveis():
    """O árbitro: se os dois relatórios são válidos, ninguém errou."""
    lucros, restricoes = montadora_com_bancada()
    for y in ([F(50), F(50), F(0)], [F(0), F(75), F(25)], [F(25), F(125, 2), F(25, 2)]):
        c = dual_viavel(lucros, restricoes, y)
        assert c["viavel"], f"{c['y']} não é dual viável"
        assert F(c["custo"]) == 1100


def test_derivada_pela_esquerda_e_pela_direita_divergem(texto):
    """O fato que desfaz a pergunta 'qual é O preço'."""
    lucros, restricoes = montadora_com_bancada()
    d = derivadas(lucros, restricoes, 0)
    assert (d["z_menos_um"], d["z"], d["z_mais_um"]) == ("1050", "1100", "1100")
    assert d["derivada_pela_esquerda"] == "50"
    assert d["derivada_pela_direita"] == "0"
    assert not d["coincidem"]
    assert "z(9) = 1050 · z(10) = 1100 · z(11) = 1100" in texto


def test_a_faixa_do_lucro_nao_muda_o_plano():
    """A promessa que a faixa do coeficiente faz, conferida resolvendo de novo.

    A faixa do Tipo 1 é [75, 150], e a promessa tem TRÊS regimes — o do meio é o
    que quase todo texto omite, e foi este teste que o cobrou:

      - ESTRITAMENTE dentro: o plano é o mesmo, e é o único ótimo;
      - NA fronteira: o plano continua ótimo, mas EMPATA com outro. Em c₁ = 75,
        (8,2) e (0,6) rendem os dois 900, e qual deles o método devolve é
        decidido pela regra de pivoteamento — o capítulo 10 já tinha avisado.
        Exigir igualdade de ponto aqui seria testar a regra, não a faixa;
      - FORA: o plano deixa de ser ótimo.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "etapa-03-simplex"))
    from quadro import resolver

    lucros, restricoes, _ = montadora()
    plano = [F(v) for v in resolver(lucros, restricoes)["ponto"]]
    vale = lambda c1: c1 * plano[0] + lucros[1] * plano[1]
    otimo = lambda c1: F(resolver([c1, lucros[1]], restricoes)["valor"])

    for dentro in (F(76), F(100), F(149)):
        assert resolver([dentro, lucros[1]], restricoes)["ponto"] == ["8", "2"]
    for fronteira in (F(75), F(150)):
        assert vale(fronteira) == otimo(fronteira), "na fronteira o plano tem de seguir ótimo"
    for fora in (F(74), F(151)):
        assert vale(fora) < otimo(fora), "fora da faixa o plano tem de deixar de ser ótimo"
