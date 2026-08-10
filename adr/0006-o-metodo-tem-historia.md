# ADR 0006 — Todo método tem história, e a história entra no livro

**Data:** 2026-08-09 · **Status:** aceito · **Emenda constitucional:** 1.0.0 → **1.1.0**
(Princípio XII, novo)

## Contexto

Os capítulos 07, 08 e 09 foram escritos e ficaram tecnicamente corretos: intuição antes da
fórmula, exercícios rastreando objetivos, números com procedência, "quando não serve" em todos.
E ainda assim faltava alguma coisa.

O autor nomeou o que faltava, ao ler o capítulo 09:

> *"Importante trazer um racional do porquê, algo histórico, filosófico, do problema que motivou
> ter que buscar uma alternativa e solução para alguma decisão. Por exemplo: de onde veio big-M?
> Por quê, qual a ideia. Não quero passar decoreba, o livro deve ser uma inspiração motivacional,
> ter história."*

O diagnóstico é preciso. O capítulo 09 explicava **como** o *big-M* funciona — variável
artificial, multa, expulsão na primeira iteração — e explicava até **por que a mecânica é
segura**. O que ele não dizia é de onde a ideia veio, quem estava preso em quê, e qual é o
padrão de raciocínio reaproveitável por trás do truque.

Sem isso, o leitor sai capaz de executar e incapaz de reconhecer. Ele decora que "restrição `≥`
pede artificial com multa" — e no ano seguinte, diante de um problema diferente que pede o mesmo
tipo de saída (relaxar até ficar fácil, e cobrar caro pela relaxação), não vê a conexão.

O Princípio II já exigia começar pelo problema. Mas "problema" ali era o **problema abstrato**
que o método resolve. Não cobria o **problema histórico concreto** — a Força Aérea sem método de
planejamento em 1947, o programa de logística que ninguém sabia otimizar — que é o que dá peso
narrativo e faz o leitor querer continuar.

## Decisão

Criar o **Princípio XII — Nenhum método cai do céu**, não-negociável, com cinco consequências
verificáveis:

1. Seção **"De onde isto veio"** obrigatória em todo capítulo de método, incluindo **o que se
   fazia antes**.
2. Nome com origem é nome explicado.
3. Todo artifício declara a **ideia reaproveitável** por trás dele.
4. História é afirmação e vale o Princípio III: sem fonte, `⏳`, e não sustenta afirmação.
5. A história tem de **mudar alguma coisa** — se sai sem perda, é curiosidade decorativa.

## Alternativas avaliadas

**Expandir o Princípio II em vez de criar um novo.** Rejeitada. O II é sobre a **ordem de
exposição** (intuição → matemática → código) e sobre honestidade metodológica ("quando não
serve"). O que o autor pede é outra coisa: uma exigência de **narrativa e motivação**, com
requisito próprio de fonte. Enfiá-la no II tornaria os dois vagos, e princípio vago não barra
nada.

**Inserir o princípio novo na posição II ou III, onde ele encaixa melhor logicamente.**
Rejeitada, com desconforto. Seria a posição certa, mas renumeraria de III a XI — e há dezenas de
referências a "Princípio III", "Princípio V", "Princípio XI" espalhadas por capítulos, planos,
ADRs, portões e mensagens de commit. Renumeração em massa foi exatamente a origem do defeito que
o `verifica-referencias.mjs` existe para pegar. **A ordem de leitura vale menos do que a
estabilidade das referências.** Fica como XII, com ponteiro a partir do II.

**Deixar como recomendação no Guia Editorial, sem status constitucional.** Rejeitada. O Guia é
onde ficam as regras de forma; recomendação de forma não barra publicação. O autor não pediu um
estilo, pediu uma característica do livro — e o que não é constitucional aqui não tem portão.

**Tratar como seção opcional, escrita quando houver material.** Rejeitada. É a formulação que
garante que a seção só apareça nos capítulos fáceis, e some justamente onde o esforço de
pesquisa seria maior — que costuma ser onde ela mais ensinaria.

## Consequências

**Boas:**

- O livro ganha o que o autor chamou de inspiração motivacional, com critério: história que
  ensina, não anedota.
- A exigência de **ideia reaproveitável** ataca a transferência de aprendizagem diretamente, que
  é o problema pedagógico real por trás de "decoreba".
- A seção é verificável, e ganhou portão: `verifica-capitulos.mjs` passa a exigi-la, com lista
  de dívida declarada para os capítulos que ainda não a têm.

**Custosas, e assumidas:**

- **Todo capítulo de método fica mais caro.** Pesquisa histórica com fonte é trabalho, e este
  ambiente não alcança arquivo primário — as fontes de história ficarão predominantemente em
  `⏳`, "localizado por busca, não confirmado na fonte", por um tempo.
- **Dívida retroativa imediata.** Os capítulos 07 e 08 estão publicados **sem** a seção. Entram
  na lista de dívida declarada do portão, e a quitação vira item de roadmap. Fingir que o
  princípio nasce só para o futuro seria conveniente e desonesto.
- **Risco novo, e é o mais sério: a história é o terreno mais fácil para inventar.** Uma data
  errada e uma atribuição plausível passam por qualquer revisão apressada, porque soam bem. A
  consequência 4 existe exatamente por isso, e a rodada 004 já mostrou que o risco é real: um
  endereço de vídeo inventado só não foi publicado por acaso.
