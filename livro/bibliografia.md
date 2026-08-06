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

> **⏳ Aguardando anexo.** Os dois livros ainda não foram registrados. Quando forem, esta
> seção recebe: autor, título, edição, editora, ano, ISBN e o **mapa de correspondência**
> entre as vagas do handbook e as unidades de cada obra.
>
> **O que entra no repositório:** apenas metadados bibliográficos e a tabela de
> correspondência. **O que não entra:** o texto, as figuras, os exercícios ou o arquivo das
> obras — em nenhuma hipótese (constituição, Princípio X; ver
> [`materiais/README.md`](../materiais/README.md)).

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
