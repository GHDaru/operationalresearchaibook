# Estudo 002 — De onde vieram os métodos

> **Pesquisa capturada em 2026-08-09** · insumo da rodada `005-historia-dos-metodos` · autor:
> Gilsiley Henrique Darú, com apoio de agente de IA.

Este documento é o **insumo das seções "De onde isto veio"** dos capítulos que ainda vêm
(constituição, [Princípio XII](../.specify/memory/constitution.md)). Não é capítulo de livro: é
nota de pesquisa, e nem tudo aqui vai virar texto publicado.

Ele existe por uma razão prática. Pesquisar história capítulo a capítulo sai caro e sai
incoerente — as histórias se conectam, e quem descobre a conexão depois já publicou os dois lados
sem ela. O caso exemplar já aconteceu: **Motzkin** aparece no capítulo 08, redescobrindo a
eliminação de Fourier, e reaparece no 09, batizando o Simplex. A conexão só apareceu porque as
duas pesquisas foram feitas juntas.

## Como ler os selos

| Selo | Significa |
|---|---|
| ✓ | **Fonte aberta e lida.** O que está afirmado foi conferido no texto |
| ✓ᵐ | **Só os metadados** foram conferidos (autor, obra, ano, DOI). O conteúdo não foi lido |
| ⏳ | **Atribuição corrente**, repetida na literatura didática, **não confirmada em fonte primária** |
| ❌ | Procurei e **não achei fonte** |
| 📖 | **Leitura editorial** — interpretação deste handbook, não afirmação histórica |

A regra do Princípio XII vale aqui inteira: **inventar história é pior do que omiti-la**, porque
é convincente. Onde há dúvida, ela está escrita.

---

## 1. Para a Parte II — o que falta da Programação Linear

### 1.1 Capítulo 10 — degenerescência e ciclagem

**A fonte primária existe e é antiga.** ✓ᵐ CHARNES, A. "Optimality and Degeneracy in Linear
Programming". *Econometrica*, v. 20, n. 2, p. 160, 1952.
DOI [10.2307/1907845](https://doi.org/10.2307/1907845).

É o mesmo artigo a que a literatura didática atribui o *big-M* (⏳, ver capítulo 09). Vale abrir
uma vez e resolver as duas dívidas de atribuição de uma tacada.

**A saída para a ciclagem tem data e nome.** ✓ᵐ BLAND, Robert G. "New Finite Pivoting Rules for
the Simplex Method". *Mathematics of Operations Research*, v. 2, n. 2, p. 103–107, 1977.
DOI [10.1287/moor.2.2.103](https://doi.org/10.1287/moor.2.2.103).

📖 **O ângulo editorial que este capítulo pede.** A ciclagem é o caso em que o algoritmo faz tudo
certo e não sai do lugar — e a solução de Bland é deliciosamente anticlimática: **desempate pelo
menor índice**. Uma regra arbitrária, sem nenhuma justificativa de eficiência, que existe apenas
para garantir terminação. É um bom lugar para ensinar que *garantia* e *desempenho* são coisas
diferentes, e que às vezes se paga uma pela outra.

### 1.2 Capítulo 12 — dualidade

⏳ **A história que a literatura conta**, e que eu **não** consegui confirmar: em outubro de 1947,
Dantzig teria apresentado seu problema a **John von Neumann**, em Princeton. Von Neumann teria
cortado a explicação, dito algo como "vá direto ao ponto", e então discorrido por mais de uma hora
sobre a teoria de dualidade — porque vinha da teoria dos jogos, onde a estrutura já estava.

**Onde está a prova, e por que ela não está aqui.** O relato é do próprio Dantzig, em
✓ᵐ "Origins of the simplex method", em *A History of Scientific Computing*, p. 141–151, 1990,
DOI [10.1145/87252.88081](https://doi.org/10.1145/87252.88081) — texto que a editora **recusa a
acesso automatizado** (`403`). **É o item de maior valor da fila de verificação**: fecharia esta
história e mais a atribuição do nome *simplex* a Motzkin.

📖 Se confirmada, é uma das melhores histórias do handbook: **a dualidade não foi descoberta,
foi reconhecida** — alguém que olhava para outro problema viu que era o mesmo objeto. Serve
exatamente ao que o Princípio XII quer, que é ensinar a reconhecer o padrão fora do lugar onde
ele foi aprendido.

### 1.3 Capítulo 14 — pontos interiores, e a imprensa

Aqui há uma história pronta, documentada, e com uma lição que vale mais que o algoritmo.

✓ᵐ KHACHIYAN, L. G. "Polynomial algorithms in linear programming". *USSR Computational
Mathematics and Mathematical Physics*, v. 20, p. 53–72, 1980.
DOI [10.1016/0041-5553(80)90061-0](https://doi.org/10.1016/0041-5553(80)90061-0). O método
elipsoidal: **o primeiro algoritmo de tempo polinomial para Programação Linear**.

✓ **A repercussão fora da ciência.** O resultado foi parar na **primeira página do *New York
Times*, em 7 de novembro de 1979**, sob o título "A Soviet Discovery Rocks World of Mathematics".
Antes disso, em outubro, o *Guardian* publicara "Soviet Answer to Traveling Salesmen" — afirmando
que **o problema do caixeiro-viajante tinha sido resolvido**, o que é falso e nasceu de uma
interpretação errada de uma matéria anterior.

📖 **A lição, e ela é dupla.** Primeira: *polinomial não quer dizer rápido*. O método elipsoidal é
polinomialmente limitado e, na prática, perde do Simplex — que é exponencial no pior caso. É o
contraexemplo perfeito para quem sai da aula de complexidade achando que a classe resolve a
escolha. Segunda: **a imprensa entendeu errado de um jeito específico e reincidente** — confundiu
"resolver Programação Linear em tempo polinomial" com "resolver problemas combinatórios difíceis".
Um handbook que ensina a ler artigo aplicado (Parte XI) tem aqui o seu primeiro exemplo, e ele é
de 1979.

✓ᵐ KARMARKAR, N. "A new polynomial-time algorithm for linear programming". *Combinatorica*, v. 4,
p. 373–395, 1984. DOI [10.1007/bf02579150](https://doi.org/10.1007/bf02579150). O método de
pontos interiores que, diferente do elipsoidal, **competiu de verdade** com o Simplex.

⏳ A controvérsia da **patente da AT&T** sobre o algoritmo, e o debate sobre patentear método
matemático, é fortemente citada e **não foi verificada** aqui.

---

## 2. Para a Parte III — redes e fluxos

Esta é a parte com a melhor história do levantamento inteiro, e ela muda o que se ensina.

### 2.1 O fluxo máximo nasceu de um problema de bombardeio

✓ **Fonte aberta e lida:** SCHRIJVER, Alexander. "On the history of the transportation and maximum
flow problems". *Mathematical Programming*, v. 91, p. 437–445, 2002.
DOI [10.1007/s101070100259](https://doi.org/10.1007/s101070100259).
[PDF do autor](https://homepages.cwi.nl/~lex/files/histtrpclean.pdf)

Schrijver revisa um relatório da RAND de **T. E. Harris e F. S. Ross, de 1955**, **secreto até
pouco antes** do artigo, que Ford e Fulkerson citam como a motivação para estudar o fluxo máximo.
O relatório aplica o método à **rede ferroviária da União Soviética e do Leste Europeu**.

E aqui está o ponto:

> Ao contrário do que Ford e Fulkerson dizem, o interesse de Harris e Ross **não era achar um
> fluxo máximo, e sim um corte mínimo** — *interdiction*, na palavra do relatório: quais trechos
> ferroviários destruir.

O relatório abre assim, em citação direta trazida por Schrijver: *"Poder aéreo é um meio eficaz de
interditar o sistema ferroviário inimigo, e tal uso é uma missão lógica e importante para esta
Arma."*

📖 **Por que isso é material didático de primeira.** O teorema *fluxo máximo = corte mínimo* é
ensinado como uma curiosidade elegante: duas quantidades que por acaso coincidem. A história diz
outra coisa — **as duas metades tinham dois donos com objetivos opostos**. Um lado queria fazer
passar o máximo; o outro queria cortar pelo menor custo. **A dualidade não é elegância, é conflito
formalizado**, e é assim que ela deve ser apresentada no capítulo 12.

Há também uma questão que o handbook não deve varrer para baixo do tapete, e que é boa para a
sala: **de onde vem o dinheiro que financia um método muda o método?** Aqui, a pergunta militar
produziu matemática que hoje roteia pacotes, escala turnos e planeja logística humanitária. O
handbook não precisa julgar; precisa **contar**.

### 2.2 O problema de transporte é 10 anos mais velho do que se atribui

✓ Mesma fonte. **A. N. Tolstoĭ, 1930**, publicou "Métodos para achar a quilometragem total mínima
no planejamento de transporte de carga no espaço", num livro editado pelo **Comissariado Nacional
de Transportes da União Soviética**. Ele estudou o problema de transporte, desenvolveu um
**critério de ciclo negativo** e resolveu **à otimalidade** uma instância 10 × 68 — grande, para a
época.

As atribuições usuais são dos anos 1940 em diante.

📖 **A lição.** Não é "os soviéticos chegaram antes" — é mais desconfortável e mais útil: **o que
entra no cânone é o que é lido**, e o que é lido depende de língua, de circulação e de política.
Um handbook vivo, que se propõe a atualizar-se por Radar, precisa dizer isso em voz alta.

### 2.3 Kantorovich

✓ᵐ KANTOROVICH, L. V. "Mathematical Methods of Organizing and Planning Production".
*Management Science*, v. 6, n. 4, p. 366–422, 1960.
DOI [10.1287/mnsc.6.4.366](https://doi.org/10.1287/mnsc.6.4.366) — tradução para o inglês, **21
anos depois** do original de 1939.

Acompanha-a ✓ᵐ KOOPMANS, T. C. "A Note About Kantorovich's Paper". *Management Science*, v. 6,
n. 4, p. 363–365, 1960. DOI [10.1287/mnsc.6.4.363](https://doi.org/10.1287/mnsc.6.4.363).

⏳ A história corrente — Kantorovich formulou a Programação Linear em 1939 a partir de um problema
de corte num truste de compensados, e o trabalho foi ignorado; ele dividiu o Nobel de Economia de
1975 com Koopmans — **não foi verificada em fonte primária** aqui. Os dois artigos acima são o
caminho mais curto para verificar, e ambos são de 1960.

📖 **O gancho editorial:** o intervalo de 21 anos entre o original e a tradução é, ele mesmo, o
argumento da seção 2.2.

### 2.4 Dijkstra, vinte minutos e um café

⏳ **Relato do próprio autor**, numa entrevista de 2001 a Philip L. Frana, do Charles Babbage
Institute — localizado em busca, **não aberto na fonte**: Dijkstra projetou o algoritmo de caminho
mínimo em cerca de **vinte minutos**, **sem papel e lápis**, sentado num terraço de café em
Amsterdã, tomando um café com a noiva. Ele mesmo observa que a ausência de papel foi parte da
razão de o algoritmo ter saído tão limpo.

✓ᵐ DIJKSTRA, E. W. "A note on two problems in connexion with graphs". *Numerische Mathematik*,
v. 1, p. 269–271, **1959** — publicado três anos depois de concebido.

📖 **Duas leituras, e a segunda é a boa.** A primeira é a óbvia: restrição gera simplicidade — sem
papel, só sobrevive o que cabe na cabeça. A segunda é sobre **as três páginas**: o artigo é
minúsculo, e resolveu um problema que hoje roda bilhões de vezes por dia. É um bom antídoto contra
a ideia de que contribuição se mede por volume.

---

## 3. Para a Parte IV — programação inteira

### 3.1 O caixeiro de 49 cidades

✓ᵐ DANTZIG, G.; FULKERSON, R.; JOHNSON, S. "Solution of a Large-Scale Traveling-Salesman
Problem". *Journal of the Operations Research Society of America*, v. 2, n. 4, p. 393–410, 1954.
DOI [10.1287/opre.2.4.393](https://doi.org/10.1287/opre.2.4.393).

📖 **O que faz este artigo valer um lugar de honra** é o método, não o tamanho: eles resolveram um
caixeiro-viajante à otimalidade **sem ter um algoritmo geral para inteiros** — relaxando,
resolvendo Programação Linear, e **acrescentando restrições à mão** quando a solução violava
alguma condição. É a ideia de plano de corte antes de ela existir com esse nome, e é o argumento
mais forte a favor da tese do capítulo 07: **quem sabe formular resolve coisas para as quais não
existe método**.

### 3.2 Os cortes de Gomory e o *branch and bound*

✓ᵐ GOMORY, R. E. "Outline of an algorithm for integer solutions to linear programs".
*Bulletin of the American Mathematical Society*, v. 64, p. 275–278, 1958.
DOI [10.1090/s0002-9904-1958-10224-4](https://doi.org/10.1090/s0002-9904-1958-10224-4).

✓ᵐ LAND, A. H.; DOIG, A. G. "An Automatic Method of Solving Discrete Programming Problems".
*Econometrica*, v. 28, n. 3, p. 497, 1960.
DOI [10.2307/1910129](https://doi.org/10.2307/1910129).

📖 Vale notar, e é história de sala: **os dois pilares da programação inteira exata nasceram com
dois anos de diferença**, e a prática levou décadas para juntá-los no *branch and cut* que os
solvers de hoje executam. Ter as duas ideias não é ter o método.

---

## 4. Para a Parte V — heurísticas e metaheurísticas

### 4.1 Onde a palavra "metaheurística" nasceu

✓ᵐ GLOVER, F. "Future paths for integer programming and links to artificial intelligence".
*Computers & Operations Research*, v. 13, n. 5, p. 533–549, 1986.
DOI [10.1016/0305-0548(86)90048-1](https://doi.org/10.1016/0305-0548(86)90048-1).

⏳ A atribuição da **cunhagem do termo *metaheuristic*** a este artigo é corrente e **não foi
confirmada** por leitura. Vale confirmar: o capítulo de abertura da Parte V ganha muito ao poder
dizer a frase exata e a página.

### 4.2 O recozimento

✓ᵐ KIRKPATRICK, S.; GELATT, C. D.; VECCHI, M. P. "Optimization by Simulated Annealing", 1983
(edições posteriores em coletâneas conferidas; o original em *Science* **não** foi aberto aqui).

📖 O gancho é o empréstimo: o método vem da **metalurgia** — resfriar devagar para o material
assentar num estado de energia baixa. É o exemplo mais limpo do handbook para a ideia de que
**metáfora física boa é ferramenta, e metáfora física ruim é enfeite** — distinção que a Parte V
vai precisar fazer com frequência, porque a área produziu muita metáfora ruim.

### 4.3 Colônia de formigas

✓ᵐ DORIGO, M.; MANIEZZO, V.; COLORNI, A. "Ant system: optimization by a colony of cooperating
agents". *IEEE Transactions on Systems, Man, and Cybernetics*, v. 26, n. 1, p. 29–41, 1996.
DOI [10.1109/3477.484436](https://doi.org/10.1109/3477.484436).

---

## 5. A fila de verificação

O que fecharia mais dívida por unidade de esforço, em ordem:

| # | O que abrir | Fecha |
|---|---|---|
| 1 | **DANTZIG, "Origins of the simplex method"** (1990) | O nome *simplex* por Motzkin (cap. 08 e 09) **e** a história de von Neumann (cap. 12) |
| 2 | **CHARNES** (1952), *Econometrica* | A atribuição do *big-M* (cap. 09) **e** a base do cap. 10 |
| 3 | **KANTOROVICH** (1960) + nota de **KOOPMANS** | A história de 1939 e o argumento sobre cânone (Parte III) |
| 4 | **GLOVER** (1986) | A cunhagem de "metaheurística" (Parte V) |
| 5 | Entrevista de **Dijkstra** ao Charles Babbage Institute (2001) | Os vinte minutos no café (Parte III) |

O item 1 está atrás de um `403` de editora — **não é bloqueio da política de rede deste ambiente,
é a editora recusando acesso automatizado**. Um exemplar em papel ou um acesso institucional
resolve.

## 6. O que este estudo mudou no que já está publicado

Nada, ainda — por desenho. Este documento é **insumo**, e cada história só entra no livro pela
rodada do seu capítulo, com a seção "De onde isto veio" escrita ali.

Duas exceções previsíveis, que devem entrar como revisão pontual quando as rodadas chegarem:

1. **O capítulo 12 (dualidade) ficou com um encaminhamento mais forte** do que o previsto: a
   história de Harris–Ross diz que fluxo máximo e corte mínimo tinham donos com objetivos opostos.
   Dualidade como conflito formalizado, e não como coincidência elegante.
2. **A Parte XI (fronteira), que ensina a ler artigo aplicado, ganhou seu exemplo mais antigo**: a
   confusão da imprensa em 1979 entre "Programação Linear em tempo polinomial" e "caixeiro-viajante
   resolvido".
