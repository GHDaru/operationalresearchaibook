# Spec 008 — Capítulo 11: Simplex revisado e implementação eficiente

**Data:** 2026-08-12 · **Raia:** plena · **Estado:** **aguardando ratificação do autor**

## Por que este capítulo, e por que agora

Não é escolha de sumário: **os capítulos publicados já contraíram a dívida**, por escrito, e o
leitor que chegou ao fim do 10 está segurando duas promessas.

> **Capítulo 09**, "quando não serve", item 2 — *"Esta implementação recalcula a tabela inteira a
> cada iteração. Num modelo com milhares de restrições, quase todas com coeficiente zero, isso é
> desperdício de memória e de precisão. Solvers usam a **forma revisada**, que mantém só o que
> precisa e refatora — capítulo 11."*

> **Capítulo 10**, "quando não serve", item 5 — *"ciclagem é rara; **estagnação** é comum.
> Tratá-la exige a forma revisada e as escolhas de implementação do capítulo 11."*

E há uma terceira, feita no item 4 do mesmo capítulo e não endereçada a ninguém: em ponto
flutuante o arredondamento *"troca um problema honesto por um pior, o de decidir se dois números
'iguais' são iguais"*. **Esse problema é deste capítulo.**

## A pergunta que o capítulo responde

**Por que o solver real não faz o que o quadro faz?**

O leitor sai do capítulo 09 sabendo pivotear e sai do 10 sabendo ler vereditos. Os dois usaram um
quadro que recalcula tudo, em aritmética exata, num problema com duas variáveis. Nenhum solver do
mundo faz isso — e o aluno que não souber por quê vai achar que a diferença é detalhe de
engenharia. Não é: é a diferença entre um método didático e um método que resolve modelo de
verdade.

## Objetivos de aprendizagem

| # | Ao fim do capítulo, o leitor consegue |
|---|---|
| **O1** | Escrever o Simplex em **forma matricial** e dizer o que cada peça faz — $B$, $B^{-1}$, custo reduzido por preço-sombra |
| **O2** | Explicar por que manter $B^{-1}$ e **refatorar** custa menos que recalcular o quadro, e **em que instâncias** isso deixa de ser verdade |
| **O3** | Reconhecer **esparsidade** como propriedade do modelo, e não do algoritmo, e dizer o que ela muda |
| **O4** | Diagnosticar **estagnação** e distingui-la de ciclagem e de lentidão — encadeando no capítulo 10 |
| **O5** | Explicar por que a **tolerância numérica** é decisão de modelagem, e o que dá errado quando ela é escolhida por acaso |

## O que a rodada mede (Princípio IV)

Uma etapa nova do `po-zero`, `etapa-05-revisado`, que **não** ensina um método novo: ela mostra o
**mesmo** método, escrito de outro jeito, e mede a diferença. A comparação é contra a etapa 03,
que está publicada.

| Medição | O que ela prova |
|---|---|
| Forma revisada e quadro dão **a mesma resposta** nas instâncias das etapas 03 e 04 | O capítulo é sobre implementação, não sobre método. Se a resposta mudar, o capítulo está errado |
| **Contagem de operações** e de valores tocados por iteração, nas duas formas, em instâncias de tamanho crescente | O ganho da forma revisada deixa de ser afirmação e vira curva |
| **Densidade** da matriz nas instâncias sintéticas | Mostra que o ganho depende da esparsidade — e some quando ela some |
| A mesma instância em **`Fraction` e em `float`** | O item 4 do capítulo 10, pago: onde o arredondamento muda o veredito |
| Uma instância que **estagna** — muitas iterações sem melhora, e finitas | Separa estagnação de ciclagem com o instrumento, não com a prosa |

**Compromisso de honestidade, declarado antes de medir:** se a forma revisada **não** ganhar nas
instâncias que este handbook consegue construir em CPU, isso entra no capítulo como resultado. O
livro não vai afirmar um ganho que o experimento não mostrar — e a explicação, nesse caso, passa
a ser *por que o ganho só aparece em escala que não cabe aqui*, o que também é conteúdo.

## Critérios de aceite

| # | | Critério |
|---|---|---|
| **A1** | M | ≥3 exercícios com devolutiva que explica, cada um rastreando a um objetivo; ≥1 vídeo curado |
| **A2** | M | Seção **"De onde isto veio"** (Princípio XII), com a ideia reaproveitável declarada |
| **A3** | M | Seção **"quando não serve"** (Princípio II) |
| **A4** | M | `po-zero/etapa-05-revisado` regenera todos os números do capítulo por script, com saída determinística |
| **A5** | M | A forma revisada devolve **a mesma resposta** que a etapa 03 em todas as instâncias publicadas — verificado por comparação, não por leitura |
| **A6** | M | As **duas dívidas** dos capítulos 09 e 10 são pagas e o texto diz de onde vieram |
| **A7** | M | Build verde, `verifica-fontes` verde, 24+ testes do tutor verdes |
| **A8** | M | Capacidade nova do tutor nos dois lados do espelho |
| **A9** | H | `HISTORICO.md`, `videoteca.md`, `glossario.md`, `bibliografia.md` e Radar atualizados |
| **A10** | H | **Revisão em contexto fresco** |
| **A11** | M | Toda fonte nova com DOI passa pelo portão da rodada 007 — **é o primeiro capítulo que nasce sob o portão** |

## Perguntas de clarify — vão ao autor

Estas eu **não** resolvo sozinho, porque mudam o que o capítulo é.

**C1 — Qual é o piso de álgebra linear?** A forma revisada exige matriz inversa e resolução de
sistema. O handbook nunca exigiu isso do leitor até aqui: o capítulo 08 foi geométrico e o 09 foi
aritmético. Três posições possíveis, e elas produzem capítulos diferentes:
*(a)* assumir álgebra linear e seguir em notação matricial;
*(b)* construir a ponte dentro do capítulo, gastando espaço com $B^{-1}$;
*(c)* ficar em nível de ideia, sem inverter matriz explicitamente, e mandar o rigor para a etapa
do `po-zero`.

**C2 — Fatoração LU entra?** É o que os solvers de verdade fazem, e é o passo que explica
"refatorar". Mas é um capítulo inteiro de métodos numéricos se for feito com rigor. Entra como
**caixa-preta com consequência declarada**, ou como conteúdo?

**C3 — Regras de precificação** (*Dantzig, steepest edge, devex*) entram aqui ou viram o miolo do
capítulo 13? O capítulo 10 já ensinou que trocar a regra muda o caminho e pode mudar qual ótimo
se recebe; *devex* é a continuação natural dessa conversa, mas também é assunto de desempenho.

**C4 — Até onde vai a conversa sobre ponto flutuante?** O item 4 do capítulo 10 abriu a porta.
Fechar essa dívida com honestidade custa espaço, e o risco é o capítulo virar aula de análise
numérica em vez de aula de Pesquisa Operacional (PO).

## Riscos que a spec já enxerga

| Risco | Por que importa |
|---|---|
| **Virar capítulo de engenharia de software** | O leitor é aluno de PO. A pergunta é "por que o solver não faz o que eu fiz", não "como escrever um solver" |
| **Afirmar ganho sem medir** | Já declarado acima: o compromisso é publicar o que o experimento mostrar |
| **A etapa 05 duplicar a 03** | A 03 foi parametrizada na rodada 006 em vez de duplicada. A 05 deve reusar `Restricao`, `CustoM` e as instâncias — e a comparação exige que as duas leiam a **mesma** entrada |
| **Estagnação virar palavra** | Se o experimento não produzir uma instância que estagne de verdade, o capítulo não pode ensinar a diagnosticá-la |
