"""O capítulo tem de bater com a medição — e é o teste que decide, não a boa fé.

POR QUE ESTE ARQUIVO EXISTE, e a razão é um defeito de verdade.

O capítulo 12 foi escrito com duas faixas erradas: `[13/2, 12]` e `[10, 39/2]`,
quando o certo é `[6, 12]` e `[10, 20]`. Os números saíram de uma varredura de
meio em meio que media em que base o Simplex aterrissa, e não para que lado
direito a base continua ótima. Nove portões do livro passaram verdes por cima
disso, porque nenhum deles sabia que o capítulo tinha número para conferir.

Era a SEGUNDA vez que um número entrava no livro sem portão: a primeira foi o
ótimo errado do `cap07.exC`, que produziu o `verifica-otimos.mjs`. Defeito de
mesma classe pela segunda vez é defeito do pipeline, não do artefato — então a
correção não podia ser trocar dois números.

O que este arquivo faz: recalcula a medição e exige que **cada número que o
capítulo publica** apareça no texto na forma exata. Se a medição mudar e o
capítulo não, fica vermelho. Se alguém editar o capítulo à mão, fica vermelho.

Rode com: python -m pytest po-zero/etapa-05-parte2/ -q
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path

import pytest

from dual import (confere_faixa, dual_explicito, faixa_de_custo,
                  faixa_de_validade, montadora, precos_sombra)

CAPITULO = Path(__file__).resolve().parents[2] / "livro/capitulos/12-dualidade.md"


@pytest.fixture(scope="module")
def instancia():
    return montadora()


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


def test_dualidade_forte(instancia):
    """Os dois problemas, resolvidos separadamente, chegam ao mesmo valor."""
    lucros, restricoes, _ = instancia
    primal = precos_sombra(lucros, restricoes)
    dual = dual_explicito(lucros, restricoes)
    assert dual["valor_dual"] is not None
    assert F(primal["valor"]) == F(dual["valor_dual"])


def test_precos_sombra_sao_os_publicados(instancia, texto):
    lucros, restricoes, _ = instancia
    precos = precos_sombra(lucros, restricoes)["precos"]
    assert precos == {"CPUs": "50", "pentes de memória de 16 GB": "50"}
    assert "R\\$/CPU" in texto and "R\\$/pente" in texto


@pytest.mark.parametrize("indice", [0, 1])
def test_faixa_confere_por_caminho_independente(instancia, indice):
    """NA fronteira o preço tem de acertar; ALÉM dela, tem de errar.

    Esta é a verificação que a versão por varredura não tinha. Uma faixa curta
    demais passa despercebida — o preço simplesmente acerta além dela.
    """
    lucros, restricoes, _ = instancia
    faixa = faixa_de_validade(lucros, restricoes, indice)
    c = confere_faixa(lucros, restricoes, indice, faixa)
    for lado in ("piso", "teto"):
        assert c[lado]["preco_acerta_na_fronteira"], f"{c['componente']}: faixa longa demais no {lado}"
        assert c[lado]["preco_erra_alem"], f"{c['componente']}: faixa curta demais no {lado}"


def test_faixas_de_estoque_estao_no_capitulo(instancia, texto):
    """Cada fronteira medida aparece no texto publicado, na forma exata."""
    lucros, restricoes, _ = instancia
    esperado = {"CPUs": ("6", "12"), "pentes de memória de 16 GB": ("10", "20")}
    for i in range(len(restricoes)):
        f = faixa_de_validade(lucros, restricoes, i)
        assert (f["pode_cair_ate"], f["pode_subir_ate"]) == esperado[f["componente"]]
        # A tabela do capítulo publica a faixa em linguagem natural ("de X a Y")
        # e o bloco de saída a publica no formato do script.
        assert f"[{f['pode_cair_ate']}, {f['pode_subir_ate']}]" in texto, \
            f"o capítulo não publica a faixa medida de {f['componente']}"


def test_faixas_de_custo(instancia):
    """A outra metade do relatório de sensibilidade — usada pelo capítulo 13."""
    lucros, restricoes, _ = instancia
    faixas = {c["produto"]: c for c in
              (faixa_de_custo(lucros, restricoes, j, f"x{j+1}") for j in range(len(lucros)))}
    assert (faixas["x1"]["pode_cair_ate"], faixas["x1"]["pode_subir_ate"]) == ("75", "150")
    assert (faixas["x2"]["pode_cair_ate"], faixas["x2"]["pode_subir_ate"]) == ("100", "200")
    assert faixas["x1"]["na_base"] and faixas["x2"]["na_base"]


def test_o_capitulo_nao_publica_as_faixas_antigas(texto):
    """Guarda contra o defeito exato que aconteceu.

    Um teste que só confere o valor certo passa verde num capítulo que publica
    o certo E o errado, em lugares diferentes — que é a forma pela qual uma
    correção parcial se disfarça de correção.
    """
    for errado in ("13/2", "6,5", "39/2", "19,5"):
        assert errado not in texto, f"o capítulo ainda publica a faixa antiga e errada: {errado}"


def test_o_prejuizo_do_telefonema(instancia, texto):
    """O número que o capítulo existe para impedir, refeito do zero."""
    from quadro import Restricao, resolver
    lucros, restricoes, _ = instancia
    z0 = F(resolver(lucros, restricoes)["valor"])
    # Compra de 10 CPUs a R$ 45: o estoque vai de 10 para 20.
    alt = [Restricao(list(r.coefs), r.sinal, r.b + (10 if i == 0 else 0), r.rotulo)
           for i, r in enumerate(restricoes)]
    z1 = F(resolver(lucros, alt)["valor"])
    assert z1 - z0 == 100                      # ganho real
    assert (z1 - z0) - 10 * 45 == -350         # prejuízo
    assert "R$ 350" in texto
