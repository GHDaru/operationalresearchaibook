"""O capítulo 06 e a sua bateria têm de bater com a medição.

O selo 🔵 do capítulo 06 depende deste arquivo. O vínculo é feito nas duas
direções — o número medido aparece no texto, e o texto não afirma o que a
medição não sustenta —, e há um detalhe deste capítulo que merece atenção
especial: **os números da tabela de ponto flutuante são dependentes de versão**.

Isso é sentido, e não descuido. Se uma versão nova do CBC passar a reportar mais
casas, este teste fica vermelho — e ficar vermelho é o comportamento certo,
porque o capítulo publica dígitos e diz a versão ao lado. Um número publicado que
envelhece em silêncio é o defeito que este handbook mais combate.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

import pytest

from ferramentas import multiplos_otimos, racao, vereditos

RAIZ = Path(__file__).resolve().parents[2]
CAPITULO = RAIZ / "livro/capitulos/06-ferramentas.md"


@pytest.fixture(scope="module")
def texto():
    return CAPITULO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def exercicios():
    return {e["id"]: e for e in json.loads((RAIZ / "livro/exercicios.json").read_text(encoding="utf-8"))}


# --- 1. múltiplos ótimos ---------------------------------------------------

@pytest.fixture(scope="module")
def empate():
    return multiplos_otimos()


def test_todos_chegam_ao_mesmo_valor(empate):
    assert empate["exato"]["valor"] == "10"
    for s in empate["solvers"]:
        assert s["status"] == "Optimal"
        assert s["valor"] == pytest.approx(10.0)


def test_o_exato_e_os_solvers_escolhem_planos_diferentes(empate):
    """A afirmação central do capítulo 06 — e ela é sobre DISCORDÂNCIA.

    Um teste que só verificasse "todos acham o ótimo" perderia justamente o
    ponto: o valor é o mesmo e o plano não é.
    """
    assert empate["exato"]["ponto"] == ["6", "4"]
    for s in empate["solvers"]:
        assert [round(v) for v in s["ponto"]] == [2, 8]


def test_a_tabela_do_empate_esta_no_capitulo(texto):
    assert "| Simplex didático, aritmética exata | **A = 6, B = 4** | 10 |" in texto
    assert "| PuLP + HiGHS | **A = 2,0, B = 8,0** | 10,0 |" in texto
    assert "| PuLP + CBC | **A = 2,0, B = 8,0** | 10,0 |" in texto


# --- 2. ponto flutuante ----------------------------------------------------

@pytest.fixture(scope="module")
def flutuante():
    return racao()


def test_o_exato_e_a_fracao(flutuante):
    assert flutuante["exato"]["valor"] == "780/17"
    assert flutuante["exato"]["ponto"] == ["180/17", "48/17"]


def test_nenhum_solver_devolve_a_fracao(flutuante):
    for s in flutuante["solvers"]:
        assert F(s["valor"]).limit_denominator(10 ** 15) != F(780, 17)


def test_os_dois_solvers_discordam_entre_si(flutuante):
    a, b = flutuante["solvers"]
    assert a["valor"] != b["valor"], "o capítulo afirma que HiGHS e CBC reportam números diferentes"
    assert a["erro_absoluto"] < 1e-12
    assert b["erro_absoluto"] > 1e-9


def test_a_tabela_do_flutuante_esta_no_capitulo(texto, flutuante):
    """A LINHA inteira de cada solver, e não o número solto em qualquer lugar.

    A versão anterior deste teste procurava `repr(valor)` no documento inteiro.
    Como `45.882352` também aparece na Síntese e na Leitura executiva, **apagar
    a linha do CBC da tabela deixava a suíte verde** — e trocar a célula por
    `99.999999` também. Era o único número que o docstring deste arquivo chamava
    de "dependente de versão" e para o qual prometia vermelho.
    """
    higs, cbc = flutuante["solvers"]
    erros = {"HiGHS": "4,18 × 10⁻¹⁶", "CBC": "9,41 × 10⁻⁷"}
    for s in (higs, cbc):
        linha = f"| PuLP + {s['solver']} | {s['valor']!r} | {erros[s['solver']]} |"
        assert linha in texto, f"a linha do {s['solver']} não confere com a medição: esperada {linha!r}"
    assert "| Simplex didático, `Fraction` | **780/17** | 0 — é a fração |" in texto


def test_o_capitulo_declara_as_versoes_que_produziram_os_digitos(texto):
    """O capítulo enunciava a regra da versão e a violava no mesmo diretório.

    `resultados-ferramentas.json` gravava os NOMES dos solvers no campo
    `versoes`. As versões do HiGHS e do CBC — que são as que produzem os dígitos
    da tabela acima — não estavam em lugar nenhum.
    """
    import json as _json
    v = _json.loads((RAIZ / "po-zero/parte-I-fundamentos/resultados-ferramentas.json")
                    .read_text(encoding="utf-8"))["versoes"]
    assert f"Python {v['python']}" in texto
    assert f"PuLP {v['pulp']}" in texto
    assert f"HiGHS\n> {v['solvers']['HiGHS']}" in texto or f"HiGHS {v['solvers']['HiGHS']}" in texto
    assert v["solvers"]["CBC"] in texto
    assert v["solvers"]["HiGHS"] != "HiGHS", "o campo `versoes` voltou a gravar nome em vez de versão"


def test_os_decimais_publicados_do_empate_conferem(texto, empate):
    """`A = 2,0, B = 8,0` é texto publicado, e `round()` não o verificava.

    Se o solver devolvesse 2,4 o teste anterior passaria e a tabela estaria
    errada — a asserção era sobre o inteiro mais próximo, não sobre o publicado.
    """
    for s in empate["solvers"]:
        a, b = (f"{v:.1f}".replace(".", ",") for v in s["ponto"])
        assert f"| PuLP + {s['solver']} | **A = {a}, B = {b}** | 10,0 |" in texto, \
            f"a linha do empate para {s['solver']} não confere: ponto medido {s['ponto']}"


def test_o_capitulo_declara_a_regra_da_tolerancia(texto):
    """Sem esta frase, a tabela vira curiosidade em vez de instrução."""
    assert "nunca compare saídas de solver por igualdade exata" in texto.lower() or \
           "Nunca compare saídas de solver com `==`" in texto


# --- 3. vereditos ----------------------------------------------------------

def test_os_vereditos_concordam():
    v = vereditos()
    assert v["ilimitado"]["exato"] == "ilimitado"
    assert v["ilimitado"]["solvers"] == ["Unbounded", "Unbounded"]
    assert v["inviavel"]["exato"] == "inviavel"
    assert v["inviavel"]["solvers"] == ["Infeasible", "Infeasible"]


def test_a_tabela_de_vereditos_esta_no_capitulo(texto):
    assert "| `ilimitado` | `Unbounded` | `Unbounded` |" in texto
    assert "| `inviavel` | `Infeasible` | `Infeasible` |" in texto


def test_o_capitulo_diz_o_que_a_concordancia_significa(texto):
    """A leitura acionável: trocar de solver não conserta modelo."""
    assert "trocar de solver não vai resolver" in texto


# --- o ambiente que o capítulo manda montar --------------------------------

def test_o_arquivo_de_dependencias_que_o_capitulo_cita_existe():
    """O bloco de instalação do capítulo 06 aponta para um arquivo real.

    E é o MESMO que a integração contínua instala — o que torna a instrução
    executada a cada envio, em vez de conferida por alguém de vez em quando.
    """
    req = RAIZ / "po-zero/requirements.txt"
    assert req.exists()
    conteudo = req.read_text(encoding="utf-8")
    for pacote in ("pulp", "highspy", "numpy", "pytest"):
        assert pacote in conteudo

    ci = (RAIZ / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "po-zero/requirements.txt" in ci, "a CI deixou de instalar o que o capítulo 06 manda instalar"


def test_a_bateria_do_capitulo_existe_com_tres_exercicios(exercicios):
    assert len([e for e in exercicios if e.startswith("cap06.")]) >= 3


# --- B2: a Síntese e a Leitura executiva do capítulo 06 -----------------------

def _secao(texto: str, titulo: str) -> str:
    inicio = texto.index(titulo)
    resto = texto[inicio + len(titulo):]
    fim = resto.find("\n## ")
    return resto if fim < 0 else resto[:fim]


def test_a_sintese_e_a_executiva_repetem_os_numeros_medidos(texto, empate, flutuante):
    """Treze das dezenove mutações que passaram na revisão estavam nestas seções.

    E o risco não é teórico: cada correção desta rodada teve de atualizar a mesma
    medição em três lugares à mão. Esquecer um deixaria a suíte verde com o
    capítulo se contradizendo.
    """
    higs, cbc = flutuante["solvers"]
    exato = empate["exato"]["ponto"]
    for nome in ("## Síntese — o que levar", "### Leitura executiva"):
        secao = _secao(texto, nome)
        assert repr(higs["valor"]) in secao, f"{nome}: o valor do HiGHS não confere"
        assert repr(cbc["valor"]) in secao, f"{nome}: o valor do CBC não confere"
        assert flutuante["valor_exato_fracao"] in secao, f"{nome}: a fração exata não confere"
        assert f"({exato[0]}, {exato[1]})" in secao, f"{nome}: o plano do Simplex exato não confere"
        assert f"{higs['casas_reportadas']} " in secao and f"{cbc['casas_reportadas']}" in secao, \
            f"{nome}: a contagem de casas não confere com a medição"
