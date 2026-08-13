# Spec 010 — Parte I: Fundamentos, escritos por último de propósito

**Data:** 2026-08-13 · **Raia:** plena · **Unidade:** a **Parte** ([ADR 0013](../../adr/0013-o-que-e-a-v0.md), D1)
· **Estado:** aguardando ratificação do autor

## O lote

Seis capítulos, na ordem declarada em D8 — Parte I vem **depois** da Parte II.

| Vaga | Capítulo | Estado-alvo |
|---|---|---|
| 01 | O que é Pesquisa Operacional | 🟡 v0 |
| 02 | O ciclo de modelagem | 🟡 v0 |
| 03 | Anatomia de um modelo de otimização | 🟡 v0 |
| 04 | Classificação de problemas e escolha de método | 🟡 v0 |
| 05 | Complexidade computacional para quem modela | 🟡 v0 |
| 06 | Ferramentas de trabalho | 🟡 v0 |

## Por que a Parte I vem depois — e por que isso muda o que ela é

A decisão já está publicada no sumário: *"escritas depois da Programação Linear, de propósito"*.
Agora ela tem consequência escrita.

Um capítulo "O que é Pesquisa Operacional" escrito **antes** de qualquer método é uma promessa: o
leitor tem de acreditar. Escrito **depois** de nove capítulos medidos, ele vira **balanço** — pode
apontar para o prejuízo de R$ 350 do capítulo 12, para o preço ambíguo do 13, para o padrão errado
do 15, para os 22 contra 30 do 38. **A Parte I do handbook não apresenta o campo: ela o demonstra
com o que já está medido no próprio livro.**

Isso é regra do lote, não estilo: **todo capítulo da Parte I aponta para pelo menos um número
medido da Parte II**, e nenhum deles introduz medição nova que não tenha script.

## O teto que este lote encosta, e ele é do próprio portão

A ADR 0013 D2 estabelece que **mais de 3 🟡 por ✅ obriga a próxima rodada a ser de promoção**, e o
portão de maturidade transformou isso em aritmética. Hoje: **6 🟡 e 4 ✅**, teto **12**.

Este lote leva a **12 🟡 e 4 ✅** — exatamente no teto, e o portão passa. **O lote 011 não pode ser
de capítulo novo**: ou promove, ou o build fica vermelho. É o freio funcionando por dado próprio,
e está registrado aqui para não ser descoberto como surpresa.

## Objetivos e exercícios — três e três, um para um

Por D5, e com a mesma progressão do lote 1: **A** reconhecimento · **B** `diagnosticar`
(inegociável) · **C** julgar/escolher.

| Capítulo | O1 | O2 | O3 |
|---|---|---|---|
| **01** | Dizer o que distingue PO de "usar matemática no negócio" | Diagnosticar um problema apresentado como de PO que não é | Julgar se um caso publicado sustenta o que promete |
| **02** | Situar uma tarefa no ciclo (definir → formular → resolver → validar → implantar) | Diagnosticar um projeto que pulou a validação | Decidir quando **não** modelar |
| **03** | Separar variável de decisão, parâmetro, objetivo e restrição num enunciado | Diagnosticar um modelo em que um parâmetro virou variável (ou o inverso) | Julgar um modelo com dois objetivos genuínos |
| **04** | Classificar uma instância pelas quatro perguntas (linear? inteira? incerta? convexa?) | Diagnosticar uma escolha de método feita pela fama e não pela instância | Escolher família de método para um caso descrito |
| **05** | Explicar o que P e NP decidem **na prática** de quem modela | Diagnosticar a conclusão "é NP-difícil, logo é impossível" | Decidir quando parar de buscar o ótimo |
| **06** | Montar a trilha padrão do `po-zero` e rodar um modelo | Diagnosticar uma dependência que quebra o custo zero | Julgar a escolha de uma ferramenta para um contexto |

## Critérios de aceite

| # | | Critério |
|---|---|---|
| **A1** | M | 3 objetivos e 3 exercícios por capítulo, um para um, com o B em `diagnosticar` |
| **A2** | M | **Todo capítulo aponta para ao menos um número medido da Parte II**, com link |
| **A3** | M | Nenhum capítulo introduz número novo sem script que o regenere (D3) |
| **A4** | M | Os onze portões passam, incluindo os dois de costura criados na rodada 009 |
| **A5** | M | `maturidade` declarada; o lote fecha em **12 🟡 · 4 ✅**, no teto |
| **A6** | H | Capítulo sem fonte histórica publica **"De onde isto veio — em dívida"** |
| **A7** | M | Capítulo que não for de método entra em `NAO_E_CAPITULO_DE_METODO` **com justificativa**, e não por conveniência |
| **A8** | H | **Revisão em contexto fresco do lote inteiro**, lida como leitor — e desta vez com a instrução explícita de procurar o defeito "corpo afirma o que a tabela nega", que reincidiu na 009 |
| **A9** | M | Um commit por capítulo |
| **A10** | M | O capítulo 06 **prova a trilha**: as instruções que ele publica são executadas e a saída é colada |

## O que este lote NÃO faz

- **Não escreve a prova.** Continua sendo produto separado (ADR 0013, D6).
- **Não promove ninguém a ✅.** Promoção é o lote 011, por força do teto.
- **Não toca a Parte X nem a XI.** Fora do escopo da v0 (D7).
