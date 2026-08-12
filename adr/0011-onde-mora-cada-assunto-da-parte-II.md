# ADR 0011 — Onde mora cada assunto da Parte II: a ponte de álgebra e a precificação

**Data:** 2026-08-12 · **Status:** aceito na branch, **pendente de ratificação do autor no gate
de merge** · **Rodada:** 008 · **Decisão por:** o autor, em resposta direta

## Contexto

O capítulo 11 (Simplex revisado) precisa de notação matricial, e o handbook nunca exigiu álgebra
linear do leitor: o capítulo 08 foi geométrico e o 09, aritmético. Ao mesmo tempo, o capítulo 10
prometeu que a conversa sobre **regras de pivoteamento** continuaria — e essa conversa é também
assunto de desempenho.

Duas perguntas de escopo foram ao autor, porque mudam o que o capítulo é. Este registro existe
porque **as duas já moveram artefatos do livro** e vinculam capítulos que ainda não existem — e o
guardião do processo apontou que decisão desse alcance vivendo só numa spec de rodada é decisão
que ninguém relê.

## Decisão

### D1 — A ponte de álgebra linear é construída **dentro do capítulo 11**

Não se assume álgebra linear, nem se fica no nível da ideia. O capítulo apresenta $B$, $N$,
$B^{-1}$ e o vetor de preços $y = c_B B^{-1}$, em seção própria, **depois da intuição** e antes
da matemática do laço revisado.

**A ponte não constrói exemplo — ela renomeia números que o leitor já conferiu à mão.** Isto foi
**medido**, não suposto:

```
quadro final do capítulo 09        B⁻¹ calculada do zero      y = c_B·B⁻¹
    f1     f2                          [ 2  -1]                [50  50]
     2     -1                          [-1   1]
    -1      1
    50     50   ← linha z
```

As colunas sob $f_1$ e $f_2$ **são** $B^{-1}$; os dois `50` da linha $z$ **são** $y$. Conferido
contra a inversa de $B = \begin{smallmatrix}1&1\\1&2\end{smallmatrix}$, calculada
independentemente.

**Alcance da decisão:** ela **prepaga** os capítulos 12 (dualidade) e 14 (pontos interiores), que
precisariam da mesma ponte. Por isso o vetor de preços é nomeado como **o mesmo objeto que o
capítulo 12 chamará de variáveis duais** — senão a ponte cria dois nomes soltos em vez de
antecipar trabalho.

**Risco que a decisão cria, e a defesa obrigatória.** A ponte, feita bem, ensina o **oposto** da
tese: calcular $B^{-1}$ numericamente é ótimo para ver o objeto e é *precisamente a única coisa
que solver nenhum faz*. A ponte fecha com uma caixa dizendo isso em voz alta. **Esta caixa é
requisito, não estilo** — tem critério de aceite próprio na spec.

### D2 — As regras de precificação vão para o **capítulo 13**

*Dantzig*, *steepest edge* e *devex* saem do 11. O 11 fica com uma tese só: estrutura de dados e
álgebra.

**A dívida que isso cria é visível, e é paga como conteúdo, não como desculpa.** O capítulo 11
fecha a seção de estagnação com a **taxonomia dos remédios**:

> Estagnação tem duas famílias de remédio. Uma mexe em **qual coluna entra** — é precificação, e
> é o capítulo 13. A outra mexe em **como o método decide que dois números são iguais** — é
> tolerância, e é este capítulo. Saber qual das duas você está acionando é o que impede a
> conversa de virar "troquei a configuração e melhorou".

O redirecionamento **entrega um critério de diagnóstico** que o leitor não tinha. Nunca seção
própria, nunca a palavra "infelizmente", nunca parágrafo de nota editorial.

## Os quatro artefatos que esta decisão toca

O guardião apontou que a lista de ratificação tinha **um** item para **quatro** artefatos.
Corrigida:

| # | Artefato | O que muda | Estado |
|---|---|---|---|
| 1 | `livro/mapa-do-handbook.md` (vaga 13) | Registra que **recebe** a precificação | ✅ já alterado |
| 2 | `ROADMAP.md` (rodada 010) | Idem | ✅ já alterado |
| 3 | **`livro/capitulos/09-simplex.md`, linhas 625-630** | Manda a comparação entre regras para o Radar **sem endereço de capítulo**. Passa a ter endereço | ⏳ **texto publicado** |
| 4 | **`livro/capitulos/10-casos-especiais.md`, item 5 do "quando não serve"** | Promete que estagnação é tratada com "as escolhas de implementação do capítulo 11" — metade agora mora no 13 | ⏳ **condicional**, ver abaixo |

**Sobre o item 4.** Duas saídas, e a escolha é do autor: *(a)* o capítulo 11 **assume a promessa
inteira**, tratando estagnação e apenas apontando o endereço da outra família; ou *(b)* o item 5
do capítulo 10 é editado. **A conduta adotada é (a)** — porque a taxonomia dos remédios já
entrega o que a promessa prometia, e editar texto publicado sem necessidade é pior. Se o
experimento não produzir instância que estagne, (a) deixa de ser possível e (b) vira obrigatório
**na mesma rodada**.

Decidir isso **depois** de escrever o capítulo seria decidir sob pressão de trabalho já feito.

## Alternativas avaliadas

**Assumir álgebra linear sem ponte.** *Rejeitada pelo autor.* Seria o primeiro capítulo a exigir
pré-requisito que os anteriores não pediram, sem aviso.

**Ficar no nível da ideia, com o rigor só no `po-zero`.** *Rejeitada pelo autor.* O objetivo O1
do capítulo — escrever o Simplex em forma matricial — teria de cair, e a ponte apenas mudaria de
endereço: os capítulos 12 e 14 pagariam, com juros.

**Precificação dentro do capítulo 11.** *Rejeitada pelo autor.* É continuação direta do capítulo
10, mas engordaria um capítulo que já carrega forma matricial, esparsidade, estagnação e
tolerância. Uma tese por capítulo.

## Consequências

- O capítulo 11 fica maior do que a estimativa inicial, e o teto passa a ser **aferido por
  máquina**, não prometido.
- Os capítulos 12 e 14 nascem mais baratos.
- O glossário ganha $B$, $N$, $y$ — e o verbete **custo reduzido** fica **incompleto**: hoje
  (`livro/glossario.md`, linhas 102-104) define o objeto pelo **efeito**, sem a leitura por preço
  $c_j - y^{\top}a_j$, que é justamente a que o capítulo 12 vai reaproveitar. Corrigir é
  requisito desta rodada.
- **A dívida do leitor cresce:** entre a promessa do capítulo 10 e o pagamento no 13 haverá dois
  capítulos e duas rodadas. Se a rodada 010 escorregar, a dívida envelhece — e o `ROADMAP` é o
  lugar onde isso fica visível.
