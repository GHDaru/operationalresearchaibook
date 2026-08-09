# 07 — Formulação de modelos lineares

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-07 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Distinguir**, numa situação descrita em prosa, o que é variável de decisão, o que é
parâmetro, o que é objetivo e o que é restrição.

**O2.** **Formular** um modelo linear completo, com unidades coerentes dos dois lados de cada
restrição.

**O3.** **Diagnosticar** um erro de formulação a partir do modelo e da saída que ele produz.

**O4.** **Avaliar** quando a formulação linear não serve, e qual família de método assume dali
em diante.

## O problema

Último dia do mês numa montadora de computadores. O que entrar no estoque hoje é vendido —
não há dúvida de demanda, há dúvida de **o que montar**.

Dois modelos saem da linha, e os dois disputam o mesmo estoque de unidades centrais de
processamento (CPU) e de pentes de memória de 16 gigabytes (GB):

| | Lucro por unidade | CPU | Memória |
|---|---|---|---|
| **Tipo 1** | R$ 100 | 1 | 16 GB — **1 pente** |
| **Tipo 2** | R$ 150 | 1 | 32 GB — **2 pentes** |

O estoque só tem pentes de 16 GB. Um Tipo 2 leva dois deles.

Isto é **planejamento de necessidades de materiais (MRP) ao contrário**. O MRP clássico anda
para a frente: parte da demanda, explode a lista de materiais e diz o que comprar. Aqui não há
o que comprar — o mês acabou. Parte-se do **componente que existe** e pergunta-se o que dá para
montar com ele.

### Primeira pergunta: quanto dá para ganhar?

Sem mais informação nenhuma, quanto essa montadora ganha hoje?

**Infinito.** Se nada limita, monte infinitos Tipo 2 e fature infinito. O modelo é
**ilimitado** — e essa é a resposta correta para a pergunta como ela foi feita.

Vale parar aqui, porque a lição é maior do que parece. O modelo não deu resposta absurda porque
estava mal resolvido; deu porque **estava mal perguntado**. Um sistema sem restrição não é um
sistema modelável.

> **Restrição não é burocracia do método. É o que torna a pergunta respondível.**

Todo sistema real tem pelo menos uma. Encontrá-la é metade do trabalho.

### Segunda pergunta: e com 10 CPUs?

Digamos que haja **10 CPUs** em estoque, e memória à vontade. Agora o que montar?

A resposta vem antes do raciocínio: **10 do Tipo 2, R$ 1.500**. Cada máquina custa exatamente
uma CPU — a mesma CPU —, então monte a que paga mais. Não há discussão.

E está certo. Mas repare no que acabou de acontecer: **você respondeu com uma regra, não com um
método.** Então:

*Você tem certeza? Como é que se prova isso?*

Deixe a pergunta em suspenso. Ela é a espinha da Parte II inteira, e o capítulo seguinte
começa a pagá-la.

### Terceira pergunta: e a memória?

Há **12 pentes** de 16 GB. Só isso.

Agora tente responder antes de continuar lendo. Quantos de cada tipo?

A regra de antes diz "faça o que paga mais": 12 pentes dão para **6 do Tipo 2**, e sobram 4
CPUs paradas. R$ 900.

Mas há outra regra igualmente razoável. O pente virou o recurso apertado, então olhe o lucro
**por pente**: o Tipo 1 paga R$ 100 por pente e o Tipo 2 paga R$ 75. Por esse critério, faça
Tipo 1: **10 unidades** (as CPUs acabam antes dos pentes). R$ 1.000.

**Duas regras sensatas, dois produtos diferentes, dois resultados diferentes.** E nenhuma das
duas está certa:

| Plano | O que acaba | Lucro |
|---|---|---|
| 6 do Tipo 2 — "o que paga mais" | pentes; sobram 4 CPUs | R$ 900 |
| 10 do Tipo 1 — "o que paga mais por pente" | CPUs; sobram 2 pentes | R$ 1.000 |
| **8 do Tipo 1 e 2 do Tipo 2** | **os dois, exatamente** | **R$ 1.100** |

O ótimo é uma **mistura**, e ele é o único plano que esgota os dois recursos ao mesmo tempo.
Nenhuma regra que olha um recurso de cada vez chega nele — porque o problema não é de um
recurso de cada vez.

> Todos os números deste capítulo vêm de `po-zero/etapa-01-formulacao/experimento.py` e estão
> em `resultados.json`, com as versões de biblioteca e solver declaradas.

**É por isso que o método existe.** E o método começa aqui: em escrever o problema de um jeito
que uma máquina possa responder — o que é o assunto deste capítulo.

## A intuição

Formular é responder a **quatro perguntas**, nesta ordem. Parecem óbvias e quase nunca são
feitas em voz alta.

### 1. O que quem decide pode de fato escolher?

Isso — e só isso — é **variável de decisão**.

Na montadora: quantos Tipo 1 e quantos Tipo 2 montar. O estoque de CPUs **não** é escolha: já
está lá. O lucro total **não** é escolha: é consequência.

O teste é brutal e funciona: **se ninguém pode mudar aquilo por decisão, não é variável.**

### 2. Qual é a única medida a maximizar ou minimizar?

Uma. Aqui é o lucro total. Se aparecerem duas — "maximizar lucro e minimizar estoque parado" —,
o problema não tem função objetivo: tem duas, e isso é outro assunto.

### 3. O que limita as combinações?

Cada limite vira uma **restrição**. Na montadora, um limite por componente em estoque.

A verificação mais barata e mais ignorada: **as unidades batem dos dois lados?** Se a esquerda
está em pentes e a direita em reais, a restrição está errada — e nenhum solver vai avisar.

### 4. O que é dado, e não escolhido?

**Parâmetro.** O lucro unitário, o consumo de cada componente, o estoque disponível.

A fronteira entre parâmetro e variável é a fronteira entre o que você aceita e o que você
decide. Mover um número de um lado para o outro muda o problema — às vezes é exatamente o que
se quer fazer. (Se a montadora *pudesse* comprar pentes hoje, o estoque viraria decisão, e o
modelo seria outro.)

## A matemática

Com as quatro respostas na mão, o modelo se escreve quase sozinho.

**Notação.** Seja $x_j$ a quantidade a montar do produto $j$, em unidades. Seja $c_j$ o lucro
do produto $j$, em reais por unidade. Seja $a_{ij}$ a quantidade do componente $i$ que uma
unidade do produto $j$ consome — **é a lista de materiais** —, e $b_i$ o estoque do componente
$i$.

$$
\begin{aligned}
\text{maximizar} \quad & \sum_j c_j x_j \\
\text{sujeito a} \quad & \sum_j a_{ij} x_j \le b_i \quad \text{para cada componente } i \\
& x_j \ge 0
\end{aligned}
$$

Para a montadora:

$$
\begin{aligned}
\text{maximizar} \quad & 100\,x_1 + 150\,x_2 && \text{(lucro, R\$)} \\
\text{sujeito a} \quad & x_1 + x_2 \le 10 && \text{(CPUs)} \\
& x_1 + 2\,x_2 \le 12 && \text{(pentes de 16 GB)} \\
& x_1,\, x_2 \ge 0
\end{aligned}
$$

Confira as unidades na restrição de memória: $(\text{pentes/unid}) \times (\text{unid}) =
\text{pentes}$, contra pentes em estoque. Bate. Faça isso em toda restrição que escrever.

### As três hipóteses que fazem o modelo ser linear

Vale saber o nome de cada uma, porque é por elas que a formulação quebra:

| Hipótese | O que significa | Quando quebra |
|---|---|---|
| **Proporcionalidade** | Dobrar $x_j$ dobra o lucro e o consumo | Desconto por volume; tempo de setup por lote |
| **Aditividade** | O total é a soma das partes, sem interação | Produtos que compartilham um preparo comum |
| **Divisibilidade** | $x_j$ pode ser fracionário | Montar 8,5 computadores |

A terceira já está incomodando, e com razão — voltaremos a ela.

### Por que a não-negatividade não é decoração

$x_j \ge 0$ parece burocracia, e é a restrição que mais se esquece. Sem ela, o modelo pode
"montar" quantidades negativas — o que significaria **desmontar** computadores para liberar
componente. E aí ele desmonta infinito para montar infinito: a mesma rota de fuga da primeira
pergunta, agora escondida.

## O procedimento, passo a passo

Percorrendo a montadora do zero:

**Passo 1 — sublinhe os verbos de decisão.** "Quanto montar de cada tipo." → $x_1, x_2$.

**Passo 2 — declare a unidade de cada variável, por escrito.** "Unidades a montar hoje."
Variável sem unidade declarada é a origem silenciosa de metade dos erros de restrição.

**Passo 3 — escreva o objetivo e pergunte "é isto que a pessoa quer?".** Lucro total, uma
medida só.

**Passo 4 — uma restrição por limite, com as unidades conferidas.** Um componente, uma
restrição. Os coeficientes vêm da lista de materiais.

**Passo 5 — não-negatividade.** Sempre.

**Passo 6 — leia o modelo em voz alta, em português.** "Maximizar 100 reais por Tipo 1 mais 150
por Tipo 2, gastando no máximo 10 CPUs e 12 pentes…". Se soa estranho para quem conhece a
operação, o modelo está errado — e essa é a revisão mais barata que existe.

## O código

A [etapa 01 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-01-formulacao)
não escreve o modelo à mão: **monta o modelo a partir da lista de materiais**.

```python
for c in ativos:
    prob += (
        pulp.lpSum(dados["produtos"][p]["lista_de_materiais"].get(c, 0) * x[p] for p in x)
        <= dados["componentes"][c]["estoque"],
        f"estoque_{c}",
    )
```

Isso não é elegância gratuita. Acrescentar um terceiro produto ou um quarto componente é editar
o JSON, não o código — e é assim que se percebe que **a formulação tem forma**. É essa forma
que os métodos exploram.

O experimento percorre as três etapas da história e, na última, roda as duas regras de bolso
para refutá-las com número em vez de discurso:

```
  etapa 1 (sem restrição) : Unbounded
  etapa 2 (só CPU)        : {'tipo1': 0.0, 'tipo2': 10.0} -> R$ 1500
  etapa 3 (CPU + memória) : {'tipo1': 8.0, 'tipo2': 2.0} -> R$ 1100
    o ótimo da etapa 2 ainda é viável? False  (folga de pentes: -8)

  regras de bolso:
    por_cpu      escolhe tipo2  -> {'tipo1': 0.0, 'tipo2': 6.0} = R$ 900  (perde R$ 200)
    por_pente16  escolhe tipo1  -> {'tipo1': 10.0, 'tipo2': 0.0} = R$ 1000  (perde R$ 100)
```

Repare na linha do meio: **o ótimo da etapa 2 não sobrevive à etapa 3**. Ele pedia 20 pentes, e
só há 12 — faltavam 8. Uma restrição nova não reorganizou a resposta: ela **eliminou** a
resposta anterior.

O solver, aqui, é caixa-preta de propósito: chamamos o HiGHS e aceitamos o número. É dívida
deliberada, e ela começa a ser paga no capítulo seguinte — que responde, desenhando, a pergunta
que ficou em suspenso: *como é que se prova?*

## Quando não serve

Quatro situações concretas, e um destino declarado para cada:

| Situação | Por que quebra | Para onde vai |
|---|---|---|
| **Montar 8,5 computadores** — a solução saiu fracionária e o produto é indivisível | Quebra a **divisibilidade** | Programação inteira |
| **Decisão de sim-ou-não** — abrir ou não um segundo turno; usar ou não um fornecedor | Não é quantidade, é lógica | Variáveis binárias |
| **Desconto por volume ou custo de setup** — o lucro unitário muda com a quantidade | Quebra a **proporcionalidade** | Programação não linear, ou reformulação com binárias |
| **Estoque que é estimativa** — a contagem do sistema não bate com a prateleira | O modelo trata estimativa como certeza | Otimização sob incerteza |

Neste capítulo tivemos sorte: o ótimo saiu inteiro por acaso — 8 e 2. **Não conte com isso.**
E não caia na saída fácil: **arredondar a solução contínua** pode produzir um plano
**inviável**, ou viável e longe do ótimo. Arredondar não é resolver o problema inteiro; é
torcer.

## Fundamentos e fontes

As duas obras-base tratam formulação de maneiras que vale contrastar, porque a diferença é
decisão pedagógica, não estilo:

- **Lachtermacher** entra pela planilha e por casos de negócio, com o modelo emergindo do
  problema. Chega rápido à prática e paga na estrutura: o vocabulário formal vem depois.
- **Arenales et al.** abrem a unidade de otimização linear com um catálogo de aplicações —
  mistura, transporte, planejamento da produção, corte — antes de qualquer método. A aposta é
  que o repertório vem primeiro.

Este handbook segue uma terceira via: **um caso só, percorrido até o fim**, com o repertório de
padrões deslocado para o final desta Parte. A razão é carga cognitiva — quem ainda não formulou
um modelo inteiro não aproveita um catálogo de dez.

> **Dívida declarada.** O esqueleto de capítulo pede de 2 a 4 artigos científicos traduzidos
> para decisões nesta seção. Este capítulo não os tem: a varredura sobre ensino de formulação
> não foi feita, e **inventar citação é pior do que admitir a lacuna** (constituição, Princípio
> III). Está na fila do [Radar](../../radar/RADAR.md).

## Pratique

Quatro exercícios, em dificuldade crescente: reconhecer, formular, diagnosticar e — no último —
aplicar ao seu próprio contexto. Eles se passam **fora** da montadora, de propósito: formular é
habilidade que precisa atravessar domínios, e treinar sempre no mesmo caso ensina o caso, não a
habilidade.

<div data-bateria="cap07"></div>

## Assista

**[Aula 1 — Programação Linear: introdução](https://www.youtube.com/watch?v=Pi_ZnVd-96Q)** · autor ⏳ · duração ⏳

**O que ele resolve:** o texto aqui insiste que formular é escolher a pergunta, e faz isso com um
caso só. O vídeo cobre a introdução à Programação Linear em outro ritmo e com outro exemplo —
ouvir a mesma ideia dita por outra pessoa, com outra escolha de palavras, é o que consolida.
Assista **depois** de tentar formular o modelo da montadora por conta própria; antes disso ele
entrega resposta que você deveria estar construindo.

> ⏳ **Este vídeo está em estado provisório.** Título e endereço foram verificados; **autoria e
> duração não**. O ambiente de produção deste handbook não alcança o YouTube, e inventar esses
> campos seria pior do que deixá-los em branco (constituição, Princípio III). A
> [Videoteca](../videoteca.md) explica o estado e as duas condições que o encerram — a preferida
> sendo a troca pelo vídeo equivalente do canal parceiro.

## Síntese — o que levar

- **Sem restrição, o problema é ilimitado.** Restrição não é burocracia: é o que torna a
  pergunta respondível.
- **Formular é escolher a pergunta.** O solver responde qualquer uma com a mesma confiança.
- **Quatro perguntas bastam:** o que se pode escolher, qual a única medida, o que limita, o que
  é dado.
- **Regra de bolso não resolve mistura.** Duas heurísticas sensatas apontaram para produtos
  diferentes, e nenhuma achou o ótimo — que é o único plano que esgota os dois recursos.
- **Confira as unidades dos dois lados.** Dez segundos por restrição.
- **Leia o modelo em voz alta.** Se soa estranho para quem conhece a operação, está errado.
- **A lista de materiais é a matriz de coeficientes.** Ver isso é ver que a formulação tem forma.
- **Todo modelo linear assume três coisas** — proporcionalidade, aditividade, divisibilidade —
  e saber qual delas quebrou é o que aponta o método seguinte.

## Verificação

1. A montadora descobre que pode comprar pentes de um fornecedor vizinho, hoje, a R$ 40 cada.
   O que muda na sua formulação — e qual das quatro perguntas passa a ter outra resposta? *(O1)*
2. Um analista apresenta um modelo em que o lucro total aparece do lado esquerdo de uma
   restrição. Sem ver o resto, o que você já suspeita, e o que pergunta a ele? *(O2, O3)*
3. O fornecedor passa a dar 5% de desconto para pedidos acima de 100 pentes. Qual das três
   hipóteses da Programação Linear isso quebra, e o que muda no seu plano de modelagem? *(O4)*

### Leitura executiva

Formular um modelo linear é decidir **qual pergunta** ele vai responder — a única parte do
trabalho que nenhum solver faz. O capítulo percorre uma montadora no último dia do mês em três
etapas: sem restrição alguma o lucro é ilimitado, o que ensina que restrição é o que torna a
pergunta respondível; com 10 CPUs a intuição acerta (dez do modelo que paga mais) mas não sabe
provar, e a pergunta fica em suspenso; com 12 pentes de memória a intuição erra, e erra de duas
maneiras opostas — a regra "faça o que paga mais" rende R$ 900, a regra "faça o que paga mais
por pente" rende R$ 1.000, e o ótimo é uma mistura de R$ 1.100 que nenhuma das duas encontra.
A partir daí, quatro perguntas organizam toda formulação: o que quem decide pode escolher, qual
é a única medida, o que limita as combinações e o que é dado. A lista de materiais é a matriz de
coeficientes, e a conferência de unidades dos dois lados de cada restrição é a revisão mais
barata que existe. O modelo linear assume proporcionalidade, aditividade e divisibilidade — e
saber qual delas o seu problema quebra é o que indica o método seguinte.
