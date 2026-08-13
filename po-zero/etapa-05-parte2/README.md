# Etapa 05 — a medição da Parte II

**Uma etapa por Parte**, não por capítulo ([ADR 0013](../../adr/0013-o-que-e-a-v0.md), D3). Esta
ancora os capítulos **12** (dualidade) e **13** (sensibilidade).

```bash
python3 dual.py     # regenera resultados.json
```

## O que ela mede, e por que assim

| Medição | Serve a | Por que não é circular |
|---|---|---|
| Preços-sombra lidos no quadro final | cap. 12 | É o teorema: o custo reduzido da folga *é* o preço da restrição |
| **O dual montado e resolvido como problema próprio** | cap. 12 | **A verificação.** Ler o preço no quadro primal usa o mesmo cálculo para produzir e conferir. Montar o dual à parte e chegar ao mesmo valor é independente |
| Faixa de validade de cada estoque | cap. 13 | Varre o lado direito em passos exatos e acha onde a **base** muda — o ponto em que o preço deixa de valer |

## O resultado

```
primal   ponto (8, 2)   valor 1100
preços   CPUs = 50 · pentes de 16 GB = 50
dual     y = (50, 50)   valor 1100   (2 pivôs, problema separado)
dualidade forte confere: True

faixa do ESTOQUE — até onde o preço-sombra vale
  CPUs                        hoje 10 · faixa [6, 12]
  pentes de memória de 16 GB  hoje 12 · faixa [10, 20]
faixas conferidas por caminho independente: True

faixa do LUCRO UNITÁRIO — até onde o plano continua o mesmo
  Tipo 1 (16 GB): hoje 100 · faixa [75, 150]
  Tipo 2 (32 GB): hoje 150 · faixa [100, 200]
```

**Se a dualidade forte não conferisse, o script aborta** — e o capítulo 12 não poderia ser
escrito. A verificação é gate, não relatório.

## O que esta etapa NÃO prova

- Nada sobre solvers reais: é aritmética exata, em instância de duas variáveis.
- A faixa de validade sai de **álgebra exata** sobre o quadro final: com todas as restrições `<=`,
  as colunas de folga são $B^{-1}$, e a base segue viável enquanto $x_B + \Delta \cdot (B^{-1}e_i)
  \ge 0$. É a fronteira exata, em fração, sem passo e sem resolver de novo.

  > **Uma versão anterior desta etapa fazia isso por varredura de meio em meio, e publicou duas
  > faixas ERRADAS no capítulo 12** — `[13/2, 12]` e `[10, 39/2]`, quando o certo é `[6, 12]` e
  > `[10, 20]`. O defeito não era de precisão: a varredura media **em que base o Simplex
  > aterrissa**, e não **para que estoque a base continua ótima**. Registrado na
  > [ADR 0014](../../adr/0014-relatorio-de-sensibilidade-e-a-faixa-medida.md), D2. Toda faixa
  > passou a ser conferida por um segundo caminho, que a põe na fronteira e um pouco além e exige
  > que o preço **acerte na fronteira** e **erre além dela**.
- Em **vértice degenerado** a faixa fica ambígua, e o capítulo 10 já avisou disso. A montadora não
  é degenerada, então este caso **não está medido aqui**.
