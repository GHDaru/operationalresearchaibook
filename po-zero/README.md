# po-zero — a construção prática

> **Conteúdo revisado em 2026-08.** Uma etapa por capítulo de método. Roda em CPU, sem licença
> paga.

O handbook não afirma número que não saiba regenerar. O `po-zero` é onde essa regra vira
código: **todo número publicado no livro tem aqui um script que o produz**, com instância,
semente e versões declaradas (constituição, Princípios III e IV).

## A pilha

| Camada | Escolha | Por quê |
|---|---|---|
| Linguagem | Python 3.11+ | O que os alunos já usam |
| Modelagem | **PuLP** para começar, **Pyomo** quando o modelo cresce | PuLP tem a menor distância entre a notação matemática e a primeira linha de código; Pyomo sustenta modelos indexados e blocos |
| Solver | **HiGHS** (padrão), CBC como alternativa | Abertos, sem licença, empacotados via `pip` |
| Numérico | NumPy e SciPy | Para as implementações didáticas dos algoritmos |

Solver comercial pode aparecer no livro como **comparação**, nunca como dependência. Custo zero
é requisito, não preferência. A decisão e as alternativas avaliadas estão no
[ADR 0003](../adr/0003-stack-po-zero.md).

## A regra das duas implementações

Cada método algorítmico do núcleo aparece **duas vezes**:

1. **A implementação didática** — o algoritmo escrito para ser lido, em NumPy, com os passos
   visíveis e o estado inspecionável a cada iteração. Serve para entender, não para produzir.
2. **A chamada ao solver** — o mesmo problema resolvido como se faria no trabalho.

E o capítulo compara as duas. É essa comparação que fecha a lacuna entre o aluno que pivoteia
um quadro sem saber modelar e o que chama o solver sem saber o que ele faz — os dois modos de
sair mal de um curso de Pesquisa Operacional (PO).

## Estrutura

```
po-zero/
  README.md          ← este arquivo
  etapa-NN-nome/     ← uma por capítulo de método
    README.md        ← o que esta etapa constrói, e o objetivo do capítulo que ela serve
    modelo.py        ← a formulação
    algoritmo.py     ← a implementação didática, quando o capítulo tem uma
    experimento.py   ← gera os números citados no capítulo
    instancias/      ← os dados, versionados quando pequenos; com ficha quando não
    resultados.json  ← a saída, com semente e versões, regenerável
```

## Contrato de cada etapa

Uma etapa só é dada por pronta se:

- `experimento.py` roda do zero e **reproduz** `resultados.json` — mesma semente, mesmos
  números.
- `resultados.json` declara versão de Python, das bibliotecas e do solver.
- Toda instância tem ficha: origem, licença e limitações. Instância sem procedência não entra.
- O tempo de execução da etapa completa cabe em minutos numa máquina comum. O que não couber
  vira instância reduzida no livro, com a instância cheia documentada à parte.

## Estado atual

**Vazio, e declarado como dívida.** Esta é a rodada de fundação: existem a decisão de pilha e o
contrato acima. As etapas nascem junto com os capítulos que servem, a começar pela rodada de
Programação Linear (PL) — ver [roadmap](../ROADMAP.md).
