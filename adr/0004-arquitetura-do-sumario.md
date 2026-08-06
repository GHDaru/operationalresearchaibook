# ADR 0004 — Arquitetura do sumário em três camadas

**Data:** 2026-08-06 · **Status:** aceito

## Contexto

O pedido do autor tem quatro exigências que puxam em direções opostas:

1. Fundamentação sedimentada, cobrindo Pesquisa Operacional (PO) inteira.
2. Handbook evolutivo, que cresce sem reescrever o que já existe.
3. Módulos aplicados por área de domínio.
4. Atualização constante a partir de artigos científicos.

Um sumário que atenda só a (1) vira livro-texto comum e morre na primeira edição. Um que
atenda só a (3) e (4) vira coletânea sem espinha — cada capítulo novo negocia o próprio lugar e
a fundamentação se dissolve.

A tensão é real e não se resolve escolhendo um lado.

## Decisão

**O handbook é uma estrutura de três camadas com ritmos de envelhecimento diferentes**, e não
uma lista única de capítulos.

| Camada | O que é | Regra que a governa |
|---|---|---|
| **Núcleo** (Partes I–IX) | A fundamentação em que as obras de referência concordam | Muda por janela de revisão, nunca por notícia. Tema de fronteira não entra aqui |
| **Aplicados** (Parte X) | Um módulo por domínio, fechado em si | Cresce **por adição**: módulo novo não altera módulo existente |
| **Fronteira** (Parte XI) | O que está se movendo agora na literatura | **Cláusula de expiração obrigatória** em todo capítulo |

Três consequências operacionais:

1. **Promoção entre camadas é decisão, não deriva.** Um tema sobe de fronteira para núcleo
   quando resiste a **duas janelas de revisão** sem ser refutado. A promoção vira ADR.
2. **O Radar é o mecanismo de atualização** — não a boa vontade de reler o campo. Artigo lido
   vira linha datada em `radar/RADAR.md`; linha que altera uma recomendação dispara revisão do
   capítulo afetado.
3. **O mapa é publicado antes do conteúdo.** As 77 vagas existem declaradas em
   `livro/mapa-do-handbook.md`, de modo que um capítulo novo **ocupa uma vaga que já existia**
   em vez de negociar seu lugar.

## Alternativas avaliadas

| Alternativa | Por que não |
|---|---|
| Sumário linear único, na ordem canônica dos livros-texto | Não acomoda módulos aplicados nem fronteira sem inchar o núcleo. O livro envelheceria por inteiro no ritmo da parte mais volátil |
| Só núcleo, com aplicações como exemplos dentro dos capítulos | Aplicação vira ilustração e perde a profundidade que o autor pediu — modelagem situada é assunto, não exemplo |
| Wiki sem espinha, crescendo por demanda | Perde a fundamentação; é exatamente o modo de falhar que este ADR existe para evitar |
| Duas camadas (estável + volátil) | Não separa "cresce por adição" de "expira rápido", que são propriedades diferentes com regras diferentes |

## Consequências

**Boas.** As quatro exigências passam a ser compatíveis: o que muda toda semana não mora onde o
aluno aprende a base. A camada de aplicados é aberta sem limite porque a estrutura é declarativa
(ADR 0001) — módulo novo é arquivo novo mais uma linha no `sumario.json`.

**Ruins, e assumidas.** Um mapa de 77 vagas publicado antes do conteúdo cria expectativa que
levará anos para cumprir; por isso o mapa declara explicitamente que **vaga não é promessa de
prazo**. Além disso, a fronteira entre "núcleo" e "fronteira" será disputada em casos concretos
— aprendizado por reforço para decisão sequencial é o exemplo óbvio — e cada disputa custa uma
decisão do autor.

**Verificável.** A promessa "cresce por adição" tem teste: a primeira rodada de módulo aplicado
não pode alterar nenhum capítulo existente. Se alterar, a arquitetura está errada — e o problema
é de motor, não de conteúdo.
