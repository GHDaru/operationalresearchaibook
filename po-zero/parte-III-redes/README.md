# Parte III — Redes e Fluxos

Serve os capítulos **16 a 22**. Cinco resultados medidos, todos em aritmética exata exceto a
simulação do PERT — que é estocástica por natureza, e lá o que se declara é a **semente**.

```bash
python3 redes.py            # imprime as cinco medições e regrava resultados.json
python3 -m pytest .         # a medição, e o vínculo com o texto publicado
```

## O que está medido

| # | O quê | O resultado |
|---|---|---|
| 1 | **Dijkstra com peso negativo** | Devolve **6**; o certo é **4**. E devolve o caminho `A→C→B→D`, que custa 4 — **a resposta contradiz a si mesma**, sem emitir aviso |
| 2 | **Bellman-Ford** | Acerta os 4, e detecta o ciclo negativo que faria uma busca ingênua rodar para sempre |
| 3 | **Max-fluxo = corte mínimo** | Os dois dão **15**, e o corte é exibido: três arestas. O teorema vira coisa que se olha |
| 4 | **Transporte, relaxação linear** | Custo **220**, **todos inteiros**, sem nenhuma restrição de integralidade. Com **uma** restrição transversal de pátio, o ótimo vira **223,33** e quatro embarques saem fracionários |
| 5 | **O mesmo gesto guloso** | Ótimo na árvore (**17**, conferido por enumeração de todas as árvores geradoras) e **14,3% pior** no roteiro (**32** contra **28**) |
| 6 | **Designação** | A relaxação linear devolve **0/1** sem nenhuma variável binária declarada |
| 7 | **PERT** | A fórmula publica **21 dias**; o projeto leva **24,48** em média, e **estoura a estimativa em 82,3%** das amostras |

## O item 5 merece o parágrafo que ele tem

A comparação ingênua — fórmula contra simulação — mistura **duas causas** num número só: a
distribuição amostrada não tem a mesma média que a fórmula supõe, **e** o projeto espera a mais
lenta das tarefas paralelas (*merge bias*). Só a segunda é defeito do método.

A isolação é feita **nas mesmas amostras**: para cada sorteio calculamos a duração real do projeto
e a duração do caminho que o CPM declarou crítico **antes** de sortear. Tudo o mais é idêntico, e
a diferença é o viés puro. Ele é **0,49 dia** — muito menor do que a comparação ingênua sugeriria,
e essa honestidade é o ponto.

E ele cresce com os ramos paralelos, com **controle**:

| Ramos | Viés | Estoura a estimativa em |
|---|---|---|
| **1** (controle) | **0,0** | 76,5% |
| 2 | 1,71 | 89,7% |
| 3 | 2,55 | 94,9% |
| 5 | 3,64 | 98,5% |
| 8 | 4,45 | 99,6% |

O caso `k = 1` tem de dar **exatamente zero** — sem paralelismo, a duração do projeto *é* a do
caminho declarado. Dar zero é o que prova que a isolação está correta, e não é sorte: é o controle
do experimento. Repare também que mesmo com um ramo só a estimativa estoura em 76,5% das amostras
— essa parte **não** é merge bias, é a distribuição, e o capítulo 22 separa as duas.

## Nota de método: dois erros meus, registrados

1. **O experimento da estrutura quebrada não quebrava nada.** A restrição escolhida deixava o
   modelo **inviável**, não fracionário, e passou porque a função devolvia o plano sem que ninguém
   olhasse o `status`. Hoje há `assert` explícito: experimento que não confere o próprio veredito
   mede outra coisa.
2. **A primeira versão do PERT comparava fórmula com simulação direto**, e teria publicado um viés
   de ~4,7 dias que é quase todo artefato da distribuição escolhida. O número honesto é 0,49.
3. **O primeiro grafo de cidades não sustentava a afirmação que ele existia para sustentar.** Eu
   escolhi os pesos à mão para o guloso errar o roteiro, e **ele acertou** — 17 contra 17. A
   instância publicada saiu de uma busca com semente declarada sobre 4.000 grafos aleatórios de
   cinco cidades, tomando a de maior perda relativa. **Procurar um contraexemplo é mais honesto do
   que arranjar um**, e mais rápido do que insistir num exemplo que não coopera.
