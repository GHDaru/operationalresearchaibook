# Plan 007 — O selo vira medição

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-12
· **Estado:** escrito **antes** de qualquer linha de implementação

## Constitution Check

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | Rodada de **motor**, não de capítulo. Não cria capítulo, logo não deve exercício nem vídeo. O mínimo de 3+1 se aplica a capítulo, e o portão `verifica-capitulos.mjs` continua cobrindo os cinco publicados | ✅ não se aplica |
| II | Modelar antes de resolver | Não há método novo | ✅ não se aplica |
| III | Evidência acima de retórica | **É o princípio que a rodada serve.** Hoje "nenhum DOI inventado" é promessa; ao fim, é portão | ✅ |
| IV | Fonte-base é o experimento executável | O portão roda em CPU, sem chave paga, offline por padrão. O *lock* versionado **é** o artefato que regenera o resultado | ✅ |
| V | Arquitetura em três camadas | Aparato editorial; não toca a divisão núcleo/aplicados/fronteira | ✅ |
| VI | Atualização por Radar | Nenhum artigo novo entra no corpus. O guia externo consultado (`academic-research-skills`) **não é fonte do livro** — é ferramenta de processo, e por isso vai ao ADR, não ao Radar | ✅ |
| VII | Livro vivo | `HISTORICO.md` recebe a edição; o *lock* carrega a data de cada resolução | ✅ |
| VIII | Português canônico | *Lock* mantido como termo consagrado, com tradução na 1ª ocorrência do README do portão | ✅ |
| IX | Sigla nunca nasce nua | **DOI**, **API** e **JSON** já estão no glossário; **CI** (*Continuous Integration*, integração contínua) aparece no plano e **não está** — entra no glossário e no mapa de siglas do motor | ⚠️ **dívida aberta pelo próprio plano**, fechada na task T7 |
| X | Direitos autorais | O portão grava **metadados bibliográficos** — autor, título, ano, veículo, DOI. Nada de texto de terceiro. É exatamente o que a política de `materiais/` já permite | ✅ |
| XI | DoD verificável | Quatro testes destrutivos (A5, A6, A7 e o de rede) com saída colada em `verificacao.md` | ✅ planejado |
| XII | Nenhum método cai do céu | Não se aplica: não é capítulo de método | ✅ não se aplica |

**Violações que impediriam a rodada:** nenhuma. **Uma dívida aberta pelo plano** (IX), com task
própria — registrada aqui porque um Constitution Check sem nenhum ⚠️ costuma significar que
ninguém olhou.

## A decisão central: por que um *lock*, e não uma consulta ao vivo

O caminho óbvio seria o portão consultar o Crossref a cada `npm run build`. Foi descartado por
três razões, e o descarte é a decisão desta rodada:

| Contra a consulta ao vivo | Consequência |
|---|---|
| **O build passaria a depender de rede** | Um livro que não compila no avião é um livro quebrado. E a rede **já falhou** nesta sessão: a API do Semantic Scholar devolveu `429` persistente no rodízio anônimo |
| **O resultado deixaria de ser determinístico** | O mesmo *commit* passaria hoje e falharia amanhã, sem que nada no repositório mudasse. Isso não é portão, é sorteio |
| **Não haveria evidência anexada** | O Princípio XI pede saída colada. Uma consulta que acontece e some não prova nada depois |

O *lock* (`livro/fontes.lock.json` — arquivo de travamento, em português) resolve os três: é
versionado, é lido offline, é *diffável* em revisão, e carrega a **data** e a **camada** que
resolveram cada entrada. Renová-lo é ato deliberado (`--atualizar`), e o *diff* do renovo é o
que o revisor lê.

O padrão vem de onde já funciona: `verifica-ilha.mjs` degrada declarando quando não há navegador,
e nunca trava o build. Aqui é o mesmo contrato aplicado à rede.

## Arquitetura do portão

```
livro/bibliografia.md  ──parse──▶  entradas {selo, doi, titulo, ano}
                                        │
                                        ├── compara ──▶  livro/fontes.lock.json   (offline, sempre)
                                        │
                                        └── --atualizar ──▶ Crossref ──falhou?──▶ OpenAlex
                                                                  │
                                                                  └──▶ reescreve o lock
```

**Camadas de resolução**, na ordem, seguindo o padrão de verificação em níveis que o guia externo
descreve (ADR 0009):

1. **Crossref** — `api.crossref.org/works/{doi}`. Autoridade sobre o registro DOI.
2. **OpenAlex** — `api.openalex.org/works/doi:{doi}`. Segunda opinião quando o Crossref não
   responde ou não conhece.
3. **Nada resolveu** → a entrada é marcada `nao_resolvido` no *lock*, **com o motivo**, e o
   portão **avisa sem reprovar**. Ausência de índice não é prova de fabricação — é o caso do
   Hoffman, que existe e não está em lugar nenhum.

**Comparação de título:** similaridade normalizada, com limiar **0,70**, o mesmo que o guia
externo documenta. Abaixo do limiar, o portão reprova nomeando os dois títulos lado a lado, para
que a revisão humana decida. Acima, passa. A normalização remove pontuação, acentos, ênfase de
Markdown e caixa — porque o handbook escreve `"New Finite Pivoting **Rules** for the Simplex
Method"` com a ênfase que o texto usa para argumentar.

**Comparação de ano:** exata. Divergência de ano reprova. É o erro de citação mais comum e o mais
barato de pegar.

## O que o portão NÃO faz, e por quê

| Não faz | Por quê |
|---|---|
| Promover selo | A máquina não pode afirmar que um humano leu. `✓ᵐ` é o teto do que um DOI resolvido sustenta (C3 da spec) |
| Reprovar entrada sem DOI | Livro impresso, relatório técnico e página institucional são fontes legítimas. Exigir DOI expulsaria o Lachtermacher e o Arenales da bibliografia |
| Verificar URL comum | Uma varredura de URL no build seria consulta ao vivo com todos os defeitos acima, e um `404` transitório derrubaria o build. Fica declarado como **lacuna** — a próxima defesa contra URL inventada continua sendo humana |
| Ler texto integral | `403` das editoras. Já declarado na spec |

## Estratégia — a ordem importa

1. **O portão primeiro, contra a bibliografia como ela está hoje.** Se ele nascer depois das
   correções, não prova nada: teria sido escrito para passar.
2. **Rodar, ver o que ele acusa**, e só então corrigir o que for defeito real.
3. **Quebrar de propósito**, quatro vezes (A5, A6, A7, rede).
4. **Registro**: legenda de selos, glossário, `ROADMAP`, `HISTORICO`, ADR.

## Mudanças previstas

| Mudança | Por quê |
|---|---|
| `publicar/verifica-fontes.mjs` | O portão |
| `livro/fontes.lock.json` | A evidência versionada |
| `publicar/package.json` | Encadear no `build` e expor `fontes:atualizar` |
| `livro/bibliografia.md` — legenda | Quatro selos em uso, dois declarados (O3) |
| `livro/glossario.md` + mapa de siglas do motor | **CI** nasce nua no plano (Princípio IX) |
| `ROADMAP.md` | Numeração das rodadas (A10) |
| `adr/0009-*.md` | A decisão do *lock* e das camadas |
| `.github/workflows/ci.yml` | Nada a fazer: o portão entra pelo `npm run build`, que a CI já roda |

## Riscos

| Risco | Mitigação |
|---|---|
| **O *parser* da bibliografia é frágil** — Markdown não é formato de dados | O portão falha **alto** quando não entende uma entrada, em vez de ignorá-la em silêncio. Entrada com DOI que o *parser* não casa é erro, não *no-op*. É o defeito clássico do portão que "passa" porque não viu nada |
| Crossref mudar de contrato | O *lock* protege: o build não depende da API. Só `--atualizar` quebraria, e aí quebra na cara de quem pediu |
| O *lock* virar carimbo que ninguém lê | O *diff* é a defesa: renovo é ato explícito e aparece na revisão |
| **Falso verde**: o portão passar sem ter verificado nada | Task própria (T5): o portão **imprime quantas entradas verificou**, e o teste destrutivo A5 prova que ele reprova. Um portão que não sabe dizer quantos itens olhou não é portão |
| Limiar 0,70 aceitar título errado | Aceita mesmo — é limiar de triagem, não de prova. Por isso o ano é **exato**, e por isso a reprovação mostra os dois títulos para leitura humana |

## Desvio declarado

Esta rodada **não produz capítulo**, e portanto não passa pelo esqueleto do Guia Editorial nem
pelo mínimo de exercícios. É rodada de motor, como foi a 001. O `ROADMAP` prevê rodadas assim
implicitamente ("o que prova a máquina"), mas não as nomeia — fica o registro de que **rodada de
motor é raia plena**, não leve, porque mexe no que barra publicação.
