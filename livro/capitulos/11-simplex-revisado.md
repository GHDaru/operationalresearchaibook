# 11 — Simplex revisado e implementação eficiente

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Escrever** o Simplex em forma matricial e dizer o que cada peça faz — a base $B$, a
inversa $B^{-1}$, e o custo reduzido lido como **preço**.

**O2.** **Explicar** por que manter $B^{-1}$ custa menos que recarregar o quadro inteiro — e **em
que instâncias isso deixa de ser verdade**.

**O3.** **Reconhecer** a esparsidade como propriedade do **modelo**, não do algoritmo, e dizer o
que ela muda.

**O4.** **Diagnosticar** estagnação e distingui-la de ciclagem e de lentidão, encadeando no
capítulo 10.

**O5.** **Explicar** por que a tolerância numérica é decisão de **modelagem**, e o que dá errado
quando ela é escolhida por acaso.

## O problema

O quadro do [capítulo 09](09-simplex.md) tem $m$ linhas e $n + m$ colunas, e **cada pivô mexe em
todas elas**. Com 3 restrições e 2 variáveis isso é trivial. Com 3 mil restrições e 50 mil
variáveis, cada iteração toca 150 milhões de números — e você só precisava de $m$ deles.

E há um desperdício mais incômodo do que o tamanho. Repare no que o quadro faz a cada pivô:

> Ele **atualiza tudo**, para que a próxima iteração possa **ler** o que precisa. É um contrato
> razoável e é uma aposta: paga-se manutenção adiantada na esperança de que o que foi mantido
> seja usado. A cada iteração o Simplex usa **uma** coluna. As outras foram atualizadas por nada.

A forma revisada faz a aposta contrária: **não mantém nada** e recalcula o que precisa, a partir
dos dados originais, guardando só $B^{-1}$.

Este capítulo mede as duas apostas. E o resultado não é o que o folclore diz.

## De onde isto veio

### O aperto: a memória da máquina

O Simplex nasce em 1947 e é posto para trabalhar em máquinas cuja memória se mede em milhares de
palavras. Um quadro de umas poucas centenas de linhas por milhares de colunas **não cabe**. A
questão não era elegância: era caber.

> ⏳ **A tese acima é corrente e este handbook não a confirmou na fonte.** O artigo primário —
> Dantzig e Orchard-Hays, *"The product form for the inverse in the simplex method"*, 1954 — está
> `✓ᵐ`: identificador e existência conferidos, **conteúdo não aberto**. Se o texto não sustentar o
> aperto de memória como motivo declarado, **esta seção encolhe**, e é assim que estava previsto
> desde o plano da rodada.

### O que se fazia antes, e a virada

Antes, guardava-se o quadro. A virada tem nome no próprio título do artigo de 1954: **forma de
produto da inversa**. Em vez de guardar a matriz $B^{-1}$, guardam-se os **fatores** que a
produzem — um por iteração —, e a inversa nunca é escrita por inteiro. Dez anos depois, um
relatório técnico de **Dantzig, Harvey e McKnight** (1964) trata da **atualização** desses fatores
ao longo das iterações, que é a operação que o capítulo 09 prometeu com o verbo *refatorar* e que
esta página paga.

### A ideia reaproveitável

> **Guardar o que produz o resultado costuma custar menos do que guardar o resultado — e mantê-lo
> atualizado custa ainda menos do que refazê-lo.**

É o padrão do *log* de transações, do *event sourcing*, do controle de versão. E, como todo padrão,
tem o seu contrário: quando o resultado é pequeno e as consultas são muitas, guardar o resultado
ganha. Qual dos dois vale **não se decide no quadro-negro** — e é por isso que o resto deste
capítulo é medição.

### Procedência

| Afirmação | Estado |
|---|---|
| Dantzig e Orchard-Hays, "The product form for the inverse in the simplex method", 1954 | ✓ᵐ metadados e existência conferidos — [bibliografia](../bibliografia.md) |
| Dantzig, Harvey e McKnight, "Updating the product form of the inverse…", 1964 | ✓ᵐ metadados conferidos |
| Que o **aperto de memória** foi o motivo declarado da invenção | ⏳ **tese corrente, não confirmada** — o conteúdo dos dois artigos não foi aberto |
| A atribuição do nome "forma de produto da inversa" | ✓ᵐ está no **título** do artigo de 1954, que foi conferido |

## A ponte — o Simplex em forma matricial

Uma notação, e ela paga o resto do capítulo. Separe as colunas de $A$ em duas famílias: as da
**base** e as de fora.

| Peça | O que é |
|---|---|
| $B$ | a matriz $m \times m$ com as colunas das variáveis **básicas** |
| $B^{-1}$ | a inversa dela — a peça que a forma revisada guarda |
| $x_B = B^{-1}b$ | os valores das básicas: é a coluna $b$ do quadro |
| $y^{\top} = c_B^{\top}B^{-1}$ | os **preços-sombra** — os mesmos do [capítulo 12](12-dualidade.md) |
| $c_j - y^{\top}a_j$ | o **custo reduzido** da coluna $j$ |

A última linha é a que muda a cabeça de quem vem do quadro. No capítulo 09 o custo reduzido era
*"o número que sobrou na linha $z$ depois das eliminações"* — um resíduo de procedimento. Aqui ele
tem significado econômico: **o lucro da coluna menos o que ela custa aos preços correntes**. Se
sobra, vale a pena entrar.

> **A linha que fecha a ponte, e ela é a mais importante desta seção.** Nada disso pede que se
> **calcule** $B^{-1}$. Inverter uma matriz é caro e numericamente ruim, e **solver nenhum faz
> isso**: o que se guarda são fatores que permitem *resolver sistemas* com $B$, e o símbolo
> $B^{-1}$ é notação, não instrução. A implementação deste capítulo mantém a inversa explícita
> **de propósito didático**, e é essa escolha — não a forma revisada em si — que produz metade do
> resultado medido adiante.

## O algoritmo, em quatro linhas

Cada iteração da forma revisada:

1. **Preços:** $y^{\top} = c_B^{\top}B^{-1}$.
2. **Quem entra:** procure $j$ fora da base com $c_j - y^{\top}a_j > 0$ — usando a **coluna
   original** $a_j$.
3. **Direção:** $d = B^{-1}a_q$ para a coluna $q$ escolhida; teste da razão sobre $x_B$ e $d$.
4. **Refatorar:** atualize $B^{-1}$ e $x_B$ pelo pivô.

Compare com o quadro: os passos 1 e 2 são o que o quadro **não precisa fazer**, porque já mantém a
linha $z$ pronta; o passo 4 é o que a forma revisada faz **em $m \times m$** em vez de
$m \times (n+m)$. A troca inteira está aí, e agora ela vira número.

## O código

A [etapa 05 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-05-parte2)
implementa as duas formas sobre **a mesma primitiva aritmética instrumentada**, o que torna a
comparação justa por construção — nenhuma das duas pode deixar de contar uma operação sem deixar
de calculá-la. O desenho está na [ADR 0012](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0012-o-desenho-da-medicao-do-capitulo-11.md),
e cada decisão dela está marcada no código.

**A convenção de contagem, declarada:** contam-se multiplicações e divisões; somas acompanham as
multiplicações uma a uma nos dois lados e não mudam a comparação. **Multiplicação por zero não é
executada nem contada, nas duas formas** — é exatamente a economia que a esparsidade produz, e
escondê-la falsearia o experimento em favor do quadro.

**Três garantias, verificadas em toda instância:** as duas formas concordam com a
[etapa 03](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-03-simplex),
publicada e **intocada**, que serve de árbitro independente; as duas percorrem a **mesma
trajetória de pivô** — sem isso, as contagens mediriam caminhos diferentes e a comparação seria
sobre a regra de pivoteamento; e as seis instâncias foram **congeladas antes** da primeira
execução, com **todas** publicadas, não só as que mostraram efeito.

## O resultado, e ele contraria o esperado

```
instância            m    n  dens A  quadro fim  B⁻¹ fim  iter  ops quadro  ops revis.  quadro/revis.
pequena densa        4    6    1.00        0.68     0.81     4         172         136          1.265
pequena esparsa      4    6    0.46        0.44     0.31     6         116         124          0.935
média densa          8   30    1.00        0.81     0.45    21        6100        3262           1.87
média esparsa        8   30    0.27        0.41     0.27    17        1428        1065          1.341
magra densa         10  120    1.00        0.93     0.64    75      100990       34170          2.956
magra esparsa       10  120    0.13        0.20     0.10    32        1350        1809          0.746
```

Leia a última coluna. Acima de 1, a forma revisada gasta menos.

**Nas densas ela ganha, e o ganho cresce com a razão $n/m$:** 1,27× com 6 variáveis para 4
restrições, 1,87× com 30 para 8, **2,96×** com 120 para 10. Faz sentido: quanto mais colunas o
quadro tem de manter, mais ele mantém à toa.

**Nas esparsas ela perde**, ou quase: 0,94×, 1,34× e **0,75×**. Isto **não** é o que o folclore
diz — "a forma revisada aproveita a esparsidade" —, e entra no capítulo porque a
[spec da rodada](https://github.com/GHDaru/operationalresearchaibook/blob/main/specs/008-cap11-simplex-revisado/spec.md)
comprometeu-se com isso antes de medir.

### Por que, medido

A resposta está nas duas colunas do meio, e é a razão de elas existirem.

**O quadro perde a esparsidade ao pivotear.** É o **preenchimento** (*fill-in*): cada eliminação
transforma zeros em não-zeros. Na "média esparsa" ele parte de 0,27 e termina em **0,41** — quase
o dobro de trabalho por iteração no fim do que no começo. E ali a forma revisada ganha.

Na "magra esparsa", o quadro parte de 0,13 e termina em **0,20**: ele **quase não preenche**, e
continua barato de manter a execução inteira. Ali a forma revisada perde.

> **A troca, enunciada com precisão:** o quadro **mantém tudo para poder ler**; a forma revisada
> **não mantém nada e recalcula o que precisa**. Qual sai mais barato depende de quanto o quadro
> preenche — e preenchimento é propriedade da instância, não do método.

E há a metade que a implementação escolheu: **esta versão guarda $B^{-1}$ explicitamente**, e paga
$m^2$ por iteração independentemente da esparsidade. É exatamente o que a forma de produto da
inversa evita, e é por isso que ela existe. **O experimento não mede a forma de produto** — mede a
forma revisada com inversa explícita, que é a versão didática.

## A esparsidade é do modelo

Repare no que a tabela não tem: nenhuma coluna chamada "esparsidade do algoritmo". A densidade é
medida na matriz $A$, que vem do **modelo** — de quantos recursos cada produto de fato consome.

Um modelo de produção real é esparso porque cada produto usa poucos componentes dentre os
milhares do catálogo. Nenhuma escolha de método cria isso, e nenhuma escolha de método o destrói —
**mas a escolha de método decide se ele será aproveitado**. É a diferença entre uma propriedade e o
uso que se faz dela.

## Estagnação, ciclagem e lentidão

O [capítulo 10](10-casos-especiais.md) mediu ciclagem e disse que o problema **prático** é outro:
*estagnação* — muitas iterações sem melhora, porém finitas. Aqui isso ganha instrumento, com
limiar **declarado antes de medir**:

> **Estagnação = 3 ou mais iterações consecutivas sem melhora do objetivo.** Três e não duas
> porque um empate isolado é rotina em vértice degenerado. "Sem melhora" é igualdade exata — em
> `Fraction` não há ambiguidade sobre o que é zero.

| Fenômeno | O instrumento vê |
|---|---|
| **Ciclagem** | uma **base** já visitada volta |
| **Estagnação** | sequência ≥ 3 sem melhora, sem repetição de base |
| **Lentidão** | muitas iterações, **todas** melhorando |

### O resultado negativo, publicado como resultado

```
instância aleatória: 30 iterações · sem melhora: 0 · maior sequência: 0 · VEREDITO: lentidão
degenerada de propósito (5 restrições no mesmo vértice):
                      3 iterações · maior sequência sem melhora: 1 · VEREDITO: normal
```

**Nenhuma das duas atinge o limiar.** Este handbook **não conseguiu construir**, nos tamanhos que
cabem aqui, uma instância que estagne pela sua própria régua — nem sorteando, nem empilhando cinco
restrições sobre o mesmo vértice.

E **o limiar não foi baixado para o exemplo caber**. Baixá-lo depois de ver o resultado seria
ajustar até ficar verde, que é o modo mais comum de um experimento deixar de significar alguma
coisa. O que o capítulo entrega, então, é o **instrumento** e a distinção — e a informação de que
estagnação é fenômeno de escala, não de instância pequena.

## A tolerância é decisão de modelagem

O [capítulo 10](10-casos-especiais.md) deixou pendente o item 4: em ponto flutuante, o
arredondamento troca um problema honesto por um pior — decidir se dois números "iguais" são iguais.
Medido, na mesma instância:

```
valor exato: 965935/486   ·   valor em float: 1987.520576131687
erro absoluto: 2.274e-13  ·   relativo: 1.144e-16
iterações: 30 (exato) contra 30 (float)
mesma base ao final: True   ·   O VEREDITO MUDOU: False
```

**Segundo resultado negativo**, e ele também é publicado: aqui o ponto flutuante **não** mudou o
veredito. Erro na décima terceira casa, mesma base, mesmo número de iterações.

Isso **não** autoriza a conclusão confortável. Repare no que a última linha mede, e por que ela
existe separada do erro: **um erro pequeno no valor não garante o mesmo veredito**. Base diferente
significa **plano diferente** — outras quantidades, outros fornecedores — ainda que o lucro
coincida até a última casa que se olhou. Foi por isso que a medição comparou a **base**, e não só
o número.

E é daí que sai o objetivo O5. A tolerância que decide se um custo reduzido "é zero" não é
detalhe de implementação: ela decide **se o método para**. Apertada demais, o solver continua
pivoteando por ruído; frouxa demais, ele para antes do ótimo e ninguém percebe. Escolhê-la exige
saber a **escala dos dados do seu modelo** — que é informação de modelagem, não de código.

## Quando não serve

**1. A forma revisada não ganha sempre**, e este capítulo mediu duas instâncias em que ela perde.
O ganho depende de quanto o quadro preenche, e preenchimento é da instância.

**2. O que foi medido é a versão didática.** Guardar $B^{-1}$ explícito não é o que se faz em
produção — a forma de produto da inversa e as fatorações existem exatamente para evitá-lo. Metade
do resultado negativo desta página é consequência dessa escolha, e ela está declarada.

**3. A contagem de operações não é tempo.** Ela ignora acesso à memória, *cache*, e a diferença
entre `Fraction` e ponto flutuante — que é enorme. Uma razão de 2,96× em operações **não** é uma
promessa de 2,96× em segundos.

**4. Nenhuma instância aqui tem escala industrial.** Milhares de restrições não cabem numa página
de livro nem numa execução de segundos em aritmética exata. As tendências medidas apontam uma
direção; elas não substituem um *benchmark*.

**5. Estagnação continua sem demonstração própria.** O instrumento existe e o limiar está
declarado; a instância que o dispare, não.

## Fundamentos e fontes

**O que está medido aqui.** As seis instâncias com contagem de operações, densidades e razões; as
duas tentativas de estagnação; a comparação `Fraction` contra `float`. Tudo se regenera rodando um
script, com semente e convenção de contagem publicadas.

**O que foi conferido no registro, e não lido.** ✓ᵐ **DANTZIG, G. B.; ORCHARD-HAYS, W.** (1954) e
✓ᵐ **DANTZIG, G. B.; HARVEY, R. P.; McKNIGHT, R. D.** (1964).

**O que continua em dívida:** se o artigo de 1954 declara o **aperto de memória** como motivo. É a
tese que abre este capítulo, ela está marcada `⏳`, e se o texto não a sustentar a seção encolhe.

> 🔵 **Este capítulo está em *medido*.** Todo número dele se regenera por experimento, e ele
> **ainda não passou por revisão independente em contexto fresco** — que é o que falta para ✅.

## Pratique

<div data-bateria="cap11"></div>

Cinco exercícios, um por objetivo. O terceiro é o mais incômodo: ele pede que você **explique um
resultado que contraria o que o capítulo prometeu** — que é o trabalho de verdade quando um
experimento não coopera.

## Assista

**[Notação Matricial, Base, Solução Geral e Solução Básica em Programação
Linear](https://www.youtube.com/watch?v=bQUkXmjppK4)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 35min18s

**O que ele resolve:** este capítulo usa a notação matricial como **ferramenta** — apresenta as
peças e vai medir. O vídeo faz o percurso que falta: constrói a notação devagar, com a álgebra
inteira, e mostra de onde saem $B$, $B^{-1}$ e a solução básica. É a segunda passada para quem
sentiu a ponte curta.

## Síntese — o que levar

- **O quadro mantém tudo para poder ler; a forma revisada não mantém nada e recalcula.** É a
  troca inteira, e ela não tem vencedor universal.
- **Custo reduzido é preço:** $c_j - y^{\top}a_j$ — o lucro da coluna menos o que ela custa aos
  preços correntes. Deixa de ser resíduo de procedimento.
- **Ninguém calcula $B^{-1}$.** O símbolo é notação; solvers guardam fatores e resolvem sistemas.
- **Medido: a forma revisada ganha nas densas** (até 2,96×, e o ganho cresce com $n/m$) **e perde
  nas esparsas** (0,75×). O folclore diz o contrário.
- **A explicação é o preenchimento**, e foi medida: o quadro que preenche muito fica caro e a
  revisada ganha; o que quase não preenche continua barato e a revisada perde.
- **Esparsidade é propriedade do modelo.** O método não a cria nem a destrói — decide se ela é
  aproveitada.
- **Dois resultados negativos publicados:** nenhuma instância atingiu o limiar de estagnação, e o
  ponto flutuante não mudou o veredito. O limiar **não** foi baixado depois de ver o resultado.
- **Compare a base, não só o valor.** Erro pequeno no número não garante o mesmo plano.
- **Fora da Pesquisa Operacional:** guardar o que produz o resultado costuma custar menos do que
  guardar o resultado — e qual dos dois vale não se decide no quadro-negro.

## Verificação

1. Um colega diz que a forma revisada "é mais rápida porque não precisa do quadro". Complete a
   frase dele com a condição que falta, e diga como você a verificaria numa instância sua. *(O2)*
2. Um relatório afirma que dois solvers "chegaram ao mesmo ótimo, com diferença de $10^{-12}$". Que
   pergunta você faz antes de aceitar que a resposta é a mesma? *(O5)*
3. Um modelo roda 400 iterações. Que três hipóteses você levanta, e qual medida distingue uma da
   outra? *(O4)*

### Leitura executiva

O quadro do capítulo 09 atualiza **todas** as suas colunas a cada pivô para que a iteração seguinte
possa apenas **ler** o que precisa — e a cada iteração o Simplex usa uma coluna só. A forma
revisada faz a aposta contrária: guarda apenas $B^{-1}$, não mantém mais nada, e **recalcula** a
cada passo o que vai usar, a partir das colunas originais. Nessa releitura o custo reduzido deixa
de ser um resíduo de eliminações e vira **preço**: $c_j - y^{\top}a_j$, o lucro da coluna menos o
que ela custa aos preços-sombra correntes, que são os mesmos do capítulo 12. Vale dizer desde já
que **ninguém calcula $B^{-1}$** — inverter matriz é caro e numericamente ruim, e os solvers
guardam fatores que permitem resolver sistemas; o símbolo é notação, não instrução. Medindo as duas
formas sobre a mesma primitiva aritmética instrumentada, com a mesma trajetória de pivô e um
árbitro independente, o resultado **contraria o folclore**: a forma revisada ganha nas instâncias
densas, com vantagem crescente na razão entre variáveis e restrições (1,27×, 1,87× e 2,96×), e
**perde** em duas das três esparsas (0,94× e 0,75×). A explicação também foi medida, e é o
**preenchimento**: cada eliminação do quadro transforma zeros em não-zeros, de modo que ele fica
mais caro conforme executa — na instância em que ele salta de 0,27 para 0,41 de densidade, a forma
revisada ganha; naquela em que quase não preenche (0,13 para 0,20), ela perde. Some-se a isso que a
implementação didática guarda a inversa **explícita** e paga $m^2$ por iteração qualquer que seja a
esparsidade, que é exatamente o custo que a forma de produto da inversa existe para evitar. Duas
medições deram negativo e foram publicadas como resultado: nenhuma instância construída aqui —
nem sorteada, nem deliberadamente degenerada — atingiu o limiar de estagnação **declarado antes**
de três iterações consecutivas sem melhora, e o limiar não foi baixado depois; e o ponto flutuante
não mudou o veredito, com erro relativo de $10^{-16}$ e a mesma base final. Este último detalhe é
o que sustenta a lição sobre tolerância: comparar apenas o **valor** não basta, porque bases
diferentes significam planos diferentes ainda que o lucro coincida, e a tolerância que decide se um
custo reduzido "é zero" decide na prática **se o método para** — o que a torna decisão de
modelagem, dependente da escala dos dados, e não detalhe de implementação.
