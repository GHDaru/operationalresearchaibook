# Spec 007 — Portão de fontes: o identificador vira medição

**Data:** 2026-08-12 · **Raia:** plena · **Estado:** **aguardando ratificação do autor** (ver
"O que é do autor", ao fim)

> **Correção de honestidade.** A primeira versão desta spec dizia "Estado: aprovada para plano"
> sem nomear quem aprovou. O gate do autor sobre a especificação não é delegável (constituição,
> Governança) e eu não o tinha. A linha estava reivindicando uma aprovação que não existia.

## O problema

O handbook tem um sistema de selos de procedência — `✓`, `✓ᵐ`, `⏳`, `❌` — e ele funciona. É
honesto e é raro.

**Mas nenhum selo é verificado por máquina.** O `✓` ao lado de um identificador de objeto digital
(DOI, *Digital Object Identifier*) é uma afirmação minha. Se eu inventar um DOI, ou trocar um
dígito, ou colar o DOI de outro trabalho, **nada no `npm run build` percebe** — os seis portões
encadeados verificam capítulo, exercício, referência interna, espelho de capacidades e ótimo; o
sétimo, o da ilha, roda fora da cadeia. Nenhum olha a bibliografia.

Isto contradiz o Princípio XI no ponto em que ele mais importa: *prove, não declare*. E não é
risco hipotético. Na rodada 004 uma URL de vídeo **foi inventada** e só foi apanhada por acidente,
ao tentar abri-la — o registro está no `HISTORICO.md`. A defesa contra identificador inventado é,
hoje, o meu cuidado. **Cuidado não é portão.**

Defeito menor e imediato: a **legenda de selos** da bibliografia declara dois selos e o arquivo
usa quatro. O leitor encontra `✓ᵐ` e `❌` sem dicionário.

### A contagem, com o comando que a reproduz

A primeira versão desta spec dizia "44 marcas de pendência em onze arquivos" sem o comando — e o
número **não era reprodutível**: depende de quais diretórios entram, e a spec não declarava
quais. Corrigido:

```bash
grep -rc "⏳" --include="*.md" livro/ radar/ adr/ estudos/ | grep -v ":0"    # 50 marcas
grep -o "doi\.org/10\.[0-9]\{4\}" livro/bibliografia.md | wc -l              # 12 DOIs
```

## Cobertura — o que esta rodada NÃO alcança

Declarado em número, porque o título promete mais do que o portão entrega e essa diferença é
precisamente o tipo de coisa que este handbook não deixa o leitor inferir.

| | |
|---|---|
| Linhas com selo | **36** — `grep -cE "^(✓ᵐ\|✓\|⏳\|❌\|📖) "` |
| Dessas, **atribuições** (afirmação, não obra) | 4 |
| Obras distintas (descontada 1 duplicata) | **31** |
| **Entradas com DOI, que o portão verifica** | **12** |
| **Obras que continuam sendo afirmação humana** | **19** — os livros-base, Hillier, Winston, MacTutor, INFORMS, Blum & Roli, `awesome-ml4co`, o survey de ALNS, Dantzig–Orden–Wolfe, Fourier, Klee & Minty, Hoffman, UFMG, Sarubbi e os identificadores do arXiv |

**Depois desta rodada, 61% da bibliografia continua sem portão.**

> **Este número já esteve errado nesta própria spec**, que publicava "12 de cerca de 25" — 48% —
> sem o comando que o reproduzisse, na mesma página em que exige comando para toda contagem. A
> revisão independente mediu 36 linhas com selo e a estimativa caiu. É o defeito que a rodada foi
> combater, cometido na frase que promete não cometê-lo.

E o mais importante: **o incidente que motiva esta spec — a URL de vídeo inventada — continuaria
passando.** URL comum está fora de escopo (o motivo técnico está no plano). O item "Portão de URL
externa" do `ROADMAP` **permanece aberto**, e é provavelmente mais urgente do que este. Um portão
que cria confiança maior do que sua cobertura é pior do que portão nenhum.

### Também fora de escopo

- **Ler o que está atrás de paywall.** As editoras respondem `403` a acesso automatizado. DOI que
  resolve prova que a referência **existe** e que os metadados batem — não prova que alguém leu.
  O portão **não pode** promover `✓ᵐ` a `✓` ([ADR 0010](../../adr/0010-a-semantica-do-selo.md)).
- **Fechar as pendências históricas de conteúdo** — o nome *simplex* atribuído a Motzkin, a origem
  da letra M, a data de Hoffman. Dependem de leitura humana em acervo, não de interface de
  programação de aplicações (API).

## Objetivos

| # | Objetivo |
|---|---|
| **O1** | Todo DOI da bibliografia **existe no registro**, e o trabalho que ele identifica é o que o handbook declara — título, ano e primeiro autor |
| **O2** | O portão roda **sem tocar a rede** no caminho `build`, de forma determinística |
| **O3** | A legenda declara os cinco selos, com o que cada um prova |
| **O4** | **DOI inventado quebra o build** — inclusive o modo típico, sufixo fabricado sob prefixo verdadeiro — e **DOI deslocado** também |
| **O5** | O verde do portão **significa alguma coisa**: ele não pode passar por não ter verificado nada |

## Critérios de aceite

`M` = verificável por máquina · `H` = gate humano, declarado como tal.

| # | | Critério | Como se verifica |
|---|---|---|---|
| **A1** | M | `verifica-fontes.mjs` roda no `build` **antes de `build.mjs`**, junto dos demais verificadores, e o caminho `SEM_PDF=1` também fica verde | `npm run build` e `SEM_PDF=1 npm run build` |
| **A2** | M | Contagem independente do parser: `grep -o "doi\.org/10\.[0-9]\{4\}" livro/bibliografia.md \| wc -l` = **12** = nº de entradas do travamento. Divergência **reprova** | teste destrutivo |
| **A3** | M | No caminho `build`, o portão **não faz nenhuma chamada de rede** — provado instrumentando o cliente, não desligando a rede | teste com stub que falha se chamado |
| **A4** | H | `npm run fontes` renova o travamento a partir de `doi.org` + Crossref + OpenAlex, com saída e data coladas | caminho manual |
| **A5** | M | DOI na bibliografia e **ausente** do travamento reprova, nomeando o DOI | teste destrutivo |
| **A6** | M | **DOI fabricado** (`10.1287/opre.99.9.9.99999`) reprova | teste destrutivo |
| **A7** | M | **DOI deslocado** — DOI real de outro trabalho — reprova por divergência de **título ou ano** (autor **avisa**, ver ADR 0009 D3) | teste destrutivo |
| **A8** | M | Título divergente **acima do limiar medido** reprova; truncamento de subtítulo **passa** | teste destrutivo |
| **A9** | M | Selo usado e não declarado na legenda reprova | teste destrutivo |
| **A10** | M | Travamento com chave fora da lista fechada, ou campo de texto > 300 caracteres, reprova (Princípio X) | teste destrutivo |
| **A11** | M | Entrada com DOI que o parser **não consegue interpretar** reprova — falha por ignorância é falha, nunca aprovação | teste destrutivo |
| **A12** | M | `npm run fontes` duas vezes produz travamento idêntico a menos da data | comparação de hash |
| **A13** | M | Nenhuma credencial no repositório; o portão roda sem chave de API | `grep` |
| **A14** | M | `python -m pytest -q` do backend verde | saída colada |
| **A15** | M | Glossário e mapa de siglas do motor ganham **CI** (*Continuous Integration*, integração contínua) | `grep` nos dois |
| **A16** | H | `HISTORICO.md` registra a edição, **incluindo** que o buraco de URL continua aberto | leitura |
| **A17** | H | `ROADMAP.md` corrigido: numeração deslocada, `007 🚧` desmarcado, item "Portão de URL externa" **explicitamente ainda aberto** | leitura |
| **A18** | H | **Revisão em contexto fresco** — quem executa não verifica (constituição XI; Maestro II) | relatório anexado |
| **A19** | M | `verificacao.md` traz a saída colada de **todos** os testes destrutivos e a **primeira execução crua** do portão | leitura + presença |
| **A20** | M | Existe reconferência **agendada** do travamento na integração contínua, que falha ou abre issue se divergir | leitura do workflow |

## Clarify

**C1 — O portão deve exigir rede?** **Não.** Build que só passa com rede é build frágil, e o
custo zero é requisito. O travamento versionado é a fonte de verdade; a rede só entra em
`npm run fontes`. Mesmo contrato que `verifica-ilha.mjs` já usa para o navegador: **degradar
declarando**. *Resolvido por mim; é aplicação do Princípio IV, reversível.*

**C2 — Um DOI que não resolve deve reprovar?** **Sim, quando o registro nega a existência.** Esta
era a pergunta que eu havia respondido errado, com um exemplo (Hoffman) que **não tem DOI** e
portanto não a exigia. A consulta ao especialista mostrou que o enquadramento estava errado:
existência é decidida pelo *Handle System*, não por índice de metadados. Ver
[ADR 0009](../../adr/0009-portao-de-fontes-doi-inexistente.md) e
[ADR 0010](../../adr/0010-a-semantica-do-selo.md). *Levada a ADR e **listada para ratificação do
autor**.*

**C3 — O portão pode promover selo?** **Nunca.** [ADR 0010](../../adr/0010-a-semantica-do-selo.md),
D2. *Levada a ADR.*

## O que é do autor, e está esperando

Nada aqui foi publicado; tudo vive na branch, que é reversível.

1. **A semântica do selo** (ADR 0010) governa toda automação futura da bibliografia, não só esta
   rodada.
2. **DOI inexistente reprova, sem allowlist** (ADR 0009, D1). É a decisão que muda o que o
   handbook aceita como fonte.
3. **A numeração**: o `ROADMAP` reservava a 007 para o capítulo 11; sua ordem desloca a Parte II
   em uma unidade.
