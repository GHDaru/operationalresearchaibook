"""Os capítulos medidos da Parte III têm de bater com a medição.

Por enquanto o vínculo cobre o **capítulo 17**; os demais entram conforme forem
publicados, e o portão de maturidade cobra: capítulo 🔵 sem teste que leia o
`.md` dele falha o build.

O vínculo é feito nas duas direções, e no capítulo 17 há uma terceira coisa a
prender, que é a mais importante: **a incoerência interna da saída de Dijkstra**.
Se alguém "consertar" a implementação para se defender de peso negativo, o
contraexemplo do capítulo desaparece e o texto passa a descrever algo que não
acontece mais. O teste abaixo falha nesse caso — de propósito.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

import pytest

from redes import (COM_CICLO_NEGATIVO, COM_PESO_NEGATIVO, MALHA, bellman_ford,
                   caminho, dijkstra)

RAIZ = Path(__file__).resolve().parents[2]
CAP17 = RAIZ / "livro/capitulos/17-caminho-minimo.md"


@pytest.fixture(scope="module")
def texto17():
    return CAP17.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def exercicios():
    return {e["id"]: e for e in json.loads((RAIZ / "livro/exercicios.json").read_text(encoding="utf-8"))}


# --- a malha honesta: os dois métodos concordam ----------------------------

def test_na_malha_honesta_os_dois_concordam():
    """Quando a hipótese de Dijkstra vale, a concordância é o modo de conferir."""
    d, b = dijkstra(MALHA, "deposito"), bellman_ford(MALHA, "deposito")
    assert d["distancias"] == b["distancias"]
    assert not b["ciclo_negativo"]


@pytest.mark.parametrize("no,valor", [("sul", 2), ("norte", 3), ("leste", 8),
                                      ("oeste", 10), ("cliente", 11)])
def test_a_tabela_da_malha_esta_no_capitulo(texto17, no, valor):
    d = dijkstra(MALHA, "deposito")
    assert d["distancias"][no] == F(valor), f"a medição mudou para {no}"
    assert f"| `{no}` | **{valor}** |" in texto17, f"a linha de {no} não confere com a medição"


def test_o_caminho_publicado_confere(texto17):
    trilha = caminho(dijkstra(MALHA, "deposito"), "cliente")
    assert trilha == ["deposito", "sul", "norte", "leste", "cliente"]
    assert " → ".join(f"`{x}`" for x in trilha) in texto17 or \
           "`deposito → sul → norte → leste → cliente`" in texto17


# --- o contraexemplo, que é o coração do capítulo --------------------------

def test_dijkstra_erra_com_peso_negativo():
    d, b = dijkstra(COM_PESO_NEGATIVO, "A"), bellman_ford(COM_PESO_NEGATIVO, "A")
    assert d["distancias"]["D"] == F(6)
    assert b["distancias"]["D"] == F(4)


def test_a_saida_de_dijkstra_contradiz_a_si_mesma():
    """A afirmação mais forte do capítulo 17, e a que mais fácil se perderia.

    Não basta Dijkstra errar o número: o capítulo afirma que ele devolve um
    número **e** um caminho que não fecham entre si. Se alguém defender a
    implementação contra peso negativo, isto fica vermelho — que é o certo,
    porque aí o texto estaria descrevendo algo que não acontece mais.
    """
    d = dijkstra(COM_PESO_NEGATIVO, "A")
    trilha = caminho(d, "D")
    peso = {(u, v): c for u, v, c in COM_PESO_NEGATIVO}
    custo_do_caminho = sum(peso[(a, b)] for a, b in zip(trilha, trilha[1:]))
    assert custo_do_caminho == F(4), "o caminho devolvido deixou de custar 4"
    assert d["distancias"]["D"] != custo_do_caminho, \
        "Dijkstra parou de se contradizer — o contraexemplo do capítulo 17 morreu"


def test_a_tabela_do_contraexemplo_esta_no_capitulo(texto17):
    d, b = dijkstra(COM_PESO_NEGATIVO, "A"), bellman_ford(COM_PESO_NEGATIVO, "A")
    assert f"| **Dijkstra** | **{d['distancias']['D']}** | `A → C → B → D` |" in texto17
    assert f"| **Bellman-Ford** | **{b['distancias']['D']}** | `A → C → B → D` |" in texto17
    assert caminho(d, "D") == ["A", "C", "B", "D"]


def test_o_capitulo_explica_o_passo_em_que_a_informacao_se_perde(texto17):
    """Sem o passo a passo, o contraexemplo vira curiosidade em vez de lição."""
    assert "já está fechado" in texto17
    assert "nunca é recalculado" in texto17


# --- o veredito que Bellman-Ford dá e Dijkstra não tem como dar ------------

def test_bellman_ford_detecta_ciclo_negativo():
    assert bellman_ford(COM_CICLO_NEGATIVO, "A")["ciclo_negativo"] is True


def test_o_capitulo_publica_o_veredito(texto17):
    assert "ciclo negativo" in texto17.lower()
    assert "caminho arbitrariamente barato" in texto17


# --- a bateria -------------------------------------------------------------

def test_a_bateria_do_capitulo_17_existe(exercicios):
    assert len([e for e in exercicios if e.startswith("cap17.")]) >= 3
