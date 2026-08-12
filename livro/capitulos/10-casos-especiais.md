# 10 — Casos especiais e degenerescência

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-09 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Ler** um veredito do solver que não seja "aqui está seu plano" e dizer **o que fazer a
respeito** — a quem avisar, o que investigar, o que renegociar.

**O2.** **Detectar** no quadro final que existe mais de um plano ótimo, e **usar** essa
informação como vantagem de negociação em vez de tratá-la como ambiguidade.

**O3.** **Reconhecer** um vértice degenerado e **caçar** a restrição redundante que o produziu.

**O4.** **Distinguir** um defeito do **modelo** de um defeito da **regra de pivoteamento**,
aplicando o teste que este capítulo instala.

## O problema

Quatro segundas-feiras na montadora dos capítulos anteriores. Em todas, o modelo roda. Em nenhuma
sai um plano de produção.

| Segunda | O que o solver devolveu | O que você diz na reunião? |
|---|---|---|
| 1ª | `Infeasible` — não existe plano | ? |
| 2ª | `Unbounded` — o lucro não tem teto | ? |
| 3ª | `Optimal`, mas o colega rodou o mesmo modelo e obteve **outro plano**, com o mesmo lucro | ? |
| 4ª | `Optimal`, e o quadro tem uma variável **na base valendo zero** | ? |

E há uma quinta situação, que não cabe na tabela porque não devolve nada: **o método roda e não
termina**. Não trava, não dá erro — pivoteia, pivoteia, e não sai do lugar.

O erro caro deste capítulo **não é de conta**. É ler `Unbounded` como boa notícia — "o lucro é
infinito!" — quando é atestado de restrição esquecida. E é apresentar um plano como *a* resposta
quando existe outro, de lucro idêntico e custo político muito menor, que ninguém procurou.

### O mapa dos cinco vereditos

Dois destes você já sabe **detectar**: o capítulo 09 ensinou. O que falta é a conduta.

| Veredito | O que o algoritmo faz | Onde se aprende a **detectar** | Onde se aprende a **conduzir** |
|---|---|---|---|
| **Não existe plano** | Artificial sobra na base com valor positivo | [Cap. 09 — *big-M*](09-simplex.md#quando-a-ficção-não-sai) | §Veredito 1, aqui |
| **Sem teto** | Nenhuma razão positiva no teste da razão | [Cap. 09 — teste da razão](09-simplex.md#quadro-0--a-partida) | §Veredito 2, aqui |
| **Mais de um plano ótimo** | Custo reduzido **zero** em variável fora da base | **Aqui** | §Veredito 3 |
| **Vértice degenerado** | Variável **na base** valendo zero | **Aqui** | §Veredito 4 |
| **O método não termina** | Uma base já visitada volta | **Aqui** | §Quando o empate vira giro |

> **Se você acabou de ler o capítulo 09**, pode passar rápido pelos dois primeiros vereditos: a
> detecção você já tem, e aqui só se acrescenta o que fazer. Os três últimos são novos.

## De onde isto veio

### O aperto: o método funcionava e ninguém sabia provar que terminava

O Simplex nasceu em 1947 e foi usado em problemas reais quase imediatamente. Só que a prova de
que ele **termina** tinha um buraco, e o buraco era exatamente o assunto deste capítulo.

A prova padrão é simples: a cada iteração o objetivo melhora, e como o número de bases é finito,
nenhuma pode se repetir — logo o método para. Mas quando há **empate no teste da razão**, o
objetivo pode **não** melhorar. E aí a prova cai.

Restava a pergunta: sem a prova, isso acontece de fato?

Aconteceu. Em 1955, num artigo que este handbook leu, **Dantzig, Orden e Wolfe** registram:

> *"para certos exemplos, **Alan Hoffman** e um dos autores (**Wolfe**) mostraram que era possível
> repetir a base e assim **ciclar para sempre**, com o valor da solução permanecendo inalterado e
> maior que o mínimo desejado."*

Os primeiros exemplos de ciclagem, portanto, são de Hoffman e de Wolfe. A instância que o
**ensino** faz circular — a que este capítulo executa — costuma ser atribuída a **Beale (1955)**;
o artigo dele se chama *"Cycling in the **dual** simplex algorithm"*, e este handbook **não
afirma** que a forma primal usada aqui apareça literalmente nele. Ver
[ADR 0008](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0008-atribuicao-da-instancia-que-cicla.md).

### A frase que é a tese deste capítulo, e ela é de 1955

No mesmo artigo, os autores acrescentam uma observação que vale mais do que qualquer parágrafo
que eu pudesse escrever:

> *"por outro lado, é interessante notar que, **embora a maioria dos problemas que surgem de
> fontes práticas (na experiência dos autores) tenha sido degenerada, nenhum jamais ciclou**."*

Leia devagar. Quem inventou o método está dizendo, em 1955, que **degenerescência é o normal** —
a maioria dos problemas reais tem — e que **ciclagem é o excepcional**, nunca observado por eles
na prática.

Meio século depois isso continua valendo. **Hall e McKinnon (2004)**, também lido aqui, registram
que exemplos como o de Beale foram **construídos** e "parecem ser muito raros na prática", e
identificam qual é o problema real: não é o ciclo, é o ***stalling*** (estagnação) — uma sequência
longa, **porém finita**, de iterações sem melhora.

### O que se fazia antes, e a virada

Antes de existir regra anticiclagem, fazia-se o que ainda se faz quando um método trava sem
explicação: **mexia-se nos dados**. Perturbar levemente os lados direitos desfaz os empates — e
é a ideia por trás do método de perturbação e do lexicográfico, este último apresentado no mesmo
artigo de 1955.

A virada veio em 1977, com **Bland**, e é de outra natureza: em vez de mexer no problema, mexeu-se
na **regra de escolha**. Trocar o critério de quem entra e de quem sai por um puramente
posicional — o menor índice — basta para garantir terminação.

### A ideia reaproveitável, que é o que fica

> **O que é do modelo sobrevive à troca do método. O que some quando você troca o método era do
> método.**

Este capítulo não apenas afirma isso: **mede**. Na mesma instância, com o modelo intacto, trocando
só a regra de pivoteamento, a ciclagem some. E no modelo degenerado, com as duas regras, os
empates continuam lá.

É um teste que serve fora da Pesquisa Operacional. Quando um sistema apresenta um comportamento
ruim, a pergunta útil raramente é "de quem é a culpa?" — é **"o que muda se eu trocar a peça?"**.
O que permanece é da especificação; o que desaparece era da implementação.

### Procedência

| Afirmação | Estado |
|---|---|
| Hoffman e Wolfe construíram os primeiros exemplos de ciclagem; a citação de 1955 | ✓ **fonte aberta e lida** (Dantzig, Orden & Wolfe, *Pacific J. Math.*, 1955) |
| "A maioria dos problemas práticos tem sido degenerada; nenhum jamais ciclou" | ✓ mesma fonte |
| Método lexicográfico apresentado nesse artigo de 1955 | ✓ mesma fonte |
| Exemplos como o de Beale são construídos e raros na prática; o problema comum é o *stalling* | ✓ **fonte aberta e lida** (Hall & McKinnon, 2004) |
| A instância que circula no ensino é atribuída a Beale (1955) | ✓ᵐ metadados; ⏳ a forma **primal** aparecer literalmente ali |
| Regra de Bland, 1977 | ✓ᵐ metadados; ⏳ enunciado exato e prova de terminação |
| Prioridade de Hoffman: 1951 ou 1953 | ⏳ divergência entre levantamentos, não resolvida |
| O teste "troque o método e veja o que sobra" | 📖 **leitura deste livro** |

## Veredito 1 — não existe plano

O capítulo 09 mostrou como o quadro denuncia: a variável **artificial** sobra na base com valor
positivo. Aqui interessa o que fazer.

**Inviável não é um defeito do algoritmo. É uma contradição entre promessas.** Alguém prometeu
mais do que o recurso sustenta, e o modelo é o primeiro lugar onde as duas promessas se encontram
na mesma página.

O procedimento é sempre o mesmo, e é de investigação, não de cálculo:

1. **Isole.** Remova uma restrição de cada vez e resolva de novo. A que, ao sair, torna o modelo
   viável é a que está em conflito — ou uma das que estão.
2. **Vá à origem da restrição.** Contrato? Norma? Regra que alguém digitou? Restrição sem dono é
   frequente e é onde o erro mora.
3. **Traga a incompatibilidade, não o erro.** *"O compromisso de 8 unidades exige 16 pentes e há
   12"* é uma frase que resolve reunião. *"O modelo deu inviável"* não é.

> **Cuidado com a tentação.** A saída mais rápida — relaxar a restrição que incomoda até o modelo
> fechar — produz um plano executável para um problema que não é o seu. Se a exigência era real,
> você acabou de esconder a contradição dentro de um número bonito.

## Veredito 2 — o lucro não tem teto

Detecção no capítulo 09: nenhuma razão positiva no teste da razão, então dá para andar para
sempre naquela direção.

**Na prática, `Unbounded` quase nunca é uma descoberta sobre o mundo. É uma restrição que ninguém
escreveu.** O capítulo 07 abriu com esse caso exato: sem limite de recurso, a montadora ganha
infinito.

Duas causas dominam, e as duas são de modelagem:

| Causa | Como se reconhece |
|---|---|
| **Falta uma restrição de capacidade** | O modelo não tem nenhum limite sobre a variável que está crescendo |
| **Falta a não-negatividade** | O modelo "desmonta" para liberar recurso — a rota de fuga do capítulo 08 |

O que se leva à reunião: **"o modelo diz que não há limite para produzir; isso é falso, então
falta um limite que ninguém escreveu — qual é?"**

## Veredito 3 — há mais de um plano ótimo

Aqui começa o que o capítulo 09 não ensinou.

Volte à montadora e mude um número: suponha que o Tipo 2 pague **R$ 200** em vez de R$ 150. O
quadro final fica assim:

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $b$ |
|---|---:|---:|---:|---:|---:|
| $f_1$ | 1/2 | 0 | 1 | −1/2 | 4 |
| $x_2$ | 1/2 | 1 | 0 | 1/2 | 6 |
| $z$ | **0** | 0 | 0 | 100 | 1200 |

O critério de parada está satisfeito: nenhum negativo na linha $z$. O plano é $(0, 6)$, com
R$ 1.200.

**Mas repare no zero sob $x_1$.** A variável $x_1$ está **fora** da base — vale zero — e seu custo
reduzido também é zero. Traduzindo: **fazer $x_1$ entrar não muda o lucro.** Existe outro vértice
com exatamente o mesmo valor.

> **A regra de leitura:** custo reduzido **zero** numa variável **não-básica** anuncia mais de um
> plano ótimo. Se a variável fosse básica, zero seria outra coisa — e é o Veredito 4.

Pivoteando nessa coluna chega-se a $(8, 2)$: $100(8) + 200(2) = 1.200$. O mesmo lucro. E como
qualquer combinação entre dois pontos ótimos também é ótima, **todo o segmento entre $(0,6)$ e
$(8,2)$ rende R$ 1.200**.

A causa é a geometria do capítulo 08: o objetivo ficou **paralelo** à restrição de memória, e o
último contato da reta de iso-lucro é um lado inteiro, não um ponto.

### Por que isto é boa notícia

O reflexo comum é tratar múltiplos ótimos como ambiguidade — *"então qual eu executo?"*. É o
contrário: **você ganhou graus de liberdade de graça.**

Todos os planos do segmento custam o mesmo à empresa. Então escolha pelo que o modelo **não**
captura, e que costuma importar muito:

- o que estressa menos uma equipe;
- o que usa o fornecedor mais confiável;
- o que é mais fácil de explicar;
- o que deixa mais folga para o imprevisto de quinta-feira.

**Chegar à reunião com um plano é obedecer. Chegar com uma família de planos equivalentes e uma
recomendação é decidir.**

## Veredito 4 — o vértice sobredeterminado

Agora o outro zero — o que está **dentro** da base.

Suponha que a montadora tenha assinado um contrato de fornecimento que limita o total montado a
**10 unidades no mês**. É uma restrição legítima, veio do jurídico, e ninguém reparou que as 10
CPUs já impunham exatamente o mesmo limite.

$$x_1 + x_2 \le 10 \quad \text{(contrato)} \qquad x_1 + x_2 \le 10 \quad \text{(CPUs)}$$

O modelo roda e devolve o mesmo ótimo de sempre — $(8, 2)$, R$ 1.100. Mas o quadro final mudou:

| base | $x_1$ | $x_2$ | $f_1$ | $f_2$ | $f_3$ | $b$ |
|---|---:|---:|---:|---:|---:|---:|
| $x_1$ | 1 | 0 | 2 | −1 | 0 | 8 |
| $x_2$ | 0 | 1 | −1 | 1 | 0 | 2 |
| $f_3$ | 0 | 0 | −1 | 0 | 1 | **0** |
| $z$ | 0 | 0 | 50 | 50 | 0 | 1100 |

A folga do contrato, $f_3$, está **na base valendo zero**. Isso é um **vértice degenerado**: mais
restrições passando pelo mesmo ponto do que o necessário para sustentá-lo — exatamente o que o
capítulo 08 mostrou no desenho, agora em álgebra.

O sintoma aparece antes, no caminho — e vale olhar com cuidado, porque é fácil ver empate onde
não há:

```
iteração 0 — razões: f1 = 10, f2 = 6, f3 = 10     mínimo = 6, único
iteração 1 — razões: f1 = 8,  x2 = 12, f3 = 8     mínimo = 8, EMPATADO
```

Na iteração 0 duas razões são iguais (10 e 10) e **isso não é o sintoma**: elas não estão no
mínimo, então não decidem quem sai e não produzem pivô degenerado. **O empate que importa é o
empate no mínimo**, e ele acontece uma vez, na iteração 1 — é ali que o método fica sem critério
para escolher entre $f_1$ e $f_3$, e é dali que sai a básica em zero.

### Vértice degenerado não é defeito

Vale dizer com todas as letras, porque a palavra assusta: **vértice degenerado é comum e
legítimo**. Não há erro de conta, e o plano é executável.

O que ele é: uma **bandeira amarela** com duas consequências práticas.

1. **Provavelmente há restrição redundante.** Duas restrições dizendo a mesma coisa é o caso mais
   frequente, e vale caçar: restrição redundante custa tempo de solver, polui a leitura e esconde
   qual limite de fato governa a operação.
2. **A leitura de preço-sombra fica ambígua.** O capítulo 09 mostrou que a linha $z$ do quadro
   final diz quanto vale uma unidade a mais de cada recurso. Num vértice degenerado esse número
   **depende de qual base o solver parou** — e o capítulo 13 vai tratar disso a sério.

### Como caçar a redundante

O procedimento é o mesmo do Veredito 1, invertido: **remova uma restrição de cada vez e resolva
de novo.** A que puder sair **sem mudar o ótimo** é candidata a redundante. Depois vá à origem
dela — e a conversa costuma ser mais útil do que o modelo: *"o contrato repete o que o estoque já
limita; ele existe por quê?"*

## Quando o empate vira giro

Este capítulo inteiro defende que o defeito costuma ser do modelo. Aqui está **a única página em
que ele é do algoritmo** — e ela é declarada como exceção, de propósito.

O empate no teste da razão tem uma consequência que ainda não foi dita: quando ele acontece, a
variável que entra pode entrar valendo **zero**. O método pivoteia, troca a base, refaz o quadro —
**e não sai do ponto**. O objetivo não melhora.

Se isso se repetir e uma base já visitada voltar, o método **cicla**: gira para sempre.

### Medido, não citado

Este handbook executou a instância clássica de ciclagem no seu próprio Simplex — o do capítulo 09,
com a regra de Dantzig. O resultado:

```
5_giro_dantzig  [dantzig]  limite_de_iteracoes  pivôs=41
                CICLO período 6 (base ['f1','f2','f3'] repetiu na iteração 6)
```

A base inicial volta na iteração 6, e volta de novo na 12, na 18, na 24. **E o ponto nunca sai de
$(0,0,0,0)$** — as quarenta e uma iterações acontecem todas no mesmo vértice.

Agora a **mesma instância**, com o modelo intacto, trocando **só a regra de pivoteamento** pela de
Bland — menor índice na entrada e, entre as de menor razão, a variável básica de menor índice:

```
5_giro_bland             [bland  ] otimo                pivôs=  6 ponto=['1/25', '0', '1', '0']
```

Seis pivôs, e o detector de ciclo **não encontra base repetida** — ao contrário do caso anterior.
**O HiGHS chega ao mesmo ponto**, $(0{,}04;\ 0;\ 1;\ 0)$ com valor $0{,}05$.

### O custo da garantia

Trocar de regra não é grátis, e este handbook mede em vez de afirmar:

| Instância | Pivôs com Dantzig | Pivôs com Bland | Mesmo veredito? | Mesmo valor? | **Mesmo plano?** |
|---|---:|---:|---|---|---|
| Montadora | 2 | 2 | sim | sim | sim |
| Vértice degenerado | 2 | 2 | sim | sim | sim |
| **Múltiplos ótimos** | 1 | 2 | sim | sim | **não** |
| Sem plano | 1 | 3 | sim | — | — |

Duas leituras, e a segunda surpreende.

**A primeira:** Bland custa mais pivôs em metade das instâncias e **nunca muda o valor ótimo**. É
o formato clássico de um seguro — você paga sempre, e o benefício aparece num caso que quase
nunca ocorre.

**A segunda:** na instância com **mais de um plano ótimo**, as duas regras entregam **planos
diferentes** — Dantzig para em $(0, 6)$ e Bland em $(8, 2)$, ambos rendendo R$ 1.200. O valor não
muda; **o plano muda**.

> Isto reforça o Veredito 3 de um jeito incômodo: quando existe mais de um plano ótimo, **qual
> deles você recebe é decidido pela regra de pivoteamento**, não por você — e por nenhum critério
> de negócio. Se a escolha entre os planos importa, e a seção anterior argumentou que importa,
> então ela **não pode ser deixada para o solver**: tem de ser feita explicitamente, depois de o
> quadro anunciar que há empate.

Por isso **os solvers de mercado não usam Bland o tempo todo**. Eles usam regras rápidas e
acionam proteção quando desconfiam. E vale saber, porque impede um final feliz falso: o
procedimento anticiclagem dos solvers reais, o **EXPAND**, **não tem garantia** de evitar
ciclagem — Hall e McKinnon mostram condições em que ele falha.

### O teste que fica

Volte à tabela do custo e ao experimento:

- Trocou a regra → **a ciclagem sumiu**. Era do método.
- Trocou a regra → **os empates continuaram**. São do modelo.

> **O que é do modelo sobrevive à troca do método. O que some quando você troca o método era do
> método.**

É o único procedimento deste capítulo que você vai usar fora da Pesquisa Operacional.

## O código

A [etapa 04 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-04-casos-especiais)
não implementa método novo: **instrumenta** o Simplex do capítulo 09 para que os vereditos possam
ser observados.

| Instrumento | A pergunta que ele responde |
|---|---|
| Detecção de ciclo por repetição de base | Isto é ciclo ou só lentidão? |
| Básica em zero no quadro final | O vértice é degenerado? |
| Custo reduzido zero fora da base | Existe mais de um plano ótimo? |

Os cinco vereditos batem com o HiGHS: `Optimal`, `Optimal`, `Unbounded`, `Infeasible` e —
no caso do giro — `Optimal`, no mesmo ponto que a regra de Bland encontra.

## Quando não serve

**1. Este capítulo diagnostica, não conserta.** Ele diz que há restrição redundante; não diz qual
remover — isso é decisão de quem conhece a operação, e o modelo não tem essa informação.

**2. A leitura de preço-sombra em vértice degenerado fica pendente.** O capítulo diz que o número
vira ambíguo e para aí. A faixa de validade e o que fazer com ela são o capítulo 13.

**3. O teste "troque o método" precisa de duas implementações.** Aqui isso é barato porque o
`po-zero` tem as duas regras. Com um solver comercial de caixa fechada, você raramente pode trocar
a regra — e o teste vira leitura de documentação.

**4. Ciclagem exata é fenômeno de aritmética exata.** Este handbook usa frações, então o ciclo é
limpo e reproduzível. Em ponto flutuante o erro de arredondamento normalmente quebra o ciclo — e
troca um problema honesto por um pior, o de decidir se dois números "iguais" são iguais.

**5. O problema prático não é o que este capítulo mais treina.** As fontes lidas são explícitas:
ciclagem é rara; **estagnação** — muitas iterações sem melhora, mas finitas — é comum. Tratá-la
exige a forma revisada e as escolhas de implementação do capítulo 11.

## Fundamentos e fontes

**O que está medido aqui.** Os cinco vereditos, o ciclo de período 6, os seis pivôs de Bland e a
tabela do custo da garantia saem do experimento e se regeneram rodando um script.

**O que foi lido na fonte.** Duas obras, abertas e lidas nesta rodada:

- ✓ **DANTZIG, G. B.; ORDEN, A.; WOLFE, P.** "The generalized simplex method for minimizing a
  linear form under linear inequality restraints". *Pacific Journal of Mathematics*, v. 5, n. 2,
  p. 183–195, 1955. — Sustenta a prioridade de Hoffman e Wolfe, a citação sobre degenerescência
  ser comum e ciclagem nunca observada, e o método lexicográfico.
- ✓ **HALL, J. A. J.; McKINNON, K. I. M.** "The simplest examples where the simplex method cycles
  and conditions where EXPAND fails to prevent cycling". *Mathematical Programming*, v. 100, 2004.
  — Sustenta a raridade dos exemplos, a distinção entre ciclagem e *stalling*, e o fato de o
  EXPAND não ter garantia.

**O que continua em dívida**, com o motivo: o enunciado exato da regra de Bland e a prova de
terminação; a forma primal da instância em Beale (1955); e a atribuição do *big-M* a Charnes
(1952), herdada do capítulo 09. Os três dependem de editoras que recusam acesso automatizado. Ver
a [bibliografia](../bibliografia.md) e o [Radar](../../radar/RADAR.md).

## Pratique

<div data-bateria="cap10"></div>

Cinco exercícios, e nenhum pede para você resolver um modelo. Todos pedem para **ler uma saída e
decidir o que fazer** — que é o trabalho real quando o solver não devolve um plano.

Em três deles a resposta certa contraria o reflexo: o veredito parece uma coisa e é outra.

## Assista

**[Pesquisa Operacional I — Aula 11: Algoritmo Simplex, casos especiais](https://www.youtube.com/watch?v=GNrCFpBLqfQ)** · [UNIVESP](https://www.youtube.com/@univesptv) · duração ⏳

**O que ele resolve:** este capítulo trata os casos especiais como **conduta** — o que fazer com
cada veredito. O vídeo faz o percurso complementar, mostrando os quadros de cada caso sendo
montados. Vale como segunda passada sobre a mecânica que aqui foi deslocada para o código.

> ⏳ **Ficha parcialmente conferida.** Título, endereço e autoria foram verificados na fonte; a
> **duração não** — a página do vídeo não devolveu o campo em nenhuma das tentativas. É o único
> vídeo do handbook nesse estado; ver a [Videoteca](../videoteca.md).

## Síntese — o que levar

- **Cinco situações em que o Simplex não entrega um plano**, e cada uma tem conduta própria. O
  capítulo 09 ensinou a detectar duas; aqui se aprende a detectar as outras três e o que fazer
  com todas.
- **`Infeasible` é contradição entre promessas**, não erro de conta. Isole a restrição em conflito
  e leve a incompatibilidade, não o erro.
- **`Unbounded` quase nunca é boa notícia:** é restrição que ninguém escreveu.
- **Custo reduzido zero em variável fora da base = mais de um plano ótimo** — e isso é **vantagem**:
  você escolhe pelo que o modelo não captura.
- **Variável na base valendo zero = vértice degenerado.** Comum, legítimo, e bandeira amarela:
  provavelmente há restrição redundante, e o preço-sombra fica ambíguo.
- **Empate no teste da razão é o sintoma** da degenerescência, e aparece antes do quadro final.
- **Ciclagem existe e foi medida aqui** — período 6, sem sair do ponto. É **rara**, e é a única
  página deste livro em que o defeito é do algoritmo.
- **A regra de Bland resolve, e custa.** Nunca muda a resposta; gasta mais pivôs. É um seguro.
- **O teste que fica:** *o que é do modelo sobrevive à troca do método; o que some quando você
  troca o método era do método.*

## Verificação

1. Um analista mostra um plano ótimo e diz que ele é "a resposta do modelo". Você olha o quadro
   final e vê um zero na linha $z$ sob uma variável que não está na base. O que você pergunta a
   ele, e o que isso muda na reunião? *(O2)*
2. O modelo devolveu `Unbounded` e o gerente comercial comemorou. Em duas frases, o que você diz
   — e qual é a primeira coisa que você vai procurar? *(O1)*
3. Um quadro final tem uma variável de folga **na base valendo zero**. Que hipótese você levanta
   sobre o modelo, e qual é o teste mais barato para confirmá-la? *(O3)*
4. Um colega troca a regra de pivoteamento do solver e relata que "o problema sumiu". Que
   pergunta você faz antes de aceitar que o problema estava resolvido? *(O4)*

### Leitura executiva

Nem toda execução do Simplex termina com um plano, e os vereditos que não são plano exigem
conduta, não cálculo. **Inviável** é uma contradição entre promessas — alguém prometeu mais do que
o recurso sustenta —, e se investiga removendo uma restrição por vez até descobrir qual está em
conflito. **Ilimitado** quase nunca é uma descoberta sobre o mundo: é uma restrição que ninguém
escreveu. **Custo reduzido zero numa variável fora da base** anuncia que existe mais de um plano
ótimo, o que é vantagem e não ambiguidade: todos custam o mesmo à empresa, então a escolha passa a
ser feita pelo que o modelo não captura — risco, fornecedor, facilidade de explicar. **Uma
variável na base valendo zero** é um vértice degenerado: comum, legítimo, e bandeira amarela,
porque em geral indica restrição redundante e torna a leitura de preço-sombra ambígua. O sintoma
aparece antes, como empate no teste da razão. Há ainda o caso em que o método pivoteia sem sair do
lugar e volta a uma base já visitada: **ciclagem**. Este handbook a mediu no próprio código —
período 6, sempre no mesmo ponto —, e mostrou que trocar a regra de pivoteamento pela de Bland faz
o método terminar em seis pivôs, com o modelo intacto. A troca tem preço: Bland nunca muda a
resposta e gasta mais pivôs, o que é o formato de um seguro. Daí sai o único procedimento deste
capítulo que serve fora da Pesquisa Operacional: **o que é do modelo sobrevive à troca do método; o
que some quando você troca o método era do método.**
