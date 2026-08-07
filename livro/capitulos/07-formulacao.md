# 07 — Formulação de modelos lineares

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-06 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Distinguir**, numa situação descrita em prosa, o que é variável de decisão, o que é
parâmetro, o que é objetivo e o que é restrição.

**O2.** **Formular** um modelo linear completo, com unidades coerentes dos dois lados de cada
restrição.

**O3.** **Diagnosticar** um erro de formulação a partir do modelo e da saída que ele produz.

**O4.** **Avaliar** quando a formulação linear não serve, e qual família de método assume dali
em diante.

## O problema

A marcenaria São Bento fabrica mesas e estantes. O dono quer saber quanto produzir de cada uma
no mês. Ele tem dois recursos apertados — horas de marcenaria e horas de acabamento — e um
teto de demanda para estantes.

Alguém da equipe monta um modelo. A pergunta que ele escreve é: **maximizar a receita**. Faz
sentido, à primeira vista: mais receita, melhor. O modelo roda, o solver devolve `Optimal`, e
o plano sai:

> **60 mesas, 0 estantes.** Receita de **R$ 54.000** no mês.

Não há erro de aritmética. Não há falha de solver. O plano é viável: cabe nas horas
disponíveis. E está **errado** — de um jeito que só aparece quando se pergunta outra coisa.

Maximizando **margem de contribuição** em vez de receita, sobre exatamente as mesmas
restrições, o plano vira:

> **30 mesas, 40 estantes.** Margem de **R$ 13.800** no mês.

O plano da receita entrega margem de **R$ 13.200**. A diferença é de **R$ 600 por mês** — e
ela some para sempre, porque ninguém vai auditar um modelo que rodou, respondeu e nunca
reclamou.

Tem mais: o plano da receita deixa **60 horas de acabamento paradas**. Uma seção inteira
ociosa, num mês em que o dono acha que está no limite. O modelo não mentiu. Ele respondeu
com precisão a uma pergunta que ninguém devia ter feito.

> Todos os números deste capítulo vêm de `po-zero/etapa-01-formulacao/experimento.py`, e
> estão em `resultados.json` com as versões de biblioteca e solver declaradas.

**Este capítulo é sobre isso**: a parte do trabalho em que se decide *qual pergunta o modelo
vai responder*. É a única parte que nenhum solver faz por você — e é onde mora o erro caro.

## A intuição

Formular é responder a **quatro perguntas**, nesta ordem. Elas parecem óbvias e quase nunca
são feitas em voz alta.

### 1. O que quem decide pode de fato escolher?

Isso — e só isso — é **variável de decisão**.

É a pergunta que resolve a maior parte dos erros de iniciante. "O lucro" não é variável de
decisão: é consequência. "A demanda" não é: é dado. "A quantidade de mesas a fabricar" é,
porque o dono pode assinar embaixo dela amanhã de manhã.

O teste é brutal e funciona: **se ninguém pode mudar aquilo por decisão, não é variável.**

### 2. Qual é a única medida a maximizar ou minimizar?

Uma. Se aparecem duas — "maximizar lucro e minimizar atraso" —, o problema não tem função
objetivo: tem duas, e isso é outro assunto (otimização multiobjetivo, mais à frente no
handbook).

E aqui mora o erro da São Bento. **Receita e margem não são a mesma medida.** Receita é o que
entra; margem é o que sobra depois do que a unidade consome. Otimizar a primeira é escolher
o produto que mais fatura, não o que mais paga.

### 3. O que limita as combinações?

Cada limite vira uma **restrição**. Recurso escasso, capacidade, demanda máxima, contrato
mínimo, regra da empresa.

A verificação mais barata e mais ignorada: **as unidades batem dos dois lados?** Se a esquerda
está em horas por mês e a direita em unidades, a restrição está errada — e nenhum solver vai
avisar.

### 4. O que é dado, e não escolhido?

**Parâmetro.** Margem por unidade, tempo por unidade, horas disponíveis. Números que entram no
modelo e não são decididos por ele.

A fronteira entre parâmetro e variável é a fronteira entre o que você aceita e o que você
decide. Mover um número de um lado para o outro muda o problema — às vezes é exatamente o que
se quer fazer.

## A matemática

Com as quatro respostas na mão, o modelo se escreve quase sozinho.

**Notação.** Seja $x_j$ a quantidade a produzir do produto $j$ no mês, em unidades. Seja $c_j$
a margem de contribuição do produto $j$, em reais por unidade. Seja $a_{ij}$ o consumo do
recurso $i$ por unidade do produto $j$, e $b_i$ a disponibilidade do recurso $i$ no mês.

A forma geral de um **modelo de Programação Linear (PL)**:

$$
\begin{aligned}
\text{maximizar} \quad & \sum_j c_j x_j \\
\text{sujeito a} \quad & \sum_j a_{ij} x_j \le b_i \quad \text{para todo recurso } i \\
& x_j \ge 0
\end{aligned}
$$

Três exigências fazem dele um modelo **linear**, e vale saber o nome de cada uma porque é por
elas que a formulação quebra:

| Exigência | O que significa | Quando quebra |
|---|---|---|
| **Proporcionalidade** | Dobrar $x_j$ dobra a contribuição e o consumo | Desconto por volume; ganho de escala; tempo de setup |
| **Aditividade** | O total é a soma das partes, sem interação | Produtos que compartilham um preparo; efeito conjunto |
| **Divisibilidade** | $x_j$ pode assumir valor fracionário | Decisões que só existem inteiras, ou de sim-ou-não |

### O modelo da São Bento

Variáveis: $x_1$ = mesas por mês, $x_2$ = estantes por mês.

$$
\begin{aligned}
\text{maximizar} \quad & 220\,x_1 + 180\,x_2 && \text{(margem, R\$/mês)} \\
\text{sujeito a} \quad & 4\,x_1 + 3\,x_2 \le 240 && \text{(marcenaria, h/mês)} \\
& 2\,x_1 + 3\,x_2 \le 180 && \text{(acabamento, h/mês)} \\
& x_2 \le 50 && \text{(demanda de estantes, unid/mês)} \\
& x_1,\, x_2 \ge 0
\end{aligned}
$$

Repare na verificação de unidades na restrição de marcenaria: $(\text{h/unid}) \times
(\text{unid/mês}) = \text{h/mês}$, contra h/mês disponíveis. Bate. Faça isso em toda restrição
que escrever — é o gesto de dez segundos que evita a maioria dos modelos absurdos.

### Por que a não-negatividade não é decoração

$x_j \ge 0$ parece burocracia, e é a restrição que o iniciante mais esquece. Sem ela o solver
pode "produzir" quantidades negativas para liberar recurso e inflar o objetivo — devolvendo um
ótimo matematicamente correto e fisicamente impossível.

## O procedimento, passo a passo

O esqueleto de capítulo deste handbook reserva esta posição para *o algoritmo*. Num capítulo
de formulação, o algoritmo é **o procedimento de formular** — e ele tem passos tão definidos
quanto os de um método numérico.

Percorrendo a São Bento do zero:

**Passo 1 — Sublinhe os verbos de decisão no enunciado.** "Quanto produzir de cada produto."
Duas quantidades, dois produtos. → $x_1, x_2$.

**Passo 2 — Declare a unidade de cada variável, por escrito.** "Unidades por mês." Variável sem
unidade declarada é a origem silenciosa de metade dos erros de restrição.

**Passo 3 — Escreva o objetivo e pergunte "isto é o que a pessoa quer?".** Aqui é onde a São
Bento tropeçou. O dono não quer faturar; quer ganhar dinheiro. → margem, não receita.

**Passo 4 — Uma restrição por limite, com as unidades conferidas.** Marcenaria, acabamento,
demanda. Três limites, três restrições.

**Passo 5 — Não-negatividade.** Sempre.

**Passo 6 — Leia o modelo em voz alta, em português.** "Maximizar 220 reais por mesa mais 180
por estante, gastando no máximo 240 horas de marcenaria…". Se a leitura em voz alta soa
estranha para quem conhece a operação, o modelo está errado — e essa é a revisão mais barata
que existe.

## O código

A [etapa 01 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-01-formulacao)
traz os **dois** modelos lado a lado: o que maximiza margem e o que maximiza receita. As
restrições são as mesmas; muda uma linha.

```python
def modelo_margem(dados):
    prob = pulp.LpProblem("mix_producao_margem", pulp.LpMaximize)
    x = _variaveis(dados)
    prob += pulp.lpSum(dados["produtos"][p]["margem_reais"] * x[p] for p in x)
    _restricoes(prob, x, dados)
    return prob, x
```

Rodando os dois:

| | Plano | Margem | Receita | Folga de acabamento |
|---|---|---|---|---|
| **Modelo correto** (margem) | 30 mesas, 40 estantes | **R$ 13.800** | R$ 47.000 | 0 h |
| **Modelo errado** (receita) | 60 mesas, 0 estantes | R$ 13.200 | R$ 54.000 | **60 h** |

Duas leituras que valem a pena:

1. **O modelo errado fatura mais e ganha menos.** Ele não erra a conta: erra o alvo.
2. **A folga denuncia.** No plano correto os dois recursos ficam com folga zero — ambos estão
   apertados, e é isso que sustenta o resultado. No plano errado, 60 horas de acabamento ficam
   paradas. Folga grande num recurso que o dono jura ser gargalo é sinal de que o modelo está
   respondendo outra pergunta.

O solver, aqui, é caixa-preta de propósito: chamamos o HiGHS e aceitamos o número. Isso é uma
dívida deliberada, e ela é paga nos capítulos seguintes desta Parte — a geometria mostra
*onde* está a resposta, o Simplex mostra *como* ela é encontrada, e a dualidade mostra *o que
mais* aquela resposta estava dizendo o tempo todo.

## Quando não serve

Nenhum método é bom sem os seus limites. A formulação linear falha em quatro situações
concretas, e em cada uma há um destino declarado:

| Situação | Por que quebra | Para onde vai |
|---|---|---|
| **Decisão indivisível** — não dá para fabricar 30,4 mesas; abrir meia fábrica não existe | Quebra a **divisibilidade** | Programação inteira |
| **Decisão de sim-ou-não** — usar ou não um fornecedor, ativar ou não uma linha | Não é quantidade; é lógica | Variáveis binárias, na Parte de programação inteira |
| **Ganho de escala ou custo de setup** — o custo por unidade cai com o volume, ou há um custo fixo por lote | Quebra a **proporcionalidade** | Programação não linear, ou reformulação com binárias |
| **Dados que ninguém conhece** — a demanda do mês que vem é estimativa, não número | O modelo trata estimativa como certeza | Otimização sob incerteza |

Há um caso especialmente traiçoeiro: **arredondar a solução contínua**. Resolver com $x$
fracionário e arredondar para o inteiro mais próximo parece inofensivo e pode produzir um
plano **inviável** — ou viável e longe do ótimo. Arredondar não é resolver o problema inteiro;
é torcer.

## Fundamentos e fontes

As duas obras-base tratam formulação de maneiras que vale contrastar, porque a diferença é uma
decisão pedagógica, não estilo:

- **Lachtermacher** entra pela planilha e por casos de negócio, com o modelo emergindo do
  problema. Chega rápido à prática e paga o preço na estrutura: o vocabulário formal aparece
  depois, quando o leitor já formulou.
- **Arenales et al.** abrem a unidade de otimização linear com um catálogo de aplicações —
  mistura, transporte, planejamento da produção, corte — antes de qualquer método. A aposta é
  que o repertório de padrões vem primeiro.

Este handbook segue uma terceira via: **um caso só, percorrido até o fim**, com o repertório de
padrões deslocado para um capítulo próprio ao final desta Parte. A razão é carga cognitiva —
quem ainda não formulou um modelo inteiro não aproveita um catálogo de dez.

> **Dívida declarada.** O esqueleto de capítulo deste handbook pede 2 a 4 artigos científicos
> *traduzidos para decisões* nesta seção. Este capítulo não os tem: a varredura de literatura
> sobre ensino de formulação ainda não foi feita, e **inventar citação é pior do que admitir a
> lacuna** (constituição, Princípio III). A varredura está na fila do
> [Radar](../../radar/RADAR.md).

## Pratique

Quatro exercícios, em dificuldade crescente: reconhecer, formular, diagnosticar e — no último
— aplicar ao seu próprio problema.

<div data-bateria="cap07"></div>

## Assista

> ⏳ **Vídeo em confirmação.** A curadoria deste capítulo aponta para material aberto sobre
> modelagem de planejamento da produção em Programação Linear. A conferência de autoria e
> duração na fonte, e a escolha definitiva dentro do canal parceiro, estão pendentes — e o
> capítulo prefere dizer isso a publicar um crédito que não verificou. Ver a
> [Videoteca](../videoteca.md).

## Síntese — o que levar

- **Formular é escolher a pergunta.** O solver responde qualquer uma com a mesma confiança.
- **Quatro perguntas bastam:** o que se pode escolher, qual a única medida, o que limita, o que
  é dado.
- **Receita não é margem.** O erro mais comum de objetivo, e o mais caro, porque o resultado
  parece bom.
- **Confira as unidades dos dois lados.** Dez segundos por restrição.
- **Leia o modelo em voz alta.** Se soa estranho para quem conhece a operação, está errado.
- **A folga denuncia.** Recurso "gargalo" com folga grande é sintoma de modelo respondendo
  outra pergunta.
- **Todo modelo linear assume três coisas** — proporcionalidade, aditividade, divisibilidade —
  e saber qual delas quebrou é o que aponta o método seguinte.

## Verificação

Três perguntas abertas. Se você responde às três sem consultar o texto, os objetivos deste
capítulo estão cumpridos.

1. Uma transportadora quer "reduzir custo e melhorar o nível de serviço". Por que isso ainda
   não é uma função objetivo, e quais são as duas saídas possíveis? *(O1, O2)*
2. Um modelo de mix devolve um plano em que o recurso que a operação considera gargalo aparece
   com 40% de folga. Antes de acusar o solver, o que você investiga no modelo, e nesta ordem?
   *(O3)*
3. A fábrica passa a oferecer 5% de desconto para pedidos acima de 100 unidades. Qual das três
   hipóteses da Programação Linear isso quebra, e o que muda no seu plano de modelagem? *(O4)*

### Leitura executiva

Formular um modelo linear é decidir **qual pergunta** ele vai responder — a única parte do
trabalho que nenhum solver faz. O capítulo abre com um erro real: uma marcenaria que maximiza
receita em vez de margem obtém um plano viável, ótimo e R$ 600 por mês pior, deixando 60 horas
de acabamento paradas. A partir daí, quatro perguntas organizam toda formulação: o que quem
decide pode escolher (variáveis), qual é a única medida a otimizar (objetivo), o que limita as
combinações (restrições) e o que é dado e não escolhido (parâmetros). A verificação de unidades
dos dois lados de cada restrição e a leitura do modelo em voz alta são as duas revisões mais
baratas que existem. O modelo linear assume proporcionalidade, aditividade e divisibilidade —
e saber qual delas o seu problema quebra é o que indica o método seguinte: programação inteira,
não linear ou otimização sob incerteza.
