# Anexo C — Estudo do LearnAI

> Relatório de agente de pesquisa, 2026-07-31. Fonte: `/home/user/LearnAI` (15 arquivos versionados, ~2.900 linhas).

## Visão geral

O LearnAI é um **protótipo/demo gerado no Google AI Studio** (não um produto): SPA React de arquivo único + servidor Express que usa o Gemini para (a) quebrar um material bruto em 3 módulos, (b) conduzir um loop socrático de pergunta→resposta→nota→feedback, (c) gerar um quiz final personalizado e (d) acionar um tutor humano quando o aluno trava. **Tudo em memória, sem banco, sem autenticação, sem testes.**

Sinais de demo: 2 commits; `package.json` chama-se `"react-example"`; README é boilerplate do AI Studio; a branch de trabalho é idêntica à `main` (nada de TOC ainda).

## 1. Conceito pedagógico (codificado nos prompts/UI, não em docs)

Propósito (`metadata.json`): "Transforma materiais estáticos em trilhas de aprendizado dinâmicas, adaptativas e personalizadas com IA, incluindo relatórios para tutores."

| Elemento | Onde | O que é |
|---|---|---|
| Persona pedagógica configurável | `src/App.tsx:449-474` | 4 presets (Socrático, Mentor Gamer, Cientista, Pragmático Corporativo) injetados em todos os prompts |
| "Nunca dê a resposta pronta" | `server.ts:767` | Princípio central |
| Material bruto como fonte única | `src/App.tsx:1791` | Grounding por colagem no prompt (não é RAG) |
| Avaliação formativa contínua | `server.ts:751-771` | Nota 0-100 por resposta; ≥70 avança, <70 refaz |
| Recuperação adaptativa | `server.ts:769` | "Plano de Reforço Customizado" em Markdown |
| Escalonamento humano | `server.ts:768, 795-806` | IA decide `tutorAlertNeeded`; aluno bloqueado até intervenção |
| Certificação | `src/App.tsx:1222-1324` | Diploma imprimível |

Fluxo: **Especialista** cria trilha → **Aluno** faz o loop socrático → **Tutor** monitora dashboard e destrava. Jornada: matrícula → 3 módulos → quiz final de 3 questões geradas a partir das hesitações → certificado.

## 2. Stack

React 19 + TS + Tailwind v4 (frontend monólito `src/App.tsx`, 1.855 linhas) · Express 4 (`server.ts`, 889 linhas) · `@google/genai` · **sem banco** (3 variáveis em memória) · Vite 6 · deploy AI Studio/Cloud Run · config: `GEMINI_API_KEY`.

API REST: 13 rotas (courses/generate, session/start, next-prompt, submit, quiz-submit, alerts, analytics, heartbeat…).

## 3. Estado real

Funcional como demo: trilha gerada por IA (fixa em 3 etapas), avaliação 0-100, plano de reforço, quiz personalizado, dashboard de tutor com auditoria, modo simulação offline bem feito. **Inexistente:** auth, persistência, retomada de sessão, upload de PDF/vídeo, RAG, chat livre (é Q&A dirigido de turno único), testes/CI. **Parcialmente fake:** analytics (`engagementScore = 82 + completed*3`), certificado menciona "blockchain" falsamente.

Bugs/dívidas: model ID `"gemini-3.5-flash"` provavelmente inválido (tudo cai no modo simulação); `JSON.parse` cru sem `responseSchema`; heartbeat 8s contado como 5s (~37% de subestimação de tempo); contagem de falhas mal escopada; botão de debug exposto ao aluno; `App.tsx` insustentável.

## 4. Modelo de dados (`src/types.ts` — a peça mais reaproveitável)

```
Course { id, title, description, materials, pedagogicalGuide, steps[], createdAt }
  └─ CourseStep { id, title, contentSummary, concept }
StudentSession { id, studentName, studentEmail, courseId, courseTitle,
                 currentStepIndex, status, history[], quizAnswers[],
                 evaluationScore?, navigationTime, lastActive,
                 relearningPlan?, tutorResolved? }
  └─ Interaction { id, role, type, text, score?, concept?, timestamp }
TutorAlert { id, sessionId, studentName, ..., reason, lastStudentAnswer, status }
SystemAnalytics { totalStudents, engagementScore, averageAccuracy, ... }
```

- `status: 'learning' | 'relearning' | 'evaluating' | 'completed' | 'tutor_flagged'` — máquina de estados do aluno.
- `Interaction.type: 'concept_intro' | 'question_adaptive' | 'answer' | 'feedback' | 'relearning_plan'` — tipagem semântica que permite auditoria pedagógica.
- `CourseStep.concept` — o conceito a ser validado, critério de aprovação da IA. **Conceito de design mais valioso do projeto.**

Limitações: não há `Student`, `Enrollment`, `Cohort`, `Attempt`, versionamento de curso; cada F5 cria sessão órfã.

## 5. Reaproveitamento para TOC

**Copiar/adaptar:** modelo de domínio (`types.ts`); prompt de decomposição de material (trocar "EXATAMENTE 3" por N); **prompt de avaliação** (score + feedback + alerta + plano — o melhor ativo); prompt de quiz por lacunas; persona injetável (criar preset "Socrático Goldratt/Jonah" — literalmente o método de *A Meta*); loop de escalonamento IA→tutor + dashboard; padrão de fallback sem API key; contrato das 13 rotas.

**Construir do zero:** persistência (item #1); auth/multi-tenant; retomada de sessão; trilhas com N módulos e pré-requisitos; ingestão de material real + RAG; chat livre com streaming; analytics de verdade (mastery por conceito, funil, tempo por conceito); artefatos visuais interativos de TOC (Nuvem, ARA, PRT — o LearnAI só tem chat + MCQ); correções técnicas (model ID, responseSchema, refatoração, testes).

**Veredito:** protótipo demonstrável de ponta a ponta, zero production-ready. **Tratar como fonte de design de prompts e modelo de dados, não como base de código para evoluir.**
