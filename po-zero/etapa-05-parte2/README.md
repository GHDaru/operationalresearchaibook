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

CPUs             hoje 10 · faixa [13/2, 12]
pentes de 16 GB  hoje 12 · faixa [10, 39/2]
```

**Se a dualidade forte não conferisse, o script aborta** — e o capítulo 12 não poderia ser
escrito. A verificação é gate, não relatório.

## O que esta etapa NÃO prova

- Nada sobre solvers reais: é aritmética exata, em instância de duas variáveis.
- A faixa de validade é achada por **busca direta**, não por fórmula de sensibilidade. Ensina a
  fronteira sem exigir álgebra que o leitor v0 ainda não tem — e é por isso que o passo é `1/2`,
  não infinitesimal. **A fronteira é a menor mudança de base detectável nesse passo.**
- Em **vértice degenerado** a faixa fica ambígua, e o capítulo 10 já avisou disso. A montadora não
  é degenerada, então este caso **não está medido aqui**.
