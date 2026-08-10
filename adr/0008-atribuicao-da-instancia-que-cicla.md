# ADR 0008 — Como atribuir a instância que cicla, e quanto da regra de Bland entra

**Data:** 2026-08-09 · **Status:** aceito · **Rodada:** 006 (capítulo 10)
· **Decisão por:** consulta a especialista de pesquisa + leitura de fonte primária

## Contexto

O capítulo 10 vai **publicar e executar** uma instância de Programação Linear que faz o Simplex
ciclar. Publicar uma instância exige dizer de quem ela é — e o Princípio XII proíbe inventar
história, especialmente a que soa bem.

A atribuição corrente, repetida em quase todo material didático, é a **E. M. L. Beale (1955)**.
O especialista de pesquisa consultado levantou três problemas com aceitá-la sem exame, e a
leitura de fonte primária confirmou dois deles.

## O que foi apurado

### Lido na fonte ✓

**DANTZIG, G. B.; ORDEN, A.; WOLFE, P.** "The generalized simplex method for minimizing a linear
form under linear inequality restraints". *Pacific Journal of Mathematics*, v. 5, n. 2,
p. 183–195, 1955. [PDF aberto](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p04-s.pdf)

Duas passagens decidem a questão:

> *"para certos exemplos, **Alan Hoffman** e um dos autores (**Wolfe**) mostraram que era possível
> repetir a base e assim **ciclar para sempre**, com o valor da solução permanecendo inalterado e
> maior que o mínimo desejado."*

> *"por outro lado, é interessante notar que, **embora a maioria dos problemas que surgem de
> fontes práticas (na experiência dos autores) tenha sido degenerada, nenhum jamais ciclou**."*

**HALL, J. A. J.; McKINNON, K. I. M.** "The simplest examples where the simplex method cycles and
conditions where EXPAND fails to prevent cycling". *Mathematical Programming*, v. 100, 2004.
DOI [10.1007/s10107-003-0488-1](https://doi.org/10.1007/s10107-003-0488-1) ·
[arXiv](https://arxiv.org/abs/math/0012242)

> *"Exemplos como o de Beale foram **construídos** para mostrar que isso pode acontecer, embora
> tais exemplos pareçam ser **muito raros na prática**."*

E dois achados que o capítulo precisa absorver: a ciclagem ocorre **tanto** com o critério do
custo reduzido mais negativo **quanto** com *steepest edge*; e o procedimento anticiclagem
**EXPAND**, o dos solvers reais, **não tem garantia** de evitá-la. O problema prático comum não é
o ciclo, é o ***stalling*** — uma sequência longa, porém finita, de iterações sem melhora.

### Metadados conferidos ✓ᵐ, conteúdo não lido

- **BEALE, E. M. L.** "Cycling in the **dual** simplex algorithm". *Naval Research Logistics
  Quarterly*, v. 2, n. 4, p. 269–275, 1955.
  DOI [10.1002/nav.3800020406](https://doi.org/10.1002/nav.3800020406).
- **BLAND, R. G.** "New Finite Pivoting **Rules** for the Simplex Method". *Mathematics of
  Operations Research*, v. 2, n. 2, p. 103–107, 1977.
  DOI [10.1287/moor.2.2.103](https://doi.org/10.1287/moor.2.2.103).
- **GILL, MURRAY, SAUNDERS, WRIGHT.** "A practical anti-cycling procedure for linearly
  constrained optimization". *Mathematical Programming*, v. 45, p. 437–474, 1989.
  DOI [10.1007/BF01589114](https://doi.org/10.1007/BF01589114).

### O problema com a atribuição corrente

1. **O título de Beale fala em simplex *dual*.** A instância que o handbook executa é **primal**.
   Afirmar que ela aparece *literalmente* naquele artigo seria uma afirmação não verificada.
2. **A prioridade não é de Beale.** Fonte de 1955, lida, credita os primeiros exemplos a
   **Hoffman** e a **Wolfe**.
3. **O artigo de Bland anuncia *regras*, no plural.** Chamar "a regra de Bland" no singular é uso
   didático, não o do artigo — e o enunciado exato do desempate de saída (índice da variável
   básica ou índice da linha? a distinção muda a implementação) **não foi confirmado**.

## Decisão

**D3 — a instância é publicada com atribuição em três camadas, e nenhuma delas mente.**

O capítulo dirá, em substância:

- os **primeiros** exemplos de ciclagem são creditados a **Hoffman** e a **Wolfe**, e isso está
  registrado em fonte de 1955 que este handbook leu (✓);
- a instância que o **ensino** faz circular é atribuída a **Beale (1955)** (✓ᵐ), e o handbook
  **não afirma** que a forma primal executada aqui apareça literalmente naquele artigo (⏳);
- **o ótimo e o ciclo não são citados: são medidos** no `po-zero` (Princípio IV). O que o
  handbook afirma sobre esta instância, ele executa.

Rejeitada a alternativa de **construir uma instância própria** para evitar a questão de
atribuição: perderia a conexão com a literatura que o aluno vai encontrar, e trocaria um problema
de procedência por um de isolamento.

Rejeitada também a de **repetir "exemplo de Beale" sem ressalva**, que é o que quase todo
material faz. É barato e é exatamente o que o Princípio XII proíbe.

**D4 — Bland entra por demonstração, não por prova.**

O capítulo **mede** que a regra termina onde a de Dantzig cicla, na mesma instância, com o modelo
intacto. **Não prova** terminação: a prova é apontada como leitura, e o enunciado exato fica
marcado `⏳` enquanto o artigo não abrir.

A razão é de escopo e de honestidade. Provar terminação exige maquinário que o capítulo não tem e
que não serve ao objetivo de aprendizagem; e afirmar o enunciado exato de um artigo não lido seria
o mesmo defeito que este ADR existe para evitar.

## Emenda — a instância condutora do capítulo (D2 da spec)

Acrescentada em 2026-08-09, depois de o guardião de processo apontar que esta decisão estava
tomada e **não registrada**: ela vivia só numa tabela de "decisões de implementação" do plano, o
que descumpre o critério A11 da spec. O apontamento estava certo.

**A decisão:** o capítulo usa **duas** instâncias, e a divisão não é de conveniência.

| Fenômeno | Instância | Por quê |
|---|---|---|
| Vértice degenerado | **Montadora**, com um contrato limitando o total montado a 10 | Nasce de uma restrição de negócio plausível, redundante por acidente. É exatamente o caso que o capítulo ensina a diagnosticar |
| Mais de um plano ótimo | **Montadora**, com lucro (100, 200) | O objetivo fica paralelo à restrição de memória. Mesma história, um parâmetro trocado |
| Sem teto e sem plano | **Montadora**, casos já vistos nos capítulos 07 e 09 | Reencontro, não reensino |
| Ciclagem | **A instância clássica**, sem relação com a montadora | Ciclagem **não ocorre por acaso**: exige coeficientes construídos. Forçá-la na montadora exigiria números artificiais e ensinaria a coisa errada — que o ciclo é comum |

**A troca de instância é ela mesma a lição.** Quatro dos cinco vereditos aparecem numa fábrica
que o leitor conhece há três capítulos; o quinto precisa de uma instância de laboratório. Essa
assimetria é o argumento: *o que aparece na sua fábrica é do modelo; o que precisa ser construído
em laboratório é do método.* Está coerente com a tese fixada no
[ADR 0007](0007-fronteira-entre-modelo-e-metodo.md), e é dita ao leitor em vez de escondida.

**Alternativa rejeitada:** induzir ciclagem na montadora com coeficientes fabricados. Manteria a
continuidade narrativa e mentiria sobre a raridade do fenômeno — fonte lida de 2004 registra que
tais exemplos "parecem ser muito raros na prática".

## Consequências

**Boas:**

- O capítulo ganha **duas citações de fonte primária lida**, e uma delas — *"a maioria dos
  problemas práticos tem sido degenerada, nenhum jamais ciclou"*, de 1955 — é a **tese do
  capítulo dita pelos próprios autores do método**. Vale mais do que qualquer parágrafo meu.
- Ganha também o *stalling* de Hall e McKinnon, que corrige um mal-entendido comum: o problema
  prático não é o ciclo, é a estagnação.
- E ganha o fato incômodo de que **EXPAND, o procedimento dos solvers reais, não tem garantia** —
  o que impede o capítulo de terminar com um final feliz falso.

**Custosas, e assumidas:**

- **A seção de origem fica com ressalvas visíveis** onde a maioria dos livros afirma sem hesitar.
  Um leitor apressado pode ler isso como insegurança. É o preço do Princípio XII, e ele é menor
  do que o de atribuir errado.
- **Três itens continuam `⏳`** — a forma primal em Beale, o enunciado exato de Bland e a
  atribuição do *big-M* a Charnes. Os três dependem de acesso que este ambiente não tem, e ficam
  na fila de verificação do [estudo 002](../estudos/002-historia-dos-metodos.md).
