# 21 — Transporte, designação e transbordo

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Formular** os três clássicos como casos do modelo de fluxo, e dizer o que muda entre eles.

**O2.** **Justificar** por que a designação — que é combinatória por enunciado — não precisa de
variável binária.

**O3.** **Diagnosticar** um enunciado que parece designação e não é, e dizer o que ele exige.

## O problema

A designação é o caso mais bonito desta Parte porque ele **parece** exigir programação inteira e
não exige:

> *"Cada pessoa faz exatamente uma tarefa, cada tarefa recebe exatamente uma pessoa."* Isso é
> combinatório em cada palavra. E mesmo assim, resolvido como Programação Linear contínua, com as
> variáveis livres entre 0 e 1, **a resposta sai 0/1**. Medido nesta página: custo **9**, três
> atribuições, todas binárias, sem uma única variável declarada como `Binary`.

O erro caro deste capítulo é o gesto que parece cuidado e é desperdício:

> Alguém declara `cat="Binary"` porque *"pessoa não se divide"*, e paga o custo de resolução da
> programação inteira num problema em que a estrutura já garantia a resposta. Em instâncias
> pequenas ninguém percebe; em instâncias grandes o método muda de patamar, porque passa a haver
> *branch-and-bound* onde não precisava haver — **este handbook não cronometrou essa diferença**, e
> por isso não publica número. O que ele afirma é o outro custo, que independe de tempo: **a
> análise de sensibilidade some junto**, porque modelo inteiro não tem preço-sombra.

## De onde isto veio

### O aperto: os mesmos três problemas, em três apostilas

Transporte, designação e transbordo chegaram ao ensino como três assuntos, cada um com o seu
método tabular — o do canto noroeste, o húngaro, o de aproximação de Vogel, **nomes correntes cuja
história este handbook não abriu em fonte primária** (⏳). Aprendia-se a preencher três tabelas
diferentes, e a semelhança entre elas ficava por conta do aluno.

### A virada: perceber que os três eram um

A virada é a do [capítulo 20](20-fluxo-custo-minimo.md): a mesma conservação de fluxo descreve os
três. **Designação é transporte com todas as ofertas e demandas iguais a 1**; **transbordo é
transporte com nós que não produzem nem consomem**. Escrito assim, o repertório de três métodos
vira um modelo com três instanciações.

Os métodos especializados não ficaram obsoletos — eles ficaram **opcionais**, e a escolha passou a
ser de desempenho.

### A ideia reaproveitável

> **Um caso particular bem escolhido não é um problema menor: é o mesmo problema com dados que
> revelam a estrutura.** Colocar 1 em toda oferta e toda demanda é o que transforma transporte em
> designação — e é por isso que a integralidade sobrevive à mudança.

### A origem do nome

**"Designação"** traduz *assignment*, e o método tabular clássico é chamado **húngaro** por causa
da origem atribuída aos resultados que o fundamentam. **A atribuição é corrente e não foi
confirmada em fonte primária** nesta rodada.

### Procedência

| Afirmação | Estado |
|---|---|
| A origem húngara atribuída ao método clássico de designação | ⏳ **atribuição corrente**, não confirmada em fonte primária |
| Os nomes dos métodos tabulares (canto noroeste, Vogel) e a sua história | ⏳ **atribuições correntes**; este handbook **não abriu** as fontes |
| Que a designação desta página custe 9 e saia 0/1 sem variável binária | ✓ **medido** em `po-zero/parte-III-redes`, com teste que compara este texto à medição |
| A integralidade vir da unimodularidade total | 📖 **leitura editorial**, herdada do [capítulo 20](20-fluxo-custo-minimo.md) |

## Os três, lado a lado

| | Transporte | Designação | Transbordo |
|---|---|---|---|
| Nós | Ofertas e demandas | Pessoas e tarefas | Ofertas, demandas **e passagem** |
| Oferta de cada nó | Qualquer | Sempre **1** | Qualquer; nos de passagem, **0** |
| O que a variável significa | Quanto mandar | **Se** designar | Quanto mandar |
| Precisa de binária? | Não | **Não** — e é o que surpreende | Não |

## A designação, medida

Três pessoas, três tarefas, custos em horas:

| | `relatorio` | `auditoria` | `treinamento` |
|---|---|---|---|
| `ana` | 9 | **2** | 7 |
| `bruno` | **6** | 4 | 3 |
| `clara` | 5 | 8 | **1** |

O modelo declara `lowBound=0, upBound=1` — **contínuo**. A saída:

| Designação | Valor |
|---|---|
| `ana → auditoria` | 1 |
| `bruno → relatorio` | 1 |
| `clara → treinamento` | 1 |
| **Custo total** | **9** |

**Todos os valores saem 0 ou 1**, e nenhuma variável foi declarada binária.

> **Uma condição, e ela não é detalhe.** O que a estrutura garante é que **existe vértice ótimo
> 0/1**. Quem entrega esse vértice é o Simplex, que para em vértice. Se o solver for de pontos
> interiores com *crossover* desligado **e** houver empate no ótimo — duas pessoas igualmente boas
> nas mesmas tarefas, que é o caso mais comum de todos em escala real —, a saída pode vir
> fracionária, e **ótima**. O [capítulo 20](20-fluxo-custo-minimo.md) mede isso: numa designação
> 3×3 de custos todos iguais, a resposta sai **1/3 em toda variável**. O conselho deste capítulo —
> *não declare `Binary`* — vale com o *crossover* ligado, que é o padrão. **Desligou o *crossover*,
> confira a saída.**

> **Repare no que a solução ótima faz, porque é contraintuitivo.** `clara` é a mais rápida em
> `treinamento` (1 hora) **e** seria melhor que `bruno` em `relatorio` (5 contra 6). O ótimo dá
> `relatorio` ao `bruno` mesmo assim, porque tirar `clara` do `treinamento` custaria mais do que
> economiza. **Designação é sobre o conjunto, não sobre cada par** — e é o erro mais comum de quem
> monta escala à mão.

## Quando não serve

**1. Quando as capacidades não são 1 de verdade.** *"Cada pessoa faz até três tarefas"* ainda é
fluxo e continua inteiro. Mas *"cada pessoa faz três tarefas **da mesma área**"* já não é: a
restrição de área é transversal, e vale o que o [capítulo 20](20-fluxo-custo-minimo.md) mediu.

**2. Quando há custo de troca ou sequência.** Se o custo de `ana` fazer a auditoria depender do
que ela fez antes, o modelo não é de designação — é de sequenciamento, e é combinatório de
verdade.

**3. Quando o número de pessoas e tarefas não bate.** Não é impedimento: acrescentam-se pessoas ou
tarefas fictícias com custo zero, e o modelo continua de rede. **Mas alguém tem de declarar o que
a folga significa** — uma tarefa fictícia designada é uma tarefa que ninguém vai fazer.

**4. Quando a preferência importa mais que o custo.** Designação minimiza um total. Se o problema
é de satisfação — que ninguém fique com a pior opção —, o objetivo é outro, e somar preferências
esconde a insatisfação individual dentro de uma média boa.

## Fundamentos científicos

**KUHN (1955)** é a fonte do método húngaro ([bibliografia](../bibliografia.md)), e **KUHN
(2004)** é a reimpressão com prefácio retrospectivo do próprio autor — pelos registros, é ali que
ele explica por que chamou o método de húngaro. **Seria a fonte que fecha o `⏳` desta página**, e
ela continua `⏳`: o identificador está conferido, o texto não foi aberto, e este handbook não
transforma metadado em história. **FRANK (2004)** traz o lado húngaro da mesma questão.

**MUNKRES (1957)** é a fonte que trata designação e transporte no mesmo trabalho, que é
exatamente a unificação que esta página defende — com a diferença de que aqui a unificação é feita
pelo modelo de fluxo, e não pelo método tabular.

**O que continua sem fonte.** Os nomes dos métodos tabulares de partida — canto noroeste,
aproximação de Vogel — **não** foram localizados em registro primário nesta rodada. O `⏳` da
tabela de Procedência é honesto e permanece.

## Fundamentos e fontes

**O que está medido aqui.** O custo 9, as três designações, e o fato de que todos os valores saem
0/1 num modelo declarado contínuo. Em `po-zero/parte-III-redes/redes.py`, com teste que compara
**este texto** à medição — inclusive a asserção de que nenhuma variável foi declarada binária.

**O que continua em dívida:** as atribuições históricas dos métodos tabulares, todas `⏳`.

> 🔵 **Este capítulo está em "medido".** O que falta para ✅ é revisão independente em contexto
> fresco.

## Pratique

<div data-bateria="cap21"></div>

Três exercícios. O primeiro escreve os três clássicos como um modelo só; o segundo é o do capítulo
— justificar a ausência da binária, e prever quando ela volta a ser necessária; o terceiro
diagnostica um enunciado que parece designação e não é.

## Assista

**[Problemas de transporte e designação - Teoria](https://www.youtube.com/watch?v=Y2FFUzsfXXQ)** ·
[PET Engenharias](https://www.youtube.com/@PETEngenhariasUFAL) · 13min06s

**O que ele resolve:** este capítulo apresenta os três clássicos **já unificados** pelo modelo de
fluxo, que é a leitura que o capítulo 20 autoriza — e por isso ele não mostra os métodos tabulares.
O vídeo faz a apresentação tradicional, com transporte e designação lado a lado e a notação
clássica. Vale ver as duas leituras: a tradicional é a que o leitor vai encontrar na maior parte
dos cursos.

## Síntese — o que levar

- **Designação é transporte com todas as ofertas e demandas iguais a 1.** Transbordo é transporte
  com nós de passagem.
- **A designação não precisa de variável binária.** Medido: custo 9, saída 0/1, com o modelo
  declarado contínuo.
- **Declarar `Binary` aqui é desperdício** — e custa a análise de sensibilidade junto.
- **Designação é sobre o conjunto, não sobre cada par:** a pessoa mais rápida numa tarefa pode não
  ficar com ela.
- **Pessoas e tarefas em números diferentes não é impedimento** — mas a folga precisa de
  interpretação declarada.
- **Restrição transversal (área, sequência, troca) tira o problema da família** e devolve a
  integralidade ao preço cheio.
- **Fora da Pesquisa Operacional:** um caso particular bem escolhido é o mesmo problema com dados
  que revelam a estrutura.

## Verificação

1. Escreva o modelo de designação desta página como um problema de transporte, dizendo o que é
   oferta e o que é demanda. *(O1)*
2. Um colega vai declarar as variáveis como binárias "porque pessoa não se divide". O que você
   argumenta, e o que ele perde se insistir? *(O2)*
3. Uma empresa quer designar 6 consultores a 6 clientes, **e** garantir que nenhum consultor pegue
   dois clientes do mesmo setor. Ainda é designação? O que muda? *(O3)*

### Leitura executiva

Transporte, designação e transbordo chegaram ao ensino como três assuntos com três métodos
tabulares distintos, e são **um** modelo só: a conservação de fluxo do capítulo 20 descreve os três.
**Designação é transporte com todas as ofertas e demandas iguais a 1**, e transbordo é transporte
com nós que não produzem nem consomem — o que transforma um repertório de três métodos numa
formulação com três instanciações, e torna os métodos especializados opcionais em vez de
obrigatórios. O resultado que este capítulo mede é o que mais surpreende: a designação é
combinatória em cada palavra do enunciado — *cada pessoa faz exatamente uma tarefa* — e mesmo assim
não precisa de variável binária. Resolvida como Programação Linear contínua, com as variáveis
livres entre 0 e 1, a resposta **sai 0/1**: custo **9** e três atribuições, sem uma única variável
declarada como binária. Declarar `Binary` por precaução é o erro caro do capítulo, e ele parece
cuidado: paga-se o custo de resolução da programação inteira num problema em que a estrutura já
garantia a resposta, e **perde-se a análise de sensibilidade junto**, porque modelo inteiro não tem
preço-sombra. Vale olhar o que a solução ótima faz, porque contraria a intuição de quem monta
escala à mão: a pessoa mais rápida numa tarefa **pode não ficar com ela**, porque designação é
sobre o conjunto e não sobre cada par isoladamente. A família se preserva quando as capacidades
mudam de 1 para outro número, e se perde assim que entra uma restrição transversal — dois clientes
do mesmo setor, custo de troca entre tarefas, dependência de sequência —, caso em que a
integralidade volta a custar o preço cheio, exatamente pelo mecanismo que o capítulo 20 mediu.
