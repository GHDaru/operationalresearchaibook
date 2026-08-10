# Bibliografia

> **Conteúdo revisado em 2026-08** · fontes do handbook, com o estado de verificação de cada uma.

Toda afirmação sobre um conceito de Pesquisa Operacional (PO) é rastreável a uma obra desta
lista, citada na primeira ocorrência. O texto do handbook é **autoral**: as obras abaixo são
citadas, nunca reproduzidas (constituição, Princípio X).

## Estado de verificação

| Selo | Significa |
|---|---|
| ✓ | Fonte verificada: metadados conferidos em catálogo oficial ou na própria obra |
| ⏳ | Referência ainda não confirmada na fonte — **não sustenta afirmação no texto** |

---

## Livros-base do curso

Os dois livros didáticos em português que o autor adota com os alunos. São a **base de
compatibilidade** do handbook: cada vaga do [Mapa](mapa-do-handbook.md) recebe a
correspondência com eles, para que um aluno consiga transitar entre o handbook e o livro
impresso sem se perder.

> **O que está registrado aqui:** metadados bibliográficos e a tabela de correspondência —
> só isso. **O que não está, e nunca estará:** o texto, as figuras, os exercícios ou o arquivo
> das obras (constituição, Princípio X; ver [`materiais/README.md`](../materiais/README.md)).

✓ **LACHTERMACHER, Gerson.** *Pesquisa Operacional na Tomada de Decisões*. Rio de Janeiro:
Elsevier/Campus. Edição revista e atualizada, 4ª tiragem. 224 p. — Voltado a Administração,
Economia e Engenharia, com foco declarado em **modelagem prática em planilha eletrônica**. É
o registro que introduz o Simplex por exemplos antes das formas canônicas, e o que traz os
relatórios de sensibilidade do Excel como objeto de leitura.

✓ **ARENALES, Marcos; ARMENTANO, Vinícius Amaral; MORABITO, Reinaldo; YANASSE, Horacio
Hideki.** *Pesquisa Operacional: para cursos de engenharia*. Rio de Janeiro: Elsevier, 2007.
542 p. — A referência brasileira de maior profundidade. Cobre otimização linear, discreta,
em redes, programação dinâmica determinística e estocástica, e sistemas de filas, com forte
peso em **modelagem aplicada** e nos problemas clássicos da área.

### Estrutura das duas obras

| | Lachtermacher (224 p.) | Arenales et al. (542 p.) |
|---|---|---|
| 1 | Introdução a *Management Sciences* — modelagem, decisão, planilhas (p. 1) | Introdução à pesquisa operacional (p. 1) |
| 2 | Programação Linear — gráfica, analítica, teoremas, forma tabular, não-padrão (p. 19) | Otimização linear — aplicações, forma padrão, resolução gráfica, teoria básica e Simplex, Simplex em tabelas, solução inicial, programação de metas, dualidade e sensibilidade, teoria de jogos (p. 15) |
| 3 | Utilização de PL no mundo real — solver, aplicações (p. 51) | Otimização discreta — relaxação linear, modelagem binária, problemas clássicos, logística, produção, *branch-and-bound*, Gomory, *branch-and-cut* (p. 163) |
| 4 | O problema dual e a análise de sensibilidade — relatórios, custo reduzido, ótimos múltiplos, degeneração (p. 85) | Otimização em redes — grafos, caminho mínimo, caminho máximo, árvore geradora mínima, fluxos (p. 289) |
| 5 | Problemas de rede — transporte, escala de produção, distribuição, menor caminho, fluxo máximo (p. 119) | Programação dinâmica determinística (p. 375) |
| 6 | Programação inteira — *branch and bound* (p. 155) | Programação dinâmica estocástica — processos markovianos de decisão (p. 407) |
| 7 | Programação não linear — côncava, convexa, quadrática (p. 171) | Sistemas de filas e otimização (p. 433) |
| Ap. | A — Programação Linear com Lindo (p. 195) | Elementos de sistemas de equações lineares (p. 501) |

### Correspondência com o Mapa do handbook

Leitura: a coluna do livro indica **onde o aluno encontra o mesmo assunto** na obra impressa.
Traço (—) significa que a obra não cobre a vaga — e é exatamente aí que o handbook agrega.

| Parte do handbook | Lachtermacher | Arenales et al. |
|---|---|---|
| **I — Fundamentos** | Unidade 1 | Unidade 1 |
| **II — Programação Linear** | Unidades 2, 3 e 4 | Unidade 2 |
| **III — Redes e Fluxos** | Unidade 5 | Unidade 4 |
| **IV — Programação Inteira** | Unidade 6 (introdutório) | Unidade 3 |
| **V — Heurísticas e Metaheurísticas** | — | — (cobertura marginal) |
| **VI — Otimização Não Linear** | Unidade 7 | — |
| **VII — Otimização sob Incerteza** | — | — |
| **VIII — Modelos Probabilísticos e Dinâmicos** | — | Unidades 5, 6 e 7 |
| **IX — Decisão, Jogos e Multicritério** | — | parte da Unidade 2 (teoria de jogos) |
| **X — Módulos Aplicados** | Unidade 3 (aplicações) | Unidades 2 e 3 (mistura, corte, transporte, produção, roteamento, localização) |
| **XI — Fronteira** | — | — |

**O que essa tabela revela, e que vale como decisão editorial:** as duas obras juntas cobrem
bem as Partes I a IV, VI e VIII. **As Partes V, VII e XI — metaheurísticas, otimização sob
incerteza e fronteira — não têm cobertura em nenhuma das duas.** É a maior contribuição
própria do handbook, e confirma o recorte feito no
[estudo do corpo de conhecimento](../estudos/001-corpo-de-conhecimento-po.md) antes de as
obras serem consultadas.

Duas observações para a rodada de Programação Linear:

1. **A ordem do Lachtermacher separa dualidade de Simplex** (unidades 2 e 4, com as aplicações
   no meio); a do Arenales trata as duas na mesma unidade. O handbook segue a segunda —
   dualidade logo após o Simplex — porque a leitura econômica do preço-sombra é o que dá
   sentido ao algoritmo.
2. **Nenhuma das duas obras tem capítulo sobre casos especiais e degenerescência.** No
   Lachtermacher o assunto aparece diluído na unidade de sensibilidade. O handbook o promove a
   capítulo próprio, porque é onde o aluno descobre que o problema está no **modelo**.

## Obras de referência do campo

✓ **HILLIER, Frederick S.; LIEBERMAN, Gerald J.** *Introduction to Operations Research*.
McGraw-Hill. — A referência internacional mais adotada. Organiza o campo na sequência
canônica: modelagem, programação linear, redes, programação dinâmica, programação inteira,
programação não linear, metaheurísticas, teoria dos jogos, análise de decisão e cadeias de
Markov.
[Registro](https://books.google.com/books/about/Introduction_to_Operations_Research.html?id=NvE5PgAACAAJ)

✓ **WINSTON, Wayne L.** *Operations Research: Applications and Algorithms*. Cengage. — A obra
com maior cobertura da parte probabilística: filas, simulação, estoques determinísticos e
probabilísticos, cadeias de Markov, programação dinâmica e previsão.
[Registro](https://books.google.com/books/about/Operations_Research_Applications_and_Alg.html?id=Y9NYEAAAQBAJ)

✓ **ARENALES, Marcos; ARMENTANO, Vinícius; MORABITO, Reinaldo; YANASSE, Horacio.** *Pesquisa
Operacional: para cursos de engenharia*. Elsevier/Campus. — A referência brasileira. Modelos
determinísticos e probabilísticos com peso maior na modelagem aplicada e no vocabulário de
engenharia de produção.
[Registro](https://books.google.com/books/about/Pesquisa_Operacional.html?hl=pt-BR&id=aZbpCgAAQBAJ)

## Metaheurísticas

✓ **BLUM, Christian; ROLI, Andrea.** *Metaheuristics in Combinatorial Optimization: Overview
and Conceptual Comparison*. — A taxonomia consolidada do campo: métodos de trajetória,
populacionais e híbridos.
[PDF](https://www.iiia.csic.es/~christian.blum/downloads/blum_roli_2003.pdf)

✓ ***A survey of adaptive large neighborhood search algorithms and applications***. *Computers
& Operations Research*. — Revisão dedicada a *Adaptive Large Neighborhood Search* (ALNS), a
família que domina boa parte da prática industrial em roteamento e escalonamento.
[Registro](https://www.sciencedirect.com/science/article/abs/pii/S0305054822001654)

## Aprendizado de máquina e otimização (camada de fronteira)

> Referências desta seção estão sujeitas à cláusula de expiração dos capítulos que as usam.

✓ ***Machine learning augmented branch and bound for mixed integer linear programming***.
*Mathematical Programming*. — Panorama do uso de aprendizado de máquina nas tarefas do
*branch-and-bound*: heurísticas primais, ramificação, planos de corte, seleção de nó e
configuração do solver.
[Registro](https://link.springer.com/article/10.1007/s10107-024-02130-y)

✓ ***Rethinking Branching on Exact Combinatorial Optimization Solver: The First Deep Symbolic
Discovery Framework***. — Descoberta de políticas simbólicas de ramificação, endereçando as
duas limitações reconhecidas da abordagem neural: custo de inferência e interpretabilidade.
[OpenReview](https://openreview.net/forum?id=jKhNBulNMh)

✓ ***Planning in Branch-and-Bound: Model-Based Reinforcement Learning for Exact Combinatorial
Optimization***. [arXiv 2511.09219](https://arxiv.org/pdf/2511.09219)

✓ **Thinklab-SJTU.** *awesome-ml4co* — compilação mantida da literatura de aprendizado de
máquina para otimização combinatória. Útil como ponto de partida, **não** como fonte
verificada de afirmação individual.
[GitHub](https://github.com/Thinklab-SJTU/awesome-ml4co)

## História dos métodos (Princípio XII)

O [Princípio XII](../.specify/memory/constitution.md) exige que todo capítulo de método conte de
onde o método veio — e exige fonte para isso. Esta seção reúne as fontes de **história**, que têm
um problema de verificação próprio: elas são secundárias por natureza (alguém contando o que
outro fez), e este ambiente de trabalho **não alcança arquivo acadêmico**.

Por isso todas nascem `⏳`, e o texto que se apoia nelas diz isso ao leitor, na própria seção.

⏳ **Air Force Salutes Project SCOOP.** *ORMS Today*, INFORMS, 2007. — Sustenta: a força-tarefa
de junho de 1947, o nome do projeto (*Scientific Computation of Optimal Programs*), Dantzig como
matemático-chefe, e o sentido militar de *programming* como plano ou cronograma.
[Página](https://www.informs.org/ORMS-Today/Archived-Issues/2007/orms-12-07/Air-Force-Salutes-Project-SCOOP)

⏳ **The Life and Times of the Father of Linear Programming.** *ORMS Today*, INFORMS, 2005. —
Sustenta: o modelo construído em meados de 1947 e a ausência de método conhecido para resolvê-lo.
[Página](https://pubsonline.informs.org/do/10.1287/orms.2005.04.15/full/)

⏳ **DANTZIG, George B.** *Origins of the Simplex Method*. — O relato do próprio autor. É a fonte
primária que fecharia boa parte destas dívidas, e é justamente a que não consegui abrir.
[Registro](https://dl.acm.org/doi/10.1145/87252.88081)

⏳ **MacTutor History of Mathematics — George Dantzig.** University of St Andrews. — Biografia de
referência; corrobora datas e trajetória.
[Página](https://mathshistory.st-andrews.ac.uk/Biographies/Dantzig_George/)

⏳ **Atribuição do *big-M* a A. Charnes** ("método das penalidades"). — **Atribuição corrente na
literatura didática**, repetida em material de curso, e **não confirmada em fonte primária**. O
capítulo 09 declara esse estado explicitamente, em vez de tratá-la como fato estabelecido.

> **O que falta para estas saírem do `⏳`.** Abrir as fontes. Hoje `arxiv.org`,
> `api.crossref.org`, `api.openalex.org` e os sites das editoras respondem `403` ao proxy de
> saída deste ambiente. É uma dívida de **acesso**, não de pesquisa, e some no dia em que o
> acesso existir.

---

## Material didático aberto

✓ **CUNHA, Alexandre Salles da.** *DCC035 — Pesquisa Operacional*, UFMG. — Curso completo com
aproximadamente 55 aulas gravadas (cerca de 30 horas) publicadas como material de apoio.
[Página do curso](https://homepages.dcc.ufmg.br/~acunha/po/po.html)

✓ **SARUBBI, João.** Canal de Lógica, Matemática Discreta e Pesquisa Operacional. CEFET-MG. —
**Uso autorizado pelo autor do canal.** É a fonte curada primária de vídeo do handbook; a
política está na [Videoteca](videoteca.md).
[Canal](https://www.youtube.com/@joaosarubbi)

---

## Como esta lista cresce

Uma referência entra aqui **depois** de passar pelo [Radar](../radar/RADAR.md) — lida, datada
e com o registro do que ela muda no livro (constituição, Princípio VI). Referência que aparece
na bibliografia sem linha correspondente no Radar é dívida a corrigir, não atalho.

Metadados de obras impressas seguem o padrão autor–título–editora–ano–ISBN. Artigos seguem o
padrão com identificador de objeto digital (DOI) ou identificador do arXiv, sempre conferido
na fonte.
