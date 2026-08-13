# 09 — O método Simplex

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-09 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Explicar** por que enumerar vértices não escala, e o que o Simplex faz em vez disso.

**O2.** **Converter** um modelo de Programação Linear (PL) para a forma padrão e **identificar**
qual vértice cada base representa.

**O3.** **Executar** uma iteração do quadro: escolher quem entra, aplicar o teste da razão para
saber quem sai, e pivotear.

**O4.** **Ler** um quadro qualquer e dizer em que ponto ele põe você, quanto vale ali, e se
aquele quadro é final.

**O5.** **Partir** de um modelo cuja origem não é viável, usando variáveis artificiais e o
*big-M*, e **reconhecer** quando a partida artificial denuncia que não existe plano.

## O problema

O capítulo anterior terminou com uma frase que era, na verdade, uma promessa: *acima de três
variáveis não há desenho; o que resta é o algoritmo*.

Só que a saída óbvia parece existir. O capítulo 08 mostrou que **o ótimo está sempre num
vértice** — então bastaria listar todos os vértices e escolher o melhor. É até o que a
[etapa 02 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-02-metodo-grafico)
faz: cruza as restrições duas a duas e tria.

Essa saída morre depressa, e dá para ver exatamente onde. Um modelo com $n$ variáveis de decisão
e $m$ restrições `≤` ganha $m$ folgas na forma padrão — ou seja, $n+m$ colunas — e uma base é uma
escolha de $m$ delas. São $\binom{n+m}{m}$ bases a examinar:

| Variáveis | Restrições | Bases a enumerar |
|---:|---:|---:|
| 2 | 2 | 6 |
| 5 | 5 | 252 |
| 10 | 10 | 184.756 |
| 20 | 20 | 137.846.528.820 |
| 50 | 50 | ≈ 1,0 × 10²⁹ |

Vinte variáveis é um modelo **pequeno** — cabe numa planilha. E já são 137 bilhões de contas.
Cinquenta por cinquenta é um exercício de sala, e o número passa de 10²⁹: mais bases do que
segundos desde o Big Bang, com folga.

> Os números da tabela são **contados**, não estimados: saem de `math.comb` no
> [experimento desta etapa](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-03-simplex).

O problema, então, não é *onde* está a resposta — isso o capítulo 08 resolveu. É **como chegar
lá sem visitar todo mundo**. É isso que o Simplex faz, e é só isso.

## De onde isto veio

Nenhum método deste livro caiu do céu. Todos foram inventados por alguém que estava preso, com
prazo, e sem ferramenta. Vale a pena saber em que aperto o Simplex nasceu — porque o aperto se
repete, com outras roupas, no problema que você vai encontrar.

### O aperto: como se planeja uma organização gigantesca

Em **junho de 1947** — um mês antes do *National Security Act*, a lei que criaria a Força Aérea
dos Estados Unidos como ramo separado — ela montou uma força-tarefa para um problema que a estava
sufocando: **planejar a si mesma**. Treinamento, suprimento, deslocamento de pessoal, tudo
encadeado, em escala continental, com recursos que acabavam.

A força-tarefa recebeu depois o nome de **Projeto SCOOP** (*Scientific Computation of Optimal
Programs*), e seu matemático-chefe era **George Dantzig**. No mesmo ano, ele enunciou
matematicamente o problema de programação linear e desenvolveu o Simplex para resolvê-lo.

Aqui vale desfazer um mal-entendido que quase todo aluno carrega, e que a tradução piorou:

> **"Programação", em Programação Linear, não tem nada a ver com computador.** *Programming*
> era, naquele contexto, **termo militar para plano ou cronograma** — programação de treinamento,
> de suprimento, de deslocamento. Programação Linear significa **planejamento linear**. O nome é
> anterior ao uso corrente da palavra em computação, e nasceu de um problema de logística, não
> de código.

Se você achava que "programação linear" era um jeito de programar, não era distração sua: o nome
é enganoso há setenta anos.

### O que se fazia antes

Planejava-se **por regras encadeadas**. Alguém decidia primeiro quantos aviões, e essa decisão
virava dado para a decisão seguinte, que virava dado para a próxima. Cada passo era defensável e
o conjunto não era ótimo coisa nenhuma — é exatamente o que o capítulo 07 mostrou quando refutou
as regras gulosas, e é o que qualquer planilha encadeada ainda faz hoje.

Dantzig fez a coisa que parece óbvia depois de feita: separou **o que é possível** do **que é
melhor**. As restrições descrevem o espaço das decisões admissíveis; uma função à parte diz qual
delas se prefere. Escrever o problema assim é meio caminho — e foi aí que ele encontrou a
parede: o modelo estava formulado e **não existia método conhecido para resolvê-lo**. O Simplex
nasceu dessa parede, no mesmo ano.

### Os nomes — e são dois

**"Programação linear" foi batizada por outra pessoa.** A expressão de Dantzig era
*"programming in a linear structure"* — programar, no sentido militar de planejar, dentro de uma
estrutura linear. Quem propôs a forma curta foi o economista **T. C. Koopmans**, numa visita que
Dantzig fez à RAND Corporation em **1948** para discutir suas ideias. Pegou, e nunca mais saiu.

**"Simplex" tampouco descreve nada de simples.** A literatura didática atribui a sugestão do nome
a **T. S. Motzkin**, numa conversa, com a explicação geométrica de que as colunas da base mais a
coluna que entra formariam um **simplex** — o triângulo generalizado para qualquer dimensão.

> ⏳ **Atribuição corrente, não confirmada em fonte primária.** A cena, o interlocutor e a
> explicação geométrica circulam juntos na literatura de ensino, e **este handbook não os
> confirmou**: a fonte que fecharia isso segue inacessível (ver a tabela de procedência abaixo).
> O parágrafo acima relata o que se conta; ele não afirma que aconteceu assim.

O que **não** depende de atribuição nenhuma, e é a parte que interessa: **o método não manipula
simplexes em lugar nenhum do procedimento**. Isso se verifica lendo o algoritmo do capítulo — o
nome, venha de onde vier, não descreve o que ele faz.

E daí sai a lição que sobrevive à dívida: **não deduza o que um método faz a partir de como ele se
chama**. Aqui as duas metades do nome do campo têm origem contada em conversa e nenhuma foi
escolhida pelo autor do método — se as duas histórias forem verdadeiras, é um caso exemplar; se
não forem, o algoritmo continua não tendo simplex nenhum dentro.

### E o *big-M*, de onde saiu?

Este capítulo vai usar um artifício com cara de truque. Ele tem origem e, mais importante, tem
uma **ideia** — e a ideia vale muito mais do que o artifício.

**O aperto era outro, e é um problema de ovo e galinha.** O Simplex precisa de um vértice para
começar. Quando todas as restrições são de recurso disponível (`≤`), a origem serve de graça: não
fazer nada é sempre viável. Mas basta uma exigência mínima — um contrato, uma especificação, uma
demanda a atender — e a origem sai da região. Aí o algoritmo que serve para achar o melhor
vértice **não consegue achar nem o primeiro**. E procurar um ponto viável qualquer é, por si só,
um problema tão difícil quanto o original.

**A virada:** se não existe ponto de partida, **invente um — e cobre caro por ele.**

Acrescente uma quantidade fictícia que faça as contas fecharem, e ponha nela um preço tão alto
que a primeira prioridade do algoritmo passe a ser se livrar dela. Se ele conseguir expulsar a
ficção, você ganhou de brinde um ponto de partida legítimo e segue o método normal. Se **não**
conseguir, a ficção que sobrou é a prova de que o problema original não tinha solução.

> **A ideia reaproveitável, que é o que fica.** *Quando um problema é difícil porque não tem
> solução fácil de encontrar, afrouxe-o até que tenha — e cobre pelo afrouxamento.* O preço faz
> duas coisas ao mesmo tempo: empurra a solução de volta para o problema verdadeiro **e**, se ela
> não voltar, denuncia que o problema verdadeiro era impossível.
>
> Esse padrão não é do Simplex. É o que está por trás das restrições flexíveis (*soft
> constraints*), da relaxação lagrangiana, dos termos de regularização em aprendizado de máquina
> e, fora da matemática, de qualquer sistema que prefira **abrir com um alarme** a travar.
> Reconhecê-lo é o que transfere; decorar "restrição `≥` pede variável artificial" não.

Há um subproduto elegante nisso, e ele costuma passar despercebido: o *big-M* faz o algoritmo
responder **uma pergunta que ninguém fez**. Você perguntou "qual é o melhor plano?"; ele
responde, de quebra, "existe algum plano?". A segunda resposta é frequentemente a mais valiosa
das duas — e é ela que aparece quando alguém vendeu o que a fábrica não pode produzir.

### O que é documentado e o que é leitura nossa

O Princípio XII da [constituição](../../.specify/memory/constitution.md) exige história com
fonte, e exige separar o que está documentado do que é interpretação. Então:

| Afirmação | Estado |
|---|---|
| Força-tarefa criada em junho de 1947, um mês antes do *National Security Act* (26/07/1947), que criou a Força Aérea como ramo separado — efetivada em 18/09/1947; nomeada depois Projeto SCOOP; Dantzig como matemático-chefe; enunciado e Simplex no mesmo ano | ✓ **fonte aberta e conferida** |
| *Programming* como termo militar para planos ou cronogramas de treinamento, suprimento logístico ou deslocamento de pessoal | ✓ **fonte aberta e conferida** |
| "Programação linear" proposto por T. C. Koopmans na RAND, 1948; a expressão de Dantzig era *programming in a linear structure* | ✓ mesma fonte |
| A. Charnes, *Optimality and Degeneracy in Linear Programming*, Econometrica 20(2), 1952 | ✓ᵐ **metadados conferidos, conteúdo não lido** — a atribuição do *big-M* a esse artigo segue corrente, não confirmada |
| O nome *simplex* sugerido por T. S. Motzkin | ⏳ **atribuição corrente**, não confirmada em fonte primária |
| **Por que a letra M** | ❌ **não encontrei fonte.** A leitura óbvia é *muito grande*, mas leitura óbvia não é documento, e este livro não preenche lacuna com suposição de cara de fato |
| A leitura de que a virada foi *separar o possível do preferível*, e o padrão "afrouxe e cobre" | 📖 **interpretação deste livro**, não afirmação histórica |

As referências completas estão na [bibliografia](../bibliografia.md).

## A intuição

Volte ao desenho da montadora, o mesmo dos dois capítulos anteriores: 10 unidades centrais de
processamento (CPU), 12 pentes de memória de 16 gigabytes (GB), lucro de R$ 100 no Tipo 1 e
R$ 150 no Tipo 2. Você já sabe a resposta —
$(8, 2)$, R$ 1.100. Esqueça que sabe.

Agora imagine que você não pode ver a figura inteira. Você está **em pé sobre um vértice**, e
só enxerga as arestas que saem dali. O que dá para fazer?

1. **Comece na origem.** Não produzir nada é sempre viável, quando todas as restrições são de
   recurso disponível. Lucro zero, mas é um lugar de onde partir.
2. **Olhe as arestas que saem daqui e escolha uma que sobe.** Da origem saem duas: uma aumenta
   $x_1$, outra aumenta $x_2$. As duas sobem.
3. **Ande por essa aresta até bater em alguma coisa.** Você não anda para sempre: mais cedo ou
   mais tarde uma restrição corta o caminho. Pare exatamente ali — e ali é outro vértice.
4. **Repita.** Quando chegar num vértice de onde **nenhuma aresta sobe**, acabou.

Esse último passo é o que faz o método valer a pena, e ele merece um parágrafo próprio, porque
é onde mora a única mágica do capítulo.

### Por que parar é seguro

Num terreno qualquer, "nenhum vizinho é mais alto" não significa "sou o mais alto do mundo" —
significa apenas que você está no topo de um morro, e pode haver uma montanha do outro lado do
vale. É o que se chama de ótimo **local**.

Na região viável de um modelo linear isso não pode acontecer, e a razão é a forma da região: ela
é **convexa** — o segmento entre dois pontos viáveis quaisquer está inteiro dentro dela. Não há
vale a atravessar, porque não há reentrância nenhuma para produzir um vale. Num terreno assim,
com uma função linear por cima, **todo ótimo local é global**.

É por isso que o Simplex pode parar com a consciência tranquila ao chegar num vértice de onde
nada sobe. Ele não "confia" que achou o melhor: a geometria garante.

> **Este é o capítulo 08 fazendo trabalho.** Quem enxergou a região viável reconhece a
> convexidade no desenho. Quem pulou aquele capítulo vai decorar um procedimento de tabela sem
> saber por que ele termina certo — e é exatamente esse aluno que trava na primeira instância
> que não sai como o exemplo do quadro.

Falta um detalhe, e é o que ocupa o resto do capítulo: **como se faz isso sem o desenho?** Como
uma máquina, que não tem olhos, sabe em que vértice está, quais arestas sobem e onde ela vai
bater? A resposta é álgebra, e ela começa por transformar todas as desigualdades em igualdades.

## A matemática — a folga vira variável

No capítulo 08, folga era o que sobrava depois de decidir: "usei 8 das 10 CPUs, folga de 2". Era
uma leitura *a posteriori*. Aqui a folga muda de estatuto: ela vira uma **variável do modelo**,
com nome próprio.

O modelo da montadora era:

$$\max\ 100x_1 + 150x_2 \quad \text{s.a.}\quad x_1 + x_2 \le 10,\quad x_1 + 2x_2 \le 12,\quad x_1, x_2 \ge 0$$

Batize de $f_1$ as CPUs que sobram e de $f_2$ os pentes que sobram. Cada desigualdade vira uma
igualdade:

$$x_1 + x_2 + f_1 = 10 \qquad x_1 + 2x_2 + f_2 = 12 \qquad x_1, x_2, f_1, f_2 \ge 0$$

Isto é a **forma padrão**: só igualdades, e todas as variáveis não-negativas. Nada se perdeu —
dizer "$x_1 + x_2 \le 10$" e dizer "$x_1 + x_2 + f_1 = 10$ com $f_1 \ge 0$" é dizer a mesma
coisa. O que se ganhou é que agora existe um **sistema linear**, e álgebra linear é coisa que se
sabe fazer sem olhos.

### O sistema tem infinitas soluções — e é isso que ajuda

Duas equações, quatro incógnitas. Um sistema assim tem infinitas soluções, o que normalmente é
má notícia. Aqui é a notícia central.

Com quatro incógnitas e duas equações, dá para **escolher duas variáveis, zerá-las, e resolver o
que sobra**. As duas que ficam valendo zero chamam-se **não-básicas**; as outras duas, que o
sistema determina, formam a **base**. O resultado é uma **solução básica** — e se todas as
variáveis saírem não-negativas, é uma **solução básica viável**.

Faça isso com a montadora, para todas as escolhas possíveis:

| Zeradas (não-básicas) | Base | Solução | Viável? | Lucro |
|---|---|---|---|---|
| $x_1, x_2$ | $f_1, f_2$ | $(0, 0)$, sobra tudo | ✅ | 0 |
| $x_1, f_1$ | $x_2, f_2$ | $(0, 10)$ | ❌ pentes: precisaria de 20 | — |
| $x_1, f_2$ | $x_2, f_1$ | $(0, 6)$ | ✅ | 900 |
| $x_2, f_1$ | $x_1, f_2$ | $(10, 0)$ | ✅ | 1.000 |
| $x_2, f_2$ | $x_1, f_1$ | $(12, 0)$ | ❌ CPUs: precisaria de 12 | — |
| $f_1, f_2$ | $x_1, x_2$ | $(8, 2)$ | ✅ | 1.100 |

Compare esta tabela com a do capítulo 08, a dos pares de retas cruzadas. **São a mesma tabela.**
Seis combinações, quatro viáveis, dois descartes — e os dois descartados são os mesmos, $(0,10)$
e $(12,0)$.

Essa coincidência não é coincidência. É o resultado que sustenta o capítulo inteiro:

> **Vértice da região viável = solução básica viável do sistema.**
>
> O que o olho chama de quina, a álgebra chama de escolha de quais variáveis zerar. São duas
> línguas para o mesmo objeto.

E aqui está o ganho: escolher quais variáveis zerar é uma operação que **não precisa de
desenho**. Funciona com duas variáveis, com cinquenta, com cinquenta mil. O Simplex, daqui em
diante, é a resposta a uma pergunta puramente algébrica: *dada uma base, qual troca de variável
me leva a uma base melhor?*

### O vocabulário, de uma vez

| Termo | O que é | No desenho do capítulo 08 |
|---|---|---|
| **Forma padrão** | Só igualdades, variáveis não-negativas | — |
| **Variável de folga** | O que sobra de um recurso, promovido a variável | A distância até a reta da restrição |
| **Base** | As variáveis que o sistema determina | — |
| **Não-básica** | Variável fixada em zero | Restrição **ativa**: você está encostado nela |
| **Solução básica viável** | Solução com todas as variáveis $\ge 0$ | Um vértice |
| **Pivoteamento** | Trocar uma variável da base por uma de fora | Andar por uma aresta até o vértice vizinho |

A linha mais útil dessa tabela é a de **não-básica**. Quando uma variável vale zero, você está
encostado em alguma parede: se é uma variável de decisão, você não produz aquele produto; se é
uma folga, aquele recurso acabou. **Estar num vértice é estar encostado em tantas paredes quantas
forem as dimensões do problema.**

## O algoritmo, passo a passo

O quadro (*tableau*) é só o sistema escrito numa tabela, com uma linha a mais embaixo para
carregar o lucro. Cada coluna é uma variável; cada linha, uma restrição; a última coluna é o
lado direito.

A linha $z$ merece uma explicação, porque é a única coisa do quadro que não é óbvia. Escreva a
função objetivo como $z - 100x_1 - 150x_2 = 0$ e ponha os coeficientes dela na última linha. O
sinal invertido incomoda no começo e existe por um motivo prático: com ele, **número negativo na
linha $z$ passa a significar "esta variável ainda pode melhorar o lucro"**. Quando não sobrar
nenhum negativo, acabou.

### Quadro 0 — a partida

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $b$ |
|---|---:|---:|---:|---:|---:|
| $f_1$ | 1 | 1 | 1 | 0 | 10 |
| $f_2$ | 1 | 2 | 0 | 1 | 12 |
| $z$ | **−100** | **−150** | 0 | 0 | 0 |

A base é $\{f_1, f_2\}$: as folgas valem 10 e 12, e as variáveis de decisão valem zero. É a
origem, $(0,0)$, com lucro zero — o passo 1 da intuição.

**Quem entra.** Há dois negativos na linha $z$. A regra ensinada aqui — chamada regra de
Dantzig — escolhe **o mais negativo**: $-150$, a coluna de $x_2$. Traduzindo: de todas as
arestas que saem deste vértice, escolha a mais íngreme.

**Quem sai — o teste da razão.** Agora a pergunta é *até onde dá para andar*. Aumentar $x_2$
consome dos dois recursos, e a primeira restrição a acabar é quem manda parar:

$$\text{linha } f_1:\ \frac{10}{1} = 10 \qquad \text{linha } f_2:\ \frac{12}{2} = 6$$

Ganha a **menor razão positiva**: 6, na linha de $f_2$. Se você insistisse em ir até 10, faria
$x_2 = 10$ e precisaria de 20 pentes tendo 12 — sairia da região viável. É o descarte $(0,10)$
da tabela acima, agora feito por conta em vez de por desenho.

> **A menor razão não é uma convenção — é a região viável se defendendo.** Qualquer razão maior
> produz um ponto que viola alguma restrição. Pegar a segunda menor "porque dá um lucro maior" é
> o erro mais comum do capítulo, e ele não gera um resultado ruim: gera um resultado **inviável**,
> que é pior, porque tem cara de resposta.

Então $x_2$ **entra** e $f_2$ **sai**. O elemento no cruzamento — o **pivô** — é o 2.

**Pivoteamento.** Divida a linha do pivô por ele (para o pivô virar 1) e subtraia múltiplos dessa
linha das demais, até zerar o resto da coluna. É eliminação de Gauss, com um alvo escolhido.

### Quadro 1 — depois de uma iteração

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $b$ |
|---|---:|---:|---:|---:|---:|
| $f_1$ | 1/2 | 0 | 1 | −1/2 | 4 |
| $x_2$ | 1/2 | 1 | 0 | 1/2 | 6 |
| $z$ | **−25** | 0 | 0 | 75 | 900 |

Leia o quadro: $x_2 = 6$, $f_1 = 4$, e tudo que não está na base vale zero — logo $x_1 = 0$. O
ponto é $(0, 6)$, com lucro 900. **É um vértice do desenho do capítulo 08**, e o lucro subiu de
0 para 900.

Ainda há um negativo: $-25$, em $x_1$. Não acabou. Entra $x_1$; razões $4 \div \tfrac12 = 8$ e
$6 \div \tfrac12 = 12$; sai $f_1$, que dá a menor. Pivô $\tfrac12$.

### Quadro 2 — o final

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $b$ |
|---|---:|---:|---:|---:|---:|
| $x_1$ | 1 | 0 | 2 | −1 | 8 |
| $x_2$ | 0 | 1 | −1 | 1 | 2 |
| $z$ | 0 | 0 | **50** | **50** | **1100** |

Nenhum negativo na linha $z$. **Pare.**

$x_1 = 8$, $x_2 = 2$, lucro 1.100. As duas folgas estão fora da base, então valem zero: os dois
recursos acabaram exatamente. É — número por número — o ponto que o desenho do capítulo 08 deu,
e o mesmo que o solver do capítulo 07 tinha devolvido sem explicar.

**Duas iterações.** Três vértices visitados dos quatro existentes, num problema em que a
enumeração examinaria seis bases. A economia parece modesta porque o problema é minúsculo; volte
à tabela do começo do capítulo e imagine a mesma proporção em 137 bilhões.

### Um brinde escondido no quadro final

Repare nos dois **50** sob $f_1$ e $f_2$. Eles não são sobra de conta: dizem quanto o lucro
subiria se você tivesse **uma unidade a mais** de cada recurso.

Dá para conferir sem teoria nenhuma — é só resolver de novo com 11 CPUs: o ótimo vai para
R$ 1.150. Com 13 pentes, idem. O experimento desta etapa faz exatamente isso, e os dois números
batem com o quadro.

Guarde a observação e siga. Ela tem nome — **preço-sombra** —, tem uma faixa de validade que
ninguém declarou ainda, e é o assunto do capítulo 12. Afirmar mais do que isto agora seria
vender uma leitura sem os avisos que ela exige.

## Por que a ganância funciona aqui

Vale parar num incômodo legítimo, e quem leu o capítulo 07 com atenção já o sentiu.

Lá, **duas regras gulosas foram refutadas**: "produza só o de maior lucro unitário" e "produza só
o de maior lucro por CPU". Ambas pareciam óbvias e ambas davam planos piores que o ótimo. E
agora, dois capítulos depois, o Simplex escolhe quem entra na base pelo **maior coeficiente** —
que é exatamente a mesma ganância.

A diferença é o que cada uma decide.

- A regra gulosa do capítulo 07 decidia **o plano inteiro, de uma vez, e parava**. Escolhia
  "só Tipo 2" e ia embora com R$ 900.
- A regra do Simplex decide **só a direção da próxima aresta**. Quanto se anda naquela direção
  não é ela quem escolhe — é o teste da razão, que é o oposto de guloso: ele para no primeiro
  recurso que acaba. E depois **o algoritmo recomeça**, num vértice novo, com uma pergunta nova.

É a diferença entre escolher um destino e escolher em que direção dar o próximo passo. A ganância
do Simplex é reversível: se a direção escolhida deixa de compensar, a variável simplesmente sai
da base numa iteração seguinte.

> **A garantia não vem da regra de entrada.** Vem da convexidade da região e do critério de
> parada: enquanto houver custo reduzido negativo, ainda há **direção de melhora** — e, num
> vértice **não degenerado**, isso significa que existe vértice melhor. Trocar a regra de Dantzig
> por outra muda **quantas** iterações o método gasta e **nunca muda o valor ótimo**.
>
> **Duas qualificações, e as duas foram medidas — não afirmadas.** (a) Em vértice **degenerado** o
> custo reduzido negativo pode não render melhora alguma: é o que permite a ciclagem que o
> [capítulo 10](10-casos-especiais.md) exibe com período 6, sem sair do ponto. (b) Trocar a regra
> **pode mudar qual plano você recebe** quando existe mais de um ótimo — aquele capítulo mede o
> caso: mesmo veredito, mesmo valor, **plano diferente**. O que a regra nunca muda é *quanto*
> vale; o *onde* ela pode mudar.

> 📌 **Dívida quitada, em 2026-08-13.** Esta página usou a convexidade **a crédito**: afirmou
> que ela sustenta a garantia e não a definiu nem a demonstrou. O
> [capítulo 38](38-convexidade.md) foi antecipado da Parte VI para pagar isso — ele mostra por
> que, num conjunto convexo com objetivo linear, ótimo local é ótimo global, e **mede** o que
> acontece quando a convexidade some: mesma região, mesmo objetivo, duas partidas, 22 e 30.

## Quando a origem não serve — o *big-M*

Tudo até aqui dependeu de uma sorte que não se repete sempre: a origem era viável. Não produzir
nada respeitava todas as restrições, e a base de folgas estava pronta.

Mude uma coisa na história. **Cinco unidades do Tipo 2 já foram vendidas** — o cliente pagou,
está em contrato. O modelo ganha uma restrição de piso:

$$x_2 \ge 5$$

Agora a origem está fora: $(0,0)$ não entrega as cinco unidades. E o algoritmo não tem de onde
partir, porque uma restrição de $\ge$ **não oferece coluna de base**. Escreva-a em forma padrão e
veja por quê: o que sobra além do necessário é o **excesso** $e_3$, e ele entra subtraindo —

$$x_2 - e_3 = 5$$

Para $e_3$ servir de base, ela teria de valer $-5$. Não pode: as variáveis são não-negativas.

### A ficção, e a multa

A saída é declaradamente artificial. Invente uma variável $a_3 \ge 0$ que **finge** entregar o
que falta:

$$x_2 - e_3 + a_3 = 5$$

Com $a_3 = 5$ o sistema fecha, e existe base. Mas $a_3$ não é nada: não é produto, não é
recurso, não é folga. É uma unidade fantasma. Uma solução com $a_3 > 0$ **não é um plano de
produção** — é uma conta que só bate porque alguém inventou mercadoria.

Por isso ela entra na função objetivo com uma multa enorme:

$$\max\ 100x_1 + 150x_2 - M a_3$$

com $M$ um número **grande o bastante para superar qualquer lucro do problema**. É o método
*big-M*, e o nome descreve a ideia inteira: a ficção é permitida na partida e cobrada tão caro
que o algoritmo trata expulsá-la como sua primeira prioridade.

> **$M$ não é um número que você escolhe.** No quadro, ele anda como símbolo: a coluna de $M$ ao
> lado da numérica, e $M$ ganha de qualquer valor concreto. É assim que
> [o código desta etapa](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-03-simplex)
> implementa — e não por preciosismo. Substituir $M$ por 10⁶ e torcer produz o erro clássico do
> *M pequeno demais*: um modelo **sem solução** devolve resposta com cara de ótima, porque
> compensou pagar a multa. Um número que precisa ser "grande o suficiente" e nunca é conferido é
> uma bomba-relógio.

### O quadro de partida

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $e_3$ | $a_3$ | $b$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| $f_1$ | 1 | 1 | 1 | 0 | 0 | 0 | 10 |
| $f_2$ | 1 | 2 | 0 | 1 | 0 | 0 | 12 |
| $a_3$ | 0 | 1 | 0 | 0 | −1 | 1 | 5 |
| $z$ | −100 | **−M − 150** | 0 | 0 | $M$ | 0 | **−5M** |

Leia o valor de $z$: $-5M$. Um prejuízo fictício e gigantesco — o preço de fingir. E veja quem é
o mais negativo da linha $z$: $-M-150$, a coluna de $x_2$, porque a parte em $M$ domina. **O
algoritmo vai atrás da ficção antes de ir atrás do lucro**, que é precisamente o que se queria.

Entra $x_2$; as razões são $10$, $6$ e $5$; sai $a_3$, com a menor. Uma iteração, e a variável
artificial já saiu da base — para nunca mais voltar.

### O quadro final

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $e_3$ | $a_3$ | $b$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| $f_1$ | 0 | 0 | 1 | −1 | −1 | 1 | 3 |
| $x_1$ | 1 | 0 | 0 | 1 | 2 | −2 | 2 |
| $x_2$ | 0 | 1 | 0 | 0 | −1 | 1 | 5 |
| $z$ | 0 | 0 | 0 | 100 | 50 | **$M$ − 50** | **950** |

Três pivôs, caminho $(0,0) \to (0,5) \to (0,6) \to (2,5)$. O plano é montar 2 do Tipo 1 e 5 do
Tipo 2, com R$ 950.

Duas leituras, e a segunda é a que importa para quem vai à reunião:

1. **O primeiro ponto do caminho não era um plano.** $(0,0)$ com $a_3 = 5$ é ficção contábil. Da
   segunda iteração em diante, todo ponto é executável.
2. **O compromisso custou R$ 150.** Era R$ 1.100 sem ele, é R$ 950 com ele. Nenhuma surpresa —
   restrição nova nunca melhora o ótimo, como o capítulo 08 já garantia. Mas agora o número tem
   nome e tamanho, e "vender antes de planejar custou R$ 150 neste mês" é uma frase que se diz na
   reunião de vendas.

### Quando a ficção não sai

Troque cinco por **oito** unidades vendidas. Oito do Tipo 2 exigiriam 16 pentes de memória, e há
12. Não existe plano.

O quadro não trava nem reclama: ele para normalmente, com a linha $z$ toda não-negativa. O que
denuncia é **quem ficou na base**: $a_3$, com valor positivo. Ou seja, o único jeito de o sistema
fechar foi manter mercadoria inventada.

> **Artificial na base com valor positivo, ao final, é o atestado de que o modelo é inviável** —
> e note o que isso quer dizer: o erro não está no algoritmo, está no **modelo**. Alguém prometeu
> ao cliente o que o estoque não sustenta. O capítulo 10 trata deste e dos outros vereditos que
> não são "aqui está seu plano".

## O código

A [etapa 03 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-03-simplex)
executa o mesmo procedimento deste capítulo, e faz três escolhas que nenhum solver de verdade
faria — todas para ser lida em vez de rápida:

- **Aritmética exata** (`Fraction`): o quadro impresso é o do caderno, `1/2` é `1/2`.
- **Guarda todos os quadros**: aqui a sequência é o produto, não o resultado final.
- ***Big-M* simbólico**: $M$ nunca vira número, pelo motivo já dito.

O que ela mede:

| Caso | Veredito | Pivôs | Caminho | Concorda com o HiGHS |
|---|---|---:|---|---|
| Montadora | ótimo, R$ 1.100 | 2 | (0,0) → (0,6) → (8,2) | ✅ |
| Com compromisso de 5 | ótimo, R$ 950 | 3 | (0,0) → (0,5) → (0,6) → (2,5) | ✅ |
| Compromisso de 8 | **inviável** | 1 | — | ✅ |

O terceiro caso é o que dá valor aos outros dois. Concordar com o solver não é chegar ao mesmo
ponto: é **dar o mesmo veredito**. Um Simplex que devolvesse um número bonito para um modelo sem
solução seria pior do que um que não rodasse.

> **Uma convenção que este capítulo usa sem ter dito, e que o exercício H cobra.** Tudo aqui
> **maximiza**. Um problema de minimizar se resolve com a mesma máquina, maximizando o negativo do
> objetivo — $\min\ c^{\top}x$ é $\max\ (-c)^{\top}x$, com o sinal do valor invertido de volta no
> fim. É o que a [etapa 08](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-08-modelagem)
> faz para resolver mistura, transporte e cobertura sem método novo. **A dívida fica declarada:**
> o tratamento próprio de minimização — inclusive o que muda no *big-M* — não está neste capítulo.

## Quando não serve

**1. O pior caso é exponencial — e dá para construí-lo.**
Existe uma família de problemas, o *cubo de Klee–Minty*, que é um cubo de $n$ dimensões levemente
entortado. Com a regra de Dantzig, o Simplex passa por **todos** os $2^n$ vértices antes de
parar. Não é folclore: o experimento desta etapa constrói o cubo e conta os pivôs.

| $n$ | Vértices do cubo | Pivôs medidos |
|---:|---:|---:|
| 2 | 4 | 3 |
| 3 | 8 | 7 |
| 4 | 16 | 15 |
| 5 | 32 | 31 |
| 6 | 64 | 63 |
| 7 | 128 | 127 |

Sempre $2^n - 1$. Na prática o Simplex quase nunca se comporta assim — mas "quase nunca" é uma
afirmação sobre as instâncias do mundo, não um teorema, e um método sem garantia de tempo tem de
declarar isso.

**2. O quadro não é o que o solver executa.** Esta implementação recalcula a tabela inteira a
cada iteração. Num modelo com milhares de restrições, quase todas com coeficiente zero, isso é
desperdício de memória e de precisão. Solvers usam a **forma revisada**, que mantém só o que
precisa e refatora — capítulo 11.

**3. Problemas muito grandes e esparsos podem preferir outra família.** Métodos de pontos
interiores atravessam a região em vez de contornar os vértices, e em certas classes de instância
ganham. Capítulo 14.

**4. Degenerescência pode travar.** Quando o teste da razão empata, o Simplex pode pivotear sem
sair do lugar e, no limite, **ciclar** — voltar a uma base já visitada e girar para sempre.

Existem regras de desempate que garantem terminação, e **esta implementação não usa nenhuma
delas**. Ela desempata pela **linha** de menor índice, o que é a escolha mais simples possível e
**não evita ciclo nenhum**: o capítulo 10 exibe a instância em que este mesmo código gira para
sempre, e mostra que trocar a regra de pivoteamento pela de Bland faz o método terminar em seis
pivôs. Capítulo 10.

**5. O modelo continua sendo linear.** Nada aqui atenua o Princípio do capítulo 07: se a
realidade tem custo fixo, ganho de escala ou decisão de sim-ou-não, a resposta do Simplex é
exata para um modelo que não é o do seu problema. Programação inteira é a Parte IV.

## Fundamentos e fontes

Este capítulo é feito de dois tipos de afirmação, e eles têm procedências diferentes.

**O que está medido aqui.** A tabela combinatória, os caminhos de vértices, os três vereditos, os
preços de R$ 50 e a curva $2^n - 1$ do cubo de Klee–Minty **não são citações**: saem do
experimento desta etapa e se regeneram rodando um script. Foi uma escolha deliberada — o pior
caso exponencial é o tipo de afirmação que normalmente se empresta de uma referência, e aqui ela
é construída, o que a torna conferível por quem não tem acesso à referência.

**O que foi conferido na fonte.** A seção *De onde isto veio* passou por verificação em fontes
abertas: SCOOP e junho de 1947, o sentido militar de *programming*, e o batismo do termo por
Koopmans em 1948. O que **não** fechou está marcado `⏳` na tabela daquela seção — a atribuição do
*big-M* e o nome *simplex* seguem como atribuição corrente, e a origem da letra M continua sem
fonte nenhuma.

### O que a literatura muda no que você faz

Este capítulo deixou uma contradição em aberto e ela precisa de resposta. A seção "quando não
serve" mostra, **medindo**, que o Simplex visita todos os $2^n$ vértices no cubo de Klee–Minty.
E a mesma seção afirma que "na prática ele quase nunca se comporta assim". Duas afirmações que
não convivem sem explicação — e a explicação está na literatura.

**1. O pior caso é real, e é adversarial.**

⏳ KLEE, V.; MINTY, G. J. "How good is the simplex algorithm?", em *Inequalities III*, 1972.
Obra citada de forma corrente e **não confirmada em fonte primária** aqui — mas a afirmação **não
depende dela**: o cubo está construído no `po-zero`, e os pivôs, contados. É a razão de o
capítulo ter medido em vez de citar.

**O que fazer diferente:** não escolha método por classe de complexidade de pior caso. O pior
caso descreve a instância **construída para derrotar a regra**, e a sua instância não foi
construída para isso.

**2. Em média, o número de pivôs é polinomial.**

✓ᵐ BORGWARDT, K. H. "The average number of pivot steps required by the Simplex-Method is
polynomial". *Zeitschrift für Operations Research*, v. 26, p. 157–177, 1982.
[DOI](https://doi.org/10.1007/bf01917108) — metadados conferidos, conteúdo não lido.

O resultado é sobre um **modelo probabilístico de instâncias**. Ele explica parte do
descompasso, e tem um limite honesto: as suas instâncias não são sorteadas de uma distribuição.

**3. A reconciliação: análise suavizada.**

✓ SPIELMAN, D. A.; TENG, S.-H. "Smoothed Analysis of Algorithms: Why the Simplex Algorithm
Usually Takes Polynomial Time". *Journal of the ACM*, v. 51, p. 385–463, 2004.
[DOI](https://doi.org/10.1145/990308.990310) · [versão aberta](https://arxiv.org/abs/cs/0111050)
— **aberta e lida**.

Os autores abrem o artigo nomeando exatamente o problema deste capítulo: a comunidade de análise
de algoritmos é desafiada pela existência de algoritmos que **cientistas e engenheiros sabem que
funcionam bem na prática, e cujas análises teóricas são negativas ou inconclusivas**.

A saída que eles propõem é medir o desempenho **esperado sob pequenas perturbações aleatórias da
entrada**, tomando o pior caso sobre as entradas — um meio-termo entre pior caso e caso médio. E
provam que, nessa medida, o Simplex tem **complexidade polinomial** no tamanho da entrada e no
desvio-padrão da perturbação.

**O que fazer diferente, e é o mais útil desta seção:** a leitura correta de Klee–Minty passa a
ser que **o pior caso do Simplex é frágil** — ele exige coeficientes ajustados com precisão, e
some quando a instância é levemente perturbada. Isso muda o que você diz numa reunião. Em vez de
"o Simplex é exponencial, então não use", o defensável é: *"o pior caso existe, é construído, e
não sobrevive a ruído; ainda assim não há garantia de tempo, e um problema grande merece medição
antes de promessa."*

### O que continua em dívida

A **comparação sistemática entre regras de pivoteamento** — Dantzig, Bland, maior melhoria,
*steepest edge* — não foi levantada. É o que decidiria qual regra ensinar como padrão, e o
capítulo hoje ensina a de Dantzig por ser a que a sala pratica, não por evidência comparativa.
Entra na fila do [Radar](../../radar/RADAR.md).

## Pratique

<div data-bateria="cap09"></div>

Oito exercícios, em quatro blocos que seguem os objetivos:

| Exercícios | O que treinam | Objetivo |
|---|---|---|
| A, B | Por que não enumerar; da desigualdade ao quadro de partida | O1, O2 |
| C, D, E | A **mecânica**: quem entra, quem sai, pivotear | O3 |
| F, G | **Leitura**: dado um quadro, onde você está e se acabou | O4 |
| H | *Big-M* e o veredito de inviabilidade | O5 |

Um aviso sobre três deles — E, G e H. Neles a resposta certa é alguma forma de *"a conta está
certa e a conclusão está errada"*, que é o modo mais traiçoeiro de errar em Programação Linear,
porque não deixa rastro numérico. Executar o procedimento é metade da habilidade; perceber que
ele foi bem executado e mal interpretado é a outra — e é essa que a prova costuma cobrar sem
avisar.

## Assista

**[Pesquisa Operacional I — Aula 7: Algoritmo Simplex](https://www.youtube.com/watch?v=qf1mAyDv61E)** · [UNIVESP](https://www.youtube.com/@univesptv) · 18min48s

**O que ele resolve:** o pivoteamento é uma dessas coisas que se entendem melhor vendo a mão de
alguém escrever. O texto mostra o quadro antes e o quadro depois; o vídeo mostra a **passagem** —
que linha foi dividida por quê, que múltiplo foi subtraído de qual. É a diferença entre ver duas
fotos e ver o movimento.

> ✓ **Ficha conferida na fonte** em 2026-08-09: autor, canal, duração e data de publicação. O
> vídeo entra por link e crédito, com o player de origem — ver a política na
> [Videoteca](../videoteca.md). O que **não** foi conferido é o conteúdo: a frase "o que ele
> resolve" é leitura do editor a partir do título e da posição na série, e ninguém assistiu.

## Síntese — o que levar

- **O método nasceu de um aperto de logística, não de um problema de matemática.** Planejar a
  Força Aérea, em 1947, sem método. E "programação" ali quer dizer **plano**, não código.
- **A virada foi separar o possível do preferível:** restrições dizem o que cabe, uma função à
  parte diz o que se prefere. Antes disso, planejava-se por regras encadeadas.
- **O *big-M* é uma ideia, não um truque:** *quando não há ponto de partida, invente um e cobre
  caro por ele.* O preço empurra a solução de volta ao problema verdadeiro — e, se ela não
  voltar, prova que o problema era impossível.
- **Enumerar vértices não escala:** $\binom{n+m}{m}$ cresce absurdamente. 20×20 já são 137 bilhões
  de bases.
- **O Simplex anda de vértice em vértice, sempre subindo**, e para quando nenhuma aresta sobe.
- **Parar é seguro porque a região é convexa:** não há vale a atravessar, então ótimo local é
  ótimo global. É a geometria do capítulo 08 fazendo trabalho de garantia.
- **A folga vira variável**, a desigualdade vira igualdade, e escolher quais variáveis zerar passa
  a ser escolher um vértice — **sem desenho**.
- **Vértice = solução básica viável.** É a ponte do capítulo, e é a mesma tabela do método
  gráfico escrita em outra língua.
- **Quem entra é o mais negativo da linha $z$; quem sai é a menor razão positiva.** A menor razão
  não é convenção: é a viabilidade se defendendo.
- **A ganância do Simplex é diferente da que o capítulo 07 refutou:** ela escolhe só a direção do
  próximo passo, não o plano inteiro — e o processo itera.
- **Sem origem viável, entra a ficção com multa:** variável artificial e *big-M*. $M$ é símbolo,
  não número.
- **Artificial que sobra na base é atestado de modelo inviável** — e o defeito está no modelo,
  não no algoritmo.
- **A linha $z$ final já contém o valor de uma unidade a mais de cada recurso.** Tem nome, tem
  faixa de validade, e é o capítulo 12.

## Verificação

1. Um colega diz que o Simplex dele "achou o melhor vértice da vizinhança, mas pode haver um
   melhor do outro lado da região". Onde está o mal-entendido, e que propriedade da região você
   usaria para respondê-lo? *(O1)*
2. Num quadro qualquer, você vê a variável $f_2$ **fora** da base e $x_1$ **dentro**, valendo 8.
   Diga, sem contas, duas coisas sobre a situação da fábrica nesse ponto. *(O2, O4)*
3. Ao final de um *big-M*, a linha $z$ está toda não-negativa e uma variável artificial aparece na
   base valendo 3. Um estagiário conclui que o lucro ótimo é o valor que está no canto do quadro.
   O que você responde, e qual é o próximo lugar a investigar? *(O5)*

### Leitura executiva

O método gráfico responde onde está o ótimo, mas só existe em duas dimensões; e a alternativa
óbvia — listar todos os vértices — morre na combinatória, porque um modelo com 20 variáveis e 20
restrições já tem 137 bilhões de bases. O Simplex resolve isso andando de vértice em vértice
sempre para cima, e parando quando nenhuma aresta sobe; essa parada é segura porque a região
viável é convexa, e num terreno sem vales todo ótimo local é global. Para andar sem enxergar, o
modelo é posto em forma padrão: cada folga vira variável e cada desigualdade vira igualdade, de
modo que escolher um vértice passa a ser escolher quais variáveis zerar — **vértice é solução
básica viável**. No quadro, entra quem tem o coeficiente mais negativo na linha $z$ e sai quem der
a menor razão positiva, que é a primeira restrição a acabar; a ganância da entrada é inofensiva
porque decide apenas a direção do próximo passo, e o teste da razão decide o tamanho. Na montadora
o método chega a (8, 2) e R$ 1.100 em duas iterações, pisando exatamente nos vértices que o
desenho do capítulo 08 tinha mostrado. Quando a origem não é viável — um contrato de cinco
unidades já vendidas, por exemplo — entra uma variável artificial com multa *big-M*, que o
algoritmo expulsa na primeira iteração; o plano vira (2, 5) e R$ 950, e a diferença de R$ 150 é o
preço do compromisso. Se a artificial não sai da base, não há erro de conta: não existe plano, e o
que precisa ser revisto é o modelo.
