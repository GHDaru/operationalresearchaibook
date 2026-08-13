# 04 — Classificação de problemas e escolha de método

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Classificar** um problema descrito em português nos quatro eixos — linear ou não,
contínuo ou inteiro, determinístico ou incerto, convexo ou não — e dizer o que **ainda não dá**
para classificar.

**O2.** **Prever a consequência** de cada travessia de eixo: o que se ganha, o que se perde, e
sobretudo **qual garantia deixa de valer**.

**O3.** **Escolher** entre resolver ao ótimo e parar antes, com critério declarado, e dizer o que
a escolha autoriza prometer.

## O problema

Classificação parece a parte chata do assunto — a tabela que se decora e não se usa. Ela é o
oposto disso, e por um motivo específico:

> **A classe do problema decide o que você pode prometer.** Não quanto tempo vai levar: **o que a
> palavra `Optimal` na saída vai significar quando aparecer.**

O leitor que chega aqui já sabe formular ([capítulo 03](03-anatomia-do-modelo.md)) e sabe que três
das quatro peças erram em silêncio. Este capítulo trata do silêncio que vem **depois**: o solver
respondeu, a palavra `Optimal` está na tela, e a pergunta é se ela significa *"esta é a melhor
solução"* ou apenas *"não achei nada melhor por aqui"*.

O erro caro deste capítulo:

> Alguém apresenta um resultado dizendo "o modelo encontrou a solução ótima" para um problema **não
> convexo**, resolvido por um método que não produz limitante. O procedimento não errou nada — ele
> parou onde não havia vizinho melhor, e não emitiu erro, aviso nem bandeira. A **frase** é que está
> errada, e este handbook mediu a diferença: mesma região, mesmo objetivo, duas partidas,
> **22 contra 30** ([capítulo 38](38-convexidade.md)).

## De onde isto veio

### O aperto: o método vinha antes da classe, e o nome denunciou isso

A classificação não nasceu como taxonomia. Nasceu **para trás**, a partir dos métodos: alguém
descobria como resolver uma família de problemas, e a família ganhava nome depois — o nome da
**estrutura que o método exigia**.

O caso fundador está no próprio nome deste campo. Dantzig chamava o que fazia de *programming in
a linear structure* — programar dentro de uma estrutura linear. Foi **T. C. Koopmans**, na RAND,
em 1948, quem propôs encurtar para *linear programming*. O adjetivo *linear* no nome não é
descrição de conveniência: é a **condição que o Simplex precisa** para funcionar, promovida a
nome da classe.

> Vale desfazer aqui o mal-entendido que o nome carrega até hoje: *programming*, em 1947, queria
> dizer **plano ou cronograma** — no sentido militar de programar suprimento, treinamento e
> deslocamento de pessoal. Não tinha nada a ver com programar computadores, que mal existiam.

### O que se fazia antes, e a virada

Antes das travessias, havia uma classe e um método. A virada foi descobrir que **acrescentar uma
exigência aparentemente pequena pode mudar tudo** — e a exigência que ensinou isso foi a
integralidade.

*"As variáveis têm que ser inteiras"* soa como um detalhe de arredondamento. Não é. A região
viável deixa de ser um poliedro contínuo e vira uma nuvem de pontos, e o teorema que garante o
ótimo numa quina — o do [capítulo 08](08-geometria.md) — deixa de se aplicar. Foi preciso inventar
maquinaria nova, e a literatura credita duas viradas: a **Ralph Gomory**, em 1958, os cortes que
apertam a região sem descartar ponto inteiro nenhum; e a **Ailsa Land e Alison Doig**, em 1960, a
busca que divide o problema e poda ramos por limitante — o que hoje se chama *branch-and-bound*.

> **As duas são atribuições correntes, e este handbook as apresenta como tais.** Os dois artigos
> existem e foram conferidos por metadados — autor, veículo, ano e página. O **conteúdo não foi
> lido**, então nada aqui afirma o que está escrito dentro deles.

### A ideia reaproveitável

> **Antes de escolher a ferramenta, descubra em que classe você está — porque a classe decide o
> que a resposta significa, e não só quanto ela custa.**

Vale muito além da otimização. É a mesma disciplina de perguntar, diante de qualquer resultado
computacional, *"que garantia este procedimento oferece?"* antes de perguntar *"quanto ele
demorou?"*.

### Procedência

| Afirmação | Estado |
|---|---|
| *Programming* no sentido militar de plano/cronograma; a expressão *programming in a linear structure*; o batismo de *linear programming* por Koopmans, na RAND, em 1948 | ✓ **lida** — MacTutor, University of St Andrews (ver [bibliografia](../bibliografia.md)) |
| Gomory (1958) e os cortes para soluções inteiras | ✓ᵐ **metadados conferidos** no Crossref; o texto **não foi lido** |
| Land e Doig (1960) e o método automático para problemas discretos | ✓ᵐ **metadados conferidos** no Crossref; o texto **não foi lido** |
| Que a classificação em eixos, tal como organizada nesta página, seja o recorte canônico do campo | 📖 **leitura editorial** — os livros-texto da bibliografia organizam o mesmo material em ordens diferentes |
| Os números 22 e 30 | ✓ **medidos** no `po-zero`, etapa 06, com teste que compara o texto publicado à medição |

> A terceira e a segunda linhas são `✓ᵐ`, e a distinção importa: **existe o artigo, com autor, ano
> e página conferidos** — o que este handbook **não** afirma é qualquer coisa sobre o conteúdo
> deles além do que o próprio título diz. A atribuição do *branch-and-bound* a Land e Doig é
> corrente na literatura didática, e aqui ela é apresentada como corrente.

## Os quatro eixos

Cada eixo é uma pergunta binária sobre o **modelo**, e não sobre o assunto. As respostas se
combinam: um problema pode ser não linear, inteiro e incerto ao mesmo tempo — e aí o trabalho é
outro.

| Eixo | A pergunta | De um lado | Do outro |
|---|---|---|---|
| **Linearidade** | Objetivo e restrições são somas de variável vezes constante? | **Linear** | **Não linear** |
| **Integralidade** | Alguma variável só aceita valor inteiro (ou 0/1)? | **Contínuo** | **Inteiro / misto** |
| **Incerteza** | Os parâmetros são conhecidos quando se decide? | **Determinístico** | **Estocástico / robusto** |
| **Convexidade** | Todo ótimo local é global? | **Convexo** | **Não convexo** |

**O quarto eixo é o que decide se a garantia de global é automática**, e por isso ele tem capítulo
próprio ([38](38-convexidade.md)) e atravessa os outros três: Programação Linear é convexa sempre;
um problema inteiro **não** é convexo; e um não linear qualquer pode ser convexo ou não.

> **E aqui vale desfazer um atalho que este capítulo quase adotou.** Não é a convexidade que decide
> o significado de `Optimal` — é o **limitante**. Um modelo inteiro é não convexo e mesmo assim o
> `Optimal` de um *branch-and-bound* é **prova**, porque o método fecha a distância entre a melhor
> solução e o melhor possível. O que sobra sem convexidade **e** sem limitante — uma busca local
> num modelo não linear — é o caso em que `Optimal` quer dizer apenas *"não achei nada melhor por
> aqui"*, e é a distância de 22 para 30.
>
> A regra que vale para tudo, e cabe numa linha: **`Optimal` só é prova quando vem com limitante.**

### O que muda em cada travessia

Esta é a tabela que vale decorar — não pelas técnicas, pela **coluna da direita**:

| Travessia | O que você ganha | **A garantia que deixa de valer** |
|---|---|---|
| Linear → **Não linear** | Representar retorno decrescente, economia de escala, risco | O ótimo pode não estar numa quina; sem convexidade, não há garantia de global |
| Contínuo → **Inteiro** | Representar decisões indivisíveis: abrir ou não, ir ou não | O teorema do vértice não vale; o custo cresce muito, e a prova de otimalidade vem de limitante, não de percorrer quinas |
| Determinístico → **Incerto** | Não fingir que se conhece o futuro | Não existe mais "a" solução ótima — existe ótima **sob um critério de risco**, que precisa ser declarado |
| Convexo → **Não convexo** | Representar o mundo como ele às vezes é | Deixa de haver garantia **automática** de global. Se o método também não produzir limitante, `Optimal` passa a significar *"não achei nada melhor por aqui"* |

**Arredondar não é atravessar de volta.** A tentação diante de um modelo inteiro é resolver o
contínuo e arredondar o resultado. Às vezes funciona; às vezes o arredondado é **inviável**, e às
vezes é viável e ruim. O que ele nunca é, é **provado**: arredondar entrega um número sem
garantia nenhuma, e entregá-lo como ótimo é a versão mais comum do erro caro deste capítulo.

## O mapa de decisão, em quatro perguntas

Na ordem, porque a ordem economiza trabalho:

1. **Dá para escrever tudo como soma de variável vezes constante?** Se dá, você está em
   Programação Linear (PL), e a Parte II inteira se aplica. Não force o modelo para caber — mas
   **tente**, porque muita coisa que parece não linear vira linear com uma mudança de variável ou
   uma aproximação por partes declarada.
2. **Alguma decisão é indivisível?** Meio caminhão, meia fábrica e meio funcionário não existem.
   Se existir, você está em Programação Inteira Mista — **MILP**, na sigla consagrada —, e o custo
   muda de patamar.
3. **Algum parâmetro é uma previsão?** Demanda, preço e tempo de viagem quase sempre são. Se forem,
   a pergunta seguinte é **qual critério de risco** — e essa pergunta é de quem decide, não de quem
   modela.
4. **Se não é linear, é convexo — e o método dá limitante?** São as duas perguntas que quase
   ninguém faz diante de um relatório, e juntas elas separam "esta é a melhor solução" de "não
   achei nada melhor por aqui".

### Exato ou heurístico — a escolha que a classe força

Classificar serve para chegar nesta decisão, que é a que o cliente sente:

| Escolha | Quando ela é a certa | O que ela autoriza prometer |
|---|---|---|
| **Exato ao ótimo** | Instância cabe no tempo disponível, e a decisão é grande | *"Nenhuma outra solução é melhor"* — o que **não** quer dizer que esta seja a única melhor: o [capítulo 06](06-ferramentas.md) mede um empate em que a ferramenta escolhe o plano |
| **Exato com limite de tempo** | Instância grande, mas o solver reporta o *gap* | *"Esta solução está a no máximo X% do melhor possível"* — a promessa mais útil das três |
| **Heurístico** | Instância enorme, ou modelo que nenhum solver aceita | *"Esta é a melhor que encontrei com este procedimento"* — e nada além disso |

A linha do meio é a mais subestimada. Um *gap* de 2% reportado é uma informação de gestão: diz que
continuar buscando pode render, no máximo, 2%. **Heurística sem limitante não diz nem isso**, e é
por isso que a promessa dela é a mais curta das três.

## Quando não serve

Classificar cedo demais é um erro real, e ele tem quatro formas:

**1. Quando a classe ainda depende de decisão de modelagem, e não do problema.** O mesmo problema
de negócio pode virar linear ou não linear conforme o que se escolhe como variável. Declarar a
classe antes de fechar a formulação é declarar sobre um objeto que ainda não existe.

**2. Quando a classificação vira desculpa para não medir.** *"É NP-difícil, então vamos de
heurística"* — onde **NP** é *não determinístico polinomial*, a classe do que se **confere** rápido
— é um raciocínio que pula uma etapa: NP-difícil é afirmação sobre o **pior caso da
classe**, não sobre a sua instância de 300 variáveis, que talvez o solver resolva ao ótimo em 4
segundos. A ordem certa é tentar, medir, e então decidir — e é assunto do
[capítulo 05](05-complexidade.md).

**3. Quando o eixo que importa não está na lista.** Os quatro eixos aqui são sobre a **estrutura
matemática**. Há problemas cuja dificuldade real é o dado que não existe, o prazo de uma semana ou
o fato de que quem decide não vai confiar num modelo que ninguém entende. Nenhum desses aparece na
classificação, e todos derrubam projeto.

**4. Quando a resposta é "não modele".** Vale sempre lembrar o [capítulo 02](02-ciclo-de-modelagem.md):
antes de escolher a classe, é preciso ter passado pela pergunta de quem vai decidir diferente por
causa disso.

## Fundamentos e fontes

**O que está medido aqui.** Nenhum número novo. Os valores 22 e 30 vêm da etapa 06 do `po-zero` e
estão conferidos no [capítulo 38](38-convexidade.md), com teste que compara o texto publicado à
medição.

**O que entra por fonte:** o sentido militar de *programming*, a expressão original de Dantzig e o
batismo por Koopmans em 1948 são `✓` **lidos**. Gomory (1958) e Land & Doig (1960) entram `✓ᵐ` —
**metadados conferidos, conteúdo não lido** —, e por isso este capítulo não afirma nada sobre o
que esses artigos contêm além do que os títulos dizem.

> 🟡 **Este capítulo está em v0.** Não passou por revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap04"></div>

Três exercícios. O primeiro classifica quatro situações nos eixos e cobra o que **ainda não dá**
para classificar; o segundo pede a previsão da garantia perdida em cada travessia; o terceiro é a
decisão que o cliente sente — exato, com limite de tempo, ou heurístico — com a promessa escrita
por extenso.

## Assista

**[Classes de problemas de otimização (programação linear, não linear, misto-inteira)](https://www.youtube.com/watch?v=FFtemvRfXOk)** ·
[Bruno Santoro](https://www.youtube.com/@otimizacao) · 21min49s

**O que ele resolve:** este capítulo organiza as classes **pela garantia que cada travessia
destrói** — é uma leitura de consequência, e ela deixa de fora o que as classes têm de concreto na
notação. O vídeo faz o outro lado: mostra como cada classe **se parece** quando escrita, com os
exemplos ao lado. Ver a forma antes de discutir a consequência ajuda, e é a ordem recomendada.

## Síntese — o que levar

- **A classe decide o que você pode prometer**, e não só quanto vai custar.
- **Quatro eixos:** linearidade, integralidade, incerteza, convexidade. Eles se combinam.
- **A convexidade é o eixo que decide o significado de `Optimal`** — e por isso atravessa os
  outros três.
- **Cada travessia tem uma coluna da direita**, que é a garantia perdida. É essa coluna que se
  decora.
- **Arredondar um modelo inteiro não é atravessar de volta:** entrega um número sem garantia, e
  às vezes inviável.
- **Três promessas possíveis:** o ótimo provado, o ótimo com *gap* declarado, e "a melhor que
  encontrei". A do meio é a mais subestimada.
- **`Optimal` só é prova quando vem com limitante.** Num inteiro resolvido ao ótimo, é prova; numa
  busca local sobre região não convexa, quer dizer "não achei nada melhor por aqui" — medido: 22
  contra 30.
- **Fora da Pesquisa Operacional:** diante de qualquer resultado computacional, pergunte que
  garantia o procedimento oferece antes de perguntar quanto ele demorou.

## Verificação

1. Uma rede quer decidir **quais** centros de distribuição abrir (entre 40 candidatos) e **quanto**
   despachar de cada um. Classifique nos quatro eixos, e diga qual eixo você **não** consegue
   responder só com esse enunciado. *(O1)*
2. Um analista resolveu o modelo contínuo, arredondou as aberturas para o inteiro mais próximo e
   apresentou o resultado como ótimo. Aponte as duas coisas que podem estar erradas na frase dele,
   e diga como cada uma se manifestaria. *(O2)*
3. O solver rodou 30 minutos, parou no limite de tempo e reportou um *gap* de 1,8%. Escreva a frase
   que você diz a quem decide — e escreva a frase que você **não** pode dizer. *(O3)*

### Leitura executiva

A classe de um problema de otimização decide **o que se pode prometer sobre a resposta**, e não
apenas quanto ela vai custar em tempo de máquina. Quatro eixos organizam a decisão: o modelo é
**linear** ou não; as variáveis são **contínuas** ou há decisões indivisíveis (**inteiras**); os
parâmetros são **conhecidos** quando se decide ou são previsões (**incerteza**); e o problema é
**convexo** ou não. Os eixos se combinam, e o quarto é especial — é ele que decide o significado da
palavra `Optimal` na saída, e por isso atravessa os outros três. O que vale decorar de cada
travessia não é a técnica que ela exige, e sim **a garantia que ela destrói**: sair do linear
elimina a certeza de que o ótimo está numa quina; exigir integralidade invalida o teorema do
vértice e troca a prova de otimalidade por um argumento de limitante; admitir incerteza faz
desaparecer "a" solução ótima, que passa a existir apenas sob um critério de risco que **alguém
precisa declarar**; e sair da convexidade tira a garantia automática de global, de modo que um
método **sem limitante** reduz `Optimal` a *"não achei nada melhor por aqui"* — o
que este handbook mediu como a distância entre **22 e 30**, na mesma região, com o mesmo objetivo e
duas partidas diferentes. Duas armadilhas fecham o capítulo. A primeira é **arredondar**: resolver
o contínuo e arredondar não é atravessar o eixo de volta, porque o resultado pode ser inviável e,
mesmo quando é viável, não vem com garantia nenhuma. A segunda é **classificar cedo demais**, seja
porque a classe ainda depende de decisões de formulação que não foram tomadas, seja porque
"NP-difícil" virou desculpa para não medir a instância que se tem na mão. Na prática, a
classificação existe para chegar a uma escolha de três: resolver ao ótimo e prometer que nenhuma
outra solução é melhor; resolver com limite de tempo e prometer uma distância máxima ao melhor
possível — a promessa mais útil das três, e a mais subestimada; ou usar heurística e prometer
apenas a melhor solução encontrada por aquele procedimento, o que é pouco, mas é honesto.
