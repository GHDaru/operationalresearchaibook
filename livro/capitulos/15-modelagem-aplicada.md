# 15 — Modelagem aplicada em Programação Linear

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Reconhecer** o padrão — mistura, transporte, cobertura ou mix de produção — a partir de
um enunciado em prosa, e dizer qual é a variável de decisão de cada um.

**O2.** **Diagnosticar** um modelo cujo **padrão foi escolhido errado**, e mostrar o que a escolha
errada apagou do problema.

**O3.** **Julgar** se o modelo responde à pergunta que foi feita — mesmo quando a conta está certa
e o solver diz `Optimal`.

## O problema

Nove capítulos com a mesma montadora. Você aprendeu a formular, a enxergar a região, a pivotear, a
ler o preço, a ler a faixa, a atravessar por dentro. Falta a parte que decide se o modelo vai
servir para alguma coisa: **reconhecer que problema é esse**.

Porque a montadora não é um problema único. Ela é uma **instância** de um padrão — *mix de
produção* — e existem outros três que, juntos, cobrem a maior parte da Programação Linear
aplicada. Quem reconhece o padrão escreve o modelo em minutos. Quem não reconhece escreve **um
modelo que roda** e responde à pergunta errada.

O erro caro deste capítulo é o mais silencioso do livro inteiro, e por um motivo específico:

> Todos os erros anteriores tinham sintoma. `Infeasible` avisa. `Unbounded` avisa. Ciclagem
> trava. Preço fora da faixa dá prejuízo mensurável. **Padrão errado não avisa nada**: o modelo é
> menor, resolve mais rápido, devolve `Optimal` e um número plausível. E o número está certo —
> para outra pergunta.

Este capítulo mede exatamente isso. Mesma situação de distribuição, dois modelos: um custa
**R$ 365**, o outro **R$ 403,33**. Nenhuma conta errada nos dois.

## De onde isto veio

### O aperto: cada problema novo começava do zero

Nos primeiros anos da Programação Linear, cada aplicação era um projeto de pesquisa. Formular era
trabalho artesanal, e não havia repertório — cada equipe redescobria estruturas que outra equipe
já tinha resolvido, porque não havia nome para elas.

### A virada: perceber que os problemas se repetem

A virada não é um algoritmo. É **catalogar**: notar que a ração animal, a liga metálica e a
mistura de combustível são **o mesmo problema** com nomes diferentes; que a distribuição de
mercadorias, a alocação de tarefas e o escalonamento de turnos compartilham a mesma estrutura de
origem-destino.

Isso muda a natureza do trabalho. Modelar deixa de ser inventar e passa a ser **reconhecer e
adaptar** — que é mais rápido, menos sujeito a erro, e, o que importa mais aqui, **ensinável**.

> **A ideia reaproveitável:** *antes de projetar do zero, pergunte de que problema conhecido este
> é um caso.* Vale em modelagem, em arquitetura de software, em desenho de processo. O custo de
> não perguntar não é o tempo perdido — é reinventar uma estrutura **pior** do que a que já
> existia, sem saber que existia.

### Procedência

| Afirmação | Estado |
|---|---|
| Que estes padrões são o repertório canônico do ensino de Programação Linear | 📖 **leitura editorial** deste handbook, a partir da organização dos livros-texto citados na [bibliografia](../bibliografia.md) |
| A origem histórica de cada padrão (dieta, transporte, cobertura) e a quem se atribui | ❌ **procurada e não localizada** por identificador nesta rodada |
| Que o problema da dieta é um dos primeiros casos aplicados de Programação Linear | ⏳ atribuição corrente; a entrada de Dantzig sobre o assunto consta da bibliografia, e **não foi aberta** |

Este capítulo é o que menos depende de história do lote, e é bom que seja: ele é **repertório**,
não descoberta. O que ele afirma se sustenta na medição que roda logo abaixo.

## Os quatro padrões

A pergunta que identifica o padrão é sempre a mesma: **o que exatamente se escolhe?**

| Padrão | O que se escolhe | Objetivo típico | Restrição típica | Assinatura |
|---|---|---|---|---|
| **Mix de produção** | quanto **produzir** de cada produto | **maximizar** lucro | recursos disponíveis, `≤` | uma variável por produto |
| **Mistura** | quanto **comprar** de cada insumo | **minimizar** custo | exigências mínimas, `≥` | uma variável por insumo |
| **Transporte** | quanto **mandar** de cada origem a cada destino | **minimizar** custo | oferta `≤`, demanda `≥` | variável com **dois índices** |
| **Cobertura** | **quais** abrir, escalar, alocar | **minimizar** custo | cada item coberto ao menos uma vez | variável que **deveria ser binária** |

Repare que **mix e mistura são espelhos**: um maximiza com `≤`, o outro minimiza com `≥`. Confundir
os dois é o erro de formulação mais comum de quem está começando, e o sintoma aparece cedo — o
modelo devolve `Unbounded` ou zero.

E repare na última linha: **cobertura é o padrão que a Programação Linear não resolve direito**.
A variável honesta é binária, e este capítulo mostra o que acontece quando se finge que não é.

## O código

A [etapa 08 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-08-modelagem)
resolve os três padrões novos com o **mesmo Simplex da etapa 03**, sem uma linha de método novo.
É o ponto: o repertório é de **formulação**, não de algoritmo.

### Mistura — a ração

Dois ingredientes, duas exigências. Milho a R$ 3/kg com 9 g de proteína e 2 g de gordura; farelo a
R$ 5/kg com 30 g de proteína e 1 g de gordura. Cada saco precisa de **pelo menos** 180 g de
proteína e 24 g de gordura.

```
milho e farelo: ['180/17', '48/17'] kg  ·  custo 780/17  (2 pivôs)
```

Ou seja, ≈ 10,59 kg de milho e ≈ 2,82 kg de farelo, a ≈ R$ 45,88. Note as duas inversões em
relação à montadora: **minimiza** em vez de maximizar, e as restrições são `≥` em vez de `≤`.

### Transporte — a distribuição

Duas fábricas (30 e 40 unidades), três centros (20, 25 e 25 de demanda), com um custo por rota. A
assinatura do padrão é a variável de **dois índices**: $x_{ij}$ é quanto vai da fábrica $i$ para o
centro $j$.

```
{'x11': '20', 'x12': '0', 'x13': '10', 'x21': '0', 'x22': '25', 'x23': '15'}
custo 365  (4 pivôs)
```

O plano é legível: a fábrica 1 abastece o centro 1 inteiro e parte do 3; a fábrica 2 cobre o
centro 2 e o resto do 3.

### O padrão escolhido errado — e o modelo não avisa

Agora a mesma situação, modelada como **mix de produção**. O raciocínio parece uma simplificação
razoável: *"cada fábrica manda um total; o custo médio de cada uma resolve"*. O modelo fica menor e
mais rápido.

```
custo médio por fábrica usado no lugar do custo por rota: ['19/3', '16/3']
o modelo errado devolve custo 1210/3 e diz `Optimal`
o modelo certo   devolve custo 365
diferença: 115/3  ·  e o modelo errado NÃO diz quanto vai para cada centro
```

R$ 403,33 contra R$ 365 — uma diferença de **R$ 38,33**, cerca de 10,5%. E há um dano pior do que
o número:

> **O modelo errado não responde à pergunta.** Ele diz quanto cada fábrica manda **no total**. A
> operação precisa saber **quanto vai para cada centro**, e essa informação foi apagada na hora em
> que o destino saiu do modelo. Não é que a resposta esteja imprecisa: ela **não existe** ali.

O que o padrão errado apagou tem nome: a **variável de decisão** estava errada. Escolher a variável
errada é o erro mais caro de modelagem, porque tudo que vem depois — restrições, objetivo,
interpretação — fica coerente com ela e nada denuncia.

### Cobertura — o padrão que a Programação Linear não fecha

Quatro estações candidatas, cinco bairros, cada bairro alcançado por um subconjunto delas. A
pergunta é **quais abrir**. A variável honesta é binária: abre ou não abre. Relaxando para
contínua — porque é o que este livro tem até aqui:

```
relaxada: ['1/2', '1/2', '1/2', '1/2']  ·  custo 9  ·  fracionária: True
de verdade (por enumeração): estações [2, 3]  ·  custo 10
buraco entre a relaxação e a decisão executável: 1
```

**Meia estação em cada lugar.** O modelo está certo, a conta está certa, o solver diz `Optimal` — e
a resposta **não é executável**. Ninguém abre metade de uma estação.

E o número que fica é o mais importante do capítulo: a relaxação diz **9**, e a decisão real mais
barata custa **10**. A relaxação é um **limitante inferior**, e um limitante que **não se
alcança**. Toda a Parte de programação inteira do handbook existe para fechar esse buraco — e é
por isso que este capítulo é o último da Parte II.

## Quando não serve

**1. O repertório não cobre tudo.** Há problemas lineares que não caem em nenhum dos quatro
padrões, e forçar o encaixe é pior do que modelar do zero. O padrão é ponto de partida, não gabarito.

**2. Reconhecer o padrão não valida os dados.** O modelo pode ser do padrão certo, com estrutura
certa, e estar alimentado por um custo desatualizado. Nada neste capítulo protege contra isso.

**3. Cobertura em Programação Linear é sempre parcial.** Como a medição mostrou, a relaxação
devolve fração e um limitante que não se alcança. Sem programação inteira, o padrão de cobertura
serve para **estimar um piso**, não para decidir.

**4. Situações reais misturam padrões.** Um problema de distribuição com produção própria é
transporte **e** mix ao mesmo tempo. Os padrões são vocabulário para conversar sobre o modelo, não
caixas em que ele precisa caber inteiro.

**5. Este capítulo não ensina a coletar dado.** De onde vem o custo por rota, quem mantém a matriz
de alcance, com que frequência isso muda — é metade do trabalho real e não está aqui.

## Fundamentos e fontes

**O que está medido aqui.** As quantidades da ração, o plano de transporte e seus R$ 365, os
R$ 403,33 do padrão errado, a diferença de R$ 38,33, a solução fracionária da cobertura, o custo 9
da relaxação e o custo 10 da decisão executável — obtido por **enumeração dos 16 subconjuntos**,
para o capítulo não afirmar à mão o que dá para contar. Tudo se regenera rodando um script.

**O que não foi lido.** Nenhuma fonte nova entra neste capítulo. A organização dos padrões é
**leitura editorial** (`📖`) a partir dos livros-texto da [bibliografia](../bibliografia.md), e a
origem histórica de cada padrão está `❌` — procurada e não localizada por identificador nesta
rodada.

> 🟡 **Este capítulo está em v0.** Não passou por revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap15"></div>

Três exercícios. O primeiro é de reconhecimento puro — quatro enunciados em prosa, quatro padrões.
O segundo é o diagnóstico do padrão errado, com o prejuízo calculado. O terceiro é a pergunta que
encerra a Parte II: **este modelo responde ao que foi perguntado?**

## Assista

**[Problema de Transporte — Modelagem usando Programação
Linear](https://www.youtube.com/watch?v=NTHGKhCeJso)** ·
[Prof. Rafael Lima](https://www.youtube.com/@prof.rafaellima4531) · 17min24s

**O que ele resolve:** este capítulo trata o transporte como **um dos quatro padrões**, para que a
comparação entre eles fique visível. O vídeo faz o que o texto não faz bem: constrói o modelo de
transporte devagar, do enunciado às restrições de oferta e demanda, mostrando a variável de dois
índices nascer. É a segunda passada para quem quer sentir a formulação sendo montada.

## Síntese — o que levar

- **A pergunta que identifica o padrão é sempre a mesma:** *o que exatamente se escolhe?* A
  resposta é a variável de decisão, e ela determina tudo o mais.
- **Quatro padrões cobrem a maior parte:** mix de produção, mistura, transporte, cobertura.
- **Mix e mistura são espelhos** — um maximiza com `≤`, o outro minimiza com `≥`.
- **A assinatura do transporte é a variável de dois índices.** Se o destino não aparece na
  variável, ele não existe no modelo.
- **Padrão errado não avisa.** Medido: R$ 403,33 contra R$ 365, `Optimal` nos dois, e o modelo
  errado **não responde** à pergunta que foi feita.
- **Escolher a variável de decisão errada é o erro mais caro da modelagem**, porque tudo que vem
  depois fica coerente com ela.
- **Cobertura relaxada devolve fração**, e a fração é limitante inferior que **não se alcança** —
  medido, 9 contra 10. É a porta de entrada da programação inteira.
- **Fora da Pesquisa Operacional:** antes de projetar do zero, pergunte de que problema conhecido
  este é um caso.

## Verificação

1. *"Preciso decidir quais dos meus 12 depósitos manter abertos no ano que vem."* Qual é o padrão,
   qual é a variável de decisão, e que dificuldade você já antecipa? *(O1)*
2. Um analista modelou a distribuição da empresa com uma variável por fábrica, usando custo médio
   de frete. O modelo roda e devolve `Optimal`. Que informação a operação vai pedir e ele não vai
   ter? *(O2)*
3. Um modelo de escala de plantão devolve "0,4 enfermeiro no turno da noite". A conta está certa.
   O que você responde a quem pediu a escala, e o que precisa mudar — no modelo ou na pergunta?
   *(O3)*

### Leitura executiva

Depois de nove capítulos com a mesma montadora, o que falta para o modelo servir a alguma coisa é
**reconhecer que problema ele é** — e a pergunta que identifica isso é sempre a mesma: *o que
exatamente se escolhe?* A resposta é a variável de decisão, e dela decorrem objetivo, restrições e
leitura. Quatro padrões cobrem a maior parte da Programação Linear aplicada: **mix de produção**
(quanto produzir, maximizando lucro sob recursos `≤` — o caso da montadora), **mistura** (quanto
comprar, minimizando custo sob exigências `≥` — o espelho exato do anterior), **transporte** (quanto
mandar de cada origem a cada destino, cuja assinatura é a variável de **dois índices**) e
**cobertura** (quais abrir, escalar ou alocar, cuja variável honesta é **binária**). O erro deste
capítulo é o mais silencioso do livro porque não tem sintoma: escolher o padrão errado produz um
modelo **menor, mais rápido, que devolve `Optimal`** e um número plausível. Medido aqui: a mesma
situação de distribuição modelada como transporte custa R$ 365 e, modelada como mix de produção com
custo médio de frete, custa R$ 403,33 — e o dano maior não é a diferença de 10,5%, e sim que o
modelo errado **não diz quanto vai para cada centro**, porque o destino saiu junto com a variável.
A cobertura fecha a Parte II mostrando o limite da própria Programação Linear: relaxada para
contínua, ela devolve meia estação em cada lugar, ao custo 9, enquanto a decisão executável mais
barata — obtida por enumeração — custa 10. A relaxação é um limitante inferior que **não se
alcança**, e é exatamente esse buraco que a programação inteira existe para fechar.
