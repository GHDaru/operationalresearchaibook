# ADR 0001 — Reúso do motor de livro vivo

**Data:** 2026-08-06 · **Status:** aceito

## Contexto

O handbook de Pesquisa Operacional (PO) precisa de site navegável, geração de PDF, portões de
qualidade por página, exercícios com correção no servidor e tutor com *Retrieval-Augmented
Generation* (RAG) sobre o próprio texto. Construir isso do zero levaria a rodada inteira e não
entregaria nenhum conteúdo.

O mesmo autor já possui esse motor, escrito para o livro *Engenharia de Harness* e adaptado
para o livro *Teoria das Restrições*, sob licença MIT.

## Decisão

**Reusar o motor**, clonando o repositório do livro *Teoria das Restrições* e refundando o
conteúdo. O motor entra como está; o conteúdo, a governança e o aparato são reescritos para PO.

## Alternativas avaliadas

| Alternativa | Por que não |
|---|---|
| Motor novo, sob medida para PO | Custo alto, benefício nenhum: o que PO exige a mais (notação matemática, blocos de código) o motor já suporta via Markdown |
| Gerador de site pronto (MkDocs, Docusaurus) | Nenhum deles traz os portões de qualidade que sustentam os princípios — rubrica não publicada, exercício órfão, referência quebrada — e é neles que está o valor |
| Escrever em plataforma fechada | Perde versionamento, perde o ciclo de especificação, perde os portões |

## Consequências

**Boas.** A rodada de fundação entrega mapa, aparato e site publicável. A estrutura declarativa
(`publicar/sumario.json`) sustenta diretamente a promessa da camada de módulos aplicados:
capítulo novo é arquivo novo mais uma linha, sem tocar no motor.

**Ruins, e assumidas.** O repositório nasceu carregando conteúdo de outro livro, que precisou
ser removido nesta mesma rodada — e alguns pontos do motor estavam acoplados àquele conteúdo
(nome do livro nos artefatos de download, mapa de siglas, contagem fixa de capítulos no portão
do grafo). Esses acoplamentos foram corrigidos aqui; outros podem aparecer, e cada um vira
correção de raia leve quando aparecer.

**Herança de licença.** O código permanece MIT, com o crédito de origem preservado em
`LICENSE-CODE`.
