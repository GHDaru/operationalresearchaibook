# Etapa 04 — Os cinco vereditos

> Serve o capítulo **10 — Casos especiais e degenerescência**.

## O que esta etapa constrói

Nenhum método novo. Esta etapa **instrumenta** o Simplex do capítulo 09 para que os vereditos que
não são "aqui está seu plano" possam ser **observados**, e não apenas descritos.

Três instrumentos, e cada um responde a uma pergunta que o número sozinho não responde:

| Instrumento | A pergunta |
|---|---|
| Detecção de ciclo por **repetição de base** | Isto é um ciclo ou só lentidão? |
| Leitura de **básica em zero** no quadro final | O vértice é degenerado? |
| Leitura de **custo reduzido zero fora da base** | Existe mais de um plano ótimo? |

## Rodar

```bash
cd po-zero/etapa-04-casos-especiais
python experimento.py
```

## O que o experimento mostra

| Caso | Veredito | Pivôs | O que o quadro denuncia |
|---|---|---:|---|
| Vértice degenerado | ótimo, R$ 1.100 | 2 | `f3` **na base valendo zero**; empate no teste da razão em duas iterações |
| Mais de um ótimo | ótimo, R$ 1.200 | 1 | **custo reduzido zero** em `x1`, que está **fora** da base |
| Sem teto | ilimitado | 0 | nenhuma razão positiva |
| Sem plano | inviável | 1 | artificial sobra na base com valor positivo |
| O giro — **Dantzig** | não termina | estoura | **ciclo de período 6**: a base `(f1, f2, f3)` volta na iteração 6 |
| O giro — **Bland** | ótimo | 6 | nenhuma base repetida |

Os cinco vereditos batem com o **HiGHS**: `Optimal`, `Optimal`, `Unbounded`, `Infeasible` e —
no caso do giro — `Optimal` em (0,04; 0; 1; 0) com valor 0,05, que é exatamente o que Bland
encontra, $(1/25,\ 0,\ 1,\ 0)$ com $z = 1/20$.

## O experimento controlado, que é o ponto

Os dois últimos casos são **a mesma instância**. Muda só a regra de pivoteamento.

- Com **Dantzig**, o método gira para sempre.
- Com **Bland**, termina em 6 pivôs.
- No caso degenerado, os **empates no teste da razão continuam existindo sob as duas regras**.

Daí sai a tese do capítulo, e ela é medida, não afirmada:

> **O que é do modelo sobrevive à troca do método. O que some quando você troca o método era do
> método.**

A ciclagem some: era da regra. A degenerescência fica: é do modelo.

## Arquivos

| Arquivo | O que é |
|---|---|
| `vereditos.py` | Os três instrumentos: detecção de ciclo, de vértice degenerado e de múltiplos ótimos |
| `experimento.py` | Roda os cinco casos e confere contra o solver |
| `resultados.json` | A saída, com os quadros finais e as versões declaradas |

## Detalhes que valem nota

- **O Simplex é reusado, não duplicado.** `vereditos.py` importa `quadro.py` da etapa 03. Para
  isso, aquele módulo ganhou o parâmetro `regra` (`"dantzig"` ou `"bland"`) — mudança aditiva,
  verificada: o `resultados.json` da etapa 03 continua **byte a byte idêntico**.
- **A detecção de ciclo é *post-hoc*.** Ela lê as iterações que `resolver` já devolve, em vez de
  entrar no motor. Assim o código do capítulo 09 permanece exatamente como foi publicado.
- **O limite de iterações é evidência, não erro.** Quando a regra de Dantzig o estoura na
  instância que gira, isso **é** o resultado — e o experimento imprime a base repetida e o
  período para provar que é ciclo, e não lentidão.
- **Sobre a instância que cicla**: os primeiros exemplos são creditados a **Hoffman** e a
  **Wolfe**, o que está registrado em fonte de 1955 que este handbook leu; a instância que o
  ensino faz circular é atribuída a **Beale (1955)**, cujo artigo se chama *"Cycling in the dual
  simplex algorithm"* — e este handbook **não afirma** que a forma primal usada aqui apareça
  literalmente nele. Ver [ADR 0008](../../adr/0008-atribuicao-da-instancia-que-cicla.md).
- **Nenhuma prova.** Que Bland termina é **medido** aqui, não demonstrado. A prova está apontada
  na bibliografia, e o enunciado exato da regra no artigo original segue `⏳`.
