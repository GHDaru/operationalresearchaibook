# 18 — Árvore geradora mínima e projeto de redes

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Construir** uma árvore geradora mínima à mão, por Kruskal, e dizer por que cada aresta
foi aceita ou recusada.

**O2.** **Distinguir** o problema em que o guloso é ótimo do problema em que ele não é — pela
**estrutura**, e não pelo tamanho da instância.

**O3.** **Reconhecer** quando a decisão de projeto de rede não é uma árvore, e dizer o que ela é.

## O problema

Este capítulo existe por causa de uma pergunta que quase todo mundo faz errado:

> *"Se pegar sempre o mais barato agora funciona aqui, por que não funciona no roteiro de
> entrega?"*

A resposta não é "porque o roteiro é maior". É estrutural, e este capítulo mede a diferença **na
mesma instância, com o mesmo gesto**: o guloso é ótimo na árvore e **14,3% pior** no roteiro.

O erro caro deste capítulo:

> Alguém confirma que o guloso funcionou num problema, generaliza o gesto, e aplica no problema ao
> lado. O resultado sai, roda rápido, e ninguém tem com o que compará-lo — porque o guloso **não
> produz limitante** ([capítulo 05](05-complexidade.md)). O prejuízo fica invisível.

## De onde isto veio

### O aperto: ligar tudo, gastando o mínimo

O problema nasce concreto: eletrificar um conjunto de localidades, ligar centrais telefônicas,
puxar fibra. A pergunta é sempre a mesma — **que ligações construir para que todos fiquem
conectados, ao menor custo total** — e ela tem duas partes que se resolvem juntas: *quais* ligações
e *quantas*.

**O que se fazia antes** era desenhar à mão e conferir: um engenheiro traçava um conjunto de
ligações que parecia razoável, somava o custo, e tentava outro. Funciona com cinco pontos e falha
com quarenta, por dois motivos ao mesmo tempo — o número de configurações explode, e **não há como
saber se a que se desenhou é a melhor**. A segunda falha é a pior: ela não aparece. Um traçado
razoável e caro é indistinguível de um traçado ótimo, para quem não tem com o que comparar.

> **Quem estava preso nisso, e quando, é `⏳` neste handbook.** A motivação por eletrificação e
> telefonia é atribuição corrente da literatura didática, e não foi confirmada em fonte primária
> nesta rodada.

A segunda parte tem resposta fechada e vale saber: com $n$ pontos, **toda** solução conectada sem
desperdício tem exatamente $n - 1$ ligações. Uma a menos desconecta; uma a mais fecha ciclo, e
ciclo é gasto que não conecta ninguém novo.

### A virada: aceitar o mais barato que não fecha ciclo

O método é curto o bastante para caber numa frase: **ordene as ligações pelo custo e aceite cada
uma que não feche ciclo**. Ele é guloso — decide olhando só o presente — e, ao contrário da
maioria dos gulosos, **é ótimo, com prova**.

O que autoriza isso tem nome: se você corta o grafo em dois lados quaisquer, **a aresta mais
barata que atravessa o corte está em alguma árvore ótima**. É a *propriedade do corte*, e é ela — e
não a sorte — que sustenta o guloso.

> **Este capítulo enuncia a propriedade e não a demonstra**, do mesmo jeito que o
> [capítulo 19](19-fluxo-maximo.md) exibe o teorema do corte mínimo em vez de prová-lo. Dizer isso
> é mais honesto do que chamar o enunciado de prova.

### A ideia reaproveitável

> **Um atalho guloso é seguro quando existe um argumento local que sustenta uma conclusão global.**
> Na árvore, esse argumento existe e tem nome. No roteiro, não existe — e é só isso que separa os
> dois.

### A origem do nome

**"Árvore"** vem da forma: sem ciclo, com um caminho único entre quaisquer dois pontos, o desenho
lembra ramificação. **"Geradora"** (*spanning*) quer dizer que ela **alcança todos** os nós — uma
árvore que deixa alguém de fora não gera o grafo. A atribuição dos dois algoritmos clássicos a
**Kruskal** e a **Prim** é corrente e não foi confirmada em fonte primária nesta rodada.

### Procedência

| Afirmação | Estado |
|---|---|
| A atribuição dos métodos a Kruskal e a Prim | ⏳ **atribuição corrente**; este handbook **não abriu** as fontes primárias nesta rodada |
| A propriedade do corte como justificativa do guloso | 📖 **leitura editorial** de resultado clássico; o handbook **não reproduz a demonstração** |
| Que a árvore custe 17 e o roteiro guloso custe 32 contra 28 | ✓ **medidos** em `po-zero/parte-III-redes`, com teste que compara este texto à medição |
| Que a árvore de custo 17 seja **mínima** | ✓ **verificado por segundo caminho**: enumeração de todas as árvores geradoras da instância |

## A construção, na instância que o capítulo mede

Cinco cidades, dez ligações possíveis, custos declarados:

| Ligação | Custo | | Ligação | Custo |
|---|---|---|---|---|
| a–c | 3 | | b–e | 6 |
| c–e | 3 | | d–e | 6 |
| b–c | 5 | | a–e | 7 |
| | | | c–d | 7 |
| | | | a–b | 8 |
| | | | b–d | 8 |
| | | | a–d | 12 |

Kruskal, na ordem: aceita **a–c (3)**; aceita **c–e (3)**; aceita **b–c (5)**; recusa
**b–e (6)** — fecharia ciclo com o que já existe; aceita **d–e (6)**. São quatro arestas para cinco
cidades, e o algoritmo para.

**Custo total: 17.**

> **E este 17 foi conferido por dois caminhos.** Além do Kruskal, o `po-zero` **enumera todas as
> árvores geradoras** da instância e toma a mais barata — e chega ao mesmo 17. Chegar ao mesmo
> número por dois caminhos é o que separa uma medição de uma coincidência, e é a mesma disciplina
> que o [capítulo 12](12-dualidade.md) usa ao montar o dual como problema próprio.

### O que custa proibir uma ligação

A pergunta aparece em todo projeto real — *"e se essa rota não estiver disponível?"* — e a resposta
intuitiva está errada. Proibindo **a–c**, que custa 3:

| | Custo |
|---|---|
| Árvore ótima | **17** |
| Árvore ótima sem `a–c` | **21** |
| **Perda** | **4** |

**A aresta valia 3 e a perda foi 4.** O custo de proibir uma ligação **não é o custo dela** — aqui é
maior. A razão é que a substituta não é a próxima aresta da lista: com `a–c` fora, o nó `a` fica
isolado do resto e precisa da melhor reconexão **disponível depois que a topologia mudou**, que é
`a–e` (7). A árvore inteira se reorganiza, e a conta é entre árvores, não entre arestas.

> **A leitura para levar:** a pergunta *"quanto vale esta ligação?"* só tem resposta em relação ao
> resto da rede. É o mesmo hábito de raciocínio do preço-sombra do [capítulo 13](13-sensibilidade.md)
> — o valor de um recurso é o que muda no **ótimo** quando ele falta, e não o preço na etiqueta.

## O mesmo gesto, no problema ao lado

Agora a mesma instância, a mesma ideia — *vá sempre ao mais barato agora* —, aplicada a uma
pergunta diferente: **qual a rota mais curta que visita todas as cidades e volta ao início?**

| Como | Rota | Custo |
|---|---|---|
| **Guloso** (vizinho mais próximo, saindo de `a`) | `a → c → e → b → d → a` | **32** |
| **Ótimo** (enumeração de todas as rotas) | `a → b → d → e → c → a` | **28** |

**O guloso perde 4, ou 14,3%** — na mesma instância em que ele foi provadamente ótimo para a
árvore.

> **A instância não foi desenhada para isso, e vale dizer como ela foi obtida.** A primeira
> tentativa foi escolher os pesos à mão para o guloso errar — **e ele acertou**, 17 contra 17. A
> instância publicada saiu de uma busca sobre 4.000 grafos aleatórios de cinco cidades, com semente
> declarada, tomando a de maior perda relativa. **Procurar um contraexemplo é mais honesto do que
> arranjar um**, e é bem mais rápido do que insistir num exemplo que não coopera.

### Por que um e não o outro

| | Árvore geradora mínima | Roteiro (caixeiro-viajante) |
|---|---|---|
| O que se escolhe | Um conjunto de arestas | Uma **sequência** |
| Restrição | Não fechar ciclo | Fechar **exatamente um** ciclo, passando por todos |
| Argumento local | **Existe** — a propriedade do corte | **Não existe** |
| Guloso | Ótimo, com prova | Sem garantia; medido aqui: 14,3% pior |

A linha que decide é a terceira. Escolher a aresta mais barata do corte **nunca** impede a árvore
ótima; escolher a cidade mais próxima agora **pode** obrigar você a atravessar o mapa depois. A
decisão gulosa, no roteiro, **compromete o futuro** — e é exatamente essa a condição que o
[capítulo 17](17-caminho-minimo.md) mostrou que Dijkstra exige para fechar um nó.

## Quando não serve

**1. Quando a rede precisa aguentar uma falha.** Uma árvore tem caminho único entre dois pontos:
**qualquer** ligação que caia desconecta alguém. Se o requisito é redundância, a resposta não é
árvore — é projeto de rede com conectividade mínima, que é programação inteira.

**2. Quando o custo não é só de construir.** A árvore minimiza o custo de **ligar**. Se o que doer
for o custo de **operar** — distância que o tráfego percorre depois —, a árvore mínima pode ser
péssima: ela liga tudo barato e obriga a rotas longas.

**3. Quando há capacidade nas ligações.** Árvore não conhece capacidade. Se cada trecho escoa um
tanto, a pergunta é de fluxo, e é o [capítulo 19](19-fluxo-maximo.md).

**4. Quando nem todo mundo precisa ser ligado.** Se dá para deixar pontos de fora, ou usar pontos
intermediários que não estavam no conjunto, o problema é outro — **árvore de Steiner** — e ele é
**NP**-difícil (*não determinístico polinomial*, [capítulo 05](05-complexidade.md)), ao contrário
deste.

## Fundamentos científicos

**KRUSKAL (1956)** e **PRIM (1957)** são as duas fontes clássicas ([bibliografia](../bibliografia.md)),
e **NEŠETŘIL, MILKOVÁ e NEŠETŘILOVÁ (2001)** é a que muda o que este capítulo pode afirmar: ela
traduz e comenta dois trabalhos de **Borůvka, de 1926**, que antecedem os dois. É por isso que a
página credita o *problema* sem declarar quem o resolveu primeiro — a atribuição corrente, que
para em Kruskal e Prim, tem uma anterioridade documentada de trinta anos.

**ROSENKRANTZ, STEARNS e LEWIS (1977)** trata dos limites de garantia das heurísticas para o
caixeiro-viajante, que é o problema ao lado usado aqui como contraste. A comparação que este
capítulo publica — guloso **32** contra ótimo **28** — é uma medição própria numa instância
declarada, e **não** uma leitura desse artigo.

> Os quatro identificadores foram conferidos; **nenhum texto foi aberto**. Ver o
> [Radar](../../radar/RADAR.md).

## Fundamentos e fontes

**O que está medido aqui.** O custo 17 da árvore, conferido por dois caminhos; o custo 32 do
roteiro guloso e o 28 do ótimo; e a perda de 14,3%. Tudo em
`po-zero/parte-III-redes/redes.py`, em aritmética exata, com teste que compara **este texto** à
medição.

**O que continua em dívida:** as atribuições a Kruskal e a Prim, `⏳`.

> 🔵 **Este capítulo está em "medido".** O que falta para ✅ é revisão independente em contexto
> fresco.

## Pratique

<div data-bateria="cap18"></div>

Três exercícios. O primeiro constrói a árvore à mão e cobra a justificativa de cada recusa; o
segundo é o do capítulo — separar os dois problemas pela estrutura; o terceiro reconhece a decisão
de projeto que **não** é uma árvore.

## Assista

**[Árvore Geradora Mínima (MST) - Prim e Kruskal - LPC I 2021](https://www.youtube.com/watch?v=I9cc2NTBs60)** ·
[PROTIVA UNESP](https://www.youtube.com/@protiva_unesp) · 34min06s

**O que ele resolve:** este capítulo usa **um** algoritmo — Kruskal — e gasta o espaço na
comparação com o roteiro. O vídeo cobre os **dois** clássicos, Prim e Kruskal, lado a lado, com a
execução desenhada. Ver os dois ajuda a entender que a garantia é da **propriedade do corte**, e
não do algoritmo específico: os dois caminham diferente e chegam ao mesmo custo.

## Síntese — o que levar

- **Com $n$ pontos, toda solução conectada sem desperdício tem $n-1$ ligações.**
- **Kruskal é guloso e é ótimo com prova** — e a prova é a propriedade do corte, não a sorte.
- **Medido: árvore de custo 17**, conferida por dois caminhos (Kruskal e enumeração de todas as
  árvores geradoras).
- **O mesmo gesto guloso perde 14,3% no roteiro** — 32 contra 28, na mesma instância.
- **A diferença é estrutural, não de tamanho:** na árvore existe argumento local que sustenta
  conclusão global; no roteiro, não.
- **Árvore não tem redundância:** qualquer ligação que caia desconecta alguém.
- **Árvore minimiza o custo de ligar, não o de operar** — e os dois podem discordar muito.
- **Fora da Pesquisa Operacional:** um atalho guloso é seguro quando existe um argumento local que
  sustenta a conclusão global. Sem ele, é chute rápido.

## Verificação

1. Na instância desta página, a ligação `b–e` (custo 6) é recusada e a `d–e` (custo 6) é aceita.
   As duas custam o mesmo. Por que uma entra e a outra não? *(O1)*
2. Um colega diz: "o guloso errou no roteiro porque cinco cidades já é grande demais". Corrija a
   frase, e diga o que de fato explica a diferença. *(O2)*
3. Uma operadora quer ligar oito centrais de modo que **a queda de qualquer trecho não desconecte
   ninguém**. Isso é árvore geradora mínima? Se não, o que é? *(O3)*

### Leitura executiva

A árvore geradora mínima responde a uma pergunta concreta — **que ligações construir para conectar
todos ao menor custo** — e tem duas propriedades que a tornam o exemplo didático perfeito desta
Parte. A primeira é aritmética: com $n$ pontos, toda solução conectada sem desperdício tem
exatamente $n-1$ ligações, porque uma a menos desconecta e uma a mais fecha ciclo, que é gasto sem
conexão nova. A segunda é a que importa: **o método guloso — ordene por custo e aceite tudo o que
não feche ciclo — é ótimo, com prova**, e a prova é a *propriedade do corte*: a aresta mais barata
que atravessa qualquer corte do grafo pertence a alguma árvore ótima. Medido na instância desta
página, o custo é **17**, e ele foi conferido por dois caminhos independentes — Kruskal e a
enumeração de todas as árvores geradoras —, porque chegar ao mesmo número por dois caminhos é o que
separa medição de coincidência. O capítulo então faz a comparação que lhe dá sentido: **o mesmo
gesto guloso, na mesma instância, aplicado ao roteiro** que visita todas as cidades e volta,
devolve **32** contra um ótimo de **28** — uma perda de **14,3%**. A diferença entre os dois casos
não é de tamanho, é de estrutura: na árvore, escolher a aresta mais barata do corte nunca impede a
solução ótima; no roteiro, escolher a cidade mais próxima agora pode obrigar a atravessar o mapa
depois, e a decisão local **compromete o futuro**. Vale registrar como a instância foi obtida: a
primeira tentativa de desenhá-la à mão **falhou**, porque o guloso acertou o roteiro nela; a
publicada saiu de uma busca com semente declarada sobre 4.000 grafos aleatórios, tomando a de maior
perda — procurar um contraexemplo é mais honesto do que arranjar um. Por fim, a árvore deixa de
servir em quatro situações: quando a rede precisa aguentar falhas (uma árvore tem caminho único, e
qualquer queda desconecta alguém); quando o que dói é o custo de **operar** e não o de ligar;
quando as ligações têm capacidade, caso em que a pergunta é de fluxo; e quando nem todos os pontos
precisam ser ligados, que é a árvore de Steiner — e essa, ao contrário desta, é NP-difícil.
