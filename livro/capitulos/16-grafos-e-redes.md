# 16 — Grafos e redes: fundamentos

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Reconhecer** um problema de rede num enunciado que não fala de rede, e nomear o que são
os nós e o que são as arestas.

**O2.** **Escolher** a representação — dirigida ou não, com capacidade ou com custo — a partir da
pergunta que se quer responder.

**O3.** **Decidir quando a lente de rede atrapalha**, e dizer o que usar no lugar.

## O problema

Boa parte da Pesquisa Operacional (PO) aplicada é rede por baixo, e quase nada dela **se
apresenta como rede**. (*"Boa parte"* é impressão editorial, e fica assim: este handbook não
levantou proporção nenhuma, e um número aqui seria inventado.) Escalonar turnos, alocar máquinas, planejar produção mês a mês, casar
candidatos com vagas: nenhum desses enunciados menciona grafo, e todos os quatro viram grafo com
uma tradução de duas linhas.

> **A habilidade desta Parte não é resolver rede. É enxergá-la.** Quem enxerga ganha acesso a
> métodos especializados e — o que esta Parte de fato mede — a **garantias** que o modelo genérico
> não tem. A vantagem de tempo é real e **não é medida aqui**: este handbook não cronometrou
> nenhum dos métodos desta Parte, e por isso não publica comparação de desempenho.

O erro caro deste capítulo:

> Alguém modela como Programação Linear genérica um problema que era de rede, e paga duas vezes:
> perde o método especializado **e** perde a integralidade de graça. O
> [capítulo 20](20-fluxo-custo-minimo.md) mede a segunda perda — a relaxação de um problema de
> rede devolve solução inteira sem que ninguém peça, e uma única restrição fora da estrutura
> destrói isso.

## De onde isto veio

### O aperto: sete pontes e uma pergunta sem resposta

O caso fundador é uma piada urbana virando matemática. Em Königsberg, no século XVIII, havia sete
pontes ligando duas ilhas às margens do rio, e a cidade se perguntava se dava para caminhar
passando por cada ponte **exatamente uma vez**.

A pergunta parece de passeio e é de estrutura. **A literatura didática credita a Euler**, em 1736,
a demonstração de que a resposta é não — atribuição corrente que este handbook **não confirmou em
fonte primária** —, e o modo como a demonstração funciona é a virada: ela **joga fora o mapa**. Distâncias, tamanhos, formatos
das ilhas, nada disso importava. Sobrou o que liga o quê, e a resposta caiu de uma contagem de
graus.

### O que se fazia antes, e a virada

Antes, um problema de conexão era um problema de **geometria**, e cada caso pedia um desenho
próprio. A virada foi perceber que existe uma camada abaixo do desenho — quem se liga a quem — e
que **muita pergunta se responde só nessa camada**.

### A ideia reaproveitável

> **Jogue fora tudo o que não muda a resposta.** A força de um grafo não está no que ele
> representa; está no que ele **se recusa** a representar.

Vale em qualquer modelagem, e é o mesmo gesto do [capítulo 03](03-anatomia-do-modelo.md): separar
o que é estrutura do que é decoração.

### A origem do nome

**"Grafo"** vem do inglês *graph*, no sentido de **diagrama** — e não de gráfico estatístico. A
literatura didática credita o cunho ao século XIX, na química, para os diagramas de ligação entre
átomos; **este handbook não confirmou essa origem em fonte primária**, e ela fica como atribuição
corrente. **"Nó"** e
**"aresta"** carregam a metáfora do desenho; a literatura em inglês usa *vertex* e *edge*, e a
tradução consagrada em português mistura as duas famílias sem prejuízo.

### Procedência

| Afirmação | Estado |
|---|---|
| As pontes de Königsberg e a resolução por Euler em 1736 | ⏳ **atribuição corrente**, repetida em toda a literatura didática; este handbook **não localizou** a fonte primária por identificador nesta rodada |
| A origem de *graph* como diagrama químico no século XIX | ⏳ **atribuição corrente**, não confirmada em fonte primária |
| Os números que os capítulos 17 a 22 publicam | ✓ **medidos** em `po-zero/parte-III-redes`, com teste que compara o texto publicado à medição |
| Qualquer vantagem de **tempo** dos métodos especializados | ❌ **não medida**. Este handbook não cronometrou nada nesta Parte, e por isso não publica comparação de desempenho |

> As duas primeiras linhas são `⏳` e ficam assim até alguém abrir a fonte. A história de
> Königsberg é boa demais para ser contada sem ressalva — **é justamente das histórias boas que o
> Princípio III desconfia**.

## O vocabulário, e só o necessário

| Termo | O que é | Onde aparece nesta Parte |
|---|---|---|
| **Nó** (ou vértice) | O que se conecta | Cidade, depósito, tarefa, pessoa, período |
| **Aresta** | A conexão | Estrada, rota, precedência, compatibilidade |
| **Dirigida** | A conexão tem sentido | Fluxo, precedência de tarefa |
| **Peso** | O número na aresta | Custo, distância, tempo, capacidade |
| **Caminho** | Sequência de arestas | [Capítulo 17](17-caminho-minimo.md) |
| **Ciclo** | Caminho que volta ao início | O que a árvore proíbe e o roteiro exige |
| **Corte** | Partição dos nós em dois lados | [Capítulo 19](19-fluxo-maximo.md) |
| **Árvore geradora** | Liga todos, sem ciclo | [Capítulo 18](18-arvore-geradora.md) |

**Duas escolhas de representação decidem quase tudo**, e as duas vêm da pergunta:

1. **A aresta tem sentido?** Se a resposta depende da direção — quem vem antes, para onde escoa —
   o grafo é dirigido. Escolher não dirigido quando importa direção é o erro silencioso desta
   Parte, porque o modelo continua rodando.
2. **O número na aresta é custo ou capacidade?** Custo se soma ao longo do caminho; capacidade
   limita o que passa. Trocar um pelo outro produz um modelo que responde a outra pergunta.

### Quatro problemas que não parecem rede

| O enunciado | Os nós | As arestas |
|---|---|---|
| Escalonar turnos de enfermagem | Turnos e enfermeiros | Quem pode cobrir o quê |
| Planejar produção em 6 meses | Cada mês | Produzir agora ou estocar para depois |
| Casar candidatos com vagas | Pessoas e vagas | Compatibilidades, com peso |
| Sequenciar tarefas de um projeto | Tarefas | Precedências ([capítulo 22](22-pert-cpm.md)) |

O segundo é o que mais surpreende: **estoque é aresta que atravessa o tempo**. Um problema de
planejamento multiperíodo vira rede pondo um nó por período e uma aresta "guardar" ligando cada
período ao seguinte — e aí ele herda tudo o que o [capítulo 20](20-fluxo-custo-minimo.md) prova.

## Quando não serve

**1. Quando a restrição não é sobre pares.** Grafo representa relação **binária**. *"Estas três
tarefas não podem acontecer no mesmo dia"* não é aresta — é restrição de conjunto, e forçá-la em
grafo perde informação.

**2. Quando o número na aresta depende do caminho.** Se o custo de uma estrada muda conforme
quanto já passou por ela — congestionamento —, o modelo deixa de ser de fluxo linear. O peso da
aresta tem de ser constante para os métodos desta Parte valerem.

**3. Quando o grafo é o modelo inteiro e a decisão não é sobre ele.** Desenhar o organograma como
grafo é bonito e não decide nada. Rede é ferramenta de **decisão**, e a pergunta do
[capítulo 02](02-ciclo-de-modelagem.md) continua valendo: quem vai decidir diferente por causa
disto?

**4. Quando a estrutura de rede não sobrevive às restrições reais.** É o caso mais caro, e tem
número: acrescentar **uma** restrição transversal ao transporte faz a integralidade de graça
desaparecer ([capítulo 20](20-fluxo-custo-minimo.md)). Modelar como rede um problema que **quase**
é rede entrega as garantias erradas.

## Fundamentos e fontes

**O que está medido aqui.** Nenhum número novo — este capítulo é de vocabulário. Os números que
ele antecipa saem de `po-zero/parte-III-redes` e são conferidos nos capítulos que os produzem.

**O que continua em dívida:** as pontes de Königsberg e a origem do termo *graph*, ambas `⏳`.

> 🟡 **Este capítulo está em v0.** Não passou por revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap16"></div>

Três exercícios. O primeiro traduz quatro enunciados que não falam de rede; o segundo escolhe a
representação a partir da pergunta; o terceiro é o mais difícil — reconhecer o caso em que a lente
de rede **não** serve.

## Assista

**[Pesquisa Operacional II - Aula 25 - Introdução à Teoria dos Grafos](https://www.youtube.com/watch?v=pbDHIMFGgLk)** ·
[UNIVESP](https://www.youtube.com/@univesptv) · 21min14s

**O que ele resolve:** este capítulo é deliberadamente econômico no vocabulário — ele apresenta só
os oito termos que a Parte III usa, e gasta o espaço na **tradução** de enunciados que não parecem
rede. O vídeo faz o percurso formal que falta aqui: definições, notação e as propriedades básicas
desenhadas no quadro.

## Síntese — o que levar

- **A habilidade desta Parte é enxergar a rede**, não resolvê-la. Quem enxerga ganha método e
  ganha garantia.
- **A demonstração atribuída a Euler jogou fora o mapa.** A força de um grafo está no que ele se
  recusa a representar.
- **Duas escolhas decidem quase tudo:** a aresta tem sentido? O número é custo ou capacidade?
- **Estoque é aresta que atravessa o tempo** — e é assim que planejamento multiperíodo vira rede.
- **Grafo representa relação binária.** Restrição sobre três coisas de uma vez não é aresta.
- **Modelar como rede o que quase é rede entrega a garantia errada** — e o capítulo 20 mede quanto
  isso custa.
- **Fora da Pesquisa Operacional:** jogue fora tudo o que não muda a resposta.

## Verificação

1. Uma transportadora quer decidir quantos veículos alocar a cada rota, sabendo quais rotas cada
   tipo de veículo consegue percorrer. Nomeie os nós e as arestas, e diga se o grafo é dirigido.
   *(O1)*
2. O mesmo mapa de estradas serve para responder "qual o caminho mais barato?" e "quanto consigo
   escoar por dia?". O que muda na representação entre as duas perguntas? *(O2)*
3. Um gerente pede para modelar como rede a regra *"estas três máquinas não podem operar
   simultaneamente"*. Explique por que não cabe, e diga o que fazer. *(O3)*

### Leitura executiva

Metade da Pesquisa Operacional aplicada é rede por baixo, e quase nada dela se apresenta como
rede: escalonar turnos, planejar produção mês a mês, casar candidatos com vagas e sequenciar
tarefas são todos grafos depois de uma tradução de duas linhas. A habilidade que esta Parte
ensina, portanto, **não é resolver redes — é enxergá-las**, e quem enxerga ganha duas coisas:
**métodos especializados**, que exploram a estrutura em vez de tratar o problema como um sistema
qualquer, e **garantias** que o modelo genérico não oferece — a principal delas medida no
capítulo 20. A vantagem de desempenho dos métodos especializados é real e consagrada, mas **este
handbook não a cronometrou**, e por isso não publica número.
O vocabulário necessário é curto — nó, aresta, direção, peso, caminho, ciclo, corte, árvore
geradora — e duas escolhas de representação decidem quase tudo, ambas derivadas da pergunta: a
aresta tem sentido, e o número nela é custo ou capacidade? Trocar custo por capacidade produz um
modelo que responde a outra pergunta sem avisar. A tradução mais surpreendente é a do planejamento
multiperíodo, em que **estoque vira aresta que atravessa o tempo**: um nó por período, uma aresta
"guardar" ligando cada um ao seguinte, e o problema herda tudo o que vale para fluxo. A lente falha
em quatro situações declaradas: quando a restrição não é sobre pares (grafo representa relação
binária, e "estas três não podem coincidir" não é aresta); quando o peso depende de quanto já
passou pela aresta, como em congestionamento; quando o grafo é bonito e não decide nada; e — o caso
mais caro — quando a estrutura de rede **quase** vale, porque aí o modelo entrega a garantia
errada, e o capítulo 20 mede exatamente quanto isso custa.
