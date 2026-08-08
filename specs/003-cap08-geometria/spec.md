# Spec 003 — Capítulo 08: A geometria da Programação Linear

**Rodada:** 003 · **Raia:** plena · **Branch:** `claude/handbook-pesquisa-operacional-ucbbpu`
· **Data:** 2026-08-07 · **Status:** implementada, aguardando revisão do autor

> **Origem desta spec.** O conteúdo não é proposta minha: é a **narrativa de aula do autor**,
> passada em detalhe, e esta spec a registra. Onde eu decidi algo, está marcado como decisão de
> implementação — o resto é transcrição de sequência didática já testada em sala.

## O quê

Escrever o **capítulo 08 — A geometria da Programação Linear**, segundo capítulo da Parte II,
com o método gráfico completo: do significado de um ponto no plano até o sistema 2×2 que dá o
vértice ótimo exato.

Inclui, na mesma rodada, a **reescrita do capítulo 07** sobre o exemplo condutor do autor
(spec 002 v2). Os dois capítulos compartilham a instância, e publicar um sem o outro deixaria o
livro incoerente.

## Por quê

O capítulo anterior deixou uma pergunta em suspenso — *como é que se prova que aquele plano é o
melhor?* — e prometeu que este a responderia. Prometer e não cumprir é o defeito que a
constituição chama de omissão.

Além disso, é aqui que a intuição do Simplex é instalada. Quem enxerga a região viável e o
vértice de contato entende o algoritmo depois; quem não enxerga, decora.

## A narrativa (do autor)

1. **Cada variável ganha uma dimensão.** Duas dá; três complica; a partir de quatro é só
   matemática. O desenho é ferramenta de **entendimento**, não de trabalho.
2. **Pontos e o que significam.** Um ponto negativo seria devolução/desmonte — e não pode ser
   usado, senão há **escape infinito**. Entra $x_1 \ge 0$, hachurando o semiespaço direito;
   depois $x_2 \ge 0$, o semiespaço superior; a interseção é o primeiro quadrante.
3. **A laranja e a faca.** O espaço é uma bola fechada; a restrição é uma faca que a corta em
   dois semiespaços — um viável, onde as soluções moram, e outro descartado. Daí sai, sem
   fórmula, a propriedade: **restrição nunca aumenta a região viável; no máximo mantém**.
4. **Uma restrição, região viável, todos são solução — e então: qual é a melhor?** Entra a
   **iso-lucro**: o lucro é a *altura* do ponto, e caminhar sem subir nem descer é caminhar
   sobre uma iso-lucro.
5. **O objeto interativo.** O leitor sobe e desce a reta até o último valor que toca a região.
   Esse é o ponto de máximo, e ele é um **vértice** — a palavra entra como lacuna a preencher.
6. **A direção de crescimento** (gradiente), perpendicular à iso-lucro.
7. **Entra a segunda restrição.** Interseção, e o **ponto anterior sai da região**. Novo vértice
   ótimo: $(8, 2)$.
8. **O procedimento do aluno:** digitar as inequações, a expressão da iso-lucro, a direção do
   gradiente, caminhar até o vértice — e então **descobrir quais inequações sustentam o
   vértice**, transformá-las em equações e resolver o sistema. Esse é o ponto ótimo.

## Escopo

### Entra

- `livro/capitulos/08-geometria.md`, no esqueleto do Guia Editorial.
- **Ilha interativa** `regiao-viavel` — a substituta do GeoGebra da aula, dentro do livro.
- **10 exercícios** (`cap08`, A–J): cinco com o modelo dado, treinando o procedimento; cinco com
  enunciado, exigindo modelagem **e** resolução. Ambos com duas variáveis.
- `po-zero/etapa-02-metodo-grafico` — enumeração de vértices por pares, conferida contra o solver.
- Capacidade `geometria` no tutor.
- **Reescrita do capítulo 07** e da etapa 01 do `po-zero` sobre o exemplo do autor.

### Não entra

- Simplex, e qualquer coisa sobre percorrer vértices algoritmicamente.
- Dualidade e preço-sombra. O capítulo declara que o desenho dá o ponto e **não** dá o preço.
- Tratamento completo de degenerescência e múltiplos ótimos — aparecem como *teaser* (um
  exercício provoca o caso) e são endereçados no capítulo próprio.

## Decisões de implementação (minhas, não do autor)

1. **A ilha substitui o GeoGebra em vez de linká-lo.** Objeto externo quebra, exige cadastro e
   sai do controle editorial. A ilha faz as três interações da aula — ligar a segunda restrição,
   subir a iso-lucro, ler o vértice vencedor — e degrada para o texto sem JavaScript.
2. **Um exercício cai deliberadamente em múltiplos ótimos** (`exE`), com o objetivo paralelo a
   um lado. É o caso que o capítulo antecipa em "quando não serve", e é melhor o aluno topar
   com ele numa prática do que numa prova.
3. **Um exercício tem ótimo fracionário** (`exB`, com 1,5), para forçar a conversa sobre
   divisibilidade e sobre por que arredondar não resolve.
4. **Um exercício é de minimização com restrições `≥`** (`exJ`), para que o sentido da
   desigualdade venha do enunciado e não do costume.
5. **Num exercício, a restrição que sustenta o vértice é um eixo** (`exA`). É o erro que mais
   aparece: tratar a não-negatividade como formalidade e procurar o par "entre as restrições de
   verdade".

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| A1 | Capítulo publicado e no sumário | Página gerada e alcançável |
| A2 | A ilha monta e é interativa | Componente registrado em `viz/index.jsx`; bundle sem erro |
| A3 | Sem JavaScript, o leitor tem a mesma conclusão | A tabela de vértices e o texto em volta cobrem o conteúdo da ilha |
| A4 | 10 exercícios na série `cap08`, cada um com 3 a 5 critérios | Portão de exercícios verde |
| A5 | **Todas as dez respostas conferidas** por enumeração **e** por solver | Saída colada na verificação |
| A6 | Todo exercício rastreia a objetivo existente | Portão (verificado, não declarado) |
| A7 | `experimento.py` reproduz `resultados.json` byte a byte | Dupla execução |
| A8 | Enumeração e solver concordam nas três etapas | Saída do experimento |
| A9 | Capítulo 07 reescrito sobre o mesmo exemplo | Leitura: o 08 abre citando o resultado do 07 |
| A10 | Build e testes verdes | `npm run build` e `pytest -q` |

## Riscos

| Risco | Mitigação |
|---|---|
| O portão de exercícios limitava a bateria a 4 variantes (A–D) | Generalizado para A–Z. O limite era estado do livro de origem, não invariante deste |
| A regra "variante D é do leitor" vira arbitrária num banco de 10 | Substituída pelo campo `contexto` (`livro` \| `leitor`), que declara **natureza** em vez de **posição** |
| Ilha interativa virar enfeite | Ela responde a uma pergunta que o texto estático não responde bem: *o que acontece quando eu subo a reta?* Se não respondesse, não entraria |
| Dez exercícios com resposta errada | Todas as dez conferidas por dois caminhos independentes antes de escrever a rubrica |
