# 06 — Ferramentas de trabalho

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Montar** o ambiente do `po-zero` e resolver o primeiro modelo, com solver aberto e
custo zero.

**O2.** **Ler uma saída de solver com desconfiança calibrada**: saber o que nela é decisão do
modelo, o que é decisão da ferramenta e o que é ponto flutuante.

**O3.** **Separar modelo de dados** ao escrever, e dizer o que essa separação compra.

## O problema

O [capítulo 05](05-complexidade.md) termina com uma instrução: *rode o método exato com limite de
tempo e leia o `gap` antes de decidir qualquer coisa*. Esta página é onde se monta o que roda — e
onde se aprende a **ler** o que ele devolve.

É o capítulo mais fácil de escrever mal, porque a tentação é entregar um folheto: *instale
isto, escreva assim*. Folheto envelhece e não ensina nada. O que este capítulo faz, em vez disso,
é medir **três coisas que separam quem lê uma saída de solver de quem confia nela**.

O erro caro deste capítulo:

> Duas pessoas resolvem o **mesmo modelo** por caminhos diferentes e conferem: o valor bate. Elas
> concluem que a resposta é a mesma. **Não é.** Este capítulo mede um caso em que o valor é 10 nos
> dois e os planos são **(6, 4)** e **(2, 8)** — e é o plano que alguém vai executar na
> segunda-feira.
>
> Repare no que a medição diz e no que ela não diz: os dois solvers testados aqui **concordaram**
> entre si. A divergência apareceu entre o Simplex didático e eles. A desconfiança certa não é
> *"cuidado ao trocar de solver"* — é *"cuidado quando a face ótima é um segmento"*, seja qual for
> o caminho.

> **Mesmo aviso de pré-requisito do [capítulo 05](05-complexidade.md).** *Face ótima*, *base* e
> *custo reduzido* aparecem aqui como ferramentas de leitura e são apresentados nos
> [capítulos 08](08-geometria.md) a [10](10-casos-especiais.md). O que esta página exige de fato é
> saber rodar um modelo e olhar a saída — o resto ganha textura depois.

## De onde isto veio

### O aperto: o modelo e os dados eram o mesmo arquivo

Nos primeiros anos, escrever um modelo era escrever a **matriz** — números arrumados num formato
que o solver lia. Não havia distinção entre a estrutura do problema e os dados daquela instância:
mudar o preço de um insumo era editar um arquivo de números, e ninguém conseguia ler o modelo
para conferir se ele estava certo.

O sintoma é reconhecível hoje em qualquer planilha grande: **o modelo existe, mas ninguém consegue
enunciá-lo**, porque ele está distribuído entre células.

### A virada: a linguagem de modelagem

A virada foi criar uma notação em que se escreve o modelo **como ele se escreve na matemática** —
somatórios, índices, conjuntos — e se lê os dados de outro lugar. É a ideia da AMPL, publicada em
1990 por Fourer, Gay e Kernighan, e é a que está por trás do PuLP e do Pyomo que este handbook
usa.

O ganho não é de digitação. É que **o modelo passa a caber numa página** e a poder ser lido em voz
alta — o que significa que ele pode ser **conferido por quem entende do negócio** e não entende de
otimização.

### A ideia reaproveitável

> **Separar a estrutura dos dados transforma um artefato que se executa num artefato que se
> discute.**

É a mesma ideia do [capítulo 03](03-anatomia-do-modelo.md), agora do lado da ferramenta: lá,
separar variável de parâmetro; aqui, separar modelo de instância. E vale muito além: é por isso
que consulta parametrizada, template e configuração existem.

### A origem dos nomes

Quatro nomes atravessam este capítulo, e nenhum deles é arbitrário:

- **AMPL** — *A Mathematical Programming Language*. O nome declara a ambição: não uma biblioteca,
  uma **língua** em que o modelo é escrito.
- **PuLP** — *Python Linear Programming*. A biblioteca faz o que o nome diz, e nada além.
- **CBC** — *Coin-or Branch and Cut*, do projeto **COIN-OR** (*Computational Infrastructure for
  Operations Research*), a iniciativa que reuniu solvers abertos de Pesquisa Operacional sob um
  teto comum.
- **HiGHS** — de *High performance software for linear optimization*. É o mais recente dos quatro,
  e o solver padrão deste handbook.

> **Nome inexplicado é ruído que o leitor memoriza sem ganhar nada.** As quatro expansões vêm da
> documentação dos próprios projetos, e são a única coisa deste capítulo que não é medição.

### Procedência

| Afirmação | Estado |
|---|---|
| A atribuição da separação modelo/dados à AMPL (Fourer, Gay, Kernighan, 1990) | ✓ᵐ **metadados conferidos** no Crossref; texto não lido — atribuição corrente |
| Que o HiGHS descende do trabalho de Huangfu e Hall sobre o Simplex dual revisado | ✓ᵐ **metadados conferidos**; texto não lido — atribuição corrente |
| Os três resultados medidos nesta página | ✓ **medidos** aqui, com teste que compara o texto publicado à medição |
| Que "o modelo estava distribuído entre células da planilha" seja o quadro histórico geral | 📖 **leitura editorial** — descreve um padrão reconhecível, não um levantamento |

## A pilha, e por que cada peça

| Camada | A escolha | Por quê |
|---|---|---|
| Linguagem | **Python 3.11+** | É o que quem estuda já tem instalado |
| Modelagem | **PuLP** para começar; **Pyomo** quando o modelo cresce | PuLP tem a menor distância entre a notação matemática e a primeira linha que roda |
| Solver | **HiGHS** (padrão), **CBC** como alternativa | Abertos, sem licença, instalados por `pip` |
| Numérico | NumPy | Para as implementações didáticas dos algoritmos |

**Solver comercial pode aparecer como comparação, nunca como dependência.** Custo zero é
requisito deste handbook, e não preferência — a decisão e as alternativas estão no
[ADR 0003](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0003-stack-po-zero.md).

### Montar o ambiente

```bash
git clone https://github.com/GHDaru/operationalresearchaibook.git
cd operationalresearchaibook
python3 -m venv .venv && source .venv/bin/activate
pip install -r po-zero/requirements.txt
python3 -m pytest po-zero -q          # deve ficar verde
```

> **Este bloco não é decorativo.** O mesmo `po-zero/requirements.txt` é o que a integração
> contínua instala a cada envio, e a mesma suíte é a que ela roda. Instrução de instalação que
> ninguém executa envelhece em silêncio — esta é executada automaticamente, e quando quebra o
> build fica vermelho. Ela **já quebrou**, e o [Histórico](../HISTORICO.md) conta como.

## As três coisas que só se aprendem medindo

### 1. Com múltiplos ótimos, a ferramenta escolhe o seu plano

Um modelo minúsculo, com face ótima inteira: maximizar $A + B$ sujeito a $A + B \le 10$,
$A \le 6$, $B \le 8$. Todo ponto do segmento entre $(2,8)$ e $(6,4)$ vale 10.

| Como foi resolvido | Plano devolvido | Valor |
|---|---|---|
| Simplex didático, aritmética exata | **A = 6, B = 4** | 10 |
| PuLP + HiGHS | **A = 2,0, B = 8,0** | 10,0 |
| PuLP + CBC | **A = 2,0, B = 8,0** | 10,0 |

Nenhum está errado — os três são ótimos. Mas **o relatório vai dizer "10" nos três casos, e a
fábrica vai executar coisas diferentes**. Quem apresenta um plano de produção sem saber que a
face ótima existe está apresentando uma escolha do solver como se fosse uma conclusão do modelo.

> **O que fazer com isso**, e é curto: quando o resultado importar, **teste se há múltiplos
> ótimos**. O [capítulo 10](10-casos-especiais.md) mostra como reconhecê-los no quadro final —
> custo reduzido zero numa variável fora da base. Se houver, a escolha entre os planos empatados
> volta para quem decide, com um segundo critério declarado.

### 2. Nenhum solver de produção devolve a fração

O modelo da ração do [capítulo 15](15-modelagem-aplicada.md) tem ótimo exato em **780/17**, que
não tem representação decimal finita.

| Como foi resolvido | Custo reportado | Erro em relação a 780/17 |
|---|---|---|
| Simplex didático, `Fraction` | **780/17** | 0 — é a fração |
| PuLP + HiGHS | 45.88235294117647 | 4,18 × 10⁻¹⁶ |
| PuLP + CBC | 45.882352 | 9,41 × 10⁻⁷ |

> **As versões que produziram esses dígitos**, porque a seção seguinte manda declará-las e seria
> constrangedor não fazê-lo aqui: Python 3.11.15, PuLP 3.3.2, HiGHS
> 1.15.1, e o CBC **embutido no PuLP 3.3.2** — o binário vem embutido, então a
> versão honesta é a do pacote que o empacota. Todas saem de `resultados-ferramentas.json`, e há
> teste que fica vermelho se o capítulo e o arquivo divergirem.

Os dois solvers estão certos e **discordam entre si**. A diferença não é de qualidade do
algoritmo: é de quantas casas cada ferramenta escreve na sua saída — **14 contra 6**, e portanto
oito dígitos em que as duas saídas divergem. Oito casas decimais não mudam decisão nenhuma numa
ração — **mudam quando alguém compara duas saídas com `==`**, ou quando o número entra numa conta
que o amplifica.

> **A regra prática:** nunca compare saídas de solver por igualdade exata; compare com tolerância,
> e declare a tolerância. E ao publicar um número, diga a ferramenta e a versão que o produziu.

### 3. Os vereditos concordam — e isso também é resultado

| Situação | Simplex didático | HiGHS | CBC |
|---|---|---|---|
| Região sem teto na direção do objetivo | `ilimitado` | `Unbounded` | `Unbounded` |
| Restrições contraditórias | `inviavel` | `Infeasible` | `Infeasible` |

**Boa notícia, e vale registrar como notícia:** o *diagnóstico* não depende da ferramenta. Se o
seu solver disse `Infeasible`, trocar de solver não vai resolver — o problema é o modelo, e é o
[capítulo 10](10-casos-especiais.md) que trata dele. Muita hora se perde trocando de ferramenta
diante de um veredito que é sobre o modelo.

> ### ▶ Rode você mesmo
>
> **[Abrir a Parte I no Google Colab](https://colab.research.google.com/github/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-I.ipynb)** · fonte em
> [`po-zero/cadernos/parte-I.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-I.ipynb)
>
> As três tabelas desta seção saem de duas células do caderno — inclusive a do empate, em que você
> vê o Simplex exato e os dois solvers devolverem planos diferentes com o mesmo valor. O caderno
> **não contém o algoritmo**: chama o código publicado, que o `pytest` já verifica
> ([ADR 0016](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0016-cadernos-colab-sem-deriva.md)).

## Modelo e dados, na prática

A regra é curta e paga cedo:

- **O modelo não contém número de instância.** Nenhum preço, nenhuma capacidade, nenhum nome de
  produto escrito no meio do código.
- **A instância é um arquivo**, com **ficha**: de onde veio, sob que licença, e o que ela não
  representa. É o que o `po-zero` exige de toda instância, e é a razão de a montadora dos
  capítulos 07 e 08 morar em `instancias/montadora.json` e não dentro do script.
- **A saída declara as versões.** Todo `resultados.json` deste handbook diz em que Python e com
  que solver foi produzido — sem isso, "eu rodei e deu outro número" é uma conversa sem fim.

**O teste que revela se a separação existe:** troque a instância por outra do mesmo formato. Se
for preciso editar o código, ela não existe.

## Quando não serve

**1. Quando a ferramenta não é o problema.** É a armadilha central deste capítulo. Modelo que
devolve `Infeasible` não melhora com outro solver; modelo com a variável de decisão errada
([capítulo 03](03-anatomia-do-modelo.md)) roda perfeitamente em qualquer um. Trocar de ferramenta
diante de um defeito de modelagem é o gesto mais caro deste livro, porque **parece progresso**.

**2. Quando a escala pede outra coisa.** PuLP escreve o modelo inteiro em memória e o entrega ao
solver. Em modelos com milhões de restrições, isso deixa de caber, e a conversa passa a ser sobre
geração de colunas, Pyomo com blocos, ou interface direta com o solver — que este handbook não
cobre na v0.

**3. Quando o custo zero deixa de valer a pena.** Solver comercial existe e às vezes ganha por
margem larga em classes específicas. A régua deste handbook é declarada: custo zero é requisito
**da trilha padrão**, e comparar com comercial é legítimo desde que a comparação seja medida, e
não citada.

**4. Quando a decisão nem chega ao solver.** Se ninguém vai implantar, a ferramenta é irrelevante
— e essa checagem é do [capítulo 02](02-ciclo-de-modelagem.md).

## Fundamentos e fontes

**O que está medido aqui.** Os três blocos: os planos empatados com valor 10, os custos reportados
para a ração com o erro de cada um, e a concordância dos vereditos. O código está em
`po-zero/parte-I-fundamentos/ferramentas.py`, e há teste que compara **este texto** à medição. As
versões estão em `resultados-ferramentas.json`.

**O que entra por fonte:** Fourer, Gay & Kernighan (1990) e Huangfu & Hall (2017) entram `✓ᵐ` —
**metadados conferidos no Crossref, conteúdo não lido** —, e as atribuições que o capítulo faz a
eles aparecem como **correntes**.

> 🔵 **Este capítulo está em "medido".** Os números têm experimento que os regenera e teste que os
> compara ao texto publicado. O que falta para ✅ é revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap06"></div>

Três exercícios. O primeiro é de ambiente e primeira execução; o segundo lê três saídas de solver
e separa o que é decisão do modelo do que é decisão da ferramenta; o terceiro pega um script real
em que modelo e dados estão grudados, e cobra a separação.

## Assista

**[Solver Excel e lp_solve: Softwares de Otimização - Programação Linear - Pesquisa Operacional](https://www.youtube.com/watch?v=sWhYRauuvEA)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 25min54s

**O que ele resolve:** este capítulo assume Python e mede o que muda entre solvers. O vídeo cobre
o outro extremo do espectro de ferramenta — o Solver do Excel e o `lp_solve` —, que é onde a
maioria das pessoas em empresa de fato encontra otimização pela primeira vez. Ver o mesmo modelo
numa planilha ajuda a entender por que a separação entre modelo e dados é uma conquista, e não uma
formalidade.

## Síntese — o que levar

- **A pilha é aberta e de custo zero:** Python, PuLP (ou Pyomo), HiGHS (ou CBC), NumPy.
- **Com múltiplos ótimos, a ferramenta escolhe o seu plano.** Medido: valor 10 nos três, planos
  (6, 4) e (2, 8).
- **Nenhum solver de produção devolve a fração.** Medido: 780/17 vira 45.88235294117647 no HiGHS
  e 45.882352 no CBC — **14 casas contra 6**, os dois certos e discordantes. Quem devolve a fração
  é o Simplex didático, em aritmética exata, e é por isso que ele serve de referência e não de
  ferramenta.
- **Nunca compare saídas de solver com `==`.** Compare com tolerância, e declare a tolerância.
- **Os vereditos concordam.** `Infeasible` não se resolve trocando de solver — é o modelo.
- **Modelo não contém número de instância**, e instância tem ficha. O teste: trocar a instância
  sem editar código.
- **Trocar de ferramenta diante de defeito de modelagem parece progresso e não é.**
- **Fora da Pesquisa Operacional:** separar estrutura de dados transforma um artefato que se
  executa num artefato que se discute.

## Verificação

1. Você clonou o repositório e `python3 -m pytest po-zero -q` falhou na primeira linha, com
   `ModuleNotFoundError`. Qual é o passo que faltou, e por que ele não pode ser adivinhado a
   partir do código? *(O1)*
2. Dois colegas resolveram o mesmo modelo com solvers diferentes e reportaram o mesmo valor
   objetivo. Um deles conclui que "a resposta é a mesma". Diga em que condição ele está certo, em
   que condição está errado, e como distinguir os dois casos. *(O2)*
3. Um script tem os preços dos insumos escritos no meio da função que monta o modelo. Descreva a
   mudança que separa modelo de dados e o **teste** que comprova que a separação aconteceu. *(O3)*

### Leitura executiva

A pilha de trabalho deste handbook é aberta e de custo zero — Python, PuLP para escrever o modelo,
HiGHS como solver padrão e CBC como alternativa — e a instalação é uma linha, contra um arquivo de
dependências que a integração contínua executa a cada envio, de modo que uma instrução quebrada
fica vermelha em vez de envelhecer em silêncio. O que separa este capítulo de um folheto são três
resultados medidos, e todos os três mudam o modo como se lê uma saída de solver. O primeiro: **com
múltiplos ótimos, a ferramenta escolhe o seu plano.** Num modelo cuja face ótima é um segmento
inteiro, o Simplex didático devolve o plano (6, 4) e os dois solvers devolvem (2, 8) — todos
ótimos, todos com valor 10, e é o **plano**, não o valor, que alguém vai executar. O segundo:
**nenhum solver de produção devolve a fração.** O ótimo exato da ração é 780/17, e o HiGHS reporta
45.88235294117647 enquanto o CBC reporta 45.882352 — 14 casas contra 6, e portanto oito dígitos de
divergência. Os dois estão certos, e a diferença não muda decisão nenhuma — até alguém comparar
duas saídas com igualdade exata. A
regra que fica é comparar com tolerância declarada, e publicar sempre a ferramenta e a versão. O
terceiro é boa notícia e também é resultado: **os vereditos concordam.** `Unbounded` e `Infeasible`
saem iguais nas três implementações, o que significa que um diagnóstico não se conserta trocando de
solver — quando o solver diz que o modelo é inviável, o problema é o modelo. Fecha o capítulo a
disciplina que sustenta todo o resto: **modelo não contém número de instância**, instância mora em
arquivo e vem com ficha de origem, licença e limitações, e a saída declara as versões que a
produziram. O teste de que a separação existe é trocar a instância por outra do mesmo formato — se
for preciso editar código, ela não existe. E a advertência final é a mais cara de aprender na
prática: trocar de ferramenta diante de um defeito de modelagem **parece progresso** e não é.
