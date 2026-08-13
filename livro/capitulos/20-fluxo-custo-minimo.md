# 20 — Fluxo de custo mínimo

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Reconhecer** que transporte, designação, transbordo e planejamento multiperíodo são o
mesmo modelo, e escrever esse modelo uma vez.

**O2.** **Explicar por que a relaxação linear de um problema de rede devolve solução inteira** sem
que ninguém peça — e o que exatamente sustenta isso.

**O3.** **Detectar quando a estrutura de rede se perde**, e dizer o que isso custa.

## O problema

Este é o capítulo mais útil da Parte III, e o resultado que ele publica é o que mais muda decisão
de projeto:

> **A relaxação linear de um problema de rede já vem inteira.** Você não declara nenhuma variável
> binária, não paga nenhum *branch-and-bound* — e a resposta sai em unidades executáveis. Medido:
> custo **220**, **todos os embarques inteiros**, num modelo em que ninguém pediu integralidade.

O leitor que vem do [capítulo 04](04-classificacao-e-escolha.md) sabe o preço de exigir
integralidade: o teorema do vértice cai, o custo de resolução muda de patamar, e a prova de
otimalidade passa a vir de limitante. Aqui está o caso em que **não é preciso pagar esse preço**.

E o erro caro deste capítulo é o outro lado da mesma moeda:

> Alguém acrescenta **uma** restrição perfeitamente razoável — que não é de rede — e a
> integralidade evapora. O modelo continua rodando, continua dizendo `Optimal`, e passa a devolver
> **1,67 caminhão**. Medido nesta página: o ótimo vai de 220 para **223,33**, com **quatro**
> embarques fracionários.

## De onde isto veio

### O aperto: quatro problemas, quatro métodos, e a suspeita de que era um só

Transporte, designação, transbordo e caminho mínimo nasceram separados, cada um com o seu método
especializado — e cada um com o seu conjunto de tabelas na apostila. A suspeita de que fossem o
mesmo objeto veio da forma das restrições: todas diziam a mesma coisa, **o que entra num nó sai
dele**.

### A virada: uma equação por nó

O modelo geral cabe em uma frase: **em cada nó, o que entra menos o que sai é igual ao que aquele
nó consome ou produz**. Isso é conservação de fluxo, e é a única restrição estrutural do modelo.
Oferta é nó com produção positiva; demanda é nó com produção negativa; transbordo é nó com
produção zero.

Com isso, os quatro problemas viram **um**, e a especialização passa a ser uma escolha de
desempenho, não de modelagem.

### A ideia reaproveitável

> **Quando vários problemas têm a mesma forma de restrição, eles são o mesmo problema com dados
> diferentes.** Procurar a forma comum vale mais do que dominar os quatro métodos.

### A origem do nome

**"Transbordo"** (*transshipment*) é o nó que não produz nem consome: a carga passa por ele. O
nome vem do transporte marítimo, em que a carga muda de navio no meio do caminho. **"Totalmente
unimodular"** — a propriedade que faz este capítulo funcionar — quer dizer que **todo** determinante
de toda submatriz quadrada é 0, 1 ou −1. A atribuição do resultado que liga essa propriedade à
integralidade é `⏳` neste handbook.

### Procedência

| Afirmação | Estado |
|---|---|
| Que a matriz de incidência de um grafo dirigido seja totalmente unimodular | 📖 **leitura editorial** de resultado clássico; o handbook **não reproduz a demonstração** |
| A atribuição do teorema que liga unimodularidade total à integralidade dos vértices | ⏳ **atribuição corrente**, não confirmada em fonte primária nesta rodada |
| Que o transporte desta página custe 220 com todos os embarques inteiros | ✓ **medido** em `po-zero/parte-III-redes`, com teste que compara este texto à medição |
| Que uma restrição transversal leve o ótimo a 223,33 com quatro embarques fracionários | ✓ **medido**, na mesma suíte |

## A integralidade que vem da estrutura

Duas fábricas, três lojas, custos por rota:

| | `loja_a` | `loja_b` | `loja_c` | Oferta |
|---|---|---|---|---|
| `fabrica_1` | 4 | 6 | 9 | 20 |
| `fabrica_2` | 5 | 3 | 8 | 30 |
| **Demanda** | 15 | 25 | 10 | |

O modelo é **Programação Linear pura**: variáveis contínuas, sem `Binary`, sem `Integer`. E a
resposta:

| Rota | Quantidade |
|---|---|
| `fabrica_1 → loja_a` | **15** |
| `fabrica_1 → loja_c` | **5** |
| `fabrica_2 → loja_b` | **25** |
| `fabrica_2 → loja_c` | **5** |
| **Custo** | **220** |

**Todos inteiros.** E não por sorte, nem por arredondamento do solver: por **estrutura**. A matriz
de restrições de um problema de rede é totalmente unimodular, e com oferta e demanda inteiras
**todo vértice da região viável é inteiro**. Como o Simplex para num vértice
([capítulo 08](08-geometria.md)), a resposta não tem como sair fracionária.

> **O que isso vale, em uma frase.** Um problema que parecia exigir programação inteira — e
> portanto o custo de resolução que o [capítulo 04](04-classificacao-e-escolha.md) descreve — é
> resolvido como Programação Linear comum, com todas as garantias da Parte II intactas: preço-sombra,
> faixa de validade, análise de sensibilidade. Nada disso sobrevive a um modelo inteiro.

## E como ela se perde

Agora a mesma situação com **uma** restrição a mais, e ela é banal: as rotas ocupam espaço
diferente no pátio de carregamento. Cada unidade de `fabrica_1 → loja_a` ocupa 2 posições, cada
unidade de `fabrica_2 → loja_b` ocupa 3, e o pátio tem 100 posições.

| | Sem a restrição | Com a restrição |
|---|---|---|
| Custo ótimo | **220** | **223,33** |
| Todos inteiros? | **Sim** | **Não** |
| Embarques fracionários | — | **quatro** |

Os fracionários são `fabrica_1 → loja_b` = **1,67**, `fabrica_1 → loja_c` = **3,33**,
`fabrica_2 → loja_b` = **23,33** e `fabrica_2 → loja_c` = **6,67**.

**Nada avisou.** O solver disse `Optimal` nos dois casos. A restrição do pátio é razoável, é real,
e é a coisa mais natural do mundo de se acrescentar — e ao entrar ela tirou a matriz da família de
rede. A propriedade não é do assunto; é da **forma das restrições**.

> **A regra prática que sai daí, e ela é curta:** toda vez que você acrescentar uma restrição que
> **não** seja "o que entra num nó sai dele", desconfie da integralidade. Se a resposta precisar
> ser inteira, aí sim declare a variável como inteira — e assuma o custo, sabendo por que está
> pagando.

> ### ▶ Rode você mesmo
>
> **[Abrir a Parte III no Google Colab](https://colab.research.google.com/github/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-III.ipynb)** · fonte em
> [`po-zero/cadernos/parte-III.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-III.ipynb)
>
> As duas tabelas desta seção saem de uma célula do caderno: a integralidade aparecendo, e sumindo com uma restrição a mais. O caderno **não contém o algoritmo**: chama o código publicado, que o `pytest` já
> verifica ([ADR 0016](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0016-cadernos-colab-sem-deriva.md)).

## Os quatro problemas, num modelo só

| Problema | O que muda no modelo de fluxo |
|---|---|
| **Transporte** | Nós de oferta e de demanda, sem intermediários |
| **Designação** | Transporte com todas as ofertas e demandas iguais a 1 ([capítulo 21](21-transporte-designacao.md)) |
| **Transbordo** | Acrescenta nós com produção zero |
| **Caminho mínimo** | Uma unidade saindo da origem, uma chegando ao destino ([capítulo 17](17-caminho-minimo.md)) |
| **Planejamento multiperíodo** | Um nó por período, e uma aresta de estoque ligando cada um ao seguinte |

A última linha é a que mais paga. Um problema de produção com estoque **não parece** rede, e ao
virar rede herda a integralidade de graça — o que significa que planos de produção em unidades
inteiras saem de um modelo linear comum.

## Quando não serve

**1. Quando há dois produtos disputando a mesma malha.** Fluxo multiproduto tem uma restrição de
capacidade **compartilhada** entre os produtos, e essa restrição não é de rede. A integralidade
some pelo mesmo mecanismo medido acima.

**2. Quando há custo fixo por abrir uma rota.** *"Usar esta rota custa R$ 5.000, mais o custo por
unidade"* exige uma binária de ativação, e aí o problema é inteiro de verdade.

**3. Quando a oferta ou a demanda não são inteiras.** A garantia depende dos **dados** serem
inteiros, e não só da estrutura. Demanda de 12,5 toneladas produz vértice fracionário sem que a
matriz tenha nada de errado.

**4. Quando o custo não é linear no volume.** Desconto por quantidade quebra a linearidade antes
de quebrar a rede.

## Fundamentos e fontes

**O que está medido aqui.** O custo 220 com todos os embarques inteiros; o custo 223,33 com a
restrição de pátio; e os quatro valores fracionários. Em `po-zero/parte-III-redes/redes.py`, com
teste que compara **este texto** à medição.

> **Uma nota de método, porque o experimento errou antes de acertar.** A primeira restrição
> escolhida para quebrar a estrutura deixava o modelo **inviável**, não fracionário — e passou
> despercebida porque a função devolvia o plano sem que ninguém olhasse o `status`. Hoje há
> `assert` explícito. **Um experimento que não confere o próprio veredito mede outra coisa.**

**O que continua em dívida:** a atribuição do teorema da unimodularidade, `⏳`.

> 🔵 **Este capítulo está em "medido".** O que falta para ✅ é revisão independente em contexto
> fresco.

## Pratique

<div data-bateria="cap20"></div>

Três exercícios. O primeiro escreve o modelo único para dois problemas que pareciam diferentes; o
segundo explica a integralidade e prevê quando ela cai; o terceiro é o mais prático da Parte —
diagnosticar um modelo que começou de rede e deixou de ser.

## Assista

**[PO2: Modelo linear para o Fluxo de custo mínimo](https://www.youtube.com/watch?v=ZVFg5FZzPn0)** ·
[Pesquisa Operacional para Todos](https://www.youtube.com/@PesquisaOperacionalparatodos) · 16min17s

**O que ele resolve:** este capítulo gasta o espaço na **propriedade** — por que a resposta sai
inteira, e como isso se perde — e escreve o modelo de forma resumida. O vídeo faz a escrita
completa: a formulação linear do fluxo de custo mínimo, restrição por restrição, com a conservação
em cada nó sendo montada na tela.

## Síntese — o que levar

- **Uma equação por nó:** o que entra menos o que sai é o que o nó produz ou consome. É a única
  restrição estrutural do modelo.
- **Transporte, designação, transbordo, caminho mínimo e planejamento multiperíodo são o mesmo
  modelo** com dados diferentes.
- **A relaxação linear de um problema de rede já vem inteira.** Medido: custo 220, todos os
  embarques inteiros, sem nenhuma variável inteira declarada.
- **A garantia é da estrutura, não do assunto** — e depende também de oferta e demanda serem
  inteiras.
- **Uma restrição fora da forma de rede destrói a propriedade.** Medido: 223,33 e quatro embarques
  fracionários, com `Optimal` nos dois casos e nenhum aviso.
- **Modelo de rede mantém preço-sombra e faixa de validade.** Modelo inteiro, não.
- **Fora da Pesquisa Operacional:** quando vários problemas têm a mesma forma de restrição, eles
  são o mesmo problema com dados diferentes.

## Verificação

1. Um planejamento de produção de seis meses permite estocar de um mês para o seguinte. Escreva a
   equação de conservação do mês 3. *(O1)*
2. Um colega diz que o transporte "dá inteiro porque os custos são inteiros". Corrija, e diga do
   que a garantia de fato depende. *(O2)*
3. Um modelo de distribuição começou de rede e alguém acrescentou *"o total enviado pela frota
   terceirizada não pode passar de 40% do total"*. O que você espera que aconteça, e o que faz?
   *(O3)*

### Leitura executiva

O modelo de fluxo de custo mínimo tem uma única restrição estrutural — **em cada nó, o que entra
menos o que sai é o que aquele nó produz ou consome** — e essa forma comum é o que revela que
transporte, designação, transbordo, caminho mínimo e planejamento multiperíodo são **o mesmo
problema com dados diferentes**. O resultado que o capítulo publica é o que mais muda decisão de
projeto: **a relaxação linear de um problema de rede já devolve solução inteira**, sem nenhuma
variável binária ou inteira declarada e sem o custo de resolução que a integralidade cobra. Medido
aqui: custo **220**, com os quatro embarques em unidades exatas. A razão não é sorte nem
arredondamento — é que a matriz de restrições de uma rede é totalmente unimodular, e com oferta e
demanda inteiras **todo vértice da região viável é inteiro**; como o Simplex para num vértice, a
resposta não tem como sair fracionária. O valor prático disso é grande: um problema que parecia
exigir programação inteira é resolvido como Programação Linear comum, **mantendo preço-sombra,
faixa de validade e análise de sensibilidade**, que são exatamente as coisas que um modelo inteiro
não oferece. O outro lado da moeda é medido na mesma página: acrescentar **uma** restrição banal —
rotas ocupam espaço diferente no pátio de carregamento — tira a matriz da família de rede, e o
ótimo passa de 220 para **223,33** com **quatro embarques fracionários**, entre eles 1,67 e 3,33.
**Nada avisa**: o solver diz `Optimal` nos dois casos. A regra prática que sobrevive é curta: toda
vez que entrar uma restrição que não seja "o que entra num nó sai dele", desconfie da
integralidade; se a resposta precisar ser inteira, declare a variável como inteira e assuma o
custo sabendo por que está pagando. A propriedade também some quando há dois produtos disputando a
mesma malha, quando há custo fixo de abertura de rota, quando o custo não é linear no volume, e —
detalhe fácil de esquecer — quando a própria oferta ou demanda não é inteira, porque a garantia
depende dos dados tanto quanto da estrutura.
