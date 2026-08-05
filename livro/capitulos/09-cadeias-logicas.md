# 09 — Cadeias Lógicas

> **Conteúdo revisado em 2026-08** · edição inaugural · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

Ao final deste capítulo, você deve conseguir:

1. **Encadear** conexões de causa e efeito preservando o rigor de cada elo;
2. **Reconhecer** quando um efeito exige mais de uma causa simultânea, e representar isso;
3. **Detectar** os três defeitos clássicos de cadeia: salto, circularidade e efeito órfão;
4. **Ler** uma cadeia de baixo para cima e de cima para baixo, verificando os dois sentidos.

## O problema

Uma conexão isolada raramente explica um problema real. O que se observa na prática é uma sequência: uma causa produz um efeito, que por sua vez produz outro, até chegar ao sintoma que incomoda.

O risco do encadeamento é a **degradação silenciosa**. Cada elo, examinado sozinho, parece razoável; a cadeia inteira, no entanto, pode ir do plausível ao absurdo em quatro passos — sem que em nenhum ponto específico se consiga apontar onde quebrou.

## O conceito

Uma cadeia é a ligação de conexões em que **o efeito de um elo é a causa do seguinte**:

> Se **A**, então **B**. Se **B**, então **C**. Se **C**, então **D**.

Duas regras mantêm a cadeia honesta.

**Regra 1 — cada elo é testado sozinho.** Não existe elo que "funciona no conjunto". Se "se B então C" não passa no teste do capítulo 06 isoladamente, a cadeia está quebrada ali, por mais convincente que seja o quadro geral.

**Regra 2 — o efeito de um elo é literalmente a causa do próximo.** A mesma frase, sem reformulação. É aqui que a maior parte das cadeias vaza: o efeito escrito foi "o prazo aumenta" e a causa seguinte virou "os clientes ficam insatisfeitos com a empresa" — que não é aquilo, é uma versão ampliada. A ampliação silenciosa é a forma mais comum de salto lógico.

## Quando uma causa não basta

Frequentemente um efeito não decorre de uma causa isolada, mas da **presença simultânea de duas ou mais**. É a chamada causalidade conjunta, e representá-la explicitamente é o que impede a cadeia de mentir.

> Se **a fábrica opera no limite da capacidade** **e** **o vendedor promete datas sem consultar a fila**, então **a empresa assume compromissos que não consegue cumprir**.

Nenhuma das duas sozinha produz o efeito: uma fábrica no limite com promessas conservadoras não gera descumprimento; um vendedor otimista com fábrica ociosa também não. As duas juntas, sim.

Isso tem uma consequência direta e prática: **quando duas causas são conjuntas, remover qualquer uma delas quebra o efeito.** Você acabou de ganhar duas alternativas de intervenção onde antes parecia haver uma.

O sinal de que falta uma causa conjunta é aquele "desde que" do capítulo 06 — quando você lê "se A então B" e a resposta honesta é "sim, desde que também…", o que vem depois do "desde que" é a segunda causa.

## Os três defeitos clássicos

**Salto lógico.** Faltam elos intermediários; a cadeia pula do início ao fim. Sintoma: o leitor concorda com o começo, concorda com o fim, e não consegue explicar como se chegou de um ao outro. Correção: inserir os passos que estavam na sua cabeça e não no papel.

**Circularidade.** A cadeia volta ao ponto de partida, e cada elemento é explicado pelo outro. Nem sempre é erro — sistemas realimentados existem, e o capítulo 11 trata exatamente de um deles. Vira erro quando a circularidade é acidental e passa a funcionar como explicação ("está atrasado porque está atrasado").

**Efeito órfão.** Um efeito aparece na cadeia sem causa que o produza — geralmente porque veio da sua experiência, não do raciocínio escrito. Sintoma: quem lê pergunta "de onde saiu isso?".

## Ler nos dois sentidos

Toda cadeia deve ser lida duas vezes, e as duas leituras verificam coisas diferentes.

**De baixo para cima** (da causa ao efeito), com "se… então…": verifica a **suficiência** de cada elo. Dado isto, aquilo acontece mesmo?

**De cima para baixo** (do efeito à causa), com "porque…": verifica se a explicação **satisfaz**. O prazo aumenta *porque* a fila cresce; a fila cresce *porque* entram mais pedidos do que saem. Se em algum ponto o "porque" soar insuficiente, falta causa ali.

Ler em voz alta, nos dois sentidos, é o teste mais barato e mais eficaz que existe. Erros que passam despercebidos na leitura silenciosa costumam soar errados quando falados.

## Erros comuns

**Cadeia longa demais.** Acima de cinco ou seis elos, a chance de degradação cresce e a utilidade cai. Se a cadeia ficou longa, provavelmente há mais de um problema misturado.

**Encadear pré-requisitos como se fossem causas.** "Para reduzir o prazo é necessário ver a fila; se vemos a fila, então o prazo reduz." O segundo elo é falso: ver a fila não reduz prazo nenhum sozinho. Cadeias de causa e cadeias de pré-requisito são estruturas diferentes — a segunda é o assunto do capítulo 13.

**Construir a cadeia para chegar à conclusão desejada.** O sinal é você já saber o fim antes de escrever o meio. Um antídoto honesto: construa a cadeia que sustenta a posição de quem discorda de você.

**Não testar as premissas dos elos.** Cada elo tem premissas (capítulo 08). Numa cadeia de cinco elos, a premissa mais frágil determina a resistência do conjunto.

## Mão na massa

<div data-bateria="cap09"></div>

### Leitura executiva

Cadeia é a ligação de conexões em que o efeito de um elo é a causa do seguinte. Duas regras a mantêm honesta: **cada elo é testado isoladamente** e **o efeito de um elo é literalmente a causa do próximo** — reformular pelo caminho é a forma mais comum de salto lógico. Quando um efeito exige duas causas simultâneas (causalidade conjunta), represente as duas: isso dá duas alternativas de intervenção, já que remover qualquer uma quebra o efeito. Três defeitos clássicos: salto, circularidade acidental e efeito órfão. Leia sempre nos dois sentidos — "se… então…" de baixo para cima testa suficiência; "porque…" de cima para baixo testa se a explicação satisfaz.
