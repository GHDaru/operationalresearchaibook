"""Os três padrões que cobrem a maior parte da Programação Linear aplicada.

Etapa que ancora o capítulo 15, e ela tem uma função diferente das anteriores:
não introduz método nenhum. Usa o Simplex da etapa 03, sem alteração, para
resolver **mistura**, **transporte** e **cobertura** — e para mostrar, com
número, o que acontece quando o padrão é escolhido errado.

A montadora dos capítulos 07 a 14 é um caso de **mix de produção**. Este capítulo
mostra que ela é uma instância de algo maior, e que reconhecer o padrão certo é o
que separa modelar de adivinhar.

TRÊS COISAS SÃO MEDIDAS:

1. **Os três padrões resolvidos**, em aritmética exata, com a resposta e a
   leitura de cada uma.
2. **O padrão escolhido errado.** A mesma situação de transporte, modelada como
   se fosse mix de produção — o modelo roda, devolve `Optimal`, e a resposta é
   **outra**. Nenhum erro de conta.
3. **A resposta que não responde à pergunta.** A cobertura, relaxada para
   contínua, devolve solução **fracionária**: meia estação. O modelo está certo e
   a pergunta era outra — é a porta de entrada da programação inteira.

Rode com: python3 padroes.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "etapa-03-simplex"))
from quadro import Restricao, resolver, fmt  # noqa: E402

AQUI = Path(__file__).parent


def minimizar(custos, restricoes, nomes=None) -> dict:
    """O `quadro.resolver` maximiza. Minimizar é maximizar o negativo.

    O sinal volta na saída para o capítulo não precisar explicar o truque duas
    vezes — e para ninguém publicar um custo negativo por descuido.
    """
    r = resolver([-c for c in custos], restricoes, nomes=nomes)
    if r["status"] != "otimo":
        return {"status": r["status"]}
    return {"status": "otimo", "ponto": r["ponto"],
            "valor": fmt(-F(r["valor"])), "pivos": r["pivos"]}


# ---------------------------------------------------------------------------
# 1. MISTURA — o padrão da ração, da liga metálica, do combustível.
#    Escolhe-se QUANTO de cada insumo, para atender exigências, ao menor custo.

def mistura() -> dict:
    """Ração animal: dois ingredientes, duas exigências nutricionais.

    A pergunta é de COMPRA, não de produção: quanto de cada insumo comprar. O
    objetivo é MINIMIZAR custo, e as restrições são de MÍNIMO (`>=`) — o oposto
    da montadora em ambos. É a primeira coisa que o leitor precisa reconhecer.
    """
    # milho: R$ 3/kg, 9 g de proteína, 2 g de gordura por kg
    # farelo: R$ 5/kg, 30 g de proteína, 1 g de gordura por kg
    # exigência por saco: >= 180 g de proteína, >= 24 g de gordura
    custos = [F(3), F(5)]
    restricoes = [
        Restricao([F(9), F(30)], ">=", F(180), "proteína (g)"),
        Restricao([F(2), F(1)], ">=", F(24), "gordura (g)"),
    ]
    r = minimizar(custos, restricoes, nomes=["milho", "farelo"])
    r["padrao"] = "mistura"
    r["pergunta"] = "quanto comprar de cada insumo para atender às exigências ao menor custo"
    return r


# ---------------------------------------------------------------------------
# 2. TRANSPORTE — o padrão da distribuição, da alocação, do escalonamento.
#    Escolhe-se QUANTO mandar de cada origem para cada destino.

def transporte() -> dict:
    """Duas fábricas, três centros. Seis variáveis, uma por par.

    A assinatura do padrão é a variável com DOIS índices: x[i][j] é quanto vai de
    i para j. Quem não reconhece isso costuma criar uma variável por fábrica e
    perder a informação de destino — que é exatamente o erro do item 3 abaixo.
    """
    # custo de enviar 1 unidade da fábrica i para o centro j
    custo = [[F(4), F(6), F(9)],
             [F(5), F(3), F(8)]]
    oferta = [F(30), F(40)]
    demanda = [F(20), F(25), F(25)]

    # variáveis na ordem x11 x12 x13 x21 x22 x23
    custos = [custo[i][j] for i in range(2) for j in range(3)]
    nomes = [f"x{i+1}{j+1}" for i in range(2) for j in range(3)]

    restricoes = []
    for i in range(2):                       # não mande mais do que a fábrica tem
        coefs = [F(1) if k // 3 == i else F(0) for k in range(6)]
        restricoes.append(Restricao(coefs, "<=", oferta[i], f"oferta da fábrica {i+1}"))
    for j in range(3):                       # atenda a demanda de cada centro
        coefs = [F(1) if k % 3 == j else F(0) for k in range(6)]
        restricoes.append(Restricao(coefs, ">=", demanda[j], f"demanda do centro {j+1}"))

    r = minimizar(custos, restricoes, nomes=nomes)
    r["padrao"] = "transporte"
    r["pergunta"] = "quanto mandar de cada origem para cada destino ao menor custo"
    r["rotulos"] = nomes
    return r


def transporte_com_padrao_errado() -> dict:
    """A MESMA situação, modelada como se fosse mix de produção.

    O erro é sedutor porque parece uma simplificação razoável: "cada fábrica
    manda um total, o custo médio de cada uma resolve". O modelo fica menor,
    roda, devolve `Optimal` — e responde a outra pergunta, porque PERDEU o
    destino. Nenhuma conta está errada.
    """
    # custo médio por fábrica, que é o que sobra quando o destino some
    medio = [(F(4) + F(6) + F(9)) / 3, (F(5) + F(3) + F(8)) / 3]
    restricoes = [
        Restricao([F(1), F(0)], "<=", F(30), "oferta da fábrica 1"),
        Restricao([F(0), F(1)], "<=", F(40), "oferta da fábrica 2"),
        Restricao([F(1), F(1)], ">=", F(70), "demanda total"),
    ]
    r = minimizar(medio, restricoes, nomes=["total da fábrica 1", "total da fábrica 2"])
    r["padrao"] = "mix de produção (ERRADO para esta situação)"
    r["custo_medio_usado"] = [fmt(m) for m in medio]
    return r


# ---------------------------------------------------------------------------
# 3. COBERTURA — o padrão da localização, da escala de plantão, do rateio.
#    Escolhe-se QUAIS abrir, e a resposta honesta é binária.

def cobertura() -> dict:
    """Quatro estações candidatas, cinco bairros a cobrir. Relaxada para contínua.

    O modelo é o clássico de cobertura: cada bairro precisa de pelo menos uma
    estação que o alcance. A variável DEVERIA ser binária — abre ou não abre —,
    mas este handbook ainda não tem programação inteira. Relaxando para contínua,
    o modelo roda e devolve fração.

    E é isso que se quer mostrar: o modelo está certo, a conta está certa, e a
    resposta **não responde à pergunta que foi feita**.
    """
    custo = [F(5), F(4), F(6), F(3)]         # custo de abrir cada estação
    # quais estações alcançam cada bairro
    alcance = [[1, 0, 1, 0],                 # bairro A
               [1, 1, 0, 0],                 # bairro B
               [0, 1, 1, 0],                 # bairro C
               [0, 0, 1, 1],                 # bairro D
               [0, 1, 0, 1]]                 # bairro E
    restricoes = [Restricao([F(a) for a in linha], ">=", F(1), f"bairro {chr(65+i)}")
                  for i, linha in enumerate(alcance)]
    # sem teto, a relaxação contínua não precisa de x <= 1 para este objetivo de
    # minimização — mas ele entra porque "abrir 1,4 estação" seria pior ainda.
    for j in range(4):
        coefs = [F(1) if k == j else F(0) for k in range(4)]
        restricoes.append(Restricao(coefs, "<=", F(1), f"estação {j+1} no máximo uma vez"))

    r = minimizar(custo, restricoes, nomes=[f"estação {j+1}" for j in range(4)])
    r["padrao"] = "cobertura (relaxada para contínua)"
    r["pergunta"] = "quais estações abrir para cobrir todos os bairros ao menor custo"
    r["fracionaria"] = any("/" in v for v in r.get("ponto", []))

    # A RESPOSTA DE VERDADE, por enumeração — 2⁴ = 16 subconjuntos, e o capítulo
    # não pode afirmar à mão o que dá para contar. Serve a dois propósitos: dizer
    # ao leitor qual é a decisão executável, e medir o BURACO entre a relaxação e
    # a realidade, que é o assunto de toda a Parte de programação inteira.
    melhor, escolha = None, None
    for mascara in range(1 << 4):
        aberto = [(mascara >> j) & 1 for j in range(4)]
        if all(sum(a * b for a, b in zip(linha, aberto)) >= 1 for linha in alcance):
            c = sum(custo[j] for j in range(4) if aberto[j])
            if melhor is None or c < melhor:
                melhor, escolha = c, [j + 1 for j in range(4) if aberto[j]]
    r["inteira"] = {"estacoes": escolha, "custo": fmt(melhor)}
    r["buraco"] = fmt(melhor - F(r["valor"]))
    return r


if __name__ == "__main__":
    m, t, terrado, c = mistura(), transporte(), transporte_com_padrao_errado(), cobertura()

    print("OS TRÊS PADRÕES, RESOLVIDOS")
    print("=" * 82)
    print(f"  MISTURA   · {m['pergunta']}")
    print(f"    milho e farelo: {m['ponto']} kg  ·  custo {m['valor']}  ({m['pivos']} pivôs)")
    print(f"  TRANSPORTE · {t['pergunta']}")
    print(f"    {dict(zip(t['rotulos'], t['ponto']))}")
    print(f"    custo {t['valor']}  ({t['pivos']} pivôs)")
    print(f"  COBERTURA · {c['pergunta']}")
    print(f"    relaxada: {c['ponto']}  ·  custo {c['valor']}  ·  fracionária: {c['fracionaria']}")
    print(f"    de verdade (por enumeração): estações {c['inteira']['estacoes']}  ·  custo {c['inteira']['custo']}")
    print(f"    buraco entre a relaxação e a decisão executável: {c['buraco']}")
    print()

    print("O PADRÃO ESCOLHIDO ERRADO — mesma situação, modelo menor, resposta outra")
    print("=" * 82)
    print(f"  custo médio por fábrica usado no lugar do custo por rota: {terrado['custo_medio_usado']}")
    print(f"  o modelo errado devolve custo {terrado['valor']} e diz `Optimal`")
    print(f"  o modelo certo   devolve custo {t['valor']}")
    dif = F(terrado["valor"]) - F(t["valor"])
    print(f"  diferença: {fmt(dif)}  ·  e o modelo errado NÃO diz quanto vai para cada centro")
    print()

    saida = {"mistura": m, "transporte": t, "transporte_errado": terrado, "cobertura": c,
             "diferenca_do_padrao_errado": fmt(dif)}
    (AQUI / "resultados.json").write_text(
        json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for nome, r in (("mistura", m), ("transporte", t), ("cobertura", c)):
        if r["status"] != "otimo":
            raise SystemExit(f"✗ o padrão {nome} não resolveu: {r['status']}")
    if dif == 0:
        raise SystemExit("✗ o padrão errado deu o mesmo custo — sem lição a extrair")
    if not c["fracionaria"]:
        raise SystemExit("✗ a cobertura relaxada saiu inteira — não demonstra a porta da inteira")
    if F(c["buraco"]) <= 0:
        raise SystemExit("✗ a relaxação não é limitante inferior estrito — sem buraco a mostrar")
