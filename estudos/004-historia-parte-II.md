# Estudo 004 — História da Parte II, em lote

**Data:** 2026-08-12 · **Serve aos capítulos:** 11, 12, 13, 14, 15, e às antecipações 38 e 77
· **Regra que este documento cumpre:** [ADR 0013](../adr/0013-o-que-e-a-v0.md), D4 — *nenhum
capítulo é escrito antes de a sua entrada existir aqui*.

## Por que em lote

Precedente que decidiu a regra: a sessão concentrada da rodada 005 achou a ligação **Motzkin →
Motzkin** entre os capítulos 08 e 09 — o mesmo matemático nas duas pontas, a quem se atribui o
nome *simplex*. Pesquisa capítulo a capítulo teria perdido, porque cada uma teria parado ao achar
o que bastava para o seu capítulo.

## Selos

Os mesmos da [bibliografia](../livro/bibliografia.md): `✓` aberto e lido · `✓ᵐ` metadados
conferidos · `⏳` atribuição corrente, não confirmada · `❌` procurado e não encontrado.

**Nesta sessão, todo DOI foi conferido em duas camadas:** metadados no Crossref **e existência no
registro** (*Handle System*, `responseCode=1`) — que é o portão da rodada 007 aplicado à pesquisa,
antes de a entrada chegar à bibliografia.

---

## Capítulo 11 — Simplex revisado

### ✓ᵐ A fonte primária, e ela fecha uma dívida do plano 008

**DANTZIG, George B.; ORCHARD-HAYS, William.** "The product form for the inverse in the simplex
method". *Mathematical Tables and Other Aids to Computation*, 1954.
DOI [10.2307/2001993](https://doi.org/10.2307/2001993) · espelho na AMS:
[10.1090/s0025-5718-1954-0061469-8](https://doi.org/10.1090/s0025-5718-1954-0061469-8)

O plano 008 reservava 55 linhas para a seção "De onde isto veio" **sem uma fonte candidata
nomeada**, e o guardião marcou isso como violação do Princípio XII. **Está fechado**: existe fonte
primária, de 1954, com os dois autores certos e o título exato do artifício que o capítulo 11
ensina.

> **O que ainda não sei, e não vou afirmar:** o conteúdo. O `⏳` que resta é se o artigo declara
> o **aperto de memória de máquina** como motivo — que é a tese histórica que o meu plano
> escreveu antes de ter fonte. Se o texto não sustentar, **a tese cai e a seção encolhe**, como
> manda o critério A14.

### ✓ᵐ A continuação, que dá a data da atualização

**DANTZIG, G. B.; HARVEY, R. P.; McKNIGHT, R. D.** "Updating the product form of the inverse for
the revised simplex method", 1964. DOI [10.21236/ad0614576](https://doi.org/10.21236/ad0614576)

Relatório técnico. É a fonte do verbo **"refatorar"** — a atualização da fatoração ao longo das
iterações, que o capítulo 09 publicou como promessa e o 11 tem de pagar.

---

## Capítulo 12 — Dualidade

### ✓ᵐ **GALE, D.; KUHN, H. W.; TUCKER, A. W.** "On symmetric games", 1951.
DOI [10.1515/9781400881727-008](https://doi.org/10.1515/9781400881727-008)

Capítulo em coletânea de Princeton. É o trio canônico da dualidade em Programação Linear.

### ⏳ A ligação von Neumann → dualidade
A história corrente atribui a von Neumann, em conversa com Dantzig em 1947, a percepção de que
Programação Linear e jogos de soma zero são o mesmo objeto. **Buscado e não localizado** por
identificador nesta sessão: as buscas por "von Neumann duality" devolvem álgebras de von Neumann,
que é outro campo inteiro. Fica `⏳`, e o capítulo 12 **não afirma** a cena.

### ❌ O artigo canônico de "Linear programming and the theory of games"
Procurado, não encontrado por DOI. É de 1951, em coletânea, e a coletânea pode não ter
identificador por capítulo. **Não invento a referência.**

---

## Capítulo 13 — Análise de sensibilidade

### ⏳ Fonte primária não localizada
As buscas devolveram trabalho de **1976 sobre pós-otimalidade em programação INTEIRA**
(Geoffrion & Nauss, `10.21236/ada023278`) — que é outro assunto e outro capítulo. A análise de
sensibilidade em PL é anterior e provavelmente nasce nos próprios manuais.

**Consequência declarada:** o capítulo 13 nasce com a seção "De onde isto veio — em dívida",
nomeando o que falta. É exatamente o caso que o D4 previu, e é conforme.

---

## Capítulo 14 — Pontos interiores

### ✓ᵐ **KHACHIYAN, L. G.** "Polynomial algorithms in linear programming", 1980.
*USSR Computational Mathematics and Mathematical Physics*.
DOI [10.1016/0041-5553(80)90061-0](https://doi.org/10.1016/0041-5553(80)90061-0)

O método do elipsoide — a primeira prova de que Programação Linear é polinomial. Conecta com o
[estudo 002](002-historia-dos-metodos.md), que registra a repercussão de 1979 no *New York Times*.

### ✓ᵐ **KARMARKAR, N.** "A new polynomial-time algorithm for linear programming".
*Combinatorica*, 1984. DOI [10.1007/bf02579150](https://doi.org/10.1007/bf02579150) ·
versão do simpósio: [10.1145/800057.808695](https://doi.org/10.1145/800057.808695)

O que tornou pontos interiores **praticável**, não só polinomial. O estudo 002 registra `⏳` a
controvérsia da patente da AT&T — segue `⏳`.

---

## Capítulo 38 — Convexidade (antecipado)

### ✓ᵐ **ROCKAFELLAR, R. T.** *Convex Analysis*. Princeton, 1970.
DOI [10.1515/9781400873173](https://doi.org/10.1515/9781400873173)

A referência canônica. **Uso previsto: ponteiro, não fonte de afirmação** — é livro inteiro, e o
capítulo 38 da v0 é curto.

---

## Capítulo 77 — Como ler um artigo (antecipado)

### ✓ᵐ **KESHAV, S.** "How to read a paper". *ACM SIGCOMM Computer Communication Review*, 2007.
DOI [10.1145/1273445.1273458](https://doi.org/10.1145/1273445.1273458)

O método das três passadas. É de redes, não de Pesquisa Operacional — e **isso é uma escolha, não
um descuido**: o capítulo 77 ensina a ler artigo, e o método é de leitura, não de domínio. O
capítulo declara a origem.

---

## Balanço desta sessão

| | |
|---|---|
| Identificadores localizados e **existentes no registro** | **7 de 7** (`responseCode=1`) |
| Metadados conferidos no Crossref | 7 |
| Conteúdo aberto e lido | **0** — nenhum `✓` pleno |
| Capítulos com fonte primária nomeada | 11, 12, 14, 38, 77 |
| Capítulos que nascem **em dívida declarada** | **13** (sensibilidade), e parcialmente o **12** |

### O alarme do D4 não disparou, e é bom que não

O ADR 0013 manda parar se um lote fechar com **zero `⏳`**, porque num *long run* isso é sinal de
fabricação, não de boa pesquisa. Esta sessão fecha com **três dívidas nomeadas** — a cena de von
Neumann, o artigo de 1951 sem identificador, e a origem da análise de sensibilidade. É a
proporção que o capítulo 09 tem e que a didática apontou como sinal de saúde.

**Nenhuma delas será preenchida com invenção.** Onde não houver fonte, o capítulo diz que não há.
