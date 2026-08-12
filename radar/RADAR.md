# Radar científico

> **Conteúdo revisado em 2026-08** · o mecanismo pelo qual a literatura entra no handbook.

Um handbook que promete se atualizar com a literatura precisa de um **mecanismo**, não de boa
vontade. Este é o mecanismo (constituição, Princípio VI).

## Como funciona

1. **Ler e fichar.** Todo artigo lido vira uma linha aqui, datada, com o veredito e — o campo
   que importa — **o que ele muda no livro**.
2. **Disparar.** Linha cujo veredito é `muda recomendação` **dispara revisão** do capítulo
   afetado, sem esperar a janela trimestral.
3. **Citar.** Só depois da linha no Radar a referência entra na
   [bibliografia](../livro/bibliografia.md). Referência citada sem passar por aqui é dívida a
   corrigir, não atalho.

O Radar é *append-only*: linha publicada não se reescreve. Um artigo reavaliado ganha linha
nova que referencia a antiga.

## Vereditos

| Veredito | Significa | Consequência |
|---|---|---|
| `confirma` | Sustenta o que o livro já diz | Vira citação de apoio |
| `muda recomendação` | Contradiz ou refina algo publicado | **Dispara revisão** do capítulo |
| `abre vaga` | Tema relevante que o mapa ainda não cobre | Vira item no [roadmap](../ROADMAP.md) |
| `observar` | Promissor, evidência ainda fraca | Fica em observação; não sustenta afirmação |
| `descartado` | Não se sustenta, ou não se aplica ao escopo | Registrado para não ser relido à toa |

## Cadência

**Quinzenal** para a varredura corrente; **trimestral** para a janela de revisão, em que os
vereditos `observar` são reavaliados e os vídeos e experimentos são reconferidos.

Prioridade de varredura, nesta ordem: (1) artigos que tocam capítulos já publicados;
(2) *surveys* das partes em produção na rodada corrente; (3) fronteira.

## Registro

| Data | Registro | Fonte | Tipo | Veredito | O que muda no livro | Onde |
|---|---|---|---|---|---|---|
| 2026-08-06 | Abertura do Radar (inicial) | — | — | — | Nada ainda: o handbook está na rodada de fundação | — |
| 2026-08-09 | Complexidade suavizada do Simplex | SPIELMAN & TENG, *J. ACM* 51:385–463, 2004 · [DOI](https://doi.org/10.1145/990308.990310) · ✓ **lido** | teoria | `confirma` | Reconcilia o pior caso exponencial com o desempenho prático: o pior caso é **frágil**, não sobrevive a perturbação. Sustenta a seção de fundamentos do cap. 09 | [cap. 09](../livro/capitulos/09-simplex.md) |
| 2026-08-09 | Caso médio: pivôs polinomiais | BORGWARDT, *Z. Oper. Res.* 26:157–177, 1982 · [DOI](https://doi.org/10.1007/bf01917108) · ✓ᵐ | teoria | `observar` | Resultado sob modelo probabilístico de instâncias; **conteúdo não lido**. Não sustenta afirmação além da existência do resultado | [cap. 09](../livro/capitulos/09-simplex.md) |
| 2026-08-09 | Origem da ciclagem e método lexicográfico | DANTZIG, ORDEN & WOLFE, *Pacific J. Math.* 5(2):183–195, 1955 · [PDF](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p04-s.pdf) · ✓ **lido** | histórico | `muda recomendação` | Credita a **Hoffman e Wolfe** os primeiros exemplos de ciclagem — não a Beale, como a maioria do material didático afirma. **Disparou** a atribuição em três camadas do cap. 10 | [cap. 10](../livro/capitulos/10-casos-especiais.md) · [ADR 0008](../adr/0008-atribuicao-da-instancia-que-cicla.md) |
| 2026-08-09 | Ciclagem é rara; o problema é o *stalling* | HALL & McKINNON, *Math. Prog.* 100, 2004 · [DOI](https://doi.org/10.1007/s10107-003-0488-1) · [arXiv](https://arxiv.org/abs/math/0012242) · ✓ **lido** | teoria+prática | `muda recomendação` | O problema prático não é o ciclo, é a **estagnação finita**; e o EXPAND, dos solvers reais, **não tem garantia**. Impediu o cap. 10 de terminar com final feliz falso | [cap. 10](../livro/capitulos/10-casos-especiais.md) |
| 2026-08-09 | Regras finitas de pivoteamento | BLAND, *Math. Oper. Res.* 2(2):103–107, 1977 · [DOI](https://doi.org/10.1287/moor.2.2.103) · ✓ᵐ | teoria | `observar` | Metadados conferidos; **enunciado exato e prova não lidos**. O handbook **mede** a terminação em vez de citá-la | [cap. 10](../livro/capitulos/10-casos-especiais.md) |
| 2026-08-09 | Instância clássica de ciclagem | BEALE, *Naval Res. Log. Q.* 2(4):269–275, 1955 · [DOI](https://doi.org/10.1002/nav.3800020406) · ✓ᵐ | histórico | `observar` | Título fala em simplex **dual**; a instância que circula é **primal**. A atribuição literal segue `⏳` | [ADR 0008](../adr/0008-atribuicao-da-instancia-que-cicla.md) |
| 2026-08-09 | Procedimento anticiclagem dos solvers | GILL, MURRAY, SAUNDERS & WRIGHT, *Math. Prog.* 45:437–474, 1989 · [DOI](https://doi.org/10.1007/BF01589114) · ✓ᵐ | prática | `observar` | O EXPAND é o que os solvers usam; a falta de garantia vem da leitura de Hall & McKinnon, não deste artigo | [cap. 10](../livro/capitulos/10-casos-especiais.md) |

> **Nota da rodada 006.** As sete linhas de 2026-08-09 entraram **depois** de as fontes já
> constarem da bibliografia — o que inverte a ordem que esta página declara ("só depois da linha
> no Radar a referência entra na bibliografia"). Foi apontado pela revisão independente e está
> registrado aqui em vez de corrigido em silêncio: a dívida existiu, durou uma rodada, e o
> registro é o que impede que ela vire hábito.
>
> O registro começou vazio por honestidade. A varredura sistemática abriu junto com a primeira
> rodada de conteúdo, e a fila inicial já está identificada no
> [estudo do corpo de conhecimento](../estudos/001-corpo-de-conhecimento-po.md): revisões de
> *Adaptive Large Neighborhood Search* (ALNS), *matheuristics* e hiper-heurísticas para a Parte
> V, e a literatura de aprendizado de máquina em *branch-and-bound* para a Parte XI.
