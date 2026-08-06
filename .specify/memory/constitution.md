# Constituição — handbook vivo *Pesquisa Operacional*

> Fonte de verdade das convenções deste repositório. Prevalece sobre qualquer outra
> prática. **Todo agente e humano DEVE ler este documento antes de qualquer trabalho.**
> Emendas via Architecture Decision Record (ADR) + bump de versão.
>
> **Versão:** 1.0.0 · **Ratificada:** 2026-08-06
>
> Esta constituição **herda** a metodologia [Maestro](https://github.com/GHDaru/maestro)
> (`docs/governance/principles.md`), cujos oito princípios valem aqui integralmente. Os
> princípios abaixo são os **específicos deste handbook** — o que a metodologia genérica não
> cobre. Em caso de conflito, o Maestro prevalece nas questões de processo; esta constituição
> prevalece nas questões de conteúdo e forma do livro.

---

## Princípios

### I. É um treino, não uma leitura (NÃO-NEGOCIÁVEL)

A unidade de valor não é o capítulo lido — é a habilidade exercitada. **Todo capítulo
numerado tem prática com devolutiva.** Um capítulo que explica bem e não faz o leitor
modelar está **incompleto**, por melhor que esteja escrito.

Consequências verificáveis:

- Mínimo de **3 exercícios** e **1 vídeo** por capítulo numerado.
- Todo exercício rastreia a um objetivo de aprendizagem declarado no próprio capítulo.
- A devolutiva **explica o conceito**; dizer "errado" não é devolutiva.
- A correção mora no **servidor**, nunca no HTML publicado.

### II. Modelar antes de resolver (NÃO-NEGOCIÁVEL)

O erro caro em Pesquisa Operacional (PO) quase nunca é aritmético — é de formulação. Por
isso a ordem de exposição é **intuição → matemática → código**, sempre, e o capítulo começa
pelo **problema que o método resolve**, não pelo método.

Consequências:

1. Nenhuma fórmula aparece antes da intuição que a motiva.
2. Todo método novo é apresentado com **pelo menos um modelo mal formulado** e o que ele
   produz — o erro é material didático, não constrangimento.
3. Todo capítulo de método responde explicitamente: *quando este método não serve?*

### III. Evidência acima de retórica

Afirmação empírica exige **experimento reproduzível** (script + instância + semente +
versão de biblioteca e solver), ou citação verificada, ou não é afirmada.

- **Nenhum número sem procedência.** Nem "cerca de 10× mais rápido", nem "costuma convergir".
- Comparação de algoritmos declara instâncias, *baseline* e critério de parada. Comparação
  sem isso não é resultado, é anedota.
- Nenhuma URL ou identificador de objeto digital (DOI) inventado. Fonte não confirmada é
  marcada `⏳` e não sustenta afirmação.

### IV. A fonte-base é o experimento executável

O handbook nasce de código que roda **em CPU, sem licença paga**. A construção prática
`po-zero` acompanha o livro: uma etapa por capítulo de método. Resultado publicado tem
artefato que o regenera.

Custo zero é **requisito**, não preferência: solver aberto na trilha padrão. Solver comercial
pode aparecer como comparação, nunca como dependência.

### V. Arquitetura em três camadas (NÃO-NEGOCIÁVEL)

O handbook é **núcleo + módulos aplicados + fronteira**, e as três envelhecem em ritmos
diferentes ([Mapa do handbook](../../livro/mapa-do-handbook.md)).

| Camada | Regra que a governa |
|---|---|
| **Núcleo** | Muda por janela de revisão, não por notícia. Tema de fronteira não entra aqui. |
| **Aplicados** | Cresce **por adição**: módulo novo não altera módulo existente. |
| **Fronteira** | **Cláusula de expiração obrigatória** em todo capítulo. |

Um tema sobe de fronteira para núcleo quando resiste a **duas janelas de revisão** sem ser
refutado. A promoção é decisão do autor e vira ADR.

### VI. Atualização científica por Radar, não por boa vontade

Artigo científico entra no livro por um mecanismo, não por lembrança. O **Radar**
(`radar/RADAR.md`) registra cada artigo lido com data, veredito e **o que ele muda no livro**.

- Linha do Radar que altera uma recomendação **dispara revisão** do capítulo afetado, sem
  esperar a janela.
- Artigo citado em capítulo sem passar pelo Radar é dívida a corrigir, não atalho.
- O Radar é datado e append-only: registro não se reescreve.

### VII. Livro vivo: datado, versionado e reescrito

Nenhuma versão é final. Todo capítulo carrega a data de captura no cabeçalho; toda mudança
relevante entra no `livro/HISTORICO.md` com a edição, a data e o modelo de IA usado.

Distinguem-se três datas: a do **evento** (imutável), a da **captura** (quando fotografamos)
e a do **experimento** (quando o número foi medido, com a versão da biblioteca e do solver).

### VIII. Português como fonte canônica; inglês como dívida declarada

O português é a língua-fonte do handbook. O par em inglês é **objetivo declarado, não portão
de entrega** — a prioridade da fase atual é cobrir o corpo de conhecimento.

Regras:

1. Um capítulo é dado por pronto em português. A ausência do par em inglês é **dívida
   registrada** no `HISTORICO.md`, não omissão silenciosa.
2. Quando o par existir, tradução velha **nunca finge ser atual**: a fonte em inglês carrega
   o hash da fonte em português, e o selo de sincronia é visível ao leitor.
3. Termos técnicos consagrados ficam sem tradução forçada (*branch and bound*, *big-M*,
   *solver*, *scheduling*); traduzidos quando a prática já traduziu (restrição, viabilidade,
   dualidade).

Justificativa e alternativas avaliadas: [ADR 0002](../../adr/0002-portugues-primeiro.md).

### IX. Comunicação inteligível (herdado do Maestro, Princípio VIII)

**Lei de Ferro:** em **toda resposta, documento ou artefato**, a **primeira ocorrência** de
uma sigla é escrita por extenso, com a abreviação entre parênteses. A contagem reinicia a
cada documento — o leitor de hoje não tem obrigação de ter lido o de ontem.

Não vale como desculpa: "todo mundo conhece essa sigla" · "eu já expliquei antes" · "é jargão
da área". Jargão órfão é o que produz o amontoado. Termo novo entra também no
`livro/glossario.md`.

### X. Direitos autorais e materiais de terceiros

O texto publicado é **autoral**. Livros-texto e materiais de estudo de terceiros **não são
reproduzidos neste repositório** — nem em trechos longos, nem como arquivo, nem como imagem.

- As obras são citadas por fonte oficial na `livro/bibliografia.md`.
- Materiais de estudo do autor ficam **fora do versionamento** (ver `materiais/README.md`).
- Mapeamento capítulo-a-capítulo com livros-base é **metadado bibliográfico** (autor, obra,
  edição, capítulo, páginas) e pode ser versionado. **Conteúdo, não.**

### XI. Definition of Done verificável — "prove, não declare"

"Pronto" exige evidência anexada. Sem saída colada, não está pronto:

```bash
cd publicar && npm run build                        # site + portões de qualidade
cd chat-companion/backend && python -m pytest -q    # backend do tutor
```

Além disso: histórico atualizado, fontes verificadas, e **revisão por agente em contexto
fresco** — quem executa não verifica (Maestro, Princípio II).

---

## Governança

Esta constituição prevalece. Emendas sobem a versão semântica (MAJOR: remoção ou redefinição;
MINOR: princípio novo ou expansão; PATCH: esclarecimento) e são registradas em ADR.

**Gates humanos inegociáveis:** o autor aprova a especificação, o plano (Constitution Check),
o merge e qualquer publicação. Nenhum deles é delegável a agente.

**Raias de trabalho:**

| Raia | O que é | O que exige |
|---|---|---|
| *leve* | Typo, link quebrado, ajuste de redação | O commit é o artefato |
| *plena* | Capítulo novo, módulo, feature | Especificação completa em `specs/NNN-nome/` |
| *infra* | Deploy, migração, banco | Sempre plena, com gates de reversibilidade |
