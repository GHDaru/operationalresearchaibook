# Tasks 006 — Capítulo 10: Casos especiais e degenerescência

> Escritas **antes** de implementar o capítulo, depois do parecer do `guardiao-processo`. Na
> rodada 004 este arquivo foi escrito no fim, junto com o plano, e serviu de registro em vez de
> plano de execução. Aqui volta a ser o que deve ser.

## T1 — Instrumentação (feita antes do texto, como manda o Guia)

| # | Tarefa | Estado |
|---|---|---|
| T1.1 | `quadro.resolver` aceita `regra="dantzig" \| "bland"` | ✅ |
| T1.2 | Saída da etapa 03 verificada **byte a byte** após a mudança | ✅ `0d427a9f…` |
| T1.3 | `vereditos.py`: detecção de ciclo, de vértice degenerado e de múltiplos ótimos | ✅ |
| T1.4 | `experimento.py`: os cinco casos, conferidos contra o HiGHS **por veredito** | ✅ |
| T1.5 | Experimento controlado: mesma instância, duas regras | ✅ |
| T1.6 | **Medir** o custo da garantia (pivôs sob as duas regras) em vez de afirmá-lo | ✅ |
| T1.7 | Dupla execução produz `resultados.json` idêntico | ✅ `9a6bd6f3…` |
| T1.8 | `README.md` da etapa 04 | ✅ |

## T2 — Correções que a rodada descobriu (A9)

Três afirmações falsas sobre o desempate, todas escritas por mim em rodadas anteriores ou nesta.

| # | Onde | Estado |
|---|---|---|
| T2.1 | `etapa-03/quadro.py`: a *docstring* afirmava que Bland "prova terminação" e "é mais lento" | ✅ corrigido |
| T2.2 | `etapa-03/README.md`: dizia que o desempate por menor índice "evita os casos conhecidos" | ✅ corrigido, com a correção declarada |
| T2.3 | `capitulos/09-simplex.md`: sugere cobertura parcial contra ciclagem onde há zero | ⬜ |

## T3 — O capítulo

| # | Tarefa | Estado |
|---|---|---|
| T3.1 | Objetivos O1–O4 numerados | ⬜ |
| T3.2 | "O problema": as quatro segundas-feiras + **tabela-mapa** com a coluna "onde se aprende a detectar" (D1) | ⬜ |
| T3.3 | "De onde isto veio": Hoffman e Wolfe, a citação de 1955, o *stalling*, a ideia reaproveitável | ⬜ |
| T3.4 | Vereditos 1 e 2 (inviável, ilimitado): **conduta**, sem reensinar detecção | ⬜ |
| T3.5 | Veredito 3 (mais de um ótimo): detecção pelo quadro, e por que é **boa** notícia | ⬜ |
| T3.6 | Veredito 4 (vértice degenerado): **fato do modelo**, e a caça à restrição redundante | ⬜ |
| T3.7 | "Quando o empate vira giro": ciclagem medida, Dantzig × Bland, e o custo da garantia | ⬜ |
| T3.8 | "O código", "quando não serve", síntese, leitura executiva, verificação | ⬜ |

## T4 — Exercícios

| # | Tarefa | Estado |
|---|---|---|
| T4.1 | ≥3 exercícios `cap10`, dos tipos **ler a saída** e **diagnosticar o modelo** | ⬜ |
| T4.2 | Todo quadro publicado em enunciado sai de execução | ⬜ |
| T4.3 | Todo exercício que afirme ótimo tem `modelo` conferido pelo portão | ⬜ |

## T5 — Motor e registro

| # | Tarefa | Estado |
|---|---|---|
| T5.1 | Capacidade `casos_especiais` nos dois lados do espelho | ⬜ |
| T5.2 | Sumário, mapa (10 ✅, 11 🚧), videoteca com ficha conferida na fonte | ⬜ |
| T5.3 | Glossário: vértice degenerado, ciclagem, *stalling*, regra de pivoteamento | ⬜ |
| T5.4 | Bibliografia: as duas fontes lidas + as quatro em `✓ᵐ`/`⏳` | ⬜ |
| T5.5 | `HISTORICO.md` e `ROADMAP.md` | ⬜ |
| T5.6 | `build_corpus.py` reempacotado | ⬜ |

## T6 — Verificação e gate

| # | Tarefa | Estado |
|---|---|---|
| T6.1 | Build (7 portões), ilha, testes do tutor | ⬜ |
| T6.2 | Portões novos ou alterados provados **quebrando** | ⬜ |
| T6.3 | Revisão por agente em **contexto fresco** — quem executa não verifica | ⬜ |
| T6.4 | Empurrar para a branch e **PARAR**. O merge é do autor | ⬜ |

## O que fica para o autor decidir, e não para mim

Levantado pelo `guardiao-processo` e não resolvido nesta rodada:

1. **A tese editorial da Parte II** fixada no ADR 0007 — *o que é do modelo sobrevive à troca do
   método* — governa mais do que este capítulo.
2. **A alteração do capítulo 09**, que está publicado na `main`.

Ambos vão ao gate de merge como itens explícitos de ratificação.
