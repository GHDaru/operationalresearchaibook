# Constituição — livro vivo *Teoria das Restrições*

> Fonte de verdade das convenções deste repositório. Prevalece sobre qualquer outra
> prática. **Todo agente e humano DEVE ler este documento antes de qualquer trabalho.**
> Emendas via ADR + bump de versão.
>
> **Versão:** 1.1.0 · **Ratificada:** 2026-08-01
>
> Esta constituição **herda** a metodologia [Maestro](https://github.com/GHDaru/maestro)
> (`docs/governance/principios-maestro.md`), cujos sete princípios valem aqui integralmente.
> Os princípios abaixo são os **específicos deste livro** — o que a metodologia genérica não
> cobre. Em caso de conflito, o Maestro prevalece nas questões de processo; esta
> constituição prevalece nas questões de conteúdo e forma do livro.

---

## Princípios

### I. É um treino, não uma leitura (NÃO-NEGOCIÁVEL)

A unidade de valor deste livro não é o capítulo lido — é a habilidade exercitada. **Todo
capítulo numerado tem prática com devolutiva**, e um capítulo que explica bem sem fazer o
leitor praticar está **incompleto**, por melhor que esteja escrito.

Consequências verificáveis:

- Todo capítulo numerado tem seção de prática e seção "Mão na massa" (aplicação ao contexto
  do próprio leitor).
- A devolutiva **explica o porquê**; dizer "errado" não é devolutiva.
- O erro é barato e repetível: o leitor pode errar sem custo e refazer.

### II. Bilíngue por padrão — PT e EN (NÃO-NEGOCIÁVEL)

**O livro existe sempre em português e em inglês.** O português é a fonte canônica; o inglês
é artefato derivado, e nenhum dos dois é opcional.

Regras:

1. **Nenhum capítulo é dado por pronto sem o par EN.** Publicar conteúdo só em PT é dívida,
   não entrega.
2. **Tradução velha nunca finge ser atual.** Cada fonte EN carrega o hash da fonte PT que
   traduziu; o motor compara e exibe o selo de sincronia (em dia / atrasado). Selo atrasado é
   visível ao leitor, com o aviso de que o conteúdo mais recente está na versão PT.
3. **Sincronia é parte da Definition of Done.** Uma rodada que altera conteúdo PT e não
   atualiza o EN correspondente não fecha — ou atualiza, ou registra explicitamente a
   defasagem no `HISTORICO.md` com prazo.
4. Os objetos interativos e o tutor seguem a mesma regra: textos de interface e devolutivas
   existem nos dois idiomas.

### III. Conteúdo autoral, com fonte oficial rastreável

O texto publicado é **autoral**. Materiais de estudo de terceiros não são reproduzidos —
ficam em repositório privado. Toda afirmação sobre um conceito da Teoria das Restrições é
rastreável a uma obra na bibliografia, citada na primeira ocorrência. Formulação autoral é
sinalizada como tal.

### IV. Livro vivo: datado, versionado e reescrito

Nenhuma versão é final. Todo capítulo carrega a data da última revisão; toda mudança
relevante entra no `HISTORICO.md` com a edição, a data e o modelo de IA usado. Conteúdo
sem data é conteúdo sem prazo de validade declarado — e portanto não publicável.

### V. O tutor treina, não substitui o raciocínio (NÃO-NEGOCIÁVEL)

O tutor de IA conduz por perguntas e **nunca resolve o exercício do leitor**, mesmo sob
insistência. Responde direto apenas o que é consulta (definição, referência, localização no
texto); tudo que é conceitual ou é trabalho do leitor recebe dica em camadas.

Esta regra não é preferência de estilo: a evidência disponível indica que um assistente que
entrega a resposta pronta **piora** a aprendizagem, enquanto um tutor com scaffolding a
melhora substancialmente. O guardrail é o que separa os dois casos.

O tutor também respeita a **trilha progressiva**: no modo progressivo, só oferece o que o
livro já ensinou até o capítulo em que o leitor está, e explica de qual capítulo vem o que
ainda não foi liberado.

### VI. O processo é o Maestro, e ele comanda (NÃO-NEGOCIÁVEL)

A metodologia [Maestro](https://github.com/GHDaru/maestro) não é referência de consulta:
é a **regra vigente** deste repositório, e está **instalada** aqui.

1. **Skills instaladas comandam, não sugerem.** As skills do Maestro vivem em
   `.claude/skills/` e cada uma carrega sua *Iron Law*. Antes de agir, verifique se
   alguma se aplica; havendo chance razoável, **siga-a**:

   | Skill | Quando dispara |
   |---|---|
   | `constitution-check` | ao escrever ou revisar um `plan.md` |
   | `dod-verificavel` | ao escrever critérios de aceite (transforma julgamento em check) |
   | `diagnostico-antes-do-fix` | **SEMPRE** antes de propor correção de qualquer bug |
   | `combater-amontoado` | ao revisar texto denso |
   | `anti-padroes` | ao desenhar fluxo ou revisar trabalho de agente |

   Os comandos (`.claude/commands/`) e os agentes (`.claude/agents/`) do Maestro
   acompanham as skills.

2. **Uma spec por rodada, uma branch por rodada.** Registro em `specs/NNN-nome/`.
   Mudança de escopo volta à spec antes de virar conteúdo ou código.

3. **Raias proporcionais ao risco:** *leve* (typo, link — o commit é o artefato),
   *plena* (capítulo, feature — spec completa), *infra* (deploy, banco, migração —
   sempre plena, com gates de reversibilidade).

4. **Gates humanos inegociáveis:** o autor aprova a spec, o plan, o merge e qualquer
   deploy. Nenhum é delegável a agente.

5. **Quem executa não verifica.** A revisão final passa por agente em contexto fresco.

6. **Prove, não declare.** "Pronto" exige evidência anexada — saída de build, de teste,
   captura de tela. Afirmar que funciona não é evidência.

**Sincronia.** As skills são cópia do repositório do Maestro. Quando ele evoluir,
ressincronize com `scripts/sync-maestro.sh` — divergência silenciosa entre a regra
publicada e a instalada é o pior dos dois mundos. O modo `--check` do mesmo script
transforma isso em portão: ele acusa divergência e sai com erro.

### VII. Estrutura declarativa e crescimento por adição

O livro cresce editando o sumário e criando o arquivo — nunca alterando o motor. Módulos são
fronteiras: um módulo novo não deve exigir mudança nos existentes. Objetos interativos são
ilhas isoladas, com *progressive enhancement* obrigatório (sem JavaScript, o conteúdo
estático permanece legível).

### VIII. Acessibilidade e custo zero na trilha padrão

O livro é lido de graça, sem cadastro. O tutor opera com endpoint gratuito, com opção de
chave própria (BYOK) para quem quiser mais qualidade. Nenhum segredo em arquivo, commit ou
texto — credenciais só em `.env` fora do versionamento.

---

## Portões de qualidade (verificáveis)

Uma rodada não fecha sem **evidência anexada** ("prove, não declare"):

| Portão | Comando | O que garante |
|---|---|---|
| Build do site | `cd publicar && npm run build` | Markdown válido, links internos íntegros, sumário completo |
| Template por página | incluso no build | Hero, numeração, tempo de leitura, downloads e datação em cada capítulo |
| Sincronia PT↔EN | incluso no build (passada EN) | Princípio II: nenhuma tradução defasada sem selo |
| Testes do tutor | `cd chat-companion/backend && python -m pytest -q` | Gating por módulo e contratos das rotas |

## Governança

Esta constituição prevalece neste repositório. Emendas sobem versão semântica (MAJOR:
remoção ou redefinição de princípio; MINOR: princípio novo ou expansão; PATCH: clarificação)
e são registradas em ADR.

O processo está no Princípio VI e nas skills instaladas em `.claude/skills/`.

**Histórico:** 1.0.0 (2026-08-01) — fundação, com o princípio bilíngue (II) ratificado na
Rodada 3 · 1.1.0 (2026-08-01) — o Maestro vira princípio próprio (VI), com as skills
instaladas declaradas como regra que comanda; renumeração dos princípios seguintes.
