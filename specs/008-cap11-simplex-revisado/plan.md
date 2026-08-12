# Plan 008 — Capítulo 11: Simplex revisado e implementação eficiente

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-12
· **Estado:** escrito **antes** de qualquer linha de capítulo ou de código

## Constitution Check — os 12 princípios do handbook

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | ≥3 exercícios com devolutiva + 1 vídeo. O bloco de ponto flutuante recebe **dois** exercícios, por ser o assunto com maior distância entre "achar que entendeu" e "decidir certo" | ✅ planejado |
| II | Modelar antes de resolver | Seção "quando não serve" obrigatória. **Tensão real:** este é o capítulo mais próximo de implementação de todo o handbook, e o princípio manda a ordem intuição → matemática → código. A ponte de álgebra entra **depois** da intuição, e a medição vem **depois** da matemática | ⚠️ **com instrumento**: "vigiado" era adjetivo. O gatilho agora é aferível — se os blocos de mecânica (ponte + matemática + algoritmo + código) passarem de **50% das linhas do capítulo**, o capítulo derivou. Critério A13, medido por seção |
| III | Evidência acima de retórica | Todo número sai da `etapa-05`, e a spec se compromete a publicar o que o experimento mostrar. **Mas o próprio plano violava isso:** afirmava que a instrumentação "já produz as duas curvas — densidade crescendo e resíduo subindo", resultado pré-declarado como fato antes de existir uma linha de código. E faltavam semente, versões, máquina e critério de parada | ⚠️ **corrigido**: frase apagada; o desenho da medição virou [ADR 0012](../../adr/0012-o-desenho-da-medicao-do-capitulo-11.md), com pré-registro de instâncias |
| IV | Fonte-base é o experimento executável | `po-zero/etapa-05-revisado`, em CPU, sem licença paga | ✅ planejado |
| V | Arquitetura em três camadas | Capítulo de núcleo | ✅ |
| VI | Atualização por Radar | A ordem (Radar antes da bibliografia) está certa, mas **nenhuma fonte candidata estava nomeada** — planejar a ordem sem planejar o objeto é ✅ vazio. O Guia pede 2 a 4 artigos traduzidos em decisão nos "Fundamentos científicos" | ⚠️ **tarefa própria**: levantar as candidatas **antes** de escrever a seção, e aceitar que possam não existir com acesso aberto |
| VII | Livro vivo | `HISTORICO.md`; a ficha da `etapa-05` datada | ✅ planejado |
| VIII | Português canônico | *Stalling* já consagrado com tradução. **Colisão detectada:** "escalonamento" já significa *scheduling* na vaga 15 do mapa — o capítulo 11 usa **"escala do modelo"**, e nunca "escalonamento" | ✅ |
| IX | Sigla nunca nasce nua | **LU** nasce vestida: *Lower-Upper*, triangular **inferior** e **superior**. Verbetes novos nos **dois** lugares. **Mas a contagem reinicia a cada documento, e este plano e a spec tinham `PO`, `CPU` e `DOI` nuas** — repetição literal do bloqueio B6 da rodada 007. Acertar a sigla do capítulo e errar as do documento é o princípio julgado pela intenção | ⚠️ **corrigido nos dois documentos** |
| X | Direitos autorais | Texto autoral; a instância é do autor | ✅ |
| XI | DoD verificável | Build, portão de fontes, testes, e **revisão em contexto fresco** | ✅ planejado |
| XII | Nenhum método cai do céu | O aperto declarado — a memória de 1950-60 não comportava o quadro — **é história, e história é afirmação** (XII.4 + III). O plano reservava 55 linhas para uma seção cuja tese central não tinha fonte candidata. *"Inventar história é pior do que omiti-la, porque é convincente"* | ⚠️ **a seção não é escrita antes da fonte**: sem fonte aberta, o aperto é declarado `⏳` e a seção encolhe. Critério A14 |

## Constitution Check — os 7 princípios de processo do Maestro

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | Spec-Driven | Spec escrita antes; clarify resolvido — C1 e C3 **pelo autor**, C2 e C4 por especialista. **A spec está "aguardando ratificação"**, e no plano 007 esse mesmo estado ficou ⚠️ depois do veredito do guardião | ⚠️ **coerente com a 007** |
| II | Orquestração humano-governada | O autor decidiu as duas perguntas que definem o que o capítulo é. Nada publicado | ✅ |
| III | Reversibilidade / gates de risco | Tudo na branch `claude/handbook-pesquisa-operacional-ucbbpu`. A lista de ratificação dizia **um** item e a decisão toca **quatro** artefatos — dois já alterados (mapa, `ROADMAP`), o capítulo 09 publicado, e o capítulo 10 condicionalmente | ⚠️ **corrigido**: os quatro estão tabelados no [ADR 0011](../../adr/0011-onde-mora-cada-assunto-da-parte-II.md) |
| IV | Test-First / DoD verificável | A `etapa-05` é escrita **antes** do capítulo, e o texto só afirma o que ela mede | ✅ |
| V | Economia de contexto / fronteira | Três frentes independentes: a `etapa-05` (medição), o capítulo (texto), o aparato (glossário, mapa, Radar). A instância é a fronteira compartilhada, e ela **já existe** | ✅ |
| VI | Artefatos vivos | Capítulo, código, glossário, mapa e histórico no mesmo *commit range* | ✅ planejado |
| VII | Governança leve / YAGNI | A ilha interativa do quadro passo a passo **não** entra nesta rodada: foi para o `ROADMAP`. Esta rodada produz a **medição**; a interface vem depois, se a medição justificar | ✅ |

**Violações que impediriam a rodada:** nenhuma. **Sete ⚠️** — cinco na tabela do handbook, duas na
do Maestro. A primeira versão tinha duas, e o guardião mostrou que quatro linhas ✅ eram
otimismo: II sem instrumento, III com resultado pré-declarado, IX com sigla nua no próprio
documento, XII com história sem fonte. A lição das rodadas 006 e 007, que este plano não tinha
aplicado: **converter compromisso em instrumento**.

## O achado que barateia a rodada, e ele foi medido

O especialista de didática afirmou, e eu **verifiquei antes de aceitar** — porque o mesmo agente
já tinha errado um fato nesta sessão:

```
quadro final do capítulo 09        B⁻¹ calculada do zero      y = c_B·B⁻¹
    f1     f2                          [ 2  -1]                [50  50]
     2     -1                          [-1   1]
    -1      1
    50     50   ← linha z
```

**O quadro final do capítulo 09 já contém $B^{-1}$.** As colunas sob $f_1$ e $f_2$ **são** a
inversa da base; os dois `50` da linha $z$ **são** o vetor de preços $y = c_B B^{-1}$. Conferido
com $B = \begin{smallmatrix}1&1\\1&2\end{smallmatrix}$, cuja inversa é exatamente essa.

Consequência para o plano: **a ponte de álgebra não constrói exemplo — ela renomeia números que o
leitor já conferiu à mão.** É o tipo de linha mais barata que existe neste handbook, e é o que
permite o orçamento abaixo caber.

## O risco que a decisão C1 cria, e a defesa

Apontado pelo especialista, e é o ponto mais fino do capítulo: **a ponte, feita bem, ensina o
oposto da tese.** Calcular $B^{-1}$ numericamente para a montadora é ótimo para o leitor ver o
objeto — e é *precisamente a única coisa que solver nenhum faz*. Sem aviso, o leitor sai
convencido de que o Simplex revisado inverte matrizes.

**Defesa:** uma caixa de ~8 linhas fechando a ponte — *"acabamos de fazer, de propósito, o que o
capítulo inteiro diz que não se faz; foi para você ver o objeto. Daqui em diante ele nunca mais
aparece calculado."* É a linha mais importante do capítulo, e está orçada dentro da ponte.

**Segunda consequência:** a caixa-preta da fatoração precisa ser **declarada em voz alta**, não
implícita. Depois de uma ponte cuidadosa, o leitor fica preparado para perguntar "então como se
calcula $B^{-1}$?", e recusar a resposta em silêncio lê-se como evasiva.

## Orçamento

**Teto: 722 linhas — medido, não estimado.** É o tamanho exato de `09-simplex.md`
(`wc -l`: 722; o `10-casos-especiais.md` tem 478). Vira **critério de aceite A12, verificável por
máquina**, com checkpoint aos 450.

> **O que este orçamento era antes, e por que foi refeito.** A primeira versão dizia "teto duro
> 720 — o tamanho do capítulo 09" e "o 11 tem tamanho de 10, não de 09" — enquanto a tabela
> somava **681 linhas, que são 142% do capítulo 10**. Um plano deste repositório não pode
> publicar número que o `wc -l` derruba em um segundo, e a frase que justificava o orçamento era
> desmentida pelo próprio orçamento, na mesma seção. Apontado pelo guardião.

A estimativa de blocos abaixo continua sendo **estimativa** e está declarada como tal. O que
mudou é que agora existe **aferição**: um portão, e não boa vontade. O 11 é o capítulo mais
abstrato da Parte II, então chegar perto do teto do 09 é sinal de alerta — mas alerta aferido.

| Bloco | Linhas | Nota |
|---|---:|---|
| Cabeçalho + objetivos | 22 | |
| O problema | 35 | O custo do que o quadro calcula e ninguém olha |
| De onde isto veio | 55 | O aperto é a máquina · inclui 8 de LU histórico |
| A intuição | 38 | Uma iteração só olha uma coluna |
| **Ponte de álgebra linear** | **85** | Renomeia o quadro final do 09 · inclui a caixa de 8 linhas · custo reduzido como preço-sombra (prepaga o cap. 12) |
| A matemática — o laço revisado | 55 | |
| O algoritmo | 58 | Inclui 20 de LU: o passo "refatorar" + o envelhecimento |
| Esparsidade | 35 | É do modelo, não do algoritmo (O3) |
| Estagnação | 40 | Inclui 5 da dívida do cap. 13 |
| O código — as medições | 65 | Inclui 10 da tabela de envelhecimento e 12 da tabela `Fraction`×`float` |
| **Ponto flutuante** — seção própria | 50 | "Quando dois números 'iguais' não são iguais" |
| Quando não serve | 38 | Inclui 5 de LU, 4 de float, 3 do endereço do cap. 13 |
| Fundamentos científicos | 30 | |
| Pratique + Assista | 30 | |
| Síntese + Verificação + leitura executiva | 45 | |
| **Total** | **681** | |

Fatoração LU soma **43 linhas (6,3%)**; ponto flutuante, **66 (9,7%)**. Os dois em 16% — e é
teto, não folga.

## Desvio declarado do esqueleto

O Guia Editorial §2 fixa o esqueleto de capítulo. Este capítulo **acrescenta duas seções** que
não estão lá: a **ponte de álgebra linear** (entre "A intuição" e "A matemática") e **"Quando
dois números 'iguais' não são iguais"** (entre "O código" e "Quando não serve").

O portão só exige a seção "De onde isto veio", então o desvio passaria sem registro — e é
justamente por isso que está declarado. As duas vêm de decisão: a primeira do autor
([ADR 0011](../../adr/0011-onde-mora-cada-assunto-da-parte-II.md)), a segunda de consulta a
especialista ([ADR 0012](../../adr/0012-o-desenho-da-medicao-do-capitulo-11.md)). Precedente na
casa: "Por que a ganância funciona aqui" no capítulo 09, "Quando o empate vira giro" no 10.

## O desenho da medição

Fixado no [ADR 0012](../../adr/0012-o-desenho-da-medicao-do-capitulo-11.md), depois de o guardião
apontar seis caminhos pelos quais a medição planejada produziria número que **parece** prova.

O ponto que reorganizou o resto foi a pergunta: *contagem de operações entre duas implementações
da mesma mão é evidência de quê?* O quadro da etapa 03 foi escrito para ser **legível**; a forma
revisada seria escrita para **ganhar**. A contagem mediria a diferença de intenção tanto quanto a
diferença de método.

| Decisão | O que resolve |
|---|---|
| Uma **primitiva aritmética instrumentada, compartilhada** pelas duas formas | Duas réguas não comparam nada. A convenção de contagem é publicada junto do número |
| A `etapa-05` implementa **as duas formas**; a etapa 03 fica intocada e vira **oráculo** | Resolve três de uma vez: contagem justa, `Fraction`×`float` como *mesma implementação em dois tipos*, e o hash `0d427a9f…` preservado |
| **Trajetória de pivô idêntica, afirmada** em aritmética exata; operações **por iteração** e número de iterações reportados **separados** | Sem isso, o total mistura "menos trabalho por iteração" com "outro número de iterações" |
| **Testemunha independente** (solver aberto), como na etapa 04 | A comparação entre as duas formas compartilha camada: defeito comum é invisível às duas |
| Instâncias, **semente e regra de geração congeladas antes** de olhar resultado; todas publicadas; controle negativo obrigatório (a instância densa) | O compromisso de honestidade cobria a *direção do resultado*, não a *escolha da amostra*. Gerar até aparecer é compatível com publicar o que apareceu |
| Resíduo com **magnitude absoluta** e controle | Em `Fraction` é identicamente zero; em `float` pode ser ruído de 10⁻¹⁶ com legenda de fenômeno |
| **densidade da instância** (entrada) ≠ **preenchimento** (saída) | A mesma palavra para as duas convida ao raciocínio circular |
| Limiar de estagnação **no código antes** da primeira execução, com a cascata mapeada | O corte condicional afeta O4, os exercícios que rastreiam O4 (**quebram o build**), o capítulo 10 e o tutor — o plano declarava um elo de quatro |

## Ranking de corte

> **Correção de circularidade.** A primeira versão indicava o ranking como mitigação do risco
> "virar capítulo de engenharia de software" — e o ranking marcava **"não sai"** para ponte,
> matemática, algoritmo e código: 263 linhas, exatamente onde a deriva acontece. Cortava história,
> esparsidade, estagnação e ponto flutuante, que são os blocos que fazem o capítulo ser de
> Pesquisa Operacional. Aplicado até o fim, **produzia** o risco que prometia conter.
>
> O ranking continua servindo ao **tamanho** (A12). O risco de deriva passou a ter instrumento
> próprio: **A13 — mecânica ≤ 50% das linhas**. E o "corte zero" (gordura de prosa) deixa de ser
> ilimitado: vale **uma passada**, não um recurso permanente, senão nunca se chega ao item 1.

Se estourar, o capítulo perde **nesta ordem**, sem deixar de responder *"por que o solver real
não faz o que o quadro faz?"*.

**Corte zero, antes de qualquer bloco:** gordura de prosa. Um capítulo em 780 linhas costuma ser
um de 660 com 120 de reafirmação. E **nada sai antes dos exercícios e do vídeo** (Princípio I).

| # | Bloco | Como | Por quê aqui |
|---|---|---|---|
| 1 | História | 55 → 40 | Obrigatória, não sai — mas é onde 15 linhas custam menos: o 09 já contou a fundação, e o aperto do 11 é variação. Apontar para trás em vez de recontar |
| 2 | Estagnação | **corte condicional** | Só se a `etapa-05` não produzir instância que estagne de verdade. **Acoplamento:** se sair, o item 5 do "quando não serve" do capítulo 10 vira promessa quebrada e tem de ser editado na mesma rodada |
| 3 | Fatoração LU | piso: 1 frase + endereço | Nunca para o silêncio: o verbo "refatora" **já está publicado** no capítulo 09, e verbo publicado sem referente é jargão órfão |
| 4 | Esparsidade | piso: 1 parágrafo + a coluna de densidade | Abaixo disso o capítulo passa a prometer ganho **incondicional**, que é falso |
| 5 | Ponto flutuante | piso: os três pontos + E1 | Penúltimo: é a única dívida que **nenhum outro capítulo pode pagar** |
| 6 | Ponte de álgebra | **não sai** | Decisão do autor, e prepaga os capítulos 12 e 14 |
| 7 | Forma matricial | **não sai** | **É o capítulo.** Sem ela há um ensaio sobre a pergunta, não a resposta |

## As duas dívidas de coerência que esta rodada precisa fechar

Ambas nascem da decisão C3 (precificação vai para o capítulo 13), e **ambas tocam texto
publicado**.

| Onde | O que está lá hoje | O que a rodada faz |
|---|---|---|
| **Capítulo 10**, "quando não serve", item 5 | Promete que estagnação é tratada com "a forma revisada **e as escolhas de implementação** do capítulo 11" | O capítulo 11 fecha a seção de estagnação com a **taxonomia dos remédios**, não com desculpa: uma família mexe em *qual coluna entra* (cap. 13), a outra em *como o método decide que dois números são iguais* (aqui). O redirecionamento **entrega um critério de diagnóstico** que o leitor não tinha |
| **Capítulo 09**, linhas 625-630 | Manda a comparação entre regras de pivoteamento para o Radar, **sem endereço de capítulo** | Passa a ter endereço: capítulo 13. **Se a rodada não corrigir, o handbook publica duas promessas divergentes sobre o mesmo assunto** — e o grafo de dívidas, que sustenta a credibilidade do "livro vivo", começa a mentir |

Total da primeira: **8 linhas em dois lugares**. Nunca seção própria, nunca a palavra
"infelizmente", nunca parágrafo de nota editorial — bloco cuja única função é explicar por que o
livro está organizado como está **é** o amontoado que o guia combate.

## O que a `etapa-05` mede

Escrita **antes** do capítulo. Reusa `Restricao`, `CustoM` e as instâncias da etapa 03 — a
comparação exige que as duas formas leiam a **mesma** entrada.

| Medição | Serve a |
|---|---|
| Mesma resposta que a etapa 03 em todas as instâncias publicadas | A5 — o capítulo é sobre implementação, não sobre método |
| **Os dois caminhos passo a passo, com o pivô visível** — linha, coluna, elemento | A demonstração central. Formato vindo do material de sala do autor |
| Operações e valores tocados por iteração, nas duas formas, em tamanho crescente | O2 — o ganho vira curva |
| Densidade da matriz | O3 — o ganho **some** quando a esparsidade some |
| Resíduo $\lVert Bx - b \rVert$ ao longo das iterações | O envelhecimento da fatoração, **medido**. Sem isso, LU sai do capítulo |
| A mesma instância em `Fraction` e em `float` | O5 — onde o veredito muda |
| Uma instância que estagna | O4 — separa estagnação de ciclagem com o instrumento |

**Escopo barato para o envelhecimento, sem virar métodos numéricos:** a atualização por produto
(vetores eta) é histórica e cabe em ~30 linhas de Python. **O que ela produz é o que for
medido** — e o ADR 0012, D6, fixa a desconfiança obrigatória: em `Fraction` o resíduo é
identicamente zero, e em `float` pode ser ruído de 10⁻¹⁶ com legenda de fenômeno. Se o
envelhecimento não for demonstrável na escala que cabe em CPU (*Central Processing Unit*,
unidade central de processamento), **isso é o resultado**, e a fatoração LU cai para uma frase.

## Vocabulário — o que entra nos dois lugares

`livro/glossario.md` **e** o mapa de siglas de `publicar/build.mjs`.

**Novos:** matriz básica ($B$), matriz não-básica ($N$), **vetor de preços** $y = c_B B^{-1}$
(dizendo que é o mesmo objeto que o capítulo 12 chamará de variáveis duais — senão a ponte cria
dois nomes soltos para a mesma coisa em vez de prepagar), fatoração LU, refatoração (desfazendo a
colisão com o sentido de engenharia de software, que o leitor já conhece), esparsidade,
densidade, tolerância de viabilidade.

**Verbete existente que fica incompleto:** *custo reduzido* (glossário, linhas 102-104) define o
objeto pelo **efeito** e não traz a leitura por preço, $c_j - y^{\top}a_j$ — que é justamente a
que o capítulo 12 vai reaproveitar. A partir do 11, precisa carregar as duas.

## Riscos

| Risco | Mitigação |
|---|---|
| **Virar capítulo de engenharia de software** | O leitor é aluno de Pesquisa Operacional (PO). A pergunta é "por que o solver não faz o que eu fiz", não "como escrever um solver". O ranking de corte é a régua |
| **A ponte ensinar o oposto da tese** | A caixa de 8 linhas. É a linha mais importante do capítulo |
| Afirmar ganho sem medir | Compromisso da spec, registrado antes de medir |
| Estagnação virar palavra | Corte condicional, com o acoplamento ao capítulo 10 declarado |
| A `etapa-05` duplicar a 03 | Reuso, como a 04 fez. Se duplicar, o plano falhou |
| **Aplicar o desconto da sinergia duas vezes** | A ponte barateia *"por que não se inverte"* (6 linhas). **Não** barateia *"por que se refatora"* (37), que é a metade que paga o verbo publicado |
| **O vídeo curado pode não existir** | "Forma revisada / produto da inversa" tem pouquíssimo material gratuito em português. O capítulo 09 já publicou ficha admitindo que ninguém assistiu — repetir isso é pior que declarar a lacuna. Se não houver vídeo defensável, o Princípio I **não é cumprido por cota**: a ficha diz o que falta |
| **Notação matricial no pipeline de PDF** | Este será o capítulo com mais matemática do handbook, e a geração de PDF é a parte mais frágil do motor. Verificar **cedo**, com uma seção só, antes de escrever as outras |
| **A dívida do capítulo 13 pendurada em duas rodadas** | Entre a promessa do capítulo 10 e o pagamento haverá dois capítulos. Se a rodada 010 escorregar, a dívida envelhece — e o `ROADMAP` é onde isso fica visível |
| **Corpus do tutor e registro de exercícios** | A capacidade nova cobre o espelho; o `build_corpus.py`, o `exercicios.json` e o gating do RAG não estavam cobertos por critério. Agora são A23 |

## Fora de escopo, declarado

- **A ilha interativa** do quadro passo a passo. Esta rodada produz a **medição**; a interface
  foi para o `ROADMAP`. Construir as duas juntas é o caminho para entregar mal as duas.
- **A prova por capítulo.** Rodada própria, e tem pergunta de fundo pendente com o autor.
- **A terceira restrição da montadora.** Encenação deliberada, endereçada à vaga 23 e registrada
  na ficha da instância com um `NAO_CORRIJA`.
