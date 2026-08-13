# 03 — Anatomia de um modelo de otimização

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Identificar** as quatro peças de um modelo de otimização — variáveis de decisão, função
objetivo, restrições, parâmetros — num enunciado escrito em português, e dizer o que é peça e o
que é enfeite.

**O2.** **Prever o sintoma** de um erro em cada peça: dado o defeito, dizer o que o solver vai
devolver — inclusive quando ele devolve `Optimal`.

**O3.** **Aplicar o teste da unidade** para pegar, antes de resolver, o erro que o solver não pega.

## O problema

Um modelo de otimização tem quatro peças, e só quatro. Isso soa como boa notícia até você
descobrir a assimetria que organiza este capítulo:

> **Três das quatro peças, quando erradas, produzem um modelo que roda, devolve `Optimal` e está
> errado.** Só uma delas costuma dar erro visível — e é justamente a menos perigosa.

O leitor que vem do [capítulo 02](02-ciclo-de-modelagem.md) já sabe onde os projetos morrem. Este
capítulo desce um nível: dentro da etapa 2 — formular —, **qual peça você errou, e como o erro
se manifesta**.

O erro caro deste capítulo:

> Um modelo com a variável de decisão errada não tem defeito nenhum que se possa apontar. A
> função objetivo está certa *para aquelas variáveis*. As restrições estão certas *para aquelas
> variáveis*. O solver devolve `Optimal`. E a resposta não serve, porque ninguém pode executá-la
> — o [capítulo 15](15-modelagem-aplicada.md) mediu isso: **R$ 403,33 contra R$ 365**, com
> `Optimal` nos dois.

## De onde isto veio

### O aperto: cada grupo escrevia o modelo de um jeito

Nos anos que seguiram a formulação da Programação Linear, o modelo existia — mas **a forma de
escrevê-lo não era comum**. Cada grupo tinha a sua notação, e a consequência não era estética:
não dava para trocar problema entre equipes, nem para escrever um programa que resolvesse "um
problema linear qualquer" em vez de *aquele* problema.

O aperto é o mesmo que produziu formatos de arquivo em qualquer área: **enquanto a estrutura é
implícita, cada instância é artesanal**.

### O que se fazia antes, e a virada

Antes, o modelo era descrito em prosa e traduzido à mão para o método. A virada foi separar, de
forma explícita, **o que muda de instância para instância** (os parâmetros) do **que define o tipo
de problema** (a estrutura: variáveis, objetivo, restrições).

É essa separação que torna possível a frase que hoje parece óbvia: *"este é um problema de
Programação Linear (PL) com 3 variáveis e 4 restrições"* — uma frase que descreve um problema sem
dizer nada sobre o assunto dele.

### A ideia reaproveitável

> **Separar estrutura de dado é o que permite resolver uma classe em vez de um caso.** O
> algoritmo é escrito uma vez para a estrutura; os números entram depois.

Vale muito além da otimização: é a mesma ideia que separa consulta de banco de dados dos seus
parâmetros, e função dos seus argumentos. Reconhecê-la aqui é reconhecê-la em toda parte.

### A origem do nome

**"Variável de decisão"** carrega a definição inteira dentro do nome, e é o melhor teste que
existe: se ninguém pode **decidir** aquele valor, não é variável de decisão. Se o valor já está
dado, é **parâmetro**. Esta única distinção resolve a maior parte dos erros de formulação de
principiante.

### Procedência

| Afirmação | Estado |
|---|---|
| A anatomia em quatro peças, tal como apresentada aqui | 📖 **leitura editorial**, comum aos livros-texto da [bibliografia](../bibliografia.md) |
| O aperto histórico da falta de forma comum, com data e nome | ⏳ **narrativa estrutural**; este handbook **não localizou** a fonte primária que a documenta |
| Os números de prejuízo citados (R$ 350 e R$ 403,33) | ✓ **medidos** no `po-zero`, com teste que compara o texto publicado à medição, nos capítulos [12](12-dualidade.md) e [15](15-modelagem-aplicada.md) |

> A segunda linha é uma dívida, e ela está escrita aqui porque o Princípio XII exige contar de
> onde o método veio **e** o Princípio III proíbe inventar a história. A narrativa acima descreve
> um aperto que é real e verificável na estrutura do que existe hoje; **o que falta é a citação
> que a data e a atribui**, e enquanto ela faltar a linha fica `⏳`.

## As quatro peças

| Peça | A pergunta que a define | Quem escolhe o valor |
|---|---|---|
| **Variáveis de decisão** | O que exatamente se escolhe? | **Você.** É a saída do modelo |
| **Função objetivo** | Qual é a **única** medida? | Você declara a fórmula; o valor sai do modelo |
| **Restrições** | O que limita? | Você declara; o mundo impõe |
| **Parâmetros** | O que já está dado? | **Ninguém, agora.** É a entrada do modelo |

A tabela inteira pode ser reduzida a uma pergunta de triagem, e vale decorar esta:

> **Isto é algo que alguém decide, ou algo que alguém mede?** O que se decide é variável. O que se
> mede é parâmetro.

### Variáveis de decisão — a peça que apaga a pergunta quando erra

Uma variável de decisão precisa passar em três testes:

1. **Alguém pode escolher o valor.** Se a demanda do mês que vem entrou como variável, o modelo
   vai "escolher" a demanda — e ela virá no valor mais conveniente.
2. **Tem unidade explícita.** *"x₁ = produto A"* não é variável. *"x₁ = litros de A produzidos por
   dia"* é.
3. **Alguém consegue executar o valor.** Se o modelo devolver `x = 3,7` e o mundo só aceita
   inteiro, a resposta não é executável — e esse é o assunto do
   [capítulo 04](04-classificacao-e-escolha.md).

O teste 3 é o mais esquecido, e é o que o capítulo 15 mediu: escolher **quanto produzir de cada
mistura** quando a pergunta era **quanto mandar de cada origem para cada destino** produz um
modelo impecável que não diz a ninguém o que fazer.

### Função objetivo — a peça que exige uma escolha desconfortável

**Uma só.** A restrição mais dura da otimização clássica não é matemática, é organizacional: o
modelo exige que se declare **qual é a medida**, e organizações costumam querer três ao mesmo
tempo — barato, rápido e seguro.

Há três saídas honestas, e uma desonesta:

| Saída | O que se faz | Honesta? |
|---|---|---|
| **Escolher** | Uma vira objetivo; as outras viram restrição (*"custo mínimo, com prazo ≤ 5 dias"*) | ✔ Sim, e é a mais usada |
| **Ponderar** | Soma com pesos: `0,7·custo + 0,3·atraso` | ✔ Sim, **se** os pesos forem declarados como escolha política |
| **Fronteira** | Gerar o conjunto de soluções não dominadas e deixar a escolha para quem decide | ✔ Sim, e é o assunto da otimização multiobjetivo |
| **Somar unidades diferentes** | `minimizar custo + tempo` | ✘ **Não.** Reais e horas não somam |

A última linha é o erro que o **teste da unidade** pega, e o solver não: somar reais com horas
produz um número com `Optimal` do lado e **nenhum significado**.

### Restrições — a peça cujo erro o solver às vezes denuncia

É a única das quatro em que o erro tem chance de aparecer como veredito, e o
[capítulo 10](10-casos-especiais.md) catalogou os vereditos:

| O erro na restrição | O que o solver devolve |
|---|---|
| Faltou uma restrição que o mundo impõe | Às vezes `Unbounded` — o modelo cresce para sempre |
| Faltou, mas a região continua limitada | **`Optimal`**, com uma resposta que ninguém executa |
| Sobra uma restrição que o mundo não impõe | `Optimal`, com resposta pior do que a possível |
| Duas restrições se contradizem | `Infeasible` |

Repare que **duas das quatro linhas devolvem `Optimal`**. `Unbounded` e `Infeasible` são os casos
sortudos: o modelo grita. O caso comum é o modelo sussurrar.

### Parâmetros — a peça silenciosa

Parâmetro errado **nunca** dá erro. Ele produz a resposta certa para o mundo errado, e é por isso
que a [análise de sensibilidade](13-sensibilidade.md) existe: ela é o instrumento que diz **quanto
o parâmetro pode estar errado** antes de a resposta mudar.

Duas armadilhas específicas, ambas medidas em outros capítulos deste livro:

- **Parâmetro que na verdade é variável.** O caso clássico é o preço: se o seu preço depende de
  quanto você vende, ele não é dado.
- **Parâmetro tratado como certo quando tem faixa.** É o erro de R$ 350 do
  [capítulo 12](12-dualidade.md): um preço-sombra é um parâmetro **com prazo de validade**, e
  citá-lo fora da faixa custou dinheiro sem nenhuma conta errada.

## O teste da unidade, em 60 segundos

O único procedimento deste capítulo que se aplica sempre, antes de resolver qualquer coisa:

1. **Escreva a unidade de cada variável de decisão.** Não o nome — a unidade. `kg/dia`, `unidades
   por semana`, `1 se abrir a fábrica, 0 se não`.
2. **Multiplique pela unidade do coeficiente**, em cada termo do objetivo e de cada restrição.
3. **Confira que todos os termos de uma mesma soma têm a mesma unidade**, e que os dois lados de
   cada restrição também têm.

Um exemplo de bolso, com o defeito e o conserto lado a lado:

```
objetivo:  minimizar  12·x  +  3·y
           x = toneladas transportadas       [12] = R$/tonelada    → R$   ✔
           y = horas de caminhão paradas     [ 3] = horas          → h²   ✘

o defeito: os dois termos não somam — R$ mais h² não é nada
o conserto: [3] tem que ser R$/hora (o custo da hora parada), e aí y contribui em R$
```

**O que este teste pega que o solver não pega:** unidade incoerente, coeficiente na escala errada
(mês contra dia, milhar contra unidade) e a variável que virou parâmetro sem ninguém notar. Ele
custa um minuto e é a coisa de melhor retorno neste capítulo inteiro.

## Quando não serve

A anatomia em quatro peças é uma lente, e **lente não é o mundo**. Ela deixa de servir em pelo
menos quatro situações, e reconhecê-las cedo evita forçar o problema para dentro do formato:

**1. Quando a decisão é sequencial e reage ao que acontece.** Um modelo com variáveis fixadas de
uma vez descreve mal *"decida hoje, veja o que acontece, decida de novo"*. Isso é otimização sob
incerteza e programação dinâmica, e as quatro peças precisam de um quinto elemento — **estágio**.

**2. Quando não existe uma medida única, nem por escolha nem por peso.** Se as partes discordam do
que é melhor e a discordância é o problema, o modelo de otimização vai **esconder** a discordância
dentro de um peso. Aí o problema é de negociação, não de otimização.

**3. Quando a restrição é a própria pergunta.** Há problemas em que só se quer saber se existe uma
solução viável — escala de plantão, alocação de horários. Não há objetivo, e todo o trabalho está
nas restrições. As quatro peças ainda descrevem, mas a peça "função objetivo" fica vazia, e
inventar uma atrapalha.

**4. Quando o modelo tem mais peça do que o problema tem estrutura.** Se cada restrição vale para
exatamente uma linha de dado e nada se repete, você escreveu uma planilha com notação matemática.
Não está errado — só não está ganhando nada com isso.

## Fundamentos e fontes

**O que está medido aqui.** Nenhum número novo. Os dois citados — R$ 350 e R$ 403,33 — vêm das
etapas do `po-zero` e estão conferidos nos capítulos que os produziram, cada um com teste que
compara o texto publicado à medição.

**O que continua em dívida:** o aperto histórico da falta de uma forma comum de escrever modelos,
`⏳` — narrativa estrutural sem a citação primária que a date e a atribua.

> 🟡 **Este capítulo está em v0.** Não passou por revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap03"></div>

Três exercícios. O primeiro separa peça de enfeite num enunciado; o segundo pede a previsão do
sintoma a partir do defeito — que é o objetivo mais difícil deste capítulo; o terceiro é o teste da
unidade aplicado a um modelo que roda e está errado.

## Assista

**[Conceitos Básicos de Otimização - Programação Linear - Pesquisa Operacional](https://www.youtube.com/watch?v=YLkZS-U7WTs)** ·
[Pedro Munari](https://www.youtube.com/@munariflix) · 11min01s

**O que ele resolve:** este capítulo organiza as quatro peças **pelo erro que cada uma produz** —
é uma leitura de diagnóstico, e ela supõe que você já viu as peças montadas. O vídeo faz a
montagem: apresenta variável, objetivo e restrição na ordem em que se constrói um modelo, com a
notação sendo escrita na tela. Assistir antes de ler a seção do teste da unidade é a ordem que
funciona melhor.

## Síntese — o que levar

- **Quatro peças, e só quatro:** variáveis de decisão, função objetivo, restrições, parâmetros.
- **A triagem que resolve a maior parte dos erros:** o que se **decide** é variável; o que se
  **mede** é parâmetro.
- **Três das quatro peças, quando erradas, devolvem `Optimal`.** Só a restrição tem chance de
  gritar, e nem sempre grita.
- **Variável de decisão errada apaga a pergunta.** Medido: R$ 403,33 contra R$ 365, com `Optimal`
  nos dois e sem dizer a ninguém o que fazer.
- **Uma só função objetivo.** Escolher, ponderar ou gerar a fronteira são saídas honestas; somar
  unidades diferentes não é.
- **Parâmetro errado nunca dá erro** — dá a resposta certa para o mundo errado. É para isso que
  existe a análise de sensibilidade.
- **O teste da unidade custa um minuto** e pega o que o solver não pega.
- **Fora da Pesquisa Operacional:** separar estrutura de dado é o que permite resolver uma classe
  em vez de um caso.

## Verificação

1. Num enunciado sobre escalas de enfermagem, aparecem: o número de enfermeiros por turno, o custo
   da hora extra, quem fica de folga no domingo e a demanda prevista de pacientes. Classifique cada
   um em variável de decisão ou parâmetro, e justifique pela pergunta de triagem. *(O1)*
2. Uma equipe esqueceu a restrição de capacidade do armazém e o solver devolveu `Optimal`. Como
   isso é possível, e o que teria que ser diferente para ele devolver `Unbounded`? *(O2)*
3. Um modelo minimiza `50·x + 2·y`, onde `x` são caminhões contratados por dia e `y` são
   quilômetros rodados. Aplique o teste da unidade e diga se o modelo passa. *(O3)*

### Leitura executiva

Um modelo de otimização tem quatro peças: **variáveis de decisão** (o que se escolhe), **função
objetivo** (a única medida), **restrições** (o que limita) e **parâmetros** (o que já está dado). A
pergunta que separa as duas peças mais confundidas é sempre a mesma — *o que se decide é variável,
o que se mede é parâmetro* —, e ela resolve a maior parte dos erros de formulação. O que torna este
capítulo um capítulo de diagnóstico, e não de vocabulário, é a assimetria entre as quatro: **três
delas, quando erradas, produzem um modelo que roda e devolve `Optimal`**. Variável de decisão
errada apaga a pergunta sem deixar defeito visível — o capítulo 15 mediu R$ 403,33 contra R$ 365,
com `Optimal` nos dois modelos e, pior, com o modelo errado não dizendo quanto mandar para cada
destino. Função objetivo com unidades somadas — reais mais horas — devolve um número sem
significado. Parâmetro errado **nunca** dá erro: dá a resposta certa para o mundo errado, e é
exatamente por isso que a análise de sensibilidade existe, tendo o erro de R$ 350 do capítulo 12
como o caso em que um parâmetro com prazo de validade foi citado fora dele. Só a restrição tem
chance de gritar, e mesmo ela grita em apenas metade dos casos: restrição faltando às vezes produz
`Unbounded`, mas quando a região continua limitada produz `Optimal` com uma resposta que ninguém
executa. O instrumento prático que fecha o capítulo é o **teste da unidade**: escreva a unidade de
cada variável, multiplique pela unidade de cada coeficiente e confira que todos os termos de uma
mesma soma têm a mesma unidade. Custa um minuto, e pega o que o solver não pega. Por fim, a
anatomia deixa de servir quando a decisão é sequencial e reage ao que acontece, quando não existe
medida única nem por escolha nem por peso, quando só se busca viabilidade e não há objetivo, e
quando o problema não tem estrutura que se repita — caso em que o modelo é uma planilha escrita com
notação matemática.
