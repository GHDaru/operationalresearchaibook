# ADR 0002 — Português como fonte canônica; inglês como dívida declarada

**Data:** 2026-08-06 · **Status:** aceito

## Contexto

O motor foi herdado do livro *Teoria das Restrições*, cuja constituição declara o bilinguismo
português + inglês como princípio **não-negociável**: nenhum capítulo é dado por pronto sem o
par em inglês.

Aquele livro tem 14 capítulos. Este handbook declara **77 vagas**, e a camada de módulos
aplicados é aberta por desenho. Manter o portão bilíngue significaria dobrar o custo de cada
capítulo numa obra cuja dificuldade principal já é a **extensão do corpo de conhecimento**.

Há ainda um fato de público: o handbook é o corpo de conhecimento de uma disciplina real, dada
em português, para alunos que leem em português.

## Decisão

**O português é a fonte canônica.** O par em inglês é objetivo declarado no roadmap, **não**
portão de entrega.

1. Um capítulo é dado por pronto em português.
2. A ausência do par em inglês é **dívida registrada** no `livro/HISTORICO.md` — não omissão
   silenciosa.
3. Quando o par existir, o mecanismo de sincronia já implementado no motor passa a valer:
   a fonte em inglês carrega o hash da fonte em português e o selo de defasagem é visível ao
   leitor. Tradução velha nunca finge ser atual.

Isto é uma **emenda** ao princípio herdado, e está incorporado como Princípio VIII da
constituição deste repositório.

## Alternativas avaliadas

| Alternativa | Por que não |
|---|---|
| Manter bilíngue obrigatório | Metade da velocidade numa obra cujo risco principal é não cobrir o campo. O alcance internacional não compensa a cobertura perdida na fase de fundação |
| Bilíngue só no núcleo | Cria duas classes de capítulo e uma regra a mais para lembrar; a fronteira entre "núcleo" e "aplicado" seria negociada capítulo a capítulo |
| Abandonar o inglês | Perde alcance sem ganhar nada: o mecanismo de sincronia já existe e não custa nada enquanto não é usado |

## Consequências

**Boas.** A velocidade de cobertura dobra na fase em que ela é o gargalo. O mecanismo bilíngue
do motor permanece intacto, pronto para quando a prioridade mudar.

**Ruins, e assumidas.** O handbook não é internacionalmente legível na fase de fundação. A
dívida cresce com cada capítulo publicado — e por isso ela é registrada por capítulo, não como
uma nota genérica. Quanto mais tarde a tradução começar, maior o lote.

**Gatilho de revisão.** Esta decisão é reavaliada quando o núcleo estiver completo, ou antes
disso se houver demanda concreta de público de fora.
