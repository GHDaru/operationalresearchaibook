# Etapa 01 — Formulação

> Serve o capítulo **07 — Formulação de modelos lineares**. Roda em segundos, em CPU, sem
> licença paga.

## O que esta etapa constrói

O mesmo problema de mix de produção, formulado **duas vezes**: uma maximizando margem de
contribuição, outra maximizando receita. As restrições são idênticas; só o objetivo muda.

Os dois modelos rodam. Os dois devolvem "ótimo". **Só um responde à pergunta que a marcenaria
fez** — e a diferença entre eles é o número que abre o capítulo.

Essa é a lição da etapa: o erro caro em Pesquisa Operacional (PO) não é o solver que falha, é
o modelo que responde bem à pergunta errada.

## Rodar

```bash
cd po-zero/etapa-01-formulacao
pip install pulp highspy
python experimento.py
```

Saída esperada:

```
  correto (margem): {'mesa': 30.0, 'estante': 40.0} -> R$ 13800.00
  errado (receita): {'mesa': 60.0, 'estante': 0.0} -> margem R$ 13200.00
  custo do erro:    R$ 600.00 por mês
```

## Arquivos

| Arquivo | O que é |
|---|---|
| `instancias/moveis.json` | Os dados, **com ficha**: origem, licença e limitações declaradas |
| `modelo.py` | As duas formulações, e a função que resolve |
| `experimento.py` | Gera `resultados.json` — a procedência de todo número do capítulo |
| `resultados.json` | A saída, com versões de Python, biblioteca e solver |

## Contrato desta etapa

- **Determinística.** Não há aleatoriedade: rodar duas vezes produz `resultados.json` byte a
  byte idêntico. Por isso não há semente declarada — gravar uma semente que não é usada seria
  teatro de reprodutibilidade.
- **Versões declaradas** em `resultados.json`. Número medido sem versão não é evidência.
- **Instância com ficha.** Origem, licença e limitações estão em `instancias/moveis.json`. Ela
  é autoral e didática: não representa empresa real, e isso está dito lá.
- **Pequena de propósito.** Dois produtos e dois recursos, para que a mesma instância possa ser
  resolvida à mão nos capítulos sobre geometria e sobre o Simplex. O leitor vê o mesmo problema
  por três lentes.

## O que esta etapa deliberadamente não faz

Não abre o solver. `HiGHS` é tratado como caixa-preta aqui, e o capítulo diz isso ao leitor —
com a promessa de que os capítulos seguintes da Parte II abrem a caixa. Etapa de formulação
treina formulação.
