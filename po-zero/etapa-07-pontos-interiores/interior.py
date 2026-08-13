"""Atravessar em vez de contornar — o mesmo ótimo, alcançado por dentro.

Etapa que ancora o capítulo 14. Implementa **escalonamento afim**, que é o
método interior mais curto que existe e o suficiente para o capítulo mostrar o
que precisa mostrar. Não é o método de Karmarkar nem um *primal-dual* de
mercado; é o esqueleto deles, e o capítulo diz isso.

TRÊS COISAS SÃO MEDIDAS:

1. **A trajetória.** O Simplex anda pelas quinas; este anda por dentro. Os
   pontos intermediários são registrados, e nenhum deles é vértice.

2. **A chegada ao mesmo lugar.** Na montadora, o método interior converge para o
   mesmo $(8, 2)$ que o Simplex encontrou em 2 pivôs — por um caminho que não
   passa por vértice nenhum.

3. **O que muda quando há mais de um ótimo.** Aqui os dois métodos discordam, e a
   discordância é a lição do capítulo: o Simplex devolve **um vértice**; o método
   interior converge para o **meio da face ótima**, que não é vértice e não é
   uma "solução básica". Quem lê a resposta esperando vértice quebra.

PONTO FLUTUANTE, DECLARADO. As outras etapas deste handbook usam `Fraction` e
aritmética exata. Esta **não pode**: método interior é iterativo e converge a um
limite, então o resultado é aproximado por natureza — não por descuido de
implementação. É o primeiro lugar do livro em que isso acontece, e o capítulo 14
faz disso conteúdo em vez de rodapé. Todos os números publicados são arredondados
na saída, e a tolerância usada é declarada.

Rode com: python3 interior.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

AQUI = Path(__file__).parent
TOLERANCIA = 1e-9
MAX_ITER = 200
PASSO = 0.9          # fração do passo até a fronteira; < 1 mantém o ponto interior


def para_padrao(c, A, b):
    """max c'x s.a. Ax <= b, x >= 0  ->  forma padrão com folgas: Ax = b, x >= 0."""
    m, n = A.shape
    A_pad = np.hstack([A, np.eye(m)])
    c_pad = np.concatenate([c, np.zeros(m)])
    return c_pad, A_pad, b


def escalonamento_afim(c, A, b, x0):
    """Sobe pelo interior, reescalando o espaço a cada passo.

    A ideia em uma frase: perto da fronteira o gradiente puro é inútil, porque
    qualquer passo grande sai da região. Então, a cada iteração, o espaço é
    **reescalado** para que o ponto atual fique longe de todas as paredes; no
    espaço reescalado dá para dar um passo grande na direção do gradiente; e o
    passo volta ao espaço original encolhido perto das paredes.

    É a diferença entre os dois mundos: o Simplex escolhe uma ARESTA; este
    escolhe uma DIREÇÃO, e a região decide o tamanho do passo.
    """
    x = x0.astype(float).copy()
    trajetoria = [x.copy()]
    tol_conv = TOLERANCIA * max(1.0, float(np.linalg.norm(c)))
    parada = "iterações esgotadas"

    for _ in range(MAX_ITER):
        D = np.diag(x)
        AD = A @ D
        # w resolve o sistema normal — é o "preço" no espaço reescalado, e é o
        # mesmo objeto dual do capítulo 12, visto de outro ângulo.
        w = np.linalg.solve(AD @ AD.T, AD @ (D @ c))
        r = c - A.T @ w                      # custos reduzidos
        dx = D @ (D @ r)

        # O CRITÉRIO DE PARADA, e a primeira versão dele estava errada de um jeito
        # instrutivo. Ela declarava ILIMITADO quando nenhuma componente de `dx`
        # era negativa — raciocínio correto em teoria (sem componente que zere,
        # o passo não encontra fronteira) e errado na prática, porque é
        # exatamente o que acontece PERTO DO ÓTIMO: as folgas já estão na casa
        # de 1e-6, `dx` fica todo minúsculo, e nenhuma componente é
        # negativa além da tolerância. O método convergia e a função dizia
        # "ilimitado".
        #
        # O critério certo é o resíduo reescalado ‖D·r‖, que é a medida de quão
        # longe o ponto está de satisfazer a otimalidade. Detectar ilimitado NÃO
        # é trabalho desta etapa — as instâncias aqui são limitadas por
        # construção, e o veredito `Unbounded` é assunto do capítulo 10.
        residuo = float(np.linalg.norm(D @ r))
        if residuo < tol_conv:
            parada = "resíduo reescalado abaixo da tolerância"
            break

        negativos = dx < -TOLERANCIA
        if not negativos.any():
            parada = "nenhuma direção limitante — convergiu numericamente"
            break

        alfa = PASSO * np.min(-x[negativos] / dx[negativos])
        novo = x + alfa * dx
        if np.linalg.norm(novo - x) < TOLERANCIA:
            parada = "passo abaixo da tolerância"
            break
        x = novo
        trajetoria.append(x.copy())

    return {"status": "otimo", "x": x, "trajetoria": trajetoria,
            "iteracoes": len(trajetoria) - 1, "parada": parada,
            "residuo": float(np.linalg.norm(np.diag(x) @ (c - A.T @ w)))}


def e_vertice(x_decisao, A, b, tol=1e-6) -> bool:
    """Um ponto do plano é vértice quando DUAS restrições (contando os eixos)
    estão apertadas nele. É o critério do capítulo 08, aplicado numericamente."""
    apertadas = int(np.sum(np.abs(A @ x_decisao - b) < tol)) + int(np.sum(np.abs(x_decisao) < tol))
    return apertadas >= len(x_decisao)


def rodar(nome, c, A, b, x0):
    c_pad, A_pad, _ = para_padrao(c, A, b)
    r = escalonamento_afim(c_pad, A_pad, b, x0)
    n = len(c)
    xd = r["x"][:n]
    return {
        "instancia": nome,
        "iteracoes": r["iteracoes"],
        "parada": r["parada"],
        "residuo": round(float(r["residuo"]), 12),
        "ponto": [round(float(v), 6) for v in xd],
        "valor": round(float(c @ xd), 6),
        "chegou_em_vertice": bool(e_vertice(xd, A, b)),
        "trajetoria": [[round(float(v), 4) for v in p[:n]] for p in r["trajetoria"]],
        "algum_intermediario_e_vertice": any(
            e_vertice(p[:n], A, b) for p in r["trajetoria"][:-1]),
    }


if __name__ == "__main__":
    # 1. A montadora dos capítulos 07 a 13 — ótimo único em (8, 2).
    c1 = np.array([100.0, 150.0])
    A1 = np.array([[1.0, 1.0], [1.0, 2.0]])
    b1 = np.array([10.0, 12.0])
    x01 = np.array([1.0, 1.0, 8.0, 9.0])           # interior: folgas positivas
    montadora = rodar("montadora — ótimo único", c1, A1, b1, x01)

    # 2. A marcenaria do cap10.exC — o segmento de ótimos entre (4,0) e (2,3).
    #    Aqui os dois métodos DISCORDAM, e é o ponto do capítulo.
    c2 = np.array([6.0, 4.0])
    A2 = np.array([[3.0, 2.0], [1.0, 1.0]])
    b2 = np.array([12.0, 5.0])
    x02 = np.array([1.0, 1.0, 7.0, 3.0])
    marcenaria = rodar("marcenaria — segmento de ótimos", c2, A2, b2, x02)

    print("ESCALONAMENTO AFIM — atravessar em vez de contornar")
    print("=" * 78)
    for r in (montadora, marcenaria):
        print(f"  {r['instancia']}")
        print(f"    iterações: {r['iteracoes']}  ·  ponto {r['ponto']}  ·  valor {r['valor']}")
        print(f"    chegou em vértice: {r['chegou_em_vertice']}")
        print(f"    algum ponto intermediário é vértice: {r['algum_intermediario_e_vertice']}")
        print(f"    trajetória (primeiros 4): {r['trajetoria'][:4]}")
    # O NÚMERO QUE É A LIÇÃO, e não o defeito. O Simplex devolve 1100 exato,
    # em fração. Este devolve 1099,99982 — e não por implementação desleixada:
    # método interior converge a um LIMITE e nunca o atinge. A distância abaixo
    # é o preço declarado dessa diferença de natureza.
    erro = abs(montadora["valor"] - 1100)
    dist = float(np.linalg.norm(np.array(montadora["ponto"]) - np.array([8.0, 2.0])))
    print()
    print("A DIFERENÇA DE NATUREZA — o Simplex chega; este se aproxima")
    print("=" * 78)
    print(f"  Simplex (fração exata): ponto (8, 2) · valor 1100 · 2 pivôs")
    print(f"  interior (ponto flutuante): ponto {montadora['ponto']} · valor {montadora['valor']}")
    print(f"  distância ao vértice: {dist:.3e} · erro no valor: {erro:.3e}")
    print(f"  parada: {montadora['parada']}")
    print()
    print(f"  tolerância: {TOLERANCIA} · passo até a fronteira: {PASSO} · máximo de iterações: {MAX_ITER}")

    saida = {"tolerancia": TOLERANCIA, "passo": PASSO,
             "montadora": montadora, "marcenaria": marcenaria,
             "distancia_ao_vertice": dist, "erro_no_valor": erro}
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # A etapa só entrega se as afirmações do capítulo se sustentarem. A
    # tolerância aqui é 1e-3 e NÃO é frouxidão: é a afirmação de que o método
    # chega perto, não de que chega. Exigir 0 seria exigir do método algo que
    # ele não promete — e foi o que a primeira versão desta linha fez, falhando
    # por 1,8e-4 num resultado correto.
    if erro > 1e-3:
        raise SystemExit("✗ o método interior não chegou perto do ótimo do Simplex na montadora")
    if erro == 0:
        raise SystemExit("✗ erro exatamente zero — desconfie: método interior converge a um limite")
    if montadora["algum_intermediario_e_vertice"] or marcenaria["algum_intermediario_e_vertice"]:
        raise SystemExit("✗ a trajetória passou por vértice — não é 'por dentro'")
    if marcenaria["chegou_em_vertice"]:
        raise SystemExit("✗ com segmento de ótimos, o método interior parou num vértice — sem lição")
