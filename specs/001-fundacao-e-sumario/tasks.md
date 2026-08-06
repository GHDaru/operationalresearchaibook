# Tasks 001 — Fundação do handbook e primeira versão do sumário

**Especificação:** [`spec.md`](spec.md) · **Plano:** [`plan.md`](plan.md) · **Data:** 2026-08-06

## Bloco 1 — Limpeza

- [x] T1.1 Remover os capítulos herdados (`livro/capitulos/*.md`), preservando o diretório —
  dois portões varrem essa pasta e quebrariam se ela sumisse.
- [x] T1.2 Remover as especificações e os registros de decisão do livro anterior.
- [x] T1.3 Remover os estudos do livro anterior.
- [x] T1.4 Remover a ilha interativa do livro anterior e esvaziar o registro de componentes.
- [x] T1.5 Zerar o registro de exercícios e a cópia empacotada no backend.

## Bloco 2 — Pesquisa e decisões

- [x] T2.1 Pesquisar como o campo se organiza (livros-texto de referência, literatura recente,
  material em vídeo em português) e registrar em `estudos/001-corpo-de-conhecimento-po.md`,
  com fontes e lacunas declaradas.
- [x] T2.2 ADR 0001 — reúso do motor de livro vivo.
- [x] T2.3 ADR 0002 — português canônico, inglês como dívida declarada.
- [x] T2.4 ADR 0003 — pilha do `po-zero` (Python + PuLP/Pyomo + HiGHS).
- [x] T2.5 ADR 0004 — arquitetura do sumário em três camadas.

## Bloco 3 — Conteúdo e aparato

- [x] T3.1 **`livro/mapa-do-handbook.md`** — o entregável central: as vagas declaradas, em onze
  partes e três camadas, com o que cada capítulo trata.
- [x] T3.2 Reescrever `livro/00-introducao.md` para o handbook.
- [x] T3.3 Reescrever o Guia Editorial, com o esqueleto de capítulo obrigatório e as regras de
  exercício e de vídeo.
- [x] T3.4 Reescrever a bibliografia, com o estado de verificação por fonte e o espaço
  reservado aos livros-base.
- [x] T3.5 Criar a videoteca, com a política de curadoria e o registro da autorização de uso
  dos vídeos do canal de João Sarubbi (CEFET-MG).
- [x] T3.6 Reescrever o glossário (siglas e termos de Pesquisa Operacional).
- [x] T3.7 Criar o Banco de Exercícios (sintaxe do registro e os portões que ele atravessa).
- [x] T3.8 Reescrever o histórico, com a edição 0.1 e as dívidas declaradas.
- [x] T3.9 Criar `radar/RADAR.md` — o mecanismo de atualização científica.
- [x] T3.10 Criar `po-zero/README.md` — pilha, contrato de etapa e a regra das duas
  implementações.
- [x] T3.11 Criar `materiais/README.md` e a regra no `.gitignore`.

## Bloco 4 — Governança

- [x] T4.1 Reescrever a constituição para o handbook (versão 1.0.0, onze princípios).
- [x] T4.2 Reescrever `CLAUDE.md`, tornando a metodologia Maestro obrigatória em toda rodada.
- [x] T4.3 Reescrever o `README.md`.
- [x] T4.4 Criar o `ROADMAP.md`, com a ordem de ataque das rodadas.

## Bloco 5 — Religação do motor

- [x] T5.1 `publicar/sumario.json` — abertura + aparato do handbook.
- [x] T5.2 Renomear os artefatos consolidados de download e o pacote do motor.
- [x] T5.3 Trocar o mapa de siglas pelo de Pesquisa Operacional, espelhando o glossário.
- [x] T5.4 Reduzir o registro de capacidades do tutor ao que o handbook oferece hoje, nos dois
  lados do espelho (backend e motor).
- [x] T5.5 Reescrever o vocabulário do grafo de conhecimento (conceitos de PO e etapas do
  `po-zero`) — sem isso, os capítulos futuros seriam ligados a conceitos de outro livro.
- [x] T5.6 Substituir a contagem fixa de capítulos do portão do grafo por **invariantes**:
  todo nó publicado aparece em alguma aresta, e nenhum nó de capítulo existe fora do sumário.
- [x] T5.7 Tornar a exigência de registro de exercícios não vazio **condicional ao sumário** —
  a condição se auto-restaura quando o primeiro capítulo numerado for publicado.
- [x] T5.8 Reescrever a persona do tutor para treinar modelagem.
- [x] T5.9 Regenerar o corpus do tutor a partir do novo texto.
- [x] T5.10 Redesenhar capa e favicon (região viável e vértice ótimo, no lugar da corrente).
- [x] T5.11 Desacoplar os testes de mecanismo do conteúdo editorial, semeando um exercício
  sintético — a causa raiz de 3 das 6 falhas encontradas.
- [x] T5.12 Corrigir as referências remanescentes ao livro anterior (origens permitidas,
  título da API, assunto de e-mail) e os links relativos quebrados.

## Bloco 6 — Verificação

- [x] T6.1 `cd publicar && npm run build` verde, com todos os portões.
- [x] T6.2 `cd chat-companion/backend && python -m pytest -q` verde.
- [x] T6.3 Verificação de links relativos em todo o Markdown do repositório.
- [ ] T6.4 **Revisão por agente em contexto fresco** — gate humano, cabe ao autor acionar
  antes do merge (Maestro, Princípio II: quem executa não verifica).
- [ ] T6.5 **Aprovação do autor** ao mapa do handbook — é decisão editorial, não delegável.

## O que ficou fora, e onde está registrado

| Item | Onde |
|---|---|
| Capítulos da Parte II (Programação Linear) | Rodada 002, no [roadmap](../../ROADMAP.md) |
| Etapas do `po-zero` | Rodada 002 |
| Par em inglês | Dívida declarada no histórico (ADR 0002) |
| Correspondência com os livros-base | Aguardando o autor anexar as obras |
| Inventário de cobertura de vídeo por capítulo | Rodada 002 |
