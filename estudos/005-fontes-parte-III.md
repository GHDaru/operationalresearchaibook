# Fontes da Parte III — Redes e fluxos (capítulos 16 a 22)

> **Levantamento de 2026-08-13** · rodada de curadoria, **em lote e antes de qualquer edição de
> capítulo**, como manda o [ADR 0013](../adr/0013-o-que-e-a-v0.md), D4 — o mesmo rito do
> [estudo 004](004-historia-parte-II.md), que fez isto para a Parte II.
>
> **Este documento não edita capítulo nenhum.** Ele levanta as fontes candidatas para a seção
> **"Fundamentos científicos"** que o [Guia Editorial](../livro/GUIA-EDITORIAL.md), §2, item 9,
> exige e que os sete capítulos da Parte III hoje **não têm**.

---

## 0. A limitação desta sessão — leia antes de usar qualquer linha abaixo

**Nenhuma fonte foi aberta. Nenhum DOI foi resolvido.** O ambiente desta rodada bloqueou, por
política de egresso da rede, **todo** acesso direto a página web:

| Alvo tentado | Resultado |
|---|---|
| `doi.org` (resolução de DOI) | **bloqueado** (`EGRESS_BLOCKED`) |
| `api.crossref.org` (metadados canônicos) | **bloqueado** |
| `link.springer.com`, `pubsonline.informs.org`, `epubs.siam.org`, `dl.acm.org` | **bloqueados** |
| `rand.org`, `arxiv.org`, `eudml.org`, `dblp.org`, `en.wikipedia.org`, `ir.cwi.nl` | **bloqueados** |
| Busca web (motor de busca) | **funcionou** — foi o único canal disponível |

A instrução do ambiente é explícita: bloqueio de política **não se contorna**, não se desliga TLS
e não se mexe em `HTTPS_PROXY`. Registra-se e segue.

**A consequência disso é dura e precisa ficar dita:**

1. **Nada nesta página pode receber `✓`.** `✓` significa "um humano abriu a fonte e leu o trecho".
   Ninguém abriu nada.
2. **`✓ᵐ` aqui é mais fraco do que o `✓ᵐ` da [bibliografia](../livro/bibliografia.md).** Lá, o selo
   foi posto depois de conferência no Crossref e no *Handle System*. Aqui, ele foi posto depois de
   **busca cruzada**: o mesmo autor, título, veículo, volume e página aparecendo em resultados
   independentes, **e** o DOI aparecendo dentro de uma **URL de editora ou agregador** (que é a
   evidência mais forte disponível, porque a URL vem do índice do buscador e não do texto que o
   buscador escreve).
3. **Onde o DOI só apareceu no texto sintetizado pelo buscador**, ele está marcado
   `DOI candidato — não conferido`. Texto sintetizado por buscador é conteúdo gerado, e este
   handbook não trata conteúdo gerado como fonte.
4. **O portão é quem fecha isto.** `verifica-fontes.mjs` resolve DOI no `npm run build`. Toda linha
   abaixo que entrar na bibliografia **passa por ele**, e é ele que promove ou reprova o
   identificador. É por isso que entregar DOI candidato é aceitável aqui e **não** é aceitável no
   capítulo.

> **Regra que vale para o documento inteiro.** Toda frase de "**o que muda numa decisão**" abaixo é
> **hipótese editorial** construída a partir de metadados e de resumos de terceiros. Ela **não
> sustenta afirmação** em capítulo enquanto ninguém abrir a fonte (constituição, Princípio III).
> O que ela sustenta é a **fila de leitura**: ela diz por que vale a pena abrir aquele artigo.

### Legenda de "como conferi"

| Marca | O que significa |
|---|---|
| **URL-editora** | O DOI apareceu **dentro da URL** de um resultado de editora/agregador (`dl.acm.org/doi/…`, `pubsonline.informs.org/doi/…`, `onlinelibrary.wiley.com/doi/…`, `epubs.siam.org/doi/…`, `link.springer.com/…`). É a evidência mais forte que esta sessão conseguiu produzir |
| **cruzada** | Autor, título, veículo, volume e páginas coincidiram em **≥ 2 resultados independentes** |
| **só-resumo** | O dado apareceu **apenas** no texto que o buscador escreveu. **Não confiável.** Marcado como candidato |

---

## Capítulo 16 — Grafos e redes: fundamentos

O capítulo tem duas dívidas `⏳` declaradas na sua tabela de procedência: as pontes de Königsberg
e a origem do termo *graph*. **As duas têm fonte localizável, e uma delas tem DOI.**

### 16.1 — A fonte de Euler

⏳ **EULER, Leonhard.** "Solutio problematis ad geometriam situs pertinentis". *Commentarii
academiae scientiarum Petropolitanae*, v. 8, p. 128–140. Volume datado de **1736**, publicado em
**1741**. Índice de Eneström **E053**.
[Registro no Euler Archive](https://scholarlycommons.pacific.edu/euler-works/53/)

- **Selo: `⏳`, e o motivo é específico** — não é falta de registro, é falta de **leitura**. O
  registro bibliográfico coincidiu em várias fontes independentes; o texto não foi aberto, e um
  texto em latim do século XVIII é exatamente o caso em que "atribuição corrente" e "eu li" não
  podem ser confundidos.
- **Como conferi:** cruzada. Volume 8, p. 128–140, e o identificador E053 do catálogo de Eneström
  aparecem de forma consistente. **Não há DOI** — obra de 1741 não tem.
- **O que ela muda numa decisão (hipótese):** nada, no método. Muda a **datação** que o capítulo
  publica. O capítulo escreve *"A literatura didática credita a Euler, em 1736"*, e a evidência
  cruzada diz que **1736 é a data nominal do volume**, não a da publicação — o trabalho foi
  apresentado à Academia de São Petersburgo em **1735** e o fascículo saiu em **1741**. Três datas
  diferentes para o mesmo evento é precisamente o que a §7 do Guia Editorial manda distinguir. A
  decisão prática: **não escrever "1736" sem qualificar qual das três datas é**.
- **Sustenta (ou corrige) o trecho:** *"**A literatura didática credita a Euler**, em 1736, a
  demonstração de que a resposta é não — atribuição corrente que este handbook **não confirmou em
  fonte primária**"* (cap. 16, "O aperto"). A redação atual está **correta e cautelosa**; o que
  esta entrada acrescenta é o **registro localizado**, que hoje o capítulo nem cita.

### 16.2 — A origem do termo *graph*

✓ᵐ **SYLVESTER, J. J.** "Chemistry and Algebra". *Nature*, v. 17, p. 284, 1878.
DOI [10.1038/017284a0](https://doi.org/10.1038/017284a0).

- **Como conferi:** cruzada + a URL `nature.com/articles/017284a0` (o identificador do artigo na
  Nature **é** o sufixo do DOI legado) + o *bibcode* do NASA/ADS `1878Natur..17..284S`, que
  confirma independentemente **volume 17, página 284, 1878**. O DOI é, portanto, **derivado da
  convenção de URL da editora** e não de resolução — o portão fecha isto.
- **O que ela muda numa decisão (hipótese):** transforma um `⏳` em algo citável. O capítulo hoje
  diz que a origem química do termo é atribuição corrente **não confirmada**; com esta entrada, a
  frase pode passar a *"a literatura aponta o artigo de Sylvester na Nature, 1878, como a primeira
  ocorrência do termo no sentido de diagrama"* — que é uma afirmação **com endereço**, e portanto
  contestável por quem discordar. Essa é a diferença que o Princípio III protege.
- **Sustenta o trecho:** *"A literatura didática credita o cunho ao século XIX, na química, para os
  diagramas de ligação entre átomos; **este handbook não confirmou essa origem em fonte
  primária**"* (cap. 16, "A origem do nome").

### 16.3 — A referência de campo da Parte inteira

✓ᵐ **AHUJA, Ravindra K.; MAGNANTI, Thomas L.; ORLIN, James B.** *Network Flows: Theory,
Algorithms, and Applications*. Englewood Cliffs: Prentice Hall, 1993. ISBN 978-0-13-617549-0.

- **Como conferi:** cruzada (autoria, título, editora, ano e ISBN-13 coincidentes em catálogo de
  livraria e em cadeias de citação). Livro impresso **não tem verificação por máquina** neste
  handbook — é afirmação humana, como a bibliografia já declara para os livros-base.
- **O que ela muda numa decisão (hipótese):** é a obra que dá **cobertura única** aos capítulos 16
  a 21 — a mesma que trata modelagem, unimodularidade, caminho mínimo, fluxo máximo e custo mínimo
  como um só corpo. Para o leitor que quer ir além do handbook nesta Parte, é o **ponteiro único**,
  e evita que cada capítulo aponte para um livro diferente.
- **Sustenta:** serve de ponteiro geral. **Não sustenta afirmação específica** — e é assim que deve
  entrar, como a bibliografia já faz com Rockafellar ("ponteiro, não fonte de afirmação").

> **Recomendação para o capítulo 16:** Sylvester + Euler + Ahuja et al. — três entradas, dentro da
> faixa de 2 a 4 do guia. O capítulo 16 é de vocabulário e **não é capítulo de método**; a seção
> pode ser curta e honesta.

---

## Capítulo 17 — Caminho mínimo

### 17.1 — Dijkstra

✓ᵐ **DIJKSTRA, E. W.** "A note on two problems in connexion with graphs". *Numerische Mathematik*,
v. 1, p. 269–271, 1959. DOI [10.1007/BF01386390](https://doi.org/10.1007/BF01386390).

- **Como conferi:** URL-editora (`link.springer.com/article/10.1007/BF01386390`) + cruzada com o
  repositório institucional da TU Eindhoven e com o CWI. Páginas 269–271 coincidiram em todos.
- **O que ela muda numa decisão (hipótese):** o **título** já é a decisão. O artigo trata de
  *dois* problemas — caminho mínimo **e** árvore geradora —, o que significa que o mesmo trabalho
  está na origem do capítulo 17 **e** do 18. Para quem modela, isso reforça a tese que o capítulo
  18 mede: os dois problemas são vizinhos de origem e **não** compartilham a garantia do guloso.
- **Sustenta o trecho:** *"A literatura credita o método a **Edsger Dijkstra**, em 1959"* (cap. 17,
  "A virada") e a linha `⏳` *"A atribuição do método a Dijkstra, em 1959"* da tabela de procedência.

### 17.2 e 17.3 — As duas (ou três) origens de Bellman-Ford

✓ᵐ **BELLMAN, Richard.** "On a routing problem". *Quarterly of Applied Mathematics*, v. 16, n. 1,
p. 87–90, 1958. DOI candidato `10.1090/qam/102435` — **não conferido** (apareceu só no resumo do
buscador).

✓ᵐ **FORD, L. R., Jr.** *Network Flow Theory*. Santa Monica: RAND Corporation, Paper **P-923**,
1956. [Registro RAND](https://www.rand.org/pubs/papers/P923.html) — sem DOI.

- **Como conferi:** cruzada para os dois. O registro P-923 aparece no catálogo da própria RAND
  (a URL veio do índice do buscador; a **página não foi aberta**).
- **O que elas mudam numa decisão (hipótese):** confirmam que "Bellman-Ford" é **nome de
  convenção, não de coautoria** — são dois trabalhos independentes, de anos e veículos diferentes,
  e um deles é relatório institucional e não artigo. Para quem escreve o capítulo, isso é o
  antídoto exato contra o "gênio solitário" que a §2.2 do Guia proíbe.
- **Ressalva importante, e ela é uma correção potencial ao capítulo:** o capítulo afirma que
  *"**Bellman-Ford** carrega dois nomes porque tem **duas** origens independentes"*. A literatura
  histórica que apareceu nas buscas menciona com frequência **Shimbel (1955)** e **Moore (1957/59)**
  como origens adicionais do mesmo procedimento. **Não confirmei nenhuma das duas** nesta rodada —
  fica registrado como suspeita de que a contagem "duas" seja **baixa**, e como item da fila.

### 17.4 — O que fazer quando há peso negativo

✓ᵐ **JOHNSON, Donald B.** "Efficient algorithms for shortest paths in sparse networks". *Journal
of the ACM*, v. 24, n. 1, p. 1–13, 1977.
DOI [10.1145/321992.321993](https://doi.org/10.1145/321992.321993).

- **Como conferi:** URL-editora (`dl.acm.org/doi/abs/10.1145/321992.321993`) + cruzada.
- **O que ela muda numa decisão (hipótese):** **é a referência mais útil deste capítulo, e a que
  ele não tem.** O capítulo 17 termina em *"se houver qualquer aresta negativa, use Bellman-Ford"*
  — o que é correto e é uma recomendação de **desistência**: você troca o método rápido pelo lento
  e acabou. O trabalho de Johnson é o que diz que existe uma terceira saída: **reponderar** as
  arestas (uma passada de Bellman-Ford constrói o potencial) e **voltar a usar Dijkstra**. Para
  quem modela, a decisão muda de "peso negativo mata o método rápido" para "peso negativo custa uma
  passada de pré-processamento". Isso é exatamente o formato "o resultado X significa que, na
  prática, você deve Y" que o guia pede.
- **Sustenta o trecho:** *"**1. Dijkstra não serve com peso negativo** — e o modo como ele não
  serve é o pior possível, porque é silencioso. Se houver **qualquer** aresta negativa, use
  Bellman-Ford."* (cap. 17, "Quando não serve"). A fonte **completa** a recomendação; não a
  contradiz.

> **Recomendação para o capítulo 17:** Dijkstra 1959 + Bellman 1958 + Ford 1956 + Johnson 1977 —
> exatamente 4, o teto do guia. Johnson é a que faz a seção ser "traduzida para decisão" em vez de
> uma lista de nomes.

---

## Capítulo 18 — Árvore geradora mínima e projeto de redes

Este é o capítulo em que a história é **mais interessante do que a atribuição corrente**, e há duas
fontes secundárias de qualidade que documentam isso.

### 18.1 e 18.2 — Os dois algoritmos clássicos

✓ᵐ **KRUSKAL, Joseph B., Jr.** "On the shortest spanning subtree of a graph and the traveling
salesman problem". *Proceedings of the American Mathematical Society*, v. 7, n. 1, p. 48–50, 1956.
DOI candidato `10.1090/S0002-9939-1956-0078686-7` — **não conferido** (só-resumo).

✓ᵐ **PRIM, R. C.** "Shortest connection networks and some generalizations". *Bell System Technical
Journal*, v. 36, n. 6, p. 1389–1401, 1957.
DOI [10.1002/j.1538-7305.1957.tb01515.x](https://doi.org/10.1002/j.1538-7305.1957.tb01515.x).

- **Como conferi:** Prim por URL-editora (`onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1957.tb01515.x`)
  e cruzada, inclusive com o arquivo do *Bell System Technical Journal*. Kruskal só por cruzada —
  autor, título, veículo, volume e páginas batem em várias cadeias de citação, mas o DOI só
  apareceu em texto sintetizado.
- **O que mudam numa decisão (hipótese):** o **título do artigo de Kruskal** é, por si só, o
  argumento do capítulo. Ele põe a árvore geradora **e** o caixeiro-viajante no mesmo título, em
  1956 — ou seja, a proximidade entre os dois problemas que o capítulo 18 explora (e mede em 14,3%)
  **é a proximidade original**, não uma justaposição didática inventada aqui.
- **Sustentam o trecho:** *"A atribuição dos dois algoritmos clássicos a **Kruskal** e a **Prim** é
  corrente e não foi confirmada em fonte primária nesta rodada"* (cap. 18, "A origem do nome").

### 18.3 — Borůvka, e por que a atribuição corrente está errada

✓ᵐ **NEŠETŘIL, Jaroslav; MILKOVÁ, Eva; NEŠETŘILOVÁ, Helena.** "Otakar Borůvka on minimum spanning
tree problem: translation of both the 1926 papers, comments, history". *Discrete Mathematics*,
v. 233, n. 1–3, p. 3–36, 2001.
DOI [10.1016/S0012-365X(00)00224-7](https://doi.org/10.1016/S0012-365X(00)00224-7).

✓ᵐ **GRAHAM, R. L.; HELL, P.** "On the history of the minimum spanning tree problem". *Annals of
the History of Computing*, v. 7, n. 1, p. 43–57, 1985. DOI candidato `10.1109/MAHC.1985.10011` —
**não conferido** (só-resumo).

- **Como conferi:** Nešetřil et al. por URL-editora — o identificador PII do ScienceDirect
  (`S0012365X00002247`) **é** o sufixo do DOI, o que confere o identificador sem resolvê-lo — mais
  cruzada de volume, número e páginas. Graham & Hell por cruzada (volume 7, p. 43–57, 1985,
  consistente), com o DOI só em texto sintetizado.
- **O que mudam numa decisão (hipótese) — e esta é a entrada mais valiosa do capítulo 18:** as duas
  fontes existem justamente para **desfazer** a atribuição que o capítulo hoje repete com ressalva.
  O trabalho de Nešetřil et al. traduz **os dois artigos de Borůvka de 1926** para o inglês, e o de
  Graham & Hell registra que **Kruskal e Prim citam Borůvka** nos próprios artigos, e que há
  **várias origens independentes** — Tchecoslováquia, França e Polônia — desde o começo do século.
  A decisão editorial que isso força é direta e cabe na §2.2 do Guia: o capítulo deve parar de
  contar a história como "Kruskal e Prim" com um `⏳` de rodapé, e passar a contá-la como **o caso
  exemplar de redescoberta múltipla** — que é a própria lição de "sem heroísmo".
- **Um segundo achado, não confirmado:** as buscas indicam que **Jarník (1930)** antecede Prim no
  mesmo algoritmo. **Não confirmei** — vai para a lista da §"O que não consegui confirmar".
- **Sustentam o trecho:** a linha `⏳` *"A atribuição dos métodos a Kruskal e a Prim"* (tabela de
  procedência do cap. 18) e *"**Quem estava preso nisso, e quando, é `⏳` neste handbook.** A
  motivação por eletrificação e telefonia é atribuição corrente"* — Nešetřil et al. e Graham & Hell
  são exatamente as fontes que documentam a motivação original (eletrificação da Morávia).

### 18.4 — O limite do guloso no roteiro

✓ᵐ **ROSENKRANTZ, Daniel J.; STEARNS, Richard E.; LEWIS, Philip M., II.** "An analysis of several
heuristics for the traveling salesman problem". *SIAM Journal on Computing*, v. 6, n. 3,
p. 563–581, 1977. DOI [10.1137/0206041](https://doi.org/10.1137/0206041).

- **Como conferi:** URL-editora (`epubs.siam.org/doi/10.1137/0206041`) + cruzada de volume, número
  e páginas.
- **O que ela muda numa decisão (hipótese) — e é a fonte que o capítulo mais precisa:** o capítulo
  publica **14,3%** de perda do vizinho-mais-próximo numa instância de cinco cidades, obtida por
  busca sobre 4.000 grafos aleatórios. Esse número é uma **medição de um caso**, e o leitor
  desavisado vai guardá-lo como se fosse uma margem típica. Este artigo é o que dá o **limitante
  de pior caso** do vizinho-mais-próximo — uma razão de aproximação que **cresce com o logaritmo do
  número de cidades**. A tradução para decisão: *"o prejuízo do guloso no roteiro não tem teto
  constante; ele piora com o tamanho da instância, e por isso um resultado medido em 5 cidades não
  autoriza nenhuma expectativa em 500."* Isso fecha exatamente o buraco que o capítulo abre quando
  diz que a diferença **não é de tamanho** — ela não é de tamanho **na origem estrutural**, mas a
  **magnitude** do prejuízo é, sim, de tamanho.
- **Sustenta o trecho:** *"**O guloso perde 4, ou 14,3%** — na mesma instância em que ele foi
  provadamente ótimo para a árvore"* e *"Guloso | Ótimo, com prova | **Sem garantia**; medido aqui:
  14,3% pior"* (cap. 18).
- **Ressalva:** o valor exato do limitante (`⌈log n⌉/2 + 1/2`) apareceu **apenas em texto
  sintetizado**. **Não o reproduza no capítulo** sem abrir o artigo.

> **Recomendação para o capítulo 18:** Kruskal 1956 + Nešetřil et al. 2001 + Rosenkrantz et al.
> 1977 — três, e cada uma faz um trabalho diferente (a atribuição, a correção da atribuição, o
> limite do método). Prim e Graham & Hell entram na bibliografia, não necessariamente na seção.

---

## Capítulo 19 — Fluxo máximo e corte mínimo

### 19.1 e 19.2 — As duas descobertas independentes do teorema

✓ᵐ **FORD, L. R., Jr.; FULKERSON, D. R.** "Maximal flow through a network". *Canadian Journal of
Mathematics*, v. 8, p. 399–404, 1956. DOI candidato `10.4153/CJM-1956-045-5` — **não conferido**
(só-resumo; o registro no Cambridge Core foi localizado, mas sem o DOI na URL).

✓ᵐ **ELIAS, P.; FEINSTEIN, A.; SHANNON, C. E.** "A note on the maximum flow through a network".
*IRE Transactions on Information Theory*, v. 2, n. 4, p. 117–119, 1956. DOI candidato
`10.1109/TIT.1956.1056816` — **não conferido** (só-resumo).

- **Como conferi:** cruzada forte para os dois — veículo, volume, número e páginas coincidiram em
  fontes independentes, e o trabalho de Elias/Feinstein/Shannon tem ainda registro no Wikidata e a
  reedição como monografia da Bell de 1957.
- **O que mudam numa decisão (hipótese):** o teorema do capítulo foi **provado duas vezes, no mesmo
  ano, por dois grupos que não se falavam** — um de Pesquisa Operacional na RAND, outro de teoria
  da informação no MIT/Bell. Isso não é curiosidade: é o argumento de que o resultado é uma
  **propriedade da estrutura**, não um truque de uma comunidade — e é o que autoriza o capítulo a
  usá-lo em segmentação de imagem e em seleção de projetos, que é o que a tabela "Os problemas que
  não parecem fluxo" faz.
- **Sustentam o trecho:** a linha `📖` *"O teorema de que o fluxo máximo iguala a capacidade do
  corte mínimo"* (tabela de procedência do cap. 19). O capítulo declara que **exibe** e não prova o
  teorema; com estas duas entradas, ele passa a exibir **e apontar onde a prova está** — que é o
  mínimo que o Guia pede.

### 19.3 — A origem ferroviária, documentada

✓ᵐ **SCHRIJVER, Alexander.** "On the history of the transportation and maximum flow problems".
*Mathematical Programming*, v. 91, n. 3, p. 437–445, 2002.
DOI [10.1007/s101070100259](https://doi.org/10.1007/s101070100259).

- **Como conferi:** URL-editora, em **dois** agregadores independentes
  (`link.springer.com/article/10.1007/s101070100259` e `dl.acm.org/doi/10.1007/s101070100259`) +
  cruzada de volume e páginas.
- **O que ela muda numa decisão (hipótese) — resolve o `⏳` mais visível da Parte:** o capítulo 19
  diz que *"a formulação clássica é atribuída a um estudo de rede ferroviária"* e marca `⏳`. Este
  artigo é, pelo que os registros indicam, **exatamente o levantamento dessa história**: ele
  examina um relatório da RAND de **1955, de T. E. Harris e F. S. Ross**, então **secreto**, sobre
  a rede ferroviária **soviética** — o relatório que Ford e Fulkerson citam como motivação —, e
  ainda um artigo de **A. N. Tolstoi, de 1930**, sobre o problema de transporte com critério de
  ciclo negativo. Ou seja: a atribuição corrente **é confirmável**, e o detalhe que ela omite é o
  mais instrutivo — o problema nasceu de um exercício de **interdição**, isto é, de encontrar o
  corte para **destruí-lo**, e não para investir nele. Isso reposiciona a seção "O que fazer com o
  corte" do capítulo: a mesma matemática que diz onde investir diz onde atacar, e vale dizê-lo.
- **Sustenta o trecho:** *"a formulação clássica é atribuída a um estudo de rede ferroviária. **A
  atribuição é corrente e não foi confirmada em fonte primária** nesta rodada"* (cap. 19, "O
  aperto"). Bônus: o mesmo artigo serve ao **capítulo 21**, que precisa da história do problema de
  transporte.

### 19.4 — O que falta ao método guloso do capítulo

✓ᵐ **EDMONDS, Jack; KARP, Richard M.** "Theoretical improvements in algorithmic efficiency for
network flow problems". *Journal of the ACM*, v. 19, n. 2, p. 248–264, 1972.
DOI [10.1145/321694.321699](https://doi.org/10.1145/321694.321699).

- **Como conferi:** URL-editora (`dl.acm.org/doi/10.1145/321694.321699`) + cruzada.
- **O que ela muda numa decisão (hipótese):** o capítulo credita a **exatidão** do procedimento à
  aresta reversa — *"Deixar sempre um caminho de volta é o que permite a um procedimento guloso ser
  exato"* — e para por aí. Falta a outra metade, e ela é uma decisão de implementação: **a aresta
  reversa dá exatidão; a regra de escolha do caminho dá terminação e desempenho.** O procedimento
  como enunciado por Ford e Fulkerson não fixa *qual* caminho aumentante tomar, e é esse trabalho
  que mostra o que se ganha ao fixar a regra. Tradução: *"quem implementar caminho aumentante e
  escolher o caminho 'qualquer um que der' está deixando na mesa a única garantia que o método
  ainda não tem."*
- **Sustenta o trecho:** *"**A aresta reversa é o que torna o guloso exato.** Sem arrependimento
  não há garantia."* (cap. 19, síntese). A fonte **acrescenta uma segunda condição** que o capítulo
  hoje não menciona.

> **Recomendação para o capítulo 19:** Ford & Fulkerson 1956 + Elias/Feinstein/Shannon 1956 +
> Schrijver 2002 + Edmonds & Karp 1972 — 4, o teto. Schrijver é a que fecha o `⏳`; Edmonds & Karp
> é a que vira decisão.

---

## Capítulo 20 — Fluxo de custo mínimo

O `⏳` deste capítulo é nominal: *"A atribuição do teorema que liga unimodularidade total à
integralidade dos vértices"*. Ele tem nome, veículo e ano.

### 20.1 — O teorema

✓ᵐ **HOFFMAN, A. J.; KRUSKAL, J. B.** "Integral boundary points of convex polyhedra". In: KUHN,
H. W.; TUCKER, A. W. (ed.). *Linear Inequalities and Related Systems* (Annals of Mathematics
Studies, 38). Princeton: Princeton University Press, 1956, p. 223–246.
DOI da reedição De Gruyter
[10.1515/9781400881987-014](https://doi.org/10.1515/9781400881987-014) · DOI da reimpressão em
*50 Years of Integer Programming 1958–2008*
[10.1007/978-3-540-68279-0_3](https://doi.org/10.1007/978-3-540-68279-0_3).

- **Como conferi:** URL-editora para **os dois** identificadores, de editoras diferentes
  (`degruyterbrill.com/document/doi/10.1515/9781400881987-014/html` e
  `link.springer.com/chapter/10.1007/978-3-540-68279-0_3`), mais cruzada do volume original e das
  páginas 223–246. Ter **duas** rotas de identificador para a mesma obra é o cenário mais
  confortável desta página inteira.
- **O que ela muda numa decisão (hipótese):** dá **nome e endereço** ao que o capítulo hoje chama
  de "leitura editorial de resultado clássico" e usa como pilar de tudo. Mas o ganho real é outro,
  e é o que torna a referência não-decorativa: o resultado é uma **caracterização** — a
  unimodularidade total não é apenas *suficiente* para a integralidade dos vértices, ela é a
  condição que a caracteriza para **todo** vetor de termos independentes inteiro. A decisão que
  isso produz é exatamente a regra prática do capítulo, mas com fundamento em vez de heurística:
  *"perdeu a forma de rede, perdeu a garantia — e não adianta esperar que 'quase rede' dê 'quase
  inteiro'."* É o mecanismo pelo qual o 220 vira 223,33.
- **Sustenta os trechos:** *"A atribuição do teorema que liga unimodularidade total à integralidade
  dos vértices | ⏳ **atribuição corrente**"* (tabela de procedência) e *"a matriz de restrições de
  um problema de rede é totalmente unimodular, e com oferta e demanda inteiras **todo vértice da
  região viável é inteiro**"* (cap. 20).

### 20.2 — A versão curta do mesmo resultado

✓ᵐ **VEINOTT, Arthur F., Jr.; DANTZIG, George B.** "Integral extreme points". *SIAM Review*, v. 10,
n. 3, p. 371–372, 1968. DOI [10.1137/1010063](https://doi.org/10.1137/1010063).

- **Como conferi:** URL-editora (`dl.acm.org/doi/abs/10.1137/1010063`) + cruzada do fascículo de
  outubro de 1968 do *SIAM Review*.
- **O que ela muda numa decisão (hipótese):** **duas páginas.** É a entrada certa para o leitor que
  quer ver a demonstração e não vai atrás de um volume de 1956 dos *Annals of Mathematics Studies*.
  O capítulo declara que **não reproduz a demonstração**; esta é a fonte que torna essa recusa
  barata para o leitor, em vez de um beco sem saída.

### 20.3 — O caso que a estrutura não protege

✓ᵐ **MEGIDDO, Nimrod.** "On finding primal- and dual-optimal bases". *ORSA Journal on Computing*,
v. 3, n. 1, p. 63–65, 1991. DOI [10.1287/ijoc.3.1.63](https://doi.org/10.1287/ijoc.3.1.63).

- **Como conferi:** URL-editora (`pubsonline.informs.org/doi/abs/10.1287/ijoc.3.1.63`) + cruzada.
- **O que ela muda numa decisão (hipótese) — é a fonte da 5ª entrada de "quando não serve", que
  hoje é a mais original do capítulo e a que está mais sozinha:** o capítulo **mede** que, com
  empate no ótimo e *crossover* desligado, pontos interiores devolvem `1/3` em toda variável, e
  conclui que o *crossover* "existe justamente para desfazer isso". Este artigo é, pelos registros,
  o trabalho fundacional sobre **recuperar uma base ótima a partir de uma solução ótima não
  básica** — ou seja, o que o *crossover* é. A tradução para decisão: *"a garantia de integralidade
  não é do modelo, é do par modelo+método; se o seu solver não terminar em base, a etapa que
  restaura a base é obrigatória, e desligá-la por desempenho é uma escolha de modelagem
  disfarçada de opção de configuração."*
- **Sustenta o trecho:** *"O *crossover* existe justamente para desfazer isso, e vem ligado por
  padrão nos solvers de prateleira. **Desligá-lo em nome de desempenho é o gesto que quebra a
  garantia deste capítulo sem tocar em uma linha do modelo.**"* (cap. 20).

> **Recomendação para o capítulo 20:** Hoffman & Kruskal 1956 + Veinott & Dantzig 1968 +
> Megiddo 1991 — três. As duas primeiras fecham o `⏳`; a terceira fundamenta a única seção do
> capítulo que hoje não tem nenhum apoio externo.

---

## Capítulo 21 — Transporte, designação e transbordo

Este capítulo tem **dois** `⏳` e o primeiro deles — a origem do nome "húngaro" — tem uma resposta
documentada, escrita **pelo próprio Kuhn** e por um matemático húngaro, no mesmo fascículo.

### 21.1 — O método húngaro

✓ᵐ **KUHN, H. W.** "The Hungarian method for the assignment problem". *Naval Research Logistics
Quarterly*, v. 2, n. 1–2, p. 83–97, 1955.
DOI [10.1002/nav.3800020109](https://doi.org/10.1002/nav.3800020109).

✓ᵐ **KUHN, H. W.** "The Hungarian method for the assignment problem". *Naval Research Logistics*,
v. 52, n. 1, p. 7–21, 2005. DOI [10.1002/nav.20053](https://doi.org/10.1002/nav.20053). —
Reimpressão do artigo de 1955 **com prefácio retrospectivo do próprio autor**.

- **Como conferi:** URL-editora para os dois (`onlinelibrary.wiley.com/doi/abs/10.1002/nav.3800020109`
  e `onlinelibrary.wiley.com/doi/10.1002/nav.20053`) + cruzada de volume, número e páginas.
- **O que mudam numa decisão (hipótese):** a reimpressão de 2005 é a que interessa mais, e por um
  motivo de **procedência**: ela é o relato do autor sobre **por que ele deu esse nome**. A
  atribuição não é folclore de sala de aula — é uma **homenagem deliberada**, feita por Kuhn, aos
  trabalhos de **Dénes Kőnig** e **Jenő Egerváry**. Para o capítulo, isso substitui uma frase vaga
  (*"chamado húngaro por causa da origem atribuída aos resultados que o fundamentam"*) por uma
  frase com sujeito e verbo.

### 21.2 — O lado húngaro da mesma história

✓ᵐ **FRANK, András.** "On Kuhn's Hungarian method — a tribute from Hungary". *Naval Research
Logistics*, v. 52, n. 1, p. 2–5, 2005.
DOI [10.1002/nav.20056](https://doi.org/10.1002/nav.20056). — Há versão aberta como relatório
técnico do grupo EGRES (`egres.elte.hu/tr/egres-04-14.pdf`), **não aberta nesta rodada**.

- **Como conferi:** URL-editora (`onlinelibrary.wiley.com/doi/10.1002/nav.20056/pdf`) + cruzada com
  o registro RePEc (`v52y2005i1p2-5`), que confirma páginas 2–5 do mesmo fascículo de Frank.
- **O que ela muda numa decisão (hipótese):** é o **segundo par de olhos** sobre a mesma
  atribuição, e vem do lado atribuído — o que é a melhor situação possível para uma afirmação
  histórica. Pelos registros, ela expõe a relação **exata** entre o método de Kuhn e os resultados
  de Kőnig e Egerváry, em vez de repetir "é baseado em". A decisão editorial: com Kuhn 2005 e Frank
  2005 juntos, o `⏳` da origem húngara pode ser **fechado** — e a existência da versão aberta no
  EGRES significa que o `✓` (leitura de fato) está ao alcance de quem tiver rede.
- **Sustentam o trecho:** *"o método tabular clássico é chamado **húngaro** por causa da origem
  atribuída aos resultados que o fundamentam. **A atribuição é corrente e não foi confirmada em
  fonte primária** nesta rodada"* (cap. 21, "A origem do nome") e a linha `⏳` correspondente.

### 21.3 — O método tabular como algoritmo

✓ᵐ **MUNKRES, James.** "Algorithms for the assignment and transportation problems". *Journal of the
Society for Industrial and Applied Mathematics*, v. 5, n. 1, p. 32–38, 1957.
DOI [10.1137/0105003](https://doi.org/10.1137/0105003).

- **Como conferi:** URL-editora — o identificador aparece como parâmetro `doi=10.1137/0105003` num
  registro de indexação acadêmica — + cruzada de veículo, volume, número e páginas.
- **O que ela muda numa decisão (hipótese):** o capítulo diz que os métodos especializados
  *"ficaram **opcionais**, e a escolha passou a ser de desempenho"* — e **não publica número
  nenhum** para essa escolha (corretamente: ele declara que não cronometrou). Esta é a fonte que dá
  a base da afirmação sem exigir cronômetro: é o trabalho a que se credita a análise de
  complexidade do método, isto é, a demonstração de que ele **termina em tempo polinomial** e não
  por sorte. Tradução para decisão: *"a escolha entre o tabular e o modelo de fluxo é de
  conveniência, não de risco — nenhum dos dois é o lado exponencial de nada."*
- **Sustenta o trecho:** *"Os métodos especializados não ficaram obsoletos — eles ficaram
  **opcionais**, e a escolha passou a ser de desempenho."* (cap. 21, "A virada").

### 21.4 — O problema de transporte, e os métodos tabulares de partida

⏳ **DANTZIG, George B.** "Application of the simplex method to a transportation problem". In:
KOOPMANS, T. C. (ed.). *Activity Analysis of Production and Allocation* (Cowles Commission
Monograph 13). New York: John Wiley & Sons, 1951, p. 359–373. — **Sem DOI localizado.**

⏳ **REINFELD, N. V.; VOGEL, W. R.** *Mathematical Programming*. Englewood Cliffs: Prentice-Hall,
1958. — A obra a que a literatura credita o **método de aproximação de Vogel**. **Sem ISBN nem DOI
localizado** nesta rodada.

- **Como conferi:** cruzada, e **fraca**. O capítulo de Dantzig aparece com páginas consistentes
  (359–373) em várias cadeias de citação, mas todas são citações de terceiros. O livro de Reinfeld
  & Vogel aparece **somente** como citação dentro de artigos sobre variantes do método — não
  localizei registro de catálogo.
- **Por que ficam `⏳`:** exatamente pelo que o capítulo já declara. **Não promova estes dois.**
- **Sobre o "canto noroeste":** as buscas devolveram uma atribuição a Dantzig, com o **nome** tendo
  sido cunhado depois por Charnes e Cooper. **Isso apareceu apenas em texto sintetizado por
  buscador, e não foi confirmado em nenhum registro.** Fica como pista, não como fonte.
- **Sustentam o trecho:** *"Os nomes dos métodos tabulares (canto noroeste, Vogel) e a sua história
  | ⏳ **atribuições correntes**; este handbook **não abriu** as fontes"* (cap. 21). **A linha
  continua correta como está.**

> **Recomendação para o capítulo 21:** Kuhn 2005 + Frank 2005 + Munkres 1957 — três. Schrijver 2002
> (do cap. 19) serve de quarta, para a história do **transporte**. Os métodos tabulares seguem `⏳`
> e o capítulo continua dizendo isso.

---

## Capítulo 22 — PERT e CPM

**Este é o capítulo mais bem servido pela literatura, e o que hoje está mais descoberto.** A tese
que ele mede — que a estimativa do PERT é otimista, e que o desvio tem **duas causas separáveis** —
não é uma descoberta do handbook: é um debate de mais de sessenta anos, com números publicados. A
seção "Fundamentos científicos" aqui **não é ornamento; é a diferença entre um experimento
solitário e um experimento que replica um resultado conhecido**.

### 22.1 e 22.2 — As duas origens

✓ᵐ **MALCOLM, D. G.; ROSEBOOM, J. H.; CLARK, C. E.; FAZAR, W.** "Application of a technique for
research and development program evaluation". *Operations Research*, v. 7, n. 5, p. 646–669, 1959.
DOI [10.1287/opre.7.5.646](https://doi.org/10.1287/opre.7.5.646).

✓ᵐ **KELLEY, James E., Jr.; WALKER, Morgan R.** "Critical-path planning and scheduling". In:
*Papers presented at the December 1–3, 1959, Eastern Joint IRE-AIEE-ACM Computer Conference*,
p. 160–173. DOI [10.1145/1460299.1460318](https://doi.org/10.1145/1460299.1460318).

✓ᵐ **KELLEY, James E., Jr.** "Critical-path planning and scheduling: mathematical basis".
*Operations Research*, v. 9, n. 3, p. 296–320, 1961.
DOI [10.1287/opre.9.3.296](https://doi.org/10.1287/opre.9.3.296).

- **Como conferi:** URL-editora para as três (`pubsonline.informs.org/doi/10.1287/opre.7.5.646`,
  `dl.acm.org/doi/10.1145/1460299.1460318`, `dl.acm.org/doi/abs/10.1287/opre.9.3.296`) + cruzada de
  volume, número e páginas.
- **O que mudam numa decisão (hipótese):** fecham o `⏳` mais amplo do capítulo — *"a datação no
  fim dos anos 1950 e os contextos industrial e militar"* — com **veículos que dizem o contexto
  sozinhos**. O PERT sai numa revista de Pesquisa Operacional e está ligado ao programa de mísseis
  Polaris; o CPM sai numa **conferência de computação**, com autores da indústria química. Isso
  não é anedota: explica por que o CPM trabalha com durações fixas e o PERT com três estimativas —
  **eram encomendas diferentes**, e a §2.2 do Guia pede exatamente esse tipo de causa material.

### 22.3 — A crítica estatística, e ela é a fonte mais valiosa da Parte inteira

✓ᵐ **MacCRIMMON, K. R.; RYAVEC, C. A.** "An analytical study of the PERT assumptions". *Operations
Research*, v. 12, n. 1, p. 16–37, 1964.
DOI [10.1287/opre.12.1.16](https://doi.org/10.1287/opre.12.1.16). — Circulou antes como memorando
da RAND **RM-3408-PR** (1962), aparentemente em acesso aberto.

- **Como conferi:** URL-editora em **dois** agregadores (`pubsonline.informs.org/doi/10.1287/opre.12.1.16`
  e `dl.acm.org/doi/10.1287/opre.12.1.16`) + cruzada de volume, número e páginas, e o registro da
  versão RAND.
- **O que ela muda numa decisão (hipótese) — e por que ela é a mais importante:** o capítulo 22 faz
  uma coisa incomum e a faz bem: ele **separa as duas causas do desvio nas mesmas amostras**, e
  registra numa nota de método que a primeira versão do experimento media as duas juntas e teria
  publicado ~3,5 dias em vez de 0,49. Pelos registros, **este artigo é exatamente essa separação,
  feita analiticamente em 1964**: ele examina, um a um, os erros introduzidos pelas hipóteses do
  PERT — o uso da média $(o+4m+p)/6$ e da família beta de um lado, e o efeito de rede do outro — e
  estima **magnitude e direção** de cada um. A tradução para decisão é forte: *"o desvio do PERT
  tem duas fontes, elas têm tamanhos diferentes, e quem reporta um número único está reportando uma
  soma sem significado."* É a mesma frase que o capítulo escreveu por medição própria — e o valor
  de citar é que a medição do handbook deixa de ser um achado isolado e passa a ser uma
  **replicação**, que é o que dá confiança a um resultado.
- **Sustenta os trechos:** *"**Duas causas diferentes produzem esse desvio, e só uma é defeito do
  método.** Misturá-las daria um número grande e sem significado"* e *"A primeira versão deste
  experimento comparava a fórmula com a simulação diretamente, e teria publicado um viés de ~3,5
  dias que é quase todo artefato da distribuição escolhida"* (cap. 22).
- **Ressalva:** **não copie nenhum número deste artigo** sem abri-lo. A magnitude dos erros que ele
  estima não foi lida.

### 22.4 — O viés como resultado formal

✓ᵐ **FULKERSON, D. R.** "Expected critical path lengths in PERT networks". *Operations Research*,
v. 10, n. 6, p. 808–817, 1962. DOI candidato `10.1287/opre.10.6.808` — **não conferido**
(só-resumo). Também como memorando da RAND **RM-3075-PR**.

✓ᵐ **CLINGEN, C. T.** "Letter to the editor — a modification of Fulkerson's PERT algorithm".
*Operations Research*, v. 12, n. 4, p. 629–632, 1964.
DOI [10.1287/opre.12.4.629](https://doi.org/10.1287/opre.12.4.629).

- **Como conferi:** Clingen por URL-editora (`pubsonline.informs.org/doi/10.1287/opre.12.4.629`).
  Fulkerson por cruzada — volume 10, p. 808–817, 1962, mais o registro RAND RM-3075 —, mas o DOI só
  apareceu em texto sintetizado.
- **O que mudam numa decisão (hipótese):** é o **enunciado formal** do que o capítulo mede. Pelos
  registros, o trabalho de Fulkerson dá um procedimento que produz um valor **entre** a estimativa
  ingênua do PERT e a duração esperada verdadeira — isto é, ele trata o número do PERT como um
  **limitante inferior** da média real, e não como uma aproximação de sinal desconhecido. A decisão
  que sai daí é a mais acionável do capítulo: *"o erro do PERT tem **sinal conhecido**. Ele nunca é
  pessimista. Portanto, a estimativa dele pode ser usada como piso — e nunca como compromisso."*
  O capítulo hoje diz *"ele erra quase sempre, e para o mesmo lado"* apoiado apenas na própria
  simulação; com esta fonte, "o mesmo lado" deixa de ser observação e vira propriedade.
- **Sustenta o trecho:** *"O método não erra por pouco: ele erra quase sempre, e para o mesmo
  lado."* (cap. 22, "O problema").

### 22.5 — O viés medido numa rede real

✓ᵐ **KLINGEL, A. R., Jr.** "Bias in PERT project completion time calculations for a real network".
*Management Science*, v. 13, n. 4, p. B194–B201, 1966.
DOI [10.1287/mnsc.13.4.B194](https://doi.org/10.1287/mnsc.13.4.B194).

- **Como conferi:** URL-editora (`pubsonline.informs.org/doi/10.1287/mnsc.13.4.B194`) + cruzada de
  volume, número e páginas.
- **O que ela muda numa decisão (hipótese):** o capítulo 22 mede o viés numa rede **de quatro
  tarefas, inventada para o livro**, e depois varre o número de ramos paralelos. A objeção óbvia de
  um leitor cético é *"isso é um brinquedo"*. Este trabalho, pelos registros, mede o mesmo
  fenômeno **numa rede de projeto real**, e conclui — na leitura que os registros oferecem — que o
  viés é grande justamente quando há **vários caminhos paralelos com médias parecidas e variâncias
  altas**. Isso dá ao capítulo a condição de aplicabilidade que ele hoje não enuncia: *"o viés não
  é grande em qualquer projeto; ele é grande em projetos com muitos caminhos quase-críticos e muita
  incerteza — e é assim que você reconhece, olhando o seu cronograma, se este capítulo se aplica a
  você."* Isso é melhor do que a tabela de ramos paralelos, porque é um **teste que o leitor faz no
  próprio projeto**.
- **Sustenta o trecho:** *"### E o viés cresce com os caminhos paralelos"* e toda a tabela de 1 a 8
  ramos (cap. 22).
- **⚠️ Ressalva séria, e ela é a razão de este item não poder ser copiado:** o resumo do buscador
  descreve os resultados do PERT como *"biased high"*. A tese do capítulo 22 — e o restante da
  literatura localizada — é que a estimativa do PERT é **otimista**, isto é, **baixa demais**. Ou o
  resumo do buscador está errado, ou a expressão se refere a outra quantidade (por exemplo, à
  **probabilidade** calculada de cumprir o prazo, que fica **alta** demais precisamente porque a
  duração fica baixa demais). **Não use este artigo, nem a palavra "viés" atribuída a ele, sem
  abrir o texto.** É o caso exemplar de por que `✓ᵐ` não sustenta afirmação de conteúdo.

### 22.6 a 22.8 — Reserva

✓ᵐ **Van SLYKE, R. M.** "Letter to the editor — Monte Carlo methods and the PERT problem".
*Operations Research*, v. 11, n. 5, p. 839–860, 1963.
DOI [10.1287/opre.11.5.839](https://doi.org/10.1287/opre.11.5.839). — URL-editora + cruzada.
**Por que importa:** é, pelos registros, o trabalho que introduz **simular** o PERT em vez de somar
o caminho crítico — ou seja, **o método que o capítulo 22 usa** — e que define o **índice de
criticalidade**, a probabilidade de cada tarefa cair no caminho crítico. Isso é a formalização
direta da 2ª entrada de "quando não serve": *"Com incerteza, o caminho crítico **é aleatório**"*.
A decisão: em vez de dizer que "o" caminho crítico é uma simplificação, **meça a criticalidade de
cada tarefa** — e aí a folga vira uma distribuição, não um número.

✓ᵐ **SCHONBERGER, Richard J.** "Why projects are 'always' late: a rationale based on manual
simulation of a PERT/CPM network". *Interfaces*, v. 11, n. 5, p. 66–70, 1981.
DOI [10.1287/inte.11.5.66](https://doi.org/10.1287/inte.11.5.66). — URL-editora + cruzada.
**Por que importa:** é o artigo cujo **título é a tese do capítulo**, escrito para praticantes e
com simulação manual — isto é, reproduzível com papel. É a referência que fecha a ponte entre o
resultado técnico e o "erro caro" que o capítulo descreve (*"a conversa que se segue é sobre
disciplina de execução, quando o defeito estava na aritmética da estimativa"*).

✓ᵐ **TRIETSCH, Dan; BAKER, Kenneth R.** "PERT 21: fitting PERT/CPM for use in the 21st century".
*International Journal of Project Management*, v. 30, n. 4, p. 490–502, 2012. DOI candidato
`10.1016/j.ijproman.2011.09.004` — **não conferido** (só-resumo). Há versão aberta hospedada pela
Tuck School of Business, **não aberta nesta rodada**.
**Por que importa:** é a entrada **moderna**, e a única desta lista que propõe substituto em vez de
crítica. Pelos registros, é onde o viés do PERT aparece nomeado como **"Jensen gap"** — o efeito da
desigualdade de Jensen sobre a média de um máximo —, que é literalmente a "ideia reaproveitável"
que o capítulo já enuncia: *"A média de um máximo é maior do que o máximo das médias."* Dar nome
matemático a essa frase é o que a torna exportável para fora de projetos.

> **Recomendação para o capítulo 22:** MacCrimmon & Ryavec 1964 + Fulkerson 1962 + Klingel 1966 +
> Malcolm et al. 1959 — 4, o teto. Kelley & Walker, van Slyke, Schonberger e Trietsch & Baker vão
> para a bibliografia. **Se só couberem duas: MacCrimmon & Ryavec e Fulkerson** — são as que
> transformam a medição do handbook em replicação de um resultado conhecido.

---

## O que NÃO consegui confirmar

Esta seção vale tanto quanto o resto. Ela é o que impede que a lista acima seja lida como mais
sólida do que é.

### 1. Nada foi lido. Zero DOIs foram resolvidos.

Não é uma ressalva de forma. **É a limitação central desta rodada.** `doi.org`, `api.crossref.org`
e **todos** os hospedeiros de editora, repositório e enciclopédia responderam bloqueio de política
de egresso. O único canal foi o motor de busca. Consequências, explicitamente:

- **Nenhuma entrada pode receber `✓`.** Nenhuma afirmação de **conteúdo** desta página sustenta
  frase de capítulo.
- **Todo `✓ᵐ` acima está um degrau abaixo** do `✓ᵐ` que a [bibliografia](../livro/bibliografia.md)
  define, porque não passou pelo Crossref. Quem for promovê-los precisa passar o
  `verifica-fontes.mjs` **antes** de a linha entrar no capítulo.
- **As frases de "o que muda numa decisão" são hipóteses editoriais**, e estão marcadas como tais em
  cada item. Elas dizem **por que abrir o artigo**, não o que ele diz.

### 2. DOIs candidatos — apareceram só em texto sintetizado por buscador

Estes seis **não** foram vistos numa URL de editora. Texto de buscador é conteúdo gerado, e este
handbook não o aceita como fonte. **Todos precisam passar pelo portão antes de publicar:**

| Obra | DOI candidato |
|---|---|
| BELLMAN, "On a routing problem", 1958 | `10.1090/qam/102435` |
| KRUSKAL, "On the shortest spanning subtree…", 1956 | `10.1090/S0002-9939-1956-0078686-7` |
| GRAHAM & HELL, "On the history of the MST problem", 1985 | `10.1109/MAHC.1985.10011` |
| FORD & FULKERSON, "Maximal flow through a network", 1956 | `10.4153/CJM-1956-045-5` |
| ELIAS, FEINSTEIN & SHANNON, "A note on the maximum flow…", 1956 | `10.1109/TIT.1956.1056816` |
| FULKERSON, "Expected critical path lengths in PERT networks", 1962 | `10.1287/opre.10.6.808` |
| TRIETSCH & BAKER, "PERT 21", 2012 | `10.1016/j.ijproman.2011.09.004` |

*(São sete. A tabela está certa e a frase acima estava errada — corrigido aqui em vez de escondido.)*

### 3. Sem identificador nenhum

- ❌ **EULER, 1736/1741.** Obra do século XVIII: **não tem DOI e não vai ter.** O melhor
  identificador disponível é o índice de Eneström **E053** e o registro do Euler Archive. Segue
  `⏳` porque **não foi lida** — e um texto em latim é o último lugar do mundo onde "atribuição
  corrente" pode passar por leitura.
- ❌ **FORD, *Network Flow Theory*, RAND P-923, 1956.** Relatório institucional, sem DOI. Existe
  registro no catálogo da RAND; a página **não foi aberta**.
- ❌ **REINFELD & VOGEL, *Mathematical Programming*, 1958.** **Não localizei registro de catálogo,
  ISBN nem qualquer registro primário.** A obra aparece **exclusivamente** como citação dentro de
  artigos sobre variantes do método de Vogel. O `⏳` do capítulo 21 **está correto e deve
  permanecer**.
- ❌ **DANTZIG, "Application of the simplex method to a transportation problem", 1951.** Capítulo de
  livro; sem DOI localizado. Páginas 359–373 coincidem em cadeias de citação — todas de terceiros.

### 4. Atribuições que continuam abertas — e uma que talvez esteja errada no capítulo

- ⏳ **A origem do "canto noroeste".** Uma atribuição a Dantzig, com o nome cunhado depois por
  Charnes e Cooper, apareceu **apenas em texto sintetizado por buscador**. **Não é fonte.** O `⏳`
  do capítulo 21 permanece.
- ⏳ **Jarník (1930) como precursor de Prim.** Apareceu em título de trabalho localizado nas buscas
  ("Jarník's solution in historical and present context"). **Não confirmado.** Se confirmado, é um
  reforço direto da tese de redescoberta múltipla do capítulo 18.
- ⏳ **Shimbel (1955) e Moore (1957/59) como origens adicionais de Bellman-Ford.** Mencionados de
  passagem nas buscas; **não confirmados**. **Se confirmados, o capítulo 17 está errado** ao dizer
  que o método tem *"duas origens independentes"* — seriam três ou quatro. Vale investigar antes de
  a Parte III sair da v0, porque é uma afirmação que o capítulo faz **sem ressalva**.
- ⏳ **A direção do viés em Klingel (1966).** O resumo do buscador diz "biased high"; a tese do
  capítulo e o resto da literatura dizem que a estimativa do PERT é **otimista**. Contradição não
  resolvida. **Item bloqueante para esta referência**: não publique nada apoiado nela sem abrir o
  texto.
- ⏳ **O limitante de pior caso do vizinho-mais-próximo** (`⌈log n⌉/2 + 1/2`). O **fato** de existir
  um limitante logarítmico apareceu de forma consistente; a **fórmula exata** apareceu só em texto
  sintetizado. Cite o artigo; **não cite a fórmula** sem abri-lo.

### 5. O que não foi procurado, e é lacuna declarada

- **Nenhuma varredura sistemática** foi feita. As buscas partiram de hipóteses minhas sobre quais
  são os trabalhos canônicos de cada tema. Isso favorece o que é famoso e **esconde o que é bom e
  pouco citado** — exatamente o viés que a lacuna declarada da seção "Formulação" da bibliografia
  já registra para outro assunto.
- **Literatura em português não foi procurada.** Os dois livros-base (Lachtermacher e Arenales et
  al.) cobrem a Parte III (Unidade 5 e Unidade 4, respectivamente, segundo a tabela de
  correspondência da bibliografia) e **não** foram consultados nesta rodada.
- **O Radar não foi atualizado.** Pelo Guia Editorial, §6, uma referência entra no livro **pela
  porta do Radar**. Nenhuma linha foi escrita em `radar/RADAR.md` — este documento é o passo
  anterior, e a rodada que editar os capítulos tem essa dívida.

---

## Resumo operacional para quem for editar

| Capítulo | `⏳` que **pode** fechar com o levantado | `⏳` que **continua aberto** |
|---|---|---|
| 16 | origem do termo *graph* (Sylvester 1878) | Euler — registro localizado, **texto não lido** |
| 17 | atribuições a Dijkstra, Bellman e Ford | "duas origens" pode ser contagem baixa |
| 18 | Kruskal, Prim, **e** a motivação original (via Nešetřil et al. / Graham & Hell) | Jarník como precursor de Prim |
| 19 | a origem ferroviária (Schrijver 2002) | — |
| 20 | o teorema da unimodularidade (Hoffman & Kruskal) | — |
| 21 | a origem do nome "húngaro" (Kuhn 2005 + Frank 2005) | canto noroeste e Vogel — **sem fonte** |
| 22 | datação e contextos do PERT e do CPM | direção do viés em Klingel |

**Ordem de leitura sugerida, se houver tempo para abrir poucas fontes:** MacCrimmon & Ryavec 1964
(cap. 22), Schrijver 2002 (caps. 19 e 21), Frank 2005 (cap. 21, tem versão aberta no EGRES) e
Nešetřil et al. 2001 (cap. 18). São as quatro que **fecham** dívidas em vez de apenas nomeá-las.
