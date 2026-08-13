"""Redes e fluxos — os cinco resultados que a Parte III publica, medidos.

A Parte III é a que atravessa metade da Pesquisa Operacional aplicada, e é
também a que oferece o resultado mais bonito do campo para ser **olhado** em vez
de citado: max-fluxo igual a corte mínimo. Este módulo mede cinco coisas:

  1. **Max-fluxo = corte mínimo**, com o corte exibido.
  2. **A relaxação linear do transporte já devolve inteiro** — e quebrar a
     estrutura de rede quebra isso. É o resultado mais útil da Parte.
  3. **Dijkstra erra com peso negativo**, e Bellman-Ford acerta.
  4. **Bellman-Ford detecta ciclo negativo.**
  5. **PERT subestima o prazo**, e o erro cresce com caminhos paralelos.

Aritmética exata (`Fraction`) em tudo que decide veredito. A única exceção é a
simulação do item 5, que é estocástica por natureza — lá o que se declara é a
**semente**, e o resultado publicado é uma frequência, não um valor exato.
"""

from __future__ import annotations

import random
from fractions import Fraction as F
from pathlib import Path

# ---------------------------------------------------------------------------
# A representação. Um grafo é um dicionário de listas de adjacência, e as
# arestas carregam Fraction — não float. Isso é caro e é deliberado: um caminho
# mínimo decidido por arredondamento seria indistinguível de um caminho mínimo
# decidido por estrutura, e é a estrutura que está sendo medida.
# ---------------------------------------------------------------------------

INFINITO = None  # ausência de caminho, para não confundir com um custo grande


def vizinhos(arestas: list[tuple], origem: str) -> list[tuple]:
    return [(u, v, c) for (u, v, c) in arestas if u == origem]


def nos(arestas: list[tuple]) -> list[str]:
    vistos: list[str] = []
    for u, v, _ in arestas:
        for x in (u, v):
            if x not in vistos:
                vistos.append(x)
    return vistos


# ---------------------------------------------------------------------------
# 1. CAMINHO MÍNIMO — e o caso em que o método rápido erra
# ---------------------------------------------------------------------------

def dijkstra(arestas: list[tuple], origem: str) -> dict:
    """Dijkstra de livro — com a guarda do nó fechado, e errando mesmo assim.

    **Esta é a versão canônica**, e a guarda `if v not in abertos: continue` é
    o que a define: nó fechado não é mais relaxado. É exatamente a hipótese que
    o método usa sem declarar — *uma vez fechado, um nó nunca melhora* — e que
    só vale com peso não negativo.

    A implementação NÃO se defende de peso negativo, de propósito. Com a
    aresta `C → B` de peso −3 ela devolve **6** onde a resposta é **4**, sem
    aviso e sem exceção. O erro é do método, não do código.

    Por que a guarda importa, e por que ela voltou: sem ela, a relaxação
    escreve em nó já fechado e corrompe a árvore de predecessores, produzindo
    uma saída **internamente inconsistente** — distância 6 ao lado de um
    caminho que custa 4. Esse sintoma é artefato da variante, não propriedade
    do método, e o capítulo 17 chegou a publicá-lo como se fosse o segundo. A
    variante sem guarda continua no arquivo, com nome próprio, logo abaixo.
    """
    dist: dict[str, F | None] = {n: INFINITO for n in nos(arestas)}
    anterior: dict[str, str | None] = {n: None for n in dist}
    dist[origem] = F(0)
    abertos = set(dist)

    while abertos:
        candidatos = [n for n in abertos if dist[n] is not None]
        if not candidatos:
            break
        atual = min(candidatos, key=lambda n: dist[n])
        abertos.discard(atual)
        for _, v, custo in vizinhos(arestas, atual):
            if v not in abertos:      # <-- A GUARDA. Nó fechado não se relaxa.
                continue
            novo = dist[atual] + custo
            if dist[v] is None or novo < dist[v]:
                dist[v] = novo
                anterior[v] = atual

    return {"distancias": dist, "anterior": anterior, "metodo": "dijkstra"}


def dijkstra_sem_guarda(arestas: list[tuple], origem: str) -> dict:
    """A variante que muita gente escreve sem perceber: relaxa nó já fechado.

    É o mesmo laço acima **sem** `if v not in abertos`. Parece mais simples e
    até mais correto — *"se achei caminho melhor, atualizo"* —, e com peso não
    negativo não faz diferença nenhuma, porque a situação nunca ocorre.

    Com peso negativo ela produz um defeito de outra natureza: `dist[B]` melhora
    depois de `B` fechar, e `anterior[B]` passa a apontar para `C`, mas `dist[D]`
    — que já tinha sido relaxado a partir do `B` antigo — **não é recalculado**.
    O resultado é uma saída que **contradiz a si mesma**: distância 6 e um
    caminho que custa 4.

    Ela está aqui porque a comparação com a versão canônica é a lição: o método
    erra nas duas, e o *modo* de errar depende de um `if`.
    """
    dist: dict[str, F | None] = {n: INFINITO for n in nos(arestas)}
    anterior: dict[str, str | None] = {n: None for n in dist}
    dist[origem] = F(0)
    abertos = set(dist)

    while abertos:
        candidatos = [n for n in abertos if dist[n] is not None]
        if not candidatos:
            break
        atual = min(candidatos, key=lambda n: dist[n])
        abertos.discard(atual)
        for _, v, custo in vizinhos(arestas, atual):
            novo = dist[atual] + custo
            if dist[v] is None or novo < dist[v]:
                dist[v] = novo
                anterior[v] = atual

    return {"distancias": dist, "anterior": anterior, "metodo": "dijkstra sem guarda"}


def dijkstra_com_fila(arestas: list[tuple], origem: str) -> dict:
    """A terceira variante: fila de prioridade com entradas obsoletas.

    É a implementação mais comum em código de produção, e nela um nó **pode**
    voltar à fila. Nesta instância ela acerta — devolve 4 — e o acerto é
    **acidente**, não garantia: sem a hipótese de peso não negativo, nada aqui
    prova terminação nem otimalidade. Um ciclo negativo a faz rodar para sempre.

    Publicar esse acerto ao lado dos dois erros é o ponto do capítulo 17: três
    coisas chamadas "Dijkstra" dão três respostas diferentes assim que a
    hipótese cai.
    """
    import heapq

    dist: dict[str, F | None] = {n: INFINITO for n in nos(arestas)}
    anterior: dict[str, str | None] = {n: None for n in dist}
    dist[origem] = F(0)
    fila = [(F(0), origem)]
    while fila:
        d, u = heapq.heappop(fila)
        if dist[u] is not None and d > dist[u]:
            continue
        for _, v, custo in vizinhos(arestas, u):
            novo = d + custo
            if dist[v] is None or novo < dist[v]:
                dist[v] = novo
                anterior[v] = u
                heapq.heappush(fila, (novo, v))
    return {"distancias": dist, "anterior": anterior, "metodo": "dijkstra com fila"}


def as_tres_variantes(arestas: list[tuple], origem: str, destino: str) -> list[dict]:
    """As três variantes na mesma instância, com o veredito de cada uma.

    `contradiz` é o teste que separa erro de incoerência: a distância que a
    variante publica bate com o custo do caminho que ela mesma devolve?
    """
    peso = {(u, v): c for u, v, c in arestas}
    saida = []
    for nome, f in (("com guarda (canônica)", dijkstra),
                    ("sem guarda", dijkstra_sem_guarda),
                    ("com fila de prioridade", dijkstra_com_fila)):
        r = f(arestas, origem)
        trilha = caminho(r, destino)
        custo_do_caminho = sum(peso[(a, b)] for a, b in zip(trilha, trilha[1:]))
        saida.append({
            "variante": nome,
            "distancia": str(r["distancias"][destino]),
            "caminho": trilha,
            "custo_do_caminho": str(custo_do_caminho),
            "contradiz_a_si_mesma": r["distancias"][destino] != custo_do_caminho,
            "acerta": custo_do_caminho == F(4) and r["distancias"][destino] == F(4),
        })
    return saida


def o_que_uma_biblioteca_faz(arestas: list[tuple], origem: str) -> dict:
    """E o que faz uma biblioteca consagrada diante da mesma instância.

    Importa porque o capítulo afirmava que o método falha **em silêncio**, sem
    aviso e sem exceção. Medido: a `networkx` **levanta exceção**. O silêncio
    é propriedade de algumas implementações, não do método — e essa distinção
    é o que separa uma lição verdadeira de uma lição confortável.
    """
    import networkx as nx

    g = nx.DiGraph()
    g.add_weighted_edges_from([(u, v, float(c)) for u, v, c in arestas])
    try:
        d = nx.single_source_dijkstra(g, origem)
        return {"biblioteca": "networkx", "versao": nx.__version__,
                "avisa": False, "resultado": str(d)}
    except Exception as e:                                   # noqa: BLE001
        return {"biblioteca": "networkx", "versao": nx.__version__,
                "avisa": True, "excecao": type(e).__name__, "mensagem": str(e)[:120]}


def bellman_ford(arestas: list[tuple], origem: str) -> dict:
    """Bellman-Ford: relaxa todas as arestas |V|-1 vezes, e depois confere.

    A passada extra é o que separa "achei o caminho" de "provei que não há
    melhor": se ainda houver melhora na |V|-ésima passada, existe **ciclo
    negativo**, e aí não existe caminho mínimo — existe caminho arbitrariamente
    barato. Devolver `ciclo_negativo` é o veredito honesto.
    """
    lista = nos(arestas)
    dist: dict[str, F | None] = {n: INFINITO for n in lista}
    anterior: dict[str, str | None] = {n: None for n in lista}
    dist[origem] = F(0)

    for _ in range(len(lista) - 1):
        mudou = False
        for u, v, custo in arestas:
            if dist[u] is None:
                continue
            novo = dist[u] + custo
            if dist[v] is None or novo < dist[v]:
                dist[v], anterior[v] = novo, u
                mudou = True
        if not mudou:
            break

    for u, v, custo in arestas:
        if dist[u] is not None and (dist[v] is None or dist[u] + custo < dist[v]):
            return {"distancias": dist, "anterior": anterior,
                    "metodo": "bellman-ford", "ciclo_negativo": True}

    return {"distancias": dist, "anterior": anterior,
            "metodo": "bellman-ford", "ciclo_negativo": False}


def caminho(resultado: dict, destino: str) -> list[str] | None:
    if resultado["distancias"].get(destino) is None:
        return None
    trilha, atual = [], destino
    while atual is not None:
        trilha.append(atual)
        atual = resultado["anterior"][atual]
    return list(reversed(trilha))


# A instância em que Dijkstra erra. Ela é pequena de propósito: o leitor tem de
# conseguir conferir à mão que o caminho A→C→B→D custa 3 e que Dijkstra devolve 4.
#
#   A --1--> B --5--> D          o atalho é A→C (2), depois C→B (-3), depois B→D (5)
#   A --2--> C --(-3)--> B       total: 2 - 3 + 5 = 4?  não: A→C→B custa -1, e -1+5 = 4
#
# Os números são escolhidos para que o ótimo verdadeiro seja MENOR que o de
# Dijkstra, e para que a diferença não seja de empate.
COM_PESO_NEGATIVO = [
    ("A", "B", F(1)),
    ("A", "C", F(2)),
    ("C", "B", F(-3)),
    ("B", "D", F(5)),
]

# Um ciclo negativo: rodar em torno de B→C→B baixa o custo para sempre.
COM_CICLO_NEGATIVO = [
    ("A", "B", F(1)),
    ("B", "C", F(2)),
    ("C", "B", F(-4)),
    ("B", "D", F(3)),
]

# A malha honesta, sem peso negativo — usada para mostrar os dois métodos
# concordando quando a hipótese de Dijkstra vale.
MALHA = [
    ("deposito", "norte", F(4)), ("deposito", "sul", F(2)),
    ("norte", "leste", F(5)), ("sul", "norte", F(1)),
    ("sul", "oeste", F(8)), ("oeste", "leste", F(2)),
    ("leste", "cliente", F(3)), ("oeste", "cliente", F(6)),
]


# ---------------------------------------------------------------------------
# 2. FLUXO MÁXIMO E CORTE MÍNIMO
# ---------------------------------------------------------------------------

def fluxo_maximo(capacidades: dict, fonte: str, sumidouro: str) -> dict:
    """Ford-Fulkerson com busca em largura (Edmonds-Karp), em aritmética exata.

    A **aresta reversa** é a peça que quase todo mundo esquece ao implementar, e
    é a que faz o método estar certo: ela permite ao algoritmo *desfazer* uma
    escolha anterior. Sem ela o procedimento acha um fluxo bloqueante e para,
    devolvendo um número menor com cara de ótimo.
    """
    residual = {u: dict(vs) for u, vs in capacidades.items()}
    for u, vs in capacidades.items():
        for v in vs:
            residual.setdefault(v, {}).setdefault(u, F(0))

    total = F(0)
    caminhos = []
    while True:
        # busca em largura no grafo residual
        anterior, fila = {fonte: None}, [fonte]
        while fila and sumidouro not in anterior:
            atual = fila.pop(0)
            for v, cap in residual[atual].items():
                if cap > 0 and v not in anterior:
                    anterior[v] = atual
                    fila.append(v)
        if sumidouro not in anterior:
            break

        trilha, no = [sumidouro], sumidouro
        while anterior[no] is not None:
            no = anterior[no]
            trilha.append(no)
        trilha.reverse()

        gargalo = min(residual[a][b] for a, b in zip(trilha, trilha[1:]))
        for a, b in zip(trilha, trilha[1:]):
            residual[a][b] -= gargalo
            residual[b][a] += gargalo
        total += gargalo
        caminhos.append({"caminho": trilha, "gargalo": str(gargalo)})

    # O corte mínimo sai de graça: o que a última busca alcançou fica de um lado.
    alcancaveis, fila = {fonte}, [fonte]
    while fila:
        atual = fila.pop(0)
        for v, cap in residual[atual].items():
            if cap > 0 and v not in alcancaveis:
                alcancaveis.add(v)
                fila.append(v)

    arestas_do_corte = [
        (u, v, str(c)) for u, vs in capacidades.items() for v, c in vs.items()
        if u in alcancaveis and v not in alcancaveis
    ]
    capacidade_do_corte = sum(
        c for u, vs in capacidades.items() for v, c in vs.items()
        if u in alcancaveis and v not in alcancaveis
    )

    return {
        "fluxo": str(total),
        "caminhos": caminhos,
        "corte": {
            "lado_da_fonte": sorted(alcancaveis),
            "arestas": arestas_do_corte,
            "capacidade": str(capacidade_do_corte),
        },
        "bate": total == capacidade_do_corte,
    }


# Uma rede de distribuição pequena o bastante para o leitor conferir o corte à mão.
REDE = {
    "fabrica":  {"centro_norte": F(10), "centro_sul": F(8)},
    "centro_norte": {"loja_a": F(6), "loja_b": F(6)},
    "centro_sul": {"loja_b": F(3), "loja_c": F(7)},
    "loja_a": {"mercado": F(6)},
    "loja_b": {"mercado": F(4)},
    "loja_c": {"mercado": F(5)},
}


# ---------------------------------------------------------------------------
# 3. O TRANSPORTE, E A INTEGRALIDADE QUE VEM DE GRAÇA
# ---------------------------------------------------------------------------

def transporte(oferta: dict, demanda: dict, custo: dict) -> dict:
    """Resolve o transporte como PL **sem nenhuma restrição de integralidade**.

    E o resultado sai inteiro. Não por sorte: a matriz de restrições de um
    problema de rede é **totalmente unimodular**, e com oferta e demanda
    inteiras todo vértice da região viável é inteiro. O leitor que vem do
    capítulo 04 sabe o preço de exigir integralidade; aqui ele vê o caso em que
    não é preciso pagá-lo.

    A implementação é enumeração de vértices por eliminação — pequena, exata, e
    suficiente para as instâncias didáticas. Não é como um solver faz.
    """
    import pulp

    origens, destinos = list(oferta), list(demanda)
    p = pulp.LpProblem("transporte", pulp.LpMinimize)
    x = {(o, d): pulp.LpVariable(f"x_{o}_{d}", lowBound=0) for o in origens for d in destinos}
    p += pulp.lpSum(float(custo[(o, d)]) * x[(o, d)] for o in origens for d in destinos)
    for o in origens:
        p += pulp.lpSum(x[(o, d)] for d in destinos) <= float(oferta[o])
    for d in destinos:
        p += pulp.lpSum(x[(o, d)] for o in origens) >= float(demanda[d])

    status = pulp.LpStatus[p.solve(pulp.HiGHS(msg=False))]
    plano = {f"{o}->{d}": x[(o, d)].value() for o in origens for d in destinos}
    inteiros = all(abs(v - round(v)) < 1e-9 for v in plano.values())
    return {
        "status": status,
        "custo": pulp.value(p.objective),
        "plano": plano,
        "todos_inteiros": inteiros,
        "fracionarios": {k: v for k, v in plano.items() if abs(v - round(v)) >= 1e-9},
    }


OFERTA = {"fabrica_1": 20, "fabrica_2": 30}
DEMANDA = {"loja_a": 15, "loja_b": 25, "loja_c": 10}
CUSTO = {
    ("fabrica_1", "loja_a"): 4, ("fabrica_1", "loja_b"): 6, ("fabrica_1", "loja_c"): 9,
    ("fabrica_2", "loja_a"): 5, ("fabrica_2", "loja_b"): 3, ("fabrica_2", "loja_c"): 8,
}


def transporte_com_estrutura_quebrada() -> dict:
    """A mesma situação com UMA restrição que não é de rede — e a fração aparece.

    A restrição acrescentada é comum e inocente: as rotas ocupam **espaço
    diferente** no pátio de carregamento — cada unidade da rota `fabrica_1 →
    loja_a` ocupa 2 posições e cada unidade de `fabrica_2 → loja_b` ocupa 3, num
    pátio de 100 posições. É uma restrição de recurso compartilhado, que
    qualquer operação real tem, e **destrói a unimodularidade**: a matriz deixa
    de ser de rede, e o ótimo da relaxação cai fora dos pontos inteiros.

    É a lição que o capítulo 20 existe para dar: a integralidade de graça é
    propriedade da **estrutura**, não do assunto. Quem acrescenta uma restrição
    transversal perde a propriedade sem receber nenhum aviso.

    NOTA DE MÉTODO, porque a primeira versão deste experimento errou e o erro é
    instrutivo. A restrição escolhida antes era *"loja B e loja C somadas ≤
    34,5"* — e as duas lojas demandam 35, então o modelo ficava **inviável**, não
    fracionário. Passou despercebido porque a função devolvia o plano sem que
    ninguém olhasse o `status`. Daí a asserção explícita abaixo: um experimento
    que não confere o próprio veredito mede outra coisa.
    """
    import pulp

    origens, destinos = list(OFERTA), list(DEMANDA)
    p = pulp.LpProblem("transporte_quebrado", pulp.LpMinimize)
    x = {(o, d): pulp.LpVariable(f"x_{o}_{d}", lowBound=0) for o in origens for d in destinos}
    p += pulp.lpSum(float(CUSTO[(o, d)]) * x[(o, d)] for o in origens for d in destinos)
    for o in origens:
        p += pulp.lpSum(x[(o, d)] for d in destinos) <= float(OFERTA[o])
    for d in destinos:
        p += pulp.lpSum(x[(o, d)] for o in origens) >= float(DEMANDA[d])
    # a restrição transversal: espaço de pátio, com consumo diferente por rota
    p += 2 * x[("fabrica_1", "loja_a")] + 3 * x[("fabrica_2", "loja_b")] <= 100

    status = pulp.LpStatus[p.solve(pulp.HiGHS(msg=False))]
    assert status == "Optimal", (
        f"o experimento da estrutura quebrada precisa de um modelo VIÁVEL para "
        f"mostrar fração, e este deu {status}")
    plano = {f"{o}->{d}": x[(o, d)].value() for o in origens for d in destinos}
    frac = {k: v for k, v in plano.items() if abs(v - round(v)) >= 1e-9}
    return {
        "status": status,
        "custo": pulp.value(p.objective),
        "plano": plano,
        "todos_inteiros": not frac,
        "fracionarios": frac,
    }


# ---------------------------------------------------------------------------
# 4. CPM E PERT — o caminho crítico, e o viés que o método publica
# ---------------------------------------------------------------------------

def caminho_critico(tarefas: dict) -> dict:
    """CPM em aritmética exata: cedo, tarde, folga, e o caminho crítico.

    `tarefas` mapeia nome -> (duração, lista de predecessoras).
    """
    ordem, pendentes = [], dict(tarefas)
    while pendentes:
        prontos = [t for t, (_, pre) in pendentes.items() if all(p in ordem for p in pre)]
        if not prontos:
            raise ValueError("há ciclo entre as tarefas — não é uma rede de projeto")
        ordem.extend(sorted(prontos))
        for t in prontos:
            pendentes.pop(t)

    cedo_inicio, cedo_fim = {}, {}
    for t in ordem:
        dur, pre = tarefas[t]
        cedo_inicio[t] = max((cedo_fim[p] for p in pre), default=F(0))
        cedo_fim[t] = cedo_inicio[t] + dur

    duracao = max(cedo_fim.values())
    tarde_fim, tarde_inicio = {}, {}
    for t in reversed(ordem):
        sucessoras = [s for s, (_, pre) in tarefas.items() if t in pre]
        tarde_fim[t] = min((tarde_inicio[s] for s in sucessoras), default=duracao)
        tarde_inicio[t] = tarde_fim[t] - tarefas[t][0]

    folga = {t: tarde_inicio[t] - cedo_inicio[t] for t in ordem}
    criticas = sorted(t for t in ordem if folga[t] == 0)
    return {
        "duracao": str(duracao),
        "cedo_inicio": {t: str(v) for t, v in cedo_inicio.items()},
        "folga": {t: str(v) for t, v in folga.items()},
        "criticas": criticas,
    }


# Um projeto com DOIS caminhos quase iguais — a configuração em que o viés do
# PERT aparece. Se um caminho fosse muito mais longo, o método acertaria.
PROJETO = {
    "especificar":  (F(5), []),
    "backend":      (F(10), ["especificar"]),
    "frontend":     (F(7), ["especificar"]),
    "integrar":     (F(3), ["backend", "frontend"]),
}

# Faixas otimista/provável/pessimista, no formato que o PERT pede.
FAIXAS = {
    "especificar": (4, 5, 12),
    "backend":     (6, 10, 20),
    "frontend":    (4, 7, 16),
    "integrar":    (2, 3, 10),
}


def pert_pela_formula(faixas: dict, tarefas: dict) -> dict:
    """A estimativa que o método PERT publica: média beta no caminho crítico.

    `media = (o + 4m + p) / 6` por tarefa, somada ao longo do caminho crítico —
    e a variância do prazo tomada como a soma das variâncias `((p-o)/6)²` das
    tarefas críticas. É o procedimento de manual.
    """
    medias = {t: F(o + 4 * m + p, 6) for t, (o, m, p) in faixas.items()}
    variancias = {t: F(p - o, 6) ** 2 for t, (o, m, p) in faixas.items()}
    com_media = {t: (medias[t], pre) for t, (_, pre) in tarefas.items()}
    cpm = caminho_critico(com_media)
    return {
        "medias": {t: str(v) for t, v in medias.items()},
        "duracao_esperada": cpm["duracao"],
        "criticas": cpm["criticas"],
        "variancia_do_prazo": str(sum(variancias[t] for t in cpm["criticas"])),
    }


def pert_por_simulacao(faixas: dict, tarefas: dict, criticas: list[str],
                      amostras: int, semente: int) -> dict:
    """A mesma rede, simulada — e o viés isolado da sua causa.

    ISOLAR IMPORTA, e a primeira versão deste experimento não isolava.

    Comparar a fórmula do PERT com uma simulação mistura **duas** causas
    diferentes num número só:

      (a) a distribuição amostrada não tem a mesma média que a fórmula supõe —
          a média triangular é `(o+m+p)/3` e a do PERT é `(o+4m+p)/6`;
      (b) o **merge bias**: o projeto espera a mais lenta das tarefas paralelas,
          e a média do máximo é maior do que o máximo das médias.

    Só (b) é o defeito do método. Misturar as duas produziria um número grande e
    sem significado — exatamente o tipo de medição que este handbook recusa.

    A isolação é feita **nas mesmas amostras**: para cada sorteio calculamos
    duas coisas — a duração real do projeto (máximo sobre todos os caminhos) e a
    duração do caminho que o CPM declarou crítico **antes** de sortear. A
    diferença entre as médias é o merge bias puro, porque tudo o mais é idêntico:
    mesma distribuição, mesmos números sorteados, mesma rede.
    """
    rnd = random.Random(semente)
    projeto, so_o_caminho = [], []
    for _ in range(amostras):
        sorteio = {t: F(rnd.triangular(o, p, m)).limit_denominator(10 ** 6)
                   for t, (o, m, p) in faixas.items()}
        com_sorteio = {t: (sorteio[t], pre) for t, (_, pre) in tarefas.items()}
        projeto.append(F(caminho_critico(com_sorteio)["duracao"]))
        so_o_caminho.append(sum(sorteio[t] for t in criticas))

    def resumo(xs):
        ordenado = sorted(xs)
        return {
            "media": float(sum(ordenado) / len(ordenado)),
            "mediana": float(ordenado[len(ordenado) // 2]),
            "p90": float(ordenado[int(0.9 * len(ordenado))]),
        }

    a, b = resumo(projeto), resumo(so_o_caminho)
    atrasos = sum(1 for x in projeto if x > sum(F(o + 4 * m + p, 6) for t, (o, m, p)
                                                in faixas.items() if t in criticas))
    # Estas duas medidas existem para desmentir uma frase fácil: "adotar a média
    # dá 50% de chance de estourar". Isso é a definição de MEDIANA. Numa
    # distribuição assimétrica à direita — que é o caso de todo prazo de projeto —
    # a média fica ACIMA da mediana, e estourá-la é menos provável que 50%.
    acima_da_media = sum(1 for x in projeto if x > a["media"])
    acima_da_mediana = sum(1 for x in projeto if x > a["mediana"])
    return {
        "amostras": amostras,
        "semente": semente,
        "distribuicao": "triangular(otimista, pessimista, provavel)",
        "projeto": a,
        "so_o_caminho_declarado": b,
        "merge_bias": round(a["media"] - b["media"], 4),
        "prob_de_estourar_a_estimativa_do_pert": round(atrasos / amostras, 4),
        "prob_de_estourar_a_media_simulada": round(acima_da_media / amostras, 4),
        "prob_de_estourar_a_mediana_simulada": round(acima_da_mediana / amostras, 4),
    }


# ---------------------------------------------------------------------------
# 3b. ÁRVORE GERADORA MÍNIMA — e o guloso que funciona, ao lado do que não
# ---------------------------------------------------------------------------

def kruskal(arestas: list[tuple]) -> dict:
    """Guloso que **prova** o ótimo: ordena por peso e aceita o que não fecha ciclo.

    O capítulo 18 vive desta comparação: o mesmo gesto — *pegue sempre o mais
    barato agora* — é ótimo aqui e não é ótimo no caixeiro-viajante. A diferença
    não é de sorte nem de tamanho: é a **propriedade do corte**, que a árvore
    tem e o roteiro não.
    """
    pai = {n: n for n in nos(arestas)}

    def raiz(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]
            x = pai[x]
        return x

    escolhidas, custo = [], F(0)
    for u, v, c in sorted(arestas, key=lambda a: (a[2], a[0], a[1])):
        ru, rv = raiz(u), raiz(v)
        if ru != rv:
            pai[ru] = rv
            escolhidas.append((u, v, str(c)))
            custo += c
    return {"arestas": escolhidas, "custo": str(custo), "metodo": "kruskal"}


def tsp_guloso(arestas: list[tuple], inicio: str) -> dict:
    """O mesmo gesto guloso, no caixeiro-viajante: vá sempre ao vizinho mais perto."""
    peso = {}
    for u, v, c in arestas:
        peso[(u, v)] = peso[(v, u)] = c
    restantes = [n for n in nos(arestas) if n != inicio]
    rota, atual, custo = [inicio], inicio, F(0)
    while restantes:
        proximo = min(restantes, key=lambda n: (peso.get((atual, n), F(10 ** 9)), n))
        custo += peso[(atual, proximo)]
        rota.append(proximo)
        restantes.remove(proximo)
        atual = proximo
    custo += peso[(atual, inicio)]
    rota.append(inicio)
    return {"rota": rota, "custo": str(custo), "metodo": "guloso"}


def tsp_exato(arestas: list[tuple], inicio: str) -> dict:
    """Enumeração de todas as permutações. Só cabe porque a instância é minúscula."""
    from itertools import permutations
    peso = {}
    for u, v, c in arestas:
        peso[(u, v)] = peso[(v, u)] = c
    outros = [n for n in nos(arestas) if n != inicio]
    melhor, melhor_custo = None, None
    for ordem in permutations(outros):
        trilha = [inicio, *ordem, inicio]
        if any((a, b) not in peso for a, b in zip(trilha, trilha[1:])):
            continue
        c = sum(peso[(a, b)] for a, b in zip(trilha, trilha[1:]))
        if melhor_custo is None or c < melhor_custo:
            melhor, melhor_custo = trilha, c
    return {"rota": melhor, "custo": str(melhor_custo), "metodo": "enumeração"}


# Um grafo completo de cinco cidades em que o mesmo gesto guloso acerta a árvore
# e ERRA o roteiro.
#
# A instância não foi desenhada à mão: a primeira tentativa foi, e o guloso
# acertou o roteiro nela — a afirmação "guloso erra no caixeiro" não se
# sustentava no exemplo que eu tinha escolhido. Esta saiu de um sorteio com
# semente declarada (20260813), `randint(1, 12)` em cada uma das dez arestas.
#
# CORREÇÃO REGISTRADA. Até a revisão desta rodada, este comentário e o capítulo
# 18 diziam que a instância era "a de MAIOR perda relativa entre 4.000 grafos".
# **Não é**, e a afirmação era conferível: a busca está agora implementada em
# `varredura_do_guloso_no_roteiro()`, e ela mostra que a instância publicada é o
# **sorteio nº 3**, com perda de 14,3% — enquanto a de maior perda, o sorteio
# 1867, perde 150%. O que aconteceu de fato foi parar no primeiro sorteio com
# perda substancial, que é uma escolha legítima e **outra** da que foi narrada.
#
# A instância continua publicada: ela serve ao capítulo, e trocá-la por outra
# não conserta o defeito, que era de procedência e não de número. O que mudou é
# que agora existe o código, e ele publica também a distribuição — que diz o
# contrário do que o capítulo insinuava: nestas instâncias o guloso é ótimo
# **mais vezes do que erra**.
CIDADES = [
    ("a", "b", F(8)), ("a", "c", F(3)), ("a", "d", F(12)), ("a", "e", F(7)),
    ("b", "c", F(5)), ("b", "d", F(8)), ("b", "e", F(6)),
    ("c", "d", F(7)), ("c", "e", F(3)),
    ("d", "e", F(6)),
]


SEMENTE_CIDADES = 20260813
SORTEIOS_CIDADES = 4000


def varredura_do_guloso_no_roteiro(semente: int = SEMENTE_CIDADES,
                                   sorteios: int = SORTEIOS_CIDADES) -> dict:
    """A busca que o comentário acima descrevia e o repositório não continha.

    Ela existe por dois motivos, e o segundo é mais importante que o primeiro.

    **Primeiro**: procedência é afirmação, e afirmação de procedência tem de ser
    conferível. Enquanto a busca era só prosa, "tomando a de maior perda
    relativa" era indistinguível de uma lembrança errada — e era uma.

    **Segundo**: a distribuição corrige uma distorção pedagógica do capítulo 18.
    Ao publicar só a instância em que o guloso perde 14,3%, o texto insinuava que
    o guloso costuma falhar no roteiro. Medido, ele é **ótimo na maioria** das
    instâncias aleatórias de cinco cidades, e os 14,3% ficam perto do percentil
    80. A lição verdadeira do capítulo não é "o guloso erra" — é "o guloso **não
    tem como avisar** quando erra", e essa não depende de frequência.
    """
    from itertools import combinations

    rnd = random.Random(semente)
    perdas, indice_da_publicada = [], None
    for i in range(sorteios):
        arestas = [(u, v, F(rnd.randint(1, 12)))
                   for u, v in combinations(("a", "b", "c", "d", "e"), 2)]
        g, o = tsp_guloso(arestas, "a"), tsp_exato(arestas, "a")
        perdas.append(F(g["custo"]) / F(o["custo"]) - 1)
        if arestas == CIDADES:
            indice_da_publicada = i

    ordenadas = sorted(perdas)
    publicada = perdas[indice_da_publicada] if indice_da_publicada is not None else None
    pct = lambda x: round(float(x) * 100, 2)  # noqa: E731
    return {
        "semente": semente,
        "sorteios": sorteios,
        "indice_da_instancia_publicada": indice_da_publicada,
        "perda_da_publicada": pct(publicada) if publicada is not None else None,
        "indice_da_maior_perda": max(range(sorteios), key=lambda i: perdas[i]),
        "maior_perda": pct(ordenadas[-1]),
        "mediana": pct(ordenadas[sorteios // 2]),
        "guloso_ja_otimo": round(sum(1 for p in perdas if p == 0) / sorteios * 100, 2),
        "p90": pct(ordenadas[int(0.9 * sorteios)]),
        "quantas_batem_ou_superam_a_publicada":
            sum(1 for p in perdas if publicada is not None and p >= publicada),
        "percentil_da_publicada":
            round(sum(1 for p in perdas if publicada is not None and p < publicada)
                  / sorteios * 100, 2),
    }


def mst_por_enumeracao(arestas: list[tuple]) -> dict:
    """Confere Kruskal por um segundo caminho: enumera TODAS as árvores geradoras.

    Chegar ao mesmo número por dois caminhos é o que separa medição de
    coincidência. Só cabe porque a instância tem cinco nós.
    """
    from itertools import combinations
    lista = nos(arestas)
    melhor, melhor_custo = None, None
    for escolha in combinations(arestas, len(lista) - 1):
        pai = {n: n for n in lista}

        def raiz(x):
            while pai[x] != x:
                x = pai[x]
            return x

        ok = True
        for u, v, _ in escolha:
            ru, rv = raiz(u), raiz(v)
            if ru == rv:
                ok = False
                break
            pai[ru] = rv
        if not ok:
            continue
        c = sum(x[2] for x in escolha)
        if melhor_custo is None or c < melhor_custo:
            melhor, melhor_custo = escolha, c
    return {"custo": str(melhor_custo),
            "arestas": [(u, v, str(c)) for u, v, c in melhor],
            "metodo": "enumeração de árvores geradoras"}


def custo_de_proibir(arestas: list[tuple], u: str, v: str) -> dict:
    """Quanto custa **proibir** uma aresta da árvore ótima?

    A resposta intuitiva — *"custa o que a aresta valia"* — está errada, e esta
    medição existe para mostrar isso com número. Proibir a aresta `a–c`, que
    custa 3, encarece a árvore em 4: a substituta não é a próxima aresta da
    lista, é a **melhor reconexão disponível depois que a topologia mudou**.

    A perda pode ser maior ou menor que o peso da aresta proibida. Publicar a
    lição no sentido errado seria pior do que não publicá-la.
    """
    proibida = {(u, v), (v, u)}
    restantes = [a for a in arestas if (a[0], a[1]) not in proibida]
    com = mst_por_enumeracao(arestas)
    sem = mst_por_enumeracao(restantes)
    peso = next(a[2] for a in arestas if (a[0], a[1]) in proibida)
    return {
        "aresta_proibida": [u, v, str(peso)],
        "custo_com": com["custo"],
        "custo_sem": sem["custo"],
        "arestas_sem": sem["arestas"],
        "perda": str(F(sem["custo"]) - F(com["custo"])),
        "perda_maior_que_o_peso_da_aresta": F(sem["custo"]) - F(com["custo"]) > peso,
    }


# ---------------------------------------------------------------------------
# 3c. DESIGNAÇÃO — a integralidade de graça, de novo, e agora em 0/1
# ---------------------------------------------------------------------------

def designacao(custo: dict) -> dict:
    """Aloca pessoas a tarefas resolvendo **PL contínua**, sem variável binária.

    E a saída sai 0/1. É a mesma unimodularidade do transporte, no caso em que
    ela mais surpreende: o problema é combinatório por enunciado — *cada pessoa
    faz exatamente uma tarefa* — e mesmo assim não precisa de programação
    inteira. Quem declara `cat="Binary"` aqui paga um preço que a estrutura já
    tinha dispensado.
    """
    import pulp

    pessoas = sorted({p for p, _ in custo})
    tarefas = sorted({t for _, t in custo})
    p = pulp.LpProblem("designacao", pulp.LpMinimize)
    x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", lowBound=0, upBound=1) for i, j in custo}
    p += pulp.lpSum(float(custo[(i, j)]) * x[(i, j)] for i, j in custo)
    for i in pessoas:
        p += pulp.lpSum(x[(i, j)] for j in tarefas) == 1
    for j in tarefas:
        p += pulp.lpSum(x[(i, j)] for i in pessoas) == 1

    status = pulp.LpStatus[p.solve(pulp.HiGHS(msg=False))]
    valores = {f"{i}->{j}": x[(i, j)].value() for i, j in custo}
    escolhidos = sorted(k for k, v in valores.items() if v > 0.5)
    binarios = all(abs(v - round(v)) < 1e-9 for v in valores.values())
    return {"status": status, "custo": pulp.value(p.objective),
            "escolhidos": escolhidos, "todos_binarios": binarios}


EQUIPE = {
    ("ana", "relatorio"): 9, ("ana", "auditoria"): 2, ("ana", "treinamento"): 7,
    ("bruno", "relatorio"): 6, ("bruno", "auditoria"): 4, ("bruno", "treinamento"): 3,
    ("clara", "relatorio"): 5, ("clara", "auditoria"): 8, ("clara", "treinamento"): 1,
}


def designacao_por_ponto_interior(custos: list[list[float]], crossover: str) -> dict:
    """O contraexemplo que delimita a garantia de integralidade.

    A unimodularidade total garante que **existe vértice ótimo inteiro** — não
    que a resposta de qualquer solver seja inteira. Um método de pontos
    interiores ([capítulo 14](../../livro/capitulos/14-pontos-interiores.md))
    não para em vértice: ele converge para o **centro da face ótima**. Quando o
    ótimo é único, a face é um ponto e a distinção não aparece. Quando há
    empate — e designação empata o tempo todo —, o centro da face é fracionário.

    Com empate — `n × n` de custos todos iguais — a saída medida sem *crossover*
    é `1/n` em toda variável. Com *crossover* ligado, o método volta a um vértice
    e a saída é 0/1. Com ótimo único, a face é um ponto e a saída sai 0/1 dos
    dois jeitos.

    Não é defeito do solver: é o que pontos interiores fazem, e é por isso que
    *crossover* existe.

    Um aviso de projeto de experimento, porque custou uma tentativa: custo da
    forma `a_i + b_j` **não** serve de instância de ótimo único. Toda designação
    soma `Σa + Σb`, então tudo empata, e o "controle" mede o mesmo que o caso.
    """
    import highspy
    import numpy as np

    n = len(custos)
    vazio_i, vazio_f = np.array([], dtype=np.int32), np.array([], dtype=np.float64)
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("solver", "ipm")
    h.setOptionValue("run_crossover", crossover)
    for i in range(n):
        for j in range(n):
            h.addCol(float(custos[i][j]), 0.0, 1.0, 0, vazio_i, vazio_f)
    for i in range(n):  # cada pessoa faz exatamente uma tarefa
        h.addRow(1, 1, n, np.array([i * n + j for j in range(n)], dtype=np.int32),
                 np.ones(n))
    for j in range(n):  # cada tarefa recebe exatamente uma pessoa
        h.addRow(1, 1, n, np.array([i * n + j for i in range(n)], dtype=np.int32),
                 np.ones(n))
    h.run()
    valores = [round(v, 6) for v in h.getSolution().col_value]
    return {
        "n": n, "crossover": crossover,
        "objetivo": round(h.getObjectiveValue(), 6),
        "valores": valores,
        "todos_binarios": all(abs(v - round(v)) < 1e-6 for v in valores),
        "versao_do_highs": h.version(),
    }


def rede_com_ramos(k: int) -> tuple[dict, dict, list[str]]:
    """Uma rede de projeto com `k` ramos paralelos idênticos entre duas tarefas.

    Serve para medir como o merge bias cresce com o número de caminhos que se
    juntam. O caso `k = 1` é o **controle**: sem paralelismo, a duração do
    projeto É a duração do caminho declarado, e o viés tem de dar exatamente
    zero. Um experimento sem controle não distingue medição de artefato.
    """
    tarefas = {"especificar": (F(5), [])}
    faixas = {"especificar": (4, 5, 12)}
    ramos = [f"ramo_{i + 1}" for i in range(k)]
    for r in ramos:
        tarefas[r] = (F(10), ["especificar"])
        faixas[r] = (6, 10, 20)
    tarefas["integrar"] = (F(3), ramos)
    faixas["integrar"] = (2, 3, 10)
    return tarefas, faixas, ramos


RAMOS_MEDIDOS = (1, 2, 3, 5, 8)
AMOSTRAS_VARREDURA_PERT = 8_000


def varredura_de_ramos() -> list[dict]:
    """O viés e a probabilidade de estouro, conforme os ramos paralelos crescem."""
    saida = []
    for k in RAMOS_MEDIDOS:
        tarefas, faixas, ramos = rede_com_ramos(k)
        declarado = ["especificar", ramos[0], "integrar"]
        s = pert_por_simulacao(faixas, tarefas, declarado,
                               AMOSTRAS_VARREDURA_PERT, SEMENTE)
        saida.append({"ramos": k, "merge_bias": s["merge_bias"],
                      "prob_de_estourar": s["prob_de_estourar_a_estimativa_do_pert"]})
    return saida


AQUI = Path(__file__).resolve().parent
SEMENTE = 20260813
AMOSTRAS_PERT = 20_000


if __name__ == "__main__":
    import json

    print("1. CAMINHO MÍNIMO — e o caso em que o método rápido erra")
    print("=" * 82)
    dm, bm = dijkstra(MALHA, "deposito"), bellman_ford(MALHA, "deposito")
    print(f"  malha honesta: os dois concordam? {dm['distancias'] == bm['distancias']}"
          f"  ·  caminho {' → '.join(caminho(dm, 'cliente'))} custa {dm['distancias']['cliente']}")
    dn, bn = dijkstra(COM_PESO_NEGATIVO, "A"), bellman_ford(COM_PESO_NEGATIVO, "A")
    print(f"  com peso negativo: dijkstra diz {dn['distancias']['D']}, "
          f"bellman-ford diz {bn['distancias']['D']}")
    print(f"  e o pior: dijkstra devolve o caminho {' → '.join(caminho(dn, 'D'))}, "
          f"que custa {bn['distancias']['D']} — a resposta CONTRADIZ a si mesma")
    print(f"  ciclo negativo detectado por bellman-ford: "
          f"{bellman_ford(COM_CICLO_NEGATIVO, 'A')['ciclo_negativo']}")
    print()

    print("2. FLUXO MÁXIMO E CORTE MÍNIMO")
    print("=" * 82)
    f = fluxo_maximo(REDE, "fabrica", "mercado")
    print(f"  fluxo máximo: {f['fluxo']}  ·  capacidade do corte: {f['corte']['capacidade']}"
          f"  ·  batem: {f['bate']}")
    print(f"  o corte: {[(u, v) for u, v, _ in f['corte']['arestas']]}")
    print()

    print("3. TRANSPORTE — a integralidade que vem da estrutura, e some com ela")
    print("=" * 82)
    tr = transporte(OFERTA, DEMANDA, CUSTO)
    print(f"  relaxação linear, SEM restrição de integralidade: custo {tr['custo']:g}"
          f"  ·  todos inteiros: {tr['todos_inteiros']}")
    qb = transporte_com_estrutura_quebrada()
    print(f"  com UMA restrição transversal: custo {qb['custo']:.4f}"
          f"  ·  todos inteiros: {qb['todos_inteiros']}")
    print(f"  frações que aparecem: "
          f"{ {k: round(v, 4) for k, v in qb['fracionarios'].items()} }")
    print()

    print("3b. O MESMO GESTO GULOSO: ótimo na árvore, 14% pior no roteiro")
    print("=" * 82)
    kr, enu = kruskal(CIDADES), mst_por_enumeracao(CIDADES)
    print(f"  árvore por Kruskal: custo {kr['custo']}  ·  por enumeração de TODAS as "
          f"árvores: {enu['custo']}  ·  batem: {kr['custo'] == enu['custo']}")
    pr = custo_de_proibir(CIDADES, "a", "c")
    print(f"  proibir a aresta a–c (que vale {pr['aresta_proibida'][2]}): a árvore passa de "
          f"{pr['custo_com']} para {pr['custo_sem']}  ·  perda {pr['perda']}  ·  "
          f"perda MAIOR que o peso da aresta: {pr['perda_maior_que_o_peso_da_aresta']}")
    tg, te = tsp_guloso(CIDADES, "a"), tsp_exato(CIDADES, "a")
    perda = F(tg["custo"]) - F(te["custo"])
    print(f"  roteiro guloso: {tg['custo']} ({' → '.join(tg['rota'])})")
    print(f"  roteiro ótimo : {te['custo']} ({' → '.join(te['rota'])})")
    print(f"  perda do guloso: {perda}  ·  {float(F(tg['custo']) / F(te['custo']) - 1):.1%}")
    print()

    print("3c. DESIGNAÇÃO — 0/1 sem pedir binária")
    print("=" * 82)
    dg = designacao(EQUIPE)
    print(f"  custo {dg['custo']:g}  ·  todos 0/1: {dg['todos_binarios']}  ·  {dg['escolhidos']}")
    print()

    print("3d. ONDE A GARANTIA PARA: ponto interior sem crossover, com empate")
    print("=" * 82)
    # `empate`: toda designação custa 3, a face ótima é o politopo inteiro.
    # `unico`: a instância da EQUIPE, cujo ótimo é único (custo 9).
    instancias = {
        "empate": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "unico": [[EQUIPE[(p, t)] for t in ("relatorio", "auditoria", "treinamento")]
                  for p in ("ana", "bruno", "clara")],
    }
    pi = {f"{nome}_crossover_{c}": designacao_por_ponto_interior(m, c)
          for nome, m in instancias.items() for c in ("off", "on")}
    for k, v in pi.items():
        print(f"  {k:<22} objetivo {v['objetivo']:g}  ·  todos 0/1: {v['todos_binarios']}"
              f"  ·  {v['valores'][:3]}...")
    print("  → a garantia é sobre VÉRTICE, não sobre a saída de qualquer método.")
    print()

    print("4. CPM — caminho crítico e folga")
    print("=" * 82)
    c = caminho_critico(PROJETO)
    print(f"  duração {c['duracao']}  ·  críticas {c['criticas']}  ·  folgas {c['folga']}")
    print()

    print("5. PERT — o viés isolado da sua causa")
    print("=" * 82)
    pf = pert_pela_formula(FAIXAS, PROJETO)
    ps = pert_por_simulacao(FAIXAS, PROJETO, pf["criticas"], AMOSTRAS_PERT, SEMENTE)
    print(f"  a fórmula publica: {pf['duracao_esperada']} dias")
    print(f"  simulado, o projeto leva em média {ps['projeto']['media']:.2f}"
          f"  ·  só o caminho declarado: {ps['so_o_caminho_declarado']['media']:.2f}")
    print(f"  MERGE BIAS (nas mesmas amostras): {ps['merge_bias']}")
    print(f"  probabilidade de estourar a estimativa do PERT: "
          f"{ps['prob_de_estourar_a_estimativa_do_pert']:.1%}")
    print()
    print("  e como ele cresce com os ramos paralelos (k=1 é o controle, tem de dar 0):")
    varredura = varredura_de_ramos()
    for v in varredura:
        print(f"    {v['ramos']} ramo(s): viés {v['merge_bias']:>7}  ·  "
              f"estoura em {v['prob_de_estourar']:.1%} das amostras")
    print()

    saida = {
        "caminho_minimo": {
            "malha": {"distancias": {k: str(v) for k, v in dm["distancias"].items()},
                      "caminho_ate_cliente": caminho(dm, "cliente"),
                      "dijkstra_e_bellman_concordam": dm["distancias"] == bm["distancias"]},
            "com_peso_negativo": {"dijkstra": str(dn["distancias"]["D"]),
                                  "bellman_ford": str(bn["distancias"]["D"]),
                                  "caminho_que_dijkstra_devolve": caminho(dn, "D")},
            "ciclo_negativo_detectado": bellman_ford(COM_CICLO_NEGATIVO, "A")["ciclo_negativo"],
        },
        "fluxo_maximo": f,
        "transporte": {"integral": tr, "estrutura_quebrada": qb},
        "arvore_e_roteiro": {"mst_kruskal": kr, "mst_por_enumeracao": enu,
                             "custo_de_proibir_a_c": pr,
                             "tsp_guloso": tg, "tsp_exato": te, "perda_do_guloso": str(perda)},
        "designacao": dg,
        "designacao_por_ponto_interior": pi,
        "cpm": c,
        "pert": {"formula": pf, "simulacao": ps, "varredura_de_ramos": varredura},
        "versoes": {"aritmetica": "fractions.Fraction (exata), exceto a simulação do PERT",
                    "semente": SEMENTE},
    }
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"resultados.json gravado em {AQUI}")
