# Plan 007 — Portão de fontes

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-12
· **Estado:** revisto após o veredito do guardião; **nenhuma linha do portão escrita ainda**

> **Histórico deste documento.** A primeira versão foi ao `guardiao-processo` antes de qualquer
> implementação — como manda o ciclo, e como a rodada 004 não fez. Ele devolveu **PODE PROSSEGUIR
> COM RESSALVAS** com **dez bloqueios**, três dos quais travavam a primeira linha de código. Esta
> versão responde aos dez. O que cada um era, e o que virou, está em "O que o guardião barrou".

## Constitution Check — os 12 princípios do handbook

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | Rodada de **motor**, não de capítulo: não deve exercício nem vídeo | ✅ não se aplica |
| II | Modelar antes de resolver | Não há método novo | ✅ não se aplica |
| III | Evidência acima de retórica | **É o princípio que a rodada serve** — mas o plano o violava. O limiar 0,70 entrou como "o mesmo que o guia externo documenta": citação sem fonte nomeável, num plano cuja rodada existe para eliminar números sem procedência. A cobertura real (12 de ~25) não estava declarada, e a contagem de "44 marcas" não era reprodutível | ⚠️ **corrigido**: o limiar virou **experimento** (`calibracao.json`, limiar 0,78 medido); cobertura e comandos declarados na spec |
| IV | Fonte-base é o experimento executável | Portão em CPU, sem chave paga, offline por padrão. O travamento **é** o artefato que regenera o resultado. O caminho `npm run fontes` ganhou *fixture* e é reexecutável | ✅ |
| V | Arquitetura em três camadas | Aparato editorial | ✅ |
| VI | Atualização por Radar | Nenhum artigo novo no corpus. O guia externo consultado é **ferramenta de processo**, não fonte do livro — e está **nomeado e datado** no ADR 0009, porque fundamenta desenho | ✅ |
| VII | Livro vivo | `HISTORICO.md` (A16); cada entrada do travamento carrega `verificado_em` | ✅ planejado |
| VIII | Português canônico | *Lock* traduzido como **travamento** na 1ª ocorrência | ✅ |
| IX | Sigla nunca nasce nua | Julgado, na 1ª versão, com a desculpa que **o próprio princípio proíbe** ("já está no glossário"). A contagem reinicia a cada documento, e havia sigla nua na spec, no plano **e** na bibliografia — que usa DOI na linha 157 e só expande na 314 | ⚠️ **corrigido** nos três; **CI** entra no glossário e no mapa de siglas (A15) |
| X | Direitos autorais | O Crossref devolve `abstract`, `license` e `funder`. Gravar a resposta crua versionaria **texto de terceiro** — exatamente o que o princípio proíbe. A 1ª versão *descrevia* os campos e não **restringia** o código | ⚠️ **corrigido**: lista fechada de chaves + o portão reprova campo fora da lista ou texto > 300 caracteres (A10) |
| XI | DoD verificável | Faltavam o `pytest` do backend e a **revisão em contexto fresco** — que nesta rodada é a única defesa contra o conflito de interesse | ⚠️ **corrigido**: A14 e A18 |
| XII | Nenhum método cai do céu | Não é capítulo de método | ✅ não se aplica |

## Constitution Check — os 7 princípios de processo do Maestro

Esta tabela **não existia** nos planos 002 a 006. A skill `constitution-check` a exige — "nenhum
plano sem as 7 linhas" — e a constituição do handbook herda a metodologia sem transcrever os
princípios, de modo que ninguém os conferia linha a linha. A lacuna é anterior a esta rodada e
está registrada aqui porque foi aqui que apareceu.

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | Spec-Driven | Nasce de `spec.md`, escrita antes do plano. **Mas a spec ainda não tem o gate do autor** — a 1ª versão reivindicava aprovação que não existia | ⚠️ **corrigido**: estado da spec agora diz "aguardando ratificação" |
| II | Orquestração humano-governada | O **A** (*Accountable*) humano é preservado: três itens explícitos de ratificação, e nada publicado | ✅ |
| III | Reversibilidade / gates de risco | Tudo na branch; a `main` está intocada. O gerador **recusa rodar em integração contínua** (D8 do ADR 0009), para que o reparo de um build vermelho não seja "regerar até ficar verde" | ✅ |
| IV | Test-First / DoD verificável | Onze testes destrutivos (A2, A3, A5–A12) escritos **como critério antes** da implementação | ✅ |
| V | Economia de contexto / fronteira | Três fronteiras independentes: **gerador** (rede), **portão** (leitura) e **contrato** (esquema do travamento). O contrato congela primeiro; os outros dois não compartilham estado | ✅ |
| VI | Artefatos vivos | ADR, glossário, `HISTORICO`, `ROADMAP` e código no mesmo *commit* range | ✅ planejado |
| VII | Governança leve / YAGNI | A quarentena (A6 do ADR 0009) foi **projetada e não construída**: mecanismo de exceção sem instância real é convite | ✅ |

**Violações que impediriam a rodada:** nenhuma. **Cinco ⚠️**, todas corrigidas antes da primeira
linha de código.

## A decisão central: por que um travamento, e não consulta ao vivo

| Contra a consulta ao vivo | Consequência |
|---|---|
| **O build dependeria de rede** | Livro que não compila no avião é livro quebrado. E a rede **falhou duas vezes nesta sessão**: `429` persistente no Semantic Scholar, e `403 Host not in allowlist` no `fetch` do Node |
| **O resultado deixaria de ser determinístico** | O mesmo *commit* passaria hoje e falharia amanhã. Isso não é portão, é sorteio |
| **Não haveria evidência anexada** | Consulta que acontece e some não prova nada depois |

O travamento (`livro/fontes.lock.json`) resolve os três: versionado, lido offline, *diffável*, com
data e camada por entrada. Renová-lo é ato deliberado, e o *diff* é o que o revisor lê.

## Arquitetura

```
livro/bibliografia.md ──parse──▶ {selo, doi, titulo, ano, primeiro_autor}
                                     │
                                     ├── compara ──▶ livro/fontes.lock.json      [portão, offline]
                                     │
   npm run fontes ──▶ doi.org/api/handles  (existe?)                             [gerador, rede]
                  ──▶ api.crossref.org/prefixes  (de quem é o prefixo?)
                  ──▶ Crossref /works  →  OpenAlex /works/doi:  (que trabalho é?)
```

Estados, defesas e alternativas rejeitadas: [ADR 0009](../../adr/0009-portao-de-fontes-doi-inexistente.md).
Semântica do selo: [ADR 0010](../../adr/0010-a-semantica-do-selo.md).

## O que o guardião barrou

| # | Apontamento | Situação |
|---|---|---|
| **B1** | O4 prometia "DOI inventado quebra o build" e a camada 3 mandava **avisar sem reprovar** — que é o destino de um DOI inventado. A exceção era justificada pelo Hoffman, que **não tem DOI** | **Resolvido por consulta a especialista**, com o enquadramento refeito: existência é pergunta ao *Handle System*, não a índice. ADR 0009. **Vai ao autor para ratificação** |
| **B2** | **Conflito de interesse**: travamento e bibliografia saem da mesma mão. O portão passaria a verificar bibliografia contra si mesma | **Quatro defesas** adicionadas: reconferência agendada na integração contínua (A20), primeira execução crua colada antes de qualquer correção (A19), revisão em contexto fresco (A18), idempotência do travamento (A12) |
| **B3** | **Falso verde por rede**: as duas bases fora do ar na hora de gerar ⇒ tudo "não resolvido", quatro testes passam, zero verificação com build verde | **Canários** que abortam a geração sem escrever + limiar de degradação em massa + `indeterminado` nunca gravado (ADR 0009, D5) |
| **B4** | Princípio III desonesto: limiar sem procedência, cobertura não declarada, contagem não reprodutível | **Corrigido, e virou experimento** — ver abaixo |
| **B5** | Princípio X sem *enforcement*: o travamento poderia versionar `abstract` | Lista fechada de chaves + teste (A10) |
| **B6** | Princípio IX julgado pela desculpa que o princípio proíbe | Siglas abertas nos três arquivos; **CI** ao glossário (A15) |
| **B7** | A9/A10 eram leitura humana em tabela dita de máquina; A3 sem procedimento determinístico; A2 circular | Tabela agora marca **M/H** por linha; A3 virou "**zero chamadas de rede**", instrumentado; A2 exige contagem independente = 12 |
| **B8** | A1 exigia só "encadeado no build" | Posição fixada **antes de `build.mjs`**, e `SEM_PDF=1` também verde |
| **B9** | Pasta `007-atribuicoes-pendentes` prometia o que a spec põe fora de escopo; `ROADMAP:59` marcava `007 🚧`; o item "Portão de URL externa" continuava aberto | Pasta renomeada para **`007-portao-de-fontes`**; A17 cobre os dois pontos do `ROADMAP`, **dizendo que o buraco de URL continua aberto** |
| **B10** | Armadilhas de parser sem teste: `✓ᵐ` prefixado por `✓`, DOI *case-insensitive*, entradas com dois links, ênfase Markdown no título | A11 (falha por ignorância reprova) + os casos entram no *fixture*. **Uma armadilha já se materializou** — ver abaixo |

**E o apontamento que não era meu para resolver:** o guardião observou que C2 fixa o **padrão de
prova da bibliografia**, que vale para todas as rodadas futuras. Foi para ADR e está na lista de
ratificação do autor.

## O experimento que o plano devia ter trazido — e o que ele derrubou

O limiar 0,70 caiu. Não por argumento: por medição, em
[`calibra-limiar.mjs`](calibra-limiar.mjs) e [`coleta-amostra.mjs`](coleta-amostra.mjs).

**Primeiro derrubou o meu extrator.** A alternância única do *regex* casava o **nome do autor em
negrito** antes do título entre aspas, porque o motor escolhe pela **posição** antes de escolher
pelo ramo: em `**DANTZIG, George B.** "The Diet Problem"`, o ramo do itálico acha casamento no
segundo asterisco. Doze "títulos declarados" que eram doze nomes de autor. É exatamente a
armadilha de parser que o B10 previa, materializada antes da implementação.

**Depois derrubou a ideia de limiar único.** Com os títulos certos, o pior par legítimo (0,517 —
Spielman & Teng, cujo subtítulo o Crossref corta) ficou **abaixo** do melhor impostor (0,560 —
dois títulos diferentes que compartilham *"simplex method"*). Janela negativa: **não havia limiar
defensável**.

A correção foi de **critério**, não de número. Divergência legítima tem forma: truncamento produz
**contenção**; jargão compartilhado, não. Com contenção antes de bigramas:

```
12 pares legítimos → todos 1,000
melhor impostor    → 0,560
janela             → 0,440      limiar medido: 0,78
```

## Estratégia — a ordem importa

1. **Congelar o contrato** do travamento (fronteira compartilhada).
2. **O portão, contra a bibliografia como ela está hoje**, e **colar a saída crua antes de
   corrigir qualquer coisa** — sem isso ninguém distingue "a bibliografia estava certa" de "a
   bibliografia foi ajustada até o portão calar".
3. Corrigir o que for defeito real.
4. **Quebrar de propósito**, onze vezes.
5. Registro: legenda, glossário, `ROADMAP`, `HISTORICO`, reconferência agendada.
6. **Revisão em contexto fresco.**

## Riscos

| Risco | Mitigação |
|---|---|
| **Parser frágil** — Markdown não é formato de dados | Falha **alto**: entrada com DOI que não se interpreta é erro, nunca *no-op* (A11). Já cobrou seu preço uma vez, antes da implementação |
| **Falso verde**: passar sem ter verificado nada | O portão **imprime a contagem** e A2 exige que ela bata com uma contagem independente |
| Crossref mudar de contrato | O travamento protege: só `npm run fontes` quebraria, e na cara de quem pediu |
| Travamento virar carimbo | *Diff* + reconferência agendada (A20). O *diff* defende contra desatenção; o agendamento, contra auto-atestação |
| Limiar aceitar título errado | É triagem, não prova: por isso o **ano é exato** (o autor **avisa** — ver ADR 0009, D3), e a reprovação mostra os dois valores |
| **O portão criar confiança maior que a cobertura** | Declarado em número na spec, no `HISTORICO` e no `ROADMAP`: 12 de ~25, e a URL de vídeo — o incidente que motivou tudo — **continua sem mecanismo** |

## Desvio declarado

Rodada de **motor**: não produz capítulo, não passa pelo esqueleto do Guia Editorial nem pelo
mínimo de exercícios. A regra que isso fixa — **rodada de motor é raia plena, não leve** — foi
para o [ADR 0010](../../adr/0010-a-semantica-do-selo.md), anexo R1, porque plano expira e regra
não.
