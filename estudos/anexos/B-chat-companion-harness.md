# Anexo B — Estudo do Chat Companion do livro "Engenharia de Harness"

> Relatório de agente de pesquisa, 2026-07-31. Fonte: `/home/user/harness_engineering/chat-companion/` + `publicar/tema/` + specs.

Resumo executivo: **é um harness de agente completo, próprio, em ~950 linhas de Python + 590 de JS puro, sem frameworks de chat/RAG**. É extremamente portável para TOC.

---

## 1. Arquitetura

### Stack

| Camada | Tecnologia | Onde |
|---|---|---|
| Backend | Python 3.11 + FastAPI + uvicorn + httpx + pydantic + psycopg3 | `chat-companion/backend/` |
| Frontend | **JavaScript puro, zero dependências, zero build** | `publicar/tema/companion.js` + `companion.css` |
| Banco | Postgres (Neon) — fallback `MemoryStore` | `backend/store.py` |
| Hospedagem backend | **Railway** (NIXPACKS) | `backend/railway.json`, `Procfile` |
| Hospedagem site | **GitHub Pages** (estático) via GitHub Actions | `.github/workflows/publicar.yml` |

```
Navegador (GitHub Pages, estático)
   │  widget flutuante — {session_id anônimo, message, chapter, mode, byok_key?}
   ▼
Backend FastAPI (Railway)
   ├─ LLMPort   → endpoint OpenAI-compatible (NVIDIA NIM) | BYOK por requisição
   ├─ ToolPort  → tools sandbox (hora, cálculo AST-safe, busca no livro)
   ├─ gating    → capacidades liberadas por capítulo (avançado × progressivo)
   ├─ BookIndex → RAG lexical próprio sobre corpus.json
   └─ StorePort → Postgres (Neon) | memória
```

### Arquivos do backend

| Arquivo | Linhas | Papel |
|---|---|---|
| `app.py` | 351 | Composition root + rotas FastAPI + CORS + rate limit + system prompt + SSE |
| `store.py` | 250 | `StorePort` (Protocol) + `MemoryStore` + `PostgresStore` (DDL inline) |
| `llm.py` | 121 | `LLMPort` (Protocol) + `EchoAdapter` + `OpenAICompatAdapter` (complete + stream) |
| `ragindex.py` | 100 | `BookIndex` — índice lexical do livro (carrega `corpus.json` ou varre `livro/`) |
| `tools.py` | 100 | Registro de tools sandbox + schemas OpenAI + gating na execução |
| `config.py` | 95 | Config por env var + `_load_dotenv()` caseiro |
| `loop.py` | 86 | Loop de tool-calling (`MAX_TURNS = 6`), sync e streaming |
| `capabilities.py` | 82 | `REGISTRO` das 12 capacidades × capítulo que libera × tools |
| `build_corpus.py` | 23 | Gera `corpus.json` a partir de `livro/` |
| `corpus.json` | 707 blocos / 509 KB | Corpus do livro versionado no git |
| `tests/test_smoke.py` | 188 | 15 testes, sem rede e sem banco (adapter echo + memória) |

### Endpoints (`app.py`)

| Método | Rota | Papel |
|---|---|---|
| GET | `/health` | healthcheck do Railway |
| GET | `/capabilities?chapter=&mode=` | mapa de capacidades |
| POST | `/session` | garante a sessão anônima |
| POST | `/chat` | turno completo (síncrono) |
| POST | `/chat/stream` | SSE — `{delta}/{trace}/{done}/{erro}` |
| GET | `/history?session_id=` | histórico para retomar |
| DELETE | `/session/{id}` | direito ao esquecimento (LGPD) |
| POST | `/suggestion` | sugestão do leitor → banco + email SMTP |
| GET | `/suggestions?token=` | autor lê sugestões (ADMIN_TOKEN) |
| POST | `/consent` | grava aceite versionado do disclaimer |
| POST | `/telemetry` | navegação anônima (slug × sessão), só com consentimento |
| GET | `/telemetry/publico` | agregado público (Apêndice de Uso) |
| GET | `/telemetry?token=` | resumo admin |
| POST/GET | `/objetivo` | objetivo declarado do leitor (`/plano`) |

---

## 2. Integração com o livro — widget injetado em build-time

Não é iframe nem página separada. O motor (`publicar/build.mjs`, 741 linhas, Markdown → HTML) injeta um snippet de 3 linhas no final de cada página gerada (`build.mjs:190-195`): `window.COMPANION={backend, chapter, mode, lang, capabilities}` + link CSS + script defer.

Pontos-chave:
- `build.mjs:391` injeta em toda página; `build.mjs:492` também na capa com `chapter=0`.
- `COMPANION_BACKEND` vem de `sumario.companion_backend` em `publicar/sumario.json`.
- `build.mjs:175-188` — espelho local das 12 capacidades (`COMPANION_CAPS`), duplicado de `capabilities.py`. **Única duplicação de fonte-da-verdade do sistema.**
- `capituloDe(titulo)` extrai o número do capítulo do título; capa/apêndices → 0.
- `<body data-slug data-lang data-titulo>` — o `data-slug` alimenta telemetria.
- O PDF usa `_print.html` que não injeta o companion.

### O widget (`publicar/tema/companion.js`, 590 linhas)

- Launcher flutuante + painel; 3 layouts: `float` / `dock` / `max`
- Streaming SSE com fallback para `/chat` clássico
- Markdown mínimo seguro (escapa antes de formatar)
- Chips de capacidade com tooltip (✓ / 🔒 "libera no cap. NN")
- Paleta de comandos `/`: `/sugerir`, `/chave`, `/limpar`, `/bastidores`, `/plano`, `/tour`
- Painel "Bastidores": tokens estimados, janela de contexto, trechos RAG, tools, persistência, objetivo
- Tour de onboarding com spotlight (5 passos)
- Banner de consentimento versionado (`CONSENT_V = "v1"`) que bloqueia o chat até aceite
- BYOK: chave só em `localStorage`, mascarada
- i18n rudimentar via `CFG.lang`

CSS: `companion.css` (198 linhas), namespace `.cmp-*`, theme-aware. Ilha de dados: `uso.js` consome `/telemetry/publico` para o apêndice de uso + contador de visitas.

---

## 3. LLM e injeção de contexto

- **Qualquer endpoint OpenAI-compatible.** Default: NVIDIA NIM, modelo gratuito com function calling (constituição exige custo zero). Cliente httpx cru — trocar de provedor = novo adapter de ~40 linhas.
- **BYOK**: chave chega no body, usada só naquela chamada, nunca persistida/logada.
- `EchoAdapter` permite rodar e testar sem rede/chave.

### RAG lexical caseiro (não vetorial)

`ragindex.py`: quebra os `.md` em blocos por cabeçalho/parágrafo, normaliza (NFD, sem acentos, stopwords PT+EN), score = sobreposição de termos. `buscar(query, k)` → `{fonte, titulo, trecho[:600]}`.

System prompt em camadas (`app.py:70-91`): persona fixa → capacidades ativas → texto do modo (avançado/progressivo) → objetivo declarado do leitor → trechos RAG (k=3, com instrução de citar) → histórico (limit=40). Tool `buscar_no_livro` (k=4) liberada a partir do cap. 05.

**Dívida:** `corpus.json` é gerado manualmente e commitado; **não há step de CI que o regenere** — pode ficar defasado em relação ao livro.

---

## 4. Monitoramento / telemetria — o gap

### O que existe

Tabelas: `messages` (conversas completas), `sessions`, `suggestions`, `consents`, `nav_events`, `goals`. Telemetria por turno (`_debug`): trechos RAG, nº de mensagens, chars do prompt, tokens estimados, tools, modo, capacidades, objetivo.

### O que NÃO existe

1. **Nenhuma análise por IA das conversas** — as mensagens ficam no Postgres e ninguém as lê automaticamente.
2. **Nenhum endpoint admin para ler conversas** (sugestões e telemetria têm ADMIN_TOKEN; conversas não).
3. **Nenhum dashboard de autor/professor.**
4. **`/history` sem auth** — qualquer um com o `session_id` lê a conversa. Corrigir antes de usar com alunos identificados.
5. Sem tracing, custo por turno, latência, taxa de erro, logs estruturados.
6. Sem avaliação de qualidade das respostas.

---

## 5. Configuração e deploy

Env vars principais: `LLM_ADAPTER` (echo|openai), `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `LLM_MODEL`, `DATABASE_URL` (vazio → memória), `ALLOWED_ORIGINS`, `RATE_LIMIT_*`, `ALLOW_BYOK`, `SUGGESTION_EMAIL_TO`, `SMTP_*`, `ADMIN_TOKEN`.

Deploy: Railway com **Root Directory = `chat-companion/backend`** (é o que força o corpus versionado), healthcheck `/health`, domínio gerado. Banco Neon — tabelas criadas sozinhas na subida (`CREATE TABLE IF NOT EXISTS`), zero migrations. Site: GitHub Pages via workflow (build PT+EN → Playwright → PDF → deploy).

Rodar local: `uvicorn app:app --reload` sobe em echo + memória sem config. Testes: `python -m pytest` (15 testes, sem rede).

---

## 6. O que mudar para reutilizar com TOC

### Trabalho mínimo (10 pontos)

| # | Arquivo | Mudança | Esforço |
|---|---|---|---|
| 1 | `capabilities.py` | Reescrever `REGISTRO` → trilha TOC ("Pensamento Crítico" → "Nuvem" → "Druida" → "Injeções" → "APR"…). Mecânica não muda | Médio |
| 2 | `app.py` (`_system_prompt`) | Persona → tutor de TOC | Baixo |
| 3 | `tools.py` | Renomear `buscar_no_livro`; adicionar tools TOC (validar nuvem, validar UDE…) | Médio |
| 4 | `ragindex.py` | Zero mudanças se conteúdo for markdown; ajustar paths hard-coded | Baixo |
| 5 | `build_corpus.py` + `corpus.json` | Regerar; **criar o step de CI que falta** | Baixo |
| 6 | `build.mjs:175-188` | Espelhar novo REGISTRO (melhor: JSON único compartilhado) | Baixo |
| 7 | `sumario.json` | Nova URL Railway | Trivial |
| 8 | `companion.js` | Strings PT hard-coded (greet, consentimento, comandos, tour) | Médio |
| 9 | `config.py` | `SUGGESTION_EMAIL_TO` | Trivial |
| 10 | `.env.example`, `README.md`, `EMAIL.md` | Textos e URLs | Baixo |

**Não muda:** `llm.py`, `loop.py`, `store.py`, CORS/rate-limit/SSE/consent/telemetry, `companion.css`, ~80% de `companion.js`.

### Mudanças estruturais recomendadas para plataforma educacional

1. Externalizar persona e capacidades para config (`prompt.md` + `capabilities.json`) — mesmo backend serve vários cursos.
2. **Identidade de aluno** (auth magic-link, `user_id` nas tabelas) — hoje é UUID anônimo em localStorage.
3. **Auth no `/history`.**
4. **Camada de monitoramento por IA (não existe — construir):** endpoint admin `GET /conversas?token=` com filtros; job periódico LLM classificando conversas (tema, tipo de dúvida, conceito TOC, confusão, lacuna, sentimento); tabela `analises` + dashboard do professor; alertas (aluno travado, pergunta sem resposta no material); métricas operacionais. O `LLMPort` já dá a base — é o mesmo port com outro system prompt.
5. RAG vetorial se o corpus crescer — troca local em `BookIndex.buscar()`; Neon suporta pgvector.
6. Corpus no CI.

### Licença

`chat-companion/` é **MIT** (`LICENSE-CODE`) — livre para reuso. O texto do livro é CC, mas não afeta o companion com conteúdo substituído.

### Specs de referência

`specs/016-chat-companion-backend` (arquitetura), `017-widget-chat-companion`, `047-companion-sse`, `048-byok-widget`, `049-rate-limit-persistente`, `053-chat-ux`, **`054-experiencia-educacional`** (a mais relevante — consentimento, tour, telemetria, plano de ensino), `055-apendice-uso-vivo`, `058-contador-visitas`. ADRs: `adr/0006-design-system-componentes.md`, `0007-cadencia-livro-vivo.md`.
