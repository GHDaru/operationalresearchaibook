# Anexo E — Ficha de pesquisa: formato de curso digital com tutor de IA

> Relatório de agente curador-pesquisa, captura 2026-07-31. Método: busca web + leitura crítica; força da evidência marcada por achado (forte = RCT/meta-análise revisada por pares; média = estudo observacional em escala ou relato institucional; fraca = marketing de fornecedor/blog).

**Pergunta-mãe:** que formato de curso online, com chat de IA e monitoramento de aprendizagem por IA, o estado da arte 2024–2026 recomenda para adultos profissionais (gestores/empreendedores) aprendendo Teoria das Restrições?

---

## Q1. Formatos que funcionam para adultos profissionais

1. **Self-paced puro tem conclusão baixíssima; coorte tem conclusão alta — mas o contraste vem majoritariamente de fornecedores.** Mercado repete 3–15% (self-paced) vs. 70–96% (coorte): [FourthRev](https://fourthrev.com/cohort-based-vs-self-paced-learning-which-model-works-better-for-career-changers/), [Kajabi](https://www.kajabi.com/blog/self-paced-vs-cohort-based-courses), [Xperiencify](https://xperiencify.com/cohort-based-courses/), [DigitalDefynd](https://digitaldefynd.com/IQ/cohorts-vs-self-paced-learning/). Números de coorte são enviesados (evidência fraca); a base baixa do self-paced é corroborada por "The MOOC Pivot" (Reich & Ruipérez-Valiente, *Science* 2019, ~3%): https://www.science.org/doi/10.1126/science.aav7958. Mecanismo causal plausível: prazo + accountability social. Nota: ~65% dos adultos preferem a autonomia do self-paced.

2. **Microlearning tem efeito positivo real sobre retenção (evidência forte).** Meta-análise 2024/2025: OR = 1,87 para retenção e d = 0,74 para resultados ([MATHEMA](https://publikasi.teknokrat.ac.id/index.php/jurnalmathema/article/view/517); [ResearchGate](https://www.researchgate.net/publication/394265408_Microlearning_Effectiveness_in_Higher_Education_A_Systematic_Review_and_Meta-Analysis_of_Student_Retention_and_Learning_Outcomes)). Meta-análise em profissionais de saúde (17 estudos): ganho de conhecimento, confiança, retenção mais longa ([eLearning Industry](https://elearningindustry.com/microlearning-statistics-facts-and-trends); [ERIC EJ1423546](https://files.eric.ed.gov/fulltext/EJ1423546.pdf)). Mecanismo: prática distribuída + retrieval practice.

3. **Learning-by-doing tem a evidência causal mais sólida ("doer effect").** Koedinger (CMU/OLI): fazer exercícios formativos intercalados tem efeito ~6x maior que ler/assistir, com replicação causal em escala ([ACM LAK 2023](https://dl.acm.org/doi/pdf/10.1145/3576050.3576103); [replicação](https://www.researchgate.net/publication/353463711_The_Doer_Effect_Replicating_Findings_that_Doing_Causes_Learning)). Prática formativa **gerada por IA** em "textbooks transformados em courseware" mantém o efeito ([ACM L@S 2025](https://dl.acm.org/doi/10.1145/3698205.3733919)). Valida o formato "livro vivo interativo com prática embutida".

**Implicação TOC:** núcleo em unidades curtas com prática intercalada — exercícios de identificação de restrição, árvores, simulações de fluxo (jogo dos dados de *A Meta* digitalizado). Antídoto ao abandono: prazos, accountability e tutor proativo, não necessariamente coorte síncrona.

## Q2. Tutoria por IA

1. **RCT Harvard (Kestin et al., *Scientific Reports* 2025):** N=194, física; tutor de IA com scaffolding e guardrails → **mais do que o dobro de aprendizagem em menos tempo** vs. aula ativa (medianas 4,5 vs. 2,75) ([Nature](https://www.nature.com/articles/s41598-025-97652-6); [Harvard Gazette](https://news.harvard.edu/gazette/story/2024/09/professor-tailored-ai-tutor-to-physics-course-engagement-doubled/); [Hechinger](https://hechingerreport.org/proof-points-ai-tutor-harvard-physics/)). Ressalva: 2 aulas, tutor cuidadosamente desenhado.

2. **RCT Nigéria/Banco Mundial (2024):** 800 alunos, 6 semanas, GPT-4 + orientação docente → 0,31 DP, "melhor que 80% dos programas já testados" ([World Bank](https://blogs.worldbank.org/en/education/From-chalkboards-to-chatbots-in-Nigeria); [ICTworks](https://www.ictworks.org/genai-advance-learning-outcomes/)).

3. **Contra-evidência crucial — IA sem guardrails PREJUDICA (Bastani et al., *PNAS* 2025):** ~1.000 alunos; ChatGPT "cru" virou muleta — retirado, desempenho **caiu 17%**; a versão com guardrails (dicas, não respostas) eliminou o dano ([PNAS](https://www.pnas.org/doi/10.1073/pnas.2422633122); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486); [Wharton](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education/)). **O valor do tutor está no design pedagógico, não no LLM.**

4. **Socrático + scaffolding > resposta direta (evidência convergente, jovem):** [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0360131525002623); [CHI 2026 Scaffolding Cards](https://dl.acm.org/doi/10.1145/3772318.3791696); [arXiv](https://arxiv.org/pdf/2606.15766). Padrão emergente: híbrido (factual direto, conceitual socratizado).

5. **Khanmigo (estudo interno, não revisado por pares):** ≥30 min/semana → +22% proficiência vs. +9% sem IA ([Khan Academy](https://blog.khanacademy.org/khan-academy-efficacy-results-november-2024/)); estudo independente menor sem diferença quantitativa ([ERIC EJ1487444](https://eric.ed.gov/?id=EJ1487444)). Autosseleção como confundidor; sugestivo.

**Implicação TOC:** tutor com persona "Jonah" (perguntas socráticas são o método do Goldratt — alinhamento raro entre pedagogia e conteúdo). Regras: nunca resolver o exercício; dica em camadas; direto apenas no factual; guardrails anti-muleta.

## Q3. Monitoramento de aprendizagem por IA

1. **Sinais a coletar:** (a) interações de chat classificadas — pedido de resposta pronta vs. engajamento genuíno, off-topic, dúvidas recorrentes ([RECIPE4U, arXiv 2410.15025](https://arxiv.org/abs/2410.15025); [análise de prompts, arXiv 2405.19691](https://arxiv.org/pdf/2405.19691)); (b) prática formativa — acerto/erro por conceito, tentativas, tempo; (c) ritmo — inatividade, atraso.
2. **Dashboards:** revisão sistemática 2025 ([MDPI](https://www.mdpi.com/2076-3417/15/15/8679)) — engajamento, feedback automatizado, detecção de risco; pipelines simples (prompt engineering + classificadores). Tendência: dashboard conversacional ([VizChat](https://link.springer.com/chapter/10.1007/978-3-031-64299-9_13); [arXiv 2411.15597](https://arxiv.org/pdf/2411.15597)).
3. **Detecção de aluno em dificuldade:** early-warning consolidado ([JLA](https://learning-analytics.info/index.php/JLA/article/view/8735)); Uplimit opera agentes de nudge/escalonamento ([VentureBeat](https://venturebeat.com/ai/uplimit-raises-stakes-in-corporate-learning-with-suite-of-ai-agents-that-can-train-1000-employees-simultaneously); [Forbes](https://www.forbes.com/sites/jeannemeister/2024/07/23/how-uplimit-harnesses-ai-to-drive-an-enterprise-learning-revolution/)).

Incerteza: sem RCT de que dashboard melhora resultado final. Privacidade: analisar chats exige consentimento explícito (LGPD).

**Implicação TOC:** começar simples — (1) mastery por conceito via quizzes; (2) classificador de chat com 3–4 rótulos (dúvida genuína / muleta / off-topic / frustração); (3) alerta de inatividade com nudge e escalonamento. Dashboard conversacional é fase 2.

## Q4. Frameworks pedagógicos combinados

- **Backward Design** (Wiggins & McTighe): evidência de domínio primeiro — "o aluno aplica as ferramentas ao próprio negócio".
- **4C/ID** (van Merriënboer): tarefas-íntegras de complexidade crescente, scaffolding decrescente ([Frontiers 2025](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1631375/full); [caso blended](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12700520/)). O tutor É o scaffolding que se retira.
- **Diátaxis**: tutorial / how-to / referência / explicação ([diataxis.fr](https://diataxis.fr/); [Canonical](https://ubuntu.com/blog/diataxis-a-new-foundation-for-canonical-documentation)). Referência + explicação viram a base RAG; chat responde direto da referência, socratiza nos tutoriais.
- **Mastery + carga cognitiva**: "IA resolve o 2-sigma de Bloom" é hipótese motivadora, não fato ([Bloom's 2 sigma](https://en.wikipedia.org/wiki/Bloom%27s_2_sigma_problem); [Getting Smart](https://www.gettingsmart.com/2025/11/25/can-tutoring-and-technology-finally-solve-blooms-two-sigma-problem/)); o RCT de Harvard operacionalizou carga cognitiva no tutor.

**Síntese:** Backward Design define *o quê medir* → 4C/ID a *sequência* → Diátaxis a *arquitetura do conteúdo* (e o RAG) → mastery + doer effect o *gate de progressão* → carga cognitiva + PNAS o *comportamento do tutor*. É a mesma combinação constitucionalizada no harness_engineering — reuso direto do método editorial.

## Q5. Benchmarks de plataformas

| Plataforma | O que copiar | Fonte |
|---|---|---|
| Khan Academy / Khanmigo | Gate de mastery; regra "guia, não responde"; relatórios por habilidade | [blog](https://blog.khanacademy.org/khan-academy-efficacy-results-november-2024/) |
| Coursera Coach | IA como companion onipresente no conteúdo (não aba separada); encorajamento | [investor](https://investor.coursera.com/news/news-details/2025/Coursera-Coach-Wins-Newsweek-AI-Impact-Award/default.aspx) |
| Uplimit | Coorte-leve + agentes de nudge; **role-play com IA** (ex.: negociar com sócio cético sobre a restrição) | [Forbes](https://www.forbes.com/sites/jeannemeister/2024/07/23/how-uplimit-harnesses-ai-to-drive-an-enterprise-learning-revolution/) |
| Maven | Accountability: kickoff, entregas semanais, demo day | [maven.com](https://maven.com/courses) |
| Brilliant.org | Gramática da lição: manipular → errar barato → feedback imediato → conceito emerge | [why-brilliant](https://brilliant.org/help/why-brilliant/) |

Números de conclusão/satisfação dessas plataformas são autorreportados (fraca); copiar os **padrões de design**, que convergem com Q1–Q2.

## Recomendação fundamentada (formato híbrido)

**"Livro vivo interativo self-paced com tutor de IA socrático + camada de coorte leve":**

1. **Núcleo:** livro vivo em PT, microlearning com prática intercalada (doer effect ~6x; d = 0,74; padrão Brilliant). Diátaxis; mastery gate; sequência 4C/ID culminando em "aplique TOC ao seu negócio" (Backward Design).
2. **Tutor "Jonah":** socrático com guardrails, nunca muleta — a variável que separa dobrar a aprendizagem (Harvard) de reduzi-la 17% (PNAS). Factual → direto com fonte (RAG); conceitual → dicas em camadas com scaffolding decrescente.
3. **Anti-abandono:** janelas de coorte com prazos, encontro/fórum leve, agentes de nudge + dashboard com detecção de risco. Métricas desde o dia 1: conclusão por coorte, mastery por conceito, pré/pós-teste de aplicação.

**Incertezas declaradas:** (a) sem RCT de curso completo profissional com tutor LLM; (b) números de coorte são marketing; (c) socrático-vs-direto em adultos ocupados ainda jovem — instrumentar o próprio curso para testar (A/B da política do tutor).
