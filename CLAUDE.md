# CLAUDE.md — instruções para agentes neste repositório

Este repositório é o **handbook vivo de Pesquisa Operacional (PO)**: fundamentação completa do
campo, exercícios que corrigem, vídeos curados, módulos aplicados por domínio e atualização
contínua a partir da literatura científica.

## Regra primária

**Todo trabalho DEVE seguir a [constituição do handbook](.specify/memory/constitution.md)** —
leia-a por inteiro antes de contribuir. Em caso de conflito entre um pedido pontual e a
constituição, o conflito é explicitado ao autor antes de agir.

**Toda rodada segue a metodologia [Maestro](https://github.com/GHDaru/maestro)** — sem
exceção. A especificação é a fonte de verdade, os agentes executam, o humano decide, aprova e
verifica. O ciclo é `specify → clarify → plan → tasks → implement`, uma especificação por
rodada, registrada em `specs/NNN-nome/`.

As skills do Maestro estão em `.claude/skills/` e **comandam, não sugerem** — cada uma tem sua
Lei de Ferro. Antes de agir, verifique se alguma se aplica: `constitution-check` (ao escrever
um plano), `dod-verificavel` (ao escrever critérios de aceite), `combater-amontoado` (ao
revisar texto denso), `anti-padroes` (ao desenhar fluxo ou revisar agente),
`diagnostico-antes-do-fix` (**SEMPRE** antes de corrigir um bug).

Os princípios específicos deste handbook, resumidos:

1. **É um treino, não uma leitura** — mínimo de 3 exercícios e 1 vídeo por capítulo; correção
   no servidor, com devolutiva que explica.
2. **Modelar antes de resolver** — intuição → matemática → código, nessa ordem; todo método
   responde "quando não serve?".
3. **Evidência acima de retórica** — nenhum número sem procedência; nenhuma URL ou DOI
   inventado.
4. **A fonte-base é o experimento executável** — `po-zero`, em CPU, sem licença paga.
5. **Arquitetura em três camadas** — núcleo (estável) + aplicados (cresce por adição) +
   fronteira (expiração obrigatória).
6. **Atualização por Radar** — artigo entra datado em `radar/RADAR.md`, com o que ele muda.
7. **Livro vivo** — datado, versionado, reescrito.
8. **Português canônico**, inglês como dívida declarada.
9. **Sigla nunca nasce nua** — primeira ocorrência por extenso, em todo documento.
10. **Direitos autorais** — texto autoral; material de terceiros não é reproduzido aqui.
11. **DoD verificável** — build verde e testes verdes, com a saída colada.
12. **Nenhum método cai do céu** — todo capítulo de método conta **de onde o método veio**: o
    aperto histórico, o que se fazia antes, a virada, a **ideia reaproveitável** e a origem do
    nome. Este handbook não passa decoreba. História é afirmação e exige fonte (Princípio III);
    **inventar história é pior do que omiti-la**, porque é convincente.

As regras de escrita — método pedagógico, esqueleto de capítulo, sintaxe de exercício e
vídeo — estão no [`livro/GUIA-EDITORIAL.md`](livro/GUIA-EDITORIAL.md). Leia antes de escrever
qualquer conteúdo.

## Restrições

- **Direitos autorais.** Livros-texto de terceiros não são reproduzidos. Materiais de estudo
  do autor ficam fora do versionamento (ver [`materiais/README.md`](materiais/README.md)); as
  obras são citadas na [bibliografia](livro/bibliografia.md).
- **Sem segredos** em arquivo, commit ou texto. Credenciais só em `.env`, fora do
  versionamento.
- **Custo zero** na trilha padrão: solver aberto (HiGHS/CBC) e endpoint gratuito + BYOK no
  tutor.
- **Nenhum identificador interno de modelo de IA** em commit, conteúdo ou artefato publicado.
- **Português** com termos técnicos consagrados sem tradução forçada.

## Mapa do repositório

- `livro/` — o livro. [`mapa-do-handbook.md`](livro/mapa-do-handbook.md) (o sumário declarado,
  com as 77 vagas), `GUIA-EDITORIAL.md` (como escrever), `HISTORICO.md` (edições),
  `bibliografia.md`, `videoteca.md`, `glossario.md`, `capitulos/`, `exercicios.json`.
- `radar/RADAR.md` — o Radar científico: artigos lidos, datados, com o que cada um muda.
- `po-zero/` — a construção prática (Python + PuLP/Pyomo + HiGHS), uma etapa por capítulo de
  método.
- `publicar/` — o motor: Markdown → HTML + PDF. `build.mjs`, `sumario.json` (a estrutura
  declarada), `tema/`, `viz/` (ilhas interativas) e os portões: `verifica-capitulos.mjs`,
  `verifica-exercicios.mjs`, `verifica-referencias.mjs`, `verifica-espelho.mjs`.
- `chat-companion/backend/` — o tutor: FastAPI, RAG sobre o corpus do livro, correção de
  exercícios, gating de capacidades por capítulo (`capabilities.py`).
- `estudos/` — notas de pesquisa que fundamentam decisões editoriais.
- `ROADMAP.md` — o que vem agora, em que ordem e por quê. **Consulte antes de propor trabalho
  novo**: cada item vira uma especificação.
- `specs/` — uma pasta por rodada. `adr/` — Architecture Decision Records.
- `materiais/` — política dos materiais de terceiros (o conteúdo não é versionado).

## Verificação (o que rodar antes de dar por pronto)

```bash
cd publicar && npm run build          # gera o site + roda todos os portões de qualidade
cd chat-companion/backend && python -m pytest -q
```

O merge na `main` é o que publica.

## Notas de arquitetura

- **A estrutura do livro é declarativa.** Adicionar um capítulo = criar o `.md` + adicionar o
  item em `publicar/sumario.json`. Nenhuma mudança de motor é necessária para o livro crescer
  — e é isso que sustenta a camada de módulos aplicados.
- **O gating do tutor espelha os capítulos.** `chat-companion/backend/capabilities.py` é a
  fonte da verdade; `COMPANION_CAPS` em `build.mjs` é um espelho para exibição. Mudou um, mude
  o outro — `verifica-espelho.mjs` barra a divergência.
- **Exercícios vivem no registro editorial** `livro/exercicios.json` e são empacotados para o
  backend por `build_corpus.py`. O site publica o enunciado; o gabarito e a rubrica **nunca**
  são publicados, e há portão que verifica isso.
- **Objetos interativos** são ilhas React em `publicar/viz/`, montadas em
  `<div data-viz="chave">`. Regra: *progressive enhancement* — sem JavaScript, o Markdown em
  volta da ilha mostra o mesmo conteúdo.
- **O motor veio do livro *Engenharia de Harness*** (mesmo autor, licença MIT), via o livro
  *Teoria das Restrições*. Ver [ADR 0001](adr/0001-reuso-motor-livro-vivo.md).
