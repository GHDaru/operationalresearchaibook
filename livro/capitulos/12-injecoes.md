# 12 — Injeções

> **Conteúdo revisado em 2026-08** · edição inaugural · [histórico](../HISTORICO.md)
>
> Capítulo em primeira versão — a ser aprofundado com o material do autor.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve conseguir:

1. **Definir** injeção como um **estado**, e explicar por que não é uma ação;
2. **Levantar** premissas de uma conexão específica com quantidade antes de qualidade;
3. **Inverter** premissas para gerar candidatas a solução;
4. **Validar** que uma injeção resolve o diagrama inteiro, não apenas um lado.

## O problema

Chegamos com um conflito bem estruturado — uma Nuvem (capítulo 10) ou um loop (capítulo 11). E agora?

A tentação é partir para o *brainstorming*: reunir as pessoas e pedir ideias. O resultado costuma ser uma lista de sugestões que atendem um lado do conflito e sacrificam o outro — ou seja, mais do mesmo, com aparência de novidade.

Injeções são um caminho diferente. Em vez de gerar ideias no vazio, elas atacam **o que sustenta o conflito**: as premissas. Se o conflito existe porque certas coisas são verdadeiras, então tornar uma delas falsa dissolve o conflito.

## O conceito

> Uma **injeção** é um estado que, se fosse verdade agora, faria o problema deixar de existir.

Duas palavras carregam o peso da definição.

**Estado**, não ação. "Contratar um analista" é ação. "A fila de produção é visível para vendas no momento da venda" é estado. A diferença é decisiva: um estado admite muitas formas de ser alcançado, uma ação já fixou uma delas. Formular como estado mantém o leque de implementações aberto — e a escolha entre elas é o capítulo 13.

**Se fosse verdade agora.** A injeção é descrita como se já existisse, no presente. Não "vamos criar visibilidade", mas "a fila é visível". Essa formulação evita que a discussão sobre viabilidade contamine a geração de ideias.

O termo é de Goldratt, e a lógica por trás dele aparece em *Não é Sorte* (1994): conflitos persistem porque suas premissas persistem.

## O processo em dois passos

### Passo 1 — Levantar premissas

Escolha **uma** conexão do diagrama — uma seta da Nuvem, ou um elo de uma cadeia do loop. Uma só. Injeções nascem de foco, não de abrangência.

Para essa conexão, aplique o método do capítulo 08: complete a frase com "…porque…", pergunte o que quebraria a conexão, e escreva tudo.

Aqui a regra é **quantidade antes de qualidade**. Não filtre, não julgue viabilidade, não descarte o óbvio. Cinco premissas é o mínimo aceitável; dez é um bom alvo. As primeiras são superficiais; as boas aparecem depois.

### Passo 2 — Inverter

Para cada premissa, escreva o **oposto lógico** e pergunte: *se isto fosse verdade, o conflito ainda existiria?*

- Premissa: "a fábrica só sabe da fila depois que o pedido é fechado."
- Inversão: "a fábrica e vendas veem a mesma fila no momento da venda."
- Teste: com isso verdadeiro, ainda é preciso escolher entre atender bem e controlar custos? **Não** — a ação D deixa de exigir a exclusão de D'.

Quando o teste dá negativo — o conflito ainda existe —, descarte e siga. Quando dá positivo, você tem uma injeção candidata.

## Validação

Uma injeção precisa passar por três verificações antes de virar plano:

**Resolve o diagrama inteiro?** Numa Nuvem: as duas necessidades B e C continuam atendidas? Num loop: o giro para. Injeção que atende um lado e sacrifica o outro não é injeção — é a escolha que já estava na mesa.

**É estado, não ação?** Se começa com verbo no infinitivo ("implantar", "contratar", "criar"), reescreva.

**Gera efeitos negativos novos?** Toda mudança carrega consequências. Vale a pena listá-las agora — e, se alguma for grave, ela vira um novo conflito a examinar.

## O que ajuda a inverter

Algumas premissas resistem à inversão direta. Quatro perguntas costumam destravar:

- **Separar no tempo:** e se as duas ações acontecessem em momentos diferentes?
- **Separar no espaço:** e se acontecessem em lugares ou contextos diferentes?
- **Separar por parte:** e se valessem para partes diferentes do sistema — alguns produtos, alguns clientes?
- **Separar por condição:** e se uma regra dissesse quando vale cada uma?

Essas quatro perguntas são um resumo prático de um princípio que aparece também em outras tradições de resolução de problemas: contradições costumam se dissolver quando os dois lados param de disputar o mesmo recurso ao mesmo tempo.

## Erros comuns

**Injeção formulada como ação.** O erro mais comum. Sintoma: ela já vem com projeto, prazo e responsável.

**Filtrar durante o levantamento.** Julgar viabilidade no passo 1 mata as premissas interessantes antes de elas aparecerem.

**Atacar a premissa mais fácil.** A premissa confortável costuma gerar a injeção inócua. A premissa que incomoda é a que rende.

**Injeção que só um lado aceita.** Se a proposta resolve o conflito eliminando uma das necessidades, ela não é solução — é vitória de um lado, e o conflito volta.

**Parar na primeira injeção que funciona.** Gere várias e compare. A primeira raramente é a melhor.

## Mão na massa

<div data-bateria="cap12"></div>

### Leitura executiva

Injeção é um **estado** que, se fosse verdade agora, faria o problema deixar de existir — nunca uma ação, porque estado mantém aberto o leque de implementações. O processo tem dois passos: **levantar premissas** de uma única conexão do diagrama (quantidade antes de qualidade, dez é um bom alvo) e **inverter** cada uma, testando se o conflito sobreviveria à inversão. Valide em três frentes: resolve o diagrama inteiro (as duas necessidades seguem atendidas), é estado e não ação, e os efeitos negativos novos são aceitáveis. Quando a inversão emperra, tente separar no tempo, no espaço, por parte ou por condição.
