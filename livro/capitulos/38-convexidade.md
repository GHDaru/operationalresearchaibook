# 38 — Convexidade

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Decidir** se um conjunto dado é convexo, e **dizer por quê** — com um contraexemplo
quando não for.

**O2.** **Diagnosticar** um modelo em que o ótimo local **não** é global, e identificar **o que na
formulação** quebrou a convexidade.

**O3.** **Julgar** a afirmação "o solver achou o ótimo" quando o modelo não é convexo, e dizer o
que ela de fato autoriza.

## O problema

Este capítulo está fora de ordem de propósito. Ele é da Parte VI, e você o está lendo agora porque
o [capítulo 09](09-simplex.md) usou a convexidade **a crédito**, e não é honesto deixar essa dívida
correr.

A frase que o capítulo 09 precisou para justificar o Simplex foi esta:

> *"parar no primeiro topo é seguro"*

O método sobe de vértice em vértice e para quando nenhum vizinho melhora. **Por que isso basta?**
Num terreno qualquer, parar num topo local não prova nada — você pode estar numa colina com uma
montanha atrás. Em Programação Linear, prova. A propriedade que faz a diferença é a
**convexidade**, e ela é a razão de o Simplex ser um método e não um chute educado.

E o inverso é o erro caro deste capítulo, que custa mais do que os outros porque **não deixa
rastro**:

> Alguém roda um modelo não convexo, o solver devolve uma solução, o relatório diz **"Optimal"**, e
> a empresa executa. A solução é ótima **da região onde a busca por acaso começou**. Não há erro,
> não há aviso, e o número que ficou na mesa não aparece em lugar nenhum.

Este capítulo mede exatamente esse caso: mesma região, mesmo objetivo, duas partidas — **22 e 30**.

## De onde isto veio

### O aperto: os métodos funcionavam e ninguém sabia dizer quando

Desde muito antes da Pesquisa Operacional já se resolviam problemas de otimização por condições de
primeira ordem — derive, iguale a zero, resolva. O procedimento acha **pontos estacionários**, e a
pergunta que ele não responde é qual deles é a resposta. Máximo? Mínimo? Nem um nem outro?

A prática convivia com isso por inspeção: desenhava-se, olhava-se, decidia-se. Funciona em duas
dimensões e para de funcionar exatamente onde os problemas ficam interessantes.

### A virada: a propriedade se muda do método para o conjunto

A virada é conceitual, e é das mais econômicas da matemática aplicada: **em vez de perguntar se o
método é bom, pergunte se o problema é convexo**. Se for, uma garantia global sai de uma
verificação local — e a garantia vale para **qualquer** método que suba, não para um método
específico.

É isso que faz a convexidade valer um capítulo próprio em vez de um parágrafo dentro do Simplex.
Ela não é sobre o Simplex. O Simplex é um dos usuários dela.

### A ideia reaproveitável

> **Uma garantia global a partir de uma verificação local é sempre uma propriedade do problema,
> nunca uma esperteza do algoritmo.**

Quando alguém disser que um procedimento "sempre encontra a melhor solução", a pergunta útil não é
sobre o procedimento: é *qual propriedade da estrutura sustenta isso?* Sem uma, a afirmação é
publicidade.

### Procedência

| Afirmação | Estado |
|---|---|
| *Convex Analysis*, de Rockafellar (Princeton, 1970), é a referência canônica do campo | ✓ᵐ metadados conferidos — [bibliografia](../bibliografia.md) |
| A história da formação do conceito (Minkowski, Fenchel, e a linhagem que leva ao livro de 1970) | ❌ **procurada e não localizada** por identificador nesta rodada |
| A origem do termo "convexo" em otimização | ❌ procurada, não encontrada |

> **Uso declarado da referência:** Rockafellar entra como **ponteiro**, não como fonte de
> afirmação. É um livro inteiro, não foi aberto nesta rodada, e nenhuma frase deste capítulo se
> apoia nele além do reconhecimento de que é a referência canônica. Este capítulo é **v0** e curto;
> quem precisar de profundidade tem para onde ir, e é esse o serviço prestado aqui.

## A intuição — o teste do elástico

Pegue dois pontos quaisquer **dentro** do conjunto e estique um elástico entre eles. Se o elástico
nunca sai do conjunto, seja qual for o par, o conjunto é **convexo**.

$$x, y \in C \ \Rightarrow\ \lambda x + (1-\lambda)y \in C \quad \text{para todo } \lambda \in [0,1]$$

Formalizado assim, o teste vira mecânico — e, o que é melhor, vira **refutável**: um único par cujo
segmento escape encerra a questão. Não é preciso examinar todos.

| Convexo | Não convexo |
|---|---|
| Um triângulo, um disco, uma sala retangular | Uma lua crescente, um donut, um "L" |
| A região viável de qualquer modelo linear | Qualquer região definida com "**ou**" |

A última linha da segunda coluna é a que importa em Pesquisa Operacional, e vamos voltar a ela.

### Por que isso salva o Simplex

Junte duas coisas. Primeira: a região viável de um modelo linear é uma interseção de semiespaços, e
interseção de convexos é convexa. Segunda: a função objetivo é linear.

Num conjunto convexo, com objetivo linear, **um ótimo local é um ótimo global**. A razão cabe em
uma frase: se existisse um ponto melhor em outro lugar, o segmento até ele estaria dentro da região
— e, sendo a função linear, andar por esse segmento melhoraria o objetivo **desde o primeiro
passo**. Então o ponto de partida não era um ótimo local.

É esse argumento, e só ele, que autoriza o Simplex a parar. A dívida do capítulo 09 está paga.

## A matemática

### Conjunto convexo

Já está acima. O que vale acrescentar é a operação que mais se usa: **interseção de convexos é
convexa**, para qualquer número de conjuntos. É o que faz todo poliedro ser convexo — cada
restrição $\le$ define um semiespaço, que é convexo, e a região é a interseção de todos.

**União, não.** A união de dois convexos quase nunca é convexa, e é daí que vem a maior parte da
não convexidade acidental em modelagem.

### Função convexa

$$f(\lambda x + (1-\lambda)y) \ \le\ \lambda f(x) + (1-\lambda)f(y)$$

Em português: **a corda fica acima da curva**. Uma tigela é convexa; um morro é côncavo; uma
paisagem com vários morros não é nem uma coisa nem outra — e é essa a terceira que aparece nos
problemas reais.

### O teorema que se usa

> Se $C$ é convexo e $f$ é convexa, então **todo mínimo local de $f$ em $C$ é mínimo global**.
> (Para maximização, troque "convexa" por "côncava".)

Uma função **linear** é convexa **e** côncava ao mesmo tempo — é o caso degenerado que serve aos
dois lados, e por isso Programação Linear tem a garantia de graça, tanto para maximizar quanto para
minimizar.

## O código

A [etapa 06 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-06-convexidade)
mede as duas coisas que este capítulo afirma. Em aritmética exata, com grade de meio em meio: o
resultado se regenera igual em qualquer máquina, sem semente e sem ponto flutuante.

### O teste do ponto médio

```
região da montadora (Programação Linear)
  pares testados: 12561
  nenhum contraexemplo em toda a grade — evidência de convexidade, não prova

região com 'fornecedor A OU fornecedor B'
  pares testados: 15
  contraexemplo: ['0', '8'] e ['6', '0'] estão dentro · meio ['3', '4'] está FORA
  NÃO é convexo — o contraexemplo prova
```

**Leia a diferença entre as duas linhas de veredito, porque ela é o ponto.** Doze mil pares sem
contraexemplo **não provam** convexidade — nenhuma amostragem prova. **Quinze** pares bastaram para
provar a **não** convexidade, porque um contraexemplo é uma prova completa. O teste é assimétrico
por natureza, e essa assimetria é a forma de quase toda verificação empírica útil.

### O ótimo local que não é global

A região não convexa vem de uma regra de negócio banal: *o contrato exige volume mínimo de **um dos
dois** fornecedores* — 6 unidades de A **ou** 8 de B, com o total limitado a 10. Maximizando
$3x_1 + 2x_2$:

```
partindo de ['0', '8']: para em ['2', '8'] com lucro 22 (4 passos)
partindo de ['6', '0']: para em ['10', '0'] com lucro 30 (8 passos)
melhor de toda a região: ['10', '0'] com lucro 30
diferença entre a pior parada e o ótimo: 8
```

A busca local é honesta: só aceita vizinho **viável** e **melhor**, e para quando ninguém em volta
é melhor. É o esqueleto de quase toda heurística. Partindo de $(0,8)$ ela termina em $(2,8)$ e
**nenhum vizinho é melhor** — é um ótimo local de verdade. E ele vale **22 contra 30**.

Repare no que **não** aconteceu: nenhum erro, nenhum aviso, nenhuma bandeira. A busca fez
exatamente o que devia. O que estava errado era a suposição de que fazer isso bastava.

## Quando não serve

**1. Convexidade é do problema, não da formulação.** Um mesmo problema pode ser escrito de forma
convexa ou não. Reformular é, muitas vezes, mais barato do que trocar de método — e é o que a
programação inteira faz ao substituir o "ou" por variável binária, no [capítulo 23](../mapa-do-handbook.md).

**2. Convexo não quer dizer fácil.** Há problemas convexos caros de resolver. A garantia é sobre
**o que a resposta significa**, não sobre quanto custa obtê-la.

**3. Testar por amostragem não prova.** Como a medição acima deixa explícito: a ausência de
contraexemplo é evidência, não prova. A prova vem da estrutura — "é interseção de semiespaços" —,
não de doze mil pares.

**4. Este capítulo é v0 e é uma ponte.** Ele existe para que ~40 capítulos possam **apontar** em
vez de reexplicar, e para pagar a dívida do capítulo 09. Otimização convexa como campo — cones,
dualidade de Lagrange, condições de Karush-Kuhn-Tucker (KKT) — é a Parte VI inteira.

**5. Fora da convexidade, "ótimo" muda de sentido.** Um solver de programação não linear que
devolve "Optimal" quase sempre quer dizer **"encontrei um ponto que satisfaz as condições locais"**.
Isso é diferente de "esta é a melhor solução", e a diferença é a de 22 para 30.

## Fundamentos e fontes

**O que está medido aqui.** O contraexemplo, os 12.561 pares, os 15 pares, as duas paradas da busca
local e a diferença de 8 saem da etapa 06 e se regeneram rodando um script.

**O que foi conferido no registro, e não lido.** ✓ᵐ **ROCKAFELLAR, R. T.** *Convex Analysis*.
Princeton, 1970 — usado como **ponteiro**, não como fonte de afirmação.

**O que continua em dívida:** a história da formação do conceito e a origem do termo, ambas `❌`
procuradas e não localizadas por identificador nesta rodada. Ver a
[bibliografia](../bibliografia.md).

> 🟡 **Este capítulo está em v0**, e além disso é **curto por desenho**: ele é uma ponte, não um
> tratado. Não passou por revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap38"></div>

Três exercícios. O primeiro pede decisão com justificativa — e, quando a resposta for "não
convexo", **um contraexemplo**, porque é o único tipo de prova que cabe numa resposta curta. O
segundo é o diagnóstico do ótimo local. O terceiro é sobre acreditar num relatório.

## Assista

**[Hiperplano, semi-espaço, poliedro, raio, conjunto e envoltório convexo, função convexa —
Otimização](https://www.youtube.com/watch?v=eDhsMJAcPz0)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 17min55s

**O que ele resolve:** este capítulo entra pela intuição do elástico e vai direto para o que a
convexidade **autoriza**, porque é isso que ele deve ao capítulo 09. O vídeo cobre o vocabulário
formal que fica de fora — hiperplano, semiespaço, envoltório convexo — e é a ponte natural para a
Parte VI, onde esses termos passam a ser ferramenta de trabalho.

## Síntese — o que levar

- **Teste do elástico:** dois pontos dentro, o segmento inteiro dentro. É a definição, e é
  operacional.
- **Interseção de convexos é convexa; união quase nunca é.** É por isso que todo poliedro é convexo
  e que todo "**ou**" é suspeito.
- **A garantia é esta:** em conjunto convexo com objetivo convexo (ou linear), **ótimo local é
  ótimo global**. É ela que autoriza o Simplex a parar no primeiro topo.
- **Um contraexemplo prova a não convexidade; nenhuma amostragem prova a convexidade.** Medido:
  15 pares bastaram para refutar, 12.561 não bastaram para provar.
- **Fora da convexidade, uma busca honesta para no topo do morro em que começou** — 22 contra 30,
  sem erro, sem aviso e sem rastro.
- **"O solver achou o ótimo" precisa da pergunta seguinte:** *o modelo é convexo?* Sem isso, a
  frase quer dizer "encontrei um ponto localmente bom".
- **Fora da Pesquisa Operacional:** garantia global a partir de verificação local é sempre
  propriedade da estrutura, nunca esperteza do procedimento.

## Verificação

1. Uma equipe afirma que a região viável do modelo dela é convexa "porque testamos mil pontos".
   O que você responde, e o que pediria no lugar? *(O1)*
2. Um modelo tem a restrição *"a produção da linha A deve ser zero **ou** pelo menos 50 unidades"*.
   O que isso faz com a região viável, e qual é a consequência para a leitura do resultado? *(O2)*
3. Um relatório de solver não linear informa `Optimal` e um valor. Que **duas** perguntas você faz
   antes de levar esse número a uma decisão? *(O3)*

### Leitura executiva

Convexidade é a propriedade que transforma uma verificação **local** em garantia **global**: num
conjunto convexo, com objetivo linear ou convexo, todo ótimo local é ótimo global — e é
exclusivamente isso que autoriza o Simplex a parar quando nenhum vértice vizinho melhora, dívida
que o capítulo 09 contraiu e que este capítulo paga. O teste é o do elástico: tomados dois pontos
quaisquer do conjunto, o segmento entre eles também precisa estar dentro. Ele é **assimétrico**, e
a assimetria é útil: um único contraexemplo **prova** a não convexidade, enquanto nenhuma
quantidade de pares bem-comportados prova a convexidade — medido aqui, 15 pares bastaram para
refutar uma região e 12.561 não bastaram para provar outra, cuja convexidade vem da **estrutura**
(interseção de semiespaços), não da amostragem. Em modelagem, a não convexidade quase sempre entra
pela porta da frente, escrita em português: qualquer regra com "**ou**" — *compre do fornecedor A
ou do B*, *produza zero ou pelo menos 50* — produz uma união de regiões, e união de convexos quase
nunca é convexa. A consequência é concreta e não deixa rastro: numa região dessas, uma busca local
honesta, que só aceita vizinho viável e melhor, **para no topo do morro em que começou**. Este
handbook mede o caso — mesma região, mesmo objetivo, duas partidas, resultados **22 e 30**, sem
erro, sem aviso e sem bandeira. Daí a leitura obrigatória de qualquer relatório: `Optimal` num
solver não linear costuma significar "encontrei um ponto que satisfaz as condições locais", e a
distância entre isso e "esta é a melhor solução" é a distância entre 22 e 30.
