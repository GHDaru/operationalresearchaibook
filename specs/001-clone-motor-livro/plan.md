# Plan 001 — Clonar o motor do livro vivo

> Como implementar a spec `001-clone-motor-livro`. Raia plena.

## Constitution Check (princípios do Maestro)

| Princípio | Conformidade | Nota |
|---|---|---|
| **I. Spec-Driven** | ✅ | `spec.md` escrita e aprovada antes do código; mudança de escopo volta à spec |
| **II. Orquestração humano-governada** | ✅ | Gates humanos preservados: aprovação da spec, do plan e do merge. Agente executa; autor decide |
| **III. Reversibilidade e gates proporcionais** | ✅ | Trabalho em branch isolada; nenhuma ação destrutiva; deploy (irreversível) **fora de escopo** — fica para rodada com gate próprio |
| **IV. Test-First e DoD verificável** | ✅ | Os portões já existem no motor: `npm run build`, `verifica-capitulos.mjs`, `pytest` do chat. "Prove, não declare" = anexar a saída |
| **V. Economia de contexto e corte por fronteira** | ✅ | Módulos do livro = fronteiras; sumário declarativo isola conteúdo de motor |
| **VI. Artefatos vivos e rastreabilidade** | ✅ | spec ↔ commits ↔ build verde; `HISTORICO.md` do livro registra a edição |
| **VII. Governança leve (YAGNI)** | ✅ | O núcleo da decisão: **reusar em vez de construir**. Não se adota nada especulativo (EN, deploy, loop pedagógico ficam fora) |

**Violações:** nenhuma. **Justificativas necessárias:** nenhuma.

## Decisões de implementação

### D1 — Copiar o motor inteiro, adaptar por configuração
Copiar `publicar/` e `chat-companion/` sem poda inicial; adaptar os pontos de
identidade (strings, URLs, sumário, capacidades). O que for exclusivo do harness
(diagrama, componentes de benchmark) é removido, não reescrito.

### D2 — PT-only na v1
O motor é bilíngue, mas manter EN sem tradução gera site quebrado. A v1 constrói só
PT; a máquina EN permanece intacta para quando houver tradução. *Alternativa
descartada:* EN com conteúdo PT (site incoerente).

### D3 — Ilhas de visualização como mecanismo dos objetos interativos
O motor já compila ilhas React (`<div data-viz="...">` + esbuild). É exatamente o
mecanismo pedido para objetos interativos — reusar em vez de introduzir framework.
*Alternativa descartada:* SPA no front (contradiz o site estático e o YAGNI).

### D4 — Estrutura modular por partes do sumário
Cada módulo é uma `parte` do `sumario.json`. Crescer = adicionar item + arquivo.
Nenhuma mudança de motor é necessária para o livro evoluir.

### D5 — Gating do chat espelha os módulos
`capabilities.py` reescrito: cada capacidade libera no capítulo do módulo que a
ensina. É a trilha pedagógica progressiva com a mecânica que já existe.

### D6 — Conteúdo v1: fundamentos lógicos com profundidade, resto estruturado
A prioridade declarada é exercitar a lógica primeiro. Os capítulos de fundamentos
lógicos saem com conteúdo substantivo; os módulos seguintes saem com estrutura,
objetivos e esqueleto — para o autor moderar e o material do `tocmaterials`
preencher.

## ADRs a registrar

- **ADR 0001** — Reuso do motor do livro de harness (esta decisão).
- **ADR 0002** — Front: GitHub Pages na v1; Vercel reavaliado quando os objetos
  interativos pedirem SSR. *(a registrar quando houver a necessidade real)*

## Sequência

1. Motor copiado e podado do que é exclusivo do harness.
2. Identidade trocada (sumário, strings, capa, créditos, URLs).
3. Estrutura do livro criada (arquivos do sumário).
4. Objeto interativo do módulo de lógica.
5. Chat: capacidades da trilha de TOC + corpus do novo livro.
6. CI adaptada.
7. Governança (`CLAUDE.md`, `HISTORICO.md`).
8. Verificação: build + verifica + pytest, com evidência.

## DoD desta rodada

- [ ] `npm run build` verde (evidência anexada)
- [ ] `verifica-capitulos.mjs` verde
- [ ] `pytest` do chat verde
- [ ] Nenhuma menção residual ao tema do harness no site gerado
- [ ] Objeto interativo presente e compilado
- [ ] `HISTORICO.md` com a edição inaugural
- [ ] Rastreabilidade spec ↔ commits
