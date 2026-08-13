# 05 — Complexidade computacional para quem modela

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Ler** uma afirmação de complexidade — "é NP-difícil", "o pior caso é exponencial" — e
dizer **sobre o que exatamente ela fala**, e sobre o que não fala.

**O2.** **Decidir** se vale tentar resolver ao ótimo, com base em medição da instância, e não na
classe do problema.

**O3.** **Reconhecer** os três usos errados da teoria da complexidade em conversa de projeto, e
dizer o que colocar no lugar de cada um.

## O problema

Este é o capítulo em que a teoria mais bonita da computação encontra o trabalho de quem modela, e
o encontro produz uma frase perigosa:

> *"Esse problema é NP-difícil, então vamos direto para uma heurística."*

A frase parece rigor. Ela é o contrário: é uma decisão de projeto tomada **sem medir nada**, com a
autoridade emprestada de um teorema que fala de outra coisa.

O erro caro deste capítulo:

> Alguém desiste do ótimo por causa da classe do problema, entrega uma heurística — que não vem
> com limitante — e nunca descobre que o solver resolveria aquela instância em quatro segundos.
> **O prejuízo é invisível**, porque não existe nada com que comparar.

O contrário também é caro, e este capítulo mede os dois lados: o pior caso **existe**, é
construível, e não some porque você o achou improvável.

> **Um aviso de pré-requisito, na mesma linha do que o [capítulo 01](01-o-que-e-po.md) faz.** A
> evidência desta página é medida **sobre o Simplex** — vértice, pivô, regra de pivoteamento —, e
> nada disso é apresentado aqui: é dos [capítulos 08](08-geometria.md) e [09](09-simplex.md). Se
> você está lendo a Parte I na ordem do sumário, o argumento continua de pé (o que importa é a
> **distância** entre as duas colunas de cada tabela), mas "63 pivôs" só ganha textura depois do
> capítulo 09. O handbook foi escrito fora de ordem de propósito, e prefere avisar a fingir.

## De onde isto veio

### O aperto: "esse algoritmo é bom" não queria dizer nada

Nos anos 1960 já havia algoritmos para todo tipo de problema combinatório, e não havia como
comparar honestamente dois deles. *"É rápido"* dependia da máquina, do programador e do exemplo
escolhido para demonstrar. A área precisava de um critério que não dependesse de nenhuma das três
coisas.

A proposta que pegou foi **tempo polinomial**: um algoritmo é "bom" se o número de operações
cresce como uma potência fixa do tamanho da entrada, e "ruim" se cresce exponencialmente. A
literatura credita a proposta a **Jack Edmonds**, em 1965, no artigo dos caminhos, árvores e
flores.

O critério é grosseiro de propósito — um algoritmo com $n^{100}$ operações é inútil na prática e
"bom" pela definição. Ele foi adotado porque é **robusto**: não muda quando você troca de máquina,
de linguagem ou de exemplo.

### A virada: descobrir que os problemas difíceis são o mesmo problema

O passo seguinte foi maior. Em 1971, **Stephen Cook** mostrou que existe um problema para o qual
qualquer problema de uma classe grande pode ser **traduzido** — e em 1972 **Richard Karp**
publicou uma lista de problemas combinatórios famosos, todos traduzíveis uns nos outros.

A consequência é o que dá à sigla NP o peso que ela tem: **não são muitos problemas difíceis
independentes; é um problema difícil usando muitas roupas.** Achar um algoritmo polinomial para um
deles seria achar para todos — e é por isso que ninguém espera que você ache.

### A ideia reaproveitável

> **Um critério grosseiro que não depende de quem mede vale mais do que um critério fino que
> depende.** Foi assim que "esse algoritmo é bom" passou a significar alguma coisa.

E o corolário, que é o assunto deste capítulo:

> **Uma classificação de pior caso não é uma previsão sobre a sua instância.** Ela é uma garantia
> sobre a pior instância que alguém consegue construir — e construir é o verbo certo.

### A origem do nome

**NP** não quer dizer *"não polinomial"*, e a confusão é tão comum que vale desfazer com todas as
letras. Quer dizer **não determinístico polinomial**: a classe dos problemas cuja **resposta**,
se alguém entregar uma, pode ser **conferida** em tempo polinomial. Conferir é fácil; achar é que
não se sabe.

### Procedência

| Afirmação | Estado |
|---|---|
| A atribuição do critério polinomial a Edmonds (1965) | ✓ᵐ **metadados conferidos** no Crossref; texto não lido — atribuição corrente |
| A atribuição da NP-completude a Cook (1971) e da lista de reduções a Karp (1972) | ✓ᵐ **metadados conferidos**; textos não lidos — atribuições correntes |
| O cubo de Klee–Minty e o seu comportamento | ✓ **medido** neste handbook, `po-zero/parte-I-fundamentos` e `etapa-03-simplex`. A fonte original de 1972 é ponteiro, e o livro **não depende** dela |
| Os números de pivôs desta página | ✓ **medidos**, com teste que compara o texto publicado à medição |
| O significado de "NP" como *não determinístico polinomial* | 📖 **leitura editorial** de definição de manual; não é afirmação empírica |

## O que a teoria diz, em uma tabela

| A afirmação | Sobre o que ela fala | Sobre o que ela **não** fala |
|---|---|---|
| *"O problema é NP-difícil"* | A classe inteira, no pior caso, quando o tamanho cresce | A sua instância de 300 variáveis |
| *"O algoritmo tem pior caso exponencial"* | A pior entrada que alguém consegue construir | A entrada que você tem |
| *"Não existe algoritmo polinomial conhecido"* | O estado do conhecimento | A existência de um; ninguém provou que não há |
| *"É polinomial"* | Que cresce como potência fixa | Que é rápido — $n^{100}$ é polinomial |

Três dessas quatro linhas são sobre **o pior caso**, e é aí que mora a distância entre a teoria e a
mesa de trabalho. As duas medições a seguir mostram a distância dos dois lados.

## O pior caso existe, e é construído

O Simplex é o exemplo didático perfeito, porque a sua reputação prática e a sua classificação
teórica **discordam**. Existe uma família de instâncias — o **cubo de Klee–Minty** — em que o
método, com a regra de pivoteamento clássica, visita **todos** os vértices antes de parar.

Medido aqui, em aritmética exata:

| $n$ | Vértices do cubo | Pivôs | $2^n - 1$ |
|---|---|---|---|
| 2 | 4 | **3** | 3 |
| 3 | 8 | **7** | 7 |
| 4 | 16 | **15** | 15 |
| 5 | 32 | **31** | 31 |
| 6 | 64 | **63** | 63 |
| 7 | 128 | **127** | 127 |

Não é aproximação nem tendência: é **exatamente** $2^n - 1$, em todos os tamanhos medidos. O pior
caso não é folclore.

### E ele não é frágil como se costuma dizer

Há uma frase que circula junto com esse resultado — *"tudo bem, o pior caso é frágil; qualquer
perturbaçãozinha desmancha"*. Ela vem de uma leitura apressada da **análise suavizada** de
Spielman e Teng (2004), que este handbook cita no [capítulo 09](09-simplex.md).

Testar essa frase é barato. **O modelo de perturbação importa e vai declarado**: cada coeficiente
não nulo da matriz vira $c \cdot (1 + \delta)$, com $\delta$ uniforme em
$[-\text{magnitude}, +\text{magnitude}]$, e **o padrão de zeros é preservado**. Com $n = 6$, cujo
caminho puro custa 63 pivôs, sobre **200 sementes por magnitude**:

| Perturbação relativa | Mediana de pivôs | Caminhos intactos |
|---|---|---|
| 0,1% | **63** | **200/200** |
| 1% | **63** | **200/200** |
| 10% | **63** | 147/200 |
| 25% | **49** | 18/200 |
| 50% | **33** | 2/200 |

**Perturbações pequenas não mudam nada** — e "nada" aqui é literal: em 0,1% e em 1%, as **200**
sementes devolvem os mesmos 63 pivôs. A partir de 10% o caminho **às vezes** encurta, e só em 25%
e 50% ele encurta com regularidade — quando a perturbação já é grande o bastante para a instância
ser, honestamente, outra instância.

> **Por que a tabela não publica mínimo e máximo**, e por que isso é o assunto e não um detalhe.
> Esta tabela já foi publicada duas vezes errado. Primeiro como **um sorteio por magnitude**, sem
> dizer que era um. Depois com mínimo e máximo de **20** sementes — e mínimo e máximo são
> estatísticas de ordem, que se mexem com o tamanho da amostra mesmo quando a distribuição não
> mudou: o máximo da linha de 50% vai de 47 para 63 só por passar de 20 para 200 sementes. A
> mediana e a fração de caminhos intactos ficam paradas. **A tabela publica o que estabiliza.**

### O eixo que a tabela acima não olha

A tabela mede um tamanho só, e o teorema de 2004 faz a sua afirmação sobre o **crescimento em
$n$**. Ignorar esse eixo seria discutir um resultado assintótico com uma medição cega ao
assintótico. Fração de caminhos intactos, 25 sementes por célula:

| Perturbação | $n=4$ | $n=5$ | $n=6$ | $n=7$ | $n=8$ |
|---|---|---|---|---|---|
| 1% | **25/25** | **25/25** | **25/25** | **25/25** | **25/25** |
| 10% | 25/25 | 23/25 | 20/25 | 13/25 | 7/25 |

Duas leituras, e as duas importam. A de **1%** é a que sustenta o capítulo: o caminho fica intacto
em todos os tamanhos medidos — a perturbação pequena não desmancha o pior caso, e não desmancha
mais à medida que o cubo cresce. A de **10%** vai na direção que a análise suavizada prevê: quanto
maior o cubo, mais fácil quebrar o caminho. **Isso é a favor do teorema, não contra** — e é a razão
de esta tabela existir aqui.

> **O que esta medição não autoriza concluir.** Ela **não** refuta o resultado de 2004. Aquele
> teorema é assintótico, vale **em esperança**, sob perturbação gaussiana e com uma regra de
> pivoteamento específica — e nenhuma das três condições vale nas tabelas acima. O que a medição
> refuta é a **frase de corredor**, que trata um teorema delicado como se dissesse *"mexeu um
> pouco, melhorou"*. Não diz.

## A sua instância não é o pior caso

Do outro lado da distância está o número que decide o projeto. Instâncias aleatórias do **mesmo
tamanho** do cubo, sem nenhuma malícia — coeficientes inteiros pequenos, todas as restrições `≤`,
**200 amostras por tamanho**:

| $n = m$ | Mediana de pivôs | Pior das 200 | O cubo do mesmo tamanho |
|---|---|---|---|
| 5 | **2** | 6 | 31 |
| 10 | **4** | 12 | 1.023 |
| 15 | **5** | 16 | 32.767 |
| 20 | **7** | 19 | 1.048.575 |

Aqui o **máximo é publicado**, ao contrário da tabela de perturbação, e a diferença tem razão: é
ele que faz o argumento. Dizer que a **pior** de 200 instâncias de tamanho 20 custou 19 pivôs, onde
o cubo do mesmo tamanho custa mais de um milhão, é mais forte do que dizer que a mediana custou 7.

> **E o nome da última coluna mudou de propósito.** Ela dizia "pior caso teórico", e não é isso:
> $2^n-1$ é o custo do cubo de Klee–Minty, um pior caso **construído** para uma regra de
> pivoteamento específica. O número de vértices que um poliedro daquele tamanho **pode** ter é
> muito maior. Num capítulo cujo primeiro objetivo é dizer sobre o que exatamente uma afirmação
> fala, o rótulo escorregava.

> **Cuidado com o que esta tabela sustenta.** Ela mede instâncias **aleatórias com esta receita**,
> e problemas reais não são aleatórios — são estruturados, e a estrutura pode ajudar ou atrapalhar.
> O que a tabela sustenta é a negação de uma inferência, não a afirmação de uma regra: **da
> classificação de pior caso não se deduz o custo da sua instância**. Para saber o custo da sua,
> rode a sua.

> ### ▶ Rode você mesmo
>
> **[Abrir a Parte I no Google Colab](https://colab.research.google.com/github/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-I.ipynb)** · fonte em
> [`po-zero/cadernos/parte-I.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-I.ipynb)
>
> O caderno **não contém o algoritmo**: ele busca o código publicado e chama as mesmas funções que
> o `pytest` do repositório verifica — não há segunda cópia para envelhecer
> ([ADR 0016](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0016-cadernos-colab-sem-deriva.md)).
> Lá dentro você **dá o seu palpite sobre a perturbação antes de ver o resultado**, e depois muda
> o tamanho da instância aleatória para ver a distância abrir.

## Os três usos errados, e o que pôr no lugar

| O uso errado | Por que é errado | O que pôr no lugar |
|---|---|---|
| *"É NP-difícil, vamos de heurística"* | Decide sem medir; joga fora o limitante que só o método exato dá | **Rode o exato com limite de tempo.** Se em 10 minutos o *gap* for 0,4%, acabou a conversa |
| *"O Simplex é exponencial, use pontos interiores"* | Confunde pior caso com desempenho típico; e o [capítulo 14](14-pontos-interiores.md) mostrou que a escolha se faz pela instância | **Meça as duas** na sua instância, e escolha pelo que o seu problema pede — inclusive preço-sombra, que o interior não dá |
| *"É polinomial, então cabe"* | Polinomial não é rápido, e a constante não aparece na notação | **Meça o tempo real** no tamanho que você tem, e no dobro dele |

**A ordem que este capítulo defende, e ela é curta:** modele, jogue no solver exato com limite de
tempo, olhe o *gap*, e **só então** decida se precisa de outra coisa. A teoria da complexidade
entra depois, para explicar o que você viu — não antes, para decidir o que você nem tentou.

## Quando não serve

**1. Quando o tamanho é grande de verdade e o relógio é curto.** Se a instância tem milhões de
variáveis e a decisão é de hoje, a medição que este capítulo pede não cabe. Aí a classificação
teórica é o único guia disponível — e usá-la é legítimo, desde que dito.

**2. Quando o problema nem chega a ser formulável.** Complexidade fala de problemas bem definidos.
Um problema cuja função objetivo ninguém consegue escrever não é difícil no sentido da teoria: é
outra coisa, e o [capítulo 03](03-anatomia-do-modelo.md) trata dela.

**3. Quando a dificuldade real não é computacional.** Muito projeto trava no dado que não existe,
no prazo, ou em quem não vai confiar no resultado. Nenhum desses aparece numa classe de
complexidade, e todos derrubam projeto — é a lista do [capítulo 02](02-ciclo-de-modelagem.md).

**4. Quando o que se quer é uma garantia formal, e não um número.** Se a pergunta é *"existe
algoritmo polinomial para isto?"*, medir instâncias não responde. Aí a teoria não é o guia errado:
é o único.

## Fundamentos e fontes

**O que está medido aqui.** Tudo o que é número nesta página: os pivôs do cubo de Klee–Minty para
$n$ de 2 a 7, a distribuição de perturbação com $n = 6$ sobre **200 sementes** por magnitude, a
varredura em $n$ com 25 sementes por célula, e o perfil de **200 instâncias aleatórias** por
tamanho, para $n = 5, 10, 15, 20$. O código está em `po-zero/parte-I-fundamentos/complexidade.py`, roda em
aritmética exata (`Fraction`), declara semente, e há teste que compara **este texto** à medição.

**O que entra por fonte, e como:** Edmonds (1965), Cook (1971) e Karp (1972) entram `✓ᵐ` —
**metadados conferidos no Crossref, conteúdo não lido**. As atribuições que este capítulo faz a
eles são apresentadas como **correntes**, e estão registradas assim na
[bibliografia](../bibliografia.md). O artigo original de Klee e Minty (1972) não tem DOI localizado
e fica como ponteiro: **o handbook não depende dele**, porque constrói e mede o cubo.

> 🔵 **Este capítulo está em "medido".** Os números têm experimento que os regenera e teste que os
> compara ao texto publicado. O que falta para ✅ é revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap05"></div>

Três exercícios. O primeiro separa o que uma afirmação de complexidade diz do que ela não diz; o
segundo é a decisão de projeto com números na mesa; o terceiro pega os três usos errados em
conversa real.

## Assista

**[Complexidade e Classes de Problemas em Otimização: P, NP, NP-completo, NP-difícil, Redução, Provas](https://www.youtube.com/watch?v=ApRmVUOOY_o)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 29min56s

**O que ele resolve:** este capítulo é deliberadamente **anti-teórico** — ele usa a teoria para
decidir o que fazer na segunda-feira, e por isso não define classe nenhuma com rigor. O vídeo faz
exatamente o que falta aqui: define P, NP, NP-completo e NP-difícil, e mostra o que é uma redução,
que é a peça que dá sentido à frase "é um problema difícil usando muitas roupas".

## Síntese — o que levar

- **NP quer dizer *não determinístico polinomial***, não "não polinomial". É a classe do que se
  **confere** rápido.
- **Afirmação de complexidade é sobre a classe no pior caso**, não sobre a sua instância.
- **O pior caso existe e é construído.** Medido: o cubo de Klee–Minty custa exatamente $2^n - 1$
  pivôs, de $n = 2$ a $n = 7$.
- **E não é frágil como se diz.** Medido em 200 sementes por magnitude: com $n = 6$, perturbar a
  matriz em 0,1% ou 1% deixa os 63 pivôs intactos nas **200 de 200** — e a 1% isso vale em todos os
  tamanhos medidos, de $n=4$ a $n=8$.
- **A sua instância provavelmente está longe do pior caso.** Medido em 200 instâncias por tamanho:
  mediana de 2 a 7 pivôs, e a **pior** de 200 no tamanho 20 custou 19 — contra o cubo de
  Klee–Minty do mesmo tamanho, que custa mais de um milhão.
- **Da classe não se deduz o custo da sua instância.** Para saber o custo da sua, rode a sua.
- **A ordem certa:** modele, rode o exato com limite de tempo, olhe o *gap*, e só então decida.
- **Fora da Pesquisa Operacional:** um critério grosseiro que não depende de quem mede vale mais
  do que um critério fino que depende.

## Verificação

1. Um artigo diz que o problema de roteirização é NP-difícil. Um colega conclui que "não adianta
   tentar o ótimo". Aponte o salto lógico, e diga que informação faltaria para a conclusão dele
   ficar de pé. *(O1)*
2. Você tem uma instância com 400 variáveis binárias e três dias de prazo. Descreva, em quatro
   passos, o que você faz **antes** de decidir entre exato e heurístico — e diga qual número decide.
   *(O2)*
3. Numa reunião, alguém diz: *"o Simplex é exponencial, então vamos de pontos interiores"*. O que
   está errado na frase, e o que você propõe? *(O3)*

### Leitura executiva

Afirmações de complexidade computacional — *"é NP-difícil"*, *"o pior caso é exponencial"* — falam
sobre **a classe do problema no pior caso**, e não sobre a instância que está na sua mesa. A
distinção não é filosófica: ela decide projeto. Usar a classificação para não tentar o ótimo é
tomar uma decisão sem medir nada, com a autoridade emprestada de um teorema que fala de outra
coisa — e o prejuízo é invisível, porque quem desiste do método exato fica sem o limitante que
permitiria saber o que perdeu. Este capítulo mede os dois lados da distância. De um lado, **o pior
caso é real e construível**: o cubo de Klee–Minty faz o Simplex com a regra clássica visitar todos
os vértices, e a medição em aritmética exata devolve exatamente $2^n-1$ pivôs para $n$ de 2 a 7.
Ele também **não é frágil** como a conversa de corredor sugere: medido em 200 sementes por
magnitude, perturbar a matriz em 0,1% ou 1% deixa os 63 pivôs de $n=6$ intactos nas duzentas — e a
1% isso se mantém de $n=4$ a $n=8$ —, enquanto a 10% o caminho já quebra às vezes, e quebra mais
quanto maior o cubo. Nada disso refuta a análise suavizada de 2004, que é assintótica, vale em
esperança e supõe outra regra de pivoteamento; refuta a leitura popular dela. Do outro lado,
**instâncias aleatórias do mesmo tamanho ficam muito longe do caso construído**: a mediana vai de 2
a 7 pivôs e a pior de 200 instâncias de tamanho 20 custou 19, contra o cubo de Klee–Minty do mesmo
tamanho, que custa mais de um milhão. A conclusão prática é uma ordem de
trabalho, não uma teoria: modele, rode o método exato com limite de tempo, olhe o *gap* que ele
reporta, e **só então** decida se precisa de outra coisa. A teoria da complexidade entra depois,
para explicar o que você viu — não antes, para decidir o que você nem tentou. Ela volta a ser o
único guia disponível em quatro situações declaradas: quando a instância é enorme e o relógio é
curto, quando o problema nem chega a ser formulável, quando a dificuldade real não é computacional,
e quando a pergunta é formal — *"existe algoritmo polinomial para isto?"* —, caso em que medir
instâncias não responde nada.
