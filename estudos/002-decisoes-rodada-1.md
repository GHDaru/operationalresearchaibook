# Decisões da Rodada 1 (estudo)

> **Data:** 2026-07-31 · **Decisor:** Gilsiley Darú
> Registro das decisões tomadas sobre o estudo `001-estudo-educacional-e-roadmap.md`.
> Cada uma será detalhada em ADR próprio quando a fundação do repositório for criada.

## Decisões do autor

1. **Fundamentos lógicos primeiro.** O curso abre exercitando as questões lógicas
   (causa-e-efeito, pré-requisito, premissas, cadeias lógicas — a ideia do módulo
   Pensamento Crítico do BBIT) antes das ferramentas TOC. O piloto de conteúdo é o
   módulo de fundamentos lógicos, não o de Nuvens.

2. **Livro evolutivo e em módulos.** Livro vivo que cresce módulo a módulo, conforme
   novos materiais forem adicionados. Arquitetura modular: sumário incremental +
   gating de capacidades do chat por módulo.

3. **Materiais-fonte privados + referências oficiais.** Os materiais de estudo ficam
   em repositório privado (não são redistribuídos). O livro publicado é autoral e
   cita cada obra por suas fontes oficiais (autor, editora, edição). Isso endereça o
   risco de direitos autorais apontado no estudo (§6).

4. **Processo Maestro.** Todo o trabalho segue a metodologia Maestro
   (`GHDaru/maestro`): spec-driven (`specify → clarify → plan (Constitution Check) →
   tasks → implement`), **uma spec por rodada, cada rodada em sua própria branch**,
   raias de trabalho (leve/plena/infra), DoD verificável ("prove, não declare"),
   revisão independente em contexto fresco, gates humanos inegociáveis (spec, plan,
   merge, deploy).

5. **Objetos interativos com o usuário.** O livro terá componentes interativos
   (exercícios de lógica, diagramas manipuláveis, quizzes) — não apenas texto + chat.

6. **O livro terá backend.** Stack decidido:
   - **Banco:** Neon (Postgres)
   - **Backend:** Railway
   - **Frontend:** Vercel ou GitHub Pages (decisão em aberto — ADR na fundação)

## Consequências para o roadmap

- A Fase 1 (conteúdo piloto) passa a ser o **módulo de fundamentos lógicos**.
- O backend deixa de ser só o chat: passa a servir também os objetos interativos e o
  progresso do aluno — reforça a escolha do fork do `chat-companion` (mesmo stack
  Railway + Neon já validado) como base.
- A decisão Vercel × GitHub Pages fica para o ADR de stack da fundação (critérios:
  objetos interativos podem pedir SSR/ISR ou continuar estáticos consumindo a API).

## Pendência

- O autor passará o diretório de materiais (`150_TOC`, hoje local) — provavelmente
  via repositório privado no GitHub ou Google Drive. A spec da Rodada 2 (fundação)
  aguarda esse insumo para mapear o acervo.

## Encerramento da rodada

Rodada 1 = estudo educacional + pesquisa de formato + roadmap (`001`) + estas
decisões. Branch `claude/educational-material-toc-ai-naotqe`, mergeada na `main`
com a publicação deste registro.
