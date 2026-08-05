# ADR 0004 — Adicionar o Módulo 0 e renumerar o livro

- **Status:** aceito
- **Data:** 2026-08-01
- **Rodada:** 9 (`specs/007-modulo-0`)
- **Decisor:** Gilsiley Darú (gate humano)

## Contexto

O livro se chama *Teoria das Restrições*. Medido no código, antes desta rodada:

| Conceito | Ocorrências |
|---|---|
| "restrição" como conceito definido | **0** — a palavra aparecia 2× de passagem |
| Cinco passos de focalização | **0** |
| Ótimo local × ganho global | **0** |
| Ganho / Inventário / Despesa Operacional | **0** |
| Tambor-Pulmão-Corda | **0** |

O que existia era um treinamento nos **Processos de Raciocínio** — um ramo da TOC — sem a
teoria que lhes dá propósito. A capa traz uma corrente com o elo restritivo em âmbar, e o
livro nunca explicava esse elo.

O autor, lendo o livro no papel de auditor, formulou o problema antes de qualquer medição:
*"para TOC, senti que está fraco; este está excelente para o processo de raciocínio — não o
perca"*. A frase contém as duas restrições da decisão: **o nome precisa ser honrado** e **o
conteúdo existente não pode ser perdido**.

## Alternativas avaliadas

### A — Adicionar a espinha (escolhida)

Um Módulo 0 novo (a restrição, o ótimo local, os cinco passos, as três perguntas); o
conteúdo atual é preservado e **reposicionado** como a resposta às três perguntas.

- **A favor:** o livro passa a merecer o nome; nada se perde; o conteúdo existente ganha
  endereço em vez de ficar solto; abre caminho natural para o módulo de operações.
- **Contra:** ~4 capítulos novos a escrever e moderar; obriga a renumerar o livro inteiro,
  com risco de referências cruzadas quebradas (risco que se materializou — ver
  "Consequências"); amplia a dívida da tradução EN em quatro capítulos.

### B — Renomear o livro

Assumir o que ele é: um treinamento em raciocínio rigoroso. A TOC vira contexto, não
título.

- **A favor:** honesto e barato — zero conteúdo novo, zero renumeração, entrega imediata.
- **Contra:** abre mão do guarda-chuva TOC, que é o corpo de conhecimento que o autor
  domina e pretende ensinar por inteiro. O módulo de operações (a expertise dele) não teria
  onde morar. Resolve o problema de coerência eliminando a ambição, não cumprindo-a.

### C — Dois livros

Este permanece como está; a TOC completa vira outro livro vivo.

- **A favor:** preserva o foco de cada um; o motor já é reaproveitável.
- **Contra:** duplica infraestrutura, público e esforço editorial num projeto que ainda não
  tem leitores; e os dois livros ficariam incompletos um sem o outro — o que é um argumento
  para serem o mesmo livro.

## Decisão

**Caminho A.** O Módulo 0 entra com quatro capítulos (01–04) e o livro inteiro é
renumerado para acomodá-lo. O conteúdo anterior não muda de texto: muda de **papel**.

O reposicionamento é o coração da decisão, e não um efeito colateral dela: os módulos 2, 3
e 4 passam a ser, um a um, **as respostas às três perguntas** formuladas no Módulo 0. O
Módulo 1 (fundamentos lógicos) passa a ser a gramática comum das três.

| Módulo | Capítulos | Papel |
|---|---|---|
| Abertura | 00 | Introdução |
| **0 — A restrição** | 01–04 | novo: o sistema, o ótimo local, os cinco passos, as três perguntas |
| 1 — Fundamentos lógicos | 05–09 | a gramática comum (era 01–05) |
| 2 — O que mudar | 10–11 | Nuvem e conflitos recorrentes (era 06–07) |
| 3 — Para o que mudar | 12 | Injeções (era 08) |
| 4 — Como causar a mudança | 13–14 | APR e aplicação integrada (era 09–10) |

## Consequências

**Boas.** O livro define o próprio título. As ferramentas deixam de ser um catálogo e
passam a ser respostas a perguntas declaradas. O vocabulário fundador (restrição, gargalo,
ótimo local, ganho/inventário/despesa operacional) entra no glossário e fica disponível
para os módulos futuros.

**Ruins, e conhecidas.** A renumeração quebrou quatro referências em conteúdo publicado —
a substituição foi ancorada na palavra-chave ("capítulo NN") e o **segundo número de toda
referência composta** ("capítulos 06 a 09", "caps. 08 e 12") nunca foi visto. Chegaram a
sair: `capítulos 06–05` na leitura executiva da introdução, `capítulos 10 e 08` na
bibliografia e `(caps. 08 e 08)` na rubrica do exercício final. Foram achados pela revisão
em contexto fresco, corrigidos, e o modo de falha virou portão
(`publicar/verifica-referencias.mjs`).

**Registro datado.** As edições 0.1 a 0.6 do `HISTORICO.md` usam a numeração antiga. Não
foram reescritas — registro datado não se reescreve —, mas ganharam nota de época, porque
o histórico é página publicada e alimenta o RAG do tutor.

**Dívida ampliada.** O par em inglês (Princípio II) passou a dever quatro capítulos a mais.

**Fica aberto.** O módulo de **operações** — Tambor-Pulmão-Corda, gestão de pulmões,
contabilidade de ganhos — é o que fecha a TOC como corpo, e é a expertise do autor. O
Módulo 0 já introduz o vocabulário (ganho, inventário, despesa operacional) que esse módulo
vai precisar.
