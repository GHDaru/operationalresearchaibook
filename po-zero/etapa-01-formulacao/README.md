# Etapa 01 — Formulação

> Serve o capítulo **07 — Formulação de modelos lineares**. Roda em segundos, em CPU, sem
> licença paga.

## O que esta etapa constrói

O modelo da montadora **montado a partir da lista de materiais**, e não escrito à mão. É MRP ao
contrário: o planejamento de necessidades de materiais clássico anda da demanda para o
componente; aqui parte-se do componente que existe e pergunta-se o que dá para montar.

O experimento percorre as três etapas da narrativa do capítulo e, na última, **refuta com
número** as duas regras de bolso que o aluno naturalmente inventa.

## Rodar

```bash
cd po-zero/etapa-01-formulacao
pip install pulp highspy
python experimento.py
```

Saída esperada:

```
  etapa 1 (sem restrição) : Unbounded
  etapa 2 (só CPU)        : 10 do Tipo 2 -> R$ 1500
  etapa 3 (CPU + memória) : 8 e 2        -> R$ 1100
    o ótimo da etapa 2 ainda é viável? False  (folga de pentes: -8)

  por CPU     escolhe tipo2 -> R$  900  (perde R$ 200)
  por pente   escolhe tipo1 -> R$ 1000  (perde R$ 100)
```

## Arquivos

| Arquivo | O que é |
|---|---|
| `instancias/montadora.json` | Os dados, **com ficha**: origem, licença e limitações declaradas |
| `modelo.py` | Monta o modelo a partir da lista de materiais; avalia planos arbitrários; aplica as regras gulosas |
| `experimento.py` | Gera `resultados.json` — a procedência de todo número do capítulo |
| `resultados.json` | A saída, com versões de Python, biblioteca e solver |

## Por que o modelo vem da lista de materiais

Acrescentar um terceiro produto ou um quarto componente é **editar o JSON, não o código**. É
assim que se percebe que a formulação tem *forma*, e que a forma é o que os métodos exploram.
Um modelo escrito à mão esconde exatamente isso.

A função `regra_gulosa` existe para ser **refutada**: ela implementa a heurística "faça o que
paga mais por unidade de X" e mostra, com número, que duas escolhas razoáveis de X levam a
produtos diferentes e nenhuma ao ótimo.

## Contrato desta etapa

- **Determinística.** Rodar duas vezes produz `resultados.json` byte a byte idêntico. Não há
  aleatoriedade, e por isso não há semente declarada — gravar uma semente não usada seria teatro
  de reprodutibilidade.
- **Versões declaradas** em `resultados.json`.
- **Instância com ficha**, autoral e didática.
- **Ilimitado é resultado, não erro.** A etapa 1 do capítulo depende disso, e o código trata
  esse status como saída legítima.

## O que esta etapa deliberadamente não faz

Não abre o solver, e não desenha nada. Formulação treina formulação; a geometria é a
[etapa 02](../etapa-02-metodo-grafico/README.md).
