# Estudo 003 — O comitê da v0

**Data:** 2026-08-12 · Três pareceres independentes sobre a mesma pergunta, com lentes
diferentes. Este documento é **síntese**, não transcrição — e o que eu **verifiquei por medição**
está marcado, porque parecer de agente não é fonte.

## A pergunta

O autor mandou construir a v0 do livro completo — 72 capítulos restantes, 3 exercícios cada,
prova ao final, em *long run*, um ciclo por capítulo, sem parar. Justificativa: *"como é um livro,
tudo é reversível e de baixo impacto"*.

## Onde os três convergiram, sem combinar

1. **A unidade da rodada tem de ser a Parte, não o capítulo.** Os três chegaram lá por caminhos
   diferentes: o arquiteto pela aritmética de esforço, a didática pelo fio pedagógico da Parte, o
   guardião pela reviewabilidade do gate.
2. **Selo de maturidade por capítulo, visível e verificado por máquina.** A didática pôs como
   condição de parecer favorável.
3. **A prova sai do *long run*.** É o único artefato genuinamente irreversível.
4. **A premissa "tudo é reversível" é verdadeira sobre arquivo e falsa sobre leitura.**
5. **Faltam portões para princípios não-negociáveis.**

Divergência real: **nenhuma** nos pontos estruturais. Isso é incomum e merece desconfiança — mas
os três citaram evidência diferente para a mesma conclusão, o que é o padrão de convergência
legítima, não de eco.

## O que eu verifiquei antes de aceitar

| Afirmação do comitê | Verificação | Resultado |
|---|---|---|
| `verifica-capitulos.mjs` não exige "quando não serve" | `grep -c` | **0 ocorrências — confirmado** |
| Não exige vídeo | `grep -c` | **0 ocorrências — confirmado** |
| `verifica-exercicios.mjs` não exige piso de 3 | leitura do código | **confirmado** |
| Os 4 capítulos publicados têm os três | varredura | **confirmado — por disciplina** |
| A constituição promete anonimato | `grep -in` por 4 termos | **FALSO. Zero ocorrências.** Eu havia afirmado o contrário ao autor e no `DEPLOY.md` |
| Quem promete anonimato | `grep -rn` | `store.py`, README do backend e **`tema/uso.js`, que o leitor vê** |
| Capítulo 09 = 722 linhas, 10 = 478 | `wc -l` | **confirmado** |
| 27 exercícios em 4 baterias: 4, 10, 8, 5 | contagem | **confirmado** |

## Achados que viraram tarefa imediata

- **Dois princípios não-negociáveis sem portão** — corrigido no mesmo dia, com os três provados
  quebrando-os de propósito.
- **`BANCO-DE-EXERCICIOS.md` linha 114** diz "os cinco que importam" e lista **seis**.
- **Duas taxonomias divergentes de tipo de exercício** — o `BANCO` e o Guia Editorial §4.1 usam
  nomes diferentes para o mesmo campo obrigatório, e o Guia omite `resolver`. Com 4 baterias é
  ruído; com 76, o campo `tipo` vira lixo.
- **Dois tipos declarados nunca usados:** `interpretar` e `escolher`, zero em 27 exercícios. São
  justamente dois dos mais indicados para prova com nota.
- **Glossário e o mapa `SIGLAS` do `build.mjs` são duas fontes de verdade sem portão de espelho**
  — e o `verifica-espelho.mjs` já faz exatamente isso para outro par.

## O alarme que eu não teria pensado sozinho

Da didática, e é contraintuitivo o bastante para ficar registrado:

> A tabela de procedência do capítulo 09 tem 4 afirmações `✓`, 1 `⏳`, 1 `❌` e 1 `📖`. **Essa
> proporção é sinal de saúde.** Um lote de 10 capítulos que saia com 100% `✓` e nenhuma dívida
> marcada **não** é sinal de boa pesquisa — num *long run*, é sinal de fabricação.

Virou regra em [ADR 0013](../adr/0013-o-que-e-a-v0.md), D4.
