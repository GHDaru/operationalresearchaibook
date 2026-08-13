# 12 — Dualidade

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Escrever** o dual de um modelo primal e **dizer o que cada variável dual significa** no
problema — em unidade, em sinal e em frase que um gerente entenda.

**O2.** **Diagnosticar** uma decisão tomada a partir de um preço-sombra lido **fora da faixa em
que ele vale**, e calcular o prejuízo do erro.

**O3.** **Julgar** uma proposta de negócio construída sobre um preço-sombra, e dizer sob que
condições ela deixa de se sustentar.

## O problema

Sexta-feira, 16h. A montadora dos capítulos 07 a 10 já tem o plano do mês: **8 computadores do
Tipo 1 e 2 do Tipo 2**, lucro de **R$ 1.100**. O quadro final está na mesa, e é aquele:

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $b$ |
|---|---:|---:|---:|---:|---:|
| $x_1$ | 1 | 0 | 2 | −1 | 8 |
| $x_2$ | 0 | 1 | −1 | 1 | 2 |
| $z$ | 0 | 0 | **50** | **50** | **1100** |

O telefone toca. Um fornecedor tem **CPUs sobrando** e oferece o lote a **R$ 45 a unidade**.
Quantas você compra?

A pergunta parece de compras e é de modelagem. Repare no que ela exige: não é "qual é o meu
plano?" — isso o capítulo 09 respondeu. É **"quanto vale, para mim, uma unidade a mais de um
recurso que já acabou?"**. O modelo que você escreveu não tem essa variável. Ninguém a declarou.

E, no entanto, a resposta está no quadro acima, escrita em dois lugares que você aprendeu a
ignorar: os dois **50** da linha $z$, debaixo das colunas de folga.

O erro caro deste capítulo tem forma fixa, e ele custa dinheiro de verdade:

> Alguém lê "a CPU vale 50", vê o preço de 45 no telefone, calcula **R$ 5 de ganho por unidade** e
> compra o lote inteiro. **Está errado**, e o próprio quadro dizia por quê — só que essa parte
> ninguém tinha ensinado a ler.

Quanto custa o erro está medido na seção [Quando não serve](#quando-não-serve). Adianto o número
para você ler o resto do capítulo com ele na cabeça: comprar **10** CPUs a R$ 45 nessa montadora
**dá prejuízo de R$ 350**.

## De onde isto veio

### O aperto: o exército queria o plano, e a economia queria o preço

Programação Linear nasce em 1947 dentro de um problema de logística militar — planejar, não
precificar. Mas a pergunta do preço aparece imediatamente, e por um motivo prosaico: quem aprova
orçamento não quer saber **qual é o plano**, quer saber **quanto vale afrouxar uma restrição**.
Um plano ótimo que não responde "e se eu conseguir mais uma tonelada de aço?" resolve metade do
problema de quem paga a conta.

Havia ainda uma pressão teórica. A **teoria dos jogos** já tinha, desde antes, um resultado com
exatamente a mesma forma — o ***minimax***, em que **dois problemas opostos têm o mesmo valor**: o
que o maximizador garante é precisamente o que o minimizador não consegue impedir. A forma daquele
resultado e a forma do que se procurava em Programação Linear são a mesma forma, e é essa
semelhança que orienta a busca.

> ⏳ **Data e autoria em dívida.** A literatura atribui o *minimax* a von Neumann, em 1928. **Este
> handbook não confirmou o identificador nesta rodada**, então a atribuição fica registrada como
> corrente e o parágrafo acima se apoia na **forma** do resultado, que é o que importa aqui — não
> na data nem no nome.

### O que se fazia antes

Antes, o valor de um recurso se estimava **rodando o modelo de novo**. Você acrescenta uma
unidade ao estoque, resolve outra vez, compara os dois lucros e chama a diferença de valor. Isso
funciona, e tem dois defeitos: custa uma execução por pergunta, e **não avisa quando a resposta
deixa de valer** — que é exatamente onde o dinheiro se perde.

### A virada: o segundo problema já estava dentro do primeiro

A virada é reconhecer que todo problema de Programação Linear carrega um **problema irmão**, com
uma variável para cada restrição do original, e que os dois têm o **mesmo valor ótimo**. Resolver
um é resolver o outro. Você não precisa rodar de novo: os preços estão no quadro que você já tem.

Deixe de lado por um instante que isso é um teorema, e olhe para o que ele afirma: *o plano e os
preços são a mesma informação, vista por lados opostos da mesa*.

### O nome, e o que este handbook não afirma

**"Dual"** é o vocabulário da matemática para "o par oposto de", e a palavra chega à Programação
Linear já pronta desse uso. **A origem exata do batismo neste campo não foi localizada por fonte
primária nesta rodada** — e, pela regra desta casa, o que não se localiza fica dito como dívida,
não como história.

O mesmo vale para a cena mais contada da área:

> ⏳ **Atribuição corrente, não confirmada aqui.** A literatura didática relata que, num encontro
> em 1947, **von Neumann** teria apontado a **Dantzig** que Programação Linear e jogos de soma
> zero são o mesmo objeto, esboçando a dualidade na hora. É uma boa história e pode ser
> verdadeira. **Este handbook não a afirma**: as buscas por identificador nesta rodada não
> localizaram a fonte primária (as consultas por "von Neumann duality" devolvem *álgebras* de von
> Neumann, que é outro campo inteiro). Registrado no
> [estudo 004](https://github.com/GHDaru/operationalresearchaibook/blob/main/estudos/004-historia-parte-II.md).

O que **está** documentado por identificador é o trabalho de **Gale, Kuhn e Tucker (1951)**, que
é o trio canônico da dualidade em Programação Linear — ver a
[Procedência](#procedência) ao fim desta seção.

### A ideia reaproveitável

> **Toda restrição tem um preço, e o preço só é notícia quando a restrição está apertada.**

Isto sai da Pesquisa Operacional inteiro. Numa fábrica, numa equipe, num orçamento: o recurso que
**sobra** vale zero na margem — comprar mais dele não muda nada. O recurso que **acabou** vale
exatamente o quanto o resultado melhora se aparecer mais um. E é por isso que "onde está o
gargalo?" e "onde vale a pena investir?" são a mesma pergunta, feita duas vezes.

O corolário incomoda, e é o mais útil: **investir no que não é gargalo é gastar dinheiro para não
mudar nada** — e o quadro te dizia isso de graça.

### Procedência

| Afirmação | Estado |
|---|---|
| Gale, Kuhn e Tucker publicam sobre dualidade e jogos simétricos, 1951 | ✓ᵐ metadados conferidos no registro — [bibliografia](../bibliografia.md) |
| von Neumann publica o teorema *minimax* em 1928 | ⏳ atribuição corrente; sem identificador conferido nesta rodada |
| A cena von Neumann → Dantzig, 1947 | ⏳ **não afirmada** — procurada e não localizada |
| A origem do nome "dual" neste campo | ❌ procurada, não encontrada |
| Programação Linear nasce em contexto de logística militar, 1947 | ✓ᵐ herdado do [capítulo 09](09-simplex.md) |

## A intuição — duas perguntas, uma resposta

Ponha duas pessoas na mesa.

**A gerente de produção** olha para o estoque e pergunta: *"com o que eu tenho, qual é o maior
lucro que eu consigo montar?"* Ela escolhe **quantidades**: quantos do Tipo 1, quantos do Tipo 2.

**O comprador** olha para o mesmo estoque e pergunta outra coisa: *"por quanto eu venderia esse
estoque inteiro, em vez de produzir?"* Ele escolhe **preços**: quanto pela CPU, quanto pelo pente.

O comprador não pode chutar preço baixo: se ele avaliar o estoque abaixo do que a produção rende,
a gerente recusa — vale mais montar. Então ele precisa que **cada produto**, avaliado pelos seus
componentes, custe **pelo menos** o lucro que aquele produto daria. Sujeito a isso, ele quer
pagar **o mínimo possível**.

Um maximiza escolhendo quantidades. O outro minimiza escolhendo preços. E aqui está o teorema,
antes de virar fórmula:

> **Os dois chegam ao mesmo número.** Não é acaso nem aproximação: no ótimo, o maior lucro que a
> produção consegue e o menor valor pelo qual o estoque se vende são **o mesmo valor**.

Se fossem diferentes, alguém estaria deixando dinheiro na mesa — e o método acharia como pegá-lo.

## A matemática

### A notação

| Símbolo | O que é | Unidade, no exemplo |
|---|---|---|
| $x_j$ | quanto produzir do produto $j$ | unidades |
| $c_j$ | lucro unitário do produto $j$ | R$/unidade |
| $b_i$ | estoque do recurso $i$ | unidades do componente |
| $a_{ij}$ | quanto do recurso $i$ cada unidade de $j$ consome | componente/unidade |
| $y_i$ | **preço do recurso $i$** — a variável dual | **R$/componente** |

A linha que mais importa é a última. $y_i$ **não** é "um número auxiliar do algoritmo": é um
preço, com unidade, e a unidade é a do lucro dividida pela do recurso.

### O par

O primal da montadora, como o capítulo 07 o escreveu:

$$\max\ 100x_1 + 150x_2 \quad \text{s.a.}\quad x_1 + x_2 \le 10,\quad x_1 + 2x_2 \le 12,\quad x_1, x_2 \ge 0$$

O dual dele:

$$\min\ 10y_1 + 12y_2 \quad \text{s.a.}\quad y_1 + y_2 \ge 100,\quad y_1 + 2y_2 \ge 150,\quad y_1, y_2 \ge 0$$

Leia o dual em português, restrição por restrição. A primeira diz: *"o Tipo 1 consome uma CPU e um
pente; a soma desses dois preços tem de ser pelo menos os R$ 100 que ele rende"*. A segunda diz o
mesmo do Tipo 2, que consome uma CPU e **dois** pentes. E o objetivo diz: *"pague o mínimo pelo
estoque inteiro — 10 CPUs e 12 pentes"*.

### A receita, em quatro trocas

| No primal | Vira, no dual |
|---|---|
| $\max\ c^{\top}x$ | $\min\ b^{\top}y$ |
| uma **restrição** $i$ | uma **variável** $y_i$ |
| uma **variável** $j$ | uma **restrição** $j$ |
| $Ax \le b$, $x \ge 0$ | $A^{\top}y \ge c$, $y \ge 0$ |

A matriz **transpõe**: a coluna do produto vira a linha do preço. É a mesma tabela lida por
colunas em vez de linhas — o que é, no fundo, a razão de o teorema existir.

### Os dois teoremas, e o que cada um autoriza

**Dualidade fraca.** Qualquer $y$ viável no dual dá um valor **maior ou igual** a qualquer $x$
viável no primal. Consequência prática: **um dual viável é um certificado**. Se você tem um plano
que rende 1.100 e um conjunto de preços viável que custa 1.100, acabou — não existe plano melhor,
e você não precisa procurar.

**Dualidade forte.** Se o primal tem ótimo finito, o dual também tem, e **os dois valores são
iguais**.

$$c^{\top}x^{*} = b^{\top}y^{*}$$

Isto não é afirmação de autoridade neste handbook: está **conferido por execução**, resolvendo os
dois problemas separadamente. Ver [O código](#o-código).

### Folgas complementares — o teorema que vira faro

O terceiro resultado é o mais útil no dia a dia, e cabe numa frase:

> **Recurso que sobra tem preço zero. Preço positivo só em recurso que acabou.**

Formalmente, no ótimo, para cada recurso $i$: ou a folga $f_i$ é zero (o recurso acabou), ou o
preço $y_i$ é zero (ele não vale nada na margem). Nunca os dois positivos ao mesmo tempo.

$$y_i \cdot f_i = 0 \quad \text{para todo } i$$

Use isto como **teste de sanidade**: se alguém te mostrar um relatório com sobra de matéria-prima
**e** preço-sombra positivo para ela, o relatório está errado, ou não é do modelo que você acha
que é. Você acabou de auditar um número sem refazer conta nenhuma.

## O algoritmo — o preço já está no seu quadro

Não há método novo neste capítulo. Há uma **leitura nova do quadro que você já sabe montar**.

Volte ao quadro final da montadora. A linha $z$, sob as colunas de **folga**:

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $b$ |
|---|---:|---:|---:|---:|---:|
| $x_1$ | 1 | 0 | 2 | −1 | 8 |
| $x_2$ | 0 | 1 | −1 | 1 | 2 |
| $z$ | 0 | 0 | **50** | **50** | **1100** |

**O custo reduzido da folga da restrição $i$ é o preço-sombra da restrição $i$.** Sob $f_1$ (a
folga das CPUs) está 50; sob $f_2$ (a folga dos pentes) está 50. Logo:

$$y_1 = 50 \ \text{R\$/CPU} \qquad y_2 = 50 \ \text{R\$/pente de 16 GB}$$

E a conferência que fecha: $10 \times 50 + 12 \times 50 = 1100$ — o mesmo lucro do plano. **É a
dualidade forte aparecendo no seu quadro**, sem você ter resolvido nada de novo.

### Ler não basta: a conferência independente

Ler o preço no quadro do primal é conveniente e **circular** — usa o mesmo cálculo para produzir e
para conferir. Por isso o experimento deste capítulo faz a coisa mais chata possível: **monta o
dual como um problema separado** e o resolve do zero, com as restrições $\ge$ entrando por
*big-M*, a máquina do capítulo 09.

Resultado da execução: $y = (50, 50)$, valor **1.100**, em **2 pivôs**. O mesmo número, por dois
caminhos que não se falam. Se divergissem, o erro seria deste capítulo, e ele não poderia ser
escrito.

### Até onde o preço vale

Aqui está a metade que quase ninguém ensina junto, e é a metade cara. O preço de 50 por CPU **não
vale para sempre**. Ele vale enquanto o plano continuar apoiado nas **mesmas** restrições — a
mesma base. Medido:

| Recurso | Estoque hoje | Faixa em que o preço de R$ 50 vale |
|---|---:|---|
| CPUs | 10 | de **6** a **12** |
| pentes de 16 GB | 12 | de **10** a **20** |

Leia a primeira linha com atenção, porque ela é a resposta ao telefonema: **acima de 12 CPUs, a
CPU seguinte vale zero**. Não "vale um pouco menos" — vale **zero**, porque a partir dali o
gargalo passou a ser outro, e comprar mais CPU não muda plano nenhum.

Como usar a faixa é o [capítulo 13](../mapa-do-handbook.md). O que este capítulo exige de você é
mais simples e mais urgente: **nunca cite um preço-sombra sem citar a faixa junto**.

## O código

A [etapa 05 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-05-parte2)
regenera **todos** os números deste capítulo, em aritmética exata:

```
instância: Montadora — último dia do mês, MRP inverso
primal   : ponto ['8', '2']  valor 1100
preços   : {'CPUs': '50', 'pentes de memória de 16 GB': '50'}
dual     : y = ['50', '50']  valor 1100  (2 pivôs)
dualidade forte confere: True

  CPUs: hoje 10 · faixa [6, 12]
  pentes de memória de 16 GB: hoje 12 · faixa [10, 20]
faixas conferidas por caminho independente: True
```

Três coisas que o script faz de propósito:

1. **Lê a instância do arquivo**, nunca redigita os números — a montadora muda num lugar só.
2. **Resolve o dual como problema próprio**, e compara em **fração**, não em texto: `"1100"` e
   `"1100/1"` são o mesmo número e textos diferentes, e a comparação errada daria falso negativo
   justo na única verificação que a etapa existe para fazer.
3. **Encerra com erro se a dualidade forte não conferir.** O capítulo não pode ser publicado com o
   experimento vermelho.

## Quando não serve

**1. O preço-sombra é marginal, e "marginal" quer dizer *a próxima unidade*.** Ele não é o preço
justo do recurso nem o preço de mercado. Fora da faixa medida, ele simplesmente deixa de valer.

**2. Em vértice degenerado o preço é ambíguo.** O [capítulo 10](10-casos-especiais.md) mostrou
que, com uma básica valendo zero, mais de um conjunto de preços sustenta o mesmo ótimo — e o que
você lê no quadro depende de qual base o método parou. Nesse caso, **o número que sai do relatório
não é *o* preço**: é *um* dos preços válidos.

**3. Dualidade forte exige ótimo finito.** Se o primal é inviável, o dual é ilimitado ou inviável;
se o primal é ilimitado, o dual é inviável. Ler preço de um modelo que não tem plano é ler ruído.

**4. Isto é Programação Linear.** Em programação **inteira** não existe preço-sombra com essa
garantia: a relaxação linear dá um número, e ele **não** é o valor de uma unidade a mais do
recurso no problema inteiro. Quem carrega a intuição deste capítulo para lá erra, e erra com
confiança.

**5. O modelo é de um período e vende tudo que produz** — está na ficha da instância. Um preço-
sombra tirado dele não autoriza contrato de doze meses. O que ele autoriza é uma compra, agora,
dentro da faixa.

### O erro do telefonema, medido

Volte à sexta-feira, 16h. CPUs a R$ 45, e o quadro diz que a CPU vale 50.

| | Cálculo | Resultado |
|---|---|---|
| **O que o reflexo diz** | 10 CPUs × (50 − 45) | ganho de **R$ 50** |
| **O que acontece** | o estoque vai de 10 para 20 CPUs; o novo ótimo é (12, 0), lucro **R$ 1.200** | ganho real de **R$ 100** |
| **O custo** | 10 × R$ 45 | **R$ 450** |
| **Resultado** | 100 − 450 | **prejuízo de R$ 350** |

Só as **2 primeiras** CPUs valiam 50 — as outras 8 valiam zero, porque a faixa acabava em 12. A
compra certa era **2 unidades**: ganho de R$ 100 por um custo de R$ 90.

E note o que produziu o erro: **nenhuma conta errada**. O 50 estava certo, a subtração estava
certa, a multiplicação estava certa. O que faltou foi a faixa — a informação que o mesmo
experimento produz e que quase nenhum relatório publica ao lado do número.

## Fundamentos e fontes

**O que está medido aqui.** Os preços (50 e 50), o valor dual (1.100), os 2 pivôs, as duas faixas
de validade e os números do telefonema saem todos da etapa 05 do `po-zero` e se regeneram rodando
um script.

**O que foi conferido no registro, e não lido.** ✓ᵐ **GALE, D.; KUHN, H. W.; TUCKER, A. W.** "On
symmetric games", 1951 — metadados e existência conferidos; o **conteúdo não foi aberto**, e por
isso nenhuma afirmação deste capítulo se apoia nele além da atribuição do trio.

**O que continua em dívida**, com o motivo: a cena von Neumann → Dantzig de 1947, e a origem do
nome "dual" neste campo. As duas foram procuradas por identificador nesta rodada e não
localizadas; nenhuma via de acesso aberto devolveu texto para os artigos candidatos. Ver a
[bibliografia](../bibliografia.md) e o [Radar](../../radar/RADAR.md).

> 🟡 **Este capítulo está em v0.** O esqueleto está completo e todo número tem experimento que o
> regenera, mas ele **ainda não passou por revisão independente em contexto fresco**. O selo no
> alto da página diz isso, e ele muda quando a revisão acontecer.

## Pratique

<div data-bateria="cap12"></div>

Três exercícios, e nenhum deles pede para você resolver um modelo do zero. O primeiro pede para
**escrever o dual e dizer o que os preços significam**; o segundo dá um erro que já rodou e pede o
**diagnóstico com o prejuízo calculado**; o terceiro põe você do lado de quem decide.

## Assista

**[Interpretação Econômica, Dualidade, Dual, Programação Linear, Otimização, Pesquisa
Operacional](https://www.youtube.com/watch?v=HYKllgOuMzA)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 12min44s

**O que ele resolve:** este capítulo chega ao preço-sombra pela leitura do quadro final, que é o
caminho de quem já montou o Simplex à mão. O vídeo faz o percurso econômico — parte da
interpretação do dual como avaliação de recursos e volta para a formulação. É a segunda passada
que fixa a *unidade* de $y_i$, que é onde a maioria dos erros começa.

## Síntese — o que levar

- **Todo modelo carrega um irmão.** Uma variável dual por restrição primal, e resolver um é
  resolver o outro.
- **A variável dual é um preço, com unidade** — reais por CPU, reais por hora, reais por
  tonelada. Se você não sabe dizer a unidade, não entendeu o número.
- **Dualidade forte:** no ótimo, os dois valores são iguais. Aqui isso foi **conferido por
  execução independente**, não afirmado.
- **Dualidade fraca dá certificado:** um dual viável com o mesmo valor prova que o plano é ótimo,
  sem procurar mais.
- **Folgas complementares:** recurso que sobra vale zero; preço positivo só onde a restrição
  aperta. Serve como auditoria instantânea de relatório.
- **O preço está no quadro que você já tem** — é o custo reduzido da coluna de folga.
- **Preço-sombra sem faixa de validade é uma armadilha**, e a armadilha tem preço: R$ 350 de
  prejuízo no exemplo deste capítulo, sem nenhuma conta errada.
- **Fora da Pesquisa Operacional:** investir onde não há gargalo é gastar para não mudar nada.

## Verificação

1. Uma fábrica tem três restrições e o relatório informa preço-sombra positivo para uma
   matéria-prima que **sobrou** no plano. Sem refazer conta alguma, o que você afirma sobre esse
   relatório, e com base em qual resultado? *(O1)*
2. Um analista apresenta "a CPU vale R$ 50" e propõe comprar 10 unidades a R$ 45. Que **única
   pergunta** você faz antes de aprovar, e o que muda na decisão conforme a resposta? *(O2)*
3. Um fornecedor oferece um contrato de 12 meses ao preço exato do preço-sombra de hoje. Liste as
   duas condições do modelo que precisariam ser verdadeiras para esse contrato fazer sentido — e
   diga se elas são verdadeiras na instância deste capítulo. *(O3)*

### Leitura executiva

Todo problema de Programação Linear tem um problema irmão, o **dual**, com uma variável para cada
restrição do original. Enquanto o primal escolhe **quantidades** para maximizar lucro, o dual
escolhe **preços** para os recursos, minimizando o valor pelo qual o estoque inteiro seria
vendido. Os dois chegam ao mesmo número — é a **dualidade forte**, e neste handbook ela não foi
afirmada: os dois problemas foram resolvidos separadamente e ambos deram R$ 1.100. A consequência
prática é que **o preço de cada recurso já está no quadro final que o Simplex produziu**, como
custo reduzido da coluna de folga: na montadora, R$ 50 por CPU e R$ 50 por pente de 16 GB. Um
terceiro resultado, as **folgas complementares**, diz que recurso que sobra tem preço zero e preço
positivo só existe onde a restrição aperta — o que transforma "onde está o gargalo?" e "onde vale
investir?" na mesma pergunta, e permite auditar um relatório sem refazer conta. O perigo mora na
metade que raramente é publicada junto: o preço é **marginal e tem faixa de validade**. Na
montadora, os R$ 50 por CPU valem entre 6 e 12 unidades de estoque; acima de 12, a CPU seguinte
vale **zero**. Um comprador que lesse o número sem a faixa e adquirisse 10 CPUs a R$ 45 teria
prejuízo de R$ 350 — com todas as contas certas. Daí a regra que fica: **nunca cite um preço-sombra
sem citar a faixa junto**, e lembre que nada disto vale em programação inteira, onde a relaxação
linear devolve um número que não é o valor de uma unidade a mais do recurso.
