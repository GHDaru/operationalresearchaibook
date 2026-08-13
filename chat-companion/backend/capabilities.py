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
    {"chave": "o_que_e_po", "rotulo": "O que é (e o que não é) PO", "libera": 1, "tools": (),
     "descricao": "Aplico com você as quatro perguntas que decidem se um problema é de Pesquisa "
                  "Operacional — há alavanca? há medida única? há restrição? dá para dizer o que a "
                  "resposta NÃO autoriza? — e ajudo a julgar um caso publicado."},
    {"chave": "ciclo_modelagem", "rotulo": "O ciclo de modelagem", "libera": 2, "tools": (),
     "descricao": "Situo com você a tarefa nas cinco etapas — definir, formular, resolver, validar, "
                  "implantar — e cobro o entregável que falta. Pergunto sempre a mesma coisa antes "
                  "de ajudar a formular: quem vai decidir diferente por causa disto?"},
    {"chave": "anatomia_modelo", "rotulo": "Anatomia de um modelo", "libera": 3, "tools": (),
     "descricao": "Separo com você as quatro peças de um modelo — variáveis, objetivo, restrições, "
                  "parâmetros — pela pergunta que resolve a maioria dos erros: isto é algo que "
                  "alguém decide, ou algo que alguém mede? E aplico o teste da unidade, que pega "
                  "o erro que o solver não pega."},
    {"chave": "classificacao", "rotulo": "Classificação e escolha de método", "libera": 4, "tools": (),
     "descricao": "Classifico com você um problema nos quatro eixos — linear, inteiro, incerto, "
                  "convexo — e digo qual garantia cada travessia destrói. Antes de discutir "
                  "método, cobro a pergunta que decide tudo: o que você vai poder prometer sobre "
                  "esta resposta?"},
    {"chave": "formulacao", "rotulo": "Formulação de modelos", "libera": 7, "tools": (),
     "descricao": "Conduzo a formulação de um problema seu pelas quatro perguntas — o que se escolhe, "
                  "qual a única medida, o que limita, o que é dado — e confiro as unidades com você."},
    {"chave": "geometria", "rotulo": "Geometria e método gráfico", "libera": 8, "tools": (),
     "descricao": "Ajudo a enxergar a região viável, a subir a reta de iso-lucro e a achar as "
                  "restrições que sustentam o vértice ótimo."},
    {"chave": "casos_especiais", "rotulo": "Casos especiais e degenerescência", "libera": 10, "tools": (),
     "descricao": "Ajudo a ler um veredito que não é um plano — inviável, ilimitado, mais de um "
                  "ótimo, vértice degenerado — e a decidir o que fazer com ele. Distingo defeito "
                  "de modelo de defeito de regra de pivoteamento."},
    {"chave": "simplex_revisado", "rotulo": "Simplex revisado", "libera": 11, "tools": (),
     "descricao": "Leio o Simplex em forma matricial com você — B, B⁻¹, custo reduzido como preço "
                  "— e ajudo a distinguir estagnação de ciclagem e de lentidão. Cobro a escala dos "
                  "seus dados antes de qualquer conversa sobre tolerância numérica."},
    {"chave": "dualidade", "rotulo": "Dualidade e preço-sombra", "libera": 12, "tools": (),
     "descricao": "Escrevo o dual com você, confiro a unidade de cada variável dual e leio o "
                  "preço-sombra no quadro final. Cobro a faixa de validade antes de deixar "
                  "qualquer decisão de compra sair do preço."},
    {"chave": "sensibilidade", "rotulo": "Análise de sensibilidade", "libera": 13, "tools": (),
     "descricao": "Leio o relatório de sensibilidade com você e separo as duas famílias de faixa — "
                  "a do lucro, que protege o plano, e a do estoque, que protege o preço. Digo "
                  "quando a resposta já está no relatório e quando é preciso resolver de novo."},
    {"chave": "pontos_interiores", "rotulo": "Pontos interiores", "libera": 14, "tools": (),
     "descricao": "Explico por que atravessar não contradiz o teorema do vértice, e ajudo a ler "
                  "uma saída que NÃO é vértice — sem base, sem zeros exatos, sem preço-sombra. "
                  "Ajudo a escolher entre Simplex e interior pela instância, não pela fama."},
    {"chave": "modelagem_aplicada", "rotulo": "Padrões de modelagem", "libera": 15, "tools": (),
     "descricao": "Ajudo a reconhecer o padrão de um enunciado — mix, mistura, transporte, "
                  "cobertura — começando pela única pergunta que importa: o que exatamente se "
                  "escolhe? E cobro se o modelo responde à pergunta que foi feita."},
    {"chave": "convexidade", "rotulo": "Convexidade", "libera": 38, "tools": (),
     "descricao": "Ajudo a decidir se um conjunto é convexo — pela estrutura, não por amostragem — "
                  "e a achar o contraexemplo quando não é. Cobro a pergunta que quase ninguém faz "
                  "diante de um relatório: o modelo é convexo?"},
    {"chave": "leitura_critica", "rotulo": "Leitura crítica de artigo", "libera": 77, "tools": (),
     "descricao": "Conduzo as três passadas num artigo que você trouxe e cobro a checklist de "
                  "comparação computacional — instâncias, baseline, critério de parada, máquina, "
                  "semente, versão de solver. Não digo se o artigo é bom: ajudo você a dizer o "
                  "que ele sustenta."},
    {"chave": "simplex", "rotulo": "Simplex de quadro", "libera": 9, "tools": (),
     "descricao": "Acompanho o quadro iteração a iteração: quem entra, quem sai pelo teste da "
                  "razão, e em que vértice cada quadro põe você. Confiro o seu pivoteamento — "
                  "não o faço no seu lugar."},
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
