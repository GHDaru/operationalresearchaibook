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
    """Dijkstra, escrito para ser lido — e para errar quando tem de errar.

    A implementação NÃO se defende de peso negativo, de propósito. Defender-se
    esconderia o que o capítulo 17 precisa mostrar: o método não avisa que
    falhou, ele devolve um número errado com toda a confiança do mundo. A razão
    é a hipótese que ele usa sem dizer — **uma vez fechado, um nó nunca melhora**
    —, e ela só vale com peso não negativo.
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

    return {"distancias": dist, "anterior": anterior, "metodo": "dijkstra"}


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
    return {
        "amostras": amostras,
        "semente": semente,
        "projeto": a,
        "so_o_caminho_declarado": b,
        "merge_bias": round(a["media"] - b["media"], 4),
        "prob_de_estourar_a_estimativa_do_pert": round(atrasos / amostras, 4),
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
        "cpm": c,
        "pert": {"formula": pf, "simulacao": ps, "varredura_de_ramos": varredura},
        "versoes": {"aritmetica": "fractions.Fraction (exata), exceto a simulação do PERT",
                    "semente": SEMENTE},
    }
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"resultados.json gravado em {AQUI}")
