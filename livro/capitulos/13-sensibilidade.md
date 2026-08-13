# 13 — Análise de sensibilidade e pós-otimização

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Ler** um relatório de sensibilidade e dizer, para cada faixa, **o que exatamente ela
autoriza** — e o que ela não autoriza.

**O2.** **Diagnosticar** a leitura de faixa em modelo **degenerado**, onde o preço-sombra é
ambíguo, e explicar por que dois relatórios corretos podem discordar.

**O3.** **Decidir** se uma mudança de dado exige **resolver de novo** ou se a resposta já está no
relatório que você tem.

## O problema

O [capítulo 12](12-dualidade.md) terminou com uma dívida explícita. Ele mostrou que a CPU vale
R$ 50, mostrou que esse preço só vale entre **6 e 12** unidades de estoque, e disse: *nunca cite um
preço-sombra sem citar a faixa junto*. Depois mandou você para cá.

Então: sexta-feira de novo, o mesmo telefone. Só que agora a conversa é outra, e é a que acontece
de verdade nas empresas.

| Quem liga | O que pergunta |
|---|---|
| Compras | *"Consigo mais 4 pentes. Vale?"* |
| Comercial | *"Vou ter que dar 20% de desconto no Tipo 1. Muda o plano?"* |
| Financeiro | *"O custo do componente subiu. Preciso refazer tudo?"* |
| Diretoria | *"Quanto a mais eu ganho se dobrar a bancada?"* |

**Três dessas quatro perguntas você responde sem rodar nada.** Uma delas exige resolver de novo. O
capítulo inteiro é sobre distinguir quais são quais — porque em produção "resolver de novo" nem
sempre é barato, e porque responder "deixa eu rodar" a uma pergunta que já está respondida é o
jeito mais rápido de o modelo virar oráculo em vez de ferramenta.

O erro caro aqui tem uma forma específica, e é diferente do erro do capítulo 12:

> Alguém lê no relatório **"permitido aumentar: 50"** e não percebe que existem **duas famílias de
> faixa com os mesmos rótulos** — uma para o lucro do produto, outra para o estoque do recurso. A
> primeira diz até onde o **plano** aguenta. A segunda diz até onde o **preço** vale. Trocar uma
> pela outra produz uma decisão errada com um número certo.

## De onde isto veio — em dívida

Este capítulo **não tem a sua fonte primária**, e isso é dito aqui em vez de disfarçado.

**O que foi procurado**, na sessão de história desta Parte ([estudo 004](https://github.com/GHDaru/operationalresearchaibook/blob/main/estudos/004-historia-parte-II.md)),
em 2026-08-12: a origem da análise de sensibilidade em Programação Linear, por identificador.

**O que voltou:** trabalho de 1976 sobre **pós-otimalidade em programação inteira** (Geoffrion &
Nauss, `10.21236/ada023278`). É outro assunto — programação inteira não tem preço-sombra com a
mesma garantia, como este capítulo explica em [Quando não serve](#quando-não-serve) — e portanto
**não serve** como origem.

| Afirmação | Estado |
|---|---|
| A origem da análise de sensibilidade em Programação Linear | ❌ **procurada e não localizada** |
| A hipótese de que ela nasce nos próprios manuais, e não em artigo | ⏳ **plausível e não confirmada** — não sustenta nada neste capítulo |
| A origem dos nomes "preço-sombra" e "análise de sensibilidade" | ❌ procurada, não encontrada |

**O que se pode dizer sem fonte, porque é raciocínio e não história:** a pergunta desta seção não
é nova nem sofisticada. Assim que alguém teve um plano ótimo nas mãos, apareceu quem perguntasse
*"e se o dado estiver um pouco errado?"* — e a resposta pré-Simplex era a única disponível:
**resolver de novo com o outro número**. O ganho aqui é o mesmo do capítulo 12, e vem do mesmo
lugar: o quadro final **já contém** a resposta para uma vizinhança inteira de perguntas, e
percebê-lo dispensa a maioria das reexecuções.

> A **ideia reaproveitável** é essa, e ela sai da Pesquisa Operacional inteira: **antes de refazer
> a conta, pergunte se a conta que você já fez cobre o novo caso.** A maior parte das reexecuções
> em qualquer área é retrabalho por não se saber o alcance do resultado anterior.

Esta seção é curta de propósito. Inventar história é pior do que omiti-la, porque história
inventada soa bem.

## A intuição — duas famílias de faixa, e elas não se misturam

Tudo neste capítulo se resume a distinguir duas perguntas.

**Pergunta 1 — mexe no *lucro*.** *"Se o Tipo 1 render menos, eu continuo produzindo a mesma
coisa?"* Mudar um coeficiente do objetivo **inclina a reta de iso-lucro** que o capítulo 08
desenhou. Enquanto a inclinação não passar da inclinação de uma das arestas que se encontram no
seu vértice, **o vértice ótimo continua sendo o mesmo** — o plano não muda, só o lucro total.

**Pergunta 2 — mexe no *estoque*.** *"Se eu conseguir mais pentes, quanto eu ganho?"* Mudar um
lado direito **desloca uma das retas paralelamente**. O vértice se move, o plano muda, e o lucro
muda a uma taxa constante — **o preço-sombra** — enquanto forem as **mesmas duas restrições** a
sustentar o ótimo.

| | Mexe em | Geometria | O que a faixa protege |
|---|---|---|---|
| **Faixa do lucro** | coeficiente do objetivo | a reta de iso-lucro **gira** | **o plano** — as quantidades não mudam |
| **Faixa do estoque** | lado direito | a restrição **desliza** | **o preço** — a taxa continua a mesma |

Elas costumam aparecer no mesmo relatório, com rótulos parecidos ou idênticos. **Não são a mesma
coisa e não autorizam a mesma coisa.**

## A matemática

### Notação, e a convenção de sinal declarada

Este handbook põe na linha $z$ do quadro os valores $z_j - c_j$. Num problema de **maximizar**,
valor **negativo** significa que a variável ainda melhora o objetivo, e o quadro é final quando não
há nenhum negativo — foi assim no [capítulo 09](09-simplex.md).

> **Confira a convenção do seu relatório antes de interpretá-lo.** Implementações diferentes
> publicam o custo reduzido com sinais opostos, e um sinal trocado transforma "ainda vale a pena"
> em "não vale" sem mudar nenhum número.

### A faixa do estoque

Com todas as restrições $\le$, as colunas de folga do quadro final são $B^{-1}$. Somar $\Delta$ ao
estoque $i$ desloca as básicas por $\Delta$ vezes a coluna $i$ de $B^{-1}$, e a base continua
viável enquanto todas continuarem não negativas:

$$x_B + \Delta \cdot (B^{-1}e_i) \ \ge\ 0$$

Cada básica dá um limite para $\Delta$; a faixa é a interseção deles. É a fronteira **exata**, em
fração, sem varredura e sem resolver de novo.

### A faixa do lucro

Para uma variável **básica** na linha $r$, somar $\delta$ ao seu lucro desloca a linha $z$ em
$\delta \cdot a_{rk}$ em cada coluna $k$ **fora** da base. A otimalidade exige que todos continuem
não negativos:

$$(z_k - c_k) + \delta \cdot a_{rk} \ \ge\ 0 \qquad \text{para toda coluna } k \text{ fora da base}$$

Para uma variável **fora** da base é uma desigualdade só: ela entra no plano quando o próprio custo
reduzido dela zera.

Repare no que as duas fórmulas têm em comum: **nenhuma resolve um problema**. As duas leem o
quadro que você já tem. É por isso que o relatório de sensibilidade sai junto com a resposta, sem
custo adicional relevante.

## O relatório

O que segue é gerado pela [etapa 05 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-05-parte2),
para a montadora dos capítulos anteriores:

```
RELATÓRIO DE SENSIBILIDADE — formato do handbook
lucro do plano: 1100

PRODUTOS — até onde o lucro unitário pode variar sem mudar O PLANO
produto                 produzir    lucro   pode cair até  pode subir até
Tipo 1 (16 GB)                 8      100              75             150
Tipo 2 (32 GB)                 2      150             100             200

RECURSOS — até onde o estoque pode variar com O PREÇO ainda valendo
recurso                           estoque   usado   preço   pode cair até  pode subir até
CPUs                                   10      10      50               6              12
pentes de memória de 16 GB             12      12      50              10              20
```

**Este formato é do handbook, e a escolha é deliberada** ([ADR 0014](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0014-relatorio-de-sensibilidade-e-a-faixa-medida.md),
D1). O relatório de um solver de mercado empilha as duas famílias numa grade só, com os mesmos
rótulos nas duas — e é essa fusão visual que produz o erro que abre o capítulo. Aqui os dois blocos
têm títulos que dizem **o que cada faixa protege**.

### Lendo linha por linha

**"Tipo 1 · lucro 100 · de 75 a 150."** Enquanto o lucro unitário do Tipo 1 estiver entre R$ 75 e
R$ 150, **o plano continua sendo 8 e 2**. O lucro total muda; as quantidades, não. Se o comercial
der 20% de desconto — o lucro cai para R$ 80, dentro da faixa —, você não precisa rodar nada: o
plano é o mesmo e o lucro passa a ser $80(8) + 150(2) = 940$.

> **Precisão que quase todo texto omite, e ela custa uma frase.** Exatamente **na** fronteira da
> faixa, o plano continua ótimo mas **deixa de ser o único**. Com o lucro do Tipo 1 em R$ 75, os
> planos $(8,2)$ e $(0,6)$ rendem os dois R$ 900 — é o caso de múltiplos ótimos do
> [capítulo 10](10-casos-especiais.md), e qual deles o solver devolve é decidido pela regra de
> pivoteamento, não por você. Estritamente **dentro** da faixa, o plano é o mesmo e é único.

**"CPUs · estoque 10 · preço 50 · de 6 a 12."** Cada CPU a mais rende R$ 50, **até 12 unidades de
estoque**. Acima de 12, a próxima CPU vale zero — foi o telefonema do capítulo 12. Abaixo de 6, o
plano se apoia em outras restrições e o preço deixa de valer.

**"usado 10 · estoque 10."** As duas restrições estão **apertadas**: nada sobra. É coerente com
os dois preços serem positivos — [folgas complementares](12-dualidade.md#folgas-complementares--o-teorema-que-vira-faro),
do capítulo anterior.

### Os mesmos conceitos, com os nomes que você vai encontrar

Você vai ver estes conceitos com outros nomes, quase sempre em inglês. Esta tabela é de **nomes**,
não de layout.

| Neste handbook | Termo consagrado na literatura |
|---|---|
| preço-sombra | *shadow price*, *dual value* |
| custo reduzido | *reduced cost* |
| faixa do estoque | *right-hand side ranging* |
| faixa do lucro | *objective coefficient ranging* |
| pode subir até / pode cair até | *allowable increase* / *allowable decrease* |

> ⏳ **Dívida declarada, capturada em 2026-08-13.** Os termos acima são os da **literatura**, e são
> verificáveis. Os **rótulos exatos da interface** de cada produto comercial — que variam por
> versão e por idioma — **não foram conferidos em fonte oficial aberta** nesta rodada, e por isso
> não são publicados aqui. Um rótulo de produto é uma afirmação como qualquer outra.

## O algoritmo — as três perguntas da pós-otimização

Chegou uma mudança de dado. Faça as perguntas nesta ordem, e pare na primeira que responder.

**1. A mudança está dentro de uma faixa do relatório?**
→ Se sim, **você já tem a resposta**. Faixa de lucro: o plano é o mesmo, recalcule só o total.
Faixa de estoque: o lucro muda pelo preço-sombra vezes a variação.

**2. A mudança é de um dado que o relatório não cobre?**
→ Coeficiente **dentro** da matriz (o Tipo 2 passa a consumir 3 pentes), restrição nova, variável
nova. **Resolva de novo.** O relatório fala de objetivo e de lado direito; não fala da matriz.

**3. A mudança sai da faixa?**
→ **Resolva de novo**, e não tente extrapolar. Fora da faixa o preço-sombra costuma **cair**, e
usar o valor antigo superestima o ganho — que é exatamente o erro de R$ 350 do capítulo 12.

| A pergunta que chegou | Resposta |
|---|---|
| *"Mais 4 pentes, vale?"* | Já respondida: 12 + 4 = 16, dentro de $[10, 20]$ → +R$ 200 |
| *"Desconto de 20% no Tipo 1?"* | Já respondida: 80 está em $[75, 150]$ → plano igual, total R$ 940 |
| *"O Tipo 2 vai consumir 3 pentes"* | **Resolver de novo** — mudou a matriz |
| *"Dobrar a bancada?"* | **Resolver de novo** — a bancada nem está no modelo |

## Quando o preço é ambíguo

O [capítulo 10](10-casos-especiais.md) avisou que em **vértice degenerado** a leitura de
preço-sombra fica ambígua, e parou aí. Aqui isso é **exibido**.

### A instância

A montadora, mais uma restrição que **não muda nada**: a bancada de teste comporta 8 unidades por
dia, e o plano ótimo já produz exatamente 8 do Tipo 1.

$$\max\ 100x_1 + 150x_2 \quad \text{s.a.}\quad x_1 + x_2 \le 10,\quad x_1 + 2x_2 \le 12,\quad x_1 \le 8,\quad x_1, x_2 \ge 0$$

O ótimo continua $(8, 2)$ com R$ 1.100. Mas agora **três** restrições passam pelo mesmo ponto, e
no plano bastam duas para determinar um vértice. É a degenerescência.

### Dois analistas, dois relatórios, os dois certos

Rodando a **mesma implementação**, mudando **só a ordem em que as restrições foram digitadas**:

```
ordem CPU, pente, bancada    ponto ['8','2']  valor 1100
      preços: CPUs = 50 · pentes = 50 · horas de bancada = 0
ordem bancada, pente, CPU    ponto ['8','2']  valor 1100
      preços: horas de bancada = 25 · pentes = 75 · CPUs = 0
```

O primeiro relatório diz que a CPU vale R$ 50 e a bancada não vale nada. O segundo diz que a CPU
**não vale nada** e a bancada vale R$ 25. Mesmo modelo, mesmo plano, mesmo lucro.

**Nenhum dos dois está errado.** Ambos foram conferidos como soluções viáveis do dual, com o mesmo
custo:

```
y = ['50', '50', '0']         viável: True   b'y = 1100
y = ['0', '75', '25']         viável: True   b'y = 1100
y = ['25', '125/2', '25/2']   viável: True   b'y = 1100
```

A terceira linha é o ponto médio, e ela entrega o essencial: **o dual não tem um ótimo, tem um
segmento inteiro de ótimos**. Todo ponto entre os dois primeiros é um conjunto de preços legítimo.

### O que a pergunta tinha de errado

A pergunta "qual é *o* preço da CPU?" pressupõe que existe um. Meça diretamente, alterando o
estoque e resolvendo:

```
z(9) = 1050 · z(10) = 1100 · z(11) = 1100
derivada pela esquerda: 50 · pela direita: 0
```

**Perder uma CPU custa R$ 50. Ganhar uma CPU rende R$ 0.** O preço-sombra é uma derivada, e neste
ponto a derivada pela esquerda e pela direita **não coincidem** — então nenhum número único
responde, e o relatório escolhe um por acidente de implementação.

### O que fazer com isso

1. **Detecte.** Básica valendo zero no quadro final, ou faixa de estoque com um dos lados colado no
   valor atual. O capítulo 10 ensinou o sintoma.
2. **Não negocie com o número.** Em vértice degenerado, "a CPU vale 50" não é base para comprar.
3. **Pergunte dos dois lados.** *Quanto eu perco se tirar um* e *quanto eu ganho se puser um* são
   perguntas diferentes, e nesse ponto têm respostas diferentes. **As duas são acionáveis** — só
   não são o mesmo número.
4. **Procure a redundância.** Degenerescência costuma vir de restrição que não restringe. Se a
   bancada nunca limita, ela talvez não devesse estar no modelo — e sem ela o preço volta a ser
   único.

## O código

A [etapa 05 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-05-parte2)
regenera o relatório inteiro e a demonstração de ambiguidade, em aritmética exata. Três decisões
de engenharia que o capítulo herda:

1. **As faixas saem de álgebra, não de varredura.** Uma versão anterior varria o estoque de meio em
   meio e publicou duas faixas **erradas** no capítulo 12. O erro não era de precisão: a varredura
   media em que base o Simplex aterrissa, e não para que estoque a base continua ótima. Registrado
   na [ADR 0014](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0014-relatorio-de-sensibilidade-e-a-faixa-medida.md),
   D2.
2. **Toda faixa é conferida por um segundo caminho**, que põe o estoque na fronteira e um pouco
   além e exige que o preço **acerte na fronteira** e **erre além dela**. Faixa curta demais escapa
   de qualquer teste que só confira o valor certo.
3. **A demonstração de ambiguidade tem árbitro.** Os preços alternativos não são apresentados como
   "olha só": são **verificados** como soluções duais viáveis de mesmo custo, e a etapa encerra com
   erro se não forem.

> ### ▶ Rode você mesmo
>
> **[Abrir a Parte II no Google Colab](https://colab.research.google.com/github/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-II.ipynb)** · fonte em
> [`po-zero/cadernos/parte-II.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-II.ipynb)
>
> O caderno **não contém o algoritmo**: ele busca o código publicado e chama as mesmas funções que
> o `pytest` do repositório verifica — não há segunda cópia para envelhecer
> ([ADR 0016](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0016-cadernos-colab-sem-deriva.md)).
> Lá dentro você **roda o telefonema antes de ver a resposta**, mexe no lote de compra e vê a
> fronteira aparecer sozinha.
>
> **O Colab é conveniência, não dependência.** O mesmo caderno roda no seu terminal, e o
> experimento de verdade é o script em `po-zero/`, que roda em qualquer CPU sem licença paga.

## Quando não serve

**1. A faixa vale para uma mudança de cada vez.** Mexer em dois dados ao mesmo tempo pode sair da
região de validade mesmo com cada um dentro da sua faixa. Para mudanças simultâneas há regras mais
finas — e, na dúvida, resolver de novo é barato e honesto.

**2. Em vértice degenerado o número é ambíguo**, como a seção anterior mediu. A faixa também: um
dos lados fica colado no valor atual e o relatório não avisa.

**3. Nada disto vale em programação inteira.** A relaxação linear devolve preço-sombra e faixas, e
eles **não** descrevem o problema inteiro. Recurso a mais pode não render nada até completar uma
unidade indivisível. Levar a intuição deste capítulo para lá é o erro que o capítulo 23 vai tratar.

**4. O relatório não fala da matriz.** Mudou quanto cada produto **consome**, mudou uma restrição,
entrou produto novo: resolva de novo. Nenhuma faixa aqui cobre isso.

**5. Faixa é sobre o modelo, não sobre o mundo.** Ela diz até onde a **matemática** aguenta. Se o
lucro cair 25% porque o mercado virou, o modelo continua válido e a **pergunta** provavelmente
mudou — e nenhum relatório de sensibilidade avisa isso.

## Fundamentos e fontes

**O que está medido aqui.** O relatório inteiro, as duas faixas de cada produto e de cada recurso,
os três vetores de preços do exemplo degenerado e as derivadas pela esquerda e pela direita saem
todos da etapa 05 e se regeneram rodando um script.

**O que foi conferido no registro, e não lido.** Nada de novo neste capítulo: ele se apoia no
aparelho do [capítulo 12](12-dualidade.md), cuja fonte de dualidade é ✓ᵐ Gale, Kuhn e Tucker
(1951).

**O que continua em dívida:** a origem da análise de sensibilidade em Programação Linear, `❌`
procurada e não localizada, e a origem dos nomes. Ver [Em dívida](#de-onde-isto-veio--em-dívida),
no alto, e a [bibliografia](../bibliografia.md).

> 🟡 **Este capítulo está em v0.** O esqueleto está completo e todo número tem experimento que o
> regenera, mas ele **ainda não passou por revisão independente em contexto fresco**.

## Pratique

<div data-bateria="cap13"></div>

Três exercícios. O primeiro é de leitura pura — um relatório e o que ele autoriza. O segundo é o
caso degenerado, em que dois relatórios corretos discordam. O terceiro é a decisão que este
capítulo existe para treinar: **resolver de novo ou não?**

## Assista

**[Análise de Sensibilidade: Teoria — Dualidade, Programação Linear, Pesquisa
Operacional](https://www.youtube.com/watch?v=uaTbCLa-U60)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 27min42s

**O que ele resolve:** este capítulo entra pela leitura do relatório, que é o caminho de quem já
tem uma resposta na mão e precisa decidir. O vídeo faz o percurso inverso — deriva as faixas a
partir da álgebra do quadro — e fecha o círculo para quem quer ver de onde as duas fórmulas saem.
Há também um [vídeo de exercício resolvido](https://www.youtube.com/watch?v=LdyUG-Ds4sY) do mesmo
autor (33min46s), útil depois da bateria.

## Síntese — o que levar

- **Duas famílias de faixa, e elas não se misturam.** A do **lucro** protege o **plano**; a do
  **estoque** protege o **preço**. Rótulos parecidos, autorizações diferentes.
- **A maior parte das perguntas de "e se?" já está respondida** no relatório que você tem. Rodar de
  novo por reflexo é retrabalho.
- **Resolva de novo em três casos:** mudou a matriz, entrou restrição ou variável nova, ou a
  mudança **saiu da faixa**.
- **Fora da faixa, o preço costuma cair** — extrapolar superestima o ganho, e foi o prejuízo de
  R$ 350 do capítulo 12.
- **Em vértice degenerado não existe *o* preço.** O dual tem um **segmento** de ótimos, e o
  relatório escolhe um por acidente de implementação. Medido aqui: R$ 50 pela esquerda, R$ 0 pela
  direita.
- **A pergunta certa nesse caso é dos dois lados:** *quanto perco se tirar* e *quanto ganho se
  puser* são perguntas diferentes, e as duas são acionáveis.
- **Confira a convenção de sinal** do seu relatório antes de interpretá-lo.
- **Fora da Pesquisa Operacional:** antes de refazer a conta, pergunte se a conta que você já fez
  cobre o novo caso.

## Verificação

1. Um relatório informa, para um produto, "permitido aumentar: 30" e, para um recurso, "permitido
   aumentar: 30". As duas linhas autorizam a mesma coisa? Explique a diferença em uma frase cada.
   *(O1)*
2. Dois analistas rodam o mesmo modelo e apresentam preços-sombra diferentes, ambos com o mesmo
   plano e o mesmo lucro. Que hipótese você levanta, como confirma, e o que responde à diretoria
   que quer "o número"? *(O2)*
3. Chegam três mudanças: o lucro de um produto cai 10% (dentro da faixa), um recurso ganha 5
   unidades (a faixa permitia 3) e um produto passa a consumir mais matéria-prima. Para cada uma,
   diga se você resolve de novo, e por quê. *(O3)*

### Leitura executiva

O relatório de sensibilidade responde, sem custo adicional, a uma vizinhança inteira de perguntas
"e se?" — e a maior parte do valor está em **não** rodar o modelo de novo. Ele traz duas famílias
de faixa que costumam aparecer com rótulos parecidos e autorizam coisas diferentes: a **faixa do
lucro unitário** garante que, enquanto o coeficiente ficar dentro dela, **o plano não muda** (só o
total), e a **faixa do estoque** garante que, enquanto o lado direito ficar dentro dela, **o
preço-sombra continua valendo**, de modo que o lucro varia à taxa constante daquele preço. Na
montadora, o Tipo 1 pode render entre R$ 75 e R$ 150 sem que as quantidades mudem, e a CPU rende
R$ 50 por unidade enquanto o estoque estiver entre 6 e 12. Daí sai um procedimento de três
perguntas: se a mudança cai dentro de uma faixa, a resposta já existe; se ela toca a **matriz** —
quanto cada produto consome, uma restrição nova, uma variável nova —, resolva de novo, porque o
relatório não fala disso; e se ela **sai da faixa**, resolva de novo em vez de extrapolar, porque
fora da faixa o preço em geral cai e o valor antigo superestima o ganho. A limitação mais séria
aparece em **vértice degenerado**: ali o problema dual não tem um ótimo, tem um **segmento** de
ótimos, e dois relatórios corretos podem publicar preços diferentes — este handbook exibe o caso,
com a mesma implementação e só trocando a ordem em que as restrições foram digitadas, obtendo
"CPU vale 50 e bancada vale 0" e "CPU vale 0 e bancada vale 25", ambos verificados como soluções
duais viáveis de mesmo valor. Medindo diretamente, perder uma CPU custa R$ 50 e ganhar uma CPU
rende R$ 0: a derivada pela esquerda e pela direita não coincidem, e é a pergunta "qual é *o*
preço" que está mal feita. Nada disto vale em programação inteira, onde a relaxação linear devolve
faixas que não descrevem o problema real.
