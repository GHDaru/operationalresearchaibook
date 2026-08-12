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

> **O1 sobrevive porque o autor escolheu construir a ponte** (C1). Na opção "ficar no nível da
> ideia", este objetivo teria de cair — e está registrado aqui para que a relação entre a decisão
> e o objetivo fique rastreável.

## O que a rodada mede (Princípio IV)

Uma etapa nova do `po-zero`, `etapa-05-revisado`, que **não** ensina um método novo: ela mostra o
**mesmo** método, escrito de outro jeito, e mede a diferença. A comparação é contra a etapa 03,
que está publicada.

| Medição | O que ela prova |
|---|---|
| **A mesma instância resolvida pelas duas formas, passo a passo, lado a lado** — com o pivô visível: qual linha, qual coluna, qual elemento | É a demonstração central. Sem ver os dois caminhos, "a forma revisada faz menos trabalho" é retórica. Vem do formato que o autor usa em sala |
| Forma revisada e quadro dão **a mesma resposta** nas instâncias das etapas 03 e 04 | O capítulo é sobre implementação, não sobre método. Se a resposta mudar, o capítulo está errado |
| **Contagem de operações** e de valores tocados por iteração, nas duas formas, em instâncias de tamanho crescente | O ganho da forma revisada deixa de ser afirmação e vira curva |
| **Densidade** da matriz nas instâncias sintéticas | Mostra que o ganho depende da esparsidade — e some quando ela some |
| A mesma instância em **`Fraction` e em `float`** | O item 4 do capítulo 10, pago: onde o arredondamento muda o veredito |
| Uma instância que **estagna** — muitas iterações sem melhora, e finitas | Separa estagnação de ciclagem com o instrumento, não com a prosa |

**Compromisso de honestidade, declarado antes de medir:** se a forma revisada **não** ganhar nas
instâncias que este handbook consegue construir na CPU (*Central Processing Unit*, unidade central de processamento), isso entra no capítulo como resultado. O
livro não vai afirmar um ganho que o experimento não mostrar — e a explicação, nesse caso, passa
a ser *por que o ganho só aparece em escala que não cabe aqui*, o que também é conteúdo.

## Critérios de aceite

| # | | Critério |
|---|---|---|
| **A1** | M | ≥3 exercícios com devolutiva que explica, cada um rastreando a um objetivo; ≥1 vídeo curado |
| **A2** | M | Seção **"De onde isto veio"** (Princípio XII), com a ideia reaproveitável declarada |
| **A3** | M | Seção **"quando não serve"** (Princípio II) |
| **A4** | M | `po-zero/etapa-05-revisado` regenera todos os números do capítulo por script, com saída determinística |
| **A5** | M | A forma revisada devolve **o mesmo vértice e o mesmo valor** que a etapa 03 em todas as instâncias publicadas. *"Mesma resposta" era ambíguo num livro que acabou de ensinar múltiplos ótimos: sob mais de um ótimo o valor não muda e o plano muda* |
| **A6a** | M | A edição do capítulo 09 (linhas 625-630) dá endereço à comparação entre regras: `git diff` mostra "capítulo 13" |
| **A6b** | H | O capítulo 11 ancora explicitamente nas duas promessas — capítulos 09 e 10 — e diz de onde vieram |
| **A7** | M | Build verde, `verifica-fontes` verde, e **pelo menos um teste NOVO** do tutor para a capacidade de A8. *"24+ testes" já estava satisfeito hoje: são exatamente 24 — piso que o passado cumpre não é piso* |
| **A8** | M | Capacidade nova do tutor nos dois lados do espelho |
| **A9** | H | `HISTORICO.md`, `videoteca.md`, `glossario.md`, `bibliografia.md` e Radar atualizados |
| **A10** | H | **Revisão em contexto fresco** |
| **A11** | M | Toda fonte nova com identificador de objeto digital (DOI, *Digital Object Identifier*) passa pelo portão da rodada 007 — **é o primeiro capítulo que nasce sob o portão**. A cobertura é declarada em número na verificação: as fontes históricas prováveis deste capítulo (relatórios técnicos dos anos 1950) tipicamente **não têm DOI** e ficam fora do alcance |
| **A12** | M | `wc -l livro/capitulos/11-*.md` ≤ **722** — o tamanho medido do capítulo 09. Checkpoint aos 450 |
| **A13** | M | Os blocos de mecânica (ponte + matemática + algoritmo + código) ≤ **50%** das linhas do capítulo. É o instrumento do risco "virar capítulo de engenharia de software" |
| **A14** | M | A seção "De onde isto veio" **não afirma o aperto histórico sem fonte**: ou há fonte aberta, ou o aperto é declarado `⏳` |
| **A15** | M | O capítulo entra em `publicar/sumario.json` e no mapa — *é possível escrever o capítulo inteiro e ele não existir no livro* |
| **A16** | M | A **caixa que fecha a ponte** existe: o capítulo diz que calcular $B^{-1}$ é o que solver nenhum faz. *O plano a chama de "a linha mais importante do capítulo" e ela não tinha critério* |
| **A17** | M | O verbete **custo reduzido** do glossário passa a trazer a leitura por preço, $c_j - y^\top a_j$ |
| **A18** | M | **Todo objetivo** (O1–O5) tem ≥1 exercício. *Com 5 objetivos e piso de 3 exercícios, dois deles em ponto flutuante, O1/O2/O3 poderiam terminar sem evidência — Backward Design invertido* |
| **A19** | M | A `etapa-05` publica semente, versões, máquina, critério de parada e a **convenção de contagem**; e **todas** as instâncias geradas, não as que mostraram o efeito ([ADR 0012](../../adr/0012-o-desenho-da-medicao-do-capitulo-11.md)) |
| **A20** | M | A **saída crua da primeira execução** é colada na verificação, antes de qualquer ajuste — critério herdado da rodada 007 |
| **A21** | M | O solver aberto confere o ótimo de toda instância publicada — **testemunha independente**, como na etapa 04 |
| **A22** | M | `po-zero/etapa-03-simplex/resultados.json` permanece **byte a byte idêntico** (`0d427a9f…`) |
| **A23** | M | O corpus do tutor e `livro/exercicios.json` são regenerados e o gating por capítulo cobre o 11 |

## Clarify

**C1 — Qual é o piso de álgebra linear?** → **Construir a ponte dentro do capítulo.**
*Decisão do autor, 2026-08-12.* A forma revisada exige matriz inversa e resolução de sistema, e o
handbook nunca exigiu isso: o capítulo 08 foi geométrico e o 09, aritmético. A lacuna é real, e
fechá-la aqui **paga adiantado** o capítulo 12 (dualidade) e o 14 (pontos interiores) — que
precisariam da mesma ponte. O capítulo fica mais longo; ninguém fica para trás.

> Consequência para o esqueleto: a ponte é uma seção própria, **antes** de "A matemática", e o
> Guia Editorial manda que ela venha depois da intuição. O custo reduzido é apresentado **como
> preço-sombra**, porque essa leitura é a que o capítulo 12 vai reaproveitar.

**C3 — Onde ficam as regras de precificação?** → **No capítulo 13.**
*Decisão do autor, 2026-08-12.* O 11 fica com uma tese só: estrutura de dados e álgebra. O
catálogo (*Dantzig*, *steepest edge*, *devex*) e a comparação medida vão para a análise de
desempenho, junto da sensibilidade.

> **Dívida declarada, e ela é visível ao leitor.** O capítulo 10 prometeu que a conversa sobre
> regra de pivoteamento continuaria; agora ela continua **dois capítulos depois**. O capítulo 11
> tem de dizer isso em voz alta, com o endereço — silenciar a promessa seria pior do que adiá-la.
> O `ROADMAP` e a vaga 13 do mapa registram o recebimento.

**C2 — Fatoração LU entra?** → **Sim, como caixa-preta declarada em voz alta, com o
envelhecimento MEDIDO.** Nem conteúdo com rigor (seria meio capítulo de métodos numéricos), nem
fora (o verbo "refatora" **já está publicado** no capítulo 09, e verbo publicado sem referente é
jargão órfão). A âncora é barata porque reusa o que o leitor já fez: *o pivoteamento do capítulo
09 já é eliminação de Gauss, e fatorar é guardar essa eliminação em vez de jogá-la fora.*
**Sem a medição do envelhecimento, o assunto cai para uma frase.**

**C4 — Até onde vai o ponto flutuante?** → **Uma ideia só, em seção própria:** *tolerância é
decisão de modelagem e tem unidade*. Fica fora tudo que é representação de número — IEEE 754,
mantissa, épsilon de máquina, condicionamento. Fecha uma dívida do capítulo 09 que ninguém tinha
cobrado: o 09 ensinou que **$M$ pequeno demais mente sobre inviabilidade**; num solver real $M$ é
obrigatoriamente um número, e **$M$ grande demais mente sobre viabilidade**. O aluno conhece
metade da simetria.

*As duas decisões vêm de consulta ao especialista de didática, revisada depois que o autor
respondeu C1 e C3. **Alteram o esqueleto do Guia Editorial** — duas seções novas — e por isso
estão registradas no [ADR 0012](../../adr/0012-o-desenho-da-medicao-do-capitulo-11.md) e
declaradas como desvio no plano.*

## Riscos que a spec já enxerga

| Risco | Por que importa |
|---|---|
| **Virar capítulo de engenharia de software** | O leitor é aluno de Pesquisa Operacional (PO). A pergunta é "por que o solver não faz o que eu fiz", não "como escrever um solver" |
| **Afirmar ganho sem medir** | Já declarado acima: o compromisso é publicar o que o experimento mostrar |
| **A etapa 05 duplicar a 03** | A 03 foi parametrizada na rodada 006 em vez de duplicada. A 05 deve reusar `Restricao`, `CustoM` e as instâncias — e a comparação exige que as duas leiam a **mesma** entrada |
| **Estagnação virar palavra** | Se o experimento não produzir uma instância que estagne de verdade, o capítulo não pode ensinar a diagnosticá-la |
