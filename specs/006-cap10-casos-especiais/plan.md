# Plan 006 — Capítulo 10: Casos especiais e degenerescência

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-09
· **Estado:** escrito **antes** da implementação do capítulo

> **Por que esta linha existe.** Na rodada 004 este documento foi escrito **depois** da
> implementação, e isso o esvaziou: um Constitution Check escrito depois descreve, não autoriza.
> Aqui ele volta a ser gate. O que já existe quando este plano é escrito é apenas **medição** —
> a instrumentação do `po-zero`, que o Guia Editorial manda vir antes do texto. Nenhuma linha de
> capítulo foi escrita.

## Constitution Check

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | ≥3 exercícios com devolutiva que explica + 1 vídeo. Os exercícios são do tipo **ler a saída** e **diagnosticar o modelo** (Guia §4.1), que é o que este capítulo treina | ✅ planejado |
| II | Modelar antes de resolver | É a **tese** do capítulo, e ela ganhou teste operacional ([ADR 0007](../../adr/0007-fronteira-entre-modelo-e-metodo.md)): *o que é do modelo sobrevive à troca do método*. Seção "quando não serve" obrigatória | ✅ |
| III | Evidência acima de retórica | Duas fontes primárias **lidas**; o que não abriu está `⏳` no [ADR 0008](../../adr/0008-atribuicao-da-instancia-que-cicla.md). **Mas**: no momento em que este plano foi submetido ao gate, os números "Dantzig cicla / Bland termina" já estavam afirmados na spec e no ADR 0007 **sem artefato que os regenerasse**, e a *docstring* de `quadro.py` afirmava que Bland "prova terminação" e "é mais lento" — as duas sem fonte e sem medição | ⚠️ **corrigido durante a rodada** — ver §"O que o guardião barrou" |
| IV | Fonte-base é o experimento executável | `po-zero/etapa-04-casos-especiais`, CPU, solver aberto, saída determinística | ✅ planejado |
| V | Arquitetura em três camadas | Capítulo de núcleo | ✅ |
| VI | Atualização por Radar | Os artigos lidos entram na bibliografia e no Radar. **A ordem foi invertida**: entraram primeiro na bibliografia, e o Radar só foi atualizado depois que a revisão independente apontou | ⚠️ **corrigido, com a dívida registrada na própria página do Radar** |
| VII | Livro vivo | Selo de datação; edição no histórico | ✅ planejado |
| VIII | Português canônico | Só PT (ADR 0002). *Stalling* mantido como termo consagrado, com tradução ao lado na 1ª ocorrência | ✅ |
| IX | Sigla nunca nasce nua | PL aberta na 1ª ocorrência do capítulo; verbetes novos no glossário | ✅ planejado |
| X | Direitos autorais | A instância de ciclagem é **dado matemático**, não texto de terceiro, e entra com atribuição em três camadas (ADR 0008). Nenhuma reprodução de prosa alheia | ✅ |
| XI | DoD verificável | Build, ilha e testes verdes, com saída colada. **No gate, o hash `0d427a9f…` era alegado sem `verificacao.md` que o anexasse** — alegação sem evidência é o que o princípio proíbe | ⚠️ **corrigido**: [`verificacao.md`](verificacao.md) criado, com o alcance da evidência declarado |
| XII | Nenhum método cai do céu | Seção "De onde isto veio" com duas fontes lidas e ressalvas visíveis. Ideia reaproveitável declarada | ✅ |

**Violações que impediriam a rodada:** nenhuma — mas a tabela **não nasceu honesta**, e a
correção está registrada abaixo. Uma tabela de Constitution Check com zero ⚠️ é, por si só, um
sinal de alerta: as rodadas 003 e 004 tinham uma cada.

**Riscos constitucionais que o plano assume conscientemente:** o Princípio III fica visivelmente
"sujo" nesta rodada — a seção de origem terá mais `⏳` do que um livro comum exibiria. É
consequência direta do XII, e o ADR 0008 argumenta por que isso é preferível a atribuir errado.

## Decisões já registradas em ADR

A numeração é a **canônica da spec**. Uma versão anterior deste plano renumerava, o que quebrava
a rastreabilidade — apontado pelo guardião e corrigido.

| # (spec) | Decisão | Onde |
|---|---|---|
| **D1** — divisão 09/10 | Detecção já ensinada no cap. 09 vira **linha de tabela com âncora**; detecção inédita vira **seção** | [ADR 0007](../../adr/0007-fronteira-entre-modelo-e-metodo.md) |
| **D2** — instância condutora | Montadora para quatro vereditos; instância de laboratório só para o ciclo, e **a troca de instância é a lição** | [ADR 0008 — emenda](../../adr/0008-atribuicao-da-instancia-que-cicla.md#emenda--a-instância-condutora-do-capítulo-d2-da-spec) |
| **D3** — quanto de Bland | Entra por **demonstração**, não por prova; enunciado exato fica `⏳` | [ADR 0008](../../adr/0008-atribuicao-da-instancia-que-cicla.md) |
| **D4** — onde mora a degenerescência | **Sintoma de modelo**; ciclagem é **defeito de regra**; a distinção vira o teste que o leitor leva | [ADR 0007](../../adr/0007-fronteira-entre-modelo-e-metodo.md) |

Registro à parte, porque não estava na spec e virou decisão: **a atribuição da instância que
cicla** entra em três camadas (Hoffman e Wolfe primeiro, ✓ lido; Beale como a que o ensino faz
circular, ✓ᵐ; a forma primal exata, `⏳`). ADR 0008.

## Estratégia

Quatro blocos, nesta ordem — e a ordem é a do Guia Editorial:

1. **A instrumentação primeiro.** O Simplex do capítulo 09 ganha a regra de pivoteamento como
   **parâmetro**, e a etapa 04 mede os cinco casos. Só então o capítulo é escrito.
2. **Objetivos e exercícios antes do corpo** (Backward Design).
3. **O capítulo**, na estrutura recomendada pelo especialista de didática (ADR 0007).
4. **Motor e registro**: capacidade do tutor nos dois lados do espelho, sumário, mapa,
   videoteca, glossário, bibliografia, histórico — e a **correção do capítulo 09**.

## Decisões de implementação

| Decisão | Por quê |
|---|---|
| **Parametrizar `quadro.resolver(regra=...)` na etapa 03**, em vez de duplicar o Simplex na etapa 04 | Duplicar 200 linhas para trocar duas escolhas seria pior de manter e pior de ler. A mudança é **aditiva e retrocompatível**, e foi verificada: `resultados.json` da etapa 03 permanece **byte a byte idêntico** (`0d427a9f…` antes e depois) |
| **Detectar ciclo por repetição de base, na etapa 04, e não dentro de `quadro.py`** | Manter o motor do capítulo 09 exatamente como publicado. A detecção é *post-hoc* sobre as iterações que `resolver` já devolve |
| **Degenerescência induzida por uma restrição de negócio plausível** — contrato limitando o total montado a 10, que coincide com o limite de CPU | Uma restrição redundante inventada "para o exemplo" ensinaria menos. Esta tem história, e é exatamente o caso que o capítulo quer diagnosticar |
| **Múltiplos ótimos na própria montadora**, com lucro (100, 200) | O objetivo fica paralelo à restrição de memória. O quadro final mostra **custo reduzido zero em variável não-básica** — a detecção que o capítulo 10 ensina e o 09 não ensinou |
| **O limite de iterações vira evidência, não erro** | Quando a regra de Dantzig estoura o limite na instância que cicla, isso **é** o resultado. O experimento imprime as bases repetidas para provar que é ciclo, e não lentidão |

## Mudanças de motor previstas

| Mudança | Por quê |
|---|---|
| `quadro.resolver` aceita `regra="dantzig" \| "bland"` | Sem isso não há como **medir** a diferença entre as regras, que é o centro do capítulo |
| Capacidade `casos_especiais` nos dois lados do espelho | Gating por capítulo, como as anteriores |
| Nenhum portão novo previsto | Os sete existentes cobrem esta rodada. Se a implementação revelar afirmação não verificável, o portão entra — e o motivo vai para a verificação |

## Riscos de implementação

| Risco | Mitigação |
|---|---|
| **Quebrar a etapa 03**, que está publicada | Já verificado por hash: saída idêntica. O portão de reprodutibilidade roda de novo no fim |
| Ciclagem virar curiosidade sem consequência | O experimento mede **as duas regras na mesma instância**; o preço da troca é **medido** (`custo_da_garantia`): Bland gasta mais pivôs em 2 das 4 instâncias e nunca muda o **valor** — mas **muda o plano** quando há mais de um ótimo |
| O capítulo ficar curto em mecânica | Previsto no ADR 0007: a mecânica vai para a etapa 04 e para exercícios de *ler a saída* |
| Afirmar o enunciado exato da regra de Bland sem ter lido o artigo | A implementação declara **qual** desempate usa e que a correspondência com o artigo é `⏳` |
| Repetir o defeito de confiar em resumo de busca | Nesta rodada, tudo que recebeu `✓` foi **aberto por `curl` e lido**, e os arquivos ficam listados na verificação com tamanho e código de resposta |

## Desvio declarado do esqueleto de capítulo

O Guia Editorial §2 pede, entre outros, os itens "A intuição", "A matemática" e "O algoritmo".
**Este capítulo não os tem como seções**, e o desvio é deliberado: ele não apresenta um método
novo — apresenta **conduta diante de vereditos de um método já ensinado**. Não há intuição a
instalar nem algoritmo a percorrer; há leitura de quadro e decisão.

O que substitui: cada veredito é uma seção com detecção (quando inédita), diagnóstico e conduta.
O portão só exige a seção "De onde isto veio", então este desvio passaria sem registro — e é
justamente por isso que ele está declarado aqui. Apontado pela revisão independente.

## O que o guardião barrou

O plano foi submetido ao `guardiao-processo` **antes** de qualquer linha de capítulo, e ele
devolveu **PODE PROSSEGUIR COM RESSALVAS**, com cinco bloqueios. Quatro eram defeitos reais:

| # | Apontamento | Situação |
|---|---|---|
| 1 | `quadro.py` afirmava que Bland "prova terminação" e "é mais lento" — sem fonte e sem medição, contradizendo o próprio ADR 0008 | **Corrigido.** A *docstring* agora afirma só o que a etapa 04 mede, e "mais lento" virou **medição** (`custo_da_garantia` no `resultados.json`) |
| 2 | `etapa-03/README.md` dizia que o desempate por menor índice "evita os casos conhecidos" — **falso** | **Corrigido**, com a correção declarada no próprio README. A9 foi ampliado para cobrir as três ocorrências |
| 3 | O **D2 da spec** (a instância condutora) estava decidido e **não registrado** em ADR — A11 descumprido | **Corrigido**: emenda ao ADR 0008 |
| 4 | Faltava `verificacao.md`, e o hash era alegado sem evidência anexada | **Corrigido**, com o **alcance** da evidência declarado: o hash prova invariância dos três casos da etapa 03, não retrocompatibilidade geral de `quadro.py` |
| 5 | A spec continuava com status "em clarify" enquanto o plano era construído sobre ela | **Corrigido** |

**E um apontamento que não é meu para resolver.** O guardião observa que o ADR 0007 fixa uma
**tese editorial da Parte II inteira** e obriga a **alterar capítulo já publicado** (o 09), e que
isso está mais perto de "publicação" — gate do autor — do que de *clarify*. Observa também,
corretamente, que **um ADR não pode declarar inaplicável o gate do autor**, como o 0007 fez ao
escrever que esperar não era opção.

A conduta adotada: **o trabalho prossegue na branch, que é reversível, e a tese e a alteração do
capítulo 09 vão ao autor como itens explícitos de ratificação no gate de merge.** Nada foi
publicado na `main`.
