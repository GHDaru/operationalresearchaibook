# 01 — O sistema e a restrição

> **Conteúdo revisado em 2026-08** · edição inaugural · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

Ao final deste capítulo, você deve conseguir:

1. **Definir** sistema e restrição, e explicar por que todo sistema tem pelo menos uma restrição;
2. **Distinguir** restrição de gargalo, e classificar uma restrição como física, de mercado ou de política;
3. **Identificar**, num caso descrito, qual parte determina o resultado do conjunto;
4. **Explicar** por que eliminar uma restrição não resolve o problema — desloca a restrição.

## O problema

Uma gráfica de bairro passou três anos investindo. Trocou a impressora por um modelo mais rápido, informatizou o orçamento, treinou os acabadores, contratou mais um vendedor. Nenhuma dessas decisões foi errada e nenhuma foi barata.

O prazo de entrega ao cliente continua o mesmo.

Essa história é comum a ponto de ser banal, e ela não é sobre má execução. É sobre uma pergunta que ninguém fez antes de investir: **nesta gráfica, o que determina o prazo?** Enquanto a resposta não existir, "melhorar" é uma aposta — e a maior parte das apostas cai fora.

O nome deste livro é a resposta a essa pergunta. Este capítulo define a palavra.

## O conceito

### Primeiro, o sistema

Na gráfica, um pedido passa por orçamento, aprovação, pré-impressão, impressão, acabamento e expedição. Se a pré-impressão para, a impressora fica sem o que fazer. Se o acabamento atrasa, a expedição não tem o que despachar.

Isso é **interdependência**: o que uma parte consegue fazer depende do que as outras fizeram.

> Um **sistema** é um conjunto de partes interdependentes que existe para um objetivo.

Duas palavras carregam o peso. **Interdependentes** — um conjunto de partes que não dependem umas das outras não é um sistema, é uma coleção. E **objetivo** — sem objetivo declarado, não existe critério para dizer se o sistema vai bem ou mal.

O objetivo não é escolhido pelo método: é declarado por quem é dono do sistema. Em *A Meta* (1984), Goldratt trabalha com o objetivo de uma empresa com fins lucrativos — ganhar dinheiro agora e no futuro. Uma clínica pública ou uma escola têm outros objetivos, e o raciocínio deste livro vale igual. O que não vale é não ter objetivo nenhum.

### A corrente

Uma pilha de tijolos aguenta o peso da soma dos tijolos. Uma corrente aguenta o peso do **elo mais fraco**.

A diferença entre as duas é a interdependência. Numa pilha, cada tijolo trabalha por si e as contribuições se somam. Numa corrente, cada elo depende do vizinho, e o conjunto inteiro cede onde um só cede.

A consequência é dura: reforçar um elo que não é o mais fraco não aumenta a resistência da corrente. Não aumenta pouco — não aumenta nada.

Uma empresa se parece muito mais com a corrente do que com a pilha.

### A restrição

> A **restrição** de um sistema é aquilo que limita o desempenho desse sistema em relação ao seu objetivo.

Esta é a definição de Goldratt (*A Meta*, 1984), sistematizada em Dettmer (2007). Repare que ela é relativa ao objetivo: mude o objetivo declarado e a restrição pode passar a ser outra coisa. Não existe "a restrição" de uma empresa em abstrato — existe a restrição dela em relação ao que ela decidiu perseguir.

### Por que sempre existe uma

Suponha que não houvesse restrição alguma. Nada limitaria o desempenho do sistema, e ele cresceria sem limite: a gráfica imprimiria infinito, a clínica atenderia infinitos pacientes, a empresa ganharia dinheiro infinito.

Nada disso acontece. Logo, algo limita. A pergunta útil nunca é *se* existe uma restrição — é **onde ela está**.

E são poucas: em sistemas reais, quase sempre uma (Cox & Schleier, 2010). Se todas as partes limitassem o resultado na mesma medida, qualquer melhoria em qualquer lugar melhoraria o todo — e não foi o que aconteceu com a gráfica do começo deste capítulo.

### Restrição não é sinônimo de gargalo

**Gargalo** é o recurso cuja capacidade é igual ou menor que a demanda colocada sobre ele (*A Meta*, 1984): um conceito de capacidade, aplicável a recursos.

**Restrição** é mais amplo. Um gargalo é uma restrição enquanto for o elo mais fraco — mas há restrições que não são recursos e não têm capacidade nenhuma.

### Onde a restrição costuma estar

Três lugares, na sistematização corrente da literatura (Dettmer, 2007):

**Restrição física.** Um recurso com capacidade menor que a demanda: a impressora, a sala de reabilitação equipada, o único técnico que sabe mexer no sistema legado. É a mais fácil de enxergar, porque deixa rastro — o trabalho se acumula antes dela e falta depois dela.

**Restrição de mercado.** A capacidade sobra e a demanda falta: a gráfica imprime mais do que vende. A restrição está fora das paredes, e tratá-la como se fosse interna produz justamente o desperdício que a empresa quer evitar.

**Restrição de política.** Nenhum recurso está no limite, e ainda assim algo limita: uma regra, um indicador, uma prática. A gráfica que só programa a impressora depois que o pedido inteiro está orçado. O suporte que mede o técnico por chamados fechados por dia. A loja que só compra em lote fechado, para não perder o desconto.

A distinção entre física e de política é a mais consequente deste livro, porque muda o **tipo de trabalho** necessário. Uma restrição física se descobre **medindo**: onde está a fila. Uma restrição de política não tem fila, não aparece em relatório de capacidade e não se descobre medindo — ela se descobre **raciocinando**.

Guarde essa frase. Ela é o motivo pelo qual existem os módulos seguintes.

### A restrição não é um defeito

A tentação é ler tudo isso como "achar o culpado e eliminá-lo". É o erro mais caro do capítulo.

A restrição não é um erro de projeto. É onde o sistema está hoje — um fato a gerenciar, não um defeito a extirpar.

E ela não desaparece quando é eliminada: **muda de lugar**. A gráfica que compra a segunda impressora descobre, três semanas depois, que agora o acabamento não dá conta. O sistema continua sendo uma corrente; o que mudou foi qual elo é o mais fraco. O que fazer com esse fato é o assunto do capítulo 03.

### O achado contraintuitivo

Junte as duas pontas: a restrição determina o resultado, e ela costuma ser uma. Portanto **a maior parte do sistema não é a restrição**.

Numa gráfica de seis etapas, cinco não determinam o prazo. Melhorar qualquer uma dessas cinco não encurta a entrega em um dia — nem em uma hora. E como toda melhoria custa dinheiro, atenção e paciência das pessoas, melhorar "tudo" é a forma mais confiável de gastar muito e não mudar nada.

O capítulo seguinte é sobre por que isso acontece com gente competente, de boa-fé, o tempo todo.

## Erros comuns

**Chamar de restrição o que incomoda.** *Sinal:* a restrição apontada é sempre a área com que se tem atrito, e nunca a área de quem está falando.

**Confundir a restrição com quem reclama mais alto.** *Sinal:* a "restrição" muda de nome conforme quem está na reunião.

**Procurar a restrição sem ter declarado o objetivo.** *Sinal:* duas pessoas discordam sobre onde está a restrição e, quando perguntadas sobre o que o sistema deve entregar, descrevem coisas diferentes.

**Tratar a restrição como culpa.** *Sinal:* a conversa vira sobre quem falhou. A restrição é uma propriedade do sistema, não o desempenho de uma pessoa — e quem trabalha nela costuma ser o mais pressionado de todos.

**Responder "a restrição é o dinheiro" ou "somos todos a restrição".** *Sinal:* a resposta não aponta um lugar onde se possa observar uma fila, medir uma capacidade ou ler uma regra. Resposta vaga não sustenta decisão.

## Mão na massa

<div data-bateria="cap01"></div>

### Leitura executiva

Um **sistema** é um conjunto de partes interdependentes que existe para um objetivo declarado por quem é seu dono. Pela interdependência, ele se comporta como corrente e não como pilha: a resistência é a do **elo mais fraco**, e reforçar outro elo não muda nada. A **restrição** é o que limita o desempenho do sistema em relação ao seu objetivo (*A Meta*, 1984), e sempre existe — sem ela o desempenho seria infinito. Não é sinônimo de gargalo: pode estar num recurso (física), fora das paredes (de mercado) ou numa regra (de política). A distinção que mais importa é a última: restrição física se descobre medindo; de política, raciocinando. E a restrição não é defeito a eliminar — eliminá-la apenas a desloca. Como a maior parte do sistema não é a restrição, melhorar "tudo" custa caro e não muda o resultado.
