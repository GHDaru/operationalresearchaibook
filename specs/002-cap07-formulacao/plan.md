# Plan 002 — Capítulo 07: Formulação de modelos lineares

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-06

## Constitution Check

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | 4 exercícios com devolutiva que explica, corrigidos no servidor. **1 vídeo, ainda sem autoria e duração conferidas** | ⚠️ **dívida declarada** — ver §"A dívida do vídeo" |
| II | Modelar antes de resolver | É o objeto do capítulo. Ordem intuição → matemática → código respeitada; o solver é caixa-preta explícita; seção "quando não serve" com quatro situações e destino de cada uma | ✅ |
| III | Evidência acima de retórica | Todo número vem de `experimento.py`; `resultados.json` traz versões; nenhuma citação inventada. **A seção de fundamentos científicos declara a lacuna em vez de preenchê-la** | ✅ com lacuna declarada |
| IV | Fonte-base é o experimento executável | `po-zero/etapa-01-formulacao` roda em CPU, solver aberto, saída determinística verificada por dupla execução | ✅ |
| V | Arquitetura em três camadas | Capítulo de núcleo; nenhum conteúdo de fronteira entrou | ✅ |
| VI | Atualização por Radar | Nenhum artigo citado, logo nada a registrar. A varredura pendente **entra na fila do Radar** | ✅ |
| VII | Livro vivo | Selo de datação no capítulo; edição 0.3 no histórico com as duas dívidas | ✅ |
| VIII | Português canônico | Só PT, conforme ADR 0002 | ✅ |
| IX | Comunicação inteligível | "Pesquisa Operacional (PO)" e "Programação Linear (PL)" abertas na primeira ocorrência do capítulo | ✅ |
| X | Direitos autorais | Instância autoral com ficha; o contraste entre as obras-base é análise própria, sem reprodução | ✅ |
| XI | DoD verificável | Build e testes verdes, com saída colada em [`verificacao.md`](verificacao.md) | ✅ |

**Violações que impediriam a rodada:** nenhuma. As duas marcas são **dívidas declaradas**, com
prazo e responsável, e estão registradas no `HISTORICO.md` — não escondidas na prosa.

### A dívida do vídeo

O Princípio I pede um vídeo por capítulo; a Videoteca pede autor e duração declarados. Este
ambiente **não consegue ler o YouTube de forma automatizada**, então conferir autoria e duração
na fonte é impossível daqui.

As opções eram: (a) publicar um crédito não verificado, (b) segurar o capítulo inteiro, ou
(c) publicar com `⏳` e dizer por quê. Escolhemos (c): (a) violaria o Princípio III e a regra de
atribuição da própria Videoteca, e (b) trocaria um capítulo inteiro por um campo de metadado.
A decisão está visível ao leitor, no capítulo e na Videoteca.

### A leitura do item 5 do esqueleto

O esqueleto obrigatório reserva a quinta posição para *o algoritmo*. Num capítulo de formulação
não há algoritmo a executar — o que há é **o procedimento de formular**, e ele tem passos tão
definidos quanto os de um método numérico. A seção se chama "O procedimento, passo a passo" e
cumpre a função da posição: método explícito, com exemplo percorrido do zero.

## Estratégia

Quatro blocos, nesta ordem — e a ordem importa porque o texto não pode citar número que ainda
não foi medido:

1. **O experimento primeiro.** `po-zero/etapa-01-formulacao` roda e produz `resultados.json`.
   Só então o capítulo é escrito, citando o que existe.
2. **Objetivos e exercícios antes do corpo** (Backward Design). Se o exercício não se deixa
   escrever, o objetivo está vago.
3. **O capítulo**, no esqueleto do Guia Editorial.
4. **Motor e registro**: capacidade do tutor nos dois lados do espelho, sumário, videoteca,
   histórico.

## Decisões de implementação

| Decisão | Por quê |
|---|---|
| **Instância com duas variáveis e dois recursos** | Pequena o bastante para ser resolvida à mão nos capítulos de geometria e Simplex. O leitor vê o mesmo problema por três lentes, e a economia cognitiva é real |
| **Os dois modelos no mesmo módulo** (`modelo_margem` e `modelo_receita`) | O erro é material didático. Mantê-lo no código, e não só no texto, permite ao leitor rodar os dois e ver a diferença |
| **Sem semente declarada** | O experimento é determinístico. Gravar uma semente não usada seria teatro de reprodutibilidade |
| **Marcador de vaga declarada na navegação** | O livro passa a publicar fora da ordem do mapa. Sem marcador, a lacuna lê como descuido; com ele, lê como plano |

## Mudanças de motor previstas

| Mudança | Por quê |
|---|---|
| `cartaoEnt` passa a aceitar item sem `arquivo` | Sustenta o marcador de vaga declarada como cartão, em vez de fazer a vaga sumir da parte |
| `.ent-card-vaga` no tema | Borda tracejada e sem elevação: parece o que é, um lugar reservado |
| `objetivo` vira campo **obrigatório e verificado** no portão de exercícios | O Guia Editorial afirmava que o build falharia; não falhava. Transformar a afirmação em check é o trabalho (Maestro, Princípio IV) |

## Riscos de implementação

| Risco | Mitigação |
|---|---|
| Número no texto divergir do experimento | Conferência número a número contra `resultados.json`, registrada na verificação |
| O portão novo passar sem medir nada | **Provado quebrando de propósito**: com um objetivo inexistente o build falha; restaurado, passa. A saída está na verificação |
| Exemplo de documentação colidir com rubrica real | Aconteceu. O portão de rubrica pegou, o exemplo foi reescrito e o motivo ficou registrado no próprio Banco de Exercícios |
