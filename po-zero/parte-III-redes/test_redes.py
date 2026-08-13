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


# ===========================================================================
# CAPÍTULO 18 — a árvore, e o mesmo gesto no problema ao lado
# ===========================================================================

from redes import (CIDADES, REDE, fluxo_maximo, kruskal, mst_por_enumeracao,  # noqa: E402
                   tsp_exato, tsp_guloso)

CAP18 = RAIZ / "livro/capitulos/18-arvore-geradora.md"
CAP19 = RAIZ / "livro/capitulos/19-fluxo-maximo.md"


@pytest.fixture(scope="module")
def texto18():
    return CAP18.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def texto19():
    return CAP19.read_text(encoding="utf-8")


def test_a_arvore_minima_confere_por_dois_caminhos():
    """Kruskal e a enumeração de TODAS as árvores geradoras chegam ao mesmo custo.

    É a disciplina do capítulo 12 aplicada aqui: chegar ao mesmo número por dois
    caminhos é o que separa medição de coincidência. Se algum dia divergirem, o
    defeito está no guloso — e é exatamente isso que o capítulo 18 afirma que
    não pode acontecer.
    """
    k, e = kruskal(CIDADES), mst_por_enumeracao(CIDADES)
    assert k["custo"] == e["custo"] == "17"
    assert len(k["arestas"]) == 4, "cinco cidades pedem exatamente n−1 = 4 ligações"


def test_o_custo_da_arvore_esta_no_capitulo(texto18):
    assert f"**Custo total: {kruskal(CIDADES)['custo']}.**" in texto18


def test_o_guloso_perde_no_roteiro():
    """A afirmação que o capítulo 18 existe para fazer — e que quase não se sustentou.

    A primeira instância foi escolhida à mão e o guloso ACERTOU o roteiro nela.
    Esta saiu de busca com semente declarada. Se alguém trocar a instância por
    uma "mais limpa", este teste avisa que a tese caiu junto.
    """
    g, e = tsp_guloso(CIDADES, "a"), tsp_exato(CIDADES, "a")
    assert F(g["custo"]) > F(e["custo"]), "o guloso parou de errar — o capítulo 18 perdeu a tese"
    assert g["custo"] == "32" and e["custo"] == "28"


def test_a_tabela_do_roteiro_esta_no_capitulo(texto18):
    g, e = tsp_guloso(CIDADES, "a"), tsp_exato(CIDADES, "a")
    assert f"`{' → '.join(g['rota'])}` | **{g['custo']}** |" in texto18
    assert f"`{' → '.join(e['rota'])}` | **{e['custo']}** |" in texto18
    perda = F(g["custo"]) / F(e["custo"]) - 1
    pct = f"{float(perda) * 100:.1f}".replace(".", ",")
    assert f"{pct}%" in texto18, f"a perda publicada não confere: medida {pct}%"


def test_o_capitulo_18_registra_como_a_instancia_foi_obtida(texto18):
    """Sem isto, a instância parece desenhada para dar o resultado que dá."""
    assert "4.000" in texto18 and "semente" in texto18
    assert "ele acertou" in texto18


# ===========================================================================
# CAPÍTULO 19 — a igualdade, exibida
# ===========================================================================

def test_o_fluxo_maximo_iguala_o_corte_minimo():
    f = fluxo_maximo(REDE, "fabrica", "mercado")
    assert f["bate"] is True
    assert f["fluxo"] == f["corte"]["capacidade"] == "15"


def test_o_corte_publicado_confere(texto19):
    f = fluxo_maximo(REDE, "fabrica", "mercado")
    assert len(f["corte"]["arestas"]) == 3
    for u, v, c in f["corte"]["arestas"]:
        assert f"| `{u} → {v}` | {c} |" in texto19, f"a aresta do corte {u}→{v} não confere"
    assert f"| **Total** | **{f['corte']['capacidade']}** |" in texto19
    assert f"**Fluxo máximo medido: {f['fluxo']}.**" in texto19


def test_o_corte_nao_e_uma_camada_da_rede():
    """A afirmação de gestão do capítulo: gargalo é conjunto, não etapa.

    Se o corte medido virasse "todas as arestas que saem da fábrica" ou "todas
    as que entram no mercado", a lição do capítulo cairia — e a tabela de
    propostas do exercício B deixaria de fazer sentido.
    """
    f = fluxo_maximo(REDE, "fabrica", "mercado")
    origens = {u for u, _, _ in f["corte"]["arestas"]}
    destinos = {v for _, v, _ in f["corte"]["arestas"]}
    assert len(origens) > 1, "o corte virou uma camada só de saída"
    assert len(destinos) > 1, "o corte virou uma camada só de chegada"


def test_a_aresta_de_maior_capacidade_nao_esta_no_corte(texto19):
    """`fabrica → centro_norte` tem 10 e sobra folga — investir nela não muda nada."""
    f = fluxo_maximo(REDE, "fabrica", "mercado")
    no_corte = {(u, v) for u, v, _ in f["corte"]["arestas"]}
    assert ("fabrica", "centro_norte") not in no_corte
    assert "**Investir numa aresta fora do corte não muda nada.**" in texto19


def test_o_capitulo_19_diz_que_exibe_e_nao_demonstra(texto19):
    """A honestidade que separa medir um caso de provar um teorema."""
    assert "não prova" in texto19 and "exibe" in texto19


def test_as_baterias_de_18_e_19_existem(exercicios):
    assert len([e for e in exercicios if e.startswith("cap18.")]) >= 3
    assert len([e for e in exercicios if e.startswith("cap19.")]) >= 3
