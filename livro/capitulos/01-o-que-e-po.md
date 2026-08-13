# 01 — O que é Pesquisa Operacional

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Dizer** o que distingue Pesquisa Operacional (PO) de "usar matemática no negócio" — com
um critério que decide casos concretos, não com uma definição decorada.

**O2.** **Diagnosticar** um problema apresentado como de PO que **não é**, e nomear o que falta.

**O3.** **Julgar** se um caso publicado sustenta o que promete.

## O problema — e por que este capítulo vem depois, não antes

Este é o capítulo 01 e você provavelmente não está começando por ele. **É de propósito.**

Um capítulo "o que é Pesquisa Operacional" escrito antes de qualquer método só pode fazer uma
coisa: **prometer**. Diria que o campo ajuda a decidir melhor, que os modelos revelam o que a
intuição não vê, e você teria de acreditar — ou não.

Escrito depois da Parte II, ele pode fazer outra coisa: **prestar contas**. Tudo o que este
capítulo afirma sobre o campo já foi medido nas páginas anteriores, e cada afirmação aponta para
o número que a sustenta.

O erro caro deste capítulo é o mais difundido do livro, porque não é de conta nem de modelagem —
é de **expectativa**:

> Alguém traz um problema, alguém constrói um modelo, o modelo roda, e ninguém percebe que a
> pergunta que foi respondida não era a pergunta que foi feita. **Não há erro em lugar nenhum**, e
> o projeto fracassa mesmo assim.

Os capítulos anteriores mediram esse erro em quatro formas diferentes. Este capítulo o nomeia.

## O que a PO é, em uma frase — e o que a frase exige

> **Pesquisa Operacional é a disciplina de transformar uma decisão em um modelo explícito, resolvê-lo
> com um método cujas garantias você conhece, e saber o que a resposta autoriza a decidir.**

Três partes, e cada uma exclui alguma coisa.

**"Decisão"** — não descrição. Se ninguém pode escolher nada, não há problema de PO. Prever a
demanda do mês que vem é estatística; **decidir quanto produzir dada uma previsão** é PO. A
diferença é a existência de uma alavanca.

**"Modelo explícito"** — escrito, com variáveis, objetivo e restrições declarados. Um julgamento de
especialista pode ser melhor que um modelo, e frequentemente é; o que ele não é, é **auditável**.

**"Saber o que a resposta autoriza"** — a parte que a maioria das definições omite e que este
handbook mediu página a página. Um número sem alcance declarado não é resposta, é risco.

### O critério que decide casos

Definição decorada não separa nada. Este critério, sim:

| Pergunte | Se a resposta for "não"… |
|---|---|
| Alguém pode **escolher** algo? | não é PO — é previsão, medição ou relatório |
| Existe uma medida **única** para comparar as escolhas? | não é PO ainda — é decisão multicritério, que precisa de outro aparato |
| As escolhas são **limitadas** por algo? | não é PO — se não há restrição, escolha o extremo e pronto |
| Você consegue dizer **o que a resposta não autoriza**? | é PO malfeita, e é o caso mais comum |

A última linha é a que este handbook adiciona ao repertório usual, e ela é a razão de a Parte II ter
vindo primeiro.

## De onde isto veio

### O aperto: decisões grandes demais para a intuição, e urgentes demais para o hábito

A Pesquisa Operacional é correntemente datada da **Segunda Guerra Mundial**, em equipes reunidas
para responder a perguntas que nenhuma disciplina existente cobria: como dispor os radares, como
organizar comboios, quanto de cada recurso alocar a cada frente. Eram decisões com **alavanca real,
medida única e restrição dura** — os três itens da tabela acima.

> ⏳ **Atribuição corrente, não confirmada por identificador nesta rodada.** A origem britânica em
> tempo de guerra e o próprio termo *operational research* aparecem em toda a literatura didática.
> Este handbook **não localizou fonte primária** com identificador para a cena fundadora, e por isso
> a conta como atribuição, não como fato datado. O que **está** conferido é o marco seguinte:
> Programação Linear nasce em 1947, em contexto de logística militar (`✓ᵐ`, [capítulo 09](09-simplex.md)).

### O que se fazia antes

Decidia-se por **experiência acumulada** — o que funcionou da última vez —, e isso funciona
enquanto o problema for parecido com o anterior e pequeno o bastante para caber na cabeça de
alguém. Os dois pressupostos caem juntos quando a escala cresce, e caem exatamente quando a
decisão fica cara.

### A virada: a decisão vira objeto

A virada é tratar **a decisão** como objeto de estudo — escrevê-la, medi-la, compará-la — em vez de
tratá-la como atributo de quem decide. É o que permite que uma decisão seja discutida sem que a
discussão seja sobre a pessoa.

### A ideia reaproveitável

> **Escrever a decisão muda a conversa.** Um modelo explícito transfere a discussão de "eu acho"
> para "esta restrição está certa?" — e a segunda pergunta tem resposta.

Isto vale muito além do campo. A maior parte do valor de um modelo aparece **antes de ele rodar**,
no momento em que alguém precisa dizer, por escrito, o que está sendo escolhido e o que limita.

### Procedência

| Afirmação | Estado |
|---|---|
| A PO nasce em equipes britânicas na Segunda Guerra, e daí o termo *operational research* | ⏳ **atribuição corrente**, sem identificador conferido nesta rodada |
| Programação Linear nasce em 1947, em logística militar | ✓ᵐ herdado do [capítulo 09](09-simplex.md) |
| O recorte do campo adotado por este handbook | 📖 **leitura editorial**, registrada no [estudo 001](https://github.com/GHDaru/operationalresearchaibook/blob/main/estudos/001-corpo-de-conhecimento-po.md) |

## O que a PO entrega, medido nas páginas anteriores

Aqui está a diferença entre este capítulo e uma apresentação do campo: **nada abaixo é promessa**.
Todos os números saem de scripts que rodam neste repositório.

| O que se costuma prometer | O que este livro mediu | Onde |
|---|---|---|
| *"o modelo acha a melhor decisão"* | Acha — **e só dentro de uma faixa**. Um preço-sombra citado fora dela custou **R$ 350** numa compra sem nenhuma conta errada | [cap. 12](12-dualidade.md) |
| *"o modelo dá **o** número"* | Nem sempre existe **um**. Em vértice degenerado, a mesma CPU vale **50 pela esquerda e 0 pela direita** | [cap. 13](13-sensibilidade.md) |
| *"escolher o método certo é detalhe técnico"* | O padrão errado custou **R$ 403,33 contra R$ 365** — com `Optimal` nos dois e **sem dizer** quanto vai para cada destino | [cap. 15](15-modelagem-aplicada.md) |
| *"o solver achou o ótimo"* | Só se o modelo for convexo. Sem isso, mesma região e mesmo objetivo devolveram **22 e 30**, conforme onde a busca começou | [cap. 38](38-convexidade.md) |
| *"método mais novo é melhor"* | Medido: a forma revisada do Simplex **perde** em duas das três instâncias esparsas testadas | [cap. 11](11-simplex-revisado.md) |

**Leia a coluna do meio inteira antes de seguir.** Ela não é uma lista de defeitos da Pesquisa
Operacional — é a lista do que a disciplina **entrega de verdade** quando alguém sabe ler o que
ela devolve. Cada linha é uma decisão que teria sido tomada errado por quem só olhasse o número.

## Quando não serve

**1. Quando não há alavanca.** Se ninguém pode mudar nada, o modelo produz um retrato. Retrato é
útil e não é decisão.

**2. Quando a medida única não existe de verdade.** Muitos problemas reais têm objetivos
genuinamente conflitantes — custo e risco, lucro e emprego. Forçá-los numa única função objetivo
esconde a escolha em vez de revelá-la, e o [capítulo 03](03-anatomia-do-modelo.md) trata disso.

**3. Quando o dado não existe.** Um modelo bom com dado inventado é pior do que nenhum modelo,
porque tem aparência de rigor. A PO não cria dado.

**4. Quando a decisão é política.** Há decisões em que a pergunta *"qual maximiza o quê?"* é a
pergunta errada, e o modelo serve para dar cobertura técnica a uma escolha já feita. Reconhecer
isso é competência profissional, não cinismo.

**5. Quando o custo de modelar excede o valor da melhoria.** Decisão que se repete mil vezes por
dia justifica modelo; decisão única e barata, raramente.

## Fundamentos e fontes

**O que está medido aqui.** Nenhum número novo — de propósito. Os cinco da tabela acima vêm das
etapas 05 a 08 do `po-zero` e estão conferidos nos capítulos que os produziram, cada um com teste
que compara o texto publicado com a medição.

**O que continua em dívida:** a fonte primária da origem do campo na Segunda Guerra, `⏳` procurada
e não localizada por identificador nesta rodada.

> 🟡 **Este capítulo está em v0.** Não passou por revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap01"></div>

Três exercícios, e nenhum pede conta. O primeiro aplica o critério de quatro perguntas; o segundo
diagnostica um projeto que se apresenta como de PO; o terceiro julga um caso publicado.

## Assista

**[O que é Pesquisa Operacional — EP 1](https://www.youtube.com/watch?v=y5zDojg3hzo)** ·
[João Sarubbi](https://www.youtube.com/@joaosarubbi) · 7min28s

**O que ele resolve:** este capítulo define o campo **por exclusão** — pelo critério que decide o
que não é PO — porque quem chega aqui já viu nove capítulos de método. O vídeo faz a apresentação
direta, com exemplos, em menos de oito minutos. É a porta de entrada para quem chegou pelo
capítulo 01 de verdade, e a segunda passada para quem chegou pela Parte II.

> **Fonte autorizada.** O canal de João Sarubbi, professor titular do Centro Federal de Educação
> Tecnológica de Minas Gerais (CEFET-MG), **autorizou o uso dos seus vídeos neste handbook** — é a
> fonte curada primária da [Videoteca](../videoteca.md), e esta é a primeira vez que ela é usada.

## Síntese — o que levar

- **PO é transformar uma decisão em modelo explícito, resolvê-lo com um método cujas garantias
  você conhece, e saber o que a resposta autoriza.** As três partes excluem coisas diferentes.
- **Quatro perguntas decidem se é PO:** há alavanca? há medida única? há restrição? você sabe dizer
  o que a resposta **não** autoriza?
- **A última das quatro é a que este handbook acrescenta**, e a Parte II inteira existe para
  responder a ela.
- **Nada neste capítulo é promessa** — os cinco números da tabela saem de scripts que rodam aqui.
- **Prever não é decidir.** Sem alavanca, o modelo produz retrato.
- **Modelo com dado inventado é pior do que nenhum**, porque tem aparência de rigor.
- **Fora da Pesquisa Operacional:** escrever a decisão muda a conversa — de "eu acho" para "esta
  restrição está certa?", que é uma pergunta com resposta.

## Verificação

1. Um gerente pede um "modelo de PO" para prever o volume de chamados do próximo trimestre. Aplique
   as quatro perguntas e diga o que você responde. *(O1)*
2. Um projeto entrega um modelo que roda, com `Optimal`, e ninguém consegue dizer sob que condições
   a recomendação deixa de valer. O que falta, e por que isso é defeito e não detalhe? *(O2)*
3. Um caso publicado relata "economia de 30% em custos logísticos com Pesquisa Operacional". Que
   três perguntas você faz antes de citá-lo? *(O3)*

### Leitura executiva

Pesquisa Operacional é a disciplina de **transformar uma decisão em modelo explícito, resolvê-lo
com um método cujas garantias se conhecem, e saber o que a resposta autoriza decidir** — e cada uma
dessas três partes exclui algo. "Decisão" exclui descrição: prever a demanda é estatística, decidir
quanto produzir dada a previsão é PO, e a diferença é a existência de uma alavanca. "Modelo
explícito" exclui o julgamento não escrito, que pode ser melhor e não é auditável. "Saber o que a
resposta autoriza" é a parte que a maioria das definições omite e que este livro mediu página a
página. Quatro perguntas decidem casos concretos onde a definição decorada não decide: há algo a
escolher? há uma medida única para comparar? há restrição? e você consegue dizer o que a resposta
**não** autoriza? — sendo a última a contribuição própria deste handbook, e a razão de a Parte II
ter vindo antes desta página. O que sustenta tudo isso não é promessa: um preço-sombra citado fora
da faixa custou **R$ 350** numa compra em que nenhuma conta estava errada; em vértice degenerado a
mesma CPU vale **50 pela esquerda e 0 pela direita**, de modo que "o número" às vezes não existe; o
padrão de modelagem escolhido errado custou **R$ 403,33 contra R$ 365** e, pior, deixou de
responder à pergunta feita; um modelo não convexo devolveu **22 ou 30** conforme onde a busca
começou, com `Optimal` nos dois casos; e a forma mais moderna do Simplex **perdeu** em duas das
três instâncias esparsas medidas. A disciplina serve quando há alavanca, medida única, restrição e
dado real — e não serve quando a decisão é política, quando os objetivos são genuinamente
conflitantes, ou quando o custo de modelar excede o valor da melhoria.
