# Etapa 03 — O Simplex de quadro

> Serve o capítulo **09 — O método Simplex**.

## O que esta etapa constrói

A etapa anterior enumerava vértices por força bruta. Esta faz o que o Simplex faz: **anda de
vértice em vértice, sempre subindo, sem nunca olhar para o desenho**.

1. põe o modelo na forma padrão — cada `≤` ganha uma folga, cada `≥` ganha um excesso e uma
   artificial, cada `=` ganha uma artificial;
2. monta o quadro e calcula os custos reduzidos;
3. escolhe quem entra (o custo reduzido mais negativo) e quem sai (o teste da razão);
4. pivoteia, e repete até nenhum custo reduzido ser negativo.

O produto desta etapa **é a sequência de quadros**, não só a resposta. Um solver descarta os
quadros intermediários; aqui eles são o material didático.

## Rodar

```bash
cd po-zero/etapa-03-simplex
python experimento.py
```

## O que o experimento mostra

| Caso | Veredito | Pivôs | Caminho | Concorda com o HiGHS |
|---|---|---|---|---|
| Montadora | ótimo, R$ 1.100 | 2 | (0,0) → (0,6) → (8,2) | ✅ |
| Montadora com compromisso (`x2 ≥ 5`) | ótimo, R$ 950 | 3 | (0,0) → (0,5) → (0,6) → (2,5) | ✅ |
| Compromisso impossível (`x2 ≥ 8`) | inviável | 1 | — | ✅ |

Três coisas valem a leitura:

- **O caminho da montadora pisa exatamente nos vértices do capítulo 08.** O algoritmo cego chega
  ao mesmo lugar que o desenho — e é isso que o capítulo precisa mostrar, não afirmar.
- **No caso com compromisso, o primeiro ponto não é um plano real.** (0,0) só "existe" porque a
  variável artificial paga a diferença. A primeira coisa que o algoritmo faz é expulsá-la.
- **Concordar não é chegar ao mesmo ponto: é dar o mesmo veredito.** Por isso o caso impossível
  está aqui. Um Simplex que devolvesse um número bonito para um modelo sem solução seria pior do
  que um que não rodasse.

## Arquivos

| Arquivo | O que é |
|---|---|
| `quadro.py` | O Simplex de quadro: forma padrão, custos reduzidos, teste da razão, pivoteamento |
| `experimento.py` | Roda os três casos, mede a combinatória e confere contra o solver |
| `resultados.json` | A saída, com os quadros em texto e as versões declaradas |

## Detalhes que valem nota

- **Aritmética exata (`Fraction`).** O quadro impresso é o quadro do caderno: `1/2` é `1/2`. Sem
  isso, comparar papel e máquina viraria discussão sobre epsilon — e o capítulo perderia o ponto.
- **O *big-M* é simbólico**, não numérico. Cada custo é o par `(parte em M, parte numérica)`, e a
  comparação é lexicográfica, que é o que "M grande o suficiente" quer dizer. Escolher um valor
  concreto para M é justamente o atalho que produz o erro clássico de M pequeno demais, em que um
  modelo inviável devolve resposta com cara de ótima.
- **A combinatória é contada, não estimada.** `C(n+m, m)` para alguns tamanhos, no
  `resultados.json`: com 20 variáveis e 20 restrições são 137.846.528.820 bases. É o número que
  justifica o algoritmo existir.
- **O preço de uma unidade a mais de cada recurso é medido por reexecução** — resolve-se de novo
  com estoque +1 — e bate com o que a linha z do quadro final já mostrava (R$ 50 para cada um
  dos dois recursos). O capítulo 12 vai chamar isso de preço-sombra; aqui é só um número
  registrado, com duas procedências independentes.
- **Ciclagem não é tratada.** O desempate do teste da razão usa o menor índice, que evita os
  casos conhecidos, mas o assunto é do capítulo 10 e fingir cobertura aqui seria pior do que
  declarar a lacuna.
