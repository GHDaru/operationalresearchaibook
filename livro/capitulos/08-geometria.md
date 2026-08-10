# 08 — A geometria da Programação Linear

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-09 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Representar** um modelo de duas variáveis no plano e **interpretar** o que cada ponto
significa na operação — inclusive os pontos que o modelo precisa proibir.

**O2.** **Explicar** por que toda restrição corta o espaço em dois semiespaços, e por que
acrescentar restrição **nunca** aumenta a região viável.

**O3.** **Encontrar** o vértice ótimo subindo a reta de iso-lucro na direção do gradiente.

**O4.** **Determinar** o ponto ótimo pelo sistema formado pelas restrições que o sustentam.

**O5.** **Formular** um modelo de duas variáveis a partir de um enunciado em prosa e **resolvê-lo**
pelo método gráfico, do zero ao ponto exato.

## O problema

No capítulo anterior o solver respondeu, e nós aceitamos. Ele disse: monte 8 do Tipo 1 e 2 do
Tipo 2, lucro de R$ 1.100. Ficou uma pergunta pendurada, e ela era a mais importante: **como
você sabe que é isso?**

Este capítulo responde — e responde **desenhando**. Com duas variáveis, o problema inteiro cabe
numa folha, e a resposta deixa de ser um número que veio de fora para virar um lugar que dá
para apontar com o dedo.

Um aviso honesto antes de começar. Com duas variáveis, o desenho é confortável. Com três, já
exige esforço: são planos cortando um sólido, e o papel atrapalha mais do que ajuda. **A partir
de quatro, não há desenho** — há álgebra, e é dela que trata o capítulo seguinte.

Então por que gastar um capítulo inteiro com um método que só serve para dois? Porque **a
intuição que ele instala continua valendo em qualquer dimensão**. O Simplex não faz nada além
de caminhar pelos vértices que você vai enxergar aqui. Quem viu o desenho entende o algoritmo;
quem não viu, decora o algoritmo.

## De onde isto veio

O desenho não é um recurso didático que alguém inventou para facilitar a vida do aluno. Ele é,
historicamente, **como o assunto foi entendido pela primeira vez** — e por mais de um século foi
tudo o que havia.

### O aperto: a matemática sabia resolver igualdades e travava nas desigualdades

Esta é a assimetria que causa estranheza quando se olha de perto. Sistemas de **equações**
lineares já eram território dominado no século XIX: eliminação, determinantes, matrizes, tudo
resolvido e ensinado. Sistemas de **desigualdades** lineares, não. O progresso foi escasso, e o
atraso durou décadas.

Por quê? Porque os dois objetos são de naturezas diferentes:

> Uma **equação** fixa um ponto — ou uma reta, ou um plano: algo que a álgebra da época sabia
> manipular. Uma **desigualdade** descreve uma **região**, e não havia álgebra para regiões.
> Faltava, literalmente, o que escrever.

É o mesmo desconforto que o leitor sente ao encontrar a primeira restrição `≤`: com `=` você
resolve; com `≤`, resolve o quê?

### A virada: Fourier, e a decisão de olhar

Em **1826**, **Joseph Fourier** — o mesmo das séries de Fourier — publicou um trabalho com o
título modesto de *Solution d'une question particulière du calcul des inégalités*. Ele vinha
esbarrando em desigualdades em problemas de mecânica, probabilidade e estatística, e fez duas
coisas.

A primeira foi **algébrica**: um procedimento para eliminar variáveis de um sistema de
desigualdades, uma por vez.

A segunda é a deste capítulo: um método **geométrico** para achar a **região das soluções**. Em
vez de procurar uma álgebra que ainda não existia, ele mudou de representação para uma em que
"região" é um objeto natural — algo que se desenha e se olha.

**Cento e vinte anos antes de existir o Simplex, a região viável já estava desenhada.**

### O nome, e um fio que atravessa dois capítulos

O procedimento algébrico de Fourier foi esquecido e **redescoberto em 1936 por Theodore
Motzkin**, que o transformou em algoritmo sistemático, fundado na geometria dos conjuntos
convexos. Por isso hoje ele se chama **eliminação de Fourier–Motzkin**.

Guarde o sobrenome. **É o mesmo Motzkin** que, alguns anos depois, numa conversa com Dantzig,
sugeriu o nome de um algoritmo que você vai encontrar no próximo capítulo — o **Simplex**. A
mesma pessoa está nas duas pontas: na redescoberta de como olhar para desigualdades, e no
batismo do método que finalmente as resolveu em escala.

### Por que a eliminação não virou o método padrão

Vale saber, porque explica a estrutura deste livro. A eliminação de Fourier–Motzkin **funciona**
e é exata. O problema é o custo: cada variável eliminada **acrescenta** desigualdades ao sistema que
sobra, e o número delas **cresce exponencialmente**. Serve para provar coisas; não serve para
planejar uma fábrica.

Ou seja: a geometria deu o **entendimento** e não deu a **ferramenta** — que é exatamente o que
este capítulo vai dizer de si mesmo em "quando não serve". O desenho ensina e não trabalha. A
ferramenta chega no capítulo 09.

> **A ideia reaproveitável, que é o que fica.** *Quando a álgebra não te dá alça, troque de
> representação.* Fourier não inventou uma álgebra nova para desigualdades — ele mudou o
> problema para um terreno onde o objeto que lhe interessava, a região, já era natural de
> enxergar.
>
> Mudar de representação até o problema ficar visível é um movimento geral, e provavelmente o
> mais barato de todos: é o que faz alguém desenhar a arquitetura num guardanapo, converter uma
> regra de negócio numa tabela de decisão, ou plotar os dados antes de modelar. **Nada do
> problema muda; muda o que você consegue ver dele.**

### O que é documentado e o que é leitura nossa

| Afirmação | Estado |
|---|---|
| Fourier, nos anos 1820, estudando desigualdades em mecânica, probabilidade e estatística; **métodos algébrico e geométrico** para achar a região das soluções | ✓ **fonte aberta e conferida** |
| Desigualdades lineares são mais complicadas do que equações lineares, e ficaram para trás | ✓ mesma fonte |
| O trabalho de Fourier foi ampliado por T. Motzkin — daí eliminação de Fourier–Motzkin | ✓ mesma fonte |
| A eliminação de cada variável acrescenta desigualdades, e **o número delas cresce exponencialmente** | ✓ mesma fonte (antes estava aqui como "não medida") |
| Título e ano exatos do trabalho de 1826, e a data de 1936 para Motzkin | ⏳ localizados em busca, **não abertos na fonte** |
| É o mesmo Motzkin que sugeriu o nome *simplex* a Dantzig | ⏳ **atribuição corrente**, não confirmada em fonte primária. É a última pendência desta seção |
| A leitura de que "a geometria deu o entendimento e não a ferramenta", e o padrão "troque de representação" | 📖 **interpretação deste livro** |

As referências completas estão na [bibliografia](../bibliografia.md).

## A intuição

### Cada variável ganha um eixo

Duas variáveis de decisão, dois eixos. No eixo horizontal, $x_1$: quantos computadores do Tipo
1 montar — cada um com uma unidade central de processamento (CPU) e um pente de memória. No vertical, $x_2$: quantos do Tipo 2. **Um ponto do plano é um plano de produção** —
um par de números que alguém pode assinar.

O ponto $(8, 2)$ diz "monte oito do Tipo 1 e dois do Tipo 2". O ponto $(3, 5)$ diz outra coisa.
O ponto $(0, 0)$ diz "não monte nada" — que é uma decisão, e é viável.

### E os pontos negativos?

Agora um ponto como $(-4, 6)$. O que ele diz?

Literalmente: monte seis do Tipo 2 e **menos quatro** do Tipo 1. Isso tem um significado
físico — seria uma devolução, um desmonte, computadores voltando para virar componente. E
repare no que ele faz com o estoque: desmontar quatro máquinas **libera** quatro CPUs e quatro
pentes para montar outras coisas.

É por aí que mora o problema. Se o modelo aceitar desmontar, ele descobre que pode desmontar
infinitamente para liberar componente infinito, e montar infinitamente com ele. **É uma rota de
fuga**, e o lucro escapa por ela sem limite.

Não é um detalhe formal: é a mesma coisa da etapa sem restrições do capítulo anterior. O modelo
não é ilimitado porque o mundo é generoso; é ilimitado porque **esquecemos de dizer o que não
pode**.

Daí a primeira restrição, que quase todo mundo escreve no automático sem perceber o que ela
está fechando:

$$x_1 \ge 0 \qquad x_2 \ge 0$$

### Uma restrição é uma faca

Desenhe $x_1 \ge 0$. A reta $x_1 = 0$ é o eixo vertical, e a desigualdade fica com **tudo o que
está à direita dela**. Metade do plano sobrevive; a outra metade é descartada.

Agora $x_2 \ge 0$: a reta é o eixo horizontal, e sobrevive **tudo o que está acima**. Cruzando
as duas sobras, resta o **primeiro quadrante**.

Vale guardar a imagem, porque ela é o capítulo inteiro em uma frase. Pense no espaço de todos
os planos possíveis como uma **laranja**. Uma restrição é uma **faca** que atravessa a laranja
de lado a lado: ela não tira um pedaço do meio, não faz um buraco, não deixa duas ilhas
separadas. Ela **corta em dois** — e você fica com um lado e joga o outro fora. O lado que fica
é onde as soluções moram; o outro deixou de existir para o problema.

Disso decorre a propriedade mais útil deste capítulo, e ela é imediata:

> **Acrescentar uma restrição nunca aumenta a região viável.** No máximo mantém do mesmo
> tamanho — quando a faca passa fora e não corta nada.

Não é uma regra a decorar: é o que a faca faz. E vai economizar muito raciocínio adiante, porque
significa que **toda restrição nova só pode piorar (ou empatar) o melhor resultado possível**.
Se alguém acrescentar uma exigência ao problema e o lucro ótimo subir, há erro em algum lugar.

### A região ainda é infinita

O primeiro quadrante é infinito. Todo ponto dele é um plano de produção legítimo — só que a
maioria é fantasia, porque não há componente para tanto. Falta dizer o que existe no estoque.

**Primeira faca de verdade: as CPUs.** São 10, e cada máquina usa uma:

$$x_1 + x_2 \le 10$$

A reta $x_1 + x_2 = 10$ liga $(10, 0)$ a $(0, 10)$, e o lado que fica é o de baixo. Agora sim a
região é **finita**: um triângulo com vértices em $(0,0)$, $(10,0)$ e $(0,10)$.

## O que é "melhor" — a reta de iso-lucro

Todo ponto desse triângulo é viável. Todos são **soluções**. E aí vem a pergunta que o método
existe para responder: **qual é a melhor?**

Para comparar, precisamos de um jeito de ver o lucro no desenho. O truque é este: pense no
lucro como **altura**. Cada ponto do plano tem uma altura dada por

$$z = 100\,x_1 + 150\,x_2$$

e o objetivo é chegar no ponto mais alto da região. O plano deixa de ser plano: vira uma rampa.

Agora a pergunta certa: **por onde se anda sem subir nem descer?** Pelos pontos de mesma
altura — e o conjunto deles é uma reta:

$$100\,x_1 + 150\,x_2 = z$$

Essa é a **reta de iso-lucro**. Fixe $z = 900$ e você tem todos os planos que rendem R$ 900. É
uma curva de nível, igual às de um mapa topográfico: andar sobre ela é andar na horizontal da
montanha.

Mudar $z$ desloca a reta **paralelamente** — a inclinação não muda, porque ela só depende dos
lucros unitários. Subir $z$ empurra a reta para longe da origem.

E o método aparece sozinho: **suba a reta de iso-lucro até o último valor em que ela ainda
toca a região viável.** Onde ela toca por último é o ótimo.

<div data-viz="regiao-viavel">

*(Objeto interativo — precisa de JavaScript. Sem ele, a tabela de vértices mais adiante nesta
página traz os mesmos números, e o texto a seguir descreve o que a interação mostra.)*

</div>

Suba a reta no controle acima. Antes de chegar ao teto, ela **corta** a região: há muitos planos
com aquele lucro. No último valor, ela não corta mais — apenas **encosta**.

Repare **onde** ela encosta. Não é no interior da região. É na borda, e — nesta instância — numa
quina: num **vértice**.

O caso em que ela encosta num lado inteiro existe, e o capítulo volta a ele em "quando não
serve". O que vale sempre, e é a afirmação que sustenta o resto da Parte II, é mais precisa do
que "o contato é um ponto só":

> **Se existe ótimo, existe um vértice ótimo.** Pode haver outros pontos ótimos junto com ele —
> mas nunca é preciso procurar fora dos vértices.

Guarde essa palavra, porque ela é a ponte para todo o resto da Parte II. Com a restrição de CPU
sozinha, a reta encosta por último em $(0, 10)$: dez máquinas do Tipo 2, **R$ 1.500**. Que é
exatamente o que a intuição do capítulo anterior tinha dito — e agora sabemos *por quê*.

### A direção de crescimento

Vale nomear para onde a reta sobe. O vetor dos coeficientes do objetivo,

$$\nabla z = (100,\ 150),$$

é o **gradiente**: a direção em que o lucro cresce mais rápido. Ele é **perpendicular** à reta
de iso-lucro — o que faz sentido, porque andar ao longo da reta não muda o lucro, e a direção
que mais muda é a que sai dela em ângulo reto.

Na prática do desenho, o gradiente diz para que lado empurrar a régua. É a seta âmbar no
gráfico.

## Entra a segunda faca

Agora a memória: 12 pentes de 16 GB, com o Tipo 1 usando um e o Tipo 2 usando dois.

$$x_1 + 2\,x_2 \le 12$$

Ligue a restrição no controle acima e observe **três** coisas, nesta ordem:

1. **A região encolheu.** Como manda a faca — nunca cresce.
2. **O ótimo anterior sumiu.** O ponto $(0, 10)$ pedia 20 pentes, e só há 12. Ele não é mais um
   plano possível: **faltavam 8 pentes** para ele existir.
3. **O novo ótimo é outro vértice** — e ele não é nenhum dos dois "óbvios".

O novo vértice ótimo é $(8, 2)$, com **R$ 1.100**. Ele é o encontro das duas restrições, e é a
resposta que o solver deu no capítulo anterior sem explicar.

E agora dá para ver, no desenho, por que as duas regras de bolso erram:

| Plano | Onde está | Lucro |
|---|---|---|
| 10 do Tipo 1 | vértice $(10, 0)$ — sobra memória | R$ 1.000 |
| 6 do Tipo 2 | vértice $(0, 6)$ — sobra CPU | R$ 900 |
| **8 do Tipo 1 e 2 do Tipo 2** | **vértice $(8, 2)$ — nada sobra** | **R$ 1.100** |

Cada heurística gulosa corre para um canto e esgota **um** recurso, deixando o outro parado. O
ótimo é o único vértice que esgota **os dois** — e é por isso que ele é uma mistura, e por isso
que nenhuma regra que olha um recurso de cada vez consegue encontrá-lo.

## O procedimento, passo a passo

O desenho é bonito, mas a resposta precisa ser exata — e olho não lê coordenada. O procedimento
fecha essa lacuna e é o que você vai exercitar:

**Passo 1 — desenhe as retas.** Uma por restrição, trocando `≤` por `=`. Inclua os eixos: a
não-negatividade é restrição como as outras.

**Passo 2 — ache o lado que fica.** Para cada reta, teste um ponto qualquer fora dela — a origem
serve quase sempre. Se ele satisfaz a desigualdade, o lado dele é o que sobrevive.

**Passo 3 — interseque tudo.** O que resta é a região viável.

**Passo 4 — trace uma reta de iso-lucro qualquer** e empurre-a na direção do gradiente até o
último contato.

**Passo 5 — identifique as duas restrições que sustentam aquele vértice.** Este é o passo que
o olho não faz por você, e é o passo que separa o desenho da resposta. Um vértice no plano é o
encontro de **duas** retas: descubra quais são.

**Passo 6 — resolva o sistema.** Troque as duas desigualdades por igualdades e resolva o
sistema $2 \times 2$. O resultado é o ponto ótimo, exato.

No nosso caso, o vértice de cima é sustentado por CPU e memória. Então:

$$
\begin{cases}
x_1 + x_2 = 10 \\
x_1 + 2x_2 = 12
\end{cases}
\;\Longrightarrow\;
x_2 = 2,\quad x_1 = 8
$$

Subtraindo a primeira da segunda, $x_2 = 2$; substituindo, $x_1 = 8$. Lucro
$100(8) + 150(2) = 1.100$. **Exato, sem ler coordenada no gráfico.**

**Passo 7 — confira.** O ponto satisfaz todas as outras restrições? Se não satisfizer, ele é
interseção de duas retas mas **não é vértice da região** — e isso acontece o tempo todo.

## O código

A [etapa 02 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-02-metodo-grafico)
faz exatamente o procedimento acima, mas para **todos os pares de restrições**, e não só para o
par que o olho escolheu:

1. toma as restrições duas a duas — inclusive os eixos;
2. resolve cada sistema $2 \times 2$;
3. descarta o que viola qualquer outra restrição;
4. avalia o lucro no que sobrou.

Com CPU e memória, são seis pares. **Quatro sobrevivem** — $(0,0)$, $(10,0)$, $(0,6)$ e
$(8,2)$ — e dois são descartados: $(0,10)$ viola a memória, e $(12,0)$ viola a CPU.

Note o que a lista mostra: **a conta é fácil, a triagem é que dá trabalho.** Resolver um sistema
$2\times2$ é trivial; saber quais dos resultados são vértices de verdade é o serviço.

O experimento confere a enumeração contra o HiGHS nas duas etapas, e os dois concordam. Isso
**prova**, neste caso, a afirmação que o capítulo faz e não demonstra em geral: o ótimo está num
vértice. A demonstração geral é trabalho do capítulo do Simplex.

## Quando não serve

O método gráfico tem um limite duro e vários limites finos.

**O limite duro é a dimensão.** Duas variáveis, confortável. Três, um sólido cortado por planos
— possível, penoso e propenso a erro. **Quatro ou mais, impossível**: não há papel com quatro
eixos, e a intuição visual simplesmente acaba. Como quase todo problema real tem centenas de
variáveis, o método gráfico **não é uma ferramenta de trabalho — é uma ferramenta de
entendimento**. Use-o para aprender, não para resolver.

Os limites finos aparecem já em duas variáveis, e cada um vira assunto adiante:

| Situação | O que acontece no desenho | Onde é tratada |
|---|---|---|
| Nenhum ponto satisfaz tudo | As facas não deixam nada de pé | Capítulo de casos especiais |
| A região é aberta na direção do crescimento | A reta sobe para sempre | Já vimos: é o ilimitado |
| A reta de iso-lucro fica **paralela** a um lado | Ela encosta num lado inteiro, não num ponto: infinitos ótimos | Capítulo de casos especiais |
| Três restrições passando pelo mesmo vértice | Vértice "sustentado" por mais retas do que precisa | Degenerescência, mesmo capítulo |

Há ainda um limite que o desenho esconde: ele dá o **ponto**, mas não dá o **preço**. Quanto
vale a décima primeira CPU? O gráfico não responde — e essa pergunta é a porta de entrada da
dualidade.

## Fundamentos e fontes

O tratamento gráfico é onde as duas obras-base mais divergem em estratégia:

- **Lachtermacher** abre a unidade de Programação Linear pela resolução gráfica, antes da
  analítica e da forma tabular. A geometria vem primeiro, e o algoritmo depois.
- **Arenales et al.** colocam a resolução gráfica **depois** de um catálogo extenso de
  aplicações e da forma padrão, como preparação imediata para a teoria do Simplex.

Este handbook fica com a ordem do primeiro pela razão do segundo: geometria antes do algoritmo,
mas explicitamente **como preparação para ele** — o vértice não é curiosidade visual, é o objeto
que o Simplex vai percorrer.

> **Dívida declarada.** Esta seção deveria trazer de 2 a 4 artigos científicos traduzidos para
> decisões. Ela não traz: a varredura sobre visualização e ensino de otimização não foi feita, e
> **inventar citação é pior do que admitir a lacuna** (constituição, Princípio III). Está na
> fila do [Radar](../../radar/RADAR.md), junto com a do capítulo anterior.

## Pratique

Dez exercícios, em dois blocos de cinco.

Os cinco primeiros **dão o modelo pronto** e treinam o procedimento (objetivos O3 e O4):
identificar as restrições que sustentam o vértice e resolver o sistema. Os cinco seguintes **dão
só o enunciado** e cobram o objetivo O5 — formular e depois resolver. É a primeira vez no
handbook em que as duas habilidades são exigidas na mesma tarefa.

<div data-bateria="cap08"></div>

## Assista

**[Aula 2 — Programação Linear: método gráfico](https://www.youtube.com/watch?v=0QwcirNrU3E)** · [André Brochi](https://www.youtube.com/@matematicaeestatistica) · 24min20s

**O que ele resolve:** este capítulo tem uma ilha interativa, e ela é boa para *experimentar* —
subir a reta, ver a região encolher. O que ela não faz é **narrar**: alguém desenhando no quadro,
errando de propósito, explicando por que traçou aquela reta e não outra. O vídeo faz isso, e é a
segunda passada sobre o mesmo conteúdo, no ritmo de quem está pensando em voz alta.

É a continuação direta do vídeo do capítulo anterior, na mesma série.

> ✓ **Ficha conferida na fonte** em 2026-08-09: autor, canal, duração e data de publicação. O
> vídeo entra por link e crédito, com o player de origem — ver a política na
> [Videoteca](../videoteca.md). O que **não** foi conferido é o conteúdo: a frase "o que ele
> resolve" é leitura do editor a partir do título e da posição na série, e ninguém assistiu.

## Síntese — o que levar

- **O desenho não é muleta didática: foi como o assunto se entendeu primeiro.** Fourier achava a
  região das soluções geometricamente em 1826, 120 anos antes de existir o Simplex.
- **Quando a álgebra não dá alça, troque de representação.** Nada do problema muda; muda o que
  você consegue ver dele.

- **Cada variável é um eixo; cada ponto é um plano de produção.** Inclusive os impossíveis.
- **A não-negatividade não é formalidade:** sem ela existe rota de fuga, e o lucro escapa.
- **Restrição é faca:** corta o espaço em dois e você fica com um lado. Por isso ela **nunca**
  aumenta a região viável.
- **Lucro é altura; iso-lucro é curva de nível.** Subir a reta até o último contato é o método.
- **Se existe ótimo, existe um vértice ótimo.** Pode haver mais pontos ótimos junto — mas nunca é preciso procurar fora dos vértices. É a ideia que o Simplex vai transformar em algoritmo.
- **O gradiente aponta para onde subir**, e é perpendicular à reta de iso-lucro.
- **Vértice se resolve por sistema, não por olho:** ache as duas restrições que o sustentam,
  troque `≤` por `=`, resolva o $2\times2$ — e confira contra as demais.
- **O desenho é ferramenta de entendimento, não de trabalho.** Acima de três variáveis, ele
  acaba; a intuição não.

## Verificação

1. Um colega diz que acrescentou uma restrição ao modelo e o lucro ótimo **subiu**. Sem ver o
   modelo dele, o que você já sabe, e por quê? *(O2)*
2. Ao subir a reta de iso-lucro, ela encosta ao mesmo tempo em dois vértices vizinhos. O que
   isso significa para a decisão, e o que você responde a quem perguntar "então qual eu faço?"
   *(O3)*
3. Você resolveu o sistema de duas restrições e obteve um ponto com lucro maior que o do vértice
   que tinha encontrado no desenho. Qual é a explicação mais provável, e como você testa? *(O4)*

### Leitura executiva

Com duas variáveis, um modelo de Programação Linear cabe no plano: cada variável é um eixo e
cada ponto é um plano de produção. Pontos negativos representariam desmonte e abririam uma rota
de fuga infinita — por isso a não-negatividade é restrição de verdade, e é ela que produz o
primeiro quadrante. Toda restrição funciona como uma faca que corta o espaço em dois
semiespaços, do que decorre a propriedade mais útil do capítulo: **acrescentar restrição nunca
aumenta a região viável**. O lucro é lido como altura, e a reta de iso-lucro é a curva de nível;
subi-la na direção do gradiente até o último contato com a região encontra o ótimo — e, se existe
ótimo, **existe um vértice ótimo**, de modo que nunca é preciso procurar fora das quinas. Como olho não lê coordenada, o ponto exato vem do sistema formado pelas
duas restrições que sustentam aquele vértice. No caso da montadora, a restrição de memória
elimina o ótimo anterior — que pedia 20 pentes e só havia 12 — e o novo ótimo é (8, 2), com
R$ 1.100, o único vértice que esgota os dois recursos. O método é ferramenta de entendimento,
não de trabalho: acima de três variáveis não há desenho, e a partir daí o que resta é o
algoritmo.
