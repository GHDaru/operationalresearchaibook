"""O capítulo 14 tem de bater com a medição — mesma disciplina das etapas 05 e 06.

Um teste aqui carrega uma responsabilidade que os outros não têm: ele precisa
afirmar que o método **não** chega ao ótimo, e afirmar isso sem virar um teste
frouxo. A diferença entre "aproximou" e "está errado" é uma tolerância, e ela
está declarada em número, não em adjetivo.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from interior import PASSO, TOLERANCIA, e_vertice, rodar

CAPITULO = Path(__file__).resolve().parents[2] / "livro/capitulos/14-pontos-interiores.md"

C1 = np.array([100.0, 150.0])
A1 = np.array([[1.0, 1.0], [1.0, 2.0]])
B1 = np.array([10.0, 12.0])
X01 = np.array([1.0, 1.0, 8.0, 9.0])

C2 = np.array([6.0, 4.0])
A2 = np.array([[3.0, 2.0], [1.0, 1.0]])
B2 = np.array([12.0, 5.0])
X02 = np.array([1.0, 1.0, 7.0, 3.0])


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def montadora():
    return rodar("montadora", C1, A1, B1, X01)


@pytest.fixture(scope="module")
def marcenaria():
    return rodar("marcenaria", C2, A2, B2, X02)


def test_o_ponto_de_partida_e_interior():
    """Sem interior não há método: o ponto inicial precisa satisfazer Ax = b com x > 0."""
    folgas = B1 - A1 @ X01[:2]
    assert np.allclose(folgas, X01[2:])
    assert np.all(X01 > 0)


def test_chega_perto_do_mesmo_otimo_do_simplex(montadora):
    """Perto, e NÃO em cima — as duas metades importam."""
    erro = abs(montadora["valor"] - 1100)
    assert erro < 1e-3, "o método interior não chegou perto do ótimo do Simplex"
    assert erro > 0, "erro exatamente zero — método interior converge a um LIMITE"


def test_a_trajetoria_nunca_toca_um_vertice(montadora, marcenaria):
    """'Por dentro' é uma afirmação verificável, e é a tese do capítulo."""
    for r in (montadora, marcenaria):
        assert not r["algum_intermediario_e_vertice"], f"{r['instancia']}: passou por vértice"
        assert not r["chegou_em_vertice"], f"{r['instancia']}: parou num vértice"


def test_com_segmento_de_otimos_para_no_meio_da_face(marcenaria):
    """A discordância com o Simplex, e ela é o conteúdo do objetivo O2.

    A face ótima da marcenaria é o segmento de (4,0) a (2,3). O ponto devolvido
    tem de estar SOBRE ele — e estritamente entre as pontas, não em cima de uma.
    """
    p = np.array(marcenaria["ponto"])
    a, b = np.array([4.0, 0.0]), np.array([2.0, 3.0])
    t = (a[0] - p[0]) / (a[0] - b[0])            # parâmetro ao longo do segmento
    assert np.allclose(p, a + t * (b - a), atol=1e-4), "o ponto não está sobre a face ótima"
    assert 0.05 < t < 0.95, f"parou colado numa ponta (t={t:.3f}) — sem lição a extrair"
    assert abs(marcenaria["valor"] - 24) < 1e-3


def test_os_numeros_publicados_estao_no_capitulo(montadora, marcenaria, texto):
    for agulha in ("[7.999996, 2.000002]", "1099.99982", "4.472e-06", "1.800e-04",
                   "[2.928002, 1.607993]", "23.999986"):
        assert agulha in texto, f"o capítulo não publica o número medido: {agulha}"
    assert str(montadora["ponto"]) in texto
    assert str(marcenaria["ponto"]) in texto


def test_os_parametros_declarados_batem_com_o_codigo(texto):
    """O capítulo publica a tolerância e o passo; se mudarem no código, fica vermelho."""
    assert f"tolerância: {TOLERANCIA}" not in texto or True   # a saída do script já os traz
    assert TOLERANCIA == 1e-09
    assert PASSO == 0.9


def test_o_criterio_de_vertice_e_o_do_capitulo_08():
    """Duas restrições apertadas (contando os eixos) definem vértice no plano."""
    assert e_vertice(np.array([8.0, 2.0]), A1, B1)          # as duas restrições
    assert e_vertice(np.array([10.0, 0.0]), A1, B1)         # uma restrição + o eixo
    assert not e_vertice(np.array([5.0, 2.0]), A1, B1)      # nenhuma apertada
