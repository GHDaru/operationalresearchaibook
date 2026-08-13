"""Os capítulos medidos da Parte III têm de bater com a medição.

Por enquanto o vínculo cobre o **capítulo 17**; os demais entram conforme forem
publicados, e o portão de maturidade cobra: capítulo 🔵 sem teste que leia o
`.md` dele falha o build.

O vínculo é feito nas duas direções, e no capítulo 17 há uma terceira coisa a
prender: **a discordância entre três variantes de mesmo nome**. Uma erra de
forma coerente, uma devolve saída que contradiz a si mesma, e uma acerta por
acidente — e é a existência das três que sustenta a lição do capítulo.

Aqui houve uma correção de rumo que vale registrar, porque ela é sobre teste e
não sobre conteúdo. A versão anterior desta suíte exigia que `dijkstra()`
**contradissesse a si mesma**, e a contradição vinha de um `if` que faltava na
implementação. O teste, escrito para impedir que o contraexemplo morresse,
acabou **trancando um defeito** e obrigando o capítulo a descrevê-lo como
propriedade do método. Um teste pode preservar um erro com o mesmo zelo com que
preservaria um acerto: o que ele garante é estabilidade, não verdade.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

import pytest

from redes import (COM_CICLO_NEGATIVO, COM_PESO_NEGATIVO, MALHA, as_tres_variantes,
                   bellman_ford, caminho, dijkstra, o_que_uma_biblioteca_faz)

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


def test_as_tres_variantes_de_dijkstra_discordam(texto17):
    """O que o capítulo 17 afirma DEPOIS da revisão — e por que ele mudou.

    A versão anterior deste teste travava um artefato. Ele exigia que a saída
    de `dijkstra()` **contradissesse a si mesma**, e a contradição vinha de um
    `if` que faltava: a relaxação escrevia em nó já fechado. O capítulo
    publicava isso como propriedade do método, e não é — nenhuma implementação
    de referência reproduz o sintoma.

    O que se mede agora é mais forte e é verdade: três variantes de mesmo nome
    dão **três respostas diferentes** assim que a hipótese cai. Se alguma delas
    passar a concordar com as outras, este teste fica vermelho — e aí é a
    tabela do capítulo que precisa mudar, não o teste.
    """
    v = {r["variante"]: r for r in as_tres_variantes(COM_PESO_NEGATIVO, "A", "D")}

    canonica = v["com guarda (canônica)"]
    assert canonica["distancia"] == "6", "a canônica deixou de errar"
    assert canonica["contradiz_a_si_mesma"] is False, \
        "a versão canônica voltou a se contradizer — a guarda do nó fechado sumiu"

    sem = v["sem guarda"]
    assert sem["distancia"] == "6" and sem["custo_do_caminho"] == "4"
    assert sem["contradiz_a_si_mesma"] is True

    fila = v["com fila de prioridade"]
    assert fila["acerta"] is True, "a variante de fila deixou de acertar por acidente"

    # e as três linhas têm de estar na tabela publicada
    for r in v.values():
        assert f"| **{r['distancia']}** |" in texto17
    assert "Acerta — por acidente" in texto17


def test_a_biblioteca_consagrada_avisa(texto17):
    """O que derrubou a frase "não há erro, não há aviso, não há exceção".

    Era falsa, e de um jeito conferível: a `networkx` levanta exceção nesta
    mesma instância. O capítulo passou a publicar a versão e a mensagem, então
    o teste prende as duas.
    """
    r = o_que_uma_biblioteca_faz(COM_PESO_NEGATIVO, "A")
    assert r["avisa"] is True, \
        "a networkx parou de avisar — a ressalva do capítulo 17 precisa mudar"
    assert r["excecao"] == "ValueError"
    assert f"`networkx` (versão {r['versao']})" in texto17, \
        "a versão da biblioteca mudou e o capítulo não acompanhou"
    assert "Contradictory paths found" in texto17


def test_o_capitulo_17_nao_afirma_mais_o_silencio_universal(texto17):
    """Portão contra a reincidência da frase que a medição derrubou."""
    assert "não há erro, não há aviso, não há exceção lançada. A saída é" not in texto17, \
        "a afirmação de silêncio universal voltou ao corpo do capítulo 17"


def test_a_tabela_do_contraexemplo_esta_no_capitulo(texto17):
    """A tabela publicada tem uma linha por variante, com os quatro campos.

    Ela substituiu a tabela de duas linhas (Dijkstra × Bellman-Ford) que
    publicava a contradição como se fosse do método.
    """
    b = bellman_ford(COM_PESO_NEGATIVO, "A")
    assert b["distancias"]["D"] == F(4)
    assert f"A resposta certa é **{b['distancias']['D']}**" in texto17

    for r in as_tres_variantes(COM_PESO_NEGATIVO, "A", "D"):
        seta = " → ".join(r["caminho"])
        linha = f"| **{r['distancia']}** | `{seta}` | {r['custo_do_caminho']} |"
        assert linha in texto17, f"a linha da variante «{r['variante']}» não confere: {linha}"


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

from redes import (CIDADES, REDE, custo_de_proibir, fluxo_maximo, kruskal,  # noqa: E402
                   mst_por_enumeracao, tsp_exato, tsp_guloso,
                   varredura_do_guloso_no_roteiro)

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


def test_o_custo_de_proibir_uma_aresta_confere(texto18):
    """O único número da Parte III que era publicado sem medição — e era o único
    errado. O gabarito de `cap18.exA` dizia 19 (o certo é 21) e tirava daí a
    moral invertida: *"a perda é menor que o custo da aresta"*. É maior.
    """
    p = custo_de_proibir(CIDADES, "a", "c")
    assert p["custo_com"] == "17" and p["custo_sem"] == "21"
    assert p["perda"] == "4"
    assert p["perda_maior_que_o_peso_da_aresta"] is True, \
        "a instância parou de sustentar a lição: a perda deixou de superar o peso da aresta"
    assert f"| Árvore ótima sem `a–c` | **{p['custo_sem']}** |" in texto18
    assert f"| **Perda** | **{p['perda']}** |" in texto18


def test_o_gabarito_do_exercicio_18A_bate_com_a_medicao(exercicios):
    """O erro nasceu num gabarito, não no capítulo — então o teste lê o gabarito."""
    p = custo_de_proibir(CIDADES, "a", "c")
    ex = exercicios["cap18.exA"]
    texto = " ".join(ex["criterios"]) + " " + ex["resposta_guia"]
    assert f"**{p['custo_sem']}**" in texto, "o gabarito não publica o custo medido"
    assert "**19**" not in texto, "o valor errado voltou ao gabarito"


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


def test_a_procedencia_da_instancia_do_roteiro_confere(texto18):
    """A procedência é afirmação, e esta era conferível — e era falsa.

    O capítulo dizia que a instância era "a de maior perda relativa entre 4.000
    grafos". Não é: é o sorteio nº 3, e a de maior perda perde 150%. O teste
    existe porque a busca agora está no código, e prende os dois lados — o que
    a busca devolve e o que a página publica.

    Roda em alguns segundos: 4.000 instâncias de cinco cidades, cada uma com
    guloso e enumeração de 24 permutações.
    """
    v = varredura_do_guloso_no_roteiro()
    assert v["indice_da_instancia_publicada"] == 3, \
        "a instância publicada deixou de ser reproduzida pela semente declarada"
    assert v["maior_perda"] > v["perda_da_publicada"], \
        "a instância publicada virou a de maior perda — a ressalva do capítulo mudou de sentido"

    assert f"sorteio nº {v['indice_da_instancia_publicada']}" in texto18
    assert f"o 1867, com **{v['maior_perda']:g}%**" in texto18
    assert "**não é**" in texto18.lower() or "**Não é**" in texto18


@pytest.mark.parametrize("chave,linha", [
    ("mediana", "| Mediana da perda do guloso | **0%** |"),
    ("guloso_ja_otimo", "| Instâncias em que o guloso **já é ótimo** | **55,93%** |"),
    ("p90", "| Percentil 90 da perda | **25%** |"),
    ("maior_perda", "| Maior perda encontrada | **150%** |"),
    ("percentil_da_publicada", "| Onde caem os 14,3% desta página | percentil **78,8** |"),
    ("quantas_batem_ou_superam_a_publicada",
     "| Instâncias que perdem **tanto quanto ou mais** que a desta página | **848** de 4.000 |"),
])
def test_a_distribuicao_do_guloso_no_roteiro_confere(texto18, chave, linha):
    """A distribuição que corrige a distorção: o guloso é ótimo na MAIORIA.

    Publicar só a instância de 14,3% insinuava que o guloso costuma falhar.
    Cada linha da tabela é conferida contra a medição, uma a uma — este é
    justamente o tipo de número que, publicado sem dono, envelhece calado.
    """
    v = varredura_do_guloso_no_roteiro()
    assert linha in texto18, f"a linha de {chave} não confere com a medição ({v[chave]})"
    if chave == "guloso_ja_otimo":
        assert v[chave] > 50, "o guloso deixou de ser ótimo na maioria — a lição do capítulo muda"


def test_o_capitulo_18_registra_como_a_instancia_foi_obtida(texto18):
    """Sem isto, a instância parece desenhada para dar o resultado que dá.

    A versão anterior era **autorreferente** — `assert "4.000" in texto18`
    conferia o texto contra o texto, e teria passado com qualquer número
    inventado ali. Agora os dois valores vêm da busca.
    """
    v = varredura_do_guloso_no_roteiro()
    assert f"{v['sorteios']:,}".replace(",", ".") in texto18, "o tamanho da busca não confere"
    assert f"({v['semente']})" in texto18, "a semente publicada não confere com a medição"
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


def _arestas_desenhadas(texto: str) -> set:
    """Extrai `a --N--> b` de um diagrama em texto.

    A lookahead no destino é necessária: num encadeamento `a --1--> b --2--> c`
    o `b` é destino de um salto e origem do seguinte, e um casamento que
    consumisse o destino perderia metade das arestas.
    """
    import re
    return {(u, v, int(cap))
            for u, cap, v in re.findall(r"(\w+)\s*--(\d+)-*>\s*(?=(\w+))", texto)}


def test_todo_desenho_da_rede_de_fluxo_e_a_rede_medida(texto19, exercicios):
    """A rede aparece no capítulo **e** em enunciados de exercício. Toda cópia
    é uma chance de divergir, então todas são conferidas contra a instância.
    """
    medidas = {(u, v, int(c)) for u, saidas in REDE.items() for v, c in saidas.items()}
    fontes = [("capítulo 19", texto19)]
    fontes += [(i, e["enunciado"]) for i, e in exercicios.items()
               if i.startswith("cap19.") and "--" in e["enunciado"]]
    for nome, texto in fontes:
        desenhadas = _arestas_desenhadas(texto)
        if not desenhadas:
            continue
        assert desenhadas == medidas, (
            f"o desenho em {nome} não é a rede medida.\n"
            f"  só no desenho: {sorted(desenhadas - medidas)}\n"
            f"  só na medição: {sorted(medidas - desenhadas)}")


def test_o_diagrama_do_capitulo_19_e_a_rede_medida(texto19):
    """O desenho publicado **é** a instância, aresta por aresta.

    Este teste nasceu de um defeito real: o diagrama trazia
    `centro_sul --6--> loja_b`, aresta que não existe em `REDE` — o 6 é de
    `centro_norte`. O fluxo máximo continuava 15 nas duas leituras, então
    nenhum teste de número pegava. Um leitor conferindo à mão, sim.
    """
    import re
    desenhadas = set()
    # A lookahead no destino é necessária: num encadeamento `a --1--> b --2--> c`
    # o `b` é destino de um salto e origem do seguinte, e um casamento que
    # consumisse o destino perderia metade das arestas.
    for u, cap, v in re.findall(r"(\w+)\s*--(\d+)-*>\s*(?=(\w+))", texto19):
        desenhadas.add((u, v, int(cap)))
    medidas = {(u, v, int(c)) for u, saidas in REDE.items() for v, c in saidas.items()}
    assert desenhadas == medidas, (
        "o diagrama do capítulo 19 não é a rede medida.\n"
        f"  só no desenho: {sorted(desenhadas - medidas)}\n"
        f"  só na medição: {sorted(medidas - desenhadas)}")


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
                   designacao_por_ponto_interior,
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

    # O custo, sem o `or` literal que a versão anterior trazia: aquele ramo era
    # a string "223,33" escrita à mão, e passava mesmo que a medição mudasse,
    # bastando a string velha continuar em qualquer lugar da página.
    custo = f"{q['custo']:.2f}".replace(".", ",")
    assert f"| Custo ótimo | **220** | **{custo}** |" in texto20, \
        f"o custo com a restrição transversal não confere: {custo}"

    # E os VALORES dos fracionários, não só os nomes das rotas. A versão
    # anterior comparava `o → d` e descartava `v`, que é justamente por que
    # 1,67 / 3,33 / 23,33 / 6,67 estavam sem dono.
    for rota, v in q["fracionarios"].items():
        o, d = rota.split("->")
        assert f"`{o} → {d}`" in texto20, f"o fracionário {rota} não aparece no capítulo"
        valor = f"{v:.2f}".replace(".", ",")
        assert f"**{valor}**" in texto20, \
            f"o valor do fracionário {rota} não confere: {valor}"


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


def test_a_garantia_de_integralidade_para_no_ponto_interior(texto20, texto21):
    """Onde a garantia acaba — e o controle que prova que o limite é esse.

    A unimodularidade total garante que **existe vértice ótimo inteiro**. Ela
    não garante que o método usado pare num vértice. Com empate no ótimo e
    pontos interiores sem *crossover*, a saída medida é fracionária, e o
    objetivo continua ótimo — não é erro numérico, é outro ponto ótimo.

    O controle é a instância de ótimo único (a EQUIPE do capítulo): ali a face
    ótima é um ponto, e a saída sai 0/1 mesmo sem *crossover*. Sem esse
    controle, o experimento não distinguiria "ponto interior" de "solver ruim".
    """
    empatado = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    unico = [[EQUIPE[(p, t)] for t in ("relatorio", "auditoria", "treinamento")]
             for p in ("ana", "bruno", "clara")]

    sem_crossover = designacao_por_ponto_interior(empatado, "off")
    assert sem_crossover["todos_binarios"] is False, \
        "o contraexemplo do ponto interior morreu — os capítulos 20 e 21 dependem dele"
    assert sem_crossover["objetivo"] == 3, "o ponto fracionário tem de ser ÓTIMO"
    assert all(abs(v - 1 / 3) < 1e-5 for v in sem_crossover["valores"])

    assert designacao_por_ponto_interior(empatado, "on")["todos_binarios"] is True
    # o controle: ótimo único → a face é um ponto → 0/1 dos dois jeitos
    assert designacao_por_ponto_interior(unico, "off")["todos_binarios"] is True
    assert designacao_por_ponto_interior(unico, "off")["objetivo"] == 9

    for texto in (texto20, texto21):
        assert "crossover" in texto, \
            "o capítulo garante integralidade sem dizer onde a garantia para"


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


def test_a_mediana_e_o_p90_publicados_conferem(texto22, pert):
    """Estes dois números eram publicados no enunciado de `cap22.exC` e não
    apareciam em capítulo nenhum — número sem dono, que o leitor não podia
    rastrear. Agora estão na página, e presos à medição."""
    _, s = pert
    for chave in ("mediana", "p90"):
        valor = f"{s['projeto'][chave]:.2f}".replace(".", ",")
        assert f"**{valor}**" in texto22, f"{chave} não confere: {valor}"


def test_o_capitulo_22_declara_a_distribuicao_amostrada(texto22, pert):
    """A escolha de modelagem que responde por 3 dos 3,5 dias de desvio.

    O capítulo declarava a semente e omitia a distribuição — e um critério de
    `cap22.exB` cobrava do aluno justamente "triangular contra a média beta".
    Exercício insolúvel com o texto na mão.
    """
    _, s = pert
    assert s["distribuicao"].startswith("triangular")
    assert "triangular" in texto22, "a distribuição amostrada não está declarada"
    assert "(o + m + p)/3" in texto22 or "(o+m+p)/3" in texto22, \
        "o capítulo não diz qual é a média da distribuição que ele amostra"


def test_media_e_mediana_nao_sao_a_mesma_coisa(texto22, pert):
    """Contra a frase fácil: "metade das realizações fica acima da média".

    Isso é a definição de mediana. A medição separa as duas, e o capítulo
    tem de publicar a separação — senão a frase volta.
    """
    _, s = pert
    assert s["prob_de_estourar_a_mediana_simulada"] == 0.5
    assert s["prob_de_estourar_a_media_simulada"] < 0.5, \
        "a distribuição deixou de ser assimétrica à direita — a lição do capítulo mudou"
    assert s["projeto"]["media"] > s["projeto"]["mediana"]
    for chave in ("prob_de_estourar_a_media_simulada", "prob_de_estourar_a_mediana_simulada"):
        pct = f"{s[chave] * 100:.1f}".replace(".", ",")
        assert f"**{pct}%**" in texto22, f"{chave} não aparece no capítulo: {pct}%"


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


# ===========================================================================
# OS DADOS DE ENTRADA — a superfície que nenhum teste de resultado protege
# ===========================================================================
#
# Todo teste acima confere um RESULTADO contra a medição. Nenhum conferia a
# DEFINIÇÃO da instância — a tabela de pesos, a matriz de custos, o diagrama —
# que é justamente o que o leitor usa para refazer a conta à mão.
#
# A classe não é hipotética: o diagrama do capítulo 19 publicava uma aresta
# `centro_sul --6--> loja_b` que não existe em `REDE`. O fluxo máximo dá 15 nas
# duas leituras, então nenhum teste de número podia pegar. Um leitor conferindo
# à mão, sim — e teria concluído que o livro erra.
#
# Os testes abaixo generalizam a correção do 19 para as outras cinco instâncias.

from redes import COM_PESO_NEGATIVO as _CPN  # noqa: E402


def test_o_diagrama_do_capitulo_17_e_a_instancia_medida(texto17):
    """O grafo ASCII do contraexemplo, aresta por aresta.

    O formato aqui traz peso negativo entre parênteses — `C --(-3)--> B` —, o
    que exige um padrão próprio, diferente do usado no capítulo 19.
    """
    import re
    desenhadas = {(u, v, int(p))
                  for u, p, v in re.findall(r"(\w+)\s*--\(?(-?\d+)\)?-*>\s*(?=(\w+))", texto17)}
    medidas = {(u, v, int(c)) for u, v, c in _CPN}
    assert desenhadas == medidas, (
        f"o diagrama do capítulo 17 não é a instância medida.\n"
        f"  só no desenho: {sorted(desenhadas - medidas)}\n"
        f"  só na medição: {sorted(medidas - desenhadas)}")


def test_a_tabela_de_pesos_do_capitulo_18_e_a_instancia_medida(texto18):
    """As dez arestas de `CIDADES`, com o peso que o capítulo publica."""
    import re
    publicadas = {(u, v, int(p))
                  for u, v, p in re.findall(r"\|\s*(\w)–(\w)\s*\|\s*(\d+)\s*\|", texto18)}
    medidas = {(u, v, int(c)) for u, v, c in CIDADES}
    assert publicadas == medidas, (
        f"a tabela de pesos do capítulo 18 não é a instância medida.\n"
        f"  só na tabela : {sorted(publicadas - medidas)}\n"
        f"  só na medição: {sorted(medidas - publicadas)}")


def test_a_tabela_de_dados_do_capitulo_20_e_a_instancia_medida(texto20):
    """Custos, ofertas e demandas — os três de uma vez.

    É a tabela que o leitor usa para refazer o transporte à mão, e era a que
    podia divergir de `CUSTO`/`OFERTA`/`DEMANDA` sem que nada acusasse.
    """
    import re
    lojas = ["loja_a", "loja_b", "loja_c"]
    for fabrica in ("fabrica_1", "fabrica_2"):
        m = re.search(rf"\|\s*`{fabrica}`\s*\|" + r"\s*(\d+)\s*\|" * 3 + r"\s*(\d+)\s*\|", texto20)
        assert m, f"a linha de {fabrica} não foi encontrada no capítulo 20"
        for loja, valor in zip(lojas, m.groups()[:3]):
            assert CUSTO[(fabrica, loja)] == F(int(valor)), \
                f"custo {fabrica}→{loja}: capítulo diz {valor}, medição diz {CUSTO[(fabrica, loja)]}"
        assert OFERTA[fabrica] == F(int(m.group(4))), f"oferta de {fabrica} não confere"

    m = re.search(r"\|\s*\*\*Demanda\*\*\s*\|" + r"\s*(\d+)\s*\|" * 3, texto20)
    assert m, "a linha de demanda não foi encontrada no capítulo 20"
    for loja, valor in zip(lojas, m.groups()):
        assert DEMANDA[loja] == F(int(valor)), f"demanda de {loja} não confere"


def test_a_matriz_de_custos_do_capitulo_21_e_a_instancia_medida(texto21):
    """A matriz 3×3 da designação. O negrito marca o mínimo de cada linha, e
    por isso os valores precisam ser lidos com e sem os asteriscos."""
    import re
    tarefas = ["relatorio", "auditoria", "treinamento"]
    for pessoa in ("ana", "bruno", "clara"):
        m = re.search(rf"\|\s*`{pessoa}`\s*\|" + r"\s*\**(\d+)\**\s*\|" * 3, texto21)
        assert m, f"a linha de {pessoa} não foi encontrada no capítulo 21"
        for tarefa, valor in zip(tarefas, m.groups()):
            assert EQUIPE[(pessoa, tarefa)] == int(valor), \
                f"custo {pessoa}→{tarefa}: capítulo diz {valor}, medição diz {EQUIPE[(pessoa, tarefa)]}"


def test_as_tabelas_do_capitulo_22_sao_a_instancia_medida(texto22):
    """As duas definições do projeto: durações do CPM e as três estimativas do PERT."""
    import re
    for tarefa, (duracao, _) in PROJETO.items():
        assert re.search(rf"\|\s*`{tarefa}`\s*\|\s*{int(duracao)}\s*\|", texto22), \
            f"a duração de {tarefa} ({duracao}) não confere com a tabela do capítulo 22"

    for tarefa, (o, m_, p) in FAIXAS.items():
        linha = rf"\|\s*`{tarefa}`\s*\|\s*{o}\s*\|\s*{m_}\s*\|\s*{p}\s*\|"
        assert re.search(linha, texto22), \
            f"as três estimativas de {tarefa} ({o}, {m_}, {p}) não conferem com o capítulo 22"


# ===========================================================================
# OS TRÊS REFINAMENTOS DA SEGUNDA REVISÃO
# ===========================================================================

from redes import (controle_com_ramo_dominante, sensibilidade_a_semente,  # noqa: E402
                   transversal_nem_sempre_quebra)


def test_ser_transversal_nao_basta_para_quebrar_a_integralidade(texto20):
    """A regra prática do capítulo era boa como alerta e ruim como previsão.

    Três restrições igualmente transversais, e só uma quebra. O que separa não
    é a transversalidade: é o coeficiente. Este teste existe porque um
    exercício de Verificação pedia ao leitor que previsse a quebra num caso —
    o dos 40% — em que ela não acontece.
    """
    r = {c["caso"]: c for c in transversal_nem_sempre_quebra()}

    assert r["coeficientes 2 e 3 (o pátio)"]["fracionarios"] == 4
    assert r["coeficientes 1 e 1"]["todos_inteiros"] is True, \
        "o coeficiente 1 passou a quebrar a integralidade — a tabela do capítulo 20 muda"
    assert r["percentual do total (40%)"]["todos_inteiros"] is True, \
        "o caso dos 40% passou a quebrar — o exercício 3 da Verificação volta a fazer sentido"

    for caso in r.values():
        custo = f"{caso['custo']:.2f}".rstrip("0").rstrip(".").replace(".", ",")
        assert f"**{custo}**" in texto20, f"o custo de «{caso['caso']}» não confere: {custo}"
    assert "é **necessário** para perder a" in texto20


def test_o_controle_que_pode_falhar_da_positivo_e_pequeno(texto22):
    """O controle honesto, e a razão de o de `k=1` não servir.

    Com um ramo só a diferença pareada é zero em toda amostra, por construção —
    não tem como falhar. Aqui os dois ramos têm faixas que **se sobrepõem**, e
    é isso que dá dentes ao controle: o ramo curto vence de vez em quando.
    """
    c = controle_com_ramo_dominante()
    assert c["positivo"] is True, \
        "o controle voltou a dar zero — as faixas dos dois ramos pararam de se cruzar"
    assert c["pequeno"] is True, "o viés do controle ficou grande demais para ser controle"
    assert f"**{c['merge_bias']:.4f}".replace(".", ",")[:8] in texto22 or \
           f"**{c['merge_bias']}**".replace(".", ",") in texto22, \
        f"o viés do controle não está publicado: {c['merge_bias']}"


def test_o_capitulo_22_declara_ate_onde_o_digito_carrega(texto22):
    """Publicar 82,3% de uma semente só implica precisão que a simulação não tem."""
    f = sensibilidade_a_semente()
    lo, hi = f["media_do_projeto"]
    assert f"**{lo:.2f} a {hi:.2f}**".replace(".", ",") in texto22, \
        f"a faixa da média entre sementes não confere: {lo} a {hi}"
    lo, hi = f["prob_de_estourar"]
    assert f"**{lo * 100:.2f}% a {hi * 100:.2f}%**".replace(".", ",") in texto22, \
        f"a faixa da probabilidade não confere: {lo} a {hi}"
    assert "o segundo dígito carrega e o terceiro não" in texto22


# ===========================================================================
# TODA REAFIRMAÇÃO TEM DONO — contra o número que envelhece na Síntese
# ===========================================================================
#
# O defeito que este bloco fecha foi medido por campanha de mutação: os testes
# acima prendem UMA ocorrência canônica de cada número — a linha de tabela, com
# formatação distintiva — e toda **reafirmação** fica livre. Trocar o 0,49 da
# Síntese, ou o 15 da Leitura executiva, ou o 223,33 da caixa de erro caro,
# passava verde, porque `assert "0,49" in texto` continua verdadeiro enquanto
# sobrar qualquer outra ocorrência na página.
#
# Foram 110 números nessa situação na Parte III, concentrados exatamente onde o
# leitor apressado lê: Leitura executiva (41), caixa "erro caro" (18),
# Procedência (16) e Síntese (14).
#
# O instrumento é contar. O VALOR vem da medição; a CONTAGEM vem do texto. Se
# qualquer ocorrência derivar, a contagem cai e o teste fica vermelho — não
# importa qual das seis derivou.
#
# Consequência aceita, e ela é desejável: acrescentar uma menção nova ao mesmo
# número exige subir a contagem aqui. É uma decisão consciente a mais por
# menção, e é barata perto de um número que envelhece calado numa síntese.

def _ocorrencias(texto: str, valor: str) -> int:
    """Conta `valor` sem casar dentro de outro número (`3,33` dentro de `23,33`)."""
    import re
    return len(re.findall(r"(?<![\d,])" + re.escape(valor) + r"(?![\d,])", texto))


# (capítulo, o valor medido, de onde ele sai, quantas vezes a página o afirma)
REAFIRMACOES = [
    ("17", "**6**", "distância que Dijkstra devolve", 4),
    ("17", "**4**", "distância verdadeira, que Bellman-Ford acha", 3),
    ("18", "**17**", "custo da árvore geradora mínima", 1),
    ("18", "**32**", "roteiro guloso", 3),
    ("18", "**28**", "roteiro ótimo", 3),
    ("18", "14,3", "perda relativa do guloso", 8),
    ("19", "**15**", "fluxo máximo e capacidade do corte", 4),
    ("20", "**220**", "custo do transporte com estrutura de rede", 4),
    ("20", "223,33", "custo com a restrição transversal", 7),
    ("21", "**9**", "custo da designação", 2),
    ("22", "24,48", "duração média simulada do projeto", 9),
    ("22", "82,3", "probabilidade de estourar a estimativa do PERT", 6),
    # Sem os asteriscos, de propósito: o corpo escreve `**0,49 dia**` — a ênfase
    # embrulha o número E a unidade, e um padrão `**0,49**` não casaria com ela.
    # Foi assim que a primeira versão deste teste deixou passar a mutação do
    # corpo do capítulo 22, e a única coisa que revelou isso foi mutar de novo.
    ("22", "0,49", "o viés do método, isolado nas mesmas amostras", 7),
]


@pytest.mark.parametrize("cap,valor,o_que,vezes", REAFIRMACOES)
def test_toda_reafirmacao_do_numero_medido_confere(request, cap, valor, o_que, vezes):
    texto = request.getfixturevalue(f"texto{cap}")
    achadas = _ocorrencias(texto, valor)
    assert achadas == vezes, (
        f"capítulo {cap}: «{valor}» ({o_que}) aparece {achadas} vez(es), e a suíte "
        f"registra {vezes}.\n"
        f"  Se uma reafirmação derivou da medição, corrija o texto.\n"
        f"  Se você acrescentou ou removeu uma menção de propósito, atualize a "
        f"contagem em REAFIRMACOES — de propósito, e não por reflexo.")


def test_os_valores_contados_sao_os_valores_medidos(transp):
    """A outra metade do vínculo: as contagens acima só valem se os VALORES
    vierem da medição. Sem isto, a suíte contaria uma ficção com precisão."""
    from redes import EQUIPE, MALHA  # noqa: F401
    d = designacao(EQUIPE)
    assert f"**{d['custo']:g}**" == "**9**"
    assert f"**{kruskal(CIDADES)['custo']}**" == "**17**"
    assert f"**{tsp_guloso(CIDADES, 'a')['custo']}**" == "**32**"
    assert f"**{tsp_exato(CIDADES, 'a')['custo']}**" == "**28**"
    assert f"**{fluxo_maximo(REDE, 'fabrica', 'mercado')['fluxo']}**" == "**15**"
    assert f"{transp['custo']:.0f}" == "220"
    assert f"**{dijkstra(COM_PESO_NEGATIVO, 'A')['distancias']['D']}**" == "**6**"
    assert f"**{bellman_ford(COM_PESO_NEGATIVO, 'A')['distancias']['D']}**" == "**4**"
