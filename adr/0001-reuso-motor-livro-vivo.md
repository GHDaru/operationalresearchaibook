# ADR 0001 — Reusar o motor do livro *Engenharia de Harness*

- **Status:** aceito
- **Data:** 2026-08-01
- **Rodada:** 2 (`specs/001-clone-motor-livro`)
- **Decisor:** Gilsiley Darú

## Contexto

O projeto precisa de um livro vivo publicado, com chat tutor e objetos interativos. O estudo da Rodada 1 (`estudos/001-estudo-educacional-e-roadmap.md`) apurou que o livro *Engenharia de Harness*, do mesmo autor, já opera em produção com exatamente essa máquina: motor próprio Markdown → HTML + PDF, tema, ilhas React, chat com RAG e gating por capítulo, e CI de publicação no GitHub Pages. O código é MIT.

A alternativa era construir do zero — o que repetiria trabalho já validado e adiaria em várias rodadas o momento em que o autor veria o livro no ar.

## Decisão

**Clonar o motor inteiro e trocar o conteúdo**, adaptando apenas os pontos de identidade (sumário, strings, URLs, capacidades do tutor, assets).

Consequências diretas do desenho herdado que foram mantidas de propósito:

- **Estrutura declarativa** — o livro cresce editando `publicar/sumario.json`; o motor não muda.
- **Gating por capítulo** — a mecânica que no livro original liberava capacidades técnicas passa a ser a **trilha pedagógica progressiva** (o *fading* do 4C/ID).
- **Ilhas React** como mecanismo dos objetos interativos, em vez de introduzir um framework de front.

## Alternativas avaliadas

| Alternativa | Por que não |
|---|---|
| Construir motor próprio do zero | Repetiria trabalho validado; atrasaria o feedback do autor em várias rodadas; sem ganho identificável |
| Plataforma de curso pronta (LMS) | Não entrega livro vivo versionado em Markdown nem tutor com RAG sobre o próprio texto; prende o conteúdo |
| Evoluir o protótipo LearnAI | Estudado na Rodada 1: sem persistência, sem auth, trilha travada em 3 módulos. Serve como **fonte de design** (loop pedagógico, modelo de dados), não como base de código |
| Site estático genérico (Docusaurus, MkDocs) | Resolveria a publicação, mas não traz chat, gating nem o portão de qualidade por página — que é o que garante consistência editorial |

## Consequências

**Positivas**

- Livro no ar em uma rodada, com PDF, busca, tema claro/escuro, telemetria e consentimento LGPD já resolvidos.
- Portão de qualidade por página (`verifica-capitulos.mjs`) força consistência editorial desde o primeiro capítulo.
- O tutor nasce com RAG sobre o texto do próprio livro.

**Negativas e dívidas assumidas**

- **Acoplamento a um motor não documentado como produto.** Mitigação: o build e a verificação por página são o portão que denuncia quebra.
- **Espelho duplicado de capacidades** (`capabilities.py` ↔ `COMPANION_CAPS` em `build.mjs`). Herdado do original. Mitigação por ora: nota no `CLAUDE.md`. Unificar num JSON compartilhado quando o custo aparecer.
- **RAG lexical, não vetorial.** Suficiente para o tamanho atual do livro; a troca é local (`BookIndex.buscar`).
- **PT-only na v1.** O motor é bilíngue e a máquina EN permanece intacta, desativada por ausência do `sumario.en.json`.

**Corrigido em relação ao original**

- O corpus do tutor passa a ser **regerado no CI** a cada build. No livro original ele era gerado à mão e commitado, podendo ficar defasado em relação ao texto.
