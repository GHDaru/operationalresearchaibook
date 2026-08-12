# ADR 0012 — O desenho da medição do capítulo 11, e o que ela não prova

**Data:** 2026-08-12 · **Status:** aceito na branch, **pendente de ratificação no gate de merge**
· **Rodada:** 008 · **Origem:** consulta a especialista de didática (C2/C4) + sete bloqueios do
guardião do processo sobre falso verde

## Contexto

O capítulo 11 afirma que a forma revisada faz **menos trabalho** que o quadro completo. Essa é a
tese, e ela é empírica. O guardião apontou seis vetores pelos quais a medição planejada podia
produzir número que **parece** prova e não é — e uma pergunta que reorganiza o resto:

> "Contagem de operações comparando duas implementações escritas pela mesma pessoa é evidência de
> quê, exatamente?"

A resposta honesta: é evidência sobre **este par de implementações, nestas instâncias, sob uma
convenção de contagem escolhida por quem quer que o resultado dê certo**. O quadro da etapa 03
foi escrito para ser **legível**; a forma revisada seria escrita para **ganhar**. A contagem
mediria a diferença de intenção tanto quanto a diferença de método.

Este ADR fixa o desenho que torna a medição defensável, e declara o que ela continua não
provando.

## Decisão

### D1 — Uma primitiva aritmética instrumentada, compartilhada pelas duas formas

A `etapa-05` define um tipo numérico que **conta** as operações e é genérico sobre a aritmética
de base. **As duas formas usam o mesmo tipo.** Duas réguas diferentes não comparam nada.

A convenção de contagem é **publicada junto do número**: o que conta como operação (multiplicação,
divisão, soma, comparação) e o que não conta (indexação, cópia de estrutura).

### D2 — A etapa 03 **não é tocada**, e vira oráculo

Instrumentar a aritmética quebraria a invariância byte a byte de `po-zero/etapa-03-simplex/resultados.json`
(hash `0d427a9f…`), que a rodada 006 estabeleceu como prática. E `quadro.py` fixa `Num = Fraction`
na linha 29, de modo que rodar em `float` exigiria generalizar código publicado.

**Conduta:** a `etapa-05` implementa **as duas formas**, ambas sobre a primitiva instrumentada. A
etapa 03 permanece intocada e serve de **oráculo**: a forma-quadro da etapa 05 tem de reproduzir
exatamente os resultados publicados. Isso resolve três problemas de uma vez —

| Problema | Como se resolve |
|---|---|
| Contagem justa | As duas formas da etapa 05 compartilham a primitiva |
| `Fraction` × `float` honesto | **A mesma implementação**, dois tipos de base. Não é "duas implementações em duas aritméticas" |
| Regressão da etapa 03 | Hash preservado, e a igualdade com o publicado é o teste da forma-quadro nova |

O custo — o quadro implementado duas vezes — é **assumido**, e é menor que o de publicar como
efeito do ponto flutuante algo que pode ser efeito da reimplementação.

### D3 — Trajetória de pivô idêntica, provada, e dois números separados

As duas formas usam a **mesma regra de entrada e o mesmo desempate de saída**, e a `etapa-05`
**afirma a identidade da sequência de bases** em aritmética exata. Sem isso, o total de operações
mistura *"menos trabalho por iteração"* com *"outro número de iterações"* — dois efeitos, um
número, atribuição impossível.

O relatório publica **operações por iteração** e **número de iterações**, separadas. Nunca só o
produto.

### D4 — Testemunha independente, como na etapa 04

A comparação forma-revisada × forma-quadro compara código que compartilha camada: defeito comum
é invisível às duas. A etapa 04 já resolveu isto
(`po-zero/etapa-04-casos-especiais/experimento.py`, *"o solver de mercado como testemunha
independente"*), e abandonar a prática seria regressão.

**O solver aberto confere o ótimo de toda instância publicada.**

### D5 — Instâncias congeladas **antes** de olhar resultado

O compromisso da spec — *publicar o que o experimento mostrar* — cobre a **direção do resultado**,
não a **escolha da amostra**. Gerar até aparecer é compatível com publicar o que apareceu.

Conduta, herdada do critério A19 da rodada 007:

1. **Regra de geração e semente ficam no código antes da primeira execução.**
2. **Todas as instâncias geradas são publicadas**, não as que mostraram o efeito.
3. **A saída crua da primeira execução é colada na verificação, antes de qualquer ajuste.**
4. Um **controle negativo** obrigatório: a instância **densa**, onde a forma revisada **não** deve
   ganhar. Experimento sem caso em que a tese falharia não é experimento.

### D6 — O resíduo é medido com desconfiança declarada

$\lVert Bx - b\rVert$ em `Fraction` é **identicamente zero** — reta em zero não prova
envelhecimento. Em `float`, nas instâncias que este livro constrói, ele vive na casa de
$10^{-16}$, e "subida" em escala logarítmica pode ser ruído de arredondamento com legenda de
fenômeno.

**Obrigatório:** magnitude **absoluta** publicada junto da curva; um **controle** (refatorar a
cada $k$ iterações contra nunca refatorar); e o tamanho de instância em que o efeito seria
detectável, **pré-declarado**. Se esse tamanho não couber em CPU, **isso é o resultado**, e o
capítulo diz que o envelhecimento não foi demonstrado aqui.

> Uma versão anterior do plano da rodada escreveu que a instrumentação *"já produz as duas
> curvas — densidade crescendo e resíduo subindo"*. Isso era resultado experimental
> **pré-declarado como fato**, antes de existir uma linha de código, num plano cuja spec promete
> publicar o que o experimento mostrar. Apagado.

### D7 — "Densidade" nomeia uma coisa só

Havia duas: a densidade **de entrada** das instâncias e a densidade **crescente** do arquivo de
atualizações, que é **saída**. Publicar as duas sob o mesmo nome é convite ao raciocínio circular.

- **densidade da instância** — entrada;
- **preenchimento** (*fill-in*) — saída.

E, para atribuir efeito à esparsidade, o experimento varia **densidade com tamanho fixo** e
**tamanho com densidade fixa**. Variar só "tamanho crescente" e medir densidade é fatorial
incompleto.

### D8 — "Estagna de verdade" tem limiar pré-declarado

Estagnação é **sequência de iterações consecutivas em que o valor do objetivo não muda**, em
aritmética exata, com a base mudando. O limiar fica no código **antes** da primeira execução.

**A cascata do corte, mapeada** — o plano declarava um elo de quatro:

| Se estagnação sair | Consequência |
|---|---|
| **O4** cai | Objetivo declarado na spec deixa de existir |
| Exercícios que rastreiam O4 | **Quebram o build** — o portão exige que todo exercício aponte para objetivo existente |
| Capítulo 10, item 5 | A promessa vira endereço errado; a saída *(b)* do [ADR 0011](0011-onde-mora-cada-assunto-da-parte-II.md) passa a ser obrigatória |
| Capacidade do tutor | A descrição muda nos dois lados do espelho |

## O que esta medição **não** prova, e vai escrito no capítulo

1. **Nada sobre solvers reais.** Mede duas implementações didáticas, em Python, em instâncias
   pequenas. Solver de produção é outra espécie.
2. **Nada sobre "a forma revisada" em geral.** Mede *estas* implementações, sob *esta* convenção
   de contagem.
3. **O envelhecimento da fatoração** só é demonstrável se a escala couber em CPU. Pode não caber.
4. A escolha da convenção de contagem é **do autor**, e favorecer um lado é possível. A defesa é
   publicá-la, não escondê-la.

## Consequências

- A `etapa-05` fica maior do que o previsto — implementa duas formas, e não uma.
- A etapa 03 fica **intacta**, com o hash preservado.
- O capítulo ganha um controle negativo, que é conteúdo: *onde a forma revisada não ganha* é
  metade da resposta à pergunta-tese.
- **Se a tese não se sustentar nas instâncias que cabem em CPU, o capítulo publica isso** — e a
  explicação vira *por que o ganho só aparece em escala que não cabe aqui*, que também ensina.
