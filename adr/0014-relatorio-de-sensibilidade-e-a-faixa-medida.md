# ADR 0014 — O relatório de sensibilidade, e como uma faixa entra no livro

**Data:** 2026-08-13 · **Rodada:** 009 (lote 1 da v0) · **Estado:** decidido pelo agente sob a
delegação do autor; **aguardando ratificação**

## Contexto

O capítulo 13 (Análise de sensibilidade) tem como objetivo O1 *"ler um relatório de sensibilidade
e dizer o que cada faixa autoriza"*. Isso abriu uma decisão editorial e expôs, no caminho, um
defeito de medição que já tinha chegado a texto de capítulo.

Um comitê de três especialistas foi consultado — lentes **didática**, **conformidade
constitucional** e **rigor técnico**. Cada recomendação foi **reconferida por medição própria
antes de ser aceita**; o que segue é o que sobreviveu à reconferência.

---

## D1 — O relatório de sensibilidade é de formato próprio, com tabela de correspondência

**Decisão:** o capítulo 13 publica um relatório **neutro**, gerado pelo `po-zero`, e **depois** do
exemplo percorrido apresenta uma tabela curta de correspondência de **nomes** ("neste handbook" ↔
"como costuma aparecer em relatórios comerciais"). Não reproduz o layout de nenhum fornecedor.

**Por quê.** As três lentes convergiram, por caminhos diferentes:

- **Conformidade.** O Princípio IV é literal: *"Custo zero é requisito, não preferência: solver
  aberto na trilha padrão. Solver comercial pode aparecer como comparação, nunca como
  dependência."* Fazer um objetivo declarado depender do layout de um produto licenciado é
  dependência. O Princípio X autoriza **metadado** e proíbe **conteúdo** — nome de campo é
  metadado; grade reproduzida é imitação de produto.
- **Didática.** O erro caro não é não achar a coluna: é ler a coluna certa com o significado
  errado. O relatório comercial empilha **duas famílias de faixa com os mesmos rótulos** —
  "permitido aumentar/reduzir" aparece para coeficiente do objetivo (quanto o **plano** aguenta) e
  para lado direito (quanto o **preço** vale). Um formato próprio pode **rotular a distinção**;
  imitar a grade de outro é herdar a fusão que produz o erro.

**Contenção declarada, porque a tabela de correspondência é ímã de amontoado:** duas colunas, uma
linha por campo, **data de captura** na tabela, e `⏳` no rótulo que não foi conferido em fonte
aberta. Fornecedor que acumular `⏳` sai da tabela — dívida declarada vence invenção.

**Lacuna registrada na constituição.** O Princípio X proíbe reproduzir *"livros-texto e materiais
de estudo de terceiros"* e **não nomeia** artefato emitido por software. A proibição aqui é
sustentada pelo IV, não pelo X. Fica anotado como candidato a emenda PATCH; **não** foi emendado
nesta rodada, porque emenda constitucional é decisão do autor.

---

## D2 — Faixa não entra no livro por varredura. Entra por álgebra, com conferência independente

**Decisão:** toda faixa de sensibilidade publicada é calculada por **álgebra exata** sobre o
quadro final, e **conferida por um segundo caminho que não usa a mesma derivação**. A etapa
encerra com erro se a conferência falhar.

**O defeito que produziu esta decisão.** A `faixa_de_validade` da etapa 05 varria o lado direito
de meio em meio e reportava o último valor em que a base do quadro final ainda era a mesma. O erro
não é de precisão, é de definição: a varredura mede **em que base o Simplex aterrissa**, não **para
que lado direito a base continua ótima**. Na fronteira o vértice fica degenerado e o método pode
aterrissar em outra base equivalente — então a varredura lê "mudou" um passo cedo demais.

| Recurso | Publicado no capítulo 12 | Correto |
|---|---|---|
| CPUs | `[13/2, 12]` | **`[6, 12]`** |
| pentes de 16 GB | `[10, 39/2]` | **`[10, 20]`** |

Conferido à mão, por caminho independente, antes de aceitar a correção: com estoque de 6 CPUs o
ótimo é $(0,6)$ e $z = 900$, e $6 \times 50 + 12 \times 50 = 900$ — o preço de 50 ainda prevê o
valor. Com 5,5, o ótimo real é 825 contra 875 previstos: quebra. A fronteira é 6.

**O detalhe que torna o defeito pior do que "dois números errados":** o teto `12` saiu **certo**,
por sorte de desempate. Um método que erra um lado e acerta o outro sem avisar não é medição — é
um gerador de números com aparência de medição.

**O método correto**, e ele cabe no quadro que o leitor já tem: com todas as restrições `<=`, as
colunas de folga do quadro final são $B^{-1}$. Somar $\Delta$ ao estoque $i$ desloca as básicas por
$\Delta$ vezes a coluna $i$ de $B^{-1}$, e a base segue viável enquanto todas continuarem $\ge 0$.
Exato, em fração, sem passo e sem resolver de novo.

**A conferência independente** não usa $B^{-1}$: põe o estoque na fronteira e um pouco além, e
exige que o preço **acerte na fronteira** e **erre além dela**. Faixa curta demais passa
despercebida por qualquer teste que só confira o valor certo — o preço simplesmente acerta além.

---

## D3 — Número publicado sem portão pela segunda vez é defeito do pipeline

**Decisão:** a medição da Parte ganha uma suíte de testes que **lê o capítulo publicado** e exige
que cada número medido apareça no texto na forma exata — e que **as versões antigas não apareçam**.

**Por quê.** O sinal D9.6 da [ADR 0013](0013-o-que-e-a-v0.md) diz: *"defeito de mesma classe pela
segunda vez — aí o defeito é do pipeline, não do artefato"*. É a segunda vez:

| Quando | Defeito | O que nasceu dele |
|---|---|---|
| Rodada 005 | `cap07.exC` declarava um ótimo que o modelo não tinha | `verifica-otimos.mjs` |
| **Rodada 009** | O capítulo 12 publicava duas faixas que a medição não sustentava | **`test_dual.py`** |

Os dois defeitos são a mesma classe: **número no livro que nenhum portão sabia conferir**. Nove
portões passaram verdes sobre as faixas erradas, e todos estavam certos em passar — nenhum deles
tinha como saber que aquele texto continha uma medição.

O teste inclui, de propósito, uma guarda contra a **correção parcial**: um teste que só confere o
valor certo passa verde num capítulo que publica o certo **e** o errado em lugares diferentes.

---

## D4 — A dívida histórica do capítulo 13 é curta, e nomeada

**Decisão:** o capítulo 13 abre a seção de origem como **"De onde isto veio — em dívida"**,
declarando o que foi procurado, quando, e o que voltou — incluindo que a busca devolveu
**Geoffrion & Nauss (1976)**, que é **pós-otimalidade em programação inteira** e portanto **não
serve**. A hipótese "a análise de sensibilidade nasce nos próprios manuais" entra como `⏳` e **não
sustenta afirmação**. A origem dos nomes fica `❌` se não localizada.

**A seção deve ser curta.** O Princípio XII manda que *inventar história é pior do que omiti-la*.
Curta e honesta passa; longa e plausível é exatamente o que o princípio combate.

**Correção junto:** o capítulo 12 afirmava em prosa que o *minimax* foi "publicado por von Neumann
em 1928" enquanto a sua própria tabela de Procedência marcava a afirmação `⏳`. Corpo afirmando o
que a tabela nega é o modo mais silencioso de um sistema de selos deixar de valer. Corrigido nesta
rodada.

---

## Consequências

**Boas.**

- As faixas do livro passam a ser exatas e conferidas por dois caminhos.
- A etapa 05 ganha a **faixa dos coeficientes do objetivo** (`[75, 150]` e `[100, 200]` para os
  dois produtos da montadora), que é a metade do relatório de sensibilidade que ainda não tinha
  artefato — o critério A4 da spec 009 passa a ser cumprível para o capítulo 13.
- O livro ganha um portão de classe nova: **texto conferido contra medição**.

**Ruins, e declaradas.**

- O capítulo 12 precisou ser corrigido em quatro lugares e um exercício foi reescrito. Isso
  aconteceu **antes do portão de merge** — o capítulo estava na branch, não publicado —, mas
  consumiu uma rodada de trabalho que uma medição correta teria evitado.
- `test_dual.py` acopla a etapa ao texto do capítulo. É acoplamento **deliberado**: é ele que faz
  o número no livro ter dono. O custo é que renomear ou reescrever a seção quebra o teste, e o
  teste tem de ser atualizado junto — o que é a intenção, não o efeito colateral.

## Sinal de parada que **não** disparou, e por quê

O D9.1 manda parar ao **editar texto já publicado**. O capítulo 12 estava na branch de
desenvolvimento e **não havia sido mergeado na `main`** — publicação, neste repositório, é o merge.
Corrigir trabalho em voo, dentro da mesma rodada e antes do portão humano, é o que a branch existe
para permitir. Se as faixas erradas tivessem chegado à `main`, esta ADR pararia aqui e esperaria o
autor.
