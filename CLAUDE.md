# CLAUDE.md — instruções para agentes neste repositório

Este repositório é o livro vivo **Teoria das Restrições** — um treinamento em raciocínio rigoroso, com chat tutor e (em construção) monitoramento de aprendizagem por IA.

## Regra primária

**Todo trabalho neste repositório DEVE seguir a [constituição do livro](.specify/memory/constitution.md)** — leia-a por inteiro antes de contribuir. Em caso de conflito entre um pedido pontual e a constituição, o conflito é explicitado ao autor antes de agir.

A constituição herda a metodologia **Maestro** (`GHDaru/maestro`) para o processo: a especificação é a fonte de verdade, os agentes executam, o humano decide, aprova e verifica. As skills do Maestro estão instaladas em `.claude/skills/` e **comandam, não sugerem** — cada uma tem sua Iron Law. Antes de agir, verifique se alguma se aplica: `constitution-check` (ao escrever um plan), `dod-verificavel` (ao escrever critérios de aceite), `combater-amontoado` (ao revisar texto denso), `anti-padroes` (ao desenhar fluxo ou revisar agente), `diagnostico-antes-do-fix` (SEMPRE antes de corrigir um bug).

Os princípios específicos deste livro, resumidos:

1. **É um treino, não uma leitura** — capítulo sem prática com devolutiva está *incompleto*.
2. **Bilíngue por padrão (PT+EN)** — nenhum capítulo é dado por pronto sem o par EN; tradução defasada nunca finge ser atual.
3. **Conteúdo autoral com fonte rastreável.**
4. **Livro vivo** — datado, versionado, reescrito.
5. **O tutor treina, não substitui o raciocínio** — guardrails socráticos são regra constitucional.
6. **Estrutura declarativa** — o livro cresce por adição, sem tocar no motor.
7. **Acessibilidade e custo zero** na trilha padrão.

O que isso exige na prática:

1. **Spec-driven** — nenhum trabalho nasce sem especificação. **Uma spec por rodada**, cada rodada em **sua própria branch** (`NNN-nome`), registrada em `specs/NNN-nome/`. Mudança de escopo volta à spec antes de virar conteúdo ou código.
2. **Raias de trabalho** — *leve* (typo, link quebrado: o commit é o artefato), *plena* (capítulo novo, feature: spec completa), *infra* (deploy, migração, banco: sempre plena, com gates de reversibilidade).
3. **Gates humanos inegociáveis** — o autor aprova a spec, o plan (Constitution Check), o merge e qualquer deploy. Nenhum desses é delegável a agente.
4. **Prove, não declare** — "pronto" exige evidência anexada: build verde, verificação por página verde, testes verdes. Afirmar que funciona não basta.
5. **Quem executa não verifica** — a revisão final passa por agente em contexto fresco.
6. **Decisões viram ADR** em `adr/`, com contexto, alternativas avaliadas e consequências.

As regras de escrita do livro — método pedagógico, esqueleto de capítulo, citação de fontes, objetos interativos — estão no [`livro/GUIA-EDITORIAL.md`](livro/GUIA-EDITORIAL.md). Leia antes de escrever qualquer conteúdo.

## Restrições

- **Direitos autorais.** O texto publicado é **autoral**. Materiais de estudo de terceiros ficam no repositório privado `GHDaru/tocmaterials` e **não são reproduzidos aqui**; as obras são citadas por fonte oficial na [bibliografia](livro/bibliografia.md).
- **Sem segredos** em arquivo, commit ou texto. Credenciais só em `.env` fora do versionamento.
- **Custo zero** na trilha padrão do tutor: endpoint gratuito + BYOK.
- **Português** com termos técnicos consagrados sem tradução forçada.

## Mapa do repositório

- `livro/` — o livro. `GUIA-EDITORIAL.md` (como escrever), `HISTORICO.md` (edições), `bibliografia.md`, `glossario.md`, `capitulos/`.
- `publicar/` — o motor: Markdown → HTML + PDF. `build.mjs`, `sumario.json` (a estrutura declarada do livro), `tema/` (CSS/JS), `viz/` (ilhas interativas), `verifica-capitulos.mjs` (portão de qualidade por página).
- `chat-companion/backend/` — o tutor: FastAPI, RAG sobre o corpus do livro, gating de capacidades por módulo. A persona socrática está em `app.py` (`PERSONA`) e o gating em `capabilities.py`.
- `estudos/` — o estudo educacional que originou o projeto e o registro de decisões.
- `specs/` — uma pasta por rodada.
- `adr/` — Architecture Decision Records.

## Verificação (o que rodar antes de dar por pronto)

```bash
cd publicar && npm run build          # gera o site + roda o portão de qualidade
cd chat-companion/backend && python -m pytest -q
```

O merge na `main` é o que publica (GitHub Pages, via `.github/workflows/publicar.yml`).

## Notas de arquitetura

- **A estrutura do livro é declarativa.** Adicionar um capítulo = criar o `.md` + adicionar o item em `publicar/sumario.json`. Nenhuma mudança de motor é necessária para o livro crescer.
- **O gating do tutor espelha os módulos.** `capabilities.py` é a fonte da verdade; `COMPANION_CAPS` em `build.mjs` é um espelho para exibição. Mudou um, mude o outro.
- **Objetos interativos** são ilhas React em `publicar/viz/`, montadas em `<div data-viz="chave">`. Regra: progressive enhancement — sem JS, o Markdown em volta da ilha mostra o mesmo conteúdo.
- **O motor veio do livro *Engenharia de Harness*** (mesmo autor, licença MIT), adaptado. Ver `adr/0001-reuso-motor-livro-vivo.md`.
