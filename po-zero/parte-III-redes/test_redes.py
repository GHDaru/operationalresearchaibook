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


# ===========================================================================
# CAPÍTULOS 20, 21 e 22 — integralidade, designação e o viés do PERT
# ===========================================================================

from redes import (AMOSTRAS_PERT, CUSTO, DEMANDA, EQUIPE, FAIXAS, OFERTA,  # noqa: E402
                   PROJETO, SEMENTE, caminho_critico, designacao,
                   pert_pela_formula, pert_por_simulacao, transporte,
                   transporte_com_estrutura_quebrada, varredura_de_ramos)

CAP20 = RAIZ / "livro/capitulos/20-fluxo-custo-minimo.md"
CAP21 = RAIZ / "livro/capitulos/21-transporte-designacao.md"
CAP22 = RAIZ / "livro/capitulos/22-pert-cpm.md"


@pytest.fixture(scope="module")
def texto20():
    return CAP20.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def texto21():
    return CAP21.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def texto22():
    return CAP22.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def transp():
    return transporte(OFERTA, DEMANDA, CUSTO)


def test_a_relaxacao_do_transporte_sai_inteira(transp):
    """O resultado mais útil da Parte III: integralidade sem pedir integralidade."""
    assert transp["status"] == "Optimal"
    assert transp["todos_inteiros"] is True, "a integralidade de graça sumiu"
    assert transp["fracionarios"] == {}


def test_o_plano_e_o_custo_estao_no_capitulo(texto20, transp):
    assert f"| **Custo** | **{transp['custo']:g}** |" in texto20
    for rota, q in transp["plano"].items():
        if q:
            o, d = rota.split("->")
            assert f"| `{o} → {d}` | **{q:g}** |" in texto20, f"a rota {rota} não confere"


def test_uma_restricao_transversal_quebra_a_integralidade(texto20):
    """O outro lado da moeda, e a lição do capítulo: a garantia é da FORMA.

    O `assert` de status vive dentro da própria função — um experimento que
    não confere o próprio veredito mede outra coisa, e a primeira versão deste
    aqui produzia um modelo inviável sem que ninguém notasse.
    """
    q = transporte_com_estrutura_quebrada()
    assert q["status"] == "Optimal"
    assert q["todos_inteiros"] is False
    assert len(q["fracionarios"]) == 4
    assert f"| Custo ótimo | **220** | **{q['custo']:.2f}".replace(".", ",")[:34] in texto20 or \
           "223,33" in texto20
    for rota, v in q["fracionarios"].items():
        o, d = rota.split("->")
        assert f"`{o} → {d}`" in texto20, f"o fracionário {rota} não aparece no capítulo"


# --- capítulo 21 -----------------------------------------------------------

def test_a_designacao_sai_binaria_sem_variavel_binaria(texto21):
    d = designacao(EQUIPE)
    assert d["status"] == "Optimal"
    assert d["todos_binarios"] is True, "a designação deixou de sair 0/1"
    assert d["custo"] == 9
    assert f"| **Custo total** | **{d['custo']:g}** |" in texto21
    for par in d["escolhidos"]:
        p, t = par.split("->")
        assert f"| `{p} → {t}` | 1 |" in texto21, f"a designação {par} não confere"


def test_o_codigo_da_designacao_nao_declara_binaria():
    """A afirmação central do capítulo 21, verificada no FONTE e não na saída.

    Se alguém acrescentar `cat="Binary"` ao modelo, a saída continua 0/1 e o
    capítulo passa a mentir — porque a lição não é que a resposta é binária, é
    que ela é binária **sem ter sido pedida**.
    """
    fonte = (RAIZ / "po-zero/parte-III-redes/redes.py").read_text(encoding="utf-8")
    corpo = fonte[fonte.index("def designacao("):fonte.index("EQUIPE = {")]
    # A docstring da própria função CITA `cat="Binary"` para desaconselhá-la, então
    # procurar a palavra no arquivo inteiro daria falso vermelho. O que interessa é
    # o código: as linhas que não são comentário nem docstring.
    dentro, linhas = False, []
    for linha in corpo.split("\n"):
        if linha.count('"""') == 1:
            dentro = not dentro
            continue
        if dentro or linha.lstrip().startswith("#"):
            continue
        linhas.append(linha)
    codigo = "\n".join(linhas)
    assert "Binary" not in codigo and "LpInteger" not in codigo, \
        "o modelo de designação passou a declarar variável binária — o capítulo 21 perdeu a tese"
    assert "upBound=1" in codigo


# --- capítulo 22 -----------------------------------------------------------

def test_o_caminho_critico_e_as_folgas_conferem(texto22):
    c = caminho_critico(PROJETO)
    assert c["duracao"] == "18"
    assert c["criticas"] == ["backend", "especificar", "integrar"]
    assert c["folga"]["frontend"] == "3"
    assert f"**Duração do projeto: {c['duracao']}.**" in texto22
    assert f"| `frontend` | **{c['folga']['frontend']}** |" in texto22


@pytest.fixture(scope="module")
def pert():
    f = pert_pela_formula(FAIXAS, PROJETO)
    s = pert_por_simulacao(FAIXAS, PROJETO, f["criticas"], AMOSTRAS_PERT, SEMENTE)
    return f, s


def test_a_formula_subestima_e_o_capitulo_publica_quanto(texto22, pert):
    f, s = pert
    assert f["duracao_esperada"] == "21"
    assert f"**A fórmula publica {f['duracao_esperada']} dias**" in texto22
    media = f"{s['projeto']['media']:.2f}".replace(".", ",")
    assert f"**{media}**" in texto22, f"a média simulada não confere: {media}"
    pct = f"{s['prob_de_estourar_a_estimativa_do_pert'] * 100:.1f}".replace(".", ",")
    assert f"**{pct}%**" in texto22, f"a probabilidade de estouro não confere: {pct}%"


def test_o_vies_isolado_confere(texto22, pert):
    """O número que a honestidade custou: 0,49 e não os ~3,5 da comparação ingênua."""
    _, s = pert
    vies = f"{s['merge_bias']:.2f}".replace(".", ",")
    assert f"**{vies}**" in texto22, f"o viés isolado não confere: {vies}"
    so = f"{s['so_o_caminho_declarado']['media']:.2f}".replace(".", ",")
    assert so in texto22, "a média do caminho declarado não confere"


def test_o_controle_de_um_ramo_da_exatamente_zero(texto22):
    """O número mais importante da tabela, apesar de ser zero.

    Sem paralelismo a duração do projeto É a do caminho declarado, então o viés
    não pode existir. Dar exatamente zero é o que prova que a isolação está
    correta — qualquer outro valor indicaria defeito no experimento, não no PERT.
    """
    v = varredura_de_ramos()
    controle = [x for x in v if x["ramos"] == 1][0]
    assert controle["merge_bias"] == 0.0, "o controle deixou de dar zero — a isolação quebrou"
    for linha in v:
        vies = f"{linha['merge_bias']:.2f}".replace(".", ",").rstrip("0").rstrip(",") \
            if linha["merge_bias"] else "0,0"
        assert f"| {vies} |" in texto22 or f"| **{vies}** |" in texto22, \
            f"a linha de {linha['ramos']} ramo(s) não confere: viés {linha['merge_bias']}"


def test_o_capitulo_22_separa_as_duas_causas(texto22):
    """Sem esta separação declarada, o capítulo publicaria um número inflado."""
    assert "duas causas" in texto22
    assert "nas mesmas amostras" in texto22.lower()
    assert "só uma é defeito do método" in texto22


def test_as_baterias_de_20_a_22_existem(exercicios):
    for cap in ("cap20.", "cap21.", "cap22."):
        assert len([e for e in exercicios if e.startswith(cap)]) >= 3
