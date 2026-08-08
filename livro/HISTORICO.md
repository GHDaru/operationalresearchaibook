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
| Nenhum capítulo de método publicado — logo, nenhum exercício e nenhum vídeo | I | 🟡 parcial — dois capítulos e 14 exercícios no ar; os vídeos seguem em confirmação (edições 0.3 e 0.4) |
| `po-zero` sem etapas: só o esqueleto e a decisão de pilha | IV | ✅ fechada em 2026-08-06 — etapa 01 no ar (edição 0.3) |
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

### Edição 0.3 — 2026-08-06 · Capítulo 07: formulação de modelos lineares

O primeiro capítulo de método do handbook, e a primeira vez que a máquina inteira — texto,
exercícios corrigidos no servidor e código reproduzível — roda de ponta a ponta.

**Entrou:**

- **Capítulo 07 — Formulação de modelos lineares**, abertura da Parte II. Estrutura o trabalho
  em quatro perguntas (o que se escolhe, qual a única medida, o que limita, o que é dado) e
  abre por um erro real: uma marcenaria que maximiza receita em vez de margem.
- **Quatro exercícios** (`cap07`), em dificuldade crescente — reconhecer, formular, diagnosticar
  e aplicar ao próprio contexto —, cada um rastreando a um objetivo de aprendizagem.
- **`po-zero/etapa-01-formulacao`** — as duas formulações lado a lado, resolvidas com HiGHS.
  `experimento.py` regenera `resultados.json` byte a byte, com versões declaradas.
- **Capacidade `formulacao`** no tutor, liberada no capítulo 07.
- **Marcador de vaga declarada** na navegação: as partes mostram o que ainda não foi escrito
  como cartão tracejado apontando para o Mapa, em vez de omitir. O livro passa a publicar fora
  da ordem do mapa, e diz isso ao leitor.

**Os números do capítulo, e de onde vêm.** O plano que maximiza margem produz 30 mesas e 40
estantes (R$ 13.800/mês); o que maximiza receita produz 60 mesas e nenhuma estante, fatura mais
(R$ 54.000) e entrega R$ 13.200 de margem — R$ 600 a menos por mês, deixando 60 horas de
acabamento paradas. Todos saem de `po-zero/etapa-01-formulacao/experimento.py`.

**Portões reforçados nesta rodada:**

- **Rastreio exercício → objetivo agora é verificado.** O Guia Editorial dizia que "o build
  falha se o exercício apontar para um objetivo que não existe"; até aqui isso era prosa e nada
  media. Agora o portão confere que o objetivo está declarado no capítulo que monta a bateria —
  e foi provado quebrando-o de propósito.
- **O portão de rubrica pegou um vazamento real**: o exemplo de sintaxe do Banco de Exercícios
  compartilhava os primeiros 40 caracteres de um critério do `cap07.exB`. O exemplo foi
  reescrito com texto que ninguém escreveria de verdade, e o motivo ficou registrado lá.

**Dívida declarada.** Duas, ambas do próprio capítulo:

| Dívida | Princípio | Quando fecha |
|---|---|---|
| Vídeo do capítulo 07 sem autoria e duração conferidas | I | Quando o autor indicar o vídeo do canal parceiro |
| Sem artigos científicos na seção de fundamentos — a varredura de literatura sobre ensino de formulação não foi feita | III | Fila do Radar |

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.4 — 2026-08-07 · Capítulo 08 e o exemplo de sala

A edição que troca o exemplo condutor do handbook pelo **exemplo que o autor usa em aula** e
publica o método gráfico em cima dele.

**O que motivou a troca.** O capítulo 07 tinha sido implementado antes de o autor responder qual
seria o exemplo condutor — os gates de aprovação da especificação e do plano foram encurtados, e
o capítulo nasceu com uma marcenaria genérica. O exemplo real é melhor, e o registro do erro de
processo está na [spec 002 v2](../specs/002-cap07-formulacao/spec.md).

**Entrou:**

- **Capítulo 08 — A geometria da Programação Linear**, com a narrativa de sala: cada variável
  numa dimensão, o significado dos pontos negativos, a laranja e a faca, a região viável, a reta
  de iso-lucro como curva de nível, o gradiente, e o procedimento que termina no sistema 2×2 das
  restrições que sustentam o vértice.
- **A primeira ilha interativa do handbook** (`regiao-viavel`): o leitor liga a segunda
  restrição e vê a região encolher, sobe a reta de iso-lucro e vê onde ela encosta por último.
  É o GeoGebra da aula virando objeto do livro, com degradação para o texto sem JavaScript.
- **Dez exercícios** (`cap08`): cinco de resolução com o modelo dado, cinco de modelagem a partir
  de enunciado. Um cai em múltiplos ótimos, um tem ótimo fracionário, um é de minimização com
  restrições de piso, e num deles a restrição que sustenta o vértice é um eixo.
- **`po-zero/etapa-02-metodo-grafico`** — enumeração de vértices por pares de restrições,
  conferida contra o HiGHS nas três etapas.
- **Capítulo 07 reescrito** sobre a montadora, e `etapa-01` refeita para montar o modelo a partir
  da **lista de materiais** — MRP ao contrário — com as duas regras de bolso refutadas por número.

**Os números, e de onde vêm.** Sem restrição, ilimitado. Com 10 CPUs, dez do Tipo 2 e R$ 1.500.
Com 12 pentes de 16 GB, o ótimo anterior deixa de existir (faltavam 8 pentes) e o novo é 8 do
Tipo 1 mais 2 do Tipo 2, R$ 1.100 — a única combinação que esgota os dois recursos. As duas
regras de bolso perdem R$ 200 e R$ 100 por mês. Tudo de `po-zero/etapa-01` e `etapa-02`.

**Portões alterados:**

- A bateria deixa de ser limitada a **quatro** variantes (A–D) e passa a aceitar até 26. O limite
  vinha do livro de origem, onde uma bateria era o mesmo exercício em quatro versões; aqui uma
  bateria é banco de treino.
- A regra "a variante D é a do leitor" virou o campo **`contexto`** (`livro` | `leitor`). A regra
  antiga confundia **posição** na bateria com **natureza** do exercício, e um banco de dez itens
  expôs isso.

**Dívida declarada.** As mesmas duas, agora nos dois capítulos: vídeo sem autoria e duração
conferidas, e ausência de artigos científicos na seção de fundamentos.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.
