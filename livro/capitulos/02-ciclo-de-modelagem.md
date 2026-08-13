# 02 — O ciclo de modelagem

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Situar** uma tarefa nas cinco etapas do ciclo — definir, formular, resolver, validar,
implantar — e dizer o que cada uma entrega.

**O2.** **Diagnosticar** um projeto que **pulou a validação**, e nomear o sintoma que denuncia.

**O3.** **Decidir quando não modelar**, com critério, e dizer o que fazer no lugar.

## O problema

Todo projeto de Pesquisa Operacional (PO) que fracassa fracassa da mesma forma, e não é a que se
imagina. O modelo quase nunca está errado.

| Onde as pessoas acham que o projeto morre | Onde ele morre de verdade |
|---|---|
| No algoritmo — "escolhemos o método errado" | Na **definição** — resolveu-se a pergunta errada |
| Na matemática — "a formulação estava furada" | Na **validação** — ninguém confrontou o modelo com a realidade |
| No solver — "não convergiu" | Na **implantação** — a resposta certa não virou decisão |

Os capítulos 07 a 15 são inteiros sobre a etapa do meio, e essa é a que este handbook consegue
medir. As duas pontas — o que se decide antes de formular e o que acontece depois de resolver —
são onde o dinheiro se perde, e são o assunto desta página.

O erro caro deste capítulo:

> Alguém entrega um modelo tecnicamente impecável para uma pergunta que ninguém fez. **Não há
> defeito em lugar nenhum.** O modelo roda, o número está certo, e a empresa não muda nada — o
> que, do ponto de vista de quem pagou, é indistinguível de não ter feito.

## De onde isto veio

### O aperto: o projeto que funcionava e não era usado

O ciclo em etapas não nasce de teoria. Ele nasce da observação repetida de que **modelos corretos
não são adotados** — e de que a causa raramente está no modelo.

Nomear as etapas serve a uma coisa só, e ela é organizacional antes de ser técnica: **dar nome ao
ponto em que o projeto está**, para que a conversa deixe de ser sobre a qualidade do trabalho e
passe a ser sobre o que falta.

### O que se fazia antes, e a virada

Fazia-se o ciclo inteiro **implicitamente**, dentro da cabeça de quem modelava — o que funciona
enquanto a mesma pessoa define, formula, resolve, valida e implanta. Some qualquer transferência
entre pessoas e o implícito vira lacuna: quem formula supõe que quem definiu já validou a
pergunta, e quem implanta supõe que quem resolveu já validou a resposta.

A virada é **tornar as etapas nomeáveis**, com entregável próprio. Não porque o processo seja
melhor em cascata — não é —, mas porque um projeto que não sabe dizer em que etapa está não sabe
dizer o que lhe falta.

### A ideia reaproveitável

> **Errar de etapa é mais caro do que errar dentro da etapa.** Um erro de formulação se conserta
> refazendo a formulação; um erro de definição se conserta refazendo o projeto.

Vale em qualquer trabalho com fases. O custo de um erro cresce com a distância entre onde ele
nasce e onde é descoberto — e a etapa de definição é a mais barata de corrigir e a mais cara de
ignorar.

### Procedência

| Afirmação | Estado |
|---|---|
| O recorte em cinco etapas adotado por este handbook | 📖 **leitura editorial**, a partir da organização dos livros-texto citados na [bibliografia](../bibliografia.md) |
| A quem se atribui a formulação canônica do ciclo, e quando | ❌ **procurada e não localizada** por identificador nesta rodada |
| Que projetos de PO fracassam mais por definição e adoção do que por método | ⏳ **afirmação corrente do campo**; este handbook **não a mediu** e não cita levantamento com amostra declarada |

> A última linha merece atenção, porque é uma tentação. Existe literatura sobre taxa de adoção de
> modelos, e ela seria fácil de citar de memória. **Este capítulo não cita nenhuma**, porque não
> abriu nenhuma. O que ele afirma sobre onde os projetos morrem é **estrutura de argumento**, não
> estatística — e está escrito assim de propósito.

## As cinco etapas, e o que cada uma entrega

Uma etapa não termina quando o tempo acaba. Termina quando **o entregável dela existe**.

| Etapa | A pergunta | O entregável | O sintoma de ter sido pulada |
|---|---|---|---|
| **1. Definir** | Que decisão vai mudar? | Uma frase com a **alavanca**, a medida e quem executa | Ninguém sabe dizer o que muda na segunda-feira |
| **2. Formular** | Que modelo representa isso? | Variáveis, objetivo e restrições declarados | Discussões sobre "o que o modelo quis dizer" |
| **3. Resolver** | Qual é a resposta? | Solução + **o que ela autoriza** | Um número sem faixa de validade |
| **4. Validar** | O modelo se sustenta fora do papel? | Confronto com dado real e com quem conhece a operação | O modelo nunca errou — porque nunca foi testado |
| **5. Implantar** | Isso virou decisão? | Alguém decidiu diferente por causa do modelo | O relatório foi entregue e arquivado |

**O ciclo não é cascata.** Validar quase sempre devolve o projeto à definição, e é isso que ele
tem de bom: descobrir na etapa 4 que a pergunta era outra é caro, e descobrir depois de implantar
é muito pior.

### Onde a Parte II deste livro se encaixa

Nove capítulos, todos dentro da etapa 3 — e vale ver o que eles mediram sobre as vizinhas:

| O que a Parte II mediu | De que etapa é o defeito |
|---|---|
| Preço-sombra citado fora da faixa: **R$ 350** de prejuízo, sem conta errada ([cap. 12](12-dualidade.md)) | **3** — resolver sem dizer o que a resposta autoriza |
| Padrão de modelagem errado: **R$ 403,33 contra R$ 365**, e o modelo não responde à pergunta ([cap. 15](15-modelagem-aplicada.md)) | **1 e 2** — a variável de decisão errada apaga a pergunta |
| `Optimal` num modelo não convexo: **22 ou 30**, conforme onde a busca começou ([cap. 38](38-convexidade.md)) | **4** — validar é o que pega isto |

Repare que **o número certo e a decisão errada convivem em todas as três**. É por isso que a
etapa 4 não é burocracia.

## A etapa 4, que é a mais pulada

Validar não é conferir se a conta está certa — isso é a etapa 3. **Validar é confrontar o modelo
com o mundo**, e há três formas, em ordem crescente de custo e de valor:

**1. Contra o histórico.** Rode o modelo com os dados do mês passado e compare com o que de fato
foi feito. Se ele recomendar algo muito melhor, pergunte por quê antes de comemorar: em geral há
uma restrição real que ninguém escreveu — e o [capítulo 10](10-casos-especiais.md) mostrou que
`Unbounded` é o caso extremo disso.

**2. Contra quem opera.** Mostre a resposta a quem executa e ouça a objeção. *"Isso não dá para
fazer porque…"* é uma restrição faltando, dita em português.

**3. Contra o próprio modelo.** Mexa nos dados e veja se a resposta muda de forma que faça sentido.
É a análise de sensibilidade do [capítulo 13](13-sensibilidade.md) usada como instrumento de
validação, e não só de leitura.

> **O sintoma de que a validação foi pulada é sempre o mesmo:** o modelo **nunca errou**. Não
> porque seja bom — porque ninguém deu a ele a chance de errar.

## Quando não serve — quando não modelar

O ciclo é um método, e o Princípio II vale para ele como vale para o Simplex: **também precisa
dizer quando não serve**. Esta seção existe porque a resposta honesta às vezes é "não vale a
pena", e um livro que nunca diz isso está vendendo.

**1. Quando a decisão é única e barata.** Modelo se paga na repetição. Decisão que acontece uma
vez e custa pouco não justifica o ciclo — decida e siga.

**2. Quando o dado não existe.** Modelo bom com dado inventado é pior do que nenhum, porque tem
aparência de rigor. Se a etapa 1 revelar que o dado precisa ser criado, **o projeto é de dado**,
não de otimização, e reconhecer isso cedo é o serviço mais valioso que se pode prestar.

**3. Quando a restrição é política.** Se a resposta já está decidida e o modelo serve para
justificá-la, o ciclo não se aplica — e participar disso sabendo é escolha profissional, não
técnica.

**4. Quando ninguém vai implantar.** Se na etapa 1 não há resposta para *"quem vai decidir
diferente por causa disto?"*, as etapas 2 e 3 vão produzir um relatório. Bonito, correto, e
arquivado.

**5. Quando uma regra simples resolve.** Muita decisão operacional é bem resolvida por uma regra
de bolso que a equipe entende e executa. Um modelo que ganha 2% e ninguém confia perde do lápis
que ganha 0% e é usado.

## Fundamentos e fontes

**O que está medido aqui.** Nenhum número novo. Os três da tabela de encaixe vêm das etapas 05 a
08 do `po-zero` e estão conferidos nos capítulos que os produziram, cada um com teste que compara
o texto publicado à medição.

**O que continua em dívida:** a origem do ciclo em cinco etapas, `❌` procurada e não localizada; e
a afirmação corrente de que projetos de PO fracassam mais por definição e adoção do que por
método, `⏳` — **não medida aqui e não citada de memória**.

> 🟡 **Este capítulo está em v0.** Não passou por revisão independente em contexto fresco.

## Pratique

<div data-bateria="cap02"></div>

Três exercícios. O primeiro situa tarefas reais no ciclo; o segundo diagnostica um projeto que
pulou a validação; o terceiro pede a decisão mais difícil que este capítulo ensina — **não
modelar**.

## Assista

**[Modelagem matemática 1 em Pesquisa Operacional](https://www.youtube.com/watch?v=H2R-b-RDxf4)** ·
[Acerte as Contas!](https://www.youtube.com/@acerteascontas) · 15min28s

**O que ele resolve:** este capítulo trata o ciclo como **mapa de projeto** — em que etapa você
está, o que falta entregar, quando parar. O vídeo faz o percurso complementar: pega uma situação e
mostra a passagem da etapa 1 para a 2 acontecendo, que é a transição mais difícil de descrever por
escrito e a mais fácil de ver alguém fazendo.

## Síntese — o que levar

- **Cinco etapas, cada uma com entregável próprio:** definir, formular, resolver, validar,
  implantar. Etapa termina quando o entregável existe, não quando o prazo acaba.
- **O projeto raramente morre no algoritmo.** Morre na definição, na validação ou na implantação —
  e nas três o modelo pode estar impecável.
- **Errar de etapa é mais caro do que errar dentro da etapa.**
- **O ciclo não é cascata:** validar devolve o projeto à definição, e é para isso que ele serve.
- **Validar é confrontar com o mundo**, em três níveis: histórico, quem opera, e o próprio modelo.
- **O sintoma de validação pulada:** o modelo nunca errou — porque ninguém lhe deu a chance.
- **Não modelar é resposta legítima** em cinco casos, e o mais importante é: se ninguém vai
  implantar, as outras etapas produzem um relatório arquivado.
- **Fora da Pesquisa Operacional:** o custo de um erro cresce com a distância entre onde ele nasce
  e onde é descoberto.

## Verificação

1. Uma equipe está há três semanas ajustando o solver para um modelo que roda em 40 minutos.
   Em que etapa ela está, e que pergunta você faz antes de ajudar com o solver? *(O1)*
2. Um modelo foi entregue com a observação de que "nunca apresentou inconsistência". Por que essa
   frase é motivo de preocupação, e o que você pede para verificar? *(O2)*
3. Um gerente pede um modelo para decidir o layout de uma loja nova — decisão única, dado
   inexistente, e ele mesmo vai decidir de qualquer jeito. O que você responde, e o que oferece no
   lugar? *(O3)*

### Leitura executiva

Projetos de Pesquisa Operacional raramente fracassam no algoritmo: fracassam na **definição** —
quando se resolve a pergunta errada —, na **validação** — quando ninguém confronta o modelo com a
realidade — ou na **implantação**, quando a resposta certa não vira decisão. Em todos esses casos o
modelo pode estar tecnicamente impecável, e é exatamente isso que torna o defeito difícil de ver.
O ciclo em cinco etapas — definir, formular, resolver, validar, implantar — serve para dar nome ao
ponto em que o projeto está, e cada etapa termina quando **o entregável dela existe**, não quando o
prazo acaba: a definição entrega uma frase com a alavanca, a medida e quem executa; a resolução
entrega a solução **e o que ela autoriza**; a validação entrega o confronto com dado real e com
quem conhece a operação; a implantação entrega alguém decidindo diferente por causa do modelo. O
ciclo não é cascata — validar quase sempre devolve o projeto à definição, e é essa devolução que o
torna útil, porque descobrir na etapa 4 que a pergunta era outra custa muito menos do que descobrir
depois de implantar. A etapa mais pulada é a validação, e o seu sintoma é sempre o mesmo: **o
modelo nunca errou**, não por ser bom, mas porque ninguém lhe deu a chance. Validar tem três
níveis — contra o histórico, contra quem opera, e contra o próprio modelo por análise de
sensibilidade. Por fim, **não modelar é resposta legítima**: quando a decisão é única e barata,
quando o dado não existe (e então o projeto é de dado, não de otimização), quando a restrição é
política, quando uma regra simples resolve, e sobretudo quando ninguém vai implantar — porque nesse
caso as outras etapas produzem um relatório correto, bonito e arquivado.
