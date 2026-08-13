"""A rubrica do `cap03.exC` afirma um comportamento. Aqui ele é medido.

POR QUE ESTE ARQUIVO EXISTE, E O QUE ELE NÃO É.

O capítulo 03 não produz medição própria — ele é um capítulo de diagnóstico, e
os números que cita (R$ 350, R$ 403,33) são dos capítulos que os mediram. Por
isso ele nasce 🟡, e por isso **nenhum teste deste repositório lê o `.md` dele**:
o portão de maturidade trata "🟡 com teste que o leia" como incoerência, e está
certo.

O que sobrou sem dono foi outra coisa. A rubrica do `cap03.exC` afirma que, no
modelo da transportadora, o Simplex vai **colar `k` em 120.000** — e essa é uma
afirmação sobre a solução de um modelo, não uma opinião didática. Ela escapa dos
dois portões que poderiam pegá-la:

  1. O `verifica-otimos.mjs` só resolve modelos de **duas** variáveis. Este tem
     três (`c`, `k`, `t`).
  2. Ele foi isentado em `SEM_MODELO_DECLARADO` exatamente por isso — e uma
     isenção sem contrapartida é uma afirmação solta.

Então a conferência acontece aqui, em aritmética exata, sobre a **rubrica**. O
modelo é resolvido pelo Simplex da etapa 03, que é o mesmo que sustenta os selos
🔵 da Parte II: um número novo não entra no handbook por um caminho novo.

E há um segundo achado, que vale mais do que a conferência: com a variável de
decisão errada, o modelo recomenda **zero caminhões próprios**. Não é um detalhe
— é o dano do defeito ficando visível. O exercício ensina a prever o sintoma; o
teste garante que o sintoma medido é o que a rubrica diz.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]

# A etapa 01 não tem Simplex — ela é sobre formular. Emprestar o da etapa 03 é
# deliberado: reimplementar um solver só para conferir uma rubrica criaria uma
# segunda fonte da verdade, que é a classe de defeito que a ADR 0016 proíbe nos
# cadernos e que não tem por que ser tolerada aqui.
sys.path.insert(0, str(RAIZ / "po-zero/etapa-03-simplex"))

from quadro import Restricao, resolver  # noqa: E402

# O modelo tal como o enunciado do `cap03.exC` o escreve, com a variável errada
# (`k`) ainda dentro. Minimizar custo = maximizar o negativo do custo.
CUSTOS = [F(8500), F(23, 10), F(190)]   # c: R$/mês · k: R$/km · t: R$/terceirização
NOMES = ["c", "k", "t"]
RESTRICOES = [
    Restricao([F(0), F(1), F(0)], ">=", F(120000), "malha"),
    Restricao([F(1), F(0), F(0)], "<=", F(14), "garagem"),
    Restricao([F(-9000), F(1), F(-600)], "<=", F(0), "autonomia"),
]


@pytest.fixture(scope="module")
def solucao():
    r = resolver([-c for c in CUSTOS], [
        Restricao(list(x.coefs), x.sinal, x.b, x.rotulo) for x in RESTRICOES
    ], nomes=NOMES)
    assert r["status"] == "otimo"
    return dict(zip(NOMES, r["iteracoes"][-1].ponto))


@pytest.fixture(scope="module")
def exercicios():
    return {e["id"]: e for e in json.loads((RAIZ / "livro/exercicios.json").read_text(encoding="utf-8"))}


def test_o_modelo_cola_k_no_piso(solucao):
    """A afirmação literal da rubrica: `k` vai para o mínimo que a malha exige."""
    assert solucao["k"] == F(120000)


def test_com_a_variavel_errada_o_modelo_zera_a_frota_propria(solucao):
    """O dano do defeito, medido: R$/km terceirizado é 3× mais barato que próprio.

    8500/9000 ≈ 0,944 R$/km contra 190/600 ≈ 0,317 R$/km. O modelo, livre para
    escolher, não contrata nenhum caminhão — e reporta uma economia que ninguém
    executa, porque `k` não era decidível.
    """
    assert solucao["c"] == F(0)
    assert solucao["t"] == F(200)


def test_o_custo_declarado_confere(solucao):
    esperado = sum(c * solucao[n] for c, n in zip(CUSTOS, NOMES))
    assert esperado == F(314000)


def test_a_rubrica_ainda_afirma_o_que_foi_medido(exercicios):
    """O vínculo texto↔medição, na direção que costuma apodrecer.

    Se alguém reescrever a rubrica e trocar o piso, este teste fica vermelho —
    que é o único jeito de a isenção do `verifica-otimos.mjs` continuar honesta.
    """
    rubrica = exercicios["cap03.exC"]["resposta_guia"]
    assert "120.000" in rubrica
    assert "parâmetro" in rubrica
