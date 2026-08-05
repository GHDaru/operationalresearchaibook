# 02 — O ótimo local que destrói o todo

> **Conteúdo revisado em 2026-08** · edição inaugural · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

Ao final deste capítulo, você deve conseguir:

1. **Explicar** por que a soma dos ótimos das partes não é o ótimo do todo num sistema interdependente;
2. **Distinguir** estar ocupado de estar produzindo, e eficiência local de ganho do sistema;
3. **Prever** o comportamento que um indicador vai induzir em quem é medido por ele;
4. **Identificar**, num caso, qual indicador local está produzindo o prejuízo global.

## O problema

Um time de suporte passou a ser medido por chamados fechados por técnico por dia. Em dois meses, o indicador subiu 40%.

No mesmo período, a satisfação do cliente caiu e o número de chamados reabertos dobrou.

Ninguém trapaceou. Cada técnico fez a coisa racional: pegar primeiro os chamados fáceis, encerrar rápido o que dá para encerrar, e deixar envelhecer os difíceis — que são exatamente os que fazem o cliente ligar de novo, irritado, uma semana depois.

O indicador subiu porque as pessoas fizeram o que o indicador pediu. O resultado piorou pelo mesmo motivo.

Este capítulo é sobre por que isso é a regra, e não a exceção.

## O conceito

### Duas aritméticas diferentes

Custo se comporta como uma soma. Cem reais economizados no acabamento mais cem reais economizados na expedição são duzentos reais economizados. Cada corte vale por si, em qualquer lugar, e os cortes se acumulam.

Ganho não se comporta como uma soma. O quanto o sistema entrega em relação ao seu objetivo obedece à aritmética da corrente do capítulo 01: quem determina é o elo mais fraco.

Goldratt sintetizou a diferença numa formulação que virou marca da abordagem: uma hora perdida no gargalo é uma hora perdida no sistema inteiro; uma hora ganha num não-gargalo é miragem (*A Meta*, 1984).

A formulação original fala em **gargalo**, e não em restrição — *A Meta* trata de uma fábrica, onde os dois coincidem. A literatura posterior generalizou a frase para *restrição*, porque o raciocínio vale igual quando o elo mais fraco é uma regra ou o mercado (Cox & Schleier, 2010). Neste livro usamos a versão generalizada, mas vale saber de onde ela veio: o capítulo 01 gastou uma seção separando os dois termos justamente porque essa passagem costuma embaralhá-los.

Essa é a raiz de tudo o que vem neste capítulo. As duas aritméticas convivem na mesma empresa, e a maior parte dos sistemas de gestão só sabe fazer a primeira. Quando a lógica de custo é aplicada a uma decisão de ganho, as duas dão respostas opostas — e a de custo parece mais responsável (Cox & Schleier, 2010).

### Eficiência local

**Eficiência local** mede o quanto uma parte produziu em relação ao que ela poderia produzir. É honesta, é fácil de calcular e é fácil de cobrar.

Também mede, num sistema interdependente, uma coisa que não é o resultado: mede o que a parte fez para si, não o que ela entregou ao conjunto.

Na gráfica, a máquina de corte tem capacidade sobrando. Medida por ocupação, ela precisa rodar para "não ficar parada". Rodando, ela corta material que a impressora ainda não pediu. Esse material vira pilha. A pilha vira dinheiro parado, espaço ocupado — e, pior que os dois, vira fila que esconde onde o trabalho está de fato travado.

Goldratt propôs medir o sistema por três grandezas, e não pela eficiência de suas partes (*A Meta*, 1984):

- **Ganho** — a taxa em que o sistema gera dinheiro pelas vendas, descontado o que se pagou pelo que foi vendido. É uma taxa, não um estoque: produzir sem vender não gera ganho.
- **Inventário** — todo o dinheiro que o sistema investiu em comprar aquilo que pretende vender.
- **Despesa operacional** — todo o dinheiro gasto para transformar inventário em ganho.

Nenhuma das três é a eficiência de uma parte. E a peça cortada antes da hora tem um efeito exato sobre elas: **aumenta o inventário sem aumentar o ganho**, e consome despesa operacional no caminho.

As três voltam com força quando o assunto for operações — programação, pulmões, contabilidade de ganhos. Aqui elas entram pelo que resolvem agora: dar um lugar onde a decisão local aparece com o sinal certo.

### Ocupado não é produzindo

Um recurso que não é a restrição, operando a 100%, não está produzindo mais para o sistema. Está produzindo estoque.

Daí a conclusão que mais custa a ser aceita: **a ociosidade de um recurso que não é a restrição não é desperdício**. É folga — a **capacidade de proteção** que permite ao sistema absorver a variação do dia a dia e manter a restrição sempre alimentada (Cox & Schleier, 2010).

Uma máquina de corte ocupada 100% do tempo é uma máquina que, no dia em que a impressora precisar de algo às pressas, não terá como responder. A folga não é gordura: é o que impede a restrição de parar.

Parece desleixo. É o contrário de desleixo.

### O indicador escolhe o comportamento

Goldratt resumia o efeito numa frase que ficou: *"diga-me como você me mede e eu direi como me comporto"* (*A Meta*, 1984; a formulação é retomada em Goldratt, *A Síndrome do Palheiro*, 1990, ao tratar de indicadores).

Não é cinismo, é racionalidade. Quem é medido por um número trabalha para melhorar aquele número — porque foi contratado por ele, é avaliado por ele e será promovido ou não por ele. Esperar o contrário é esperar que as pessoas ajam contra o próprio interesse declarado pela empresa.

| Indicador local | Comportamento que ele induz | Efeito no sistema |
|---|---|---|
| Chamados fechados por dia (suporte) | Pegar os fáceis; encerrar o difícil sem resolver | Reabertura e retrabalho crescem |
| Ocupação da máquina (gráfica) | Rodar lote grande para diluir o setup | Estoque em processo e prazo maior |
| Agenda cheia (clínica) | Encaixar dois pacientes no mesmo horário | Espera, evasão e reputação no bairro |
| Desconto por volume (loja) | Comprar em lote fechado | Caixa parado no que não gira |

Nenhuma dessas linhas descreve alguém agindo mal. Todas descrevem alguém agindo bem dentro da régua que recebeu.

### Por que gente competente faz isso

Três razões, e nenhuma delas é falta de capacidade.

**O indicador local é fácil de medir; o ganho do sistema é difícil de atribuir.** Quanto do resultado do mês veio da decisão do comprador da loja? Ninguém sabe dizer com precisão. Quanto de desconto ele conseguiu? Está na nota fiscal.

**A responsabilidade é da parte; o resultado é do todo.** Cada gerente responde por uma fatia. O sistema, que é o que gera o resultado, não tem dono na estrutura — e o que não tem dono não é otimizado por ninguém.

**Quem se sacrifica pelo todo aparece pior no relatório.** Esta é a mais grave. Sem uma regra explícita que proteja quem opera abaixo da própria capacidade em benefício do sistema, subordinar-se ao todo é um ato de coragem individual. E coragem individual não é política de gestão: ela funciona enquanto a pessoa aguentar, e acaba na primeira avaliação de desempenho.

Guarde este ponto. Ele volta no capítulo 03, no passo que quase todo mundo pula.

## Erros comuns

**Somar eficiências.** *Sinal:* um relatório com a "eficiência média" da operação. A média esconde justamente a informação que importa — qual é o elo mais fraco. Cinco partes a 100% e uma a 60% dão a mesma média que seis partes em torno de 93%, e as duas situações não têm nada em comum.

**Cortar custo onde não é a restrição.** *Sinal:* o corte foi aprovado porque "ali sobrava". Sobrava porque era capacidade de proteção; três meses depois, a restrição para esperando aquilo que foi cortado.

**Confundir estar ocupado com estar produzindo.** *Sinal:* alguém defende uma decisão dizendo "não podemos deixar a máquina parada", sem conseguir dizer o que o sistema ganha com ela rodando.

**Culpar a pessoa pelo comportamento que o indicador induziu.** *Sinal:* o discurso da reunião é sobre comprometimento e visão do todo, enquanto o bônus continua atrelado ao número da área.

**Trocar o indicador sem trocar a decisão que ele governa.** *Sinal:* o painel mudou e o orçamento, a meta e a promoção continuam iguais. O indicador que manda é o que paga.

**Aceitar o ótimo local porque ele é justo.** *Sinal:* a defesa da métrica é "não é justo cobrar de mim o resultado de outra área". A objeção é legítima e a conclusão é errada: a resposta não é medir cada parte por si, é fazer com que a régua da parte reflita o que o sistema precisa dela.

## Mão na massa

<div data-bateria="cap02"></div>

### Leitura executiva

Custo se soma; ganho não. O resultado de um sistema interdependente obedece à aritmética da corrente — uma hora ganha fora da restrição é miragem (*A Meta*, 1984). Por isso **eficiência local** é uma medida honesta de uma coisa que não é o resultado: um recurso que não é a restrição, operando a 100%, produz estoque, não ganho, e sua ociosidade é **capacidade de proteção**, não desperdício. O mecanismo que transforma isso em prejuízo é o indicador: quem é medido por um número trabalha para aquele número, racionalmente e de boa-fé. O time de suporte medido por chamados fechados pega os fáceis; a gráfica medida por ocupação roda lotes grandes; a clínica medida por agenda cheia encaixa dois no mesmo horário. Culpar as pessoas não corrige nada, porque o problema é a régua — e a régua que manda não é a do painel, é a que paga.
