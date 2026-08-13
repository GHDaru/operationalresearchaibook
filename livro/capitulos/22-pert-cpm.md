# 22 — Planejamento de projetos: PERT e CPM

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Calcular** o caminho crítico e a folga de cada tarefa, e dizer o que a folga autoriza.

**O2.** **Explicar por que a estimativa do PERT é otimista**, separando as duas causas do desvio.

**O3.** **Decidir** o que fazer com uma estimativa de prazo, sabendo o que ela sustenta.

## O problema

Este capítulo fecha a Parte III com o **Método do Caminho Crítico** (CPM, do inglês *Critical
Path Method*) e a **Técnica de Avaliação e Revisão de Programas** (PERT, *Program Evaluation and
Review Technique*) — dois modelos de rede que qualquer curso de gestão de projetos ensina, e o
resultado mais incômodo desta Parte:

> A fórmula do PERT publica **21 dias** para o projeto desta página. Simulado, ele leva **24,48
> dias** em média e **estoura a estimativa em 82,3% das amostras**. O método não erra por pouco:
> ele erra quase sempre, e para o mesmo lado.

O erro caro deste capítulo é o que acontece com essa estimativa depois:

> O número vira compromisso. Alguém apresenta "21 dias" como prazo, sem dizer que é uma média de
> um caminho, e a organização planeja em cima disso. **Quatro em cada cinco vezes o projeto passa
> do prazo** — e a conversa que se segue é sobre disciplina de execução, quando o defeito estava
> na aritmética da estimativa.

## De onde isto veio

### O aperto: projetos grandes demais para caber numa cabeça

O problema nasce em projetos com centenas de tarefas interdependentes, em que a pergunta *"quando
isto termina?"* deixou de ter resposta por inspeção. Duas coisas eram necessárias ao mesmo tempo: a
**duração total** e a informação de **onde apertar** para encurtá-la.

### A virada: a folga

A ideia que organiza tudo é uma subtração. Para cada tarefa, calcule o mais cedo que ela pode
começar e o mais tarde que ela pode começar sem atrasar o projeto. A diferença é a **folga** —
e as tarefas de folga zero formam o **caminho crítico**.

O que isso compra é operacional: **atrasar uma tarefa com folga não atrasa o projeto**, e acelerar
uma tarefa fora do caminho crítico não adianta nada. É a mesma lógica do corte mínimo do
[capítulo 19](19-fluxo-maximo.md), agora no tempo.

### O que o PERT acrescentou, e o que ele custou

O CPM trabalha com durações fixas. O PERT acrescenta incerteza pedindo três estimativas por
tarefa — otimista, provável, pessimista — e resumindo-as numa média, $(o + 4m + p)/6$, que ele
então **soma ao longo do caminho crítico**.

É nessa soma que mora o problema deste capítulo.

### A ideia reaproveitável

> **A média de um máximo é maior do que o máximo das médias.** Sempre que algo espera pelo mais
> lento de vários processos paralelos, planejar pela média de um deles subestima — e o erro cresce
> com o número de paralelos.

Vale muito além de projeto: vale para qualquer atendimento que só termina quando a última parte
chega.

### A origem do nome

As duas siglas dizem o que os métodos fazem: **CPM** aponta o caminho crítico; **PERT** avalia e
revisa um programa de trabalho. A literatura didática os data do **fim dos anos 1950**, em contextos
distintos — um industrial, outro militar —, e **este handbook não abriu nenhuma fonte primária**:
data, contexto e atribuição ficam `⏳`, e nenhuma das três sustenta afirmação nesta página.

### Procedência

| Afirmação | Estado |
|---|---|
| As origens do CPM e do PERT, a datação no fim dos anos 1950 e os contextos industrial e militar | ⏳ **atribuições correntes**; este handbook **não abriu** nenhuma fonte primária |
| Que a fórmula do PERT use a média $(o+4m+p)/6$ | 📖 **leitura editorial** de procedimento de manual |
| A duração 18, as folgas, e o caminho crítico do projeto desta página | ✓ **medidos** em `po-zero/parte-III-redes`, em aritmética exata |
| Os 21 dias da fórmula, os 24,48 simulados, os 82,3% de estouro e o viés de 0,49 | ✓ **medidos** por simulação com **semente declarada** |

## O caminho crítico, medido

Um projeto de quatro tarefas:

| Tarefa | Duração | Depende de |
|---|---|---|
| `especificar` | 5 | — |
| `backend` | 10 | `especificar` |
| `frontend` | 7 | `especificar` |
| `integrar` | 3 | `backend`, `frontend` |

**Duração do projeto: 18.** O caminho crítico é `especificar → backend → integrar`, e as folgas:

| Tarefa | Folga | O que isso autoriza |
|---|---|---|
| `especificar` | **0** | Nada. Um dia de atraso é um dia no projeto |
| `backend` | **0** | Nada |
| `frontend` | **3** | Pode atrasar até 3 dias **sem** afetar a entrega |
| `integrar` | **0** | Nada |

> **A folga é a informação que o método entrega de graça**, e é a que mais muda gestão: acelerar
> `frontend` não encurta o projeto em um único dia, e é exatamente lá que a pressão costuma cair,
> porque é a tarefa que "parece atrasada".

## O PERT, e as duas causas do desvio

Agora com incerteza. As três estimativas por tarefa, e o que a fórmula publica:

| Tarefa | Otimista | Provável | Pessimista | Média do PERT |
|---|---|---|---|---|
| `especificar` | 4 | 5 | 12 | 6 |
| `backend` | 6 | 10 | 20 | 11 |
| `frontend` | 4 | 7 | 16 | 8 |
| `integrar` | 2 | 3 | 10 | 4 |

**A fórmula publica 21 dias** — a soma ao longo do caminho crítico. Simulando o projeto **20 mil
vezes**, com semente declarada:

| | Medido |
|---|---|
| Duração média do projeto | **24,48** |
| Duração mediana | **24,30** |
| Percentil 90 | **29,35** |
| Probabilidade de estourar os 21 dias | **82,3%** |

> **A escolha de modelagem que precisa ficar declarada, porque metade do desvio sai dela.** Cada
> duração é sorteada de uma distribuição **triangular** sobre (otimista, provável, pessimista), cuja
> média é $(o + m + p)/3$. A fórmula do PERT usa outra média — $(o + 4m + p)/6$, que pesa o valor
> provável quatro vezes mais. Para `especificar` (4, 5, 12), uma dá 7,0 e a outra dá 6,0. **Um dia
> de diferença por tarefa, antes de qualquer efeito de rede.** Trocar a triangular por outra família
> mudaria os números desta página; o que **não** mudaria é a separação da seção seguinte, porque ela
> compara duas medições feitas nos mesmos sorteios.

> **Até onde estes dígitos carregam.** Os números acima vêm de **uma** semente, e simulação tem
> ruído. Repetindo com seis sementes diferentes, a faixa medida é:
>
> | | Faixa entre sementes |
> |---|---|
> | Duração média | **24,43 a 24,51** |
> | Probabilidade de estourar | **81,83% a 83,06%** |
> | Viés do método | **0,475 a 0,509** |
>
> Ou seja: **o segundo dígito carrega e o terceiro não.** "Cerca de 24,5 dias" e "cerca de 82%" é o
> que a medição sustenta; o `24,48` está publicado por ser exatamente reprodutível com a semente
> declarada, não por ter três dígitos de precisão. O viés, sim, sobrevive às duas casas — e a seção
> seguinte explica por quê.

**Duas causas diferentes produzem esse desvio, e só uma é defeito do método.** Misturá-las daria
um número grande e sem significado, então elas foram separadas:

### A separação, feita nas mesmas amostras

Para cada sorteio, mediram-se **duas** coisas: a duração real do projeto (o máximo sobre todos os
caminhos) e a duração do **caminho que o CPM declarou crítico antes de sortear**. Tudo o mais é
idêntico — mesma distribuição, mesmos números sorteados —, então a diferença isola o defeito.

| | Média |
|---|---|
| Só o caminho declarado | 23,99 |
| O projeto inteiro | 24,48 |
| **Diferença — o viés do método** | **0,49** |

**Este viés tem nome, e vale fixá-lo agora porque a literatura e os exercícios usam os três.** Em
inglês é ***merge bias***; em português aparece como **viés de convergência** (de caminhos) ou,
como aqui, **o viés do método**. São a mesma coisa: **o projeto espera a mais lenta entre as
tarefas paralelas, e a média de um máximo é maior que o máximo das médias**. Está no
[glossário](../glossario.md).

**O viés é 0,49 dia**, e não os ~3,5 que a comparação ingênua sugeriria. O resto do desvio vem da
**triangular não ter a mesma média que a fórmula do PERT supõe** — $(o+m+p)/3$ contra
$(o+4m+p)/6$ —, o que é uma escolha de modelagem, não um defeito do PERT.

> **E uma frase de sala de aula que não sobrevive à medição.** Diz-se que *"adotar a média dá 50% de
> chance de estourar, porque metade das realizações fica acima dela"*. A segunda metade da frase é a
> definição de **mediana**, não de média. Prazo de projeto é assimétrico à direita — a cauda longa é
> a de atraso —, então a média fica **acima** da mediana e é estourada um pouco **menos** que
> metade das vezes. Medido aqui: a média simulada (24,48) é estourada em **48,1%** das amostras, e
> a mediana (24,30) em **50,0%** exatos. A diferença é pequena e não muda o veredito — nenhuma das
> duas é compromisso —, mas o argumento correto é *"quase metade"*, e quem diz "por definição, metade"
> está trocando as duas medidas de lugar.

> **Esta honestidade custa a manchete e vale a pena.** Seria mais impressionante publicar "o PERT
> erra 3,5 dias". Seria também falso: a maior parte desse número não é do método.

### E o viés cresce com os caminhos paralelos

Medido, com **controle**:

| Ramos paralelos | Viés | Estoura a estimativa em |
|---|---|---|
| **1** (controle) | **0,0** | 76,5% |
| 2 | 1,71 | 89,7% |
| 3 | 2,55 | 94,9% |
| 5 | 3,64 | 98,5% |
| 8 | 4,45 | 99,6% |

**A linha de um ramo tem de dar zero, e dá.** Sem paralelismo, a duração do projeto **é** a do
caminho declarado — o viés não existe por construção.

> **E é justamente por ser "por construção" que esse controle prova menos do que parece.** Com um
> ramo só, a diferença pareada é zero **em toda amostra**, aconteça o que acontecer: esse controle
> não tem como falhar, e um controle que não pode falhar não controla nada. Ele confirma que a
> soma ao longo de uma cadeia está certa — útil, e bem menos do que "a isolação está correta".
>
> O controle que **pode** falhar é outro, e foi medido: dois ramos paralelos com médias muito
> desiguais — um de 40 dias, outro de 15 — e **faixas que se sobrepõem**, de modo que o ramo curto
> vença de vez em quando. Aí o viés tem de ser **positivo e pequeno**, e é: **0,0618**. Zero
> indicaria que o segundo ramo não entrou na conta; um número grande indicaria erro no
> experimento.
>
> **A primeira tentativa deste controle também não podia falhar**, e vale contar por quê: as faixas
> escolhidas foram (30, 40, 55) e (2, 5, 9), que **não se cruzam**. O ramo curto nunca vencia, o
> viés dava 0,0 por construção, e o controle escrito para substituir um controle tautológico era
> tautológico exatamente pelo mesmo motivo. **Sobreposição de faixas é o que lhe dá dentes** — e
> quem escreve controle precisa perguntar, antes de rodar, o que exatamente o faria dar diferente
> de zero.

E repare na coluna da direita na primeira linha: **mesmo sem nenhum paralelismo, a estimativa
estoura em 76,5% das amostras.** Essa parte não é viés de convergência — é a fórmula da média não
descrever o que vai acontecer.

> ### ▶ Rode você mesmo
>
> **[Abrir a Parte III no Google Colab](https://colab.research.google.com/github/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-III.ipynb)** · fonte em
> [`po-zero/cadernos/parte-III.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-III.ipynb)
>
> Lá dentro você **estima o viés antes de medi-lo** — e depois mexe no número de ramos paralelos, começando pelo controle de um ramo, que dá zero por construção. O caderno **não contém o algoritmo**: chama o código publicado, que o `pytest` já
> verifica ([ADR 0016](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0016-cadernos-colab-sem-deriva.md)).

## Quando não serve

**1. Quando as durações são correlacionadas.** A simulação supõe tarefas independentes. Se o mesmo
fornecedor atrasa três tarefas juntas, o desvio real é maior do que qualquer número desta página.

**2. Quando o caminho crítico muda de lugar.** Com incerteza, o caminho crítico **é aleatório** —
uma tarefa com folga de 3 pode virar crítica num cenário ruim. Falar de "o" caminho crítico com
durações incertas é uma simplificação, e ela é a origem do viés medido acima.

**3. Quando a rede não representa a restrição real.** Se o gargalo é uma pessoa que faz três
tarefas "paralelas" sozinha, elas não são paralelas — e nenhum caminho crítico vai mostrar isso.
É a restrição de **recurso**, e ela não está no modelo de precedência.

**4. Quando a resposta pedida é uma data, e não uma distribuição.** O método pode dar a
distribuição; a organização costuma querer um número. Entregar a média sem o percentil é o que
produz o erro caro deste capítulo.

## Fundamentos científicos

**MALCOLM e colegas (1959)** e **KELLEY e WALKER (1959)** são as origens do PERT e do CPM, no
mesmo ano e por caminhos independentes ([bibliografia](../bibliografia.md)).

**MacCRIMMON e RYAVEC (1964)** é a referência mais importante desta Parte, porque faz a mesma
pergunta que este capítulo mede: **quanto do desvio vem da fórmula e quanto vem do efeito de
rede**. Sessenta anos separam as duas. Este handbook confirmou o identificador e **não abriu o
texto**, e por isso **não afirma que os dois resultados concordam** — afirma apenas que a pergunta
é a mesma, e que ela é antiga. **FULKERSON (1962)**, com a correção de **CLINGEN (1964)**, trata
da mesma família de problemas.

**VAN SLYKE (1963)** sustenta a escolha metodológica desta página: simular o projeto, em vez de
somar médias ao longo de um caminho, é resposta de 1963 — não invenção deste handbook. O que aqui
é próprio é a **isolação nas mesmas amostras**, que separa as duas causas.

> **Uma leitura obrigatória antes de qualquer comparação.** **KLINGEN (1966)** trata de viés em
> cálculo de prazo do PERT numa rede real, e há indício de que a **direção** do viés que ele
> relata possa não ser a que este capítulo mede. O identificador está conferido e o texto não foi
> aberto. Enquanto não for, **este capítulo não faz nenhuma afirmação comparativa com a
> literatura** — e esta caixa existe para que a dívida não seja esquecida.

## Fundamentos e fontes

**O que está medido aqui.** A duração 18 e as folgas, em aritmética exata; e os 21 dias da fórmula,
os 24,48 simulados, os 82,3% de estouro, o viés de 0,49 e a varredura de ramos paralelos — todos
por simulação com **semente declarada** e 20 mil amostras. Em `po-zero/parte-III-redes/redes.py`,
com teste que compara **este texto** à medição.

> **Nota de método, e ela vale mais do que os números.** A primeira versão deste experimento
> comparava a fórmula com a simulação diretamente, e teria publicado um viés de ~3,5 dias que é
> quase todo artefato da distribuição escolhida. A separação nas mesmas amostras foi acrescentada
> depois, e com ela o número honesto caiu para 0,49. **Um experimento que mede duas causas juntas
> não mede nenhuma das duas.**

**O que continua em dívida:** as origens do CPM e do PERT, `⏳`.

> 🔵 **Este capítulo está em "medido".** O que falta para ✅ é revisão independente em contexto
> fresco.

## Pratique

<div data-bateria="cap22"></div>

Três exercícios. O primeiro calcula folgas e decide onde apertar; o segundo é o do capítulo —
separar as duas causas do desvio; o terceiro transforma uma estimativa em compromisso defensável.

## Assista

**[Método do Caminho Crítico (CPM)](https://www.youtube.com/watch?v=1G_hitQYL5w)** ·
[Prof. Demétrios Batista da Silva](https://www.youtube.com/@profDemetriosOficial) · 20min55s

**O que ele resolve:** este capítulo gasta o espaço na **crítica** ao PERT e trata o cálculo do
caminho crítico de forma resumida. O vídeo faz o cálculo completo: cedo, tarde, folga, tarefa por
tarefa, com o diagrama sendo preenchido. Ver o procedimento inteiro antes de ler a seção da
simulação é a ordem que funciona.

## Síntese — o que levar

- **Folga é a diferença entre o mais tarde e o mais cedo que a tarefa pode começar.** Folga zero é
  o caminho crítico.
- **Acelerar tarefa com folga não encurta o projeto** — medido: `frontend` tem folga 3.
- **A fórmula do PERT publica 21 dias; o projeto leva 24,48 e estoura em 82,3% das amostras.**
- **Duas causas produzem esse desvio, e só uma é do método.** Separadas nas mesmas amostras, o
  viés é **0,49**, não 3,5.
- **O viés cresce com caminhos paralelos.** O controle de um ramo dá zero **por construção** e por
  isso prova pouco; o controle que pode falhar — dois ramos desiguais com faixas que se cruzam —
  dá **0,0618**, positivo e pequeno, que é o
  que prova a isolação.
- **Mesmo sem paralelismo, a estimativa estoura em 76,5%** das amostras: média não é promessa.
- **Com incerteza, o caminho crítico é aleatório.** Falar de "o" caminho crítico é simplificação.
- **Fora da Pesquisa Operacional:** a média de um máximo é maior que o máximo das médias — sempre
  que algo espera pelo mais lento de vários paralelos.

## Verificação

1. No projeto desta página, o time quer entregar em 16 dias. Onde faz sentido investir, e onde
   não? *(O1)*
2. Um analista compara a fórmula do PERT com uma simulação e conclui que "o método subestima em
   3,5 dias". Que erro metodológico ele cometeu, e como você o corrigiria? *(O2)*
3. A diretoria pede "uma data" para o projeto. Escreva a frase que você entrega, e a que você se
   recusa a entregar. *(O3)*

### Leitura executiva

O planejamento de projetos por rede entrega duas coisas: a **duração total** e a **folga** de cada
tarefa — a diferença entre o mais tarde e o mais cedo que ela pode começar sem atrasar a entrega.
As tarefas de folga zero formam o **caminho crítico**, e a consequência operacional é imediata:
acelerar uma tarefa com folga não encurta o projeto em um único dia, e é justamente sobre ela que a
pressão costuma cair, porque é a que "parece atrasada". No projeto medido aqui, a duração é **18** e
`frontend` tem **3 dias de folga**. O PERT acrescenta incerteza pedindo três estimativas por tarefa
e somando a média $(o+4m+p)/6$ ao longo do caminho crítico — e é nessa soma que está o problema:
**a fórmula publica 21 dias, o projeto simulado leva 24,48 em média, e estoura a estimativa em
82,3% das amostras**. O método não erra por pouco nem em casos raros: erra quase sempre e para o
mesmo lado. Duas causas diferentes produzem esse desvio, e apenas uma é defeito do método, de modo
que elas foram **separadas nas mesmas amostras** — medindo, para cada sorteio, a duração real do
projeto e a duração do caminho declarado crítico antes de sortear. O viés próprio do método é
**0,49 dia**, e não os ~3,5 da comparação ingênua; o resto vem da distribuição amostrada não ter a
mesma média que a fórmula supõe, o que é escolha de modelagem. O viés cresce com o número de
caminhos paralelos — 1,71 com dois ramos, 4,45 com oito. O **controle** de um ramo só dá zero, mas
dá zero *por construção* e por isso prova pouco; o controle que **pode** falhar — dois ramos
desiguais com faixas que se sobrepõem — dá **0,0618**, positivo e pequeno, e é ele que sustenta a
correção da isolação. Vale notar que, mesmo sem paralelismo
nenhum, a estimativa estoura em 76,5% das amostras: **média não é promessa**. Por fim, o modelo não
serve quando as durações são correlacionadas, quando a restrição real é de recurso e não de
precedência — três tarefas "paralelas" feitas pela mesma pessoa não são paralelas —, e quando o que
se pede é uma data em vez de uma distribuição: entregar a média sem o percentil é exatamente o que
transforma uma estimativa razoável num compromisso que se quebra quatro vezes em cinco.
