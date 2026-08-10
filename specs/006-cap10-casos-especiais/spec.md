# Spec 006 — Capítulo 10: Casos especiais e degenerescência

**Rodada:** 006 · **Raia:** plena · **Branch:** `claude/handbook-pesquisa-operacional-ucbbpu`
· **Data:** 2026-08-09 · **Status:** **clarify encerrado** — as quatro decisões resolvidas por consulta registrada em [ADR 0007](../../adr/0007-fronteira-entre-modelo-e-metodo.md) e [ADR 0008](../../adr/0008-atribuicao-da-instancia-que-cicla.md)

> **Nota de processo.** O autor autorizou uma execução longa e instruiu: *"qualquer decisão,
> chame um especialista, veja a recomendação, registre num ADR e prossiga"*. As decisões abertas
> desta spec estão em [§Decisões abertas](#decisões-abertas) e são resolvidas por consulta
> registrada, não por escolha minha — e não por espera do autor, que está ausente.

## O quê

Escrever o **capítulo 10 — Casos especiais e degenerescência**, quarto capítulo da Parte II: o
que fazer quando o Simplex **não** devolve "aqui está seu plano".

## Por quê

Este capítulo é **dívida em letra publicada**. O capítulo 09 o cita cinco vezes, e uma delas é
uma promessa explícita, na seção "quando não serve":

> *"Degenerescência pode travar. Quando o teste da razão empata, o Simplex pode pivotear sem sair
> do lugar e, no limite, **ciclar** — voltar a uma base já visitada e girar para sempre. Existem
> regras de desempate que provam terminação; o código desta etapa usa a mais simples (menor
> índice) e **não** trata o caso completo. Capítulo 10."*

E há um motivo mais forte, que o Mapa do handbook já registra: é aqui que o aluno descobre a
lição mais dura da Parte II — **quando o Simplex dá uma resposta estranha, o defeito quase sempre
está no modelo, não no algoritmo.**

### O que já foi medido, antes de escrever uma linha

Duas execuções sobre o código **do próprio livro** (`po-zero/etapa-03-simplex`), com a instância
clássica de ciclagem:

| Regra de entrada/saída | Resultado |
|---|---|
| **Dantzig** (a que o capítulo 09 ensina) | **Cicla.** Volta à base inicial a cada 6 pivôs, indefinidamente |
| **Bland** (menor índice na entrada **e** na saída) | **Termina em 6 pivôs**, sem repetir base |

Isto muda o estatuto do capítulo: a ciclagem deixa de ser advertência de rodapé e vira
**fenômeno reproduzível no livro**, como o cubo de Klee–Minty foi no capítulo 09.

E revela um detalhe que o capítulo 09 declarou com imprecisão: o código dele desempata a **saída**
pelo menor índice, o que **não é a regra de Bland** e **não previne ciclagem**. A frase do 09 diz
que "não trata o caso completo", o que é verdade, mas sugere cobertura parcial onde há zero.
Corrigir isso é parte desta rodada.

## Escopo

### Entra

- `livro/capitulos/10-casos-especiais.md`, no esqueleto do Guia Editorial, **com a seção
  "De onde isto veio"** (Princípio XII).
- `po-zero/etapa-04-casos-especiais` — os vereditos medidos, incluindo a demonstração
  Dantzig-cicla / Bland-termina e a implementação da regra de Bland.
- **Mínimo de 3 exercícios** (`cap10`), com modelo verificável pelo portão de ótimo onde couber.
- Capacidade do tutor, vídeo curado, verbetes de glossário, sumário, mapa, histórico.
- **Correção pontual no capítulo 09**: a frase sobre o desempate por menor índice.

### Não entra

- Forma revisada e fatoração — capítulo 11.
- Dualidade e preço-sombra — capítulo 12.
- Análise de sensibilidade — capítulo 13.
- Perturbação/lexicográfico como *método completo*: entram como menção com destino, não como
  procedimento treinado.

## Decisões abertas — e onde cada uma foi resolvida

Quatro. Nenhuma delas era minha, e todas foram a especialista antes de virar texto. A numeração
abaixo é a **canônica**: os ADRs referem-se a ela.

| # | Assunto | Resolvida em |
|---|---|---|
| **D1** | Divisão de trabalho entre os capítulos 09 e 10 | [ADR 0007](../../adr/0007-fronteira-entre-modelo-e-metodo.md) |
| **D2** | A instância condutora | [ADR 0008 — emenda](../../adr/0008-atribuicao-da-instancia-que-cicla.md#emenda--a-instância-condutora-do-capítulo-d2-da-spec) |
| **D3** | Quanto da regra de Bland entra | [ADR 0008](../../adr/0008-atribuicao-da-instancia-que-cicla.md) |
| **D4** | Onde mora a degenerescência no discurso | [ADR 0007](../../adr/0007-fronteira-entre-modelo-e-metodo.md) |

As perguntas como foram feitas, preservadas para que se possa julgar se a resposta responde:

**D1. A divisão de trabalho entre os capítulos 09 e 10.** O capítulo 09 já **detecta** inviável
(artificial na base) e ilimitado (sem razão positiva). Repetir isso no 10 seria redundância; não
tratar seria deixar o mapa mentindo, porque ele promete os quatro casos aqui.
*Hipótese a validar:* 09 ensina **como o algoritmo detecta**; 10 ensina **o que cada veredito diz
sobre o modelo e o que fazer**.

**D2. A instância condutora.** A montadora atravessa os capítulos 07, 08 e 09. Degenerescência
pode ser induzida nela de forma natural; ciclagem **não** — exige coeficientes construídos.
*Hipótese a validar:* montadora para degenerescência e múltiplos ótimos; instância clássica de
ciclagem apenas para ciclar, com a raridade dela como parte da lição.

**D3. Quanto da regra de Bland entra.** Demonstrar que termina é medível. **Provar** que termina
é outra coisa, e cara.
*Hipótese a validar:* demonstrar e não provar, com a prova apontada como leitura.

**D4. Onde mora a degenerescência no discurso do livro.** Ela é patologia de algoritmo ou sintoma
de modelo? A resposta editorial muda o capítulo inteiro.
*Hipótese a validar:* sintoma de modelo — restrição redundante que passa pelo vértice —, coerente
com a tese da Parte II.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| A1 | Capítulo publicado, no sumário e no mapa | Página gerada e alcançável |
| A2 | A ciclagem é **medida**, não citada | Saída do experimento, com as bases repetidas impressas |
| A3 | Bland termina onde Dantzig cicla, na mesma instância | Saída do experimento |
| A4 | Os quatro vereditos aparecem com **o que fazer** em cada um | Leitura; D1 respondida |
| A5 | ≥3 exercícios, 3 a 5 critérios cada, rastreando objetivo existente | Portão de exercícios |
| A6 | Todo exercício que afirme ótimo tem `modelo` conferido | Portão de ótimo |
| A7 | `experimento.py` reproduz `resultados.json` byte a byte | Dupla execução |
| A8 | Seção "De onde isto veio" com fontes seladas | Portão do Princípio XII |
| A9 | As **três** afirmações falsas sobre o desempate corrigidas: capítulo 09, `etapa-03/README.md` e a *docstring* de `quadro.py` | `git diff` |
| A10 | Build, ilha e testes verdes | `npm run build`, `verifica:ilha`, `pytest -q` |
| A11 | Toda decisão aberta tem ADR com a recomendação do especialista | `adr/` |

## Riscos

| Risco | Mitigação |
|---|---|
| **Repetir o capítulo 09** com outra roupa | D1 decide a fronteira antes de escrever, e a decisão vira ADR |
| Ciclagem virar curiosidade sem consequência | O experimento mede as duas regras na mesma instância; a consequência é a escolha de regra |
| **Pular o gate de plano de novo** — aconteceu na rodada 004 | O plano vai ao `guardiao-processo` **antes** de qualquer linha de capítulo |
| Instância de ciclagem sem procedência | Vai a `curador-pesquisa`: origem, autoria e ano com selo |
| Degenerescência apresentada como defeito do Simplex | D4. Se a resposta for "sintoma de modelo", o capítulo precisa dizê-lo desde o título da seção |
