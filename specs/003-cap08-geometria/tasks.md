# Tasks 003 — Capítulo 08: A geometria da Programação Linear

**Especificação:** [`spec.md`](spec.md) · **Plano:** [`plan.md`](plan.md) · **Data:** 2026-08-07

## Bloco 1 — Experimento antes do texto

- [x] T1.1 `enumera.py`: restrições, interseção de pares, triagem, folga e restrição ativa.
- [x] T1.2 `experimento.py`: as três etapas, com enumeração conferida contra o solver.
- [x] T1.3 Determinismo verificado por dupla execução.
- [x] T1.4 `README.md` da etapa, incluindo o que ela **não** cobre (degenerescência).

## Bloco 2 — Objetivos e banco

- [x] T2.1 Cinco objetivos, com o **O5** (formular a partir de enunciado) criado após a revisão.
- [x] T2.2 Cinco exercícios de resolução (A–E), com armadilhas desenhadas: eixo como restrição
  ativa, ótimo fracionário, minimização, triagem de pares, múltiplos ótimos.
- [x] T2.3 Cinco exercícios de modelagem (F–J).
- [x] T2.4 **As dez respostas conferidas por dois caminhos independentes** antes da rubrica.
- [x] T2.5 Progressão de dificuldade dentro de cada bloco.

## Bloco 3 — Capítulo e ilha

- [x] T3.1 `08-geometria.md` no esqueleto do Guia Editorial.
- [x] T3.2 A narrativa de aula do autor, na ordem dela.
- [x] T3.3 Ilha `regiao-viavel`, com as três interações.
- [x] T3.4 Degradação sem JavaScript, com aviso dentro da própria `div`.

## Bloco 4 — Motor e registro

- [x] T4.1 Capacidade `geometria` nos dois lados do espelho.
- [x] T4.2 Sumário, mapa e histórico.
- [x] T4.3 Identificador de exercício A–Z e campo `contexto`.

## Bloco 5 — Revisão independente e correção

- [x] T5.1 Revisão por agente em contexto fresco, contra as specs 002 e 003.
- [x] T5.2 **Bloqueador:** `cap07.exC` refeito — o modelo agora tem como ótimo o plano que o
  enunciado afirma.
- [x] T5.3 Ilha: "encosta" passa a testar o ótimo, não coincidência com vértice.
- [x] T5.4 Ilha: abre desligada, na ordem da narrativa.
- [x] T5.5 Objetivo O5 criado; quatro exercícios repontados.
- [x] T5.6 Rubricas de `exE` e `exF` corrigidas.
- [x] T5.7 Absolutos do capítulo trocados pela formulação precisa.
- [x] T5.8 Nota de superação na edição 0.3 do histórico.
- [x] T5.9 Mapa, glossário e siglas.
- [x] T5.10 Saída do experimento colada de verdade.
- [x] T5.11 Artefatos de spec que faltavam (este arquivo, o plano e a verificação).

## Bloco 6 — Processo

- [x] T6.1 Registrar a causa raiz do bloqueador: **o único banco de exercícios sem verificação
  executável foi o único com erro de fato**.
- [ ] T6.2 **Portão novo a construir:** verificar automaticamente que todo exercício cujo
  enunciado afirme uma solução ótima seja consistente com o modelo que ele mesmo apresenta.
  Fica como item de rodada própria — é o portão que teria pego o `cap07.exC` sozinho.
- [ ] T6.3 **Aprovação do autor e merge** — gate humano.
