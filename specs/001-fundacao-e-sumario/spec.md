# Spec 001 — Fundação do handbook e primeira versão do sumário

**Rodada:** 001 · **Raia:** plena · **Branch:** `claude/handbook-pesquisa-operacional-ucbbpu`
· **Data:** 2026-08-06 · **Status:** implementado, aguardando gate humano

## O quê

Transformar um repositório que é hoje um **clone do livro *Teoria das Restrições*** no handbook
vivo de Pesquisa Operacional (PO), e entregar a **primeira versão do sumário** — o mapa completo
do que o handbook pretende cobrir.

## Por quê

O autor precisa de duas coisas antes de escrever qualquer conteúdo:

1. **Um mapa para discutir.** O corpo de conhecimento que ele vai aplicar com os alunos precisa
   ser visto inteiro antes de ser escrito em pedaços. Sumário é decisão editorial, e decisão
   editorial é gate humano.
2. **Uma casa que seja a dele.** Enquanto o repositório carregar o conteúdo de outro livro,
   qualquer capítulo novo entra num sumário que não é o seu, e o motor publica um site com o
   nome errado.

Sem (1), a rodada de Programação Linear (PL) começa sem saber onde termina. Sem (2), ela começa
sobre um repositório que se contradiz.

## Escopo

### Entra

- **Limpeza** de todo o conteúdo herdado: capítulos, especificações, registros de decisão,
  estudos e objeto interativo do livro anterior.
- **Governança própria**: constituição do handbook, instruções para agentes, README, roadmap.
- **Pesquisa** do corpo de conhecimento de PO, com fontes citadas, registrada em `estudos/`.
- **O mapa do handbook** — o sumário declarado, com todas as vagas, organizado em camadas.
- **Aparato editorial**: guia editorial, bibliografia, videoteca, glossário, banco de
  exercícios, histórico.
- **O Radar científico** — o mecanismo de atualização contínua.
- **Política de materiais de terceiros** e o esqueleto do `po-zero`.
- **Religação do motor** ao novo conteúdo, com todos os portões verdes.

### Não entra

- **Nenhum capítulo de método.** A Parte II (Programação Linear) é a rodada seguinte.
- **Nenhuma etapa do `po-zero`** além do contrato e da decisão de pilha.
- **O par em inglês** (dívida declarada — ADR 0002).
- **O mapeamento dos livros-base**, que depende de o autor anexá-los.

## Decisões do autor nesta rodada

Três decisões foram tomadas pelo autor antes da implementação e estão registradas como ADR:

| Decisão | Escolha | ADR |
|---|---|---|
| Herança do livro anterior | Remover todo o conteúdo já nesta rodada, reaproveitando o motor | 0001 |
| Bilinguismo | Português canônico; inglês vira dívida declarada | 0002 |
| Pilha do `po-zero` | Python + PuLP/Pyomo + HiGHS, custo zero | 0003 |

## Critérios de aceite

Cada critério é verificável por máquina ou por inspeção objetiva — sem julgamento de qualidade.

| # | Critério | Como verificar |
|---|---|---|
| A1 | Nenhum arquivo de conteúdo do livro anterior permanece | `git ls-files livro/capitulos` vazio; nenhuma ocorrência do título anterior fora do `HISTORICO.md` e dos ADRs |
| A2 | O mapa do handbook existe e declara todas as partes e vagas | `livro/mapa-do-handbook.md` presente, com as onze partes e as três camadas |
| A3 | O mapa é navegável no site publicado | Página gerada em `docs/` e alcançável pelo sumário |
| A4 | A pesquisa está registrada com fontes | `estudos/001-corpo-de-conhecimento-po.md` com seção de fontes e ao menos uma lacuna declarada |
| A5 | A constituição é do handbook, não do livro anterior | `.specify/memory/constitution.md` versão 1.0.0, com os princípios de PO |
| A6 | O Radar existe e define o mecanismo | `radar/RADAR.md` com vereditos, cadência e registro |
| A7 | A política de materiais de terceiros é explícita | `materiais/README.md`; `materiais/` ignorado pelo Git exceto o README |
| A8 | **O build passa inteiro** | `cd publicar && npm run build` sai 0, com todos os portões verdes |
| A9 | Os testes do backend passam | `cd chat-companion/backend && python -m pytest -q` sai 0 |
| A10 | Nenhuma sigla nasce nua nos documentos novos | Inspeção: primeira ocorrência por extenso em cada documento |
| A11 | Nenhum identificador interno de modelo de IA vaza para artefato publicado | Busca por padrão de identificador nos arquivos versionados |

## Riscos

| Risco | Mitigação |
|---|---|
| O motor tem acoplamentos ao conteúdo anterior que só aparecem no build | Os portões são executados; cada acoplamento encontrado vira correção nesta rodada e é registrado no ADR 0001 |
| O portão de exercícios exige registro não vazio, e não há capítulo para exercitar | O portão passa a aceitar registro vazio **apenas** enquanto o sumário não declarar capítulo numerado além da abertura — a condição se auto-restaura |
| Um mapa de 77 vagas cria expectativa de prazo | O próprio mapa declara que vaga não é promessa de prazo |

## Fora de escopo, registrado para depois

- Inventário de cobertura de vídeo por capítulo (rodada de PL).
- Revisão sistemática de metaheurísticas com protocolo (rodada da Parte V).
- Correspondência com os livros-base (quando anexados).
