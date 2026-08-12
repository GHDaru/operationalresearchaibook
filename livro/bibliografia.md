# Bibliografia

> **Conteúdo revisado em 2026-08** · fontes do handbook, com o estado de verificação de cada uma.

Toda afirmação sobre um conceito de Pesquisa Operacional (PO) é rastreável a uma obra desta
lista, citada na primeira ocorrência. O texto do handbook é **autoral**: as obras abaixo são
citadas, nunca reproduzidas (constituição, Princípio X).

## Estado de verificação

Cada selo diz **o que foi provado**, e a distinção que sustenta o sistema é entre os dois
primeiros: **existir não é dizer.** Metadados conferidos provam que a obra existe e é aquela;
não provam uma linha do que ela afirma.

| Selo | Nome | O que prova | O que **não** prova |
|---|---|---|---|
| ✓ | verificada | **Um humano abriu a fonte e leu** o trecho que sustenta a afirmação | — |
| ✓ᵐ | metadados | O registro **existe** e autor, título, ano e veículo conferem | Nada sobre o conteúdo |
| ⏳ | atribuição corrente | A afirmação circula na literatura e **não foi confirmada na fonte** | **Não sustenta afirmação no texto** |
| ❌ | sem fonte | Foi procurado e **não foi encontrado** | — |
| 📖 | leitura editorial | Interpretação **autoral**, declarada como tal | — |

> **Quem escreve o selo.** Só quem leu. Nenhum portão, agente ou script promove selo: o
> `verifica-fontes.mjs` confere identificadores e é somente leitura, e o teto do que qualquer
> automação pode sustentar é `✓ᵐ` — porque resolver um identificador prova existência e
> metadados, que é exatamente o significado desse selo. Ver
> [ADR 0010](../adr/0010-a-semantica-do-selo.md).

> **O que é verificado por máquina, e o que não é.** Os identificadores de objeto digital
> (DOI, *Digital Object Identifier*) desta página passam por portão no `npm run build`: o DOI
> tem de existir no registro, e o trabalho que ele identifica tem de ser o que está declarado
> aqui. São **12 de 31 obras distintas — 39%**. Livro impresso, página institucional e
> identificador do arXiv **continuam sendo afirmação humana** — assim como toda URL comum.
>
> A conta, reproduzível: `grep -cE "^(✓ᵐ|✓|⏳|❌|📖) " livro/bibliografia.md` dá **36**;
> quatro dessas linhas são **atribuições**, não obras, e uma obra aparece duas vezes.

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
onde o método veio — e exige fonte para isso. Esta seção reúne as fontes de **história**.

> **Nota de estado, 2026-08-09.** Estas entradas nasceram todas `⏳` porque o ambiente de trabalho
> não alcançava arquivo acadêmico. Com o acesso liberado, as fontes foram **abertas e lidas**, e a
> maioria virou `✓`. O que continua `⏳` está marcado item a item, e o motivo é dito.

### Origem do Simplex e da Programação Linear

✓ **DANTZIG, George B.** "The Diet Problem". *Interfaces*, v. 20, n. 4, p. 43–47, 1990.
DOI [10.1287/inte.20.4.43](https://doi.org/10.1287/inte.20.4.43). — **Fonte primária do capítulo
07.** Relato do próprio Dantzig: o modelo de Stigler, a computação de Laderman em 1947 (9 equações
e 77 incógnitas, nove escriturários, ~120 dias-de-trabalho, ótimo de US$ 39,69), a *Table Cloth*,
e o episódio da própria dieta — os 500 galões de vinagre, os 200 tabletes de caldo e a origem dos
limitantes superiores em variáveis.

✓ **STIGLER, George J.** "The Cost of Subsistence". *Journal of Farm Economics*, v. 27, n. 2,
p. 303, 1945. DOI [10.2307/1231810](https://doi.org/10.2307/1231810). — O artigo que formula o
problema da dieta. Metadados conferidos no Crossref; o **texto integral não foi lido**, e tudo o
que o handbook afirma sobre o conteúdo vem do relato de Dantzig acima.

✓ **"Air Force Salutes Project SCOOP".** *OR/MS Today*, INFORMS, dez. 2007. — **Fonte do
capítulo 09**: a força-tarefa de junho de 1947, um mês antes de a Força Aérea virar ramo separado;
o nome Projeto SCOOP (*Scientific Computation of Optimal Programs*) dado depois; Dantzig como
matemático-chefe.
[Página](https://www.informs.org/ORMS-Today/Archived-Issues/2007/orms-12-07/Air-Force-Salutes-Project-SCOOP)

✓ **MacTutor History of Mathematics — George Dantzig.** University of St Andrews. — Sustenta o
sentido militar de *programming* ("planos ou cronogramas para treinamento, suprimento logístico ou
deslocamento de pessoal"), a expressão original de Dantzig (*programming in a linear structure*) e
o batismo do termo "linear programming" por **T. J. Koopmans**, na RAND, em 1948. Cita
diretamente *Linear Programming and Extensions* (Dantzig, 1963).
[Página](https://mathshistory.st-andrews.ac.uk/Biographies/Dantzig_George/)

⏳ **DANTZIG, George B.** "Origins of the simplex method". In: *A History of Scientific Computing*,
p. 141–151, 1990. DOI [10.1145/87252.88081](https://doi.org/10.1145/87252.88081). — Metadados
conferidos; **o texto continua inacessível** (a editora responde `403` a acesso automatizado). É a
fonte que fecharia a atribuição do nome *simplex* a Motzkin.

⏳ **Atribuição do nome *simplex* a T. S. Motzkin.** — Atribuição corrente, repetida em material
didático e em levantamentos históricos; **não confirmada em fonte primária**.

### O *big-M*

✓ **CHARNES, A.** "Optimality and Degeneracy in Linear Programming". *Econometrica*, v. 20, n. 2,
p. 160, 1952. DOI [10.2307/1907845](https://doi.org/10.2307/1907845). — Metadados conferidos no
Crossref. É a referência a que a literatura didática atribui o método das penalidades.

⏳ **Atribuição do *big-M* a Charnes.** — O **conteúdo** do artigo acima não foi lido, então a
atribuição segue como corrente e não confirmada. O capítulo 09 declara isso ao leitor.

❌ **A origem da letra M.** — Sem fonte. A leitura óbvia é *muito grande*; leitura óbvia não é
documento.

### Geometria das desigualdades lineares

✓ **Levantamento histórico sobre o Simplex e sistemas de desigualdades**, arXiv:2305.03730. —
**Fonte do capítulo 08**: Fourier nos anos 1820, estudando desigualdades em mecânica, probabilidade
e estatística; os métodos **algébrico e geométrico** para achar a região das soluções; a ampliação
por T. Motzkin; e o fato de que cada eliminação de variável acrescenta desigualdades cujo número
**cresce exponencialmente**.
[PDF](https://arxiv.org/abs/2305.03730)

⏳ **FOURIER, Joseph.** *Solution d'une question particulière du calcul des inégalités*, 1826. —
Título e ano localizados em busca; **a obra não foi aberta**. O que o handbook afirma sobre o
conteúdo vem do levantamento acima.

⏳ **Data de 1936 para a redescoberta por Motzkin.** — Localizada em busca, não confirmada em fonte
primária.

### Complexidade do Simplex (fundamentos científicos do capítulo 09)

✓ **SPIELMAN, D. A.; TENG, S.-H.** "Smoothed Analysis of Algorithms: Why the Simplex Algorithm
Usually Takes Polynomial Time". *Journal of the ACM*, v. 51, p. 385–463, 2004.
DOI [10.1145/990308.990310](https://doi.org/10.1145/990308.990310) ·
[versão aberta](https://arxiv.org/abs/cs/0111050). — **Aberta e lida.** Reconcilia o pior caso
exponencial com o desempenho prático: sob pequenas perturbações aleatórias da entrada, o Simplex
tem complexidade polinomial. A leitura que o capítulo extrai: **o pior caso é frágil**.

✓ᵐ **BORGWARDT, K. H.** "The average number of pivot steps required by the Simplex-Method is
polynomial". *Zeitschrift für Operations Research*, v. 26, p. 157–177, 1982.
DOI [10.1007/bf01917108](https://doi.org/10.1007/bf01917108). — Metadados conferidos, conteúdo
não lido. Resultado de caso médio, sob modelo probabilístico de instâncias.

⏳ **KLEE, V.; MINTY, G. J.** "How good is the simplex algorithm?", em *Inequalities III*, 1972.
— Citação corrente, **não confirmada em fonte primária**. O handbook **não depende** dela: o cubo
é construído e os pivôs contados em `po-zero/etapa-03-simplex`.

### Degenerescência e ciclagem (capítulo 10)

✓ **DANTZIG, G. B.; ORDEN, A.; WOLFE, P.** "The generalized simplex method for minimizing a linear
form under linear inequality restraints". *Pacific Journal of Mathematics*, v. 5, n. 2,
p. 183–195, 1955. [PDF aberto](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p04-s.pdf) — **Aberta e
lida.** Credita a Hoffman e a Wolfe os primeiros exemplos de ciclagem; registra que "a maioria dos
problemas de fontes práticas tem sido degenerada, e nenhum jamais ciclou"; apresenta o método
lexicográfico.

✓ **HALL, J. A. J.; McKINNON, K. I. M.** "The simplest examples where the simplex method cycles and
conditions where EXPAND fails to prevent cycling". *Mathematical Programming*, v. 100, 2004.
DOI [10.1007/s10107-003-0488-1](https://doi.org/10.1007/s10107-003-0488-1) ·
[arXiv](https://arxiv.org/abs/math/0012242) — **Aberta e lida.** Exemplos de ciclagem são
construídos e raros; o problema prático é o *stalling*; o EXPAND **não tem garantia**.

✓ᵐ **BEALE, E. M. L.** "Cycling in the **dual** simplex algorithm". *Naval Research Logistics
Quarterly*, v. 2, n. 4, p. 269–275, 1955.
DOI [10.1002/nav.3800020406](https://doi.org/10.1002/nav.3800020406). — Metadados conferidos. A
instância que o ensino atribui a este artigo é **primal**, e o handbook **não afirma** que ela
apareça literalmente aqui. Ver [ADR 0008](../adr/0008-atribuicao-da-instancia-que-cicla.md).

✓ᵐ **BLAND, R. G.** "New Finite Pivoting **Rules** for the Simplex Method". *Mathematics of
Operations Research*, v. 2, n. 2, p. 103–107, 1977.
DOI [10.1287/moor.2.2.103](https://doi.org/10.1287/moor.2.2.103). — Metadados conferidos. O
enunciado exato e a prova de terminação seguem `⏳`; o handbook **mede** a terminação.

✓ᵐ **GILL, P. E.; MURRAY, W.; SAUNDERS, M. A.; WRIGHT, M. H.** "A practical anti-cycling procedure
for linearly constrained optimization". *Mathematical Programming*, v. 45, p. 437–474, 1989.
DOI [10.1007/BF01589114](https://doi.org/10.1007/BF01589114). — O procedimento EXPAND, dos solvers
reais.

⏳ **HOFFMAN, A. J.** "Cycling in the simplex algorithm". *National Bureau of Standards Report*
2974, 1953. — Referência **anterior** a Beale, creditada na fonte de 1955 acima. A data do
exemplo (1951 ou 1953) diverge entre levantamentos e **não foi resolvida**.

### Formulação (fundamentos científicos do capítulo 07)

✓ᵐ **BIXBY, R. E.** "Solving Real-World Linear Programs: A Decade and More of Progress".
*Operations Research*, v. 50, n. 1, p. 3–15, 2002.
DOI [10.1287/opre.50.1.3.17780](https://doi.org/10.1287/opre.50.1.3.17780). — Metadados
conferidos; **conteúdo inacessível** (a editora recusa acesso automatizado). Fica como ponteiro:
**nenhuma afirmação do handbook se apoia nele**.

> **Lacuna declarada.** A literatura específica sobre **qualidade de formulação** — como se
> avalia se um modelo está bem escrito, e não se o solver está rápido — não foi levantada por
> varredura sistemática. A impressão de quem montou esta bibliografia é que ela é fina comparada
> à de algoritmos, e essa impressão **não é resultado verificado**. Está na fila do
> [Radar](../radar/RADAR.md).

### Complementar

✓ **GARILLE, Susan Garner; GASS, Saul I.** "Stigler's Diet Problem Revisited". *Operations
Research*, v. 49, n. 1, p. 1–13, 2001.
DOI [10.1287/opre.49.1.1.11187](https://doi.org/10.1287/opre.49.1.1.11187). — Metadados
conferidos; texto **não lido** (editora responde `403`). Reexame do problema com solvers modernos;
entra na fila do [Radar](../radar/RADAR.md).

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
