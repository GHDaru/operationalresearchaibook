# 14 — Métodos de pontos interiores

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Explicar** o que "atravessar em vez de contornar" significa geometricamente, e por que
reescalar o espaço resolve o problema que o gradiente puro tem perto da fronteira.

**O2.** **Diagnosticar** o que quebra quando a resposta de um método interior **não é vértice** —
na leitura do plano, na base e no preço-sombra.

**O3.** **Escolher** entre Simplex e ponto interior para uma instância descrita, e **justificar**
pelo que a instância tem, não pela fama do método.

## O problema

Cinco capítulos atrás você aprendeu que o ótimo mora numa quina, e desde então tudo neste livro
anda pelas quinas. O [capítulo 08](08-geometria.md) provou que basta olhar os vértices; o
[capítulo 09](09-simplex.md) construiu o método que caminha de vértice em vértice; o
[capítulo 11](../mapa-do-handbook.md) o fará caber em memória.

Agora imagine um problema com **um milhão de variáveis**. O ótimo continua numa quina — o teorema
não mudou. Mas o número de quinas cresce de um jeito que não cabe em nenhuma agenda, e a pergunta
deixa de ser "o ótimo está numa quina?" e passa a ser **"quantas quinas eu vou ter de visitar
antes de achar a certa?"**.

Foi essa pergunta que abriu espaço para uma família inteira de métodos que fazem a coisa que os
dez capítulos anteriores diziam ser desnecessária: **andar por dentro**.

E aqui está o incômodo que este capítulo precisa resolver, porque ele parece uma contradição:

> Se a resposta está na quina, por que um método que **evita** as quinas é competitivo? E, pior:
> quando ele termina, **a resposta que ele entrega não é uma quina**. Como é que isso pode estar
> certo?

O erro caro deste capítulo é ler a saída de um método interior com os olhos do Simplex — esperar
uma base, esperar variáveis exatamente zeradas, esperar preço-sombra único. Nada disso vem, e
quem não foi avisado conclui que o solver errou.

## De onde isto veio

### O aperto: ninguém sabia se Programação Linear era "fácil"

Nos anos 1970 o Simplex já era ferramenta industrial havia duas décadas e funcionava bem. Mas
havia um constrangimento teórico: **ninguém tinha provado que ele é eficiente no pior caso** — e,
pior, apareceram famílias de instâncias em que ele visita um número exponencial de vértices.

A pergunta aberta era de complexidade: existe **algum** algoritmo que resolva Programação Linear
em tempo polinomial? Enquanto ela estivesse aberta, o método mais usado do mundo carregava um
asterisco.

### A virada, em duas etapas — e elas são diferentes

**1979 — Khachiyan** responde a pergunta teórica com o **método do elipsoide**: sim, Programação
Linear é polinomial. Foi notícia muito além da academia — o [estudo 002](https://github.com/GHDaru/operationalresearchaibook/blob/main/estudos/002-historia-dos-metodos.md)
registra a repercussão no *New York Times* em 1979.

E aí veio a decepção instrutiva: **na prática o método do elipsoide perdia feio para o Simplex**.
A resposta teórica estava certa e não servia para trabalhar. É um dos casos mais limpos da
computação em que *polinomial* e *rápido* se separam de forma visível.

**1984 — Karmarkar** apresenta um algoritmo que é polinomial **e** competitivo na prática. É a
virada que abre a família dos métodos de ponto interior como ferramenta, não como teorema.

| Ano | Quem | O que estabeleceu | Prática |
|---|---|---|---|
| 1979 | Khachiyan | Programação Linear **é** polinomial (elipsoide) | perdia para o Simplex |
| 1984 | Karmarkar | polinomial **e** competitivo | mudou o mercado |

### A ideia reaproveitável

> **Perto da parede, a distância importa mais do que a direção.**

O gradiente aponta para onde melhora, e perto da fronteira essa informação é quase inútil: qualquer
passo do tamanho certo sai da região. Os métodos interiores resolvem isso **reescalando o espaço**
para que o ponto atual fique longe de todas as paredes, dando o passo lá, e trazendo-o de volta —
o que automaticamente encolhe o passo nas direções apertadas.

Fora da Pesquisa Operacional o padrão é o mesmo: quando um sistema se comporta mal perto de um
limite, muitas vezes não se muda a direção do esforço — **muda-se a métrica** em que ele é medido.

### Procedência

| Afirmação | Estado |
|---|---|
| Khachiyan, "Polynomial algorithms in linear programming", 1980 | ✓ᵐ metadados conferidos — [bibliografia](../bibliografia.md) |
| Karmarkar, "A new polynomial-time algorithm for linear programming", *Combinatorica*, 1984 | ✓ᵐ metadados conferidos |
| Repercussão do resultado de 1979 no *New York Times* | ⏳ registrada no [estudo 002](https://github.com/GHDaru/operationalresearchaibook/blob/main/estudos/002-historia-dos-metodos.md), não conferida na fonte primária |
| A controvérsia da patente da AT&T sobre o algoritmo de Karmarkar | ⏳ atribuição corrente, não confirmada |
| Que o elipsoide "perdia na prática" | ⏳ **afirmação corrente do campo**; este handbook **não a mediu** e não cita comparação com instâncias declaradas |

> Os dois artigos estão `✓ᵐ`: identificador e existência conferidos, **conteúdo não aberto**.
> Nenhuma afirmação técnica deste capítulo se apoia neles — o que o capítulo ensina sai da
> [etapa 07](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-07-pontos-interiores),
> que roda aqui.

## A intuição — por dentro, e por que isso não contradiz o capítulo 08

Pense na região viável como uma sala, e no objetivo como uma direção em que você quer ir o mais
longe possível.

**O Simplex** anda pelas paredes. Vai até uma quina, escolhe a aresta que sobe, chega na quina
seguinte, repete. Nunca entra na sala.

**O método interior** começa **no meio da sala** e vai andando na direção que melhora, tomando o
cuidado de não encostar. Como não pode encostar, ele **nunca chega** na quina — chega tão perto
quanto você exigir.

E aqui está a reconciliação com o capítulo 08, que é o ponto conceitual deste capítulo:

> O teorema diz que **existe** um ótimo numa quina. Ele **não** diz que o método precisa andar
> pelas quinas para achá-lo. Um é um fato sobre onde a resposta mora; o outro seria um fato sobre
> como chegar lá — e não está no teorema.

## O código

A [etapa 07 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-07-pontos-interiores)
implementa **escalonamento afim**, que é o método interior mais curto que existe e o esqueleto dos
que o mercado usa. Não é o algoritmo de Karmarkar nem um *primal-dual* moderno, e o capítulo diz
isso em vez de deixar entender outra coisa.

### Ponto flutuante, declarado

Todas as outras etapas deste handbook usam frações e aritmética exata. **Esta não pode**, e o
motivo é de natureza, não de descuido: método interior é iterativo e converge a um **limite**.
A resposta é aproximada por construção.

É o primeiro lugar do livro em que isso acontece, e vira conteúdo em vez de rodapé.

### A montadora, atravessada

```
montadora — ótimo único
  iterações: 11  ·  ponto [7.999996, 2.000002]  ·  valor 1099.99982
  chegou em vértice: False
  algum ponto intermediário é vértice: False
  trajetória (primeiros 4): [[1.0, 1.0], [3.0302, 4.0349], [5.2775, 3.3162], [7.7995, 2.0599]]
```

Leia a trajetória. Ela parte de $(1,1)$ — bem no meio —, passa por $(3{,}03;\ 4{,}03)$, por
$(5{,}28;\ 3{,}32)$, e vai se aproximando de $(8, 2)$. **Nenhum desses pontos é vértice**, e o
último também não é.

### A diferença de natureza, em número

```
Simplex (fração exata):     ponto (8, 2)                 valor 1100        2 pivôs
interior (ponto flutuante): ponto [7.999996, 2.000002]   valor 1099.99982  11 iterações
distância ao vértice: 4.472e-06 · erro no valor: 1.800e-04
```

**O Simplex chega. Este se aproxima.** A distância de $4{,}5 \times 10^{-6}$ não é defeito de
implementação: é o que "convergir a um limite" significa. Aperte a tolerância e ela diminui;
zerá-la é impossível.

E repare no que isso implica para a leitura: no ponto interior, **nenhuma variável vale exatamente
zero**. Se você perguntar "quais restrições estão apertadas?", a resposta numérica é "todas quase".
A pergunta que o Simplex responde de graça, aqui exige uma tolerância e uma decisão.

### Quando há mais de um ótimo, os dois métodos discordam

A marcenaria do [capítulo 10](10-casos-especiais.md) tem um **segmento** de ótimos, entre $(4,0)$ e
$(2,3)$, todos valendo 24. O Simplex devolve **uma das duas quinas** — qual delas depende da regra
de pivoteamento, como aquele capítulo mediu. O método interior devolve:

```
marcenaria — segmento de ótimos
  iterações: 6  ·  ponto [2.928002, 1.607993]  ·  valor 23.999986
  chegou em vértice: False
```

Esse ponto está **no meio do segmento** — sobre a reta entre $(4,0)$ e $(2,3)$, a cerca de 54% do
caminho. Não é vértice, não é solução básica, e **está correto**: vale 24, como as duas quinas.

É a discordância mais instrutiva do capítulo:

| | O que devolve, com múltiplos ótimos |
|---|---|
| **Simplex** | uma **quina**, escolhida pela regra de pivoteamento |
| **Ponto interior** | um ponto **no meio da face ótima**, sem base associada |

Nenhum dos dois está errado. Eles respondem a perguntas ligeiramente diferentes, e é o leitor que
precisa saber qual delas fez.

## Quando não serve

**1. A resposta não é vértice, e isso quebra o que vem depois.** Sem base, não há leitura direta
de preço-sombra pelo quadro ([capítulo 12](12-dualidade.md)) nem faixa de sensibilidade pela
$B^{-1}$ ([capítulo 13](13-sensibilidade.md)). Solvers de mercado resolvem isso com uma etapa de
***crossover***, que converte a solução interior numa solução básica equivalente — e ela custa
tempo. **Se você precisa do relatório de sensibilidade, precisa do *crossover*.**

**2. Não há reotimização barata.** O Simplex reaproveita a base para reotimizar depois de uma
mudança pequena — é o que sustenta o *branch and bound* da programação inteira, que resolve
milhares de problemas parecidos em sequência. Método interior recomeça. Por isso a programação
inteira continua sendo território do Simplex.

**3. O que este capítulo mostra é um esqueleto.** Escalonamento afim ilustra a ideia; os métodos
de mercado são *primal-dual* com barreira logarítmica, preditor-corretor e álgebra esparsa. A
distância entre um e outro é grande, e este handbook não a atravessa na v0.

**4. Este handbook não mediu desempenho comparado.** Não há aqui nenhuma afirmação do tipo "ponto
interior ganha acima de $N$ variáveis" — seria exatamente o tipo de comparação sem instância,
*baseline* e máquina que o [capítulo 77](77-ler-artigo.md) ensina a recusar. O que se afirma é
**qualitativo e verificável**: em problemas grandes e esparsos a família interior é a escolha
usual do mercado, e o número de iterações cresce muito devagar com o tamanho.

**5. A tolerância é uma decisão sua.** "Convergiu" significa "o resíduo ficou abaixo do que eu
pedi". Em problemas mal condicionados, apertar a tolerância pode custar muito e, em casos ruins,
não chegar.

## Como escolher

Nenhuma regra fechada — o que existe é um conjunto de perguntas, e elas são sobre a **instância**,
não sobre a fama do método.

| Pergunte | Se sim, pesa para |
|---|---|
| O problema é grande e esparso, resolvido **uma vez**? | **ponto interior** |
| Você precisa de **preço-sombra e faixas** para decidir? | **Simplex**, ou interior **com *crossover*** |
| Vai resolver **milhares de variações** do mesmo problema (inteira, *branch and bound*)? | **Simplex**, pela reotimização |
| A instância é pequena e você quer entender o resultado? | **Simplex**, pela leitura |
| Você precisa de uma resposta **exata**, em fração? | **Simplex** |

> **O que não é critério:** "é mais moderno". Karmarkar é de 1984 e o Simplex de 1947, e os dois
> continuam nos solvers de mercado — lado a lado, porque respondem a necessidades diferentes.

## Fundamentos e fontes

**O que está medido aqui.** As 11 iterações, a trajetória, o ponto de chegada, a distância de
$4{,}5 \times 10^{-6}$ ao vértice, o erro de $1{,}8 \times 10^{-4}$ no valor e o ponto no meio do
segmento da marcenaria saem todos da etapa 07 e se regeneram rodando um script.

**O que foi conferido no registro, e não lido.** ✓ᵐ **KHACHIYAN, L. G.** (1980) e ✓ᵐ **KARMARKAR,
N.** (*Combinatorica*, 1984). Identificadores e existência conferidos; **conteúdo não aberto**, e
nenhuma afirmação técnica deste capítulo se apoia neles.

**O que continua em dívida:** a repercussão de 1979 na imprensa e a controvérsia da patente da
AT&T, ambas `⏳`; e a afirmação corrente de que o elipsoide perdia na prática, que este handbook
**não mediu** e por isso apresenta como afirmação do campo, não como resultado próprio.

> 🟡 **Este capítulo está em v0.** Não passou por revisão independente em contexto fresco, e a
> distância entre o esqueleto que ele implementa e um solver de mercado está declarada em
> [Quando não serve](#quando-não-serve).

## Pratique

<div data-bateria="cap14"></div>

Três exercícios. O primeiro é sobre a ideia geométrica e por que ela não contradiz o capítulo 08.
O segundo é o diagnóstico de uma saída que não é vértice. O terceiro é a escolha entre os dois
métodos, com justificativa pela instância.

## Assista

**[Métodos de Pontos Interiores: Ideia e um pouco de história — Programação Linear,
Otimização](https://www.youtube.com/watch?v=5F0MoJMuVhI)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 9min17s

**O que ele resolve:** este capítulo entra pela medição — a trajetória, o ponto que não é vértice,
os dois métodos discordando. O vídeo faz a apresentação da ideia e do contexto histórico em menos
de dez minutos, e é a melhor primeira passada para quem quer o mapa antes do detalhe.

## Síntese — o que levar

- **O teorema do capítulo 08 diz onde a resposta mora, não por onde ir buscá-la.** Um método que
  atravessa a região não o contradiz.
- **Perto da parede, o gradiente puro é inútil.** A ideia da família interior é **reescalar o
  espaço** para que o ponto atual fique longe de todas as paredes.
- **Duas viradas, e elas são diferentes:** 1979 respondeu a pergunta teórica (é polinomial); 1984
  entregou um método que também era prático. *Polinomial* e *rápido* não são a mesma coisa.
- **O Simplex chega; o interior se aproxima.** Medido: distância de $4{,}5 \times 10^{-6}$ ao
  vértice, erro de $1{,}8 \times 10^{-4}$ no valor. Não é defeito — é o que converger a um limite
  significa.
- **A resposta não é vértice**, e por isso não vem com base, preço-sombra nem faixa. Quem precisa
  disso precisa do ***crossover***.
- **Com múltiplos ótimos os dois discordam**, e ambos acertam: o Simplex devolve uma quina, o
  interior devolve um ponto no meio da face ótima.
- **Não há reotimização barata**, e é por isso que a programação inteira continua com o Simplex.
- **Fora da Pesquisa Operacional:** quando um sistema se comporta mal perto de um limite, às vezes
  não se muda a direção do esforço — muda-se a métrica.

## Verificação

1. Um colega diz que métodos de ponto interior "contradizem o teorema de que o ótimo está num
   vértice". Em duas frases, mostre por que não há contradição. *(O1)*
2. Um solver devolveu uma solução em que **nenhuma** variável vale exatamente zero e o relatório
   não traz preço-sombra. Que família de método foi usada, o que explica as duas coisas, e o que
   você pede se precisar dos preços? *(O2)*
3. Você vai resolver um modelo de programação **inteira** com milhares de nós de *branch and
   bound*, cada nó um problema linear parecido com o anterior. Qual família você escolhe, e qual é
   o argumento decisivo? *(O3)*

### Leitura executiva

O ótimo de um modelo linear mora num vértice — mas isso é um fato sobre **onde a resposta está**,
não sobre **por onde ir buscá-la**, e é essa distinção que abre espaço para os métodos de ponto
interior. Em vez de caminhar pelas quinas como o Simplex, eles partem do meio da região viável e
avançam por dentro, sem nunca encostar na fronteira; o obstáculo técnico — que perto da parede
qualquer passo na direção do gradiente sai da região — é contornado **reescalando o espaço** a cada
iteração, de modo que o ponto atual fique longe de todas as paredes e o passo encolha
automaticamente nas direções apertadas. Historicamente foram duas viradas distintas: em 1979
Khachiyan provou, com o método do elipsoide, que Programação Linear é polinomial, resultado
teórico que na prática perdia para o Simplex; em 1984 Karmarkar apresentou um algoritmo polinomial
**e** competitivo, e é dele que a família prática descende. A diferença de natureza aparece em
número: na montadora deste livro o Simplex devolve o ponto $(8,2)$ e o valor 1100 em fração exata,
com 2 pivôs, enquanto o método interior chega a $(7{,}999996;\ 2{,}000002)$ e 1099,99982 em 11
iterações — uma distância de $4{,}5 \times 10^{-6}$ ao vértice que **não é defeito**, e sim o
significado de convergir a um limite. A consequência prática é a que mais surpreende quem lê a
saída com os olhos do Simplex: como a resposta não é vértice, **não há base**, e portanto não há
leitura direta de preço-sombra nem faixa de sensibilidade — quem precisa desses relatórios precisa
da etapa de *crossover*. Quando existem múltiplos ótimos os dois métodos discordam e ambos acertam:
na marcenaria, cujo ótimo é um segmento inteiro, o Simplex devolve uma das quinas e o método
interior devolve um ponto no meio da face, valendo o mesmo 24. A escolha entre as duas famílias se
faz pela instância — problema grande, esparso e resolvido uma vez pende para o interior; a
necessidade de preços, faixas, resposta exata ou **reotimização barata** (o caso da programação
inteira, com milhares de problemas parecidos em sequência) pende para o Simplex.
