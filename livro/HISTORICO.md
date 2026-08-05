# Histórico

> **Conteúdo revisado em 2026-08** · edições, datas e o que mudou a cada rodada.

Este livro é vivo: não tem versão final. Cada edição registra o que mudou, quando, e com apoio de qual modelo de IA — em coerência com a nota de autoria da [Introdução](00-introducao.md).

> **Sobre os números de capítulo abaixo.** As edições 0.1 a 0.6 foram escritas antes da renumeração feita na edição 0.7 (entrada do Módulo 0). Os capítulos citados nelas seguem a **numeração da época** — o que era o capítulo 02 hoje é o 06, e assim por diante, com deslocamento de quatro a partir do antigo 01. Registro datado não se reescreve; esta nota existe para que ele não engane quem lê hoje.

### Edição 0.1 — 2026-08-01 · Estrutura inaugural e Módulo 1

Primeira publicação. O livro nasce com a máquina completa (motor de publicação, tema, ilhas interativas, chat companion) reaproveitada do livro *Engenharia de Harness*, e com uma primeira proposição de conteúdo para moderação editorial.

**Entrou:**

- **Abertura** — capítulos 00 (Introdução) e 01 (Por que ferramentas de raciocínio), este último com a fundamentação cognitiva em Kahneman.
- **Módulo 1 — Fundamentos lógicos**, com conteúdo substantivo: 02 (Causa e Efeito), 03 (Pré-Requisito), 04 (Premissas) e 05 (Cadeias Lógicas). É a prioridade editorial declarada: exercitar a lógica antes das ferramentas.
- **Módulo 2 — Conflitos**, em primeira versão: 06 (A Nuvem) e 07 (Conflitos Recorrentes).
- **Módulo 3 — Solução e implementação**, em primeira versão: 08 (Injeções), 09 (Análise de Pré-Requisitos) e 10 (Aplicação Integrada).
- **Primeiro objeto interativo** — o exercício "Que conexão é esta?", no capítulo 02, que pede ao leitor classificar afirmações entre causa e efeito e pré-requisito, com devolutiva imediata.
- **Aparato** — glossário, bibliografia com as fontes primárias, guia editorial e este histórico.

**Pendente para as próximas edições:**

- Aprofundamento dos módulos 2 e 3 com o material do autor.
- Objetos interativos para a Nuvem, o loop e a Análise de Pré-Requisitos.
- Backend em operação (banco e chat tutor), com a trilha de capacidades por módulo.
- Módulos avançados: os cinco passos de focalização, contabilidade de ganhos, gestão de projetos por corrente crítica.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e responsabilidade editorial humanas.

### Edição 0.2 — 2026-08-01 · Constituição e princípio bilíngue

Ratificação da constituição do livro e instalação da metodologia Maestro como skills executáveis no repositório.

**Entrou:**

- **Constituição** (`.specify/memory/constitution.md`) com sete princípios, entre eles: *é um treino, não uma leitura* (I), *bilíngue por padrão* (II) e *o tutor treina, não substitui o raciocínio* (V).
- **Skills, comandos e agentes do Maestro** em `.claude/`, para que as regras de processo disparem sozinhas no contexto certo.

**Dívida declarada.** Ratificar os princípios I e II coloca o estado atual deliberadamente fora de conformidade — a constituição declara o alvo, e a distância vira dívida explícita:

- **Princípio I (treino):** há 1 objeto interativo em 11 capítulos, e o tutor ainda não tem mecanismo de exercício — não propõe, não corrige, não registra.
- **Princípio II (bilíngue):** o livro está só em português. A máquina EN permanece intacta, desativada.

A tradução EN vem **depois** da moderação editorial do conteúdo: traduzir texto prestes a ser reescrito é retrabalho garantido. O selo de sincronia por hash existe justamente para conviver com essa defasagem sem enganar o leitor.

### Edição 0.3 — 2026-08-01 · O livro no ar

Primeira publicação real. O site passou a ser servido pelo Vercel em
<https://theoryofconstraintlivebook.vercel.app/>.

**Entrou:**

- **Publicação no Vercel** (ADR 0002). O deploy pelo GitHub Pages falhou: o repositório é privado, e Pages em repositório privado exige plano pago. O Vercel publica repositório privado no plano gratuito, mantendo o material de trabalho fora do ar.
- **PDFs opcionais por ambiente.** O build do Vercel não tem Chromium; em vez de deixar links de download apontando para arquivos inexistentes, os PDFs e seus links passaram a ser condicionais.
- **Widget do tutor condicional.** Enquanto não houver backend configurado, o botão de chat não aparece — um chat que não responde é pior do que nenhum chat.
- **Runbook de infraestrutura** (`docs/infra/runbook-deploy.md`) e o **estudo do protocolo de exercícios via chat** (`estudos/003-protocolo-aph-para-exercicios.md`), que desenha a próxima rodada.

**Pendente:** o tutor entra no ar quando o banco (Neon) e o backend (Railway) forem provisionados — a última linha é preencher a URL no sumário.

### Edição 0.4 — 2026-08-01 · O tutor no ar

O tutor entrou em operação. Banco no Neon, backend no Railway, site no Vercel — os três serviços ligados.

**Entrou:**

- **Tutor ativo em todas as páginas**, com a trilha progressiva funcionando: na abertura só o tutor e a busca no livro estão disponíveis; a Nuvem libera no capítulo 06; as injeções, no 08.
- **Verificação em produção**: o tutor responde perguntas factuais citando o trecho e a fonte do livro, e **recusa resolver exercícios** — o guardrail socrático do Princípio V, confirmado com um pedido explícito de resposta pronta.

**Correção nesta edição.** O banner de consentimento nunca aparecia para leitores novos, e a telemetria de navegação nunca disparava. Causa raiz: dentro de `montarBanner()`, uma variável local `tx` sombreava a função `tx(pt, en)` do escopo acima — como `var` é içado, a chamada da linha seguinte encontrava um elemento DOM no lugar da função e lançava erro. O defeito veio junto do motor herdado e existe também no livro de origem.

### Edição 0.5 — 2026-08-01 · Exercícios via chat

A maior lacuna do livro fechada: o Princípio I exige prática com devolutiva em todo capítulo, e havia um objeto interativo em onze.

**Entrou:**

- **Nove exercícios**, um por capítulo do 02 ao 10, derivados dos "Mão na massa". Cada um traz enunciado e uma **rubrica de critérios** — e a rubrica fica no servidor: o leitor não lê por quais critérios será avaliado.
- **Cartão de exercício** no corpo do capítulo, com o botão "Praticar no tutor". Sem JavaScript, o enunciado continua legível; só o botão some.
- **O livro entrega o exercício ao tutor.** A página declara apenas o identificador; o servidor resolve enunciado e critérios e os injeta como **mensagem de sistema própria**, separada da persona e do texto do leitor. O enunciado nunca viaja do cliente.
- **Registro da tentativa.** O tutor avalia contra os critérios e registra o veredito (aprovado, parcial ou refazer) no Postgres. O registro é ao mesmo tempo o progresso do leitor e o traço da ação — neste produto os dois coincidem.
- **Selo de progresso** no cartão, alimentado pelo que já foi registrado.
- Guardas que ficam fora do alcance do modelo: a sessão vem do contexto do turno, e a tentativa só pode ser registrada para o exercício que a **página** declarou.
- **ADR 0003** registra a dívida de o capítulo vir do cliente, com as condições que a fazem expirar.

**Verificação:** 24 testes verdes, incluindo os dez critérios de aceite da spec; fluxo exercitado em navegador do cartão ao envio; e o build falha se um capítulo referenciar exercício inexistente.

### Edição 0.6 — 2026-08-01 · Sincronia com o Maestro, e um portão que mede o fato

**Entrou:**

- **`scripts/sync-maestro.sh`** — ressincronia das skills, comandos e agentes do Maestro numa linha, com modo `--check` que acusa divergência e sai com erro. A constituição declara o Maestro instalado; cópia manual apodrece em silêncio.
- **Skills atualizadas**: `anti-padroes` ganhou o anti-padrão 13 (*"check que mede o proxy, não o fato"*) e `dod-verificavel` ganhou a segunda lei (*"um check que você nunca viu acusar não é um check — é uma esperança"*).
- **`publicar/verifica-espelho.mjs`** — portão que compara o espelho de capacidades do widget com a fonte da verdade no backend, e falha o build se divergirem.

**A lei nova pagou na hora.** O check que confirmava o widget na página era `grep "companion.js"` — casa com o texto, não com o artefato. Trocado por um que lê a configuração injetada, revelou que a capacidade "Exercícios" tinha sido adicionada ao backend e **esquecida no espelho** do widget: os chips do tutor não a mostravam. A correção não foi só regenerar o espelho, foi criar o portão que impede a divergência de voltar — e ele foi provado falhando antes de ser aceito.

**Baterias de exercícios.** Cada capítulo numerado passou de um exercício para uma **bateria de quatro** (duas no capstone): **34 exercícios** no total. O desenho veio da engenharia reversa das séries do curso BBIT — não do conteúdo, que é autoral, mas da arquitetura: a letra da variante troca uma variável por vez (declarado → implícito com distrator → defeituoso → seu contexto), o aviso de erro nasce no gabarito de uma variante e migra para o enunciado da seguinte, e uma espinha de cinco cenários atravessa o livro, com o produto de um exercício virando o insumo do próximo — a injeção da bateria do capítulo 08 é o objetivo da bateria do 09.

A variante **"achar o erro"** preenche uma lacuna do material de origem: o BBIT tem catálogos de erros comuns com pares errado/certo, mas nunca os transformou em exercício. Aqui o leitor recebe um raciocínio pronto e defeituoso e precisa dizer **qual teste ele falha e por quê**.

A rubrica — critérios, mecanismo do erro provável e resposta-guia — fica no servidor e **nunca é publicada**: o leitor não deve poder ler por quais critérios será avaliado antes de responder.

### Edição 0.7 — 2026-08-01 · Módulo 0: o livro passa a merecer o próprio nome

O autor, no papel de leitor-auditor, apontou: *"para TOC, senti que está fraco; este está excelente para o processo de raciocínio — não o perca"*. A medição no código confirmou a intuição de forma constrangedora: num livro chamado *Teoria das Restrições*, a palavra "restrição" aparecia **duas vezes** e nunca era definida. Cinco passos de focalização: zero. Ótimo local × ganho global: zero. A capa trazia uma corrente com o elo restritivo em âmbar, e o livro nunca explicava esse elo.

O que existia era um treinamento nos **Processos de Raciocínio** — um ramo da TOC — sem a teoria que lhes dá propósito.

**Entrou — Módulo 0, "A restrição"**, quatro capítulos novos:

- **01 O sistema e a restrição** — o que é sistema, por que a corrente e não a pilha, por que sempre existe uma restrição, os três tipos (física, de mercado, de política), e o achado que sustenta o livro: *a maior parte do sistema não é a restrição*.
- **02 O ótimo local que destrói o todo** — por que otimizar cada parte piora o conjunto, e por que gente competente e de boa-fé faz isso o tempo todo.
- **03 Os cinco passos de focalização** — identificar, explorar, subordinar, elevar, voltar sem deixar a inércia virar a restrição. Subordinar é o passo mais difícil e o mais pulado.
- **04 As três perguntas da mudança** — *o que mudar? para o que mudar? como causar a mudança?*

**O reposicionamento é o coração da edição.** Nada do conteúdo anterior se perdeu; ele mudou de papel. Os módulos 2, 3 e 4 deixaram de ser "o livro" e passaram a ser, um a um, **as respostas às três perguntas** do Módulo 0 — a Nuvem responde *o que mudar*, as injeções respondem *para o que mudar*, a Análise de Pré-Requisitos responde *como causar a mudança*. As ferramentas passaram a ter endereço, e o Módulo 1 (fundamentos lógicos) passou a ser a gramática comum das três.

O livro inteiro foi **renumerado** para abrir espaço: 15 capítulos em cinco módulos, com remapeamento de arquivos (via `git mv`, preservando histórico), títulos, ~40 referências cruzadas na prosa, ids e séries dos 34 exercícios existentes, marcadores de bateria, gating do tutor e espelho de capacidades. A introdução foi reescrita para abrir pela restrição e anunciar as três perguntas.

**Exercícios:** 4 baterias novas, **16 exercícios** — total de **50 em 13 baterias**. Elas exploram os erros que o próprio conceito convida: confundir restrição com gargalo, tratar a restrição como defeito a extirpar, confundir estar ocupado com produzir, pular *explorar* direto para *elevar*, e a subordinação de fachada — o acordo verbal que não muda regra nenhuma.

**Glossário:** 11 verbetes novos (restrição, gargalo, sistema, ótimo local, eficiência local, capacidade de proteção, explorar, subordinar, elevar, cinco passos, três perguntas) — de 17 para 28.

**Novo portão — `publicar/verifica-exercicios.mjs`.** O registro de exercícios é editorial, escrito à mão, e o motor só barrava uma coisa: bateria declarada e vazia. Exercício órfão, `capacidade` inexistente, capacidade que só libera num capítulo posterior ao do exercício, variante sem resposta-guia e **rubrica vazando para o site publicado** passavam calados. Pela segunda lei da DoD, o portão foi provado falhando em cada um dos oito casos antes de ser aceito.

**Dívida declarada.** O par em inglês continua em aberto (Princípio II) — deliberadamente, até a moderação editorial estabilizar o texto. Os capítulos 00 e 05 seguem sem bateria. O módulo de **operações** (Tambor-Pulmão-Corda, gestão de pulmões, contabilidade de ganhos) fica registrado como próxima fronteira: é o que fecha a TOC como corpo.

**A rodada não passou de primeira, e isso está registrado.** A revisão em contexto fresco — que a constituição exige justamente porque quem executa não enxerga o próprio ponto cego — encontrou **quatro referências de capítulo quebradas em conteúdo publicado**: `capítulos 06–05` na leitura executiva da introdução, `capítulos 10 e 08` na bibliografia e `(caps. 08 e 08)` na rubrica do exercício final do livro. A causa foi exata: a renumeração casou apenas números precedidos da palavra-chave ("capítulo NN"), de modo que o **segundo número de toda referência composta** nunca foi visto. O portão que deveria ter pego isso validava **links**; estas são **prosa**. Corrigidas, e o modo de falha virou `publicar/verifica-referencias.mjs` — provado restaurando os quatro defeitos e vendo o portão acusar os cinco.

A mesma revisão provou um **falso-negativo** na varredura de vazamento de rubrica: ela comparava o texto cru do registro com o HTML escapado da página, e 18% dos campos têm aspas no início — para todos eles, um vazamento real passaria com o portão dizendo "não publicada". Corrigido, e o comprimento do trecho procurado passou a ser calibrado por medição contra o corpus, não por gosto.

**Também vindo da revisão:** o glossário contradizia o capítulo na definição de gargalo; a frase "uma hora perdida…" era atribuída a *A Meta* com o termo trocado (o original fala em **gargalo**, não em restrição — a generalização agora é sinalizada); "diga-me como você me mede" estava sem fonte; ganho, inventário e despesa operacional eram usados como vocabulário obrigatório de exercício sem estarem definidos. A rubrica de `cap01.exC` reprovava a leitura de restrição de política que o próprio capítulo 01 planta — agora aceita as duas, desde que com mecanismo. E `cap02.exC` mandava aceitar que a restrição roda a 71%; agora **exige** que o leitor explique por quê, que é a melhor pergunta do exercício.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e responsabilidade editorial humanas.
