"""Registro de capacidades e o gating por capítulo.

Duas modalidades (decisão do autor):
  - "avancado": tudo liberado (o companion completo).
  - "progressivo": só o que o livro já ensinou até o capítulo atual — o
    *fading* do 4C/ID virando comportamento: o tutor só oferece o que o
    leitor já viu, e recusa (explicando) o que vem depois.

Cada capacidade declara em que capítulo é liberada e quais tools habilita.
O widget usa `capacidades(chapter, mode)` para mostrar "o que posso fazer agora".
`tools_ativas` e `loop_ativo` decidem o comportamento real do turno.
"""

from __future__ import annotations

from typing import Optional

# chave, rótulo, descrição (voltada ao leitor), capítulo que libera, tools que habilita.
# tools=() significa capacidade conceitual (sem tool nova) ou infra sempre-presente.
#
# Esta é a FONTE DA VERDADE do gating. `COMPANION_CAPS` em `publicar/build.mjs`
# é um espelho para exibição, e `verifica-espelho.mjs` barra a divergência.
# Mudou aqui, mude lá.
#
# O registro cresce com os capítulos: cada rodada de conteúdo acrescenta as
# capacidades que seus capítulos destravam (formular um modelo linear, ler um
# preço-sombra, escolher entre exato e heurístico). Hoje o handbook está na
# rodada de fundação e ainda não publicou capítulo de método.
REGISTRO = [
    {"chave": "tutor", "rotulo": "Tutor do handbook", "libera": 0, "tools": (),
     "descricao": "Explico conceitos e conduzo por perguntas, usando o texto do handbook."},
    {"chave": "busca_livro", "rotulo": "Busca no livro", "libera": 0, "tools": ("buscar_no_livro",),
     "descricao": "Encontro os trechos do livro que embasam a resposta, e cito a fonte."},
    {"chave": "mapa", "rotulo": "Mapa do handbook", "libera": 0, "tools": (),
     "descricao": "Situo um tema no mapa: em que parte ele mora, o que vem antes e o que ele destrava."},
    {"chave": "exercicios", "rotulo": "Exercícios", "libera": 1,
     "tools": ("exercicio_registrar_tentativa",),
     "descricao": "Conduzo o exercício da página, avalio sua resposta pelos critérios e registro a tentativa."},
]

MODOS = ("avancado", "progressivo")


def _norm(chapter: Optional[int], mode: str) -> tuple[int, str]:
    ch = 0 if chapter is None else max(0, int(chapter))
    md = mode if mode in MODOS else "progressivo"
    return ch, md


def _ativa(cap: dict, chapter: int, mode: str) -> bool:
    return True if mode == "avancado" else cap["libera"] <= chapter


def capacidades(chapter: Optional[int], mode: str) -> list[dict]:
    """Lista para o widget: cada capacidade com rótulo, descrição e `ativa`."""
    ch, md = _norm(chapter, mode)
    return [{"chave": c["chave"], "rotulo": c["rotulo"], "descricao": c["descricao"],
             "libera_no_capitulo": c["libera"], "ativa": _ativa(c, ch, md)}
            for c in REGISTRO]


def loop_ativo(chapter: Optional[int], mode: str) -> bool:
    """O loop de tool-calling roda quando há ao menos uma tool ativa.

    Neste livro a busca no texto vale desde a capa — o tutor precisa citar a
    fonte já na primeira pergunta —, então o loop nasce ativo.
    """
    ch, md = _norm(chapter, mode)
    return any(c["tools"] and _ativa(c, ch, md) for c in REGISTRO)


def tools_ativas(chapter: Optional[int], mode: str) -> set[str]:
    """Nomes de tools habilitadas. Só valem se o loop estiver ativo."""
    ch, md = _norm(chapter, mode)
    if not loop_ativo(ch, md):
        return set()
    ativas: set[str] = set()
    for c in REGISTRO:
        if _ativa(c, ch, md):
            ativas.update(c["tools"])
    return ativas
