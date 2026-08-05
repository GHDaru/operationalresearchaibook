# Spec 007 — Módulo 0: a espinha da TOC

> **Raia:** plena · **Rodada:** 9 · **Branch:** `010-modulo-0`
> **Decisor:** Gilsiley Darú · **Decisão:** caminho A do bloco 4 da auditoria

## Diagnóstico (o que motivou)

Num livro chamado *Teoria das Restrições*, medido no código:

| Conceito | Ocorrências antes desta rodada |
|---|---|
| "restrição" (o conceito, definido) | **0** — a palavra aparecia 2× de passagem |
| Cinco passos de focalização | **0** |
| Ótimo local × ganho global | **0** |
| Ganho / Inventário / Despesa Operacional | **0** |
| Tambor-Pulmão-Corda | **0** |

O livro era um treinamento nos **Processos de Raciocínio** — um ramo da TOC — sem a teoria
que lhes dá propósito. A capa traz uma corrente com o elo restritivo em âmbar, e o livro
nunca explicava esse elo.

O autor, no papel de auditor, formulou assim: *"para TOC, senti que está fraco; este está
excelente para o processo de raciocínio — não o perca"*.

## Decisão

**Caminho A — adicionar a espinha, sem perder nada.** O conteúdo existente é preservado
integralmente e **reposicionado**: ele deixa de ser "o livro" e passa a ser a resposta às
três perguntas que o Módulo 0 formula.

## A nova estrutura

| Módulo | Capítulos | Papel |
|---|---|---|
| Abertura | 00 | Introdução |
| **0 — A restrição** | 01–04 | **novo**: o sistema, o ótimo local, os cinco passos, as três perguntas |
| 1 — Fundamentos lógicos | 05–09 | a gramática comum (era 01–05) |
| 2 — O que mudar | 10–11 | Nuvem e conflitos recorrentes (era 06–07) |
| 3 — Para o que mudar | 12 | Injeções (era 08) |
| 4 — Como causar a mudança | 13–14 | APR e aplicação integrada (era 09–10) |

O reposicionamento é o coração da decisão: **os módulos 2, 3 e 4 são, um a um, as respostas
às três perguntas do Módulo 0.** As ferramentas passam a ter endereço.

## Escopo

1. Quatro capítulos novos (01–04), autorais, com fonte citada.
2. Bateria de exercícios para cada um (mesma arquitetura das existentes).
3. **Renumeração** de todo o livro, com remapeamento de: arquivos, títulos, referências
   cruzadas na prosa, glossário, bibliografia, ids e séries dos exercícios, marcadores de
   bateria, gating do tutor e espelho de capacidades.
4. Introdução reescrita para anunciar a estrutura e as três perguntas.
5. Três capacidades novas no tutor: `restricao` (cap. 01), `cinco_passos` (03),
   `tres_perguntas` (04).

## Fora de escopo (registrado)

Módulo de **operações** — Tambor-Pulmão-Corda, gestão de pulmões, contabilidade de ganhos
(Ganho/Inventário/Despesa Operacional). É a expertise do autor e fecha a TOC como corpo,
mas é outra rodada: o Módulo 0 já torna o livro coerente com o próprio nome.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| CA-1 | O livro define restrição | `grep -c` do conceito nos capítulos 01–04 > 0 |
| CA-2 | Os cinco passos existem, um a um | os cinco nomeados no cap. 03 |
| CA-3 | As três perguntas mapeiam para os módulos | tabela pergunta→ferramenta→módulo no cap. 04 |
| CA-4 | Nenhuma referência cruzada quebrou | build valida links internos; inspeção das 40 refs remapeadas |
| CA-5 | Os exercícios seguiram os capítulos | ids `capNN` alinhados ao novo número; 34 + novos |
| CA-6 | O gating acompanha | espelho em sincronia com `capabilities.py` (portão) |
| CA-7 | Nada regride | build, portão por página e testes verdes |

## Fechamento

Executado em 2026-08-01, branch `010-modulo-0`. A evidência de cada portão, com as saídas
capturadas e os casos quebrados de propósito, está em [`verificacao.md`](verificacao.md).
A decisão e as alternativas avaliadas estão no [ADR 0004](../../adr/0004-modulo-0-espinha-da-toc.md).

**A rodada não passou de primeira.** A revisão em contexto fresco encontrou quatro
referências de capítulo quebradas em conteúdo publicado — introdução, bibliografia e a
rubrica do exercício final — que os portões da época não viam, porque o critério CA-4 se
apoiava na validação de **links** para cobrir referências em **prosa**. Corrigidas, e o
modo de falha virou portão (`publicar/verifica-referencias.mjs`). A revisão também provou
um falso-negativo na varredura de vazamento de rubrica, corrigido e recalibrado com
medição.

**Fica em aberto (declarado):** o par em inglês (Princípio II), os capítulos 00 e 05 sem
bateria — agora declarados em código, em `SEM_BATERIA_DECLARADO` —, a coerência da espinha
de cenários entre o Módulo 0 e a Gráfica Belmonte dos capítulos 10–13, e o módulo de
operações registrado como fora de escopo.
