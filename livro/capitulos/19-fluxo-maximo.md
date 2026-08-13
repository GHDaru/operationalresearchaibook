# 19 — Fluxo máximo e corte mínimo

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Calcular** o fluxo máximo de uma rede pequena à mão, e dizer o que é um caminho
aumentante.

**O2.** **Ler o corte mínimo** como resposta de gestão: quais arestas são o gargalo, e o que muda
se você investir em cada uma.

**O3.** **Reconhecer** os problemas que não parecem fluxo e são — e os que parecem e não são.

## O problema

Este é o capítulo em que a Pesquisa Operacional (PO) entrega o resultado mais bonito do campo, e
ele é bonito por ser **útil**:

> **O quanto você consegue escoar é exatamente o quanto o seu gargalo deixa passar.** Não
> aproximadamente, não em média: **exatamente**. Medido nesta página: fluxo máximo **15**,
> capacidade do corte mínimo **15**.

A frase parece óbvia dita assim, e não é. O gargalo de uma rede **não é a aresta mais estreita** —
é um conjunto de arestas que, cortadas juntas, separam a origem do destino. Achar esse conjunto é
o que este capítulo faz, e é a diferença entre investir onde adianta e investir onde parece.

O erro caro deste capítulo:

> Uma operação identifica "o gargalo" como a etapa mais lenta que alguém consegue apontar,
> investe nela, e **a capacidade total não muda** — porque o gargalo verdadeiro era outro
> conjunto. O corte mínimo diz exatamente onde investir, e diz também quando parar: aumentar a
> capacidade de uma aresta que **não** está no corte não muda nada.

## De onde isto veio

### O aperto: quanto passa por uma malha

O problema nasce logístico — quanto material escoa de um ponto a outro por uma malha com
capacidades — e a formulação clássica é atribuída a um estudo de rede ferroviária. **A atribuição é
corrente e não foi confirmada em fonte primária** nesta rodada.

O que se fazia antes era estimar: somar as capacidades que saem da origem, ou olhar a aresta mais
estreita de um caminho. As duas estimativas erram, e erram para lados diferentes.

### A virada: procurar caminho no que ainda cabe

A ideia é achar um caminho da origem ao destino que ainda tenha folga, empurrar por ele o quanto
couber, e repetir. Chama-se **caminho aumentante**, e a virada não está nele — está na peça que
vem junto:

> **A aresta reversa.** Toda vez que se empurra fluxo por uma aresta, cria-se a possibilidade de
> **desfazer** aquela escolha depois. Sem isso o procedimento fica preso num fluxo bloqueante e
> devolve um número menor **com cara de ótimo**.

É a mesma classe de defeito do [capítulo 17](17-caminho-minimo.md): um método que para cedo e não
avisa.

### A ideia reaproveitável

> **Deixar sempre um caminho de volta é o que permite a um procedimento guloso ser exato.** Sem
> arrependimento não há garantia.

### A origem do nome

**"Corte"** é literal: uma partição dos nós em dois lados, com a origem de um e o destino do outro.
A **capacidade do corte** é a soma das capacidades que atravessam de um lado para o outro — só
nesse sentido. **"Aumentante"** traduz *augmenting*: o caminho que ainda aumenta o fluxo.

### Procedência

| Afirmação | Estado |
|---|---|
| A origem do problema num estudo de rede ferroviária, e os nomes associados ao método | ⏳ **atribuição corrente**; este handbook **não abriu** a fonte primária nesta rodada |
| O teorema de que o fluxo máximo iguala a capacidade do corte mínimo | 📖 **leitura editorial** de resultado clássico; o handbook **não reproduz a demonstração** — ele **mede** a igualdade numa instância |
| Que o fluxo máximo e o corte valham 15 na rede desta página | ✓ **medidos** em `po-zero/parte-III-redes`, em aritmética exata, com teste que compara este texto à medição |

> A segunda linha merece leitura. Este capítulo **não prova** o teorema — ele o **exibe**. Um livro
> que mede um caso e chama isso de demonstração estaria mentindo; um livro que cita o teorema e
> nunca mostra o corte estaria pedindo fé. Aqui o corte aparece, com as três arestas nomeadas, e a
> igualdade é conferida por teste.

## A rede, e os dois números

Uma distribuição pequena o bastante para conferir à mão:

```
fabrica --10--> centro_norte --6--> loja_a --6--> mercado
fabrica --8---> centro_sul   --3--> loja_b --4--> mercado
                centro_sul   --7--> loja_c --5--> mercado
                centro_norte --6--> loja_b
```

**Fluxo máximo medido: 15.**

E o corte mínimo, que sai do mesmo cálculo:

| A aresta do corte | Capacidade |
|---|---|
| `centro_norte → loja_a` | 6 |
| `loja_b → mercado` | 4 |
| `loja_c → mercado` | 5 |
| **Total** | **15** |

Os dois números batem, e é isso que o teorema promete. Repare que **as três arestas do corte não
estão no mesmo nível da rede** — uma é de saída de centro, duas são de entrada no mercado. O
gargalo de uma rede quase nunca é uma etapa; é um **conjunto**.

### O que fazer com o corte

Esta é a parte que vira decisão, e ela cabe em três linhas:

1. **Investir numa aresta do corte aumenta o fluxo** — até o corte mudar de lugar, o que acontece
   cedo.
2. **Investir numa aresta fora do corte não muda nada.** A capacidade de `fabrica → centro_norte`
   é 10 e sobra folga; dobrá-la não escoa uma unidade a mais.
3. **Depois de investir, recalcule.** O corte se move, e o próximo gargalo costuma estar em outro
   lugar — o que é a versão em rede do que a Teoria das Restrições chama de elevar a restrição e
   voltar ao passo um.

## Os problemas que não parecem fluxo

| O enunciado | A tradução |
|---|---|
| Casar candidatos com vagas, respeitando compatibilidade | Fonte → candidatos → vagas → sumidouro, todas as capacidades 1. O fluxo máximo é o **número de pares** possível |
| Escalar plantões cobrindo turnos | Mesma construção, com capacidade = quantas pessoas o turno comporta |
| Segmentar uma imagem em dois grupos | Corte mínimo, com as capacidades vindo da semelhança entre pixels vizinhos |
| Decidir quais projetos aprovar quando alguns dependem de outros | Corte mínimo num grafo de precedências |

A primeira é a mais útil de guardar: **emparelhamento máximo é fluxo máximo com capacidades 1** — e
a integralidade que o [capítulo 20](20-fluxo-custo-minimo.md) mede garante que a resposta sai em
pares inteiros, sem nenhuma variável binária.

## Quando não serve

**1. Quando o que escoa tem tipo.** Fluxo máximo trata tudo como a mesma coisa. Se há dois produtos
disputando a mesma malha, o problema é de **fluxo multiproduto**, e a integralidade de graça
**some** — o [capítulo 20](20-fluxo-custo-minimo.md) mostra o mecanismo dessa perda.

**2. Quando a capacidade depende do que já passou.** Congestionamento quebra a linearidade, do
mesmo jeito que quebrou o caminho mínimo.

**3. Quando você quer o mais barato, e não o máximo.** Fluxo máximo não conhece custo. Quando as
duas coisas importam, o modelo é o do [capítulo 20](20-fluxo-custo-minimo.md).

**4. Quando o gargalo é organizacional.** O corte mínimo aponta arestas de um modelo. Se a fila
real está numa aprovação que ninguém modelou, o modelo vai apontar para o lugar errado com toda a
precisão do mundo — e é a etapa 4 do [capítulo 02](02-ciclo-de-modelagem.md) que pega isso.

## Fundamentos científicos

**FORD e FULKERSON (1956)** e, de forma independente no mesmo ano, **ELIAS, FEINSTEIN e SHANNON
(1956)** são as fontes do teorema que esta página **exibe e não demonstra**
([bibliografia](../bibliografia.md)). A distinção é a razão de a seção existir: quando o capítulo
diz *"aqui o corte aparece, com as três arestas nomeadas"*, ele está mostrando um caso — a prova
está nestes artigos, e o handbook não a reproduz.

**SCHRIJVER (2002)** documenta a origem, e ela reenquadra o capítulo: o problema nasceu num
estudo militar sobre uma malha ferroviária, e a pergunta original era **onde cortar**, não onde
investir. O corte mínimo não é subproduto do fluxo máximo — historicamente, era o objetivo.

**EDMONDS e KARP (1972)** sustenta uma decisão que o texto acima deixa implícita: **a escolha do
caminho aumentante importa**. Não é detalhe de implementação — é o que separa um procedimento
que termina de um que pode não terminar. Este handbook **não cronometrou** nada disso e não
publica comparação.

## Fundamentos e fontes

**O que está medido aqui.** O fluxo máximo de 15, a capacidade do corte de 15, e as três arestas
que o compõem. Em `po-zero/parte-III-redes/redes.py`, aritmética exata, com teste que compara
**este texto** à medição — inclusive a igualdade entre os dois números.

**O que este capítulo não faz:** demonstrar o teorema. Ele o exibe numa instância, e diz que é isso
que está fazendo.

> 🔵 **Este capítulo está em "medido".** O que falta para ✅ é revisão independente em contexto
> fresco.

## Pratique

<div data-bateria="cap19"></div>

Quatro exercícios. O primeiro só lê o desenho, e já derruba a intuição de que a aresta mais larga é
a mais importante; o segundo calcula o fluxo à mão e encontra o corte; o terceiro é o que vira
decisão — onde investir, e onde não adianta; o quarto traduz um problema que não parece fluxo.

## Assista

**[O Método Ford-Fulkerson: Encontrando o Fluxo Máximo Passo a Passo](https://www.youtube.com/watch?v=Uu-5EOQY9Zc)** ·
[André Oliveira](https://www.youtube.com/@andrevadm) · 7min31s

**O que ele resolve:** este capítulo trata o método como meio e gasta o espaço no **corte** — que é
a parte que vira decisão. O vídeo faz o percurso mecânico que falta aqui: os caminhos aumentantes
sendo encontrados um a um, com o grafo residual sendo atualizado na tela. É especialmente útil para
ver a **aresta reversa** em ação, que é a peça difícil de entender lendo.

## Síntese — o que levar

- **O fluxo máximo é exatamente a capacidade do corte mínimo.** Medido: 15 e 15.
- **O gargalo não é uma aresta, é um conjunto** — e as arestas do corte não precisam estar no mesmo
  nível da rede.
- **A aresta reversa é o que torna o guloso exato.** Sem arrependimento não há garantia.
- **Investir numa aresta fora do corte não muda nada** — e essa é a informação de gestão que o
  método entrega de graça.
- **Depois de investir, recalcule:** o corte se move.
- **Emparelhamento máximo é fluxo máximo com capacidades 1.**
- **Fluxo máximo não conhece custo nem tipo.** Dois produtos na mesma malha é outro problema, e a
  integralidade de graça some.
- **Fora da Pesquisa Operacional:** deixar sempre um caminho de volta é o que permite a um
  procedimento guloso ser exato.

## Verificação

1. Na rede desta página, encontre um caminho aumentante partindo de `fabrica` e diga quanto ele
   empurra. *(O1)*
2. A diretoria aprovou verba para ampliar **uma** ligação. Ampliar `fabrica → centro_norte` de 10
   para 20 aumenta o escoamento? E `loja_c → mercado` de 5 para 8? Justifique com o corte. *(O2)*
3. Um hospital quer saber quantos plantões consegue cobrir com a equipe atual, dadas as
   habilitações. Modele como fluxo, dizendo o que é fonte, sumidouro e capacidade. *(O3)*

### Leitura executiva

O resultado central deste capítulo é uma igualdade, e ela é útil antes de ser bonita: **o quanto se
consegue escoar por uma rede é exatamente a capacidade do seu corte mínimo** — não aproximadamente,
não em média. Medido na instância desta página, fluxo máximo **15** e capacidade do corte **15**. O
que torna isso operacional é a natureza do corte: **o gargalo de uma rede não é a aresta mais
estreita**, é um conjunto de arestas que, removidas juntas, separam a origem do destino — e as três
arestas do corte medido aqui nem sequer estão no mesmo nível da rede. Daí saem três decisões
diretas: investir numa aresta **do** corte aumenta o fluxo; investir numa aresta **fora** dele não
muda absolutamente nada, por mais que ela pareça importante; e depois de investir é preciso
**recalcular**, porque o corte se move — o que é a versão em rede de elevar a restrição e voltar ao
início. O método que encontra os dois números é guloso — procurar um caminho com folga, empurrar o
que couber, repetir — e o que o torna **exato** não é a busca, é a **aresta reversa**, que permite
desfazer uma escolha anterior; sem ela, o procedimento trava num fluxo bloqueante e devolve um
número menor com cara de ótimo, que é a mesma classe de defeito silencioso do capítulo 17. Vale
registrar o que este capítulo **não** faz: ele não demonstra o teorema, ele o exibe numa instância
com o corte nomeado, e diz que é isso que está fazendo. Por fim, a lente falha quando o que escoa
tem **tipo** — dois produtos disputando a mesma malha é fluxo multiproduto, e a integralidade de
graça desaparece —, quando a capacidade depende do que já passou, quando o que se quer é o mais
barato em vez do máximo, e quando o gargalo real é organizacional: aí o modelo aponta para o lugar
errado com toda a precisão do mundo.
