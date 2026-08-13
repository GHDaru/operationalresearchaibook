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

from complexidade import (AMOSTRAS_ALEATORIAS, AMOSTRAS_PERTURBACAO, MAGNITUDES,
                          TAMANHOS_ALEATORIOS, perfil_aleatorio, perfil_de_perturbacao,
                          pior_caso, varredura_em_n)

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
            # Robusto: 200/200 nas duas magnitudes pequenas, e 25/25 de n=4 a n=8.
            assert p["intactas"] == p["amostras"], \
                f"perturbação de {mag} mexeu no caminho — o capítulo diz que não mexe em nenhuma semente"
        elif mag >= F(1, 2):
            # NÃO `== 0`. A versão anterior deste teste assertava zero, e zero era
            # verdade nas 20 sementes escolhidas e falso na família: com 200, dois
            # caminhos sobrevivem. Assertar o extremo de uma amostra é a mesma
            # classe de defeito que publicar um sorteio — cometida DENTRO do teste
            # que existia para pegá-la.
            assert p["intactas"] * 20 < p["amostras"], \
                f"perturbação de {mag} deveria encurtar na esmagadora maioria das sementes"


ROTULOS = {"1/1000": "0,1%", "1/100": "1%", "1/10": "10%", "1/4": "25%", "1/2": "50%"}


def test_a_tabela_de_perturbacao_esta_no_capitulo(texto):
    """Cada linha da tabela, inteira — mediana e caminhos intactos."""
    for mag in MAGNITUDES:
        p = perfil_de_perturbacao(N_PERT, mag)
        alvo = ROTULOS[str(mag)]
        intactas = f"{p['intactas']}/{p['amostras']}"
        linha_a = f"| {alvo} | **{p['mediana']}** | **{intactas}** |"
        linha_b = f"| {alvo} | **{p['mediana']}** | {intactas} |"
        assert linha_a in texto or linha_b in texto, \
            f"linha de perturbação {alvo} não confere com a medição: {p}"


def test_o_capitulo_nao_publica_extremo_de_amostra(texto):
    """Mínimo e máximo da perturbação são estatísticas de ordem, e não vão à página.

    O máximo da linha de 50% vai de 47 para 63 só por passar de 20 para 200
    sementes. Publicá-lo seria publicar ruído com cara de medição.
    """
    for mag in MAGNITUDES:
        p = perfil_de_perturbacao(N_PERT, mag)
        alvo = ROTULOS[str(mag)]
        assert f"| {alvo} | {p['minimo']} ·" not in texto, \
            f"a linha {alvo} voltou a publicar o mínimo da amostra"


@pytest.mark.parametrize("mag", [F(1, 100), F(1, 10)])
def test_a_varredura_em_n_esta_no_capitulo(texto, mag):
    """O eixo em que a análise suavizada faz a sua afirmação."""
    rotulo = ROTULOS[str(mag)]
    celulas = " | ".join(
        (f"**{l['intactas']}/{l['amostras']}**" if mag <= F(1, 100) else f"{l['intactas']}/{l['amostras']}")
        for l in varredura_em_n(mag)
    )
    assert f"| {rotulo} | {celulas} |" in texto, \
        f"a varredura em n para {rotulo} não confere: {varredura_em_n(mag)}"


def test_a_um_por_cento_o_caminho_sobrevive_em_todos_os_tamanhos():
    """A afirmação central, no eixo que a tabela de n=6 não alcança."""
    for l in varredura_em_n(F(1, 100)):
        assert l["intactas"] == l["amostras"], \
            f"a 1%, n={l['n']} quebrou o caminho — o capítulo diz que não quebra em nenhum tamanho"


def test_a_dez_por_cento_a_fragilidade_cresce_com_n():
    """A direção prevista pela análise suavizada, medida — e a favor dela."""
    fracoes = [l["intactas"] for l in varredura_em_n(F(1, 10))]
    assert fracoes[0] > fracoes[-1], "a 10%, o caminho deveria quebrar MAIS nos cubos maiores"


def test_o_capitulo_declara_quantas_sementes(texto):
    """A assimetria que a primeira revisão pegou: uma tabela declarava amostras, a outra não."""
    assert f"{AMOSTRAS_PERTURBACAO} sementes por magnitude" in texto, \
        "o capítulo publica a distribuição sem dizer sobre quantas sementes"
    assert f"{AMOSTRAS_ALEATORIAS} amostras por tamanho" in texto, \
        "o capítulo publica o perfil aleatório sem dizer sobre quantas amostras"


def test_o_capitulo_declara_o_modelo_de_perturbacao(texto):
    """Sem isto, quem reproduzir com ruído aditivo denso conclui que o livro errou.

    A perturbação é multiplicativa, relativa, entrada a entrada, e PRESERVA os
    zeros da matriz triangular do cubo. Preencher os zeros com valores da ordem
    dos não nulos derruba o caminho — e não é uma perturbação pequena, porque as
    variáveis do cubo chegam a 10ⁿ.
    """
    assert "padrão de zeros é preservado" in texto
    assert "cada coeficiente" in texto and "não nulo" in texto


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
    cubo = f"{p['pior_caso_construido']:,}".replace(",", ".")
    linha = f"| {n} | **{p['mediana']}** | {p['maximo']} | {cubo} |"
    assert linha in texto, f"linha do perfil aleatório n={n} não confere com a medição"


def test_ate_a_pior_das_amostras_fica_ordens_de_grandeza_abaixo_do_cubo():
    """A afirmação central do capítulo, e agora ela é sobre o PIOR, não a mediana.

    O nome anterior deste teste dizia "ordens de grandeza" e assertava um fator
    4 sobre a mediana — em n=5 isso era `8 < 31`, que nenhuma medição plausível
    violaria. A asserção certa é sobre o extremo, e em duas ordens de grandeza a
    partir do tamanho em que a diferença já é gritante.
    """
    razoes = []
    for n in TAMANHOS_ALEATORIOS:
        p = perfil_aleatorio(n)
        assert p["maximo"] * 5 < p["pior_caso_construido"], \
            f"n={n}: a pior das {p['amostras']} amostras custou {p['maximo']}, e o cubo {p['pior_caso_construido']}"
        razoes.append(F(p["pior_caso_construido"], p["maximo"]))

    # A afirmação do capítulo não é "a distância é grande" — é que ela **abre**.
    assert razoes == sorted(razoes), f"a distância deveria crescer com n, e deu {razoes}"
    assert razoes[-1] > 10_000, \
        f"no maior tamanho medido a distância deveria passar de quatro ordens de grandeza, e deu {float(razoes[-1]):.0f}×"


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


# --- B2: a Síntese e a Leitura executiva também são texto publicado -----------
#
# Treze das dezenove mutações que a revisão da medição conseguiu passar estavam
# nessas duas seções. E o risco não era teórico: a correção anterior teve de
# atualizar a MESMA medição em três lugares à mão — tabela, Síntese e Leitura
# executiva — e esquecer um teria deixado a suíte verde com o capítulo se
# contradizendo. O selo 🔵 diz "teste que compara ao texto publicado", e essas
# duas seções são texto publicado.

def _secao(texto: str, titulo: str) -> str:
    inicio = texto.index(titulo)
    resto = texto[inicio + len(titulo):]
    fim = resto.find("\n## ")
    return resto if fim < 0 else resto[:fim]


@pytest.fixture(scope="module")
def sintese(texto):
    return _secao(texto, "## Síntese — o que levar")


@pytest.fixture(scope="module")
def executiva(texto):
    return _secao(texto, "### Leitura executiva")


def test_a_sintese_repete_os_numeros_medidos(sintese):
    p1 = perfil_de_perturbacao(N_PERT, F(1, 100))
    assert f"{p1['intactas']} de {p1['amostras']}" in sintese.replace("**", ""), \
        "a Síntese cita a fração de caminhos intactos e ela não confere com a medição"
    assert f"{AMOSTRAS_PERTURBACAO} sementes por magnitude" in sintese
    pior = perfil_aleatorio(TAMANHOS_ALEATORIOS[-1])
    assert f"custou {pior['maximo']}" in sintese, \
        "a Síntese cita a pior instância aleatória e ela não confere"
    assert f"{2 ** N_PERT - 1} pivôs" in sintese


def test_a_leitura_executiva_repete_os_numeros_medidos(executiva):
    assert f"{AMOSTRAS_PERTURBACAO} sementes por" in executiva
    pior = perfil_aleatorio(TAMANHOS_ALEATORIOS[-1])
    assert f"custou {pior['maximo']}" in executiva, \
        "a Leitura executiva cita a pior instância aleatória e ela não confere"
    assert f"os {2 ** N_PERT - 1} pivôs" in executiva


def test_o_intervalo_de_n_do_pior_caso_e_o_mesmo_em_toda_a_pagina(texto):
    """`n de 2 a 7` aparece na tabela, na Síntese e na Leitura executiva."""
    assert texto.count("$n = 2$ a $n = 7$") + texto.count("$n$ de 2 a 7") >= 2
    assert "a $n = 9$" not in texto and "de 2 a 9" not in texto
