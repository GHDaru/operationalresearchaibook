# Estudo Educacional e Roadmap — Treinamento de TOC com Chat e Monitoramento por IA

> **Data da captura:** 2026-07-31
> **Autor:** Gilsiley Darú (com apoio de agente de IA)
> **Status:** proposta para validação — base para as primeiras specs do projeto

---

## 1. Contexto e pergunta

Construir um **treinamento digital de Teoria das Restrições (TOC)** — a partir do conteúdo do curso **BBIT, Módulo Fundamentos** (Google Drive) — em uma **plataforma educacional com chat tutor de IA e monitoramento de aprendizagem por IA**, inspirada na ideia do LearnAI e reaproveitando o chat do livro *Engenharia de Harness*.

Este estudo respondeu, com investigação real dos ativos e da literatura:

1. Que conteúdo TOC já existe e em que estado?
2. Que infraestrutura já existe e o que é portável?
3. Qual o melhor formato educacional segundo a evidência 2024–2026?
4. Qual o plano de ataque (roadmap) para construir o treinamento?

Foram estudadas 5 frentes em paralelo: (a) os módulos BBIT no Drive (~110 arquivos); (b) o `chat-companion` do harness_engineering; (c) o LearnAI; (d) o theoryofconstraintlivebook + os 4 TOC-Builders + skills TOC; (e) pesquisa de formatos educacionais com fontes citadas.

---

## 2. Inventário de ativos — o que já existe

### 2.1 Conteúdo: BBIT Módulo Fundamentos (Google Drive)

Pasta `Módulos BBIT / 1 - Fundamentos` (id `1od7gQKG-4x5WUg5HDjk36n33hUUTpDdQ`). Tradução/adaptação em português do programa **Black Belt in Thinking** (Peter Cronin), estruturado em 6 semanas, ~1h/dia:

| # | Módulo | Ferramenta ensinada |
|---|--------|---------------------|
| 0 | Introdução | Por que ferramentas de decisão (Kahneman, Sistema 1/2); operação do curso |
| 1 | Pensamento Crítico | Lógica de causa e efeito, lógica de pré-requisito, premissas, cadeias lógicas |
| 2 | Nuvens | Evaporating Cloud — conflito entre 2 ações, necessidades, objetivo comum |
| 3 | Druida | Druid Loop — problemas recorrentes/oscilantes (loop entre 2 comportamentos) |
| 4 | Injeções | Geração de soluções por levantamento e inversão de premissas |
| 5 | Análise de Pré-Requisitos | PRT simplificada: objetivo → obstáculos → OIs → sequenciamento |
| 6 | Aplicação Final | Capstone integrador cronometrado (1h): problema real → Nuvem/Druida → Injeção → APR |

**Estado do acervo:**

- ✅ **Ouro pedagógico**: desenho instrucional completo e consistente — conceito → exemplo → prática guiada com gabarito → aplicação pessoal → erros comuns → prova. Bancos de exercícios com gabarito em todos os módulos; apostilas de "Erros Comuns" de alta qualidade; provas de múltipla escolha com respostas.
- ⚠️ **100% texto (.docx)**, majoritariamente **transcrições literais de vídeo-aulas** (oralidade, digressões, tradução imperfeita) — precisam de reescrita editorial.
- ❌ **Sem vídeos, sem diagramas** (as imagens embutidas nos docx de resposta não são capturadas por extração de texto) e **infraestrutura de prática dependente de Miro + mentor humano + Zoom + Circle**.
- 🚨 **Risco jurídico**: conteúdo derivado do BBIT de Peter Cronin. Uso comercial exige licença ou **reescrita substancial** (novo texto, novos exemplos, nova estrutura autoral). Decisão a registrar em ADR antes da Fase de conteúdo.

### 2.2 Infra de chat: `harness_engineering/chat-companion` — **o ativo mais portável**

Harness completo, próprio, sem frameworks: FastAPI (~950 linhas Python) + widget JS puro (590 linhas, zero dependências) + Postgres/Neon + deploy Railway + site GitHub Pages. Licença **MIT** — livre para copiar.

**Já vem pronto:** streaming SSE, RAG lexical sobre corpus markdown, **gating de capacidades por capítulo** (mecânica perfeita para trilha pedagógica progressiva), consentimento LGPD versionado, telemetria de navegação, sugestões de leitores, painel "Bastidores", tour de onboarding, BYOK, rate limit, modo echo para testes sem rede.

**Portar para TOC é trabalho pequeno e mapeado** (10 pontos de mudança, a maioria trivial): persona do system prompt, registro de capacidades (vira a trilha TOC), corpus, URLs, e-mails. `llm.py`, `loop.py`, `store.py`, SSE, CORS e ~80% do widget não mudam.

**O que NÃO existe lá (gap central deste projeto):** análise por IA das conversas. As mensagens ficam no Postgres mas ninguém as lê. Não há dashboard de professor, classificação de dúvidas, detecção de aluno travado, nem endpoint admin de conversas. Também falta **identidade de aluno** (hoje: UUID anônimo em localStorage) e auth no `/history`.

### 2.3 Motor pedagógico: LearnAI — **fonte de design, não base de código**

Protótipo demo (Google AI Studio): sem banco, sem auth, tudo em memória, trilha travada em 3 módulos, model ID de Gemini inválido. **Não evoluir esse código.** Mas o design é valioso e será copiado:

- **Modelo de dados** (`src/types.ts`): `Course/CourseStep{concept}`, `StudentSession` com máquina de estados (`learning → relearning → evaluating → completed → tutor_flagged`), `Interaction` tipada semanticamente, `TutorAlert`.
- **Loop pedagógico**: pergunta socrática → resposta aberta → **nota 0–100 + feedback que não entrega a resposta** → plano de reforço em caso de dificuldade → **escalonamento a tutor humano** → quiz final personalizado gerado a partir das hesitações → certificado.
- **Persona pedagógica injetável** (presets) — para TOC: persona "Jonah" socrática.
- Contrato de prompt de avaliação com 4 campos (`score`, `feedback`, `tutorAlertNeeded`, `relearningPlan`).

### 2.4 Ferramentas e conteúdo TOC: tocbuilderv3 + skills

- **`theoryofconstraintlivebook` está vazio** (zero commits) — é a folha em branco destino deste projeto.
- **`tocbuilderv3`** é o único builder vivo (v1/APP/V2 são gerações anteriores da mesma app). Candidato a **laboratório prático** do curso: canvas de ARA, Nuvem que Evapora completa com premissas/injeções, i18n PT/EN, docs didáticos. Sem backend real (mocks) — `api_specifications.md` pronto e nunca implementado.
- **Tesouro em `tocbuilderv3/constants.ts`**: rubrica completa de validação de UDE (11 características, 6 eixos — praticamente um capítulo pronto), prompt de Nuvem com TRIZ (5 princípios de separação), catálogo de prompts-especialistas administrável.
- **Skills já instaladas**: `toc-evaporating-cloud` (nuvem + HTML interativo) e `toc-prt` (metodologia PRT em 8 fases) — mais rigorosas metodologicamente que o app; e `gerar-aula` (aulas HTML com quiz integrado).
- **Molde de publicação**: `harness_engineering/publicar/` (markdown → HTML + PDF, sumário JSON, tema CSS, CI GitHub Pages) — clonável direto.

### 2.5 Lacunas de conteúdo TOC (nada escrito em lugar nenhum)

5 Passos de Focalização; Throughput/Inventário/Despesa Operacional (contabilidade de ganhos); DBR/CCPM (área de expertise do autor — dissertação de mestrado); ARF e Árvore de Transição; CLR (Categorias de Reserva Legítima); Camadas de Resistência. O BBIT Fundamentos cobre só os Processos de Raciocínio básicos — esses temas são candidatos a **módulos futuros** (o Drive já tem "2 - Causando a Mudança" como próximo módulo BBIT).

---

## 3. Pesquisa: qual o melhor formato educacional (evidência 2024–2026)

Síntese dos achados com maior força de evidência:

1. **Learning-by-doing ("doer effect")** — evidência causal mais sólida: prática formativa intercalada no conteúdo ensina ~6x mais que ler/assistir vídeo (Koedinger/CMU, ACM LAK 2023; extensão com prática gerada por IA, ACM L@S 2025). Valida diretamente o formato "livro vivo com prática embutida".
2. **Microlearning** — meta-análises 2024/2025: OR 1,87 para retenção, d = 0,74 para resultados. Unidades curtas + prática distribuída.
3. **Self-paced puro tem conclusão de um dígito** (linha de base: "The MOOC Pivot", *Science* 2019, ~3%). O antídoto com precedente é **coorte leve** (prazos, accountability, nudges), não necessariamente aulas ao vivo — o público adulto prefere autonomia de ritmo.
4. **Tutor de IA: o design separa ganho de dano.** RCT Harvard (*Sci. Reports* 2025): tutor com scaffolding socrático e guardrails **dobrou** a aprendizagem vs. aula ativa. Contra-evidência PNAS 2025: ChatGPT "cru" virou muleta — desempenho **caiu 17%** quando retirado; a versão com guardrails (dica em camadas, nunca a resposta) eliminou o dano. **A política do tutor é a decisão mais importante do projeto.**
5. **Padrão socrático híbrido**: factual/referência → resposta direta com fonte (RAG); conceitual/exercício → perguntas e dicas em camadas com scaffolding decrescente. **Alinhamento raro**: é literalmente o método do Jonah em *A Meta* — a pedagogia da IA e o conteúdo do curso contam a mesma história.
6. **Monitoramento por IA**: literatura recomenda começar simples — mastery por conceito via quizzes, classificador de conversas (dúvida genuína / pedido de muleta / off-topic / frustração), alerta de inatividade com nudge e escalonamento humano. Dashboard conversacional é fase 2.
7. **Frameworks combinados** (mesma constituição pedagógica do harness_engineering): **Backward Design** define o que medir ("o aluno aplica as ferramentas ao próprio problema") → **4C/ID** define a sequência (tarefas-íntegras do simples ao complexo, scaffolding decrescente) → **Diátaxis** define a arquitetura do conteúdo e a base do RAG → **mastery + doer effect** definem o gate de progressão → **carga cognitiva + PNAS** definem o comportamento do tutor.

### Formato recomendado (decisão candidata a ADR)

**"Livro vivo interativo self-paced + tutor de IA socrático 'Jonah' + camada anti-abandono com monitoramento por IA"**:

- **Núcleo**: livro vivo em português, unidades de microlearning com prática intercalada (padrão Brilliant), publicado como site estático (molde harness). O desenho instrucional do BBIT (conceito → exemplo → prática com gabarito → aplicação pessoal → erros comuns → prova) **já é** esse formato — só muda a mídia.
- **Tutor "Jonah"**: chat-companion portado, com gating por módulo e política socrática com guardrails. O papel do "mentor humano" do BBIT é absorvido pelo loop do LearnAI (avaliação 0–100 + plano de reforço + escalonamento a humano).
- **Prática**: provas → quizzes automáticos; exercícios de diagrama (Nuvem, Druida, APR) → ferramentas interativas (tocbuilderv3 / componentes novos), substituindo o Miro.
- **Anti-abandono**: identidade de aluno, coortes leves com janelas/prazos, nudges automáticos, dashboard do professor com alertas de risco.
- **Métricas desde o dia 1**: conclusão por coorte, mastery por conceito, pré/pós-teste de aplicação — o curso deve gerar a própria evidência.

---

## 4. Arquitetura-alvo da plataforma

```
┌─ Livro vivo TOC (GitHub Pages, estático) ─────────────────┐
│  markdown → build.mjs → HTML/PDF                          │
│  lições microlearning + quizzes + diagramas interativos   │
│  widget chat "Jonah" injetado em cada página              │
└──────────────────┬────────────────────────────────────────┘
                   ▼
┌─ Backend (Railway, FastAPI — fork do chat-companion) ─────┐
│  LLMPort (OpenAI-compatible) · RAG sobre corpus do livro  │
│  gating de capacidades por módulo · SSE · consent LGPD    │
│  + identidade de aluno (magic link) e auth no histórico   │
│  + loop pedagógico LearnAI (score/feedback/reforço/alerta)│
└──────────────────┬────────────────────────────────────────┘
                   ▼
┌─ Monitoramento por IA (novo) ─────────────────────────────┐
│  job "juiz" LLM: classifica conversas por lote            │
│  (conceito TOC · tipo de dúvida · muleta · frustração)    │
│  tabela analises + dashboard do professor + alertas       │
└───────────────────────────────────────────────────────────┘
```

Componentes com dono claro: conteúdo (BBIT reescrito + constants.ts + skills), publicação (molde harness), chat (fork chat-companion), pedagogia do tutor (design LearnAI), monitoramento (novo, usando o mesmo LLMPort).

---

## 5. Roadmap — plano de ataque

Cada fase é uma entrega utilizável por si (o curso "anda" desde a Fase 2). Trabalhar spec-driven, uma branch por melhoria, no padrão já usado no harness_engineering.

### Fase 0 — Fundação do repositório (esforço: pequeno)
- Semear `theoryofconstraintlivebook`: constituição do projeto (adaptar a do harness: evidência, livro vivo, pedagogia combinada, custo zero, spec-kit), estrutura de pastas (`livro/`, `publicar/`, `chat/`, `estudos/`, `adr/`, `specs/`), guia editorial.
- **ADR-001: estratégia de direitos autorais** — reescrita autoral substancial do conteúdo BBIT (novos textos, novos exemplos brasileiros, estrutura própria) vs. licenciamento. *Bloqueia a Fase 1.*
- ADR-002: formato do curso (a recomendação da §3). ADR-003: stack (fork chat-companion + molde publicar).

### Fase 1 — Conteúdo piloto: 1 módulo de ponta a ponta (esforço: médio)
- Exportar os docx do módulo escolhido do Drive e reescrever como lições de microlearning (registro didático, exemplos próprios).
- **Piloto sugerido: Módulo 2 — Nuvens**: é o de maior sinergia (prompt TRIZ do tocbuilderv3 + skill `toc-evaporating-cloud` + conteúdo BBIT completo) e a ferramenta mais demonstrável.
- Estrutura de cada lição (Backward Design): objetivo verificável → conceito curto → exemplo → prática intercalada → erros comuns → quiz de mastery (das provas BBIT) → aplicação pessoal.
- Redesenhar os diagramas como SVG/HTML interativo.

### Fase 2 — Publicação: livro vivo no ar (esforço: pequeno)
- Clonar `publicar/` do harness (build.mjs, tema, CI GitHub Pages), adaptar sumário e identidade visual.
- Publicar o módulo piloto. **Marco: primeira URL pública do curso.**

### Fase 3 — Tutor "Jonah": chat no ar (esforço: médio)
- Fork do `chat-companion`: persona socrática com guardrails (nunca resolve o exercício; dica em camadas; factual → resposta direta com fonte), capacidades = módulos TOC, corpus do livro novo (com step de CI que faltava no original), deploy Railway + Neon.
- Tools iniciais: buscar_no_livro, validar_nuvem (rubrica do tocbuilderv3), validar_ude.
- **Marco: aluno estuda o módulo piloto conversando com o Jonah.**

### Fase 4 — Identidade de aluno e loop pedagógico (esforço: médio-grande)
- Auth por magic link; `user_id` nas tabelas; auth no `/history`; progresso durável entre dispositivos.
- Portar o loop LearnAI para o backend: avaliação de resposta aberta 0–100 com feedback, gate de mastery por lição, plano de reforço, alerta a tutor humano, quiz final personalizado, certificado.
- **Marco: trilha completa com progressão e avaliação real.**

### Fase 5 — Monitoramento por IA (esforço: médio) — *o diferencial pedido*
- Job periódico "juiz" (mesmo LLMPort): classifica conversas por lote — conceito TOC, tipo de dúvida (genuína/muleta/off-topic), sinal de frustração, lacuna do material.
- Tabela `analises` + endpoint admin autenticado + **dashboard do professor**: mastery por conceito, funil por módulo, alunos em risco (inatividade > X dias, erro persistente, padrão muleta), custo/latência por turno.
- Nudges automáticos e fila de escalonamento.
- **Marco: professor enxerga a turma sem ler conversa por conversa.**

### Fase 6 — Escala de conteúdo e coorte (esforço: grande, contínuo)
- Demais módulos na esteira das Fases 1–2: Pensamento Crítico → Druida → Injeções → APR → Aplicação Final (capstone com prazo, avaliado pelo pipeline da Fase 4).
- Coortes leves: janelas com prazos, kickoff, comunidade.
- Ferramentas interativas do tocbuilderv3 integradas como laboratório (requer implementar o backend do `api_specifications.md` — avaliar custo/benefício vs. componentes embutidos no livro).
- Módulos avançados futuros: 5 Passos de Focalização, Throughput Accounting, DBR/CCPM (expertise do autor), ARF/AT, CLR.
- Instrumentação de pesquisa: pré/pós-teste, A/B da política do tutor.

### Sequência crítica

```
ADR direitos autorais → Módulo piloto reescrito → Livro no ar → Jonah no ar
     (Fase 0)               (Fase 1)               (Fase 2)      (Fase 3)
                                                       ↓
             Coorte + escala ← Monitoramento IA ← Identidade + loop pedagógico
                (Fase 6)          (Fase 5)              (Fase 4)
```

---

## 6. Riscos e decisões em aberto

| Risco / decisão | Impacto | Mitigação proposta |
|---|---|---|
| Direitos autorais BBIT (Peter Cronin) | Bloqueia publicação comercial | ADR-001 antes de escrever; reescrita autoral com exemplos próprios, ou contato para licença |
| Tutor vira "muleta" (dá respostas) | Anula o valor pedagógico (PNAS: −17%) | Guardrails no system prompt + eval contínuo + classificador de muleta na Fase 5 |
| Conclusão baixa (self-paced) | Curso sem alunos formados | Coorte leve + nudges + monitoramento de risco (Fases 5–6) |
| Escopo do tocbuilderv3 (backend nunca implementado) | Fase 6 incha | Preferir componentes interativos embutidos no livro; builder como opcional |
| Corpus defasado do livro (dívida herdada do harness) | Tutor responde versão antiga | Step de CI que regenera o corpus no build (Fase 3) |
| Custo de LLM | Constituição exige trilha a custo zero | Manter endpoint gratuito (NIM) + BYOK, como no harness |

---

## 7. Próximo passo imediato

Validar com o autor: (1) a estratégia de direitos autorais (ADR-001); (2) o módulo piloto (sugestão: Nuvens); (3) o formato recomendado. Com isso aprovado, abrir a primeira spec (`001-fundacao-repositorio`) e iniciar a Fase 0.
