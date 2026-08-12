# Glossário

> **Conteúdo revisado em 2026-08** · os termos e as siglas do handbook, abertos.

Política: **toda sigla é apresentada por extenso na primeira ocorrência de cada documento**
(constituição, Princípio IX). Este glossário é a rede de segurança — e o espelho do mapa de
siglas do motor (`publicar/build.mjs`), que envolve cada sigla conhecida em `<abbr>` para que
passar o mouse revele o significado em qualquer ocorrência.

Ao introduzir uma sigla nova, adicione-a **nos dois lugares**.

## Siglas

| Sigla | Por extenso | O que é |
|---|---|---|
| **PO** | Pesquisa Operacional | O campo: métodos quantitativos para decisão em sistemas |
| **PL** | Programação Linear | Otimização com objetivo e restrições lineares em variáveis contínuas |
| **PI** | Programação Inteira | Otimização em que variáveis são obrigadas a assumir valores inteiros |
| **LP** | *Linear Programming* | O mesmo que PL, na literatura em inglês |
| **MILP** | *Mixed Integer Linear Programming* | Programação linear inteira mista: variáveis contínuas e inteiras no mesmo modelo |
| **MINLP** | *Mixed Integer Nonlinear Programming* | O caso não linear da anterior; sem garantia geral de ótimo global |
| **B&B** | *Branch and Bound* | Enumeração com poda por limitantes: o algoritmo exato padrão da PI |
| **B&C** | *Branch and Cut* | *Branch and bound* com planos de corte gerados durante a busca |
| **KKT** | Karush-Kuhn-Tucker | As condições necessárias de otimalidade em problemas com restrições |
| **VRP** | *Vehicle Routing Problem* | Problema de roteamento de veículos, e sua família de variantes |
| **TSP** | *Travelling Salesman Problem* | Problema do caixeiro-viajante |
| **CP** | *Constraint Programming* | Programação por restrições: paradigma de propagação e busca |
| **SA** | *Simulated Annealing* | Metaheurística de trajetória inspirada no recozimento de metais |
| **TS** | *Tabu Search* | Busca Tabu: busca local com memória de curto prazo |
| **ILS** | *Iterated Local Search* | Busca local iterada com perturbação |
| **VNS** | *Variable Neighborhood Search* | Busca em vizinhança variável |
| **GRASP** | *Greedy Randomized Adaptive Search Procedure* | Construção gulosa aleatorizada seguida de busca local |
| **LNS** | *Large Neighborhood Search* | Busca em vizinhança grande: destrói e repara parte da solução |
| **ALNS** | *Adaptive Large Neighborhood Search* | LNS com pesos adaptativos entre operadores |
| **ACO** | *Ant Colony Optimization* | Otimização por colônia de formigas |
| **PSO** | *Particle Swarm Optimization* | Otimização por enxame de partículas |
| **AG** | Algoritmo Genético | Metaheurística populacional baseada em seleção, cruzamento e mutação |
| **MDP** | *Markov Decision Process* | Processo de decisão de Markov |
| **PD** | Programação Dinâmica | Decomposição recursiva por estágios e estados |
| **DEA** | *Data Envelopment Analysis* | Análise Envoltória de Dados: eficiência relativa entre unidades |
| **AHP** | *Analytic Hierarchy Process* | Método multicritério por comparação par a par |
| **TOPSIS** | *Technique for Order of Preference by Similarity to Ideal Solution* | Método multicritério por distância ao ideal |
| **EOQ** | *Economic Order Quantity* | Lote econômico de compra |
| **CPM** | *Critical Path Method* | Método do caminho crítico |
| **PERT** | *Program Evaluation and Review Technique* | Avaliação de projetos com duração probabilística |
| **ML4CO** | *Machine Learning for Combinatorial Optimization* | Uso de aprendizado de máquina em otimização combinatória |
| **ML** | *Machine Learning* | Aprendizado de máquina |
| **RL** | *Reinforcement Learning* | Aprendizado por reforço |
| **LLM** | *Large Language Model* | Modelo de linguagem de grande porte |
| **RAG** | *Retrieval-Augmented Generation* | Geração com recuperação de trechos da fonte |
| **DoD** | *Definition of Done* | Os critérios que definem "pronto", verificáveis |
| **ADR** | *Architecture Decision Record* | Registro de decisão de arquitetura |
| **DOI** | *Digital Object Identifier* | Identificador persistente de publicação |
| **ISBN** | *International Standard Book Number* | Identificador de livro |
| **API** | *Application Programming Interface* | Interface de programação de aplicações |
| **CPU** | *Central Processing Unit* | Unidade central de processamento |
| **GB** | *gigabyte* | Unidade de capacidade de memória |
| **JSON** | *JavaScript Object Notation* | Formato de arquivo de dados usado pelas instâncias do `po-zero` |

## Termos

**Variável de decisão.** O que o modelo pode escolher. Se algo no problema não pode ser
escolhido por quem decide, não é variável de decisão — é parâmetro.

**Função objetivo.** A medida única que o modelo maximiza ou minimiza. Um modelo com dois
objetivos genuínos não tem função objetivo: tem um problema multiobjetivo.

**Restrição.** O que limita as combinações admissíveis. Restrição que nunca é violada em
nenhuma solução plausível é restrição redundante — custa tempo de solver e não muda a resposta.

**Região viável.** O conjunto de soluções que satisfazem todas as restrições. Vazia significa
modelo inviável, e quase sempre é erro de formulação, não do mundo.

**Folga.** A distância entre o lado esquerdo e o direito de uma restrição na solução. Folga
zero significa restrição **ativa** — é ela que está segurando o resultado.

**Preço-sombra.** Quanto o valor ótimo melhora por unidade adicional do recurso de uma
restrição ativa. Vale **apenas dentro de uma faixa**, e ler fora dela é o erro clássico de
interpretação.

**Forma padrão.** O modelo reescrito só com igualdades e com todas as variáveis não-negativas.
Não muda o problema — é a mesma coisa dita numa língua que a álgebra linear sabe processar.

**Variável de folga.** A folga promovida a variável do modelo, para que uma desigualdade `≤`
vire igualdade. Fora da base significa recurso esgotado; na base, recurso sobrando.

**Variável artificial.** Variável sem significado físico, introduzida só para dar uma base de
partida a restrições `≥` ou `=`. Entra na função objetivo com multa (ver *big-M*). Se ainda
estiver na base ao final, com valor positivo, o modelo é **inviável**.

***Big-M*.** A multa dada às variáveis artificiais, com $M$ maior que qualquer valor do
problema. Tratado como **símbolo**, não como número: escolher um valor concreto pequeno demais
faz um modelo inviável devolver resposta com cara de ótima.

**Base.** O conjunto de variáveis que o sistema determina; as demais são fixadas em zero. Tem
tamanho igual ao número de restrições.

**Solução básica viável.** Solução obtida de uma base, com todas as variáveis não-negativas.
**É o mesmo objeto que a geometria chama de vértice** — a ponte que o método Simplex atravessa.

**Custo reduzido.** Quanto o objetivo muda por unidade de uma variável que hoje está fora da
base. Negativo (num problema de maximizar, na convenção deste livro) significa que ainda há
como melhorar; nenhum negativo é o critério de parada.

**Pivoteamento.** Trocar uma variável da base por uma de fora, por eliminação de Gauss. No
desenho, é andar por uma aresta até o vértice vizinho.

**Teste da razão.** A conta que decide qual variável sai da base: a menor razão positiva entre
lado direito e coeficiente da coluna que entra. Não é convenção — é a única escolha que
preserva a viabilidade.

**Vértice degenerado.** Vértice sustentado por mais restrições do que o necessário — no plano,
três retas passando pelo mesmo ponto. Na álgebra, aparece como **variável básica valendo zero**.
É comum e legítimo: bandeira amarela, não defeito. Costuma indicar restrição redundante, e torna
a leitura de preço-sombra ambígua.

**Ciclagem.** O método pivoteia, troca a base, refaz o quadro e **não sai do ponto** — e, se uma
base já visitada voltar, gira para sempre. Exige degenerescência, mas não decorre dela: é defeito
da **regra de pivoteamento**, não do modelo. Rara na prática, e construída de propósito nos
exemplos que a exibem.

***Stalling*** (estagnação). Uma sequência **longa, porém finita**, de iterações sem melhora do
objetivo. É o problema prático comum — ao contrário da ciclagem, que é o problema de livro-texto.

**Regra de pivoteamento.** O critério que decide quem entra e quem sai da base. A de **Dantzig**
escolhe o custo reduzido mais negativo e é rápida; a de **Bland** escolhe por menor índice na
entrada e na saída, e garante terminação ao custo de mais iterações. Trocar de regra **nunca muda
o valor ótimo** — mas pode mudar **qual** plano ótimo você recebe, quando há mais de um, e muda
quantos passos se gasta para chegar lá.

**Convexidade.** Propriedade de um conjunto em que o segmento entre dois pontos quaisquer está
inteiro dentro dele. É o que garante, num problema linear, que todo ótimo local é global — e é
por isso que o Simplex pode parar no primeiro vértice de onde nada melhora.

**Dualidade.** A cada modelo de otimização corresponde um modelo espelho cujas variáveis são
os preços das restrições do original. Não é curiosidade teórica: é o que dá interpretação
econômica à resposta e sustenta boa parte dos algoritmos.

**Relaxação.** Uma versão mais permissiva do problema — tipicamente removendo a exigência de
integralidade. Sua solução é um **limitante** para a do problema original, e é assim que se
mede quão boa é uma solução sem conhecer o ótimo.

**Limitante (*bound*).** Um valor que garantidamente limita o ótimo por cima ou por baixo. É o
que permite dizer "esta solução está a no máximo 2% do ótimo" — a única forma honesta de
declarar qualidade sem o ótimo em mãos.

**Heurística.** Método que busca boa solução sem garantia de otimalidade. Não é o método dos
preguiçosos: é o método de quem escolheu qualidade suficiente em tempo aceitável.

**Metaheurística.** Estratégia geral que orquestra heurísticas de busca, aplicável a famílias
de problemas. Divide-se em métodos de **trajetória** (uma solução por vez) e **populacionais**.

**Instância.** Um caso concreto de um problema, com dados. Algoritmo não é rápido ou lento em
abstrato — é rápido ou lento **num conjunto de instâncias declarado**.

**Solver.** O programa que resolve o modelo. Neste handbook, a trilha padrão usa solver aberto:
custo zero é requisito, não preferência.

**Semiespaço.** Cada um dos dois pedaços em que uma restrição de desigualdade corta o espaço. A
imagem do capítulo de geometria: a restrição é uma faca que atravessa a laranja de lado a lado.
Um semiespaço fica, o outro é descartado — e é daí que decorre que **restrição nunca aumenta a
região viável**.

**Vértice.** Uma quina da região viável: o ponto onde duas restrições (em duas dimensões) se
encontram como igualdades. Importa por um motivo só, e ele sustenta toda a Parte II: **se existe
ótimo, existe um vértice ótimo** — nunca é preciso procurar fora das quinas.

**Reta de iso-lucro.** O conjunto dos planos que rendem o mesmo. É a curva de nível do objetivo:
andar sobre ela é andar sem subir nem descer. Subi-la até o último contato com a região viável é
o método gráfico.

**Gradiente.** O vetor dos coeficientes da função objetivo. Aponta a direção em que o objetivo
cresce mais rápido, e é **perpendicular** à reta de iso-lucro — porque andar ao longo dela não
muda o valor.

**Lista de materiais.** A relação de quanto de cada componente uma unidade de cada produto
consome. Num modelo de otimização ela **é** a matriz de coeficientes das restrições — ver isso é
ver que a formulação tem forma.

**Cláusula de expiração.** A declaração, num capítulo da camada de fronteira, da data a partir
da qual sua afirmação precisa ser reverificada. Sem ela, um capítulo de fronteira não é
publicável.
