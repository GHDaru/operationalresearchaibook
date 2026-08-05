# Tasks 001 — Clonar o motor do livro vivo

Estado ao fim da rodada. Evidência de verificação em `verificacao.md`.

## Motor

- [x] T01 — Copiar `publicar/` e `chat-companion/` do livro *Engenharia de Harness* (MIT)
- [x] T02 — Copiar CI de Pages, `.gitignore`, licenças
- [x] T03 — Tornar o motor monolíngue por ausência do `sumario.en.json` (flag `BILINGUE`), sem quebrar a máquina EN
- [x] T04 — Trocar identidade: URLs, site, títulos, créditos, nomes dos artefatos (PDF/MD)
- [x] T05 — Adaptar marcador de datação: "Estado da arte capturado em" → "Conteúdo revisado em"
- [x] T06 — Ajustar limiares do portão de qualidade ao tamanho deste livro (11 capítulos)
- [x] T07 — Remover assets e componentes exclusivos do harness (diagrama, viz de benchmark)
- [x] T08 — Neutralizar strings residuais no tema (`app.js`, `grafo.js`, `companion.js`) e no backend
- [x] T09 — Capa própria em SVG (metáfora do elo restritivo) + favicon + card social
- [x] T10 — DOI condicional (o livro ainda não tem um) e convite a edição EN desativado

## Estrutura e conteúdo

- [x] T11 — `sumario.json` com a estrutura modular (Abertura + 3 módulos + aparato)
- [x] T12 — Abertura: capítulos 00 e 01
- [x] T13 — Módulo 1 (fundamentos lógicos), com profundidade: 02, 03, 04, 05
- [x] T14 — Módulo 2 (conflitos), primeira versão: 06, 07
- [x] T15 — Módulo 3 (solução e plano), primeira versão: 08, 09, 10
- [x] T16 — Aparato: glossário, bibliografia com fontes primárias, histórico, guia editorial, autor

## Objetos interativos

- [x] T17 — Religar as ilhas React ao novo catálogo de componentes
- [x] T18 — Primeiro objeto: "Que conexão é esta?" (classificar causa e efeito × pré-requisito), com devolutiva explicativa e placar
- [x] T19 — CSS das ilhas, com suporte a tema claro/escuro
- [x] T20 — Fallback sem JavaScript (a lista estática do Markdown permanece visível)

## Tutor

- [x] T21 — Reescrever `capabilities.py` com a trilha de TOC (11 capacidades por módulo)
- [x] T22 — Persona socrática com guardrails explícitos (`PERSONA` em `app.py`)
- [x] T23 — Espelhar o registro em `COMPANION_CAPS` (`build.mjs`)
- [x] T24 — Regerar o corpus a partir do novo livro; remover dependência do benchmark no RAG
- [x] T25 — Atualizar os testes que codificavam o gating antigo
- [x] T26 — Regerar o corpus no CI (corrige dívida herdada do motor original)

## Governança

- [x] T27 — `CLAUDE.md` apontando ao processo Maestro
- [x] T28 — ADR 0001 (reuso do motor), com alternativas e consequências
- [x] T29 — `HISTORICO.md` com a edição inaugural
- [x] T30 — README do repositório

## Fora desta rodada (registrado para as próximas)

- [ ] Deploy do backend (Railway) e banco (Neon) — exige credenciais do autor; raia infra, com gate próprio
- [ ] ADR 0002 — front: Vercel × GitHub Pages
- [ ] Objetos interativos para Nuvem, loop e Análise de Pré-Requisitos
- [ ] Aprofundamento dos módulos 2 e 3 com o material de `tocmaterials`
- [ ] Identidade de aluno, loop pedagógico e monitoramento por IA (Fases 4–5 do roadmap)
