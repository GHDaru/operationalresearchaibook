# Anexo D — Ativos TOC existentes (livebook + TOC-Builders + skills)

> Relatório de agente de pesquisa, 2026-07-31.

## 1. `theoryofconstraintlivebook` — VAZIO

Zero commits, zero refs no remoto. Este repositório é a folha em branco criada para receber o material educacional — não um livro em andamento.

### Molde disponível: `harness_engineering` (mesmo autor, padrão "livebook" maduro)

| Componente | Path |
|---|---|
| Capítulos (PT) | `harness_engineering/livro/capitulos/` (16 capítulos) |
| Guia editorial | `livro/GUIA-EDITORIAL.md` |
| Versão EN | `livro/en/` |
| Infra de publicação | `publicar/build.mjs`, `pdf.mjs`, `grafo.mjs`, `sumario.json`, `tema/` |
| Chat companion (RAG) | `chat-companion/backend/` |
| Método spec-driven | `specs/` (69 specs), `.specify/`, `CLAUDE.md` |

Formato: markdown → HTML + PDF, sumário JSON, tema CSS, chat RAG. Diretamente clonável. Conteúdo TOC dentro do harness: praticamente nulo (só a bio do autor — mestrado UFPR com dissertação sobre sequenciamento de produção baseado em TOC).

## 2. Os quatro TOC-Builder — mesma app em gerações sucessivas

Linhagem: React 18 + TS + Vite + Gemini 2.5 Flash + canvas (`@xyflow/react`), sem backend real (mocks em memória/localStorage). Todos compartilham `api_specifications.md` (spec de 5 APIs — Projects, AI Service, Auth, Users, System Prompts — **nunca implementada**).

- **`TOC-Builder` (v1)**: protótipo. ARA canvas, chat panel, validação de UDE, esqueleto de S&T. `NodeType` mais rico: `EI`, `CAUSA`, `MULETA` — distinção didática perdida nas versões seguintes, vale resgatar no curso.
- **`TOC-Builder-APP`**: intermediária. Edição de arestas, markdown nos nós, zonas. Pouco a reaproveitar.
- **`TOC-Builder-V2`**: primeira completa. **Nuvem que Evapora** completa (ConflictCloudView, AssumptionSolutionModal), i18n PT/EN.
- **`tocbuilderv3`**: **o mais maduro — usar este.** Superconjunto do V2 + LandingPage, DocsView (docs didáticos navegáveis), EntitiesPanel, histórico de chat por projeto, `APLICATION_PURPOSE.md`. Docker incompleto (Dockerfile/nginx.conf/entrypoint vazios, 0 bytes).

### O tesouro: ativos reaproveitáveis

**a) Prompts-especialistas em `tocbuilderv3/constants.ts` (23 KB, em português):**
- `VALIDATE_UDE_DETAILED_PROMPT_TEXT` (linhas 109-240): rubrica completa de UDE — definição formal, **11 características de um UDE bem articulado**, "lacuna" vs. "dificuldade em fechar a lacuna", 6 eixos de validação, exemplos bons e ruins. **Praticamente um capítulo de curso pronto.**
- `CONFLICT_CLOUD_PROMPT_TEXT` (264-338): Nuvem que Evapora com regras estruturais, premissas nas 6 conexões, **integração com TRIZ** (5 princípios de separação: espaço, tempo, partes, grau, condição).
- `SYSTEM_PROMPT_ARA_ASSISTANT_TEXT`, `SUGGEST_EIS_PROMPT_TEXT`, `SUGGEST_CAUSES_FOR_EI_PROMPT_TEXT`, `SUGGEST_RELATIONS_PROMPT_TEXT`, `ANALYZE_TREE_PROMPT_TEXT` — catálogo editável (`INITIAL_SYSTEM_PROMPTS`, admin em `PromptAdminView.tsx`).

**b) Texto didático em `tocbuilderv3/locales/pt.ts:426-470`** — 4 tópicos em markdown (Introdução, ARA, Nuvem de Conflito, Interação com a IA), com "Funcionalidades", "Como Funciona", "Dicas de Uso". Equivalente EN.

**c) Modelo de dados TOC** em `tocbuilderv3/types.ts` — `ConflictCloudData` com 5 entidades (A/B/C/D/D') e 7 premissas nomeadas, cada uma com `assumption` + `solution` (injeção). Esquema canônico para exercícios.

**d) Specs em português** — `specs/feat_conflict_cloud.md`, `feat_direct_ara_flow.md` etc.

**e) Skills já instaladas** (mais rigorosas metodologicamente que o app):
- `toc-evaporating-cloud` — nuvem + premissas + soluções, HTML interativo, TRIZ.
- `toc-prt` + `references/prt-methodology.md` — PRT em 8 fases com regras de qualidade.
- `gerar-aula` — aulas HTML com questionário integrado (ponte conteúdo → formato curso).

## 3. Sobreposições e lacunas

**Sobreposições:** Nuvem que Evapora aparece 3× (app, skill, specs — a skill é a mais rigorosa, o app o mais visual; consolidar verbalização canônica). Validação de UDE 2×. Os 4 builders são a mesma app — tratar v3 como único vivo.

**Conteúdo TOC já escrito:** UDE (alta profundidade), Nuvem/EC (alta), PRT (alta, só na skill), ARA (média), premissas/injeções (média-alta), TRIZ (média), IA como copiloto TOC (média).

**Lacunas — não existe em lugar nenhum:**
1. O livro em si — zero capítulos.
2. **5 Passos de Focalização** — o núcleo da TOC.
3. **Throughput / Inventário / Despesa Operacional** (contabilidade de ganhos).
4. **DBR (Tambor-Pulmão-Corda), CCPM** — justamente a expertise do autor.
5. **ARF, Árvore de Transição** — só strings de enum, nenhuma implementação/texto.
6. **S&T** — parcialmente codada, desabilitada por padrão, sem texto.
7. **CLR (Categorias de Reserva Legítima)** — ausente.
8. **Camadas de Resistência** — ausente.
9. **Aparato pedagógico** — nenhum exercício, quiz, estudo de caso ou trilha (o que há é doc de produto, não didática).
10. **Backend real / persistência / auth** — tudo mock.

## Caminho mais curto sugerido

Clonar a estrutura do `harness_engineering` (livro + build + chat-companion) para o livebook vazio; semear capítulos de UDE, ARA e Nuvem extraindo `constants.ts` e `locales/pt.ts`; importar a metodologia PRT da skill; escrever do zero 5 Passos, T/I/DO, DBR/CCPM, ARF/AT e CLR; ligar `tocbuilderv3` como laboratório prático (dando-lhe antes um backend real — o `api_specifications.md` está pronto).
