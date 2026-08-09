# Plan 003 — Capítulo 08: A geometria da Programação Linear

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-07

> **Este plano foi escrito depois da implementação.** É uma falha de processo, e ela está
> registrada aqui em vez de disfarçada: a revisão em contexto fresco apontou que a rodada 003
> repetiu o encurtamento de gate que a rodada 002 tinha acabado de registrar. O Constitution
> Check abaixo foi feito **retroativamente**, e por isso vale menos do que valeria antes — um
> portão que só confirma o que já foi construído não barra nada. O que ele ainda faz é deixar o
> registro correto e a próxima rodada sem essa desculpa.

## Constitution Check

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | 10 exercícios com devolutiva; vídeo em estado provisório declarado | ✅ com dívida declarada |
| II | Modelar antes de resolver | Intuição (pontos, faca, altura) → matemática (semiespaço, iso-lucro, gradiente) → procedimento → código. "Quando não serve" com o limite duro da dimensão | ✅ |
| III | Evidência acima de retórica | Todo número em `resultados.json`; as dez respostas conferidas por enumeração e por solver; seção de fundamentos declara a lacuna em vez de preenchê-la | ✅ com lacuna declarada |
| IV | Fonte-base é o experimento executável | `etapa-02` roda em CPU, solver aberto, saída determinística | ✅ |
| V | Três camadas | Capítulo de núcleo | ✅ |
| VI | Atualização por Radar | Nenhum artigo citado; a varredura está na fila | ✅ |
| VII | Livro vivo | Selo de datação; edições 0.4 a 0.6 no histórico | ✅ |
| VIII | Português canônico | Só PT (ADR 0002) | ✅ |
| IX | Comunicação inteligível | **Falhou na primeira entrega** — CPU, GB e JSON nasceram nuas. Corrigido após a revisão; as três entraram no mapa de siglas e no glossário | ⚠️ corrigido |
| X | Direitos autorais | Instância autoral com ficha | ✅ |
| XI | DoD verificável | Ver [`verificacao.md`](verificacao.md) | ✅ |

## O que a revisão em contexto fresco encontrou

Um revisor independente checou o diff contra esta spec e a 002. O que ele achou, e o que foi
feito:

| Achado | Gravidade | Resolução |
|---|---|---|
| `cap07.exC` afirmava saída de solver **impossível** — o ótimo do modelo era (137,5; 125), não (200, 0) | Bloqueador | Modelo corrigido (lucro de B: 300 → 200), e o exercício ganhou uma terceira pergunta que a correção tornou possível |
| Spec 003 sem `plan.md`, `tasks.md` e `verificacao.md` | Bloqueador | Este arquivo e os outros dois |
| `verificacao.md` da 002 documentava o capítulo descartado | Bloqueador | Regenerada contra o repositório atual |
| A ilha dizia "encosta" em vértice **não-ótimo**, desmentindo a definição do capítulo | Alta | Teste passou a ser `nível == ótimo` |
| A ilha abria com a memória ligada, invertendo a narrativa | Alta | Abre desligada |
| Quatro exercícios apontavam para objetivos que não testavam | Alta | Objetivo **O5** criado para "formular a partir de enunciado e resolver"; os quatro repontados |
| `exE`: a resposta-guia trocava gradiente por reta de iso-lucro | Alta | Corrigida |
| `exF`: o erro provável citava número que não decorre do erro descrito | Alta | Recalculado: o erro produz (25, 0) / R$ 500 |
| Absolutos ("encosta em um ponto só", "sempre um vértice") desmentidos pelo próprio capítulo | Alta | Trocados por "se existe ótimo, existe um vértice ótimo" |
| Histórico 0.3 propagava os números descartados — e está no corpus do tutor | Alta | Nota de superação na entrada (append-only: anota, não apaga) |
| Mapa ainda marcava 07 e 08 como não escritos | Alta | Atualizado |
| Siglas nuas; glossário não tocado | Alta | Corrigido nos dois lugares |
| "Saída colada" reescrita à mão | Alta | Colada de verdade |

**A causa raiz do bloqueador:** conferi as dez respostas do capítulo 08 com código e **não
conferi** as quatro do capítulo 07. O único banco sem verificação executável foi o único com
erro de fato. A lição virou task de processo, não boa intenção.

## Decisões de implementação

Ver a §"Decisões de implementação" da spec. A que mais mudou depois da revisão foi a da ilha:
ela agora **abre no estado que o texto pressupõe** e só chama de "encosta" o último valor
possível — antes ela contradizia o capítulo no ponto exato em que o leitor forma a intuição.

## Mudanças de motor nesta rodada

| Mudança | Por quê |
|---|---|
| Identificador de exercício aceita A–Z | O limite de quatro era estado do livro de origem |
| Campo `contexto` (`livro` \| `leitor`) | A regra antiga confundia posição na bateria com natureza do exercício |
| Siglas CPU, GB e JSON no mapa do motor | Princípio IX |
