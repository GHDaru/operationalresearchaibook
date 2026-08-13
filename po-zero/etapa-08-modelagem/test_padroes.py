"""O capítulo 15 e a sua bateria têm de bater com a medição.

ESTE ARQUIVO FECHA UM BURACO CONHECIDO DO PORTÃO DE ÓTIMO, e vale dizer qual,
porque um controle compensatório que ninguém sabe que existe não compensa nada.

O `verifica-otimos.mjs` tem duas limitações, e as duas se aplicam aqui:

  1. Ele só resolve modelos de **duas variáveis** — o transporte tem seis, a
     cobertura tem quatro.
  2. Ele só olha rubricas que contenham a palavra "ótimo". As rubricas do
     capítulo 15 afirmam custos (365, 403,33, 9, 10) **sem** usar a palavra, e
     por isso passariam despercebidas. Isso não é defeito do portão: é o alcance
     dele, e o alcance está declarado.

Então a conferência acontece aqui, sobre o capítulo publicado E sobre a rubrica.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

import pytest

from padroes import (cobertura, mistura, transporte,
                     transporte_com_padrao_errado)

RAIZ = Path(__file__).resolve().parents[2]
CAPITULO = RAIZ / "livro/capitulos/15-modelagem-aplicada.md"


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def exercicios():
    return {e["id"]: e for e in json.loads((RAIZ / "livro/exercicios.json").read_text(encoding="utf-8"))}


def test_mistura(texto):
    m = mistura()
    assert m["status"] == "otimo"
    assert m["ponto"] == ["180/17", "48/17"]
    assert m["valor"] == "780/17"
    assert "['180/17', '48/17']" in texto and "780/17" in texto


def test_transporte(texto):
    t = transporte()
    assert t["status"] == "otimo"
    assert dict(zip(t["rotulos"], t["ponto"])) == {
        "x11": "20", "x12": "0", "x13": "10", "x21": "0", "x22": "25", "x23": "15"}
    assert t["valor"] == "365"
    assert "custo 365" in texto


def test_o_padrao_errado_custa_mais_e_perde_o_destino(texto, exercicios):
    """Os dois danos: o custo maior e a informação que deixou de existir."""
    t, e = transporte(), transporte_com_padrao_errado()
    assert e["status"] == "otimo"
    assert e["valor"] == "1210/3"
    dif = F(e["valor"]) - F(t["valor"])
    assert dif == F(115, 3)

    # O dano estrutural, verificado e não apenas afirmado: o modelo errado tem
    # DUAS variáveis, uma por fábrica, e portanto não pode informar destino.
    assert len(e["ponto"]) == 2
    assert len(t["ponto"]) == 6

    assert "1210/3" in texto and "115/3" in texto
    # A porcentagem publicada no capítulo e na rubrica: ~10,5%.
    pct = float(dif / F(t["valor"])) * 100
    assert 10.4 < pct < 10.6, f"a porcentagem publicada não bate: {pct:.2f}%"
    assert "10,5%" in texto
    assert "10,5%" in " ".join(exercicios["cap15.exB"]["criterios"])


def test_cobertura_relaxada_e_fracionaria_e_o_buraco_e_estrito(texto, exercicios):
    """A porta de entrada da programação inteira, medida em vez de anunciada."""
    c = cobertura()
    assert c["status"] == "otimo"
    assert c["ponto"] == ["1/2", "1/2", "1/2", "1/2"]
    assert c["valor"] == "9"
    assert c["fracionaria"]
    # A decisão executável, por enumeração dos 16 subconjuntos.
    assert c["inteira"] == {"estacoes": [2, 3], "custo": "10"}
    assert F(c["buraco"]) == 1

    for agulha in ("['1/2', '1/2', '1/2', '1/2']", "custo 9", "estações [2, 3]"):
        assert agulha in texto, f"o capítulo não publica: {agulha}"

    rubrica = " ".join([exercicios["cap15.exC"]["resposta_guia"],
                        *exercicios["cap15.exC"]["criterios"]])
    assert "10" in rubrica and "9" in rubrica
    # O arredondar-para-cima que o exercício afirma custar 18.
    assert "18" in rubrica
    assert sum([5, 4, 6, 3]) == 18


def test_a_relaxacao_e_mesmo_limitante_inferior():
    """A afirmação teórica do capítulo, conferida na instância.

    Toda decisão binária é viável no problema relaxado, logo o custo relaxado
    nunca supera o real. Aqui isso é conferido — e conferido ESTRITO, porque um
    buraco de zero não teria lição.
    """
    c = cobertura()
    assert F(c["valor"]) < F(c["inteira"]["custo"])


def test_nenhum_padrao_precisou_de_metodo_novo():
    """A tese de engenharia do capítulo: o repertório é de FORMULAÇÃO.

    Os três padrões saem do mesmo `quadro.resolver` da etapa 03, sem alteração.
    Se algum dia esta etapa passar a importar um solver próprio, este teste
    quebra — e é o que se quer, porque a tese do capítulo teria caído.
    """
    fonte = (Path(__file__).parent / "padroes.py").read_text(encoding="utf-8")
    assert "from quadro import" in fonte
    assert "etapa-03-simplex" in fonte
    for proibido in ("import scipy", "import pulp", "from scipy", "linprog"):
        assert proibido not in fonte, f"a etapa passou a usar solver externo: {proibido}"
