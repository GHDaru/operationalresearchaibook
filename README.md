# Teoria das Restrições — livro vivo

Um treinamento em raciocínio rigoroso: da lógica de causa e efeito às ferramentas de decisão da Teoria das Restrições. Livro vivo, modular e evolutivo, com objetos interativos e tutor de IA.

**Site:** <https://theoryofconstraintlivebook.vercel.app/> — publicado a cada merge na `main`.

## Como está organizado

| Diretório | O que é |
|---|---|
| `livro/` | O livro em Markdown. Comece pelo [Guia Editorial](livro/GUIA-EDITORIAL.md) e pelo [Histórico](livro/HISTORICO.md) |
| `publicar/` | O motor: Markdown → HTML + PDF. `sumario.json` declara a estrutura; `viz/` traz os objetos interativos |
| `chat-companion/` | O tutor: FastAPI + RAG sobre o texto do livro, com capacidades liberadas por módulo |
| `estudos/` | O [estudo educacional](estudos/001-estudo-educacional-e-roadmap.md) que originou o projeto, com o roadmap |
| `specs/` | Uma pasta por rodada de trabalho (metodologia Maestro) |
| `adr/` | Decisões de arquitetura, com alternativas e consequências |
| `docs/infra/` | Runbook de deploy (Vercel, Neon, Railway) |

## Estrutura do livro

- **Abertura** — por que ferramentas de raciocínio existem e o que corrigem.
- **Módulo 1 — Fundamentos lógicos** — causa e efeito, pré-requisito, premissas, cadeias. A lógica é exercitada antes das ferramentas.
- **Módulo 2 — Conflitos** — a Nuvem e o problema que sempre volta.
- **Módulo 3 — Solução e implementação** — injeções, análise de pré-requisitos e a aplicação integrada.

## Rodar localmente

```bash
# o site
cd publicar && npm ci && npm run build      # gera docs/ e roda o portão de qualidade
python3 -m http.server 8000 --directory ../docs

# o tutor (sobe sem chave nem banco, em modo echo + memória)
cd chat-companion/backend && pip install -r requirements.txt
uvicorn app:app --reload
python -m pytest -q
```

## Como contribuir

O trabalho segue a metodologia **Maestro**: uma spec por rodada, cada rodada em sua branch, com gates humanos para spec, plan e merge. As regras estão em [`CLAUDE.md`](CLAUDE.md); as regras de escrita, no [Guia Editorial](livro/GUIA-EDITORIAL.md).

## Licenças

- **Texto do livro:** ver [`LICENSE`](LICENSE).
- **Código** (motor de publicação e tutor): MIT — ver [`LICENSE-CODE`](LICENSE-CODE). O motor é derivado do livro *Engenharia de Harness*, do mesmo autor ([ADR 0001](adr/0001-reuso-motor-livro-vivo.md)).
