# Plan 004 — Capítulo 09: O método Simplex

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-09

## Aviso sobre este documento

**Ele foi escrito depois da implementação, não antes.** O ciclo Maestro é
`specify → clarify → plan → tasks → implement`, e o *plan* é um **gate**: o autor aprova o
Constitution Check antes de existir código. Aqui a spec passou pelo gate e o *clarify* foi
respondido, mas a implementação começou em seguida, direto.

Registrar isso não é formalidade. Um Constitution Check escrito depois **não tem o poder de
barrar**: ele descreve o que foi feito em vez de decidir o que pode ser feito. As decisões
abaixo foram tomadas durante a implementação e estão sendo justificadas, não autorizadas — e a
diferença é exatamente a que o Princípio "prove, não declare" existe para preservar.

É a segunda vez que um gate de processo é pulado nesta série (a primeira foi a rodada 002, com
consequência de conteúdo). Desta vez não houve dano visível ao produto, o que torna o registro
mais importante, não menos: um atalho que dá certo é o que ensina a repetir o atalho.

## Constitution Check

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | 8 exercícios com devolutiva que explica, corrigidos no servidor, todos rastreando a objetivo declarado. **1 vídeo, com autoria, duração e atribuição da série não conferidas** | ⚠️ **dívida declarada** — ver §"A dívida do vídeo" |
| II | Modelar antes de resolver | Ordem intuição → matemática → código respeitada, e a intuição vem antes por decisão de estrutura: o leitor anda pelas arestas do desenho do capítulo 08 antes de ver qualquer quadro. Seção "quando não serve" com cinco situações e destino de cada uma | ✅ |
| III | Evidência acima de retórica | Todo número sai de `experimento.py`. O pior caso exponencial, que normalmente se cita, é **construído e medido**. **Um endereço de vídeo inventado foi detectado e removido antes de publicar** — ver §"O que quase escapou" | ✅ com incidente registrado |
| IV | Fonte-base é o experimento executável | `po-zero/etapa-03-simplex` roda em CPU, solver aberto, saída determinística verificada por dupla execução | ✅ |
| V | Arquitetura em três camadas | Capítulo de núcleo; nenhum conteúdo de fronteira entrou | ✅ |
| VI | Atualização por Radar | Nenhum artigo citado, logo nada a registrar. A varredura pendente entra na fila do Radar | ✅ |
| VII | Livro vivo | Selo de datação no capítulo; edição 0.7 no histórico com as dívidas e o incidente | ✅ |
| VIII | Português canônico | Só PT, conforme ADR 0002. *Tableau* mantido entre parênteses na primeira ocorrência, como termo consagrado | ✅ |
| IX | Sigla nunca nasce nua | PL, CPU e GB abertas na primeira ocorrência do capítulo; doze verbetes novos no glossário | ✅ |
| X | Direitos autorais | Instância autoral; o cubo de Klee–Minty é construção matemática de domínio público, implementada do zero | ✅ |
| XI | DoD verificável | Build e testes verdes, com saída colada em [`verificacao.md`](verificacao.md) | ✅ |

**Violações que impediriam a rodada:** nenhuma no produto. **O processo teve uma**, e é o
próprio documento que você está lendo: o gate de plano não aconteceu.

### A dívida do vídeo

Igual à das rodadas anteriores, **com um agravante**. Nos capítulos 07 e 08 os dois vídeos eram
da mesma série, e a correspondência com os capítulos era direta. A série não cobre o Simplex,
então o vídeo deste capítulo veio de outra origem, localizada por busca — e a atribuição da
série ao curso que o resultado indica **não foi confirmada na fonte**.

Isso é um grau a mais de incerteza sob o mesmo `⏳`, e por isso ganhou seção própria na
Videoteca em vez de virar mais uma linha na tabela. Duas fichas com o mesmo símbolo não podem
esconder níveis diferentes de dúvida.

### O que quase escapou

O rascunho do capítulo trazia um endereço de YouTube que eu **inventei**: um identificador de
vídeo plausível, num formato correto, apontando para nada verificado. Foi detectado antes de
publicar, ao conferir se o ambiente alcançava a fonte, e substituído por um endereço localizado
em busca real.

Vale o registro porque a detecção foi **acidental** — não havia portão. O portão que existe
(`verifica-referencias.mjs`) confere referências a capítulos, não URLs externas. A conclusão
honesta é que a defesa contra URL inventada, hoje, é a disciplina de quem escreve, e disciplina
não é mecanismo. Fica anotado no [ROADMAP](../../ROADMAP.md) como trabalho contínuo.

## Estratégia

Quatro blocos, na ordem que o Guia Editorial impõe — o texto não pode citar número que ainda
não foi medido:

1. **O experimento primeiro.** `po-zero/etapa-03-simplex` roda e produz `resultados.json`, com
   os três casos, a combinatória e o pior caso medido. Só então o capítulo é escrito.
2. **O portão em dívida, antes dos exercícios novos.** `verifica-otimos.mjs` entra **antes** de
   a bateria `cap09` ser escrita, para que ela nasça sob verificação em vez de ser conferida
   depois. É a inversão que a edição 0.6 pediu.
3. **O capítulo**, no esqueleto do Guia Editorial.
4. **Motor e registro**: capacidade nos dois lados do espelho, sumário, mapa, videoteca,
   glossário, histórico.

## Decisões de implementação

| Decisão | Por quê |
|---|---|
| **Aritmética exata (`Fraction`) no Simplex didático** | O quadro publicado tem de ser o quadro do caderno. Com ponto flutuante, `1/2` viraria `0,4999…` e a comparação entre papel e máquina viraria discussão sobre epsilon — perdendo o ponto do capítulo |
| ***Big-M* simbólico**, com o custo como par `(parte em M, parte numérica)` | É como se faz no quadro-negro, e evita ensinar o atalho que produz o erro clássico: com M numérico pequeno demais, um modelo inviável devolve resposta com cara de ótima |
| **A segunda instância nasce da mesma história** (compromisso de 5 unidades) | Trocar de contexto no meio do capítulo custa mais do que ganha. E o subproduto é bom: o compromisso custa R$ 150, que é uma frase de reunião, não de álgebra |
| **O pior caso é construído, não citado** | As fontes acadêmicas não são alcançáveis deste ambiente. Em vez de citar o que não pude abrir, medi o que dava para medir. O resultado é mais forte: conferível por quem também não tem a referência |
| **A convexidade entra como parágrafo próprio, antes do quadro** | O critério de parada é a única coisa do método que exige justificativa, e ela é geométrica. Sem isso o capítulo vira receita de tabela — o risco declarado na spec |
| **O preço-sombra é mostrado e deixado em suspenso** | O quadro final o entrega de graça; escondê-lo seria artificial. Mas lê-lo sem a faixa de validade é o erro clássico, e a faixa é o capítulo 13. Mostrar e nomear a dívida é o meio-termo honesto |

## Mudanças de motor

| Mudança | Por quê |
|---|---|
| **`verifica-otimos.mjs`**, novo portão no build | A dívida deixada pela edição 0.6. Resolve todo modelo declarado em rubrica, em racionais exatos sobre `BigInt`, e confere o ótimo afirmado. Tem duas metades: conferir o que foi declarado **e** exigir declaração de quem afirma ótimo — sem a segunda, bastaria omitir o campo para voltar ao estado do defeito |
| **Campo `modelo` no registro de exercícios** | O portão precisa de um modelo legível por máquina. Aceita lista, para exercícios que apresentam um modelo errado e sua correção (é o caso do `cap07.exC`) |
| **`verifica-referencias.mjs` passa a medir o mapa, não o sumário** | O portão confundia "publicado" com "existe" e barrava referência a vaga declarada. Neste handbook os dois são diferentes **de propósito** (ADR 0004): apontar ao leitor onde a resposta vai morar é o que o mapa existe para permitir. O portão continua pegando número fora do mapa, par repetido e intervalo decrescente — e agora **informa** quantas referências apontam para vaga |
| Capacidade `simplex` nos dois lados do espelho | Gating por capítulo, como as anteriores |

## Riscos de implementação

| Risco | Mitigação |
|---|---|
| Quadro publicado com erro de conta | **Nenhum quadro do capítulo foi digitado à mão**: todos saem da saída do `imprimir()` do experimento. O mesmo vale para os quadros dentro dos enunciados dos exercícios |
| O portão novo passar sem medir nada | **Provado quebrando**, três vezes: com o defeito histórico do `cap07.exC` reintroduzido, ele acusa e nomeia o ótimo verdadeiro; com um `modelo` removido, acusa a falta de cobertura; com o sentido invertido num modelo de região ilimitada, acusa o ótimo finito impossível. As três saídas estão na verificação |
| Repetir o defeito da edição 0.6 numa bateria nova | A bateria `cap09` nasceu **depois** do portão, e todos os seus modelos passam por ele |
| Generalizar o portão de referências virar afrouxamento | O universo saiu do sumário (13 páginas) para o mapa (77 vagas) — continua fechado, e agora corresponde à estrutura declarada. Referência a capítulo 78 falha exatamente como antes |
