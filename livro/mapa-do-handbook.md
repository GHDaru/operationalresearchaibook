# Mapa do handbook

> **Conteúdo revisado em 2026-08** · versão 1 do sumário · [histórico](HISTORICO.md)

Este é o **sumário declarado** do handbook: o mapa inteiro do que ele pretende cobrir, publicado antes de estar escrito. O [sumário de navegação](sumario.html) mostra só o que já existe; esta página mostra o destino.

Publicar o mapa antes do conteúdo é decisão editorial, não descuido. Um handbook evolutivo sem mapa vira coletânea: cada capítulo novo negocia o próprio lugar, e a espinha se perde. Com o mapa declarado, um capítulo novo **ocupa uma vaga que já existia**.

## Como ler este mapa

| Selo | Significa |
|---|---|
| ✅ | Publicado |
| 🚧 | Próxima rodada — já com escopo definido no [roadmap](../ROADMAP.md) |
| ⬜ | Vaga declarada, ainda não escrita |

O fundamento do recorte — por que estas partes, nesta ordem — está no [estudo do corpo de conhecimento](../estudos/001-corpo-de-conhecimento-po.md).

## A arquitetura em três camadas

O handbook não é uma lista de capítulos: são três camadas que envelhecem em ritmos diferentes.

| Camada | Partes | O que é | Ritmo |
|---|---|---|---|
| **Núcleo** | I – IX | A fundamentação em que os livros-texto de referência concordam | Envelhece devagar; revisão por janela |
| **Aplicados** | X | Um módulo por domínio, cada um fechado em si | Cresce **por adição**, indefinidamente |
| **Fronteira** | XI | O que está se movendo agora na literatura | Envelhece rápido; **expiração obrigatória** |

Essa separação é o que permite as duas promessas ao mesmo tempo: fundamentação sedimentada **e** atualização constante. O que se atualiza toda semana não fica onde o aluno aprende a base.

---

## Abertura

| | Capítulo | Do que trata |
|---|---|---|
| ✅ | **00 — Introdução** | O que é este handbook, para quem, e como se estuda por ele. |

## Parte I — Fundamentos da Pesquisa Operacional

A porta de entrada. Termina com o leitor sabendo **reconhecer um problema de PO** e escolher a família de método antes de escrever qualquer modelo.

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 01 — O que é Pesquisa Operacional | Origem, natureza e o que distingue PO de "usar matemática no negócio". |
| ⬜ | 02 — O ciclo de modelagem | Da situação confusa ao modelo: definir, formular, resolver, validar, implantar. |
| ⬜ | 03 — Anatomia de um modelo de otimização | Variáveis de decisão, função objetivo, restrições, parâmetros — e o que cada erro nesses quatro produz. |
| ⬜ | 04 — Classificação de problemas e escolha de método | O mapa de decisão: linear ou não, inteiro ou contínuo, determinístico ou estocástico. |
| ⬜ | 05 — Complexidade computacional para quem modela | P, NP e o que a teoria decide na prática: quando parar de buscar o ótimo. |
| ⬜ | 06 — Ferramentas de trabalho | Solvers, linguagens de modelagem e dados. Instalação do `po-zero`. |

## Parte II — Programação Linear

O coração do handbook. Os dois primeiros capítulos estão publicados; o Simplex é a próxima
rodada de método. É aqui que o aluno aprende a modelar de verdade, e é a base de tudo que vem depois.

| | Capítulo | Do que trata |
|---|---|---|
| ✅ | 07 — Formulação de modelos lineares | Traduzir o problema em variáveis, objetivo e restrições. O capítulo mais praticado do livro. |
| ✅ | 08 — A geometria da Programação Linear | Semiespaços, região viável e por que nunca é preciso procurar o ótimo fora das quinas. |
| ✅ | 09 — O método Simplex | O algoritmo por dentro: base, pivoteamento, critério de entrada e saída, e a partida artificial por *big-M*. |
| 🚧 | 10 — Casos especiais e degenerescência | Ilimitado, inviável, múltiplos ótimos, ciclagem — e o que cada um diz sobre o **modelo**. |
| ⬜ | 11 — Simplex revisado e implementação eficiente | Forma matricial, fatoração e por que o solver real não faz o que o quadro faz. |
| ⬜ | 12 — Dualidade | O modelo espelho, o teorema forte e a leitura econômica dos preços-sombra. |
| ⬜ | 13 — Análise de sensibilidade e pós-otimização | O que a resposta suporta antes de mudar. A parte que o gestor de fato usa. |
| ⬜ | 14 — Métodos de pontos interiores | A alternativa que domina os problemas grandes, e quando ela ganha do Simplex. |
| ⬜ | 15 — Modelagem aplicada em PL | Mix de produção, mistura, corte, escalonamento, multiperíodo — o repertório de padrões. |

## Parte III — Otimização em Redes e Fluxos

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 16 — Grafos e redes: fundamentos | O vocabulário e a estrutura que atravessa metade da PO aplicada. |
| ⬜ | 17 — Caminho mínimo | Dijkstra, Bellman-Ford e as aplicações que não parecem caminho. |
| ⬜ | 18 — Árvore geradora mínima e projeto de redes | Quando a decisão é que ligações construir. |
| ⬜ | 19 — Fluxo máximo e corte mínimo | O teorema que transforma capacidade em gargalo — e a ponte com a Teoria das Restrições. |
| ⬜ | 20 — Fluxo de custo mínimo | O modelo que generaliza transporte, designação e transbordo. |
| ⬜ | 21 — Transporte, designação e transbordo | Os clássicos, com seus métodos especializados. |
| ⬜ | 22 — Planejamento de projetos: PERT e CPM | Caminho crítico, folgas e a leitura probabilística do prazo. |

## Parte IV — Programação Inteira e Otimização Combinatória

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 23 — Modelagem com variáveis inteiras e binárias | Ativação, escolha, lógica condicional, *big-M* — e o preço de cada truque. |
| ⬜ | 24 — Qualidade da formulação | Por que dois modelos corretos do mesmo problema levam horas e segundos. |
| ⬜ | 25 — *Branch and bound* | A enumeração inteligente: limitantes, poda e estratégias de ramificação. |
| ⬜ | 26 — Planos de corte e *branch and cut* | Apertar a relaxação: cortes de Gomory, de cobertura e os do solver. |
| ⬜ | 27 — Relaxação lagrangeana e limitantes | Obter garantia de qualidade quando o ótimo não vem. |
| ⬜ | 28 — Geração de colunas e decomposição de Dantzig-Wolfe | Modelos com variáveis demais para escrever. |
| ⬜ | 29 — Decomposição de Benders | Separar decisões estruturais das operacionais. |
| ⬜ | 30 — Programação por restrições | O paradigma vizinho: propagação e busca, e quando ele vence a PI. |

## Parte V — Heurísticas e Metaheurísticas

Módulo inteiro, e não um capítulo: é o que a indústria usa quando o exato não fecha.

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 31 — Heurísticas construtivas | Gulosas, por inserção, por decomposição. Como nasce uma solução inicial. |
| ⬜ | 32 — Busca local e estrutura de vizinhança | O motor comum de quase toda metaheurística. |
| ⬜ | 33 — Metaheurísticas de trajetória | *Simulated Annealing*, Busca Tabu, ILS, VNS, GRASP. |
| ⬜ | 34 — Metaheurísticas populacionais | Algoritmos genéticos e meméticos, colônia de formigas, enxame de partículas, evolução diferencial. |
| ⬜ | 35 — LNS, ALNS e *matheuristics* | Destruir e reparar; usar o solver exato dentro da heurística. |
| ⬜ | 36 — Hiper-heurísticas e configuração automática | Buscar no espaço de algoritmos, não no de soluções. |
| ⬜ | 37 — Como avaliar um algoritmo | Instâncias, *benchmarks*, perfis de desempenho, testes estatísticos, reprodutibilidade. **O capítulo que ensina a ler artigo com desconfiança.** |

## Parte VI — Otimização Não Linear

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 38 — Convexidade | A propriedade que decide se o problema é tratável. |
| ⬜ | 39 — Otimização irrestrita | Gradiente, Newton, quase-Newton e critérios de parada. |
| ⬜ | 40 — Otimização com restrições | Multiplicadores de Lagrange, condições KKT, dualidade não linear. |
| ⬜ | 41 — Programação quadrática, cônica e semidefinida | As classes que ainda são resolvidas com garantia. |
| ⬜ | 42 — Otimização global e MINLP | Quando não há garantia: relaxações, envelopes e o que se pode prometer. |

## Parte VII — Otimização sob Incerteza

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 43 — Decisão sob incerteza e risco | Cenários, valor esperado, aversão a risco, valor da informação. |
| ⬜ | 44 — Programação estocástica de dois estágios | Recurso, cenários e o *valor da solução estocástica*. |
| ⬜ | 45 — Programação estocástica multiestágio | Árvores de cenário e decomposição. |
| ⬜ | 46 — Otimização robusta | Conjuntos de incerteza, preço da robustez e o caso *distributionally robust*. |
| ⬜ | 47 — Otimização por simulação | Quando não há modelo fechado do objetivo. |

## Parte VIII — Modelos Probabilísticos e Dinâmicos

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 48 — Cadeias de Markov | Estados, transições, regime estacionário e o que se decide com isso. |
| ⬜ | 49 — Teoria de filas | Por que a fila explode antes da capacidade acabar. A matemática da variabilidade. |
| ⬜ | 50 — Programação dinâmica | Princípio da otimalidade, recursão e a maldição da dimensionalidade. |
| ⬜ | 51 — Processos de decisão de Markov | Política ótima, iteração de valor e de política — e a ponte com aprendizado por reforço. |
| ⬜ | 52 — Simulação de eventos discretos | Construir, validar e extrair decisão de um simulador. |
| ⬜ | 53 — Previsão de demanda para decisão | Séries temporais na medida em que alimentam um modelo de otimização. |

## Parte IX — Decisão, Jogos e Multicritério

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 54 — Análise de decisão | Árvores de decisão, utilidade e valor da informação perfeita. |
| ⬜ | 55 — Teoria dos jogos | Equilíbrio, jogos cooperativos e o que muda quando o outro também otimiza. |
| ⬜ | 56 — Decisão multicritério | AHP, TOPSIS, PROMETHEE, ELECTRE — e a crítica metodológica a cada um. |
| ⬜ | 57 — Otimização multiobjetivo | Fronteira de Pareto, escalarização e algoritmos evolutivos multiobjetivo. |
| ⬜ | 58 — Análise Envoltória de Dados | Eficiência relativa entre unidades, e seus limites. |

## Parte X — Módulos Aplicados

**A camada que cresce.** Cada módulo é uma unidade fechada: o problema do domínio, os modelos consagrados, os artigos que definem o estado da prática, e um caso completo no `po-zero`. Um módulo novo entra sem tocar em nenhum outro.

| | Módulo | Do que trata |
|---|---|---|
| ⬜ | 59 — Cadeia de suprimentos e projeto de rede | Localização de instalações, rede de distribuição, decisões estratégicas. |
| ⬜ | 60 — Roteamento de veículos | VRP e suas variantes: janelas de tempo, frota heterogênea, coleta e entrega. |
| ⬜ | 61 — Planejamento e programação da produção | Dimensionamento de lotes, sequenciamento, *job shop*, integração com MRP. |
| ⬜ | 62 — Gestão de estoques | Políticas, nível de serviço, estoque de segurança, multiescalão. |
| ⬜ | 63 — Corte e empacotamento | Corte unidimensional e bidimensional, carregamento de contêiner. |
| ⬜ | 64 — Escala de pessoal | Dimensionamento, escalas cíclicas, *rostering*, regras trabalhistas como restrição. |
| ⬜ | 65 — Energia | Despacho econômico, *unit commitment*, integração de renováveis. |
| ⬜ | 66 — Saúde | Bloco cirúrgico, escala médica, alocação de leitos, filas de atendimento. |
| ⬜ | 67 — Transporte e mobilidade | Redes de transporte público, alocação de tráfego, logística urbana. |
| ⬜ | 68 — Finanças | Seleção de portfólio, casamento de ativos e passivos, risco. |
| ⬜ | 69 — *Revenue management* e precificação | Alocação de capacidade, *overbooking*, precificação dinâmica. |
| ⬜ | 70 — Agronegócio e recursos naturais | Planejamento de safra, colheita, uso do solo, água. |
| ⬜ | 71 — Serviços públicos e emergência | Localização de ambulâncias, resposta a desastres, alocação orçamentária. |

> Esta lista é **aberta por desenho**. Um domínio novo — mineração, telecomunicações, esporte, defesa — entra como módulo adicional sem renumerar nada, porque o motor monta o livro a partir do `sumario.json`.

## Parte XI — Fronteira

Camada de vida curta. **Todo capítulo aqui declara cláusula de expiração**: a data em que a afirmação deixa de valer sem reverificação.

| | Capítulo | Do que trata |
|---|---|---|
| ⬜ | 72 — Aprendizado de máquina para otimização combinatória | ML dentro do *branch-and-bound*: ramificação, cortes, heurísticas primais, configuração. |
| ⬜ | 73 — *Predict-then-optimize* e aprendizado orientado à decisão | Quando treinar para prever bem não é treinar para decidir bem. |
| ⬜ | 74 — Otimização neural e solvers aprendidos | O que já entrega valor e o que ainda é promessa. |
| ⬜ | 75 — Modelos de linguagem como modeladores | Da descrição em texto ao modelo executável: o que funciona, o que quebra, como verificar. |
| ⬜ | 76 — Otimização responsável | Equidade, transparência e o que acontece com quem o modelo otimiza contra. |
| ⬜ | 77 — Como ler um artigo científico de PO | Protocolo de leitura crítica: instância, *baseline*, teste estatístico, reprodutibilidade. |

## Aparato

| | Página | Do que trata |
|---|---|---|
| ✅ | **Radar científico** | Artigos lidos, datados, com o que cada um muda no livro. É o motor da atualização contínua. |
| ✅ | **Bibliografia** | As fontes, com os livros-base do curso mapeados capítulo a capítulo. |
| ✅ | **Videoteca** | A curadoria de vídeos e a política que a governa. |
| ✅ | **Glossário** | Os termos e as siglas, abertos na primeira ocorrência. |
| ✅ | **Guia Editorial** | Como se escreve um capítulo deste livro. |
| ✅ | **Histórico** | O que mudou a cada edição, com data. |

## O que este mapa ainda não resolve

Honestidade sobre o próprio sumário:

1. **A ordem interna das Partes VI a IX não está testada com alunos.** Filas antes ou depois de programação dinâmica é discussão em aberto.
2. **A Parte X não tem prioridade declarada.** Qual módulo aplicado vem primeiro é decisão do autor em função da turma, e entra no [roadmap](../ROADMAP.md).
3. **Nenhuma vaga aqui é promessa de prazo.** Vaga declarada significa lugar reservado na estrutura, não compromisso de data.
4. **Os livros-base ainda não foram mapeados.** Quando os dois livros didáticos de referência forem anexados, cada capítulo deste mapa ganha a correspondência com eles na [bibliografia](bibliografia.md).

### Leitura executiva

O handbook cobre Pesquisa Operacional em **três camadas com ritmos diferentes**: um núcleo de nove partes (Fundamentos, Programação Linear, Redes, Programação Inteira, Metaheurísticas, Não Linear, Incerteza, Modelos Probabilísticos, Decisão), uma camada de módulos aplicados que cresce por adição sem tocar no núcleo, e uma camada de fronteira com expiração obrigatória. São 77 vagas declaradas mais o aparato. A separação em camadas é o que permite fundamentação estável e atualização científica constante ao mesmo tempo — o que se move rápido não fica onde o aluno aprende a base. A Parte II está em construção: formulação e geometria publicadas, o Simplex a seguir.
