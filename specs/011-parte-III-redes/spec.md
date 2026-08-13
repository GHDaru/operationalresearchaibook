# 011 — Parte III: Otimização em Redes e Fluxos

> Rodada de conteúdo. Sete capítulos (16 a 22), uma etapa de medição, um caderno.

## O quê

Publicar a Parte III inteira do handbook, sob a mesma régua da Parte I: bateria de três
exercícios, vídeo curado, seção "Quando não serve", seção "De onde isto veio" com procedência
declarada, selo de maturidade e — nos capítulos com número próprio — teste que compara o texto
publicado à medição.

## Por quê agora

A Parte III é a que **atravessa metade da PO aplicada**. Roteirização, escalonamento, alocação e
projeto de rede são todos redes por baixo, e nenhuma das Partes seguintes se sustenta sem ela. É
também a Parte em que o handbook pode medir o resultado mais bonito do campo — max-fluxo igual a
corte mínimo — em vez de citá-lo.

## Os cinco resultados que esta rodada mede

Nenhum deles é citação. Todos saem de `po-zero/parte-III-redes/`, em aritmética exata onde couber.

1. **Max-fluxo = corte mínimo**, medido numa instância: os dois números batem, e o corte é
   exibido. O teorema vira coisa que se olha.
2. **A relaxação linear do transporte devolve solução inteira** sem nenhuma restrição de
   integralidade — e **quebrar a estrutura de rede quebra isso**, com fração aparecendo na saída.
   É o resultado mais útil da Parte, e o que separa "inteiro é caro" de "inteiro é caro **quando
   a estrutura não ajuda**".
3. **Dijkstra devolve o caminho errado com peso negativo**, e Bellman-Ford devolve o certo. O
   "quando não serve" do capítulo 17 medido, e não afirmado.
4. **Bellman-Ford detecta o ciclo negativo** que faria uma busca ingênua rodar para sempre.
5. **PERT subestima o prazo**, e o erro cresce com o número de caminhos paralelos. Medido por
   simulação com semente declarada, contra a fórmula que o método publica.

## Critérios de aceite

- [ ] Sete capítulos publicados, cada um com ≥3 exercícios e ≥1 vídeo curado com ficha conferida.
- [ ] `npm run build` verde, com todos os portões.
- [ ] `pytest po-zero -q` verde, com teste que lê cada capítulo 🔵 e confere os números.
- [ ] Nenhuma afirmação histórica sem estado de procedência declarado no corpo **e** na tabela.
- [ ] Caderno da Parte III, sob as sete regras da ADR 0016.
- [ ] Revisão em contexto fresco, com os achados reconferidos por medição própria antes de aceitos.
