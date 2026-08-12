# Plan 008 — Capítulo 11: Simplex revisado e implementação eficiente

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-12
· **Estado:** escrito **antes** de qualquer linha de capítulo ou de código

## Constitution Check — os 12 princípios do handbook

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | ≥3 exercícios com devolutiva + 1 vídeo. O bloco de ponto flutuante recebe **dois** exercícios, por ser o assunto com maior distância entre "achar que entendeu" e "decidir certo" | ✅ planejado |
| II | Modelar antes de resolver | Seção "quando não serve" obrigatória. **Tensão real:** este é o capítulo mais próximo de implementação de todo o handbook, e o princípio manda a ordem intuição → matemática → código. A ponte de álgebra entra **depois** da intuição, e a medição vem **depois** da matemática | ⚠️ **vigiado**: se o capítulo virar "como escrever um solver", o princípio foi violado. O teste é a pergunta-tese, não o sumário |
| III | Evidência acima de retórica | Todo número do capítulo sai da `etapa-05`. **Compromisso registrado na spec antes de medir:** se a forma revisada não ganhar nas instâncias que cabem em CPU, isso entra como resultado | ✅ |
| IV | Fonte-base é o experimento executável | `po-zero/etapa-05-revisado`, em CPU, sem licença paga | ✅ planejado |
| V | Arquitetura em três camadas | Capítulo de núcleo | ✅ |
| VI | Atualização por Radar | As fontes novas entram no Radar **antes** da bibliografia — a rodada 006 inverteu essa ordem e a revisão apanhou | ✅ planejado |
| VII | Livro vivo | `HISTORICO.md`; a ficha da `etapa-05` datada | ✅ planejado |
| VIII | Português canônico | *Stalling* já consagrado com tradução. **Colisão detectada:** "escalonamento" já significa *scheduling* na vaga 15 do mapa — o capítulo 11 usa **"escala do modelo"**, e nunca "escalonamento" | ✅ |
| IX | Sigla nunca nasce nua | **LU** nasce vestida: *Lower-Upper*, as iniciais de triangular **inferior** e **superior**. Sigla decorada sem saber que são duas palavras é jargão órfão exemplar. Verbetes novos nos **dois** lugares (glossário + mapa do motor) | ✅ planejado |
| X | Direitos autorais | Texto autoral; a instância é do autor | ✅ |
| XI | DoD verificável | Build, portão de fontes, testes, e **revisão em contexto fresco** | ✅ planejado |
| XII | Nenhum método cai do céu | "De onde isto veio": o aperto é **a máquina** — a memória de 1950-60 não comportava o quadro inteiro, e a forma revisada nasce dessa restrição material. **Regra de corte:** nome sem mecânica é enfeite. Um nome só, se houver fonte | ✅ planejado |

## Constitution Check — os 7 princípios de processo do Maestro

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | Spec-Driven | Spec escrita antes; clarify resolvido — C1 e C3 **pelo autor**, C2 e C4 por especialista consultado | ✅ |
| II | Orquestração humano-governada | O autor decidiu as duas perguntas que definem o que o capítulo é. Nada publicado | ✅ |
| III | Reversibilidade / gates de risco | Tudo na branch. **Uma alteração toca capítulo publicado** (o 09, linhas 625-630) e vai à ratificação, como na rodada 006 | ⚠️ **item explícito de gate** |
| IV | Test-First / DoD verificável | A `etapa-05` é escrita **antes** do capítulo, e o texto só afirma o que ela mede | ✅ |
| V | Economia de contexto / fronteira | Três frentes independentes: a `etapa-05` (medição), o capítulo (texto), o aparato (glossário, mapa, Radar). A instância é a fronteira compartilhada, e ela **já existe** | ✅ |
| VI | Artefatos vivos | Capítulo, código, glossário, mapa e histórico no mesmo *commit range* | ✅ planejado |
| VII | Governança leve / YAGNI | A ilha interativa do quadro passo a passo **não** entra nesta rodada: foi para o `ROADMAP`. Esta rodada produz a **medição**; a interface vem depois, se a medição justificar | ✅ |

**Violações que impediriam a rodada:** nenhuma. **Duas ⚠️**, ambas com mecanismo declarado.

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

**Alvo: 660 linhas (± 40). Teto duro: 720** — o tamanho do capítulo 09. Passar disso é sinal de
que a tese se multiplicou: pare de escrever e volte ao ranking de corte.

O 11 tem tamanho de 10, não de 09, e é deliberado: o 09 podia ser longo porque era concreto —
quadro, números, tabelas que o leitor confere com lápis. O 11 é o capítulo **mais abstrato da
Parte II**, e densidade conceitual por palavra se compensa com **menos** palavras, não mais.

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

## Ranking de corte

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
(vetores eta) é histórica, cabe em ~30 linhas de Python e já produz as duas curvas — densidade
crescendo e resíduo subindo. LU segue caixa-preta; o **envelhecimento** deixa de ser retórica.

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
| **Virar capítulo de engenharia de software** | O leitor é aluno de PO. A pergunta é "por que o solver não faz o que eu fiz", não "como escrever um solver". O ranking de corte é a régua |
| **A ponte ensinar o oposto da tese** | A caixa de 8 linhas. É a linha mais importante do capítulo |
| Afirmar ganho sem medir | Compromisso da spec, registrado antes de medir |
| Estagnação virar palavra | Corte condicional, com o acoplamento ao capítulo 10 declarado |
| A `etapa-05` duplicar a 03 | Reuso, como a 04 fez. Se duplicar, o plano falhou |
| **Aplicar o desconto da sinergia duas vezes** | A ponte barateia *"por que não se inverte"* (6 linhas). **Não** barateia *"por que se refatora"* (37), que é a metade que paga o verbo publicado |

## Fora de escopo, declarado

- **A ilha interativa** do quadro passo a passo. Esta rodada produz a **medição**; a interface
  foi para o `ROADMAP`. Construir as duas juntas é o caminho para entregar mal as duas.
- **A prova por capítulo.** Rodada própria, e tem pergunta de fundo pendente com o autor.
- **A terceira restrição da montadora.** Encenação deliberada, endereçada à vaga 23 e registrada
  na ficha da instância com um `NAO_CORRIJA`.
