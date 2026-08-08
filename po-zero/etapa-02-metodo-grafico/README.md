# Etapa 02 — O método gráfico

> Serve o capítulo **08 — A geometria da Programação Linear**.

## O que esta etapa constrói

O procedimento que o leitor faz no papel, feito por código: **todo vértice é a interseção de
duas restrições tratadas como igualdade**. Então:

1. tome as restrições duas a duas — inclusive os eixos;
2. troque `≤` por `=` e resolva o sistema 2×2;
3. descarte o que viola qualquer outra restrição;
4. avalie o objetivo no que sobrou.

Isto **não é o Simplex** — é força bruta sobre pares. Serve a dois propósitos: é exatamente o
que o leitor faz no desenho, e **prova**, no caso pequeno, a afirmação que o capítulo faz e não
demonstra em geral: o ótimo está sempre num vértice.

## Rodar

```bash
cd po-zero/etapa-02-metodo-grafico
python experimento.py
```

## O que o experimento mostra

Nas três etapas da narrativa, a enumeração à mão é **conferida contra o HiGHS**, e as duas
concordam. Com CPU e memória há seis pares de restrições; quatro produzem vértices viáveis e
dois são descartados — `(0, 10)` viola a memória e `(12, 0)` viola a CPU.

A lista de candidatos inclui os descartados **de propósito**: o capítulo mostra que a conta é
fácil e que **a triagem é que dá trabalho**.

## Arquivos

| Arquivo | O que é |
|---|---|
| `enumera.py` | `Restricao`, interseção de pares, triagem e avaliação |
| `experimento.py` | Percorre as três etapas e confere contra o solver |
| `resultados.json` | A saída, com versões declaradas |

## Detalhes que valem nota

- **A não-negatividade entra como restrição de verdade** (`-x ≤ 0`), não como caso especial. É
  isso que faz os eixos aparecerem como duas retas iguais às outras — e é a razão de o primeiro
  quadrante ser, ele próprio, uma interseção.
- **`ativa()` e `folga()`** existem para o capítulo poder falar de restrição que segura o
  resultado e de recurso que sobra. São os mesmos conceitos que a dualidade vai formalizar.
- **Degenerescência não é tratada.** Um mesmo vértice pode ser produzido por mais de um par
  quando três retas se encontram; esta instância não tem esse caso, e a deduplicação fica para
  o capítulo que trata do assunto. Dizer isso é mais honesto do que fingir cobertura.
