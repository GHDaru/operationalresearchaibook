"""Todo caderno do handbook é EXECUTADO — sem Jupyter, sem rede, contra o código de hoje.

Desenho decidido na [ADR 0016](../../adr/0016-cadernos-colab-sem-deriva.md). O que
este arquivo existe para impedir é uma coisa só, e ela já custou caro a este
repositório: **artefato que parece verificado e está velho**. Duas faixas erradas
foram publicadas assim, num script sem vínculo com o texto.

Um `.ipynb` é JSON, então executá-lo é ler o JSON, concatenar as células de
código e rodá-las num namespace só. Isso não precisa de Jupyter instalado e
basta para provar o que importa: que o caderno chama funções que **existem**, com
a assinatura **atual**, e que os `assert` dele passam contra o código de agora.

O caderno clona o repositório do GitHub. Aqui o clone é substituído por um atalho
para a árvore de trabalho local — **sem rede, e contra o código local em vez do
publicado**, que é exatamente o que um portão de pré-merge tem de fazer.

Rode com: python -m pytest po-zero/cadernos -q
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
RAIZ = AQUI.parents[1]
CADERNOS = sorted(AQUI.glob("*.ipynb"))

# Se um dia não houver caderno nenhum, o teste tem de gritar em vez de passar
# vazio — teste que não testa nada é o falso verde clássico.
assert CADERNOS, "nenhum caderno em po-zero/cadernos — o portão não está medindo nada"


def celulas_de_codigo(nb):
    return [(i, "".join(c["source"])) for i, c in enumerate(nb["cells"])
            if c["cell_type"] == "code"]


@pytest.fixture(params=CADERNOS, ids=lambda p: p.stem)
def caderno(request):
    return request.param, json.loads(request.param.read_text(encoding="utf-8"))


def test_nao_guarda_saida(caderno):
    """Saída gravada é NÚMERO PUBLICADO FORA DE PORTÃO.

    É a classe de defeito das duas faixas erradas, ressuscitada num artefato que
    o `verifica-capitulos.mjs` não olha. Commit limpo, sempre.
    """
    arq, nb = caderno
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        assert c.get("outputs") == [], f"{arq.name}: célula {i} tem saída gravada"
        assert c.get("execution_count") is None, f"{arq.name}: célula {i} tem execution_count"


def test_nao_tem_algoritmo(caderno):
    """O caderno é motorista, não implementação (ADR 0016, D1).

    Uma linha de `def` aqui é uma segunda cópia do algoritmo, e segunda cópia
    envelhece. A fonte única é o `.py` que o `pytest` já verifica.
    """
    arq, nb = caderno
    for i, fonte in celulas_de_codigo(nb):
        for linha in fonte.split("\n"):
            assert not linha.startswith(("def ", "class ")), \
                f"{arq.name}: célula {i} define código próprio — a fonte única é o .py"


def test_nao_usa_magia(caderno):
    """`!git clone` e `%cd` só existem no IPython; Python puro roda nos dois lugares."""
    arq, nb = caderno
    for i, fonte in celulas_de_codigo(nb):
        for linha in fonte.split("\n"):
            assert not linha.lstrip().startswith(("!", "%")), \
                f"{arq.name}: célula {i} usa magia do IPython: {linha.strip()!r}"


def test_tem_celula_mexa_aqui_e_erro_antes_da_correcao(caderno):
    """ADR 0016, D5: o caderno tem de fazer o que a página NÃO faz.

    Sem isso ele é um script com botão. Duas coisas são exigidas: um parâmetro
    que o leitor mexe, e um erro que ele roda ANTES de ver o certo.
    """
    arq, nb = caderno
    texto = "".join("".join(c["source"]) for c in nb["cells"])
    assert "mexa aqui" in texto.lower(), \
        f"{arq.name}: sem célula 'mexa aqui' — o leitor não tem o que mudar (ADR 0016, D5)"
    assert "antes de ver o certo" in texto.lower() or "antes de rodar" in texto.lower(), \
        f"{arq.name}: sem o erro rodado antes da correção (ADR 0016, D5)"


def test_mostra_o_algoritmo_em_algum_ponto(caderno):
    """A mitigação declarada do custo do invólucro.

    Importar esconde o código, e a regra das duas implementações existe para ele
    ser LIDO. Todo caderno exibe a fonte de ao menos uma função no ponto que
    ensina.
    """
    arq, nb = caderno
    texto = "".join("".join(c["source"]) for c in nb["cells"])
    assert "getsource" in texto, \
        f"{arq.name}: nenhuma célula mostra o código-fonte — o invólucro virou caixa-preta"


def test_executa_de_verdade(caderno, tmp_path, monkeypatch):
    """A asserção que sustenta as outras: o caderno RODA, e os asserts dele passam.

    O clone vira um atalho para a árvore de trabalho: sem rede, e contra o código
    de hoje. Se uma função for renomeada no `.py` e o caderno não acompanhar,
    isto fica vermelho — que é o ponto inteiro.
    """
    arq, nb = caderno
    monkeypatch.chdir(tmp_path)
    (tmp_path / "operationalresearchaibook").symlink_to(RAIZ)

    ns: dict = {"__name__": "__caderno__"}
    for i, fonte in celulas_de_codigo(nb):
        try:
            exec(compile(fonte, f"<{arq.name}:célula {i}>", "exec"), ns)
        except Exception as e:
            pytest.fail(f"{arq.name}: célula {i} quebrou: {type(e).__name__}: {e}")


def test_o_capitulo_publica_o_link_do_caderno(caderno):
    """O vínculo com o texto, na mesma disciplina da ADR 0014 D3.

    Caderno que existe e nenhum capítulo aponta é trabalho invisível; link no
    capítulo para caderno que não existe é promessa quebrada. Aqui se confere o
    primeiro lado — o segundo é do portão do build.
    """
    arq, _ = caderno
    capitulos = (RAIZ / "livro" / "capitulos").glob("*.md")
    alvo = f"po-zero/cadernos/{arq.name}"
    achou = [c.name for c in capitulos if alvo in c.read_text(encoding="utf-8")]
    assert achou, f"nenhum capítulo aponta para {alvo} — o caderno está órfão"
