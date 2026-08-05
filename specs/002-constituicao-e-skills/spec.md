# Spec 002 — Constituição do livro, princípio bilíngue e skills do Maestro

> **Raia:** plena (governança) · **Rodada:** 3 · **Branch:** `002-constituicao-e-skills`
> **Decisor:** Gilsiley Darú · **Status:** aguardando gate humano

## Intenção

Ratificar a constituição deste livro — com o **princípio bilíngue (PT+EN) como
não-negociável** — e instalar a metodologia Maestro como skills executáveis no
repositório, para que as regras disparem sozinhas no contexto certo em vez de
depender de memória.

## Escopo

### Entra

1. **Constituição** (`.specify/memory/constitution.md`) com sete princípios específicos
   deste livro, herdando o processo do Maestro. Destaques:
   - **I — É um treino, não uma leitura:** capítulo sem prática com devolutiva está
     *incompleto*, por melhor que esteja escrito.
   - **II — Bilíngue por padrão:** o livro existe sempre em PT e EN; nenhum capítulo é
     dado por pronto sem o par EN; tradução defasada nunca finge ser atual.
   - **V — O tutor treina, não substitui o raciocínio:** guardrails socráticos como
     regra constitucional, não preferência de estilo.
2. **Skills do Maestro** em `.claude/skills/`: `constitution-check`, `dod-verificavel`,
   `combater-amontoado`, `anti-padroes`, `diagnostico-antes-do-fix`.
3. **Comandos e agentes** do Maestro (`.claude/commands/`, `.claude/agents/`).
4. **Registro honesto da dívida** aberta pelos princípios I e II (ver abaixo).

### Não entra

- A tradução EN em si — ver "Dívida declarada".
- Os objetos interativos faltantes — ver "Dívida declarada".

## Dívida declarada (consequência de ratificar I e II)

Ratificar esta constituição coloca o estado atual **fora de conformidade**, de propósito:
a constituição declara o alvo, e a distância vira dívida explícita em vez de ficar
implícita.

| Princípio | Estado atual | Dívida |
|---|---|---|
| **I — treino** | 11 capítulos com "Mão na massa" (texto, sem correção), mas **1 único objeto interativo** (cap. 02) | Faltam objetos interativos em 10 capítulos. O tutor **não tem mecanismo de exercício**: não propõe, não corrige, não acompanha |
| **II — bilíngue** | Livro só em PT; a máquina EN está intacta mas desativada | Faltam as 16 páginas em EN |

### Sequenciamento proposto (e por quê)

A tradução EN **não** vem antes da moderação editorial do conteúdo PT. Traduzir texto
que está prestes a ser reescrito é retrabalho garantido: o autor ainda vai revisar a
primeira versão, e cada capítulo alterado invalidaria sua tradução.

A própria constituição dá o mecanismo para conviver com isso sem mentir ao leitor: o
selo de sincronia por hash. Portanto:

- **Rodada 4** — exercícios (objetos interativos + mecanismo de exercício no tutor), que
  é o Princípio I e o que o autor sinalizou como prioridade de avaliação.
- **Rodada 5** — tradução EN completa, sobre o conteúdo já moderado, com o selo de
  sincronia ligado e verificado no portão de qualidade.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| CA-1 | A constituição existe e declara os sete princípios | arquivo presente, sete seções |
| CA-2 | As skills do Maestro disparam neste repositório | `.claude/skills/*/SKILL.md` presentes |
| CA-3 | O `CLAUDE.md` aponta para a constituição como regra primária | referência presente |
| CA-4 | A dívida está registrada onde é lida | `HISTORICO.md` e esta spec |
| CA-5 | Nada quebrou | build verde, portão verde, testes verdes |
