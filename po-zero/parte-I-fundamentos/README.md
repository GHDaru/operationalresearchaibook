# Parte I — Fundamentos

> A primeira etapa criada já sob a regra nova: **uma etapa por Parte**, e não por capítulo
> ([ADR 0013](../../adr/0013-o-que-e-a-v0.md), D3).

Serve o **capítulo 05 — Complexidade computacional para quem modela**, e mede a única coisa que
aquele capítulo precisa que seja medida: **a distância entre o pior caso e a instância que você
tem na mão**.

Os capítulos 01 a 04 não têm experimento próprio, e isso é declarado em vez de disfarçado. Eles
não produzem número novo: citam os que a Parte II mediu, e cada citação está presa por teste no
capítulo que a produziu. Por isso nascem 🟡, e por isso nenhum teste deste diretório lê o `.md`
deles — o portão de maturidade trata "🟡 com teste que o leia" como incoerência, e está certo.

A única exceção é uma rubrica: o `cap03.exC` afirma um comportamento de um modelo de **três**
variáveis, fora do alcance do `verifica-otimos.mjs`. A conferência mora em
[`../etapa-01-formulacao/test_anatomia.py`](../etapa-01-formulacao/test_anatomia.py), e a isenção
no portão aponta para lá.

## O que roda aqui

```bash
python3 complexidade.py          # imprime as três tabelas e regrava resultados.json
python3 -m pytest .              # 22 testes: a medição, e o vínculo com o texto publicado
```

## As três medições

| O que | O que ela responde |
|---|---|
| **O pior caso construído** | O cubo de Klee–Minty custa exatamente $2^n-1$ pivôs, de $n=2$ a $n=7$ |
| **O pior caso perturbado** | Perturbar a matriz em 0,1%, 1% ou 10% **não muda nada** — o caminho só encurta em 25% e 50% |
| **A instância aleatória** | Mesmo tamanho, sem malícia: mediana de 2 a 7 pivôs, contra pior caso teórico de 31 a mais de um milhão |

A do meio é a que vale mais, e é um **resultado negativo**. A frase de corredor *"o pior caso é
frágil, qualquer perturbação desmancha"* não sobrevive à medição. Isso **não** refuta a análise
suavizada de Spielman & Teng (2004) — aquele teorema é assintótico, vale em esperança, supõe
perturbação gaussiana e outra regra de pivoteamento, e nenhuma das três condições vale aqui. O que
a medição refuta é a leitura popular do teorema, e o capítulo declara essa diferença em prosa. Há
teste que falha se a declaração sumir numa revisão de estilo.

## O que este diretório não reimplementa

Nem o Simplex nem o cubo. Os dois vêm de [`../etapa-03-simplex`](../etapa-03-simplex), por
`sys.path`. Reimplementar qualquer um deles criaria uma segunda fonte da verdade para números que
o livro **já publicou** no capítulo 09 — que é exatamente a classe de defeito que a
[ADR 0016](../../adr/0016-cadernos-colab-sem-deriva.md) proíbe nos cadernos, e que não tem por que
ser tolerada entre etapas.

## Contrato

- Aritmética exata (`fractions.Fraction`) em tudo. Nenhum ponto flutuante decide nada: um pivô a
  mais por arredondamento seria indistinguível de um pivô a mais por estrutura, e é a estrutura
  que está sendo medida.
- Semente declarada (`SEMENTE_BASE = 20260813`) e derivada por tamanho, de modo que rodar de novo
  reproduz os mesmos números.
- Roda em segundos numa máquina comum, sem rede e sem solver instalado.
