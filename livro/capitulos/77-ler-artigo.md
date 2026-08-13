# 77 — Como ler um artigo científico de PO

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-13 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

**O1.** **Aplicar** um protocolo de três passadas a um artigo de Pesquisa Operacional (PO),
decidindo em cada passada se vale seguir para a próxima.

**O2.** **Diagnosticar** uma afirmação de desempenho que o artigo **não sustenta** — instância não
declarada, comparação sem controle, tempo sem máquina.

**O3.** **Decidir** se um resultado publicado se aplica ao **seu** problema, e dizer o que
precisaria ser verdade para que se aplicasse.

## O problema

Você precisa escolher um método para um problema de roteamento na sua empresa. Uma busca devolve
um artigo cujo resumo diz:

> *"O método proposto supera o estado da arte, sendo em média **40× mais rápido** e obtendo
> soluções de melhor qualidade."*

Quarenta vezes. Você leva para a reunião de terça, o time compra a ideia, alguém aloca duas
sprints, e três meses depois o resultado na sua instância é **pior** do que o método que já
estava rodando.

Nada de desonesto aconteceu no artigo. O que aconteceu é que a frase do resumo respondia a uma
pergunta diferente da sua, e **quase todas as informações necessárias para perceber isso estavam
no texto** — na seção de experimentos computacionais, que quase ninguém lê.

O erro caro deste capítulo é ler artigo **como se lê livro**: da primeira à última linha,
confiando, uma vez só. Artigo não se lê assim. Artigo se **interroga**, e existe uma ordem de
perguntas que economiza a maior parte do trabalho.

Este é também o capítulo que dá ao resto do handbook o direito de **citar em vez de explicar**.
Cada vez que um capítulo diz "as fontes lidas mostram que X", você deveria poder abrir a fonte e
julgar por conta própria. Aqui está como.

## De onde isto veio

### O aperto: a leitura não escala, e a produção não parou de crescer

O número de artigos publicados por ano cresceu muito mais rápido do que o número de horas que um
pesquisador tem para lê-los. A pós-graduação sempre exigiu "leia a literatura", e passou a exigir
isso sobre uma literatura que **não cabe** em nenhuma agenda. Ler tudo com a mesma profundidade
deixou de ser rigor e passou a ser impossibilidade aritmética.

### O que se fazia antes

Fazia-se o que ainda se faz por reflexo: lia-se do começo ao fim, com a mesma atenção em cada
parágrafo, e desistia-se no meio quando a energia acabava — geralmente **depois** de ter gasto o
esforço e **antes** de ter obtido o julgamento. O custo se pagava adiantado e o benefício vinha
por último, o que é exatamente a ordem errada.

### A virada: leituras de propósitos diferentes, em ordem crescente de custo

A virada é organizar a leitura em **passadas**, cada uma com um objetivo próprio e um critério
explícito de "seguir ou parar". A primeira passada custa minutos e responde *"isto é para mim?"*.
Só quem passa nela ganha a segunda. Só quem passa na segunda ganha a terceira, que é cara.

O ponto não é ler mais rápido. É **desistir cedo dos artigos errados** e chegar inteiro nos
certos.

### A origem, e o que este handbook não afirma

O protocolo de três passadas é atribuído a **S. Keshav**, em artigo de 2007 no *ACM SIGCOMM
Computer Communication Review* — e a atribuição é `✓ᵐ`: **o identificador foi conferido no
registro, e o texto não foi aberto**. Nenhuma via de acesso aberto devolveu o conteúdo nesta
rodada.

> **Consequência, e ela é o desenho deste capítulo:** o protocolo abaixo é **autoral**, escrito
> para artigos de Pesquisa Operacional. Ele credita a origem da ideia de organizar a leitura em
> passadas e **não reproduz** o texto de ninguém. Onde ele fala de conferir instância, *baseline*,
> tempo limite e versão de solver, isso é **deste handbook** — um artigo de redes de 2007 não
> teria por que tratar disso.

### A ideia reaproveitável

> **Ordene o trabalho por custo crescente e ponha um critério de desistência entre cada etapa.**

Serve muito além de artigo: triagem de candidatos, avaliação de fornecedor, revisão de código,
leitura de proposta comercial. O erro comum, em todos esses casos, é o mesmo — gastar o esforço
caro **antes** de ter aplicado o filtro barato.

### Procedência

| Afirmação | Estado |
|---|---|
| Keshav publica "How to read a paper" em 2007, no *ACM SIGCOMM CCR* | ✓ᵐ metadados e existência conferidos — [bibliografia](../bibliografia.md) |
| O conteúdo desse artigo | ❌ **não lido** — sem via de acesso aberto nesta rodada |
| O protocolo em três passadas deste capítulo | 📖 **autoral**, adaptado a PO; a ideia de passadas é creditada acima |

## O protocolo — três passadas

### Passada 1 — cinco minutos: *isto é para mim?*

Leia **só** título, resumo, introdução, títulos de seção e conclusão. Ignore o resto,
inclusive as fórmulas.

Ao fim, você tem de conseguir responder cinco perguntas. Se não conseguir, o problema pode ser
seu — ou pode ser do artigo, e isso já é informação.

| Pergunta | O que você faz com a resposta |
|---|---|
| Que **classe de problema** é atacada? | Se não é a sua classe, pare aqui |
| Que **tipo de método**? (exato, heurístico, híbrido, aprendido) | Define se a promessa é de ótimo ou de qualidade |
| Contra **o quê** ele se compara? | Sem *baseline* nomeado, a comparação não existe |
| Em **que instâncias**? | Se forem geradas pelos autores e não públicas, o resultado é local |
| O que os autores dizem que é **novo**? | Distingue contribuição de aplicação |

**Critério de parada:** se a classe de problema não é a sua e a ideia não é transferível, **pare**.
Você gastou cinco minutos e economizou uma tarde.

### Passada 2 — uma hora: *o que exatamente foi feito e medido?*

Agora sim o corpo do texto, ainda **pulando demonstrações**. O alvo desta passada é a seção de
**experimentos computacionais**, e a pergunta é uma só: *o que sustenta a frase do resumo?*

Este é o momento de aplicar a checklist da seção seguinte. Ao fim, você deveria conseguir
descrever o experimento para outra pessoa **sem** consultar o artigo. Se não consegue, ou o
experimento está mal descrito — o que é um achado — ou a passada não terminou.

**Critério de parada:** se o experimento não sustenta a afirmação que te trouxe até aqui, **pare
e registre** o que faltou. Você acabou de aprender a coisa mais útil que esse artigo tinha para te
dar.

### Passada 3 — o dia inteiro: *eu conseguiria refazer?*

Só para o artigo que você vai usar, citar ou construir em cima. Aqui você reconstrói o raciocínio
como se fosse escrevê-lo: refaz as passagens, confere as hipóteses de cada teorema, procura o
caso em que o método falharia.

O sinal de que a passada 3 terminou não é ter entendido. É conseguir dizer **o que o artigo não
faz** — e essa frase é a que vai para o seu relatório.

## O que é específico de Pesquisa Operacional

A checklist abaixo é a razão de este capítulo existir separado de um guia genérico de leitura. Em
PO, quase toda afirmação relevante é uma **comparação computacional**, e comparação computacional
tem partes obrigatórias. Faltando qualquer uma, o número perde sentido — não porque alguém mentiu,
mas porque não é reproduzível.

| O que conferir | Por que, e o que a ausência significa |
|---|---|
| **Instâncias** | Nome do conjunto, tamanho, origem. Instância gerada pelos próprios autores e não publicada não permite que ninguém confirme nada |
| ***Baseline*** | Contra qual método, em **qual versão**. "Comparado com o Simplex" não é *baseline*; "CPLEX 22.1, configuração padrão" é |
| **Critério de parada** | Tempo limite, *gap* alvo, número de iterações. Sem isso, "mais rápido" não tem unidade |
| **Máquina** | Processador, memória, número de *threads*. Um método em 32 núcleos contra outro em 1 não é comparação de métodos |
| **Semente e número de execuções** | Método com aleatoriedade rodado **uma vez** não tem resultado, tem anedota |
| ***Gap*** **e qualidade** | "Melhor qualidade" precisa de referência: ótimo conhecido, melhor limitante, melhor solução publicada |
| **Versão do solver** | Solver comercial muda de desempenho entre versões. Sem versão, o número não se reproduz |
| **Disponibilidade** | Código e dados abertos? Sem isso, você depende da descrição textual para refazer |

> **A pergunta que resume a tabela inteira:** *se eu quisesse refazer este experimento amanhã, o
> que eu ainda precisaria perguntar aos autores?* Cada item dessa lista é uma linha que faltou.

### Voltando aos 40×

Aplique a checklist à frase do começo. "**40× mais rápido**" pode significar coisas
incompatíveis entre si:

- 40× em **uma** instância, ou na média de um conjunto — e a média de razões esconde o caso em
  que perdeu;
- 40× contra um *baseline* de 2009, escolhido porque tem código aberto disponível;
- 40× com o *baseline* rodando em configuração padrão e o método proposto **ajustado** para o
  conjunto de teste;
- 40× em tempo de execução, sendo que o método precisa de uma fase de treino ou de calibração que
  não entrou na conta.

Nenhuma dessas quatro possibilidades exige má-fé de ninguém. Todas mudam completamente o que você
deveria fazer na terça-feira.

## Quando não serve

**1. Isto não é revisão sistemática.** O protocolo julga **um** artigo. Mapear um campo inteiro é
outro trabalho, com outro método — critérios de inclusão, busca declarada, mais de um leitor.

**2. A passada 1 descarta com prejuízo.** Um artigo mal escrito com uma ideia excelente falha na
primeira passada, e você nunca saberá. É o custo aceito do filtro: ele erra para o lado de
descartar. Contrapeso barato: quando alguém em quem você confia recomenda um artigo, ele entra
direto na passada 2.

**3. Nada aqui julga a *corretude* de uma demonstração.** A passada 3 confere hipóteses e
raciocínio, não substitui revisão por pares em matemática. Se o resultado é um teorema e a decisão
depende dele, você precisa de alguém da área.

**4. Artigo não é a única fonte, e às vezes não é a melhor.** Para uma decisão de ferramenta, a
documentação do solver e um teste na sua própria instância valem mais do que qualquer comparação
publicada — porque medem no seu dado, que é a única instância que decide.

**5. Isto é um protocolo, não uma garantia.** Ele reduz o custo de errar e não elimina o erro. O
artigo pode ter tudo declarado e ainda assim não valer para o seu caso.

## Fundamentos e fontes

**O que está medido aqui.** Nada — e isso é declarado de propósito. Este capítulo não publica
número nenhum, porque não tem número a publicar. Ele é protocolo.

**O que foi conferido no registro, e não lido.** ✓ᵐ **KESHAV, S.** "How to read a paper". *ACM
SIGCOMM Computer Communication Review*, 2007. Identificador e existência conferidos; **conteúdo
não aberto**.

**O que continua em dívida:** o texto do artigo de Keshav. Sem ele, este capítulo credita a
origem da ideia de leitura em passadas e **não** atribui a ele nenhum detalhe do protocolo acima.
A dívida fecha quando alguém com acesso institucional abrir o artigo e conferir o que é dele e o
que é adaptação — e o resultado pode muito bem ser encolher esta seção.

**Onde o handbook aplica isto em si mesmo.** O [Radar científico](../../radar/RADAR.md) é este
protocolo virado processo: cada artigo entra datado, com veredito e com **o que ele muda** no
livro. E a [bibliografia](../bibliografia.md) publica, para cada fonte, se ela foi lida (`✓`), se
só os metadados foram conferidos (`✓ᵐ`) ou se é atribuição corrente não confirmada (`⏳`).

> 🟡 **Este capítulo está em v0.** O esqueleto está completo, mas ele **não passou por revisão
> independente em contexto fresco**, e a fonte que dá origem à sua ideia central não foi lida. O
> selo no alto da página diz isso.

### Cláusula de expiração

Este capítulo está na **camada de fronteira**, onde toda afirmação declara quando deixa de valer
sem reverificação.

| Parte | Expira? |
|---|---|
| As três passadas e o critério de desistência | **Não expira** por conta própria. Revisar se a dívida do artigo de Keshav for quitada e o crédito precisar mudar |
| A checklist de comparação computacional | **Reverificar até 2028-08.** As normas de reprodutibilidade das conferências e periódicos de otimização mudam, e a lista precisa acompanhar |
| A afirmação de que solver comercial muda desempenho entre versões | **Reverificar até 2028-08**, com referência a um *benchmark* público |

## Pratique

<div data-bateria="cap77"></div>

Três exercícios. O primeiro é sobre **um artigo que você escolhe** — não há gabarito possível, e é
de propósito: o protocolo só vira competência quando aplicado a texto de verdade. O segundo dá uma
afirmação e pede o diagnóstico. O terceiro põe a decisão nas suas mãos.

## Assista

**[Como ler um artigo científico? (Módulo 7/20)](https://www.youtube.com/watch?v=eadVmuwEuAI)** ·
[Instituto de Computação — UFF](https://www.youtube.com/@InstitutodeComputa%C3%A7%C3%A3o-UFF) ·
1h09min06s

**O que ele resolve:** este capítulo entrega o protocolo em forma de checklist, que é o formato
certo para consultar e o formato errado para aprender a **sentir** o ritmo de uma leitura. O vídeo
é um módulo de curso de metodologia de uma universidade pública, em computação — área vizinha à
Pesquisa Operacional e com a mesma cultura de artigo com experimento computacional.

> **Aviso de duração, porque a política manda o leitor decidir com informação:** é **mais longo do
> que este capítulo**. Não é para assistir agora, de uma vez. Vale como acompanhamento na primeira
> vez que você aplicar a passada 2 num artigo de verdade.

## Síntese — o que levar

- **Artigo não se lê como livro.** Três passadas, cada uma com objetivo próprio e critério
  explícito de desistir.
- **Cinco minutos decidem a maior parte.** A passada 1 responde "isto é para mim?" e descarta
  barato.
- **A passada 2 mira o experimento**, não a teoria. É lá que a frase do resumo é sustentada — ou
  não.
- **Em PO, toda afirmação de desempenho é uma comparação**, e comparação sem instância,
  *baseline*, critério de parada, máquina, semente e versão de solver **não é resultado, é
  anedota**.
- **"40× mais rápido" não quer dizer nada sozinho** — e as quatro leituras possíveis levam a
  quatro decisões diferentes.
- **A pergunta que resume tudo:** *o que eu ainda precisaria perguntar aos autores para refazer
  isto amanhã?*
- **Fora da leitura de artigo:** ordene o trabalho por custo crescente e ponha um critério de
  desistência entre as etapas.

## Verificação

1. Você tem 20 minutos e quatro artigos. Descreva o que faz nesses 20 minutos e com que critério
   decide o que sobra para amanhã. *(O1)*
2. Um artigo afirma "reduzimos o tempo de solução em 60%" e a seção de experimentos informa o
   conjunto de instâncias e o tempo médio, mas não a máquina nem a versão do solver comparado. Que
   afirmação mais forte esse artigo autoriza, e qual você recusaria levar para uma reunião? *(O2)*
3. Um método publicado ganha do estado da arte em instâncias com até 200 clientes. O seu problema
   tem 3.000. O que precisaria ser verdade para o resultado se aplicar a você, e como você
   verificaria isso **antes** de investir? *(O3)*

### Leitura executiva

Ler artigo científico como se lê livro — do começo ao fim, com atenção constante e uma vez só —
gasta o esforço caro antes de aplicar o filtro barato, e é assim que se leva para uma reunião uma
frase de resumo que o próprio artigo não sustenta. A alternativa é ler em **três passadas de custo
crescente, com critério explícito de desistência entre elas**: cinco minutos com título, resumo,
introdução, títulos de seção e conclusão, respondendo apenas "isto é para mim?"; cerca de uma hora
no corpo do texto, pulando demonstrações e mirando a seção de experimentos computacionais; e um
dia inteiro só para o artigo que você vai usar, citar ou construir em cima, no qual o objetivo
final é conseguir dizer **o que o artigo não faz**. O que torna esse protocolo específico de
Pesquisa Operacional é a checklist da segunda passada: aqui quase toda afirmação relevante é uma
comparação computacional, e comparação computacional exige instâncias nomeadas e públicas,
*baseline* com versão declarada, critério de parada, máquina, semente e número de execuções, forma
de medir qualidade e versão do solver. A ausência de qualquer um desses itens não indica má-fé —
indica que o número **não se reproduz**, e um número que não se reproduz não decide nada. Daí a
pergunta que substitui a checklist inteira quando não há tempo: *se eu quisesse refazer este
experimento amanhã, o que eu ainda precisaria perguntar aos autores?* A ideia exportável, válida
muito além de artigo, é ordenar o trabalho por custo crescente e pôr um critério de desistência
entre as etapas — o erro comum, em triagem de candidato, avaliação de fornecedor ou revisão de
código, é sempre o mesmo: gastar o caro antes de aplicar o barato.
