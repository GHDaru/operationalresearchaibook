"""O capítulo 05 e a sua bateria têm de bater com a medição.

O selo 🔵 do capítulo 05 depende deste arquivo, e o portão de maturidade cobra
isso literalmente: capítulo "medido" sem teste que leia o `.md` dele falha o
build. A regra existe porque um selo que ninguém verifica é decoração.

O vínculo é feito nas **duas direções**, que é o que separa este teste de um
teste decorativo:

  1. Os números que o texto publica **aparecem** no texto. Se alguém apagar um,
     o teste fica vermelho.
  2. A ressalva que acompanha o resultado negativo **continua lá**. Este é o
     ponto sensível do capítulo: ele mede que perturbar o cubo em 1% não muda
     nada, e essa medição NÃO refuta a análise suavizada de 2004. Se a ressalva
     sumir numa revisão de estilo, o capítulo passa a afirmar algo que a medição
     não sustenta — e nenhum outro portão pegaria.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

import pytest

from complexidade import (AMOSTRAS_PERTURBACAO, MAGNITUDES, TAMANHOS_ALEATORIOS,
                          perfil_aleatorio, perfil_de_perturbacao, pior_caso)

RAIZ = Path(__file__).resolve().parents[2]
CAPITULO = RAIZ / "livro/capitulos/05-complexidade.md"
N_PERT = 6


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def exercicios():
    return {e["id"]: e for e in json.loads((RAIZ / "livro/exercicios.json").read_text(encoding="utf-8"))}


@pytest.mark.parametrize("n", range(2, 8))
def test_o_pior_caso_e_exatamente_dois_elevado_a_n_menos_um(n):
    p = pior_caso(n)
    assert p["status"] == "otimo"
    assert p["pivos"] == 2 ** n - 1


@pytest.mark.parametrize("n", range(2, 8))
def test_a_tabela_do_pior_caso_esta_no_capitulo(texto, n):
    p = pior_caso(n)
    linha = f"| {n} | {2 ** n} | **{p['pivos']}** | {2 ** n - 1} |"
    assert linha in texto, f"linha do pior caso n={n} não confere com a medição"


def test_perturbacao_pequena_nao_muda_nada():
    """O resultado negativo, que é o que este capítulo tem de mais próprio.

    A asserção é sobre a DISTRIBUIÇÃO, e não sobre um sorteio: em 0,1% e em 1%,
    **todas** as sementes devolvem o caminho puro. Se um dia isso mudar — outra
    regra de pivoteamento, outra construção do cubo —, este teste é o que avisa.

    A versão anterior deste teste checava uma semente por magnitude, e foi por
    isso que a linha de 10% chegou a ser publicada como "63" quando o correto
    era "63 na maioria das vezes". Um teste que confere um sorteio herda a
    fragilidade do sorteio.
    """
    puro = 2 ** N_PERT - 1
    for mag in MAGNITUDES:
        p = perfil_de_perturbacao(N_PERT, mag)
        assert p["maximo"] <= puro, f"perturbação de {mag} não pode ALONGAR o caminho"
        if mag <= F(1, 100):
            assert p["intactas"] == p["amostras"], \
                f"perturbação de {mag} mexeu no caminho — o capítulo diz que não mexe em nenhuma semente"
        elif mag >= F(1, 2):
            assert p["intactas"] == 0, f"perturbação de {mag} deveria encurtar em todas as sementes"


def test_a_tabela_de_perturbacao_esta_no_capitulo(texto):
    """Cada linha da tabela, inteira — mínimo, mediana, máximo e intactas."""
    rotulos = {"1/1000": "0,1%", "1/100": "1%", "1/10": "10%", "1/4": "25%", "1/2": "50%"}
    for mag in MAGNITUDES:
        p = perfil_de_perturbacao(N_PERT, mag)
        alvo = rotulos[str(mag)]
        intactas = f"{p['intactas']}/{p['amostras']}"
        linha_a = f"| {alvo} | {p['minimo']} · **{p['mediana']}** · {p['maximo']} | **{intactas}** |"
        linha_b = f"| {alvo} | {p['minimo']} · **{p['mediana']}** · {p['maximo']} | {intactas} |"
        assert linha_a in texto or linha_b in texto, \
            f"linha de perturbação {alvo} não confere com a medição: {p}"


def test_o_capitulo_declara_quantas_sementes(texto):
    """A assimetria que a revisão pegou: uma tabela declarava amostras, a outra não."""
    assert f"{AMOSTRAS_PERTURBACAO} sementes por magnitude" in texto, \
        "o capítulo publica a distribuição sem dizer sobre quantas sementes"


def test_a_ressalva_sobre_a_analise_suavizada_continua_no_capitulo(texto):
    """A medição é um resultado negativo estreito, e o texto tem de dizer isso.

    Sem estas três condições declaradas, o capítulo estaria dizendo que o
    resultado de Spielman & Teng está errado — o que a medição NÃO sustenta.
    """
    assert "não autoriza concluir" in texto
    assert "assintótico" in texto
    assert "esperança" in texto
    assert "gaussiana" in texto


@pytest.mark.parametrize("n", TAMANHOS_ALEATORIOS)
def test_o_perfil_aleatorio_esta_no_capitulo(texto, n):
    p = perfil_aleatorio(n)
    pior = f"{p['pior_caso_teorico']:,}".replace(",", ".")
    linha = f"| {n} | {p['minimo']} · **{p['mediana']}** · {p['maximo']} | {pior} |"
    assert linha in texto, f"linha do perfil aleatório n={n} não confere com a medição"


def test_a_mediana_fica_ordens_de_grandeza_abaixo_do_pior_caso():
    """A afirmação central do capítulo, medida em vez de retórica."""
    for n in TAMANHOS_ALEATORIOS:
        p = perfil_aleatorio(n)
        assert F(p["mediana"]) * 4 < p["pior_caso_teorico"]


def test_o_capitulo_nao_promete_o_que_a_medicao_nao_da(texto):
    """A ressalva sobre instância aleatória não ser instância real.

    O risco desta página é o leitor sair dela achando que "o Simplex é rápido"
    virou fato geral. As instâncias medidas têm uma receita, e a receita está
    declarada — o que a tabela sustenta é a NEGAÇÃO de uma inferência.
    """
    assert "problemas reais não são aleatórios" in texto
    assert "rode a sua" in texto


def test_a_bateria_do_capitulo_existe_com_tres_exercicios(exercicios):
    da_bateria = [e for e in exercicios if e.startswith("cap05.")]
    assert len(da_bateria) >= 3
