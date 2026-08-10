# Spec 004 — Capítulo 09: O método Simplex

**Rodada:** 004 · **Raia:** plena · **Branch:** `claude/handbook-pesquisa-operacional-ucbbpu`
· **Data:** 2026-08-09 · **Status:** **clarify respondido pelo autor — aprovada para implementar**

> **Esta spec é proposta, não transcrição.** Nos capítulos 07 e 08 o conteúdo veio da narrativa
> de aula do autor. Aqui eu não tenho essa narrativa: o que segue é uma **proposta** montada a
> partir do que os capítulos anteriores deixaram no lugar. Os pontos em que a decisão é do autor
> estão isolados em [§Perguntas de clarify](#perguntas-de-clarify) — **e a implementação não
> começa antes de eles serem respondidos.**

## O quê

Escrever o **capítulo 09 — O método Simplex**, terceiro capítulo da Parte II: o algoritmo por
dentro — forma padrão, base, critério de entrada, teste da razão, pivoteamento e critério de
parada — com a mesma instância da montadora que atravessa os capítulos 07 e 08.

## Por quê

O capítulo 08 termina numa afirmação e numa impossibilidade, nesta ordem:

- **A afirmação:** se existe ótimo, existe um vértice ótimo — logo, nunca é preciso procurar
  fora das quinas.
- **A impossibilidade:** acima de três variáveis não há desenho. "A partir daí, o que resta é o
  algoritmo" — é a última frase da síntese.

O Simplex é exatamente a conversão de uma na outra: **percorrer vértices sem enxergá-los**. Um
capítulo aqui não é "mais um método"; é o cumprimento de uma promessa que o livro já fez em
letra publicada.

Há ainda uma dívida pedagógica específica. O capítulo 07 refutou duas regras gulosas — produzir
só o de maior lucro unitário parecia óbvio e estava errado. O Simplex escolhe quem entra na base
por uma regra **igualmente gulosa** (o maior coeficiente). O leitor atento vai desconfiar, e com
razão. O capítulo precisa responder por que aqui a ganância não engana: porque ela decide só a
*direção*, e quem decide o *quanto* é o teste da razão — e porque o processo **itera**.

## A proposta de narrativa

1. **O problema: o desenho acabou.** Cinco variáveis, e não há papel. Enumerar todos os vértices
   também não serve — o capítulo mostra o número de combinações crescendo e por que a força
   bruta morre cedo. É preciso um jeito de **andar de vértice em vértice sempre subindo**.
2. **A intuição, sobre o desenho do capítulo 08.** No mesmo gráfico da montadora: comece na
   origem, escolha uma aresta que sobe, ande por ela **até bater na primeira restrição**, repita.
   Quando nenhuma aresta sobe, acabou. O algoritmo inteiro, antes de qualquer notação.
3. **A matemática: a forma padrão e a base.** A folga deixa de ser "o que sobrou" (leitura do
   capítulo 08) e vira **variável**. Desigualdade vira igualdade; o sistema fica com mais
   incógnitas que equações; escolher quais zerar é escolher um vértice. **Vértice = solução
   básica viável** — a ponte central do capítulo, e a razão de ele vir depois do 08.
4. **O algoritmo, passo a passo.** Quem entra (custo reduzido), quem sai (teste da razão),
   pivoteamento, critério de parada. Percorrido à mão na montadora: $(0,0) \to (0,6) \to (8,2)$,
   duas iterações, chegando ao mesmo R$ 1.100 que o desenho deu. **O leitor vê o algoritmo
   pisar nos vértices que ele mesmo desenhou.**
5. **Por que a ganância funciona aqui.** A resposta à dívida do capítulo 07, acima.
6. **O código:** `po-zero/etapa-03-simplex` — Simplex didático em NumPy, iteração a iteração,
   com a sequência de vértices impressa e conferida contra o HiGHS.
7. **Quando não serve.** Pior caso exponencial (Klee–Minty); instâncias grandes e esparsas onde
   pontos interiores ganham; ciclagem em degenerescência; e o aviso de que **este** Simplex, de
   quadro, não é o que o solver executa — o que abre os capítulos 11 e 14.

## Escopo

### Entra

- `livro/capitulos/09-simplex.md`, no esqueleto do Guia Editorial.
- **Mínimo de 5 exercícios** (`cap09`), com pelo menos um de cada tipo: executar uma iteração,
  ler um quadro e dizer em que vértice se está, diagnosticar uma escolha errada de quem sai.
- `po-zero/etapa-03-simplex` — implementação didática + conferência contra solver.
- Capacidade `simplex` no tutor, nos dois lados do espelho.
- Um vídeo curado.
- Entradas novas no glossário: base, variável básica, custo reduzido, pivoteamento, quadro.

### Não entra

- **Ilimitado, inviável, múltiplos ótimos e ciclagem** — são o capítulo 10. Aqui aparecem
  apenas como o que o critério de parada *não* cobre, com ponteiro.
- Forma matricial, fatoração e Simplex revisado — capítulo 11.
- Dualidade e preço-sombra — capítulo 12. O capítulo declara que o quadro final **já contém**
  essa informação e que o livro ainda não vai lê-la.

## Clarify — respondido pelo autor em 2026-08-09

| # | Pergunta | Resposta | O que muda |
|---|---|---|---|
| 1 | Veículo: quadro (*tableau*) ou forma algébrica? | **Quadro** | O capítulo ensina pelo quadro, que é o que a sala pratica e o que cai em prova. A álgebra aparece só onde é necessária para dar sentido ao quadro — a forma matricial fica para o capítulo 11 |
| 2 | Onde entra a Fase I / *big-M*? | **Neste capítulo 09** | O Simplex fica completo num lugar só: partida, iteração e parada. Exige uma segunda instância, em que a origem **não** é viável |
| 3 | Existe narrativa de sala? | **Não — seguir a proposta** | A narrativa acima é a implementada. Fica registrado que ela é minha, e não sequência testada em sala como nos capítulos 07 e 08 |

### Consequência da resposta 2: a segunda instância

Big-M precisa de uma instância cuja origem seja inviável, e ela deve nascer da **mesma história**
— trocar de contexto no meio do capítulo custa mais do que ganha. A escolhida é a montadora com
um **compromisso já vendido**: o cliente comprou 5 unidades do Tipo 2, o que impõe
$x_2 \ge 5$ e tira a origem da região viável.

O ganho pedagógico é duplo: o leitor vê a partida artificial **e** vê o preço do compromisso —
o ótimo cai de R$ 1.100 para R$ 950, e essa diferença é uma decisão de negócio, não um detalhe
de álgebra.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| A1 | Capítulo publicado e no sumário | Página gerada e alcançável |
| A2 | A sequência de vértices do texto é a que o código produz | `resultados.json`, citado número a número |
| A3 | O Simplex didático e o HiGHS concordam na instância da montadora | Saída do experimento |
| A4 | ≥5 exercícios na série `cap09`, 3 a 5 critérios cada | Portão de exercícios verde |
| A5 | **Toda resposta afirmada foi verificada por execução**, não por leitura | Saída colada na verificação |
| A6 | Todo exercício rastreia a objetivo existente | Portão (verificado, não declarado) |
| A7 | `experimento.py` reproduz `resultados.json` byte a byte | Dupla execução |
| A8 | Seção "quando não serve" presente e específica | Leitura; Princípio II |
| A9 | Build e testes verdes | `npm run build` e `pytest -q` |

## Riscos

| Risco | Mitigação |
|---|---|
| **Repetir a falha da rodada 002** — implementar sem a narrativa do autor | Esta spec **para no gate**. Nenhuma linha de capítulo antes das três respostas |
| Exercício com resposta errada (foi o defeito da edição 0.6) | Nenhuma resposta entra na rubrica sem sair de execução. O portão de consistência previsto no roadmap entra nesta rodada |
| O capítulo virar receita de quadro sem sentido | O item 3 da narrativa (vértice = solução básica viável) é o teste: se o leitor não sai sabendo *o que a base é geometricamente*, o capítulo falhou |
| Fase I ficar órfã entre os capítulos 09 e 10 | É a pergunta 2 do clarify, decidida antes de escrever |
| Vídeo sem autoria conferida, como nos capítulos 07 e 08 | Dívida já declarada; se o canal autorizado cobrir Simplex, ela fecha nesta rodada |

---

## Emenda em curso de rodada — Princípio XII (2026-08-09)

Depois de a implementação estar pronta e antes do merge, o autor leu o capítulo e pediu uma
mudança que **não é ajuste, é requisito novo**: todo método precisa da sua história — o aperto
que o motivou, a ideia por trás do artifício, a origem do nome. *"Não quero passar decoreba."*

Isso virou o **Princípio XII** da constituição (1.1.0, [ADR 0006](../../adr/0006-o-metodo-tem-historia.md)),
com seção obrigatória no esqueleto de capítulo e portão no build.

**Por que absorvi na rodada 004 em vez de abrir a 005.** O capítulo 09 é o motivo do pedido e
ainda não está publicado; entregá-lo sem a seção seria publicar sabendo que está incompleto pela
régua vigente. A cadência de uma rodada por capítulo continua respeitada — o que mudou foi o
escopo desta, e está registrado aqui em vez de crescer em silêncio.

**Escopo acrescentado:**

- Seção *De onde isto veio* no capítulo 09: SCOOP e 1947, *programming* como termo militar de
  planejamento, o nome sugerido por Motzkin, e a origem e a **ideia** do *big-M*.
- Tabela que separa **documentado** / **atribuição corrente** / **leitura deste livro**, com
  admissão explícita da lacuna sobre a origem da letra M.
- Seção *História dos métodos* na bibliografia, com as fontes em `⏳`.
- Portão no `verifica-capitulos.mjs`, com dívida retroativa declarada para os capítulos 07 e 08.
