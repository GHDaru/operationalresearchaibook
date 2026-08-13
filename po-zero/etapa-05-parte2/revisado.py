"""A forma revisada do Simplex, medida contra o quadro — não afirmada.

Ancora o capítulo 11. O desenho desta medição está na
[ADR 0012](../../adr/0012-o-desenho-da-medicao-do-capitulo-11.md), e cada decisão
dela está marcada no código com o identificador (D1…D8), para que quem revisar
possa cobrar uma por uma.

O QUE ESTA ETAPA NÃO FAZ: ensinar método novo. É o **mesmo** Simplex, escrito de
outro jeito. Se a resposta mudar, o capítulo 11 está errado — e a etapa 03,
publicada e intocada, é o árbitro (D2).

O COMPROMISSO DECLARADO ANTES DE MEDIR, que está na spec 008: se a forma
revisada **não** ganhar nas instâncias que este handbook consegue construir numa
CPU comum, isso entra no capítulo como resultado. O livro não afirma ganho que o
experimento não mostrar.

Rode com: python3 revisado.py
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "etapa-03-simplex"))
from quadro import Restricao, resolver, fmt  # noqa: E402

AQUI = Path(__file__).parent


# ---------------------------------------------------------------------------
# D1 — Uma primitiva aritmética instrumentada, compartilhada pelas duas formas.
#
# As duas implementações abaixo fazem TODA a sua aritmética por aqui. É o que
# torna a comparação justa por construção, em vez de justa por promessa: nenhuma
# das duas pode "esquecer" de contar uma operação sem deixar de calcular.
#
# A CONVENÇÃO DE CONTAGEM, declarada porque sem ela o número não significa nada
# (critério A19): conta-se **multiplicação e divisão**, que dominam o custo, e
# **não** se contam somas — que acompanham as multiplicações uma a uma nos dois
# lados e por isso não mudam a comparação. Multiplicação por zero NÃO é contada,
# porque nenhuma implementação séria a executa: é exatamente a economia que a
# esparsidade produz, e escondê-la falsearia o experimento em favor do quadro.

class Contador:
    def __init__(self):
        self.mult = 0
        self.div = 0

    def m(self, a, b):
        if a == 0 or b == 0:
            return type(a)(0) if isinstance(a, F) else 0.0 * a
        self.mult += 1
        return a * b

    def d(self, a, b):
        self.div += 1
        return a / b

    @property
    def total(self):
        return self.mult + self.div


# ---------------------------------------------------------------------------
# As duas formas. Ambas para  max c'x  s.a.  Ax <= b,  x >= 0,  b >= 0.
# Base inicial de folgas — é o caso que o capítulo 09 já construiu, e mantê-lo
# evita que a comparação meça big-M em vez de medir a forma.

def _pivo_quadro(T, base, m, n, ct):
    """Uma iteração do quadro cheio. Devolve (entra, sai) ou None se ótimo."""
    ncols = n + m
    z = T[m]
    entra = None
    for j in range(ncols):
        if j in base:
            continue
        if z[j] < 0:
            entra = j                      # regra de Dantzig: primeiro negativo
            break
    if entra is None:
        return None
    razao, sai = None, None
    for i in range(m):
        if T[i][entra] > 0:
            r = ct.d(T[i][ncols], T[i][entra])
            if razao is None or r < razao:
                razao, sai = r, i
    if sai is None:
        return "ilimitado"
    piv = T[sai][entra]
    for j in range(ncols + 1):
        if T[sai][j] != 0:
            T[sai][j] = ct.d(T[sai][j], piv)
    for i in range(m + 1):
        if i == sai or T[i][entra] == 0:
            continue
        f = T[i][entra]
        for j in range(ncols + 1):
            if T[sai][j] != 0:
                T[i][j] = T[i][j] - ct.m(f, T[sai][j])
    base[sai] = entra
    return (entra, sai)


def forma_quadro(c, A, b, ct):
    """O Simplex do capítulo 09, reescrito aqui para poder ser instrumentado.

    A etapa 03 NÃO é tocada (D2) — ela continua publicada e serve de oráculo.
    Esta cópia existe só para que as duas formas usem a mesma primitiva.
    """
    m, n = len(A), len(c)
    T = [[F(x) for x in A[i]] + [F(1) if k == i else F(0) for k in range(m)] + [F(b[i])]
         for i in range(m)]
    T.append([F(-x) for x in c] + [F(0)] * m + [F(0)])
    base = list(range(n, n + m))
    trajetoria = []
    while True:
        p = _pivo_quadro(T, base, m, n, ct)
        if p is None:
            break
        if p == "ilimitado":
            return {"status": "ilimitado"}
        trajetoria.append(p)
    x = [F(0)] * n
    for i, col in enumerate(base):
        if col < n:
            x[col] = T[i][n + m]
    # A densidade do QUADRO ao final. É a outra metade da explicação: o quadro
    # começa com a esparsidade do modelo e a PERDE ao pivotear — cada eliminação
    # transforma zeros em não-zeros, e o custo da iteração seguinte sobe junto.
    # O fenômeno tem nome na literatura: preenchimento (*fill-in*).
    nz = sum(1 for i in range(m + 1) for j in range(n + m) if T[i][j] != 0)
    return {"status": "otimo", "x": x, "valor": T[m][n + m], "base": sorted(base),
            "trajetoria": trajetoria, "densidade_quadro": F(nz, (m + 1) * (n + m))}


def forma_revisada(c, A, b, ct):
    """A mesma coisa, mantendo B⁻¹ em vez do quadro inteiro.

    A diferença que o capítulo 11 explica está em UMA linha: o custo reduzido
    sai de `c_j - yᵀa_j`, calculado sobre a COLUNA ORIGINAL de A, que continua
    esparsa a iteração inteira. O quadro, ao pivotear, preenche os zeros — e
    perde a esparsidade que o modelo tinha.
    """
    m, n = len(A), len(c)
    # colunas originais, guardadas ESPARSAS: só os não-zeros.
    col = []
    for j in range(n):
        col.append([(i, F(A[i][j])) for i in range(m) if A[i][j] != 0])
    for j in range(m):                       # colunas de folga
        col.append([(j, F(1))])
    custo = [F(x) for x in c] + [F(0)] * m

    Binv = [[F(1) if i == k else F(0) for k in range(m)] for i in range(m)]
    base = list(range(n, n + m))
    xb = [F(x) for x in b]
    trajetoria = []

    while True:
        # y = c_B' B⁻¹  — o preço-sombra do capítulo 12, aqui como ferramenta.
        y = [sum((ct.m(custo[base[i]], Binv[i][k]) for i in range(m)), F(0)) for k in range(m)]
        entra = None
        for j in range(n + m):
            if j in base:
                continue
            # SÓ os não-zeros da coluna original entram na conta. É aqui que a
            # esparsidade vira economia, e é a linha que o capítulo explica.
            zj = sum((ct.m(y[i], a) for i, a in col[j]), F(0))
            if zj - custo[j] < 0:
                entra = j
                break
        if entra is None:
            break

        d = [sum((ct.m(Binv[i][k], a) for k, a in col[entra]), F(0)) for i in range(m)]
        razao, sai = None, None
        for i in range(m):
            if d[i] > 0:
                r = ct.d(xb[i], d[i])
                if razao is None or r < razao:
                    razao, sai = r, i
        if sai is None:
            return {"status": "ilimitado"}

        # Refatorar: atualizar B⁻¹ e x_B pelo pivô. É o "product form of the
        # inverse" na sua versão explícita — o capítulo diz que a versão de
        # produção guarda os fatores, não a matriz.
        piv = d[sai]
        Binv[sai] = [ct.d(v, piv) for v in Binv[sai]]
        xb[sai] = ct.d(xb[sai], piv)
        for i in range(m):
            if i == sai or d[i] == 0:
                continue
            f = d[i]
            Binv[i] = [Binv[i][k] - ct.m(f, Binv[sai][k]) for k in range(m)]
            xb[i] = xb[i] - ct.m(f, xb[sai])
        base[sai] = entra
        trajetoria.append((entra, sai))

    x = [F(0)] * n
    for i, c_ in enumerate(base):
        if c_ < n:
            x[c_] = xb[i]
    valor = sum((ct.m(custo[base[i]], xb[i]) for i in range(m)), F(0))
    # A densidade de B⁻¹ ao final. Não é enfeite: é a explicação medida do
    # resultado desta etapa. Enquanto A permanece esparsa a execução inteira,
    # B⁻¹ **preenche** — e é ele que esta implementação guarda explicitamente.
    nz = sum(1 for i in range(m) for k in range(m) if Binv[i][k] != 0)
    return {"status": "otimo", "x": x, "valor": valor, "base": sorted(base),
            "trajetoria": trajetoria, "densidade_Binv": F(nz, m * m)}


# ---------------------------------------------------------------------------
# D5 — Instâncias CONGELADAS antes de olhar resultado.
#
# A lista abaixo foi escrita antes da primeira execução, e TODAS as instâncias
# entram no relatório — não só as que mostrarem o efeito (D5, critério A19).
# Semente fixa; a geração é reprodutível em qualquer máquina.

SEMENTE = 20260813
INSTANCIAS = [
    # (rótulo, m restrições, n variáveis, densidade alvo)
    ("pequena densa",   4,   6, 1.0),
    ("pequena esparsa", 4,   6, 0.35),
    ("média densa",     8,  30, 1.0),
    ("média esparsa",   8,  30, 0.20),
    ("magra densa",    10, 120, 1.0),
    ("magra esparsa",  10, 120, 0.10),
]


def gerar(m, n, densidade, rng):
    """Instância viável e limitada por construção: A >= 0, b > 0, c > 0.

    D7 — "densidade" nomeia UMA coisa: a fração de entradas não nulas da matriz
    de restrições A. Não é densidade de B⁻¹, nem da base final. O relatório
    publica a densidade REALIZADA, que difere da alvo pelo sorteio.
    """
    A = [[rng.randint(1, 9) if rng.random() < densidade else 0 for _ in range(n)]
         for _ in range(m)]
    for i in range(m):                       # nenhuma linha vazia
        if not any(A[i]):
            A[i][rng.randrange(n)] = rng.randint(1, 9)
    for j in range(n):                       # nenhuma coluna vazia
        if not any(A[i][j] for i in range(m)):
            A[rng.randrange(m)][j] = rng.randint(1, 9)
    b = [rng.randint(20, 60) for _ in range(m)]
    c = [rng.randint(1, 20) for _ in range(n)]
    nz = sum(1 for i in range(m) for j in range(n) if A[i][j] != 0)
    return c, A, b, F(nz, m * n)


def medir(rotulo, c, A, b, densidade) -> dict:
    cq, cr = Contador(), Contador()
    q = forma_quadro(c, A, b, cq)
    r = forma_revisada(c, A, b, cr)

    # D4 — testemunha independente: a etapa 03, publicada e intocada, resolve a
    # mesma instância pelo seu próprio caminho. Se as três não concordarem, a
    # medição não vale.
    restr = [Restricao([F(A[i][j]) for j in range(len(c))], "<=", F(b[i]), f"r{i+1}")
             for i in range(len(A))]
    oraculo = resolver([F(x) for x in c], restr)

    concordam = (q["status"] == r["status"] == oraculo["status"] == "otimo"
                 and q["valor"] == r["valor"] == F(oraculo["valor"]))
    # D3 — trajetória de pivô IDÊNTICA, provada. Sem isso, as duas contagens
    # estariam medindo caminhos diferentes, e a comparação seria sobre a regra
    # de pivoteamento e não sobre a forma.
    mesma_trajetoria = q["trajetoria"] == r["trajetoria"]

    return {
        "instancia": rotulo,
        "m": len(A), "n": len(c),
        "densidade_alvo": None,
        "densidade_realizada": fmt(densidade),
        "densidade_float": round(float(densidade), 4),
        "iteracoes": len(q["trajetoria"]),
        "valor": fmt(q["valor"]),
        "concordam": concordam,
        "mesma_trajetoria_de_pivo": mesma_trajetoria,
        "ops_quadro": cq.total, "ops_revisada": cr.total,
        "mult_quadro": cq.mult, "div_quadro": cq.div,
        "mult_revisada": cr.mult, "div_revisada": cr.div,
        "razao_quadro_sobre_revisada": round(cq.total / cr.total, 3) if cr.total else None,
        "densidade_Binv": fmt(r["densidade_Binv"]),
        "densidade_Binv_float": round(float(r["densidade_Binv"]), 4),
        "densidade_quadro_final": fmt(q["densidade_quadro"]),
        "densidade_quadro_final_float": round(float(q["densidade_quadro"]), 4),
        "preenchimento": round(float(q["densidade_quadro"]) - float(densidade), 4),
    }


# ---------------------------------------------------------------------------
# D8 — "Estagna de verdade" tem limiar PRÉ-DECLARADO.
#
# Sem limiar escrito antes, "estagnou" vira adjetivo: qualquer execução com duas
# iterações mornas serve de exemplo. O limiar deste handbook é:
#
#   ESTAGNAÇÃO = 3 ou mais iterações CONSECUTIVAS sem melhora do objetivo.
#
# Três, e não duas, porque um empate isolado é rotina em vértice degenerado — o
# capítulo 10 mediu isso. E "sem melhora" é igualdade exata, não "melhora
# pequena": em `Fraction` não há ambiguidade sobre o que é zero.
LIMIAR_ESTAGNACAO = 3


def perfil_de_estagnacao(c, A, b) -> dict:
    """Quantas iterações passam sem o objetivo subir, e qual a maior sequência.

    Separa três fenômenos que o capítulo 10 deixou embolados:
      - ciclagem     — uma BASE já visitada volta (aqui: detectada, não suposta);
      - estagnação   — sequência longa e FINITA sem melhora;
      - lentidão     — muitas iterações, todas melhorando.
    """
    ct = Contador()
    m, n = len(A), len(c)
    T = [[F(x) for x in A[i]] + [F(1) if k == i else F(0) for k in range(m)] + [F(b[i])]
         for i in range(m)]
    T.append([F(-x) for x in c] + [F(0)] * m + [F(0)])
    base = list(range(n, n + m))

    valores, bases_vistas, repetiu = [T[m][n + m]], {tuple(sorted(base))}, False
    while True:
        p = _pivo_quadro(T, base, m, n, ct)
        if p is None or p == "ilimitado":
            break
        valores.append(T[m][n + m])
        chave = tuple(sorted(base))
        if chave in bases_vistas:
            repetiu = True
            break
        bases_vistas.add(chave)

    sem_melhora = [i for i in range(1, len(valores)) if valores[i] == valores[i - 1]]
    maior, atual = 0, 0
    for i in range(1, len(valores)):
        atual = atual + 1 if valores[i] == valores[i - 1] else 0
        maior = max(maior, atual)

    return {
        "iteracoes": len(valores) - 1,
        "iteracoes_sem_melhora": len(sem_melhora),
        "maior_sequencia_sem_melhora": maior,
        "estagna_pelo_limiar": maior >= LIMIAR_ESTAGNACAO,
        "base_repetiu": repetiu,
        "veredito": ("ciclagem" if repetiu else
                     "estagnação" if maior >= LIMIAR_ESTAGNACAO else
                     "lentidão" if len(valores) - 1 > 10 else "normal"),
    }


# ---------------------------------------------------------------------------
# D6 — O resíduo é medido com DESCONFIANÇA declarada.
#
# A mesma instância em `Fraction` e em `float`. O que interessa não é "o float
# erra" — todo mundo sabe. É QUANTO, e se o erro chega a mudar o VEREDITO.

def fracao_contra_float(c, A, b) -> dict:
    exato = forma_quadro(c, A, b, Contador())
    ct = Contador()
    m, n = len(A), len(c)
    Tf = [[float(x) for x in A[i]] + [1.0 if k == i else 0.0 for k in range(m)] + [float(b[i])]
          for i in range(m)]
    Tf.append([-float(x) for x in c] + [0.0] * m + [0.0])
    basef = list(range(n, n + m))
    passos = 0
    while passos < 500:
        p = _pivo_quadro(Tf, basef, m, n, ct)
        if p is None or p == "ilimitado":
            break
        passos += 1

    v_exato, v_float = exato["valor"], Tf[m][n + m]
    erro = abs(float(v_exato) - v_float)
    return {
        "valor_exato": fmt(v_exato),
        "valor_float": v_float,
        "erro_absoluto": erro,
        "erro_relativo": erro / abs(float(v_exato)) if v_exato != 0 else None,
        "mesma_base": sorted(basef) == exato["base"],
        "mesmas_iteracoes": passos == len(exato["trajetoria"]),
        "iteracoes_exato": len(exato["trajetoria"]),
        "iteracoes_float": passos,
        # A DESCONFIANÇA DECLARADA: um erro pequeno no VALOR não garante que o
        # veredito seja o mesmo. Base diferente = plano diferente, ainda que o
        # lucro coincida até a última casa que se olhou.
        "veredito_mudou": sorted(basef) != exato["base"],
    }


if __name__ == "__main__":
    rng = random.Random(SEMENTE)
    linhas = []
    for rotulo, m, n, dens in INSTANCIAS:
        c, A, b, realizada = gerar(m, n, dens, rng)
        r = medir(rotulo, c, A, b, realizada)
        r["densidade_alvo"] = dens
        linhas.append(r)

    print("FORMA REVISADA CONTRA QUADRO — mesmas instâncias, mesma trajetória de pivô")
    print("=" * 100)
    print(f"{'instância':<18}{'m':>4}{'n':>5}{'dens A':>8}{'quadro fim':>12}"
          f"{'B⁻¹ fim':>9}{'iter':>6}{'ops quadro':>12}{'ops revis.':>12}{'quadro/revis.':>15}")
    print("-" * 106)
    for r in linhas:
        print(f"{r['instancia']:<18}{r['m']:>4}{r['n']:>5}{r['densidade_float']:>8.2f}"
              f"{r['densidade_quadro_final_float']:>12.2f}{r['densidade_Binv_float']:>9.2f}"
              f"{r['iteracoes']:>6}{r['ops_quadro']:>12}{r['ops_revisada']:>12}"
              f"{r['razao_quadro_sobre_revisada']:>15}")
    print()
    print(f"  todas concordam com o oráculo (etapa 03): {all(r['concordam'] for r in linhas)}")
    print(f"  todas com a MESMA trajetória de pivô     : {all(r['mesma_trajetoria_de_pivo'] for r in linhas)}")
    print(f"  semente: {SEMENTE} · convenção: contam-se multiplicações e divisões;")
    print("  multiplicação por zero não é executada nem contada, nas DUAS formas.")

    # As duas medições que servem aos objetivos O4 e O5 do capítulo 11.
    rng2 = random.Random(SEMENTE + 1)
    c2, A2, b2, dens2 = gerar(12, 60, 0.30, rng2)
    est = perfil_de_estagnacao(c2, A2, b2)

    # SEGUNDA TENTATIVA, declarada: uma instância DELIBERADAMENTE degenerada —
    # cinco restrições passando pelo mesmo vértice (2,2). Se nem ela estagnar
    # pelo limiar pré-declarado, o resultado negativo é publicado como tal, e o
    # limiar NÃO é baixado para o exemplo caber. Baixá-lo seria ajustar até
    # ficar verde, que é o sinal de parada D9.5 da ADR 0013.
    est_degenerada = perfil_de_estagnacao(
        [2, 3], [[1, 1], [1, 2], [1, 0], [0, 1], [3, 2]], [4, 6, 2, 2, 10])
    num = fracao_contra_float(c2, A2, b2)

    print()
    print("ESTAGNAÇÃO, LENTIDÃO E CICLAGEM — separadas por limiar pré-declarado")
    print("=" * 106)
    print(f"  limiar: {LIMIAR_ESTAGNACAO} iterações consecutivas sem melhora (declarado antes de medir)")
    print(f"  iterações: {est['iteracoes']} · sem melhora: {est['iteracoes_sem_melhora']}"
          f" · maior sequência: {est['maior_sequencia_sem_melhora']}")
    print(f"  base repetiu (ciclagem): {est['base_repetiu']} · VEREDITO: {est['veredito']}")
    print(f"  tentativa 2, degenerada de propósito (5 restrições no mesmo vértice):")
    print(f"    iterações: {est_degenerada['iteracoes']} · maior sequência sem melhora:"
          f" {est_degenerada['maior_sequencia_sem_melhora']} · VEREDITO: {est_degenerada['veredito']}")
    print(f"  RESULTADO NEGATIVO PUBLICADO: nenhuma das duas atinge o limiar de"
          f" {LIMIAR_ESTAGNACAO}. O limiar não foi baixado.")
    print()
    print("FRAÇÃO CONTRA PONTO FLUTUANTE — a dívida do capítulo 10, item 4")
    print("=" * 106)
    print(f"  valor exato: {num['valor_exato']} · valor em float: {num['valor_float']}")
    print(f"  erro absoluto: {num['erro_absoluto']:.3e} · relativo: {num['erro_relativo']:.3e}")
    print(f"  iterações: {num['iteracoes_exato']} (exato) contra {num['iteracoes_float']} (float)")
    print(f"  mesma base ao final: {num['mesma_base']} · O VEREDITO MUDOU: {num['veredito_mudou']}")

    saida = {"semente": SEMENTE, "instancias_declaradas": INSTANCIAS, "medicoes": linhas,
             "limiar_estagnacao": LIMIAR_ESTAGNACAO, "estagnacao": est, "estagnacao_degenerada": est_degenerada, "numerico": num}
    (AQUI / "resultados-revisado.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if not all(r["concordam"] for r in linhas):
        raise SystemExit("✗ alguma instância divergiu do oráculo — a medição não vale")
    if not all(r["mesma_trajetoria_de_pivo"] for r in linhas):
        raise SystemExit("✗ trajetórias de pivô diferentes — a comparação mediria a regra, não a forma")
