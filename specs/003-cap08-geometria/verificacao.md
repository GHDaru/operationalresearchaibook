# Verificação 003 — Capítulo 08 (e a rodada 002 refeita)

> **Executada em 2026-08-07**, depois da revisão em contexto fresco e das correções.
> Substitui a verificação anterior da rodada 002, que documentava um capítulo descartado.

## Build do site — todos os portões

```
✓ espelho de capacidades em sincronia (6 capacidades)
✓ referências de capítulo OK: 0 referências (0 compostas) apontam para capítulos existentes — a aderência semântica é leitura humana
✓ Grafo do livro: 14 nós, 20 arestas
✓ Livro gerado [pt]: 12 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 3 capítulos com C01/N02 + 9 páginas de aparato OK
✓ registro de exercícios OK: 14 exercícios em 2 baterias, rubrica não publicada
```

## Testes do backend

```
24 passed, 1 warning in 0.80s
```

## Determinismo dos dois experimentos

```
etapa 01: 43f9034151cbaabc49a1cb977cdefb28 / 43f9034151cbaabc49a1cb977cdefb28  -> IDÊNTICOS
etapa 02: 0326b7f304209656ff31c0c00d9999ec / 0326b7f304209656ff31c0c00d9999ec  -> IDÊNTICOS
```

## As 14 respostas, conferidas de forma independente

Enumeração de vértices (`enumera.py`) contra HiGHS, para os 14 exercícios dos dois capítulos:

```
cap07.exC  (200, 0)  z=96000   enumeração x solver: OK
cap08.exA  (4, 0)  z=12   enumeração x solver: OK
cap08.exB  (3, 1.5)  z=21   enumeração x solver: OK
cap08.exC  (4, 0)  z=8   enumeração x solver: OK
cap08.exD  (20, 60)  z=2600   enumeração x solver: OK
cap08.exE  (4, 2)  z=12   enumeração x solver: OK   [múltiplos ótimos]
cap08.exF  (10, 15)  z=725   enumeração x solver: OK
cap08.exG  (8, 8)  z=2240   enumeração x solver: OK
cap08.exH  (50, 50)  z=105000   enumeração x solver: OK
cap08.exI  (20, 12)  z=244   enumeração x solver: OK
cap08.exJ  (2.5, 3)  z=22.5   enumeração x solver: OK
```

**`cap07.exC` é o exercício que a revisão barrou.** Antes, com lucro (480, 300), o ótimo era
(137,5; 125) com 103.500 — e o enunciado afirmava (200, 0). Agora o modelo tem como ótimo o
plano que ele mesmo apresenta, com a solda em folga de 500 h, que é o sintoma que o exercício
manda o leitor ler.

## O que esta verificação NÃO cobre

- **Se os capítulos ensinam bem.** Leitura humana; é o gate do autor.
- **A ilha interativa em uso real.** A lógica foi corrigida e conferida por leitura, mas
  ninguém a operou num navegador. É o único artefato sem verificação executável.
- **Os vídeos**, em estado provisório declarado.
- **As seções de fundamentos científicos**, vazias por lacuna declarada.
