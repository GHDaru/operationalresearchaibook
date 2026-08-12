# ADR 0010 — A semântica do selo: o que cada um prova, e quem pode escrevê-lo

**Data:** 2026-08-12 · **Status:** aceito na branch, **pendente de ratificação do autor no gate
de merge** · **Rodada:** 007

## Contexto

A bibliografia do handbook usa um sistema de selos de procedência. Ele funciona, e é raro:
diz, item a item, o que foi lido e o que não foi. Mas nunca foi **definido** em lugar durável.

Dois sintomas do vazio:

1. **A legenda mente por omissão.** `livro/bibliografia.md` declara dois selos (`✓` e `⏳`) e usa
   quatro (`✓`, `✓ᵐ`, `⏳`, `❌`). O leitor encontra `✓ᵐ` sem dicionário.
2. **A rodada 007 automatiza a verificação** e, ao fazê-lo, precisa responder perguntas que nunca
   foram respondidas: uma máquina pode escrever selo? Um identificador que não resolve significa
   o quê? Sem definição, cada rodada responderia de um jeito.

O guardião do processo apontou que essas respostas **sobrevivem à rodada** e valem para toda
automação futura — e que enterrá-las numa spec de rodada é enterrá-las, porque ninguém relê spec
de rodada em 2027.

## Decisão

### D1 — Os cinco selos, definidos pelo que **provam**

| Selo | Nome | O que prova | O que **não** prova |
|---|---|---|---|
| `✓` | verificada | **Um humano abriu a fonte e leu** o trecho que sustenta a afirmação | — |
| `✓ᵐ` | metadados | O registro **existe** e autor, título, ano e veículo conferem | Nada sobre o conteúdo |
| `⏳` | atribuição corrente | A afirmação circula na literatura e **não foi confirmada na fonte** | **Não sustenta afirmação no texto** |
| `❌` | sem fonte | Foi procurado e **não foi encontrado** | — |
| `📖` | leitura editorial | Interpretação **autoral** declarada como tal, não atribuída a terceiro | — |

A distinção que carrega o sistema é entre `✓` e `✓ᵐ`: **existir não é dizer.** Metadados
conferidos provam que a obra existe e é aquela; não provam uma linha do que ela afirma.

### D2 — A máquina **verifica** selo. Só o humano **atribui** selo.

Nenhum portão, agente ou script escreve, promove ou rebaixa selo em `bibliografia.md`. O portão
de fontes é somente leitura, e o travamento `livro/fontes.lock.json` **não tem campo de selo**,
para que a promoção não seja sequer expressável.

A razão é direta: resolver um identificador prova existência e metadados, que é **exatamente** o
significado de `✓ᵐ`. Deixar a máquina escrever `✓` seria a máquina afirmando que um humano leu —
a única afirmação que ela nunca pode fazer.

**Corolário operacional:** o teto do que qualquer automação pode sustentar é `✓ᵐ`. Uma entrada só
sobe a `✓` pela mão de quem leu, e o *commit* que a sobe é a evidência.

### D3 — Identificador que **não existe no registro** é defeito, não pendência

`⏳` significa *"a afirmação circula e eu não confirmei"*. Um identificador que o registro nega
não é afirmação não confirmada: é **afirmação falsa com aparência de verificável** — a categoria
mais cara deste handbook, porque é convincente.

Conduta: o portão **reprova**, e o reparo é **remover o identificador**, mantendo a obra com o
localizador que ela de fato tem. Não há allowlist. O detalhamento técnico e as alternativas
rejeitadas estão no [ADR 0009](0009-portao-de-fontes-doi-inexistente.md).

**Ausência de índice é outra coisa.** Obra real cujo identificador existe mas que nenhum índice
gratuito conhece é **estado normal e aprovável** — literatura cinzenta, relatório técnico, obra
pré-digital. O caso vivo é o Hoffman, *NBS Report* 2974, 1953, que **não tem identificador** e
por isso sequer entra no alcance do portão. Entrada sem identificador é entrada legítima.

### D4 — Entrada sem identificador não é entrada de segunda classe

Livro impresso, página institucional, curso gravado, relatório técnico. Exigir identificador
expulsaria da bibliografia os dois livros-base do curso. O portão as ignora; a procedência delas
continua sendo humana, e o selo diz qual é.

## Alternativas avaliadas

**A máquina promover `⏳` → `✓ᵐ` automaticamente.** *Rejeitada.* Seria conveniente e é o erro
central: o selo deixaria de registrar o que **alguém** verificou e passaria a registrar o que a
API respondeu naquele dia. O selo é declaração editorial, não estado de cache.

**Um só selo de "verificado", sem distinguir leitura de metadados.** *Rejeitada.* É a distinção
mais útil que o sistema tem. Colapsá-la produziria exatamente a falsa confiança que o handbook
combate — e o `✓ᵐ` do Bland, cujo enunciado exato continua não lido, viraria mentira.

**Definir isto na constituição, e não em ADR.** *Considerada, e adiada.* O sistema de selos é
consequência do Princípio III, não princípio novo. Se sobreviver a mais três rodadas sem emenda,
vira candidato a texto constitucional — e este ADR é o rascunho dessa emenda.

## Consequências

- A legenda da bibliografia passa a declarar os cinco selos (rodada 007).
- Automação futura tem um teto explícito: `✓ᵐ`. Nenhuma rodada precisa redecidir.
- **Custo assumido:** o `✓` permanece não verificável por máquina, para sempre e por desenho. A
  defesa contra `✓` indevido é revisão humana e o *diff* — e isso está declarado, em vez de
  disfarçado por um portão que fingiria cobri-lo.

---

## Anexo — duas regras de processo que esta rodada fixou

Registradas aqui por não terem lugar mais durável, e apontadas pelo guardião como impróprias para
viver numa spec de rodada.

**R1 — Rodada de motor é raia plena, não leve.** A tabela de raias da constituição classifica por
tipo de artefato; uma rodada que não produz capítulo pareceria "leve". Não é: mexe no que **barra
publicação**. Rodada que altera portão, motor ou aparato de verificação exige especificação
completa.

**R2 — A numeração das rodadas é sequencial em `specs/`; o `ROADMAP` é ordem de ataque, não
contrato.** Quando o autor insere uma rodada fora da ordem prevista, o `ROADMAP` é corrigido e
nada mais precisa acontecer. O número da pasta é o identificador; a tabela do `ROADMAP` é
intenção, e intenção pode mudar.
