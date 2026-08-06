# Estudo 001 — O corpo de conhecimento da Pesquisa Operacional

> **Pesquisa capturada em 2026-08** · insumo da rodada `001-fundacao-e-sumario` · autor: Gilsiley Henrique Darú, com apoio de agente de IA.

Este documento é o **insumo** do sumário do handbook. Ele levanta como o campo se organiza hoje — nos livros-texto de referência, nas revistas científicas e nas ementas de curso — e registra as decisões de recorte que produziram [`livro/mapa-do-handbook.md`](../livro/mapa-do-handbook.md).

Não é capítulo de livro: é nota de pesquisa. O que aqui é hipótese, está marcado como hipótese.

## 1. A pergunta desta pesquisa

O pedido do autor tem quatro exigências que puxam em direções diferentes:

1. **Fundamentação sedimentada** — cobrir Pesquisa Operacional (PO) inteira, não um recorte.
2. **Handbook evolutivo** — crescer por adição, sem reescrever o que já existe.
3. **Módulos aplicados por área** — modelagem situada em domínios reais.
4. **Atualização científica contínua** — heurísticas, metaheurísticas e artigos aplicados entrando no livro ao longo do tempo.

Um sumário que atenda só a (1) vira livro-texto comum e morre na primeira edição. Um que atenda só a (3) e (4) vira coletânea sem espinha. **A tensão central deste estudo é essa**, e a §5 registra como ela foi resolvida.

## 2. Como os livros-texto de referência organizam o campo

Três obras dominam as ementas de PO no mundo e no Brasil. O que elas concordam é o que se pode chamar de núcleo do campo.

### Hillier & Lieberman — *Introduction to Operations Research*

A obra mais adotada internacionalmente. A 9ª edição organiza o campo em dezesseis capítulos: introdução e a abordagem de modelagem; programação linear (formulação, Simplex, teoria do Simplex, dualidade e sensibilidade, outros algoritmos); transporte e designação; otimização em redes; programação dinâmica; programação inteira; programação não linear; metaheurísticas; teoria dos jogos; análise de decisão; cadeias de Markov. ([Hillier & Lieberman](https://dokumen.pub/introduction-to-operations-research-9nbsped-0073376299-9780073376295.html))

**O que aprendemos daqui:** a sequência canônica é **modelagem → PL → redes → inteira → não linear → metaheurísticas → estocástico**. Ela não é arbitrária: cada bloco usa o anterior como ferramenta.

### Winston — *Operations Research: Applications and Algorithms*

Mais largo na parte probabilística. Cobre álgebra linear básica, PL, Simplex e programação por metas, sensibilidade, transporte/designação/transbordo, redes, programação inteira, tópicos avançados de PL, programação não linear, decisão sob incerteza, teoria dos jogos, modelos de estoque determinísticos (EOQ) e probabilísticos, cadeias de Markov, programação dinâmica determinística e probabilística, teoria de filas, simulação e modelos de previsão. ([Winston](https://books.google.com/books/about/Operations_Research_Applications_and_Alg.html?id=Y9NYEAAAQBAJ))

**O que aprendemos daqui:** **filas, simulação, estoques e previsão** são parte do campo, não apêndice. Um handbook que pare na otimização determinística cobre menos da metade do que a prática usa.

### Arenales, Armentano, Morabito & Yanasse — *Pesquisa Operacional (para cursos de engenharia)*

A referência brasileira. Introduz modelos determinísticos e probabilísticos e os principais métodos de solução, com material declarado como suficiente para dois cursos semestrais, voltado à Engenharia de Produção. Traz otimização discreta e um tratamento próprio de redes e grafos (caminho mínimo, caminho máximo, árvore geradora mínima, problemas de fluxo). ([Arenales et al.](https://books.google.com/books/about/Pesquisa_Operacional.html?hl=pt-BR&id=aZbpCgAAQBAJ))

**O que aprendemos daqui:** a tradição brasileira dá **peso maior à modelagem aplicada** e ao vocabulário de engenharia de produção. É o registro em que os alunos do autor vão reconhecer o campo.

### Convergência

| Bloco | Hillier | Winston | Arenales |
|---|---|---|---|
| Modelagem e ciclo de PO | ✓ | ✓ | ✓ |
| Programação linear + Simplex + dualidade | ✓ | ✓ | ✓ |
| Redes e fluxos | ✓ | ✓ | ✓ |
| Programação inteira | ✓ | ✓ | ✓ |
| Programação não linear | ✓ | ✓ | ✓ |
| Programação dinâmica | ✓ | ✓ | ✓ |
| Metaheurísticas | ✓ | — | parcial |
| Filas / estoques / simulação | parcial | ✓ | ✓ |
| Decisão / jogos | ✓ | ✓ | — |

**Conclusão da §2:** há um núcleo de sete blocos em que as três obras concordam. Esse núcleo é a espinha do handbook e não pode ser negociado por módulos aplicados.

## 3. O que os livros-texto cobrem mal

Aqui a pesquisa sai dos livros e vai para a literatura científica — é onde o pedido de "evolutivo" ganha conteúdo.

### 3.1 Metaheurísticas

A taxonomia consolidada separa **métodos de trajetória** (solução única), **métodos populacionais** e **híbridos**. Entre os de trajetória: *Simulated Annealing*, Busca Tabu, GRASP, *Variable Neighborhood Search*, *Guided Local Search*, *Iterated Local Search*. ([Blum & Roli](https://www.iiia.csic.es/~christian.blum/downloads/blum_roli_2003.pdf))

Duas famílias que os livros-texto praticamente não alcançam, e que dominam a prática industrial atual:

- **ALNS (*Adaptive Large Neighborhood Search*)** — destrói e repara grandes porções da solução, com pesos adaptativos entre operadores. Existe *survey* dedicado a algoritmos e aplicações. ([Survey ALNS](https://www.sciencedirect.com/science/article/abs/pii/S0305054822001654))
- **Matheuristics e hiper-heurísticas** — combinam solver exato e heurística; a hiper-heurística busca no espaço de heurísticas, não no de soluções.

Em roteamento de veículos, as metaheurísticas efetivamente usadas são *simulated annealing*, busca tabu, ILS, LNS, algoritmos genéticos, colônia de formigas e meméticos.

**Consequência para o sumário:** metaheurísticas merecem um **módulo inteiro**, não um capítulo — e precisam de um capítulo próprio sobre *como avaliar* um algoritmo (benchmarks, perfis de desempenho, reprodutibilidade), que é justamente o que separa artigo sério de artigo com número bonito.

### 3.2 Aprendizado de máquina aplicado à otimização combinatória (ML4CO)

Área em explosão. O aprendizado de máquina vem sendo usado para acelerar **todas as tarefas principais do *branch-and-bound***: heurísticas primais, seleção de variável de ramificação, planos de corte, seleção de nó e configuração do solver. ([ML augmented B&B, *Mathematical Programming*](https://link.springer.com/article/10.1007/s10107-024-02130-y))

Limites honestos, hoje: **custo de treino e inferência elevado e interpretabilidade limitada** restringem a adoção em solvers exatos modernos. Linhas de 2025 incluem seleção de variável, configuração dinâmica de separadores de corte por aprendizado por reforço, garantias de generalização para políticas de *branch-and-cut* e descoberta simbólica de políticas de ramificação. ([Deep symbolic branching](https://openreview.net/forum?id=jKhNBulNMh) · [Planning in B&B](https://arxiv.org/pdf/2511.09219) · [awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co))

**Consequência para o sumário:** existe uma **Parte de fronteira**, com cláusula de expiração explícita, onde este tema vive. Ele não entra no núcleo — o núcleo precisa envelhecer devagar.

### 3.3 Otimização sob incerteza

Programação estocástica, otimização robusta e otimização *distributionally robust* aparecem de forma marginal nos três livros-texto e são hoje requisito em energia, saúde e cadeia de suprimentos.

**Consequência:** módulo próprio, entre o determinístico e o probabilístico.

## 4. Vídeos: o que existe em português

O handbook usa vídeo pelo que o texto não faz bem (geometria animada, ritmo de derivação no quadro) — a política vem do livro de Machine Learning do mesmo autor.

- **Canal de João Sarubbi** ([@joaosarubbi](https://www.youtube.com/@joaosarubbi)) — professor titular do CEFET-MG; o canal cobre Lógica, Matemática Discreta e Pesquisa Operacional, com legendas, animações e efeitos sonoros. **O autor recebeu convite para uso dos vídeos** — é a fonte curada primária do handbook, registrada em [`livro/videoteca.md`](../livro/videoteca.md).
- **DCC035 / UFMG** — curso de Pesquisa Operacional com cerca de 55 aulas (~30 h) publicadas como material de apoio. ([DCC035](https://homepages.dcc.ufmg.br/~acunha/po/po.html))

**Conclusão:** há material gratuito e estável em português suficiente para cumprir o mínimo de um vídeo por capítulo no núcleo. Para os módulos de fronteira, a expectativa é material em inglês — e isso é dívida declarada, não surpresa.

## 5. Decisões de recorte

As quatro exigências da §1 foram resolvidas por uma **arquitetura de três camadas**, e não por uma lista única de capítulos.

| Camada | O que é | Como envelhece |
|---|---|---|
| **Núcleo** (Partes I–IX) | O que as três obras de referência concordam em chamar de PO. Fundamentação. | Devagar. Revisão por janela, não por evento. |
| **Aplicados** (Parte X) | Um módulo por domínio: cada um é uma unidade fechada de modelagem situada. | Cresce **por adição**. Um módulo novo não toca nos outros. |
| **Fronteira** (Parte XI) | ML4CO, *decision-focused learning*, otimização com IA generativa. | Rápido. **Cláusula de expiração obrigatória** em todo capítulo. |

Três decisões que decorrem disso, e que estão registradas como ADR:

1. **A estrutura é declarativa** — um módulo aplicado novo é um arquivo `.md` mais uma entrada no `sumario.json`. Nenhuma mudança de motor. (Herdado do motor; [ADR 0001](../adr/0001-reuso-motor-livro-vivo.md).)
2. **O Radar científico é o mecanismo de atualização**, e não a boa vontade de reler o campo. Artigo lido vira linha datada no radar; linha do radar que muda uma recomendação vira revisão do capítulo. ([ADR 0004](../adr/0004-arquitetura-do-sumario.md))
3. **Fronteira não vira núcleo por entusiasmo.** Um tema sobe de camada quando resiste a duas janelas de revisão sem ser refutado.

## 6. Lacunas desta pesquisa (honestidade)

- **Os sumários completos dos livros-base não foram verificados na fonte.** Hillier e Winston vieram de páginas de catálogo e de repositórios de terceiros; o de Arenales não foi obtido em detalhe. Quando o autor anexar os dois livros didáticos de referência, o mapeamento capítulo-a-capítulo entra em `livro/bibliografia.md` e este estudo é corrigido.
- **Não foi feita revisão sistemática de metaheurísticas.** O que está na §3.1 é a taxonomia consolidada mais dois *surveys*; uma revisão com protocolo é trabalho de outra rodada.
- **A cobertura de vídeos em português não foi inventariada por capítulo.** Sabe-se que existe massa crítica; não se sabe onde ela falha. O inventário é tarefa da rodada de Programação Linear, para o escopo dela.

## Fontes

- [Hillier & Lieberman — *Introduction to Operations Research*, 9ª ed.](https://dokumen.pub/introduction-to-operations-research-9nbsped-0073376299-9780073376295.html)
- [Winston — *Operations Research: Applications and Algorithms*](https://books.google.com/books/about/Operations_Research_Applications_and_Alg.html?id=Y9NYEAAAQBAJ)
- [Arenales, Armentano, Morabito & Yanasse — *Pesquisa Operacional*](https://books.google.com/books/about/Pesquisa_Operacional.html?hl=pt-BR&id=aZbpCgAAQBAJ)
- [Blum & Roli — *Metaheuristics in Combinatorial Optimization: Overview and Conceptual Comparison*](https://www.iiia.csic.es/~christian.blum/downloads/blum_roli_2003.pdf)
- [*A survey of adaptive large neighborhood search algorithms and applications*](https://www.sciencedirect.com/science/article/abs/pii/S0305054822001654)
- [*Machine learning augmented branch and bound for mixed integer linear programming*](https://link.springer.com/article/10.1007/s10107-024-02130-y)
- [*Rethinking Branching on Exact Combinatorial Optimization Solver*](https://openreview.net/forum?id=jKhNBulNMh)
- [*Planning in Branch-and-Bound*](https://arxiv.org/pdf/2511.09219)
- [awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co)
- [Canal de João Sarubbi](https://www.youtube.com/@joaosarubbi)
- [DCC035 — Pesquisa Operacional, UFMG](https://homepages.dcc.ufmg.br/~acunha/po/po.html)
