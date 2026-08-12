# Spec 007 — O selo vira medição

**Data:** 2026-08-12 · **Raia:** plena · **Estado:** aprovada para plano

## O problema

O handbook tem um sistema de selos de procedência — `✓`, `✓ᵐ`, `⏳`, `❌` — e ele funciona: 44
marcas de pendência espalhadas por onze arquivos dizem, item a item, o que ainda não foi
confirmado. É honesto e é raro.

**Mas nenhum selo é verificado por máquina.** O `✓` ao lado de um DOI é uma afirmação minha. Se
eu inventar um DOI, ou trocar um dígito, ou confundir o volume, **nada no `npm run build`
percebe** — os sete portões existentes verificam capítulo, exercício, referência interna,
espelho de capacidades, ótimo e ilha. Nenhum olha para a bibliografia.

Isto contradiz o Princípio XI no ponto exato em que ele mais importa: *prove, não declare*. E não
é risco hipotético. Na rodada 004 uma URL de vídeo **foi inventada** e só foi apanhada por
acidente, ao tentar abri-la — o registro está no `HISTORICO.md`. A defesa contra DOI inventado é,
hoje, o meu cuidado. Cuidado não é portão.

Há ainda um defeito menor e imediato: a **legenda de selos** da bibliografia (linhas 11–14)
declara só `✓` e `⏳`, enquanto o arquivo usa quatro selos. O leitor encontra `✓ᵐ` e `❌` sem
dicionário.

## O que esta rodada faz

Transforma o selo de **afirmação** em **medição**, com o mesmo padrão que o handbook aplica a
tudo o mais: um portão que roda no `npm run build` e barra o que não se sustenta.

### Fora de escopo, declarado

- **Ler o que está atrás de paywall.** As editoras respondem `403` a acesso automatizado. Um DOI
  que resolve prova que a referência **existe** e que os metadados batem — não prova que alguém
  leu o texto. O selo `✓ᵐ` continua significando exatamente isso, e o portão **não** pode
  promovê-lo a `✓`.
- **Verificar URL que não seja DOI.** Vídeos, páginas do INFORMS e do MacTutor ficam de fora
  desta rodada. O motivo é técnico e é dito no plano.
- **Fechar as pendências históricas de conteúdo** — a atribuição do nome *simplex* a Motzkin, a
  origem da letra M, a data de Hoffman. Essas dependem de leitura humana em acervo, não de API.

## Objetivos

| # | Objetivo |
|---|---|
| **O1** | Todo DOI citado na bibliografia resolve, e o título e o ano que o handbook declara batem com o que o registro público devolve |
| **O2** | O portão roda **sem rede** de forma determinística, e não trava o build quando a rede falha |
| **O3** | A legenda de selos declara os quatro selos que o arquivo de fato usa |
| **O4** | Um DOI inventado, ou um ano trocado, **quebra o build** — e isso é demonstrado quebrando-o de propósito |

## Critérios de aceite

Verificáveis por máquina, salvo onde declarado.

| # | Critério | Como se verifica |
|---|---|---|
| **A1** | Existe `publicar/verifica-fontes.mjs`, encadeado no script `build` do `package.json` | `grep verifica-fontes publicar/package.json` |
| **A2** | Existe `livro/fontes.lock.json` com, para cada DOI da bibliografia, os metadados resolvidos, a fonte que resolveu e a data da resolução | o arquivo existe e tem uma entrada por DOI |
| **A3** | Rodar o portão **sem rede** compara a bibliografia contra o *lock* e passa | `npm run build` com a rede indisponível termina verde |
| **A4** | Rodar `node verifica-fontes.mjs --atualizar` renova o *lock* a partir de Crossref, com OpenAlex como segunda camada | a data no *lock* muda; o campo de origem diz qual camada respondeu |
| **A5** | DOI presente na bibliografia e **ausente** do *lock* falha o portão com mensagem que nomeia o DOI | teste destrutivo |
| **A6** | Título divergente entre bibliografia e *lock*, acima do limiar, falha o portão | teste destrutivo |
| **A7** | A legenda de selos da bibliografia lista `✓`, `✓ᵐ`, `⏳` e `❌`, e o portão barra o uso de selo não declarado na legenda | teste destrutivo |
| **A8** | Nenhuma credencial no repositório; o portão funciona sem chave de API | `grep` por chave; o portão roda numa árvore limpa |
| **A9** | `specs/007-atribuicoes-pendentes/verificacao.md` traz a saída colada dos testes destrutivos | leitura |
| **A10** | O `ROADMAP.md` fica coerente com a numeração real das rodadas | leitura |

## Perguntas de clarify

Três, e as três têm resposta defensável sem o autor — ficam registradas com a decisão tomada e o
motivo, para ele reverter se discordar.

**C1 — O portão deve exigir rede?**
**Não.** Um build que só passa com rede é um build frágil, e o handbook declara custo zero e
reprodutibilidade como requisito. O *lock* versionado é a fonte de verdade do portão; a rede só
entra quando alguém pede `--atualizar`. Isto segue o mesmo padrão que o `verifica-ilha.mjs` já
usa para o navegador: **degradar declarando**, nunca travar em silêncio.

**C2 — Um DOI que não resolve deve reprovar a referência?**
**Não automaticamente.** O guia externo que li nesta sessão formula bem: *ausência de índice não
é prova de fabricação* — o registro pode existir e não estar indexado (literatura cinzenta,
relatório técnico, obra antiga). O caso vivo é o **Hoffman, NBS Report 2974, 1953**, que não
aparece nem no Crossref nem no OpenAlex e **existe**. Conduta: entrada sem DOI é legítima e o
portão a ignora; entrada **com** DOI tem de resolver, porque aí o handbook afirmou um
identificador.

**C3 — O portão pode promover selo sozinho?**
**Não, nunca.** Resolver um DOI prova existência e metadados — é exatamente o significado de
`✓ᵐ`. Deixar a máquina escrever `✓` seria a máquina afirmando que um humano leu. O portão
**verifica** selo; quem **atribui** selo é quem leu.

## O conflito de numeração, e como foi resolvido

O `ROADMAP.md` reserva a **rodada 007 para o capítulo 11**. O autor, nesta sessão, mandou a 007
ser esta — o fechamento das atribuições — e o capítulo 11 virar a 008.

A decisão é do autor e está tomada. A consequência é mecânica: a tabela da Parte II desloca em
uma unidade a partir daqui, e o `ROADMAP.md` é corrigido nesta rodada (**A10**). Fica o registro
de que a numeração das rodadas é **sequencial na pasta `specs/`**, e não uma promessa do
`ROADMAP` — que é ordem de ataque, não contrato.

## Por que agora, e não depois

Porque o custo cresce. Cada rodada de capítulo acrescenta referências, e cada referência
acrescentada sem portão é uma afirmação que ninguém mais vai reconferir. São 25 entradas hoje.
São 77 vagas no mapa. O portão entra enquanto a bibliografia ainda cabe numa leitura.
