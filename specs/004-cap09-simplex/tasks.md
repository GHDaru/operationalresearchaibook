# Tasks 004 — Capítulo 09: O método Simplex

> Escritas junto com o [plano](plan.md), **depois** da implementação. Servem de registro do que
> foi feito e de referência para as rodadas seguintes — não de plano de execução, que é o que
> deveriam ter sido.

## T1 — O experimento, antes do texto

| # | Tarefa | Estado |
|---|---|---|
| T1.1 | `quadro.py`: forma padrão, custos reduzidos, teste da razão, pivoteamento, com `Fraction` | ✅ |
| T1.2 | `CustoM`: *big-M* simbólico, comparação lexicográfica | ✅ |
| T1.3 | Detecção de status: ótimo, ilimitado, inviável (artificial na base com valor positivo) | ✅ |
| T1.4 | `experimento.py`: três casos, conferidos contra o HiGHS **por veredito**, não só por ponto | ✅ |
| T1.5 | Combinatória `C(n+m, m)` contada para cinco tamanhos | ✅ |
| T1.6 | Cubo de Klee–Minty construído, pivôs contados para $n = 2..7$ | ✅ |
| T1.7 | Ganho por unidade extra medido por reexecução, conferido contra a linha $z$ | ✅ |
| T1.8 | Dupla execução produz `resultados.json` byte a byte idêntico | ✅ |
| T1.9 | `README.md` da etapa | ✅ |

## T2 — O portão em dívida desde a edição 0.6

| # | Tarefa | Estado |
|---|---|---|
| T2.1 | `verifica-otimos.mjs`: racionais exatos sobre `BigInt`, sem ponto flutuante | ✅ |
| T2.2 | Enumeração de vértices com a não-negatividade como restrição de verdade | ✅ |
| T2.3 | Detecção de região ilimitada na direção de melhora (cone de recessão) | ✅ |
| T2.4 | Detecção de múltiplos ótimos; `segmento` como forma declarável | ✅ |
| T2.5 | Metade de cobertura: rubrica que afirma ótimo **exige** campo `modelo` | ✅ |
| T2.6 | Campo `modelo` anexado aos 11 exercícios anteriores que afirmam ótimo | ✅ |
| T2.7 | Portão ligado ao `npm run build` | ✅ |
| T2.8 | **Provado quebrando**, em três cenários distintos | ✅ |

## T3 — O capítulo

| # | Tarefa | Estado |
|---|---|---|
| T3.1 | Objetivos O1–O5, numerados | ✅ |
| T3.2 | "O problema": a combinatória que mata a enumeração | ✅ |
| T3.3 | "A intuição": andar pelas arestas; **convexidade** e por que parar é seguro | ✅ |
| T3.4 | "A matemática": forma padrão, base, e a ponte **vértice = solução básica viável** | ✅ |
| T3.5 | "O algoritmo": três quadros da montadora, todos gerados por execução | ✅ |
| T3.6 | A resposta à dívida do capítulo 07: por que a ganância não engana aqui | ✅ |
| T3.7 | *Big-M*: quadro de partida e quadro final; a leitura de negócio do compromisso | ✅ |
| T3.8 | O veredito de inviabilidade: artificial que não sai | ✅ |
| T3.9 | "Quando não serve": cinco itens, com destino declarado para cada | ✅ |
| T3.10 | Síntese, leitura executiva e três perguntas de verificação | ✅ |

## T4 — Exercícios

| # | Tarefa | Estado |
|---|---|---|
| T4.1 | 8 exercícios `cap09` A–H, cobrindo O1 a O5 | ✅ |
| T4.2 | Todo quadro publicado em enunciado sai de execução | ✅ |
| T4.3 | Três exercícios em que a conta está certa e a conclusão errada | ✅ |
| T4.4 | Todos os modelos passam pelo `verifica-otimos.mjs` | ✅ |

## T5 — Motor e registro

| # | Tarefa | Estado |
|---|---|---|
| T5.1 | Capacidade `simplex` em `capabilities.py` e no espelho `COMPANION_CAPS` | ✅ |
| T5.2 | `verifica-referencias.mjs` passa a medir o mapa; informa referências a vaga | ✅ |
| T5.3 | Sumário, mapa (09 ✅, 10 🚧), videoteca, glossário (12 verbetes) | ✅ |
| T5.4 | `HISTORICO.md` edição 0.7, com dívidas e o incidente do endereço inventado | ✅ |
| T5.5 | `build_corpus.py` reempacotado | ✅ |

## O que fica para a próxima rodada

| # | Item | Onde |
|---|---|---|
| P1 | **Portão de URL externa.** A defesa contra endereço inventado é hoje a disciplina de quem escreve. Um portão que ao menos exija que toda URL de vídeo esteja na Videoteca com estado declarado fecharia parte do buraco | ROADMAP |
| P2 | **A ilha interativa do capítulo 08 continua sem verificação em navegador.** Segue como o único artefato do livro nesse estado | ROADMAP |
| P3 | **O gate de plano não pode ser pulado de novo.** Duas vezes em quatro rodadas | Este documento |
