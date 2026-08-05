# Spec 001 — Clonar o motor do livro vivo e propor a primeira versão de conteúdo

> **Raia:** plena (feature + infra) · **Rodada:** 2 · **Branch:** `001-clone-motor-livro`
> **Apetite:** uma rodada · **Autor da decisão:** Gilsiley Darú
> **Status:** aguardando gate humano (aprovação da spec e do merge)

## Intenção

Encurtar o caminho para a primeira versão do livro vivo de Teoria das Restrições
**reaproveitando integralmente a máquina já validada** do livro *Engenharia de
Harness* (motor de publicação, tema, chat companion, CI de Pages) e **trocando o
conteúdo**. O livro nasce funcionando; o conteúdo evolui em rodadas seguintes, com
editoração humana.

## Por quê

O estudo da Rodada 1 (`estudos/001-estudo-educacional-e-roadmap.md`) mostrou que:

- O motor do harness é **conteúdo-agnóstico** e MIT: markdown → HTML + PDF, sumário
  declarativo em JSON, tema próprio, chat com RAG e gating por capítulo, CI de Pages.
- Construir do zero repetiria trabalho já feito e validado em produção.
- O gating de capacidades por capítulo é exatamente a mecânica de **trilha
  pedagógica progressiva** que o curso precisa.

Clonar primeiro e trocar conteúdo depois transforma as Fases 0–3 do roadmap em uma
única rodada, e antecipa o feedback: o autor vê o livro no ar antes de escrever.

## Escopo

### Entra

1. **Motor de publicação** (`publicar/`): `build.mjs`, `pdf.mjs`, `grafo.mjs`,
   `verifica-capitulos.mjs`, tema (CSS/JS/assets), ilhas de visualização (`viz/`).
2. **Chat companion** (`chat-companion/`): backend FastAPI completo, com o registro
   de capacidades reescrito para a trilha de TOC.
3. **CI de publicação** (`.github/workflows/publicar.yml`), sem as etapas
   específicas do harness.
4. **Identidade do livro**: título, subtítulo, URLs, créditos, capa, trilha da
   página de entrada.
5. **Estrutura modular do livro** — sumário declarativo com módulos, desenhado para
   crescer por adição (decisão da Rodada 1: livro evolutivo em módulos).
6. **Primeira versão de conteúdo** — autoral, com **fundamentos lógicos primeiro**,
   para moderação do autor.
7. **Ao menos um objeto interativo** funcionando, provando a mecânica das ilhas
   (decisão da Rodada 1: objetos interativos com o usuário).
8. **Governança**: `CLAUDE.md` apontando ao processo Maestro; estrutura de `specs/`
   e `adr/`.

### Não entra (rodadas futuras)

- Deploy real do backend (Railway) e do banco (Neon) — exige credenciais do autor.
- Decisão final Vercel × GitHub Pages (ADR próprio; v1 sai em Pages, que já vem no CI).
- Versão em inglês (o motor suporta; v1 é PT-only).
- Loop pedagógico (nota/feedback/reforço), identidade de aluno e monitoramento por
  IA — Fases 4 e 5 do roadmap.
- Conteúdo definitivo: esta rodada entrega a **primeira proposição**, não o texto final.

## Critérios de aceite (testáveis)

| # | Critério | Como verificar |
|---|---|---|
| CA-1 | O site é gerado sem erro a partir do Markdown | `npm run build` em `publicar/` sai com código 0 |
| CA-2 | O portão de qualidade por página passa | `verifica-capitulos.mjs` sai com código 0 |
| CA-3 | Nenhuma página gerada menciona "harness" como tema do livro | busca por `harness` no `docs/` gerado retorna apenas ocorrências legítimas (nenhuma) |
| CA-4 | Todo item do sumário tem arquivo correspondente | build falha se faltar arquivo (comportamento do motor) |
| CA-5 | O objeto interativo monta e responde | ilha `data-viz` presente no HTML gerado e `viz.js` compilado |
| CA-6 | O chat companion sobe e passa nos testes | `python -m pytest` em `chat-companion/backend` verde |
| CA-7 | As capacidades do chat refletem a trilha de TOC | `capabilities.py` sem capacidade de harness; espelho em `build.mjs` idêntico |
| CA-8 | O conteúdo é autoral e referenciado | cada afirmação de método TOC cita fonte oficial na bibliografia |

## Restrições

- **Direitos autorais** (decisão da Rodada 1): o texto publicado é autoral; materiais
  de terceiros ficam no repositório privado `tocmaterials`; obras são citadas por
  fonte oficial (autor, título, editora).
- **Custo zero** na trilha padrão: o chat mantém endpoint gratuito + BYOK.
- **Sem segredos** em arquivo ou commit.
- **Português** com termos técnicos consagrados sem tradução forçada.

## Riscos

| Risco | Mitigação |
|---|---|
| Motor traz acoplamento invisível ao harness | Build + verificação como portão; varredura por menções |
| Conteúdo de v1 divergir da visão do autor | É explicitamente uma **proposição para moderação**, não texto final |
| Estrutura modular não acomodar material futuro | Sumário declarativo por módulos; adicionar é editar JSON + criar arquivo |

## Rastreabilidade

Rodada 1 (`estudos/001`, `estudos/002`) → esta spec → `plan.md` → `tasks.md` →
implementação → gate humano de merge.
