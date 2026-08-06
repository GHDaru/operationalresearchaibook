# Histórico

> **Conteúdo revisado em 2026-08** · edições, datas e o que mudou a cada rodada.

Este handbook é vivo: não tem versão final. Cada edição registra o que mudou, quando, e com
apoio de qual modelo de Inteligência Artificial (IA) — em coerência com a nota de autoria da
[Introdução](00-introducao.md).

Registro é *append-only*: edição publicada não se reescreve. Quando um número ou uma
recomendação muda, a mudança entra como edição nova, e a antiga permanece.

### Edição 0.1 — 2026-08-06 · Fundação e mapa do handbook

Rodada inaugural. O repositório foi **refundado**: nasceu como clone do motor do livro *Teoria
das Restrições* (mesmo autor) e nesta edição passa a ser o handbook de Pesquisa Operacional
(PO), com governança, aparato e sumário próprios.

**Entrou:**

- **Constituição do handbook** (versão 1.0.0), com onze princípios — entre eles *modelar antes
  de resolver* (II), *arquitetura em três camadas* (V) e *atualização científica por Radar*
  (VI). Herda a metodologia [Maestro](https://github.com/GHDaru/maestro), adotada como
  obrigatória em todas as rodadas.
- **[Mapa do handbook](mapa-do-handbook.md)** — o sumário declarado: 77 vagas em onze partes,
  organizadas em três camadas (núcleo, módulos aplicados, fronteira). É o entregável central
  desta edição.
- **[Estudo do corpo de conhecimento](../estudos/001-corpo-de-conhecimento-po.md)** — a
  pesquisa que fundamenta o recorte: como Hillier & Lieberman, Winston e Arenales et al.
  organizam o campo, o que os livros-texto cobrem mal (ALNS, *matheuristics*, aprendizado de
  máquina em solvers, otimização sob incerteza) e as decisões de recorte que produziram o mapa.
- **Aparato editorial completo** — Guia Editorial com o esqueleto de capítulo obrigatório,
  bibliografia com as obras de referência verificadas, videoteca com a política de curadoria,
  glossário e banco de exercícios.
- **[Radar científico](../radar/RADAR.md)** — o mecanismo pelo qual artigo entra no livro:
  datado, com veredito e com o registro do que ele muda.
- **[Roadmap](../ROADMAP.md)** — a ordem de ataque das rodadas, que deliberadamente **não** é a
  ordem do sumário: Programação Linear (PL) vem antes dos Fundamentos.
- **Autorização de uso dos vídeos** do canal de João Sarubbi (CEFET-MG), registrada na
  videoteca.

**Saiu:** todo o conteúdo herdado do livro de Teoria das Restrições — capítulos, especificações,
registros de decisão e o objeto interativo daquele livro. O conteúdo permanece íntegro no
repositório de origem; aqui ele foi removido para que o handbook não carregue um sumário que
não é o seu.

**Decisões registradas:** reúso do motor ([ADR 0001](../adr/0001-reuso-motor-livro-vivo.md)),
português como fonte canônica com o inglês como dívida declarada
([ADR 0002](../adr/0002-portugues-primeiro.md)), pilha do `po-zero` em Python com solver aberto
([ADR 0003](../adr/0003-stack-po-zero.md)) e a arquitetura em três camadas do sumário
([ADR 0004](../adr/0004-arquitetura-do-sumario.md)).

**Dívida declarada.** Ratificar os princípios coloca o estado atual deliberadamente fora de
conformidade em três pontos, e a distância é registrada aqui em vez de escondida:

| Dívida | Princípio | Quando fecha |
|---|---|---|
| Nenhum capítulo de método publicado — logo, nenhum exercício e nenhum vídeo | I | Rodada de Programação Linear |
| `po-zero` sem etapas: só o esqueleto e a decisão de pilha | IV | Rodada de Programação Linear |
| Par em inglês inexistente | VIII | Após o núcleo, conforme roadmap |
| Livros-base ainda não mapeados na bibliografia | X | ✅ fechada em 2026-08-06 — ver edição 0.2 |

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.2 — 2026-08-06 · Livros-base mapeados

Os dois livros didáticos que o autor adota com os alunos foram registrados e mapeados contra o
[Mapa do handbook](mapa-do-handbook.md).

**Entrou:**

- **Ficha bibliográfica** das duas obras — Lachtermacher, *Pesquisa Operacional na Tomada de
  Decisões* (Elsevier/Campus, 224 p.) e Arenales, Armentano, Morabito & Yanasse, *Pesquisa
  Operacional* (Elsevier, 2007, 542 p.) — com a estrutura declarada de cada uma.
- **Tabela de correspondência** entre as partes do handbook e as unidades de cada obra, para
  que o aluno transite entre o handbook e o livro impresso sem se perder.

**O achado que vale como decisão editorial:** as duas obras juntas cobrem bem as Partes I a IV,
VI e VIII, e **não cobrem as Partes V, VII e XI** — metaheurísticas, otimização sob incerteza e
fronteira. É a maior contribuição própria do handbook, e confirma o recorte que o
[estudo do corpo de conhecimento](../estudos/001-corpo-de-conhecimento-po.md) havia feito
*antes* de as obras serem consultadas.

**Duas consequências para a rodada de Programação Linear:** o handbook mantém dualidade logo
após o Simplex (como Arenales, não como Lachtermacher), e promove casos especiais e
degenerescência a capítulo próprio — assunto que nenhuma das duas obras trata em separado.

**Direitos autorais.** Só metadados e correspondência foram versionados. Nenhum trecho, figura
ou enunciado das obras entrou no repositório (Princípio X).

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.
