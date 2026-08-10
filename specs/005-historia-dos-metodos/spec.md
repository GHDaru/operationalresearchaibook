# Spec 005 — Estudo: de onde vieram os métodos

**Rodada:** 005 · **Raia:** plena · **Branch:** `claude/handbook-pesquisa-operacional-ucbbpu`
· **Data:** 2026-08-09 · **Status:** implementada

## O quê

Uma **sessão de pesquisa histórica**, feita de uma vez, que levanta e ficha com fonte a origem
dos métodos que os capítulos futuros vão apresentar — da Parte II ao restante do núcleo. O
produto é [`estudos/002-historia-dos-metodos.md`](../../estudos/002-historia-dos-metodos.md), e
ele é **insumo**, não conteúdo publicado.

## Por quê

O [Princípio XII](../../.specify/memory/constitution.md) passou a exigir que todo capítulo de
método conte de onde o método veio. Isso cria uma escolha de processo: pesquisar **por capítulo**,
dentro de cada rodada, ou pesquisar **de uma vez**, num estudo que alimenta as rodadas.

Pesquisar por capítulo sai mais caro e sai pior, e há evidência disso no próprio livro: a conexão
entre **Motzkin** no capítulo 08 (redescobrindo a eliminação de Fourier) e **Motzkin** no capítulo
09 (batizando o Simplex) só apareceu porque as duas pesquisas foram feitas na mesma sessão. Se
tivessem sido feitas em rodadas separadas, os dois capítulos teriam sido publicados sem a ligação.

Há ainda um motivo de oportunidade: o acesso à literatura acadêmica foi liberado no ambiente de
trabalho nesta data. Concentrar a pesquisa enquanto o acesso existe é mais seguro do que depender
de ele continuar disponível a cada rodada futura.

## Decisões do autor

| # | Pergunta | Resposta |
|---|---|---|
| 1 | Formato da sessão de história | **Estudo em `estudos/`**, alimentando as rodadas futuras — em vez de capítulo próprio publicado agora |
| 2 | Profundidade da pesquisa | **Ler o que der; marcar o resto como atribuição corrente**, com o estado dito item a item |

A resposta 2 fixa o padrão de selos do estudo: `✓` lido, `✓ᵐ` só metadados, `⏳` atribuição
corrente, `❌` sem fonte, `📖` leitura editorial.

## Escopo

### Entra

- Fichamento por Parte, cobrindo o que os capítulos 10 a 15 e as Partes III, IV e V vão precisar.
- **Verificação de metadados no Crossref** para cada obra citada: autor, obra, volume, página, ano
  e identificador de objeto digital (DOI).
- **Leitura de fonte** onde o acesso permitiu.
- Um **gancho editorial** por item — o que a história ensina, marcado como leitura deste livro e
  não como afirmação histórica.
- Uma **fila de verificação** ordenada por dívida fechada por unidade de esforço.

### Não entra

- **Publicar qualquer coisa no livro.** Nenhuma seção "De onde isto veio" nova; nenhum capítulo
  novo. Cada história entra pela rodada do seu capítulo.
- Parte VI a IX e a camada de fronteira. Fora do horizonte das próximas rodadas.
- A dívida de *fundamentos científicos* dos capítulos 07 a 09 — é outro assunto (resultados, não
  história) e merece rodada própria.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| A1 | Toda obra citada tem autor, obra, ano e DOI conferidos | Consulta ao Crossref, registrada |
| A2 | Todo item tem selo de estado, e o selo diz a verdade | Leitura; nenhum `✓` sem fonte aberta |
| A3 | Nenhuma afirmação histórica sem fonte, e nenhuma leitura editorial disfarçada de fato | Selo `📖` explícito em toda interpretação |
| A4 | O estudo declara o que **não** conseguiu verificar, e por quê | Seção de fila de verificação |
| A5 | Nada é publicado no livro nesta rodada | `git diff` não toca `livro/capitulos/` |
| A6 | Build e testes verdes | `npm run build` e `pytest -q` |

## Riscos

| Risco | Mitigação |
|---|---|
| **Inventar história** — o risco central do Princípio XII, porque história falsa soa bem | Selo por item; `✓` exige fonte aberta. Onde a fonte não abriu, o item fica `⏳` mesmo quando a atribuição é unânime na literatura didática |
| Confundir metadado conferido com conteúdo lido | Selo `✓ᵐ` existe só para isso. A atribuição do *big-M* a Charnes é o caso: metadados conferidos, conteúdo não lido, atribuição segue `⏳` |
| O estudo virar enciclopédia e nunca virar capítulo | Cada item tem gancho editorial declarado. O que não tem gancho não precisa de fichamento |
| Confiar em resumo de busca | Aconteceu na rodada anterior e quase produziu um erro: um resumo secundário abreviava a fonte de modo a fazer um fato correto parecer errado. **Resumo de busca não é fonte, nem para confirmar nem para desmentir** |
