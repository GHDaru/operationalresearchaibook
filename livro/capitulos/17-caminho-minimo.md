# 17 — Caminho mínimo

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Rodar Dijkstra à mão** numa malha pequena e dizer, a cada passo, qual nó fechou e por quê.

**O2.** **Reconhecer a hipótese que Dijkstra usa sem declarar**, e prever o que acontece quando ela
não vale.

**O3.** **Escolher** entre Dijkstra, Bellman-Ford e um modelo de Programação Linear (PL) a partir do que
o problema tem, e não do que é mais conhecido.

## O problema

Caminho mínimo é o problema mais bem resolvido desta Parte, e é por isso que ele é perigoso. O
método padrão é rápido, simples e está em toda biblioteca — e tem uma hipótese que quase ninguém
enuncia ao usá-lo.

O erro caro deste capítulo é o mais desconfortável do livro inteiro:

> Dijkstra, diante de um peso negativo, **devolve uma resposta que contradiz a si mesma**. Medido
> aqui: ele reporta distância **6** até o destino e, ao mesmo tempo, reporta o caminho
> `A → C → B → D` — que custa **4**. Não há erro, não há aviso, não há exceção lançada. A saída é
> internamente inconsistente e ninguém olha.

## De onde isto veio

### O aperto: achar caminho era percorrer tudo

Antes de haver método, achar o caminho mais barato numa rede era enumerar caminhos — e o número de
caminhos cresce exponencialmente com o tamanho. Para uma malha de cidades isso já era inviável na
mão, e continuou inviável quando as máquinas chegaram, porque o problema não é de velocidade: é
de **quantidade**.

### A virada: fechar um nó para sempre

A ideia que resolve é pequena e vale decorar: **se você sempre expandir o nó aberto mais barato,
quando ele for expandido o caminho até ele já é o melhor possível** — e você pode fechá-lo,
definitivamente, sem nunca mais revisitar.

Isso troca enumeração de caminhos por uma varredura de nós. E é aqui que mora a hipótese: o
argumento só funciona se **nenhuma aresta puder baixar o custo depois**, isto é, se não houver peso
negativo. A literatura credita o método a **Edsger Dijkstra**, em 1959.

### A ideia reaproveitável

> **Uma decisão pode ser tomada em definitivo quando nada que vier depois pode melhorá-la.** É
> isso, e só isso, que autoriza fechar um nó — e é a mesma condição que autoriza qualquer atalho
> guloso, em qualquer área.

O [capítulo 18](18-arvore-geradora.md) mostra o mesmo gesto funcionando com prova, e falhando na
porta ao lado.

### A origem do nome

**Bellman-Ford** carrega dois nomes porque tem duas origens independentes, e a atribuição é
`⏳` neste handbook. **"Relaxar" uma aresta** é o verbo do método, e a leitura de que ele venha da
metáfora física — uma corda tensa que se afrouxa até acomodar — é **leitura editorial**, não
etimologia documentada. A cada passada, as distâncias "afrouxam" para o valor menor que ainda
cabe.

### Procedência

| Afirmação | Estado |
|---|---|
| A atribuição do método a Dijkstra, em 1959 | ⏳ **atribuição corrente**; este handbook **não abriu** a fonte primária nesta rodada |
| A atribuição de Bellman-Ford a Bellman e a Ford | ⏳ **atribuição corrente**, não confirmada |
| A origem do verbo "relaxar" na metáfora física | 📖 **leitura editorial**; não é afirmação documentada |
| Que Dijkstra devolva 6 e Bellman-Ford devolva 4 na instância desta página | ✓ **medido** em `po-zero/parte-III-redes`, com teste que compara este texto à medição |

## Dijkstra, e a hipótese que ele não declara

Numa malha honesta — pesos não negativos —, o método faz o que promete. Medido:

| De `deposito` até | Distância |
|---|---|
| `sul` | **2** |
| `norte` | **3** |
| `leste` | **8** |
| `oeste` | **10** |
| `cliente` | **11** |

E o caminho até o cliente é `deposito → sul → norte → leste → cliente`. **Bellman-Ford devolve
exatamente as mesmas distâncias** — quando a hipótese vale, os dois concordam, e é assim que se
sabe que ela vale.

### O que acontece quando a hipótese cai

A instância é pequena de propósito, para o leitor conferir à mão:

```
A --1--> B        B --5--> D
A --2--> C        C --(-3)--> B
```

| Método | Distância até `D` | Caminho que ele devolve |
|---|---|---|
| **Dijkstra** | **6** | `A → C → B → D` |
| **Bellman-Ford** | **4** | `A → C → B → D` |

**Olhe a linha de cima com atenção.** O caminho que Dijkstra devolve custa 2 − 3 + 5 = **4**, e a
distância que Dijkstra devolve é **6**. A saída contradiz a si mesma.

**Por que isso acontece**, e vale seguir o passo a passo porque ele é curto. O método fecha `A`
(0), depois fecha `B` com distância 1 — porque 1 < 2 — e, ao fechar `B`, relaxa `B → D` para 6.
Só então fecha `C` (2) e descobre que `C → B` melhora `B` para −1. Mas `B` **já está fechado**, e o
método não volta: `D` nunca é recalculado.

> **O que fica dessa medição, e é maior do que o algoritmo.** O defeito não foi o método errar —
> foi o método **não ter como saber** que errou. A hipótese estava na cabeça de quem escolheu
> Dijkstra, não no código. Toda vez que um procedimento rápido depende de uma condição que ninguém
> testa, existe uma versão deste episódio esperando.

> ### ▶ Rode você mesmo
>
> **[Abrir a Parte III no Google Colab](https://colab.research.google.com/github/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-III.ipynb)** · fonte em
> [`po-zero/cadernos/parte-III.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-III.ipynb)
>
> Lá dentro você **dá o seu palpite antes** de ver a contradição — e o palpite comum erra, porque quase ninguém espera que o método devolva número e caminho que não fecham entre si. O caderno **não contém o algoritmo**: chama o código publicado, que o `pytest` já
> verifica ([ADR 0016](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0016-cadernos-colab-sem-deriva.md)).

## Bellman-Ford: mais lento, e sabe o que não sabe

Ele relaxa **todas** as arestas, $|V| - 1$ vezes. Isso é mais caro — e compra duas coisas:

1. **Funciona com peso negativo**, porque nada é fechado em definitivo.
2. **Detecta o que não tem resposta.** Se ainda houver melhora numa passada extra, existe **ciclo
   negativo** — e aí não existe caminho mínimo, existe caminho arbitrariamente barato. Medido: na
   instância com o ciclo `B → C → B` de peso −2, ele devolve o veredito, em vez de um número.

Um método que devolve *"esta pergunta não tem resposta"* é melhor do que um que devolve um número
qualquer, e o [capítulo 10](10-casos-especiais.md) já tinha dito isso sobre `Infeasible`.

## Os problemas que não parecem caminho

A promessa desta Parte é **enxergar a rede** ([capítulo 16](16-grafos-e-redes.md)), e caminho mínimo
é onde ela rende mais, porque "caminho" quase nunca aparece no enunciado. Quatro casos:

| A situação | O nó é | A aresta é | O peso é |
|---|---|---|---|
| **Trocar ou reformar** um equipamento ao longo de 5 anos | o ano | *"comprei no ano `i`, troco no ano `j`"* | custo de compra + manutenção − revenda |
| **Cortar uma barra** de comprimento 100 em pedaços encomendados | o comprimento já cortado | um corte | desperdício daquele corte |
| **Converter moedas** em sequência (real → euro → iene → real) | a moeda | a conversão possível | **−log** da taxa |
| **Corrigir um texto** para outro, letra a letra | o par de posições | inserir, apagar ou trocar | 1 por operação |

O primeiro é o mais útil e o menos óbvio. *"Quando trocar o caminhão?"* não tem cara de rede — mas
uma política de troca **é** uma sequência de decisões ao longo do tempo, e toda sequência do ano 0
ao ano 5 é um caminho. O mínimo desse grafo é a política mais barata — e a tradução troca uma
enumeração de políticas por um caminho mínimo num grafo de seis nós, que é o tipo de mudança de
tamanho que o [capítulo 05](05-complexidade.md) trata. **Este handbook não cronometrou os dois**, e
por isso não publica número.

> **O terceiro merece um aviso, porque ele é a armadilha do capítulo.** Com **−log** da taxa,
> multiplicar taxas vira somar pesos, e o caminho mínimo acha a melhor sequência de conversões. Só
> que uma oportunidade de arbitragem — ganhar dinheiro dando a volta — é exatamente um **ciclo
> negativo**. Dijkstra não pode ser usado aqui: os pesos são negativos sempre que a taxa for maior
> que 1, e o método devolveria um número silenciosamente errado, como este capítulo mediu.
> **Bellman-Ford é obrigatório**, e o veredito *"ciclo negativo"* deixa de ser aviso de erro para
> virar **a resposta que se procurava**.

Repare no que muda: o mesmo veredito é defeito num problema e produto no outro. **Quem enxerga a
rede escolhe o método pela pergunta, e não pelo tamanho da instância.**

## Quando não serve

**1. Dijkstra não serve com peso negativo** — e o modo como ele não serve é o pior possível, porque
é silencioso. Se houver **qualquer** aresta negativa, use Bellman-Ford.

**2. Nenhum dos dois serve se o peso depender do caminho.** Congestionamento, desconto por volume e
pedágio progressivo quebram a hipótese de que o custo de uma aresta é constante — e aí o problema é
de fluxo, não de caminho.

**3. Nenhum dos dois serve para "o melhor caminho que passa por estes três pontos".** Isso é
roteirização, é outro problema, e o [capítulo 18](18-arvore-geradora.md) mostra por que o salto de
dificuldade entre os dois é real.

**4. A Programação Linear serve, e às vezes é a escolha certa** mesmo sendo mais lenta: quando o
caminho é **parte** de um modelo maior, com restrições que não são de rede, embutir o caminho como
PL evita ter de costurar dois métodos.

## Fundamentos e fontes

**O que está medido aqui.** As cinco distâncias da malha, a discordância entre 6 e 4 na instância
com peso negativo, o caminho que Dijkstra devolve, e a detecção do ciclo negativo. Tudo em
`po-zero/parte-III-redes/redes.py`, em aritmética exata, com teste que compara **este texto** à
medição.

**O que entra por atribuição corrente, e não por fonte aberta:** os nomes de Dijkstra, Bellman e
Ford. Este handbook **não abriu** as fontes primárias nesta rodada, e as linhas ficam `⏳`.

> 🔵 **Este capítulo está em "medido".** O que falta para ✅ é revisão independente em contexto
> fresco.

## Pratique

<div data-bateria="cap17"></div>

Três exercícios. O primeiro roda Dijkstra à mão; o segundo é o mais importante da bateria — prever
o que o método faz quando a hipótese cai, **antes** de rodar; o terceiro escolhe o método por
critério declarado.

## Assista

**[Aula 6.2: Algoritmo de Dijkstra (Caminho Mínimo)](https://www.youtube.com/watch?v=xirBe9Bu-Ik)** ·
[Matemática Para Gente Grande](https://www.youtube.com/@prof_allanIFBA) · 13min45s

**O que ele resolve:** este capítulo gasta o espaço no **contraexemplo** — o caso em que o método
falha em silêncio — e trata o procedimento em si de forma resumida. O vídeo faz o inverso: executa
Dijkstra passo a passo, com a tabela sendo preenchida na tela. Ver o método funcionando antes de
ver o método falhando é a ordem que economiza confusão.

## Síntese — o que levar

- **Dijkstra fecha nós em definitivo**, e é isso que o torna rápido.
- **A hipótese que autoriza fechar é peso não negativo** — e ela não está no código, está na cabeça
  de quem escolheu o método.
- **Com peso negativo, a saída contradiz a si mesma.** Medido: distância 6 e caminho que custa 4,
  sem erro nem aviso.
- **Bellman-Ford é mais lento e sabe o que não sabe:** funciona com peso negativo e **detecta ciclo
  negativo**, devolvendo veredito em vez de número.
- **Quando a hipótese vale, os dois concordam** — e é assim que se confere.
- **Peso que depende do caminho quebra os dois.** Aí o problema é de fluxo.
- **Fora da Pesquisa Operacional:** todo atalho guloso depende de uma condição; se ninguém a testa,
  há uma falha silenciosa esperando.

## Verificação

1. Rode Dijkstra à mão na malha desta página a partir de `deposito` e liste a ordem em que os nós
   fecham. *(O1)*
2. Sem rodar nada: um colega vai usar Dijkstra numa rede em que algumas arestas representam
   **descontos** (peso negativo). Diga o que ele vai receber e por quê — inclusive por que ele não
   vai receber um erro. *(O2)*
3. Um problema pede o caminho mais barato **e** limita o total de pedágios a três. Que método você
   usa, e por quê? *(O3)*

### Leitura executiva

Caminho mínimo é o problema mais bem resolvido desta Parte, e por isso o mais perigoso: o método
padrão está em toda biblioteca e carrega uma hipótese que quase ninguém enuncia ao usá-lo.
**Dijkstra é rápido porque fecha nós em definitivo** — se você sempre expandir o nó aberto mais
barato, o caminho até ele já é o melhor possível quando ele for expandido. Esse argumento só vale
se nenhuma aresta puder baixar o custo depois, ou seja, **se não houver peso negativo**; e a
hipótese não está no código, está na cabeça de quem escolheu o método. Quando ela cai, o resultado
é o pior tipo possível de falha: medido aqui, Dijkstra reporta distância **6** até o destino e, ao
mesmo tempo, reporta o caminho `A → C → B → D`, que custa **4** — **a saída contradiz a si mesma**,
sem erro, sem aviso e sem exceção. O motivo é curto: ele fecha o nó `B` com distância 1 e relaxa
`B → D` para 6 antes de descobrir, via `C`, que `B` valia −1; como `B` já está fechado, `D` nunca é
recalculado. **Bellman-Ford** custa mais — relaxa todas as arestas $|V|-1$ vezes — e compra duas
coisas: funciona com peso negativo, e **detecta ciclo negativo**, devolvendo o veredito de que a
pergunta não tem resposta em vez de um número qualquer. Quando a hipótese de Dijkstra vale, os dois
concordam, e essa concordância é o modo prático de conferir. Os dois falham juntos quando o peso da
aresta depende de quanto já passou por ela — congestionamento, desconto por volume, pedágio
progressivo —, caso em que o problema é de fluxo e não de caminho; e nenhum dos dois responde "o
melhor percurso que passa por estes três pontos", que é roteirização e é outro assunto. A lição que
sobrevive ao algoritmo é mais geral: **todo atalho guloso depende de uma condição, e quando ninguém
testa essa condição existe uma falha silenciosa esperando a hora**.
