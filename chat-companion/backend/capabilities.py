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
REGISTRO = [
    {"chave": "tutor", "rotulo": "Tutor do livro", "libera": 0, "tools": (),
     "descricao": "Explico conceitos e conduzo por perguntas, usando o texto do livro."},
    {"chave": "busca_livro", "rotulo": "Busca no livro", "libera": 0, "tools": ("buscar_no_livro",),
     "descricao": "Encontro os trechos do livro que embasam a resposta, e cito a fonte."},
    {"chave": "restricao", "rotulo": "A restrição", "libera": 1, "tools": (),
     "descricao": "Ajudo a identificar a restrição de um sistema seu e a testar se é ela mesma."},
    {"chave": "cinco_passos", "rotulo": "Cinco passos", "libera": 3, "tools": (),
     "descricao": "Conduzo o ciclo de focalização e aponto em que passo você está."},
    {"chave": "tres_perguntas", "rotulo": "As três perguntas", "libera": 4, "tools": (),
     "descricao": "Ajudo a enquadrar seu problema numa das três perguntas da mudança."},
    {"chave": "exercicios", "rotulo": "Exercícios", "libera": 1,
     "tools": ("exercicio_registrar_tentativa",),
     "descricao": "Conduzo o exercício da página, avalio sua resposta pelos critérios e registro a tentativa."},
    {"chave": "causa_efeito", "rotulo": "Causa e efeito", "libera": 6, "tools": (),
     "descricao": "Ajudo a testar conexões \"se… então…\" que você escreveu."},
    {"chave": "pre_requisito", "rotulo": "Pré-requisito", "libera": 7, "tools": (),
     "descricao": "Ajudo a testar conexões \"para… é necessário…\" pela negativa."},
    {"chave": "premissas", "rotulo": "Premissas", "libera": 8, "tools": (),
     "descricao": "Provoco o levantamento de premissas de uma conexão sua."},
    {"chave": "cadeias", "rotulo": "Cadeias lógicas", "libera": 9, "tools": ("calcular",),
     "descricao": "Verifico o encadeamento: saltos, circularidade e efeitos órfãos."},
    {"chave": "nuvem", "rotulo": "A Nuvem", "libera": 10, "tools": (),
     "descricao": "Conduzo a montagem de uma Nuvem e aplico os testes de verificação."},
    {"chave": "conflito_recorrente", "rotulo": "Conflitos recorrentes", "libera": 11, "tools": (),
     "descricao": "Ajudo a fechar o loop de um problema que sempre volta."},
    {"chave": "injecoes", "rotulo": "Injeções", "libera": 12, "tools": (),
     "descricao": "Provoco a inversão de premissas e valido as injeções candidatas."},
    {"chave": "apr", "rotulo": "Análise de Pré-Requisitos", "libera": 13, "tools": (),
     "descricao": "Ajudo a converter obstáculos em objetivos intermediários e a sequenciá-los."},
    {"chave": "aplicacao", "rotulo": "Aplicação integrada", "libera": 14, "tools": (),
     "descricao": "Conduzo o percurso completo em uma hora sobre um problema seu."},
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
