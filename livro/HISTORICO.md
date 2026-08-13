# Histórico

> **Conteúdo revisado em 2026-08** · edições, datas e o que mudou a cada rodada.

Este handbook é vivo: não tem versão final. Cada edição registra o que mudou, quando, e com
apoio de qual modelo de Inteligência Artificial (IA) — em coerência com a nota de autoria da
[Introdução](00-introducao.md).

Registro é *append-only*: edição publicada não se reescreve. Quando um número ou uma
recomendação muda, a mudança entra como edição nova, e a antiga permanece.

### Edição 0.1 — 2026-08-06 · Fundação e mapa do handbook

Rodada inaugural. O repositório foi **refundado**: nasceu como clone do motor do livro *Teoria
das Restrições* (mesmo autor) e nesta edição passa a ser o handbook de Pesquisa Operacional
(PO), com governança, aparato e sumário próprios.

**Entrou:**

- **Constituição do handbook** (versão 1.0.0), com onze princípios — entre eles *modelar antes
  de resolver* (II), *arquitetura em três camadas* (V) e *atualização científica por Radar*
  (VI). Herda a metodologia [Maestro](https://github.com/GHDaru/maestro), adotada como
  obrigatória em todas as rodadas.
- **[Mapa do handbook](mapa-do-handbook.md)** — o sumário declarado: 77 vagas em onze partes,
  organizadas em três camadas (núcleo, módulos aplicados, fronteira). É o entregável central
  desta edição.
- **[Estudo do corpo de conhecimento](../estudos/001-corpo-de-conhecimento-po.md)** — a
  pesquisa que fundamenta o recorte: como Hillier & Lieberman, Winston e Arenales et al.
  organizam o campo, o que os livros-texto cobrem mal (ALNS, *matheuristics*, aprendizado de
  máquina em solvers, otimização sob incerteza) e as decisões de recorte que produziram o mapa.
- **Aparato editorial completo** — Guia Editorial com o esqueleto de capítulo obrigatório,
  bibliografia com as obras de referência verificadas, videoteca com a política de curadoria,
  glossário e banco de exercícios.
- **[Radar científico](../radar/RADAR.md)** — o mecanismo pelo qual artigo entra no livro:
  datado, com veredito e com o registro do que ele muda.
- **[Roadmap](../ROADMAP.md)** — a ordem de ataque das rodadas, que deliberadamente **não** é a
  ordem do sumário: Programação Linear (PL) vem antes dos Fundamentos.
- **Autorização de uso dos vídeos** do canal de João Sarubbi (CEFET-MG), registrada na
  videoteca.

**Saiu:** todo o conteúdo herdado do livro de Teoria das Restrições — capítulos, especificações,
registros de decisão e o objeto interativo daquele livro. O conteúdo permanece íntegro no
repositório de origem; aqui ele foi removido para que o handbook não carregue um sumário que
não é o seu.

**Decisões registradas:** reúso do motor ([ADR 0001](../adr/0001-reuso-motor-livro-vivo.md)),
português como fonte canônica com o inglês como dívida declarada
([ADR 0002](../adr/0002-portugues-primeiro.md)), pilha do `po-zero` em Python com solver aberto
([ADR 0003](../adr/0003-stack-po-zero.md)) e a arquitetura em três camadas do sumário
([ADR 0004](../adr/0004-arquitetura-do-sumario.md)).

**Dívida declarada.** Ratificar os princípios coloca o estado atual deliberadamente fora de
conformidade em três pontos, e a distância é registrada aqui em vez de escondida:

| Dívida | Princípio | Quando fecha |
|---|---|---|
| Nenhum capítulo de método publicado — logo, nenhum exercício e nenhum vídeo | I | 🟡 parcial — dois capítulos e 14 exercícios no ar; os vídeos seguem em confirmação (edições 0.3 e 0.4) |
| `po-zero` sem etapas: só o esqueleto e a decisão de pilha | IV | ✅ fechada em 2026-08-06 — etapa 01 no ar (edição 0.3) |
| Par em inglês inexistente | VIII | Após o núcleo, conforme roadmap |
| Livros-base ainda não mapeados na bibliografia | X | ✅ fechada em 2026-08-06 — ver edição 0.2 |

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.2 — 2026-08-06 · Livros-base mapeados

Os dois livros didáticos que o autor adota com os alunos foram registrados e mapeados contra o
[Mapa do handbook](mapa-do-handbook.md).

**Entrou:**

- **Ficha bibliográfica** das duas obras — Lachtermacher, *Pesquisa Operacional na Tomada de
  Decisões* (Elsevier/Campus, 224 p.) e Arenales, Armentano, Morabito & Yanasse, *Pesquisa
  Operacional* (Elsevier, 2007, 542 p.) — com a estrutura declarada de cada uma.
- **Tabela de correspondência** entre as partes do handbook e as unidades de cada obra, para
  que o aluno transite entre o handbook e o livro impresso sem se perder.

**O achado que vale como decisão editorial:** as duas obras juntas cobrem bem as Partes I a IV,
VI e VIII, e **não cobrem as Partes V, VII e XI** — metaheurísticas, otimização sob incerteza e
fronteira. É a maior contribuição própria do handbook, e confirma o recorte que o
[estudo do corpo de conhecimento](../estudos/001-corpo-de-conhecimento-po.md) havia feito
*antes* de as obras serem consultadas.

**Duas consequências para a rodada de Programação Linear:** o handbook mantém dualidade logo
após o Simplex (como Arenales, não como Lachtermacher), e promove casos especiais e
degenerescência a capítulo próprio — assunto que nenhuma das duas obras trata em separado.

**Direitos autorais.** Só metadados e correspondência foram versionados. Nenhum trecho, figura
ou enunciado das obras entrou no repositório (Princípio X).

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.3 — 2026-08-06 · Capítulo 07: formulação de modelos lineares

> ⚠️ **Registro superado pela edição 0.4.** Os números citados nesta entrada — marcenaria, mesas
> e estantes, R$ 13.800 — vieram do exemplo condutor que foi **substituído** um dia depois pelo
> exemplo de sala do autor (montadora, MRP inverso). O script citado abaixo hoje produz outros
> números. Registro datado não se reescreve: esta nota existe para que a entrada não engane quem
> lê hoje, nem o tutor, que indexa esta página.

O primeiro capítulo de método do handbook, e a primeira vez que a máquina inteira — texto,
exercícios corrigidos no servidor e código reproduzível — roda de ponta a ponta.

**Entrou:**

- **Capítulo 07 — Formulação de modelos lineares**, abertura da Parte II. Estrutura o trabalho
  em quatro perguntas (o que se escolhe, qual a única medida, o que limita, o que é dado) e
  abre por um erro real: uma marcenaria que maximiza receita em vez de margem.
- **Quatro exercícios** (`cap07`), em dificuldade crescente — reconhecer, formular, diagnosticar
  e aplicar ao próprio contexto —, cada um rastreando a um objetivo de aprendizagem.
- **`po-zero/etapa-01-formulacao`** — as duas formulações lado a lado, resolvidas com HiGHS.
  `experimento.py` regenera `resultados.json` byte a byte, com versões declaradas.
- **Capacidade `formulacao`** no tutor, liberada no capítulo 07.
- **Marcador de vaga declarada** na navegação: as partes mostram o que ainda não foi escrito
  como cartão tracejado apontando para o Mapa, em vez de omitir. O livro passa a publicar fora
  da ordem do mapa, e diz isso ao leitor.

**Os números do capítulo, e de onde vêm.** O plano que maximiza margem produz 30 mesas e 40
estantes (R$ 13.800/mês); o que maximiza receita produz 60 mesas e nenhuma estante, fatura mais
(R$ 54.000) e entrega R$ 13.200 de margem — R$ 600 a menos por mês, deixando 60 horas de
acabamento paradas. Todos saem de `po-zero/etapa-01-formulacao/experimento.py`.

**Portões reforçados nesta rodada:**

- **Rastreio exercício → objetivo agora é verificado.** O Guia Editorial dizia que "o build
  falha se o exercício apontar para um objetivo que não existe"; até aqui isso era prosa e nada
  media. Agora o portão confere que o objetivo está declarado no capítulo que monta a bateria —
  e foi provado quebrando-o de propósito.
- **O portão de rubrica pegou um vazamento real**: o exemplo de sintaxe do Banco de Exercícios
  compartilhava os primeiros 40 caracteres de um critério do `cap07.exB`. O exemplo foi
  reescrito com texto que ninguém escreveria de verdade, e o motivo ficou registrado lá.

**Dívida declarada.** Duas, ambas do próprio capítulo:

| Dívida | Princípio | Quando fecha |
|---|---|---|
| Vídeo do capítulo 07 sem autoria e duração conferidas | I | Quando o autor indicar o vídeo do canal parceiro |
| Sem artigos científicos na seção de fundamentos — a varredura de literatura sobre ensino de formulação não foi feita | III | Fila do Radar |

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.4 — 2026-08-07 · Capítulo 08 e o exemplo de sala

A edição que troca o exemplo condutor do handbook pelo **exemplo que o autor usa em aula** e
publica o método gráfico em cima dele.

**O que motivou a troca.** O capítulo 07 tinha sido implementado antes de o autor responder qual
seria o exemplo condutor — os gates de aprovação da especificação e do plano foram encurtados, e
o capítulo nasceu com uma marcenaria genérica. O exemplo real é melhor, e o registro do erro de
processo está na [spec 002 v2](../specs/002-cap07-formulacao/spec.md).

**Entrou:**

- **Capítulo 08 — A geometria da Programação Linear**, com a narrativa de sala: cada variável
  numa dimensão, o significado dos pontos negativos, a laranja e a faca, a região viável, a reta
  de iso-lucro como curva de nível, o gradiente, e o procedimento que termina no sistema 2×2 das
  restrições que sustentam o vértice.
- **A primeira ilha interativa do handbook** (`regiao-viavel`): o leitor liga a segunda
  restrição e vê a região encolher, sobe a reta de iso-lucro e vê onde ela encosta por último.
  É o GeoGebra da aula virando objeto do livro, com degradação para o texto sem JavaScript.
- **Dez exercícios** (`cap08`): cinco de resolução com o modelo dado, cinco de modelagem a partir
  de enunciado. Um cai em múltiplos ótimos, um tem ótimo fracionário, um é de minimização com
  restrições de piso, e num deles a restrição que sustenta o vértice é um eixo.
- **`po-zero/etapa-02-metodo-grafico`** — enumeração de vértices por pares de restrições,
  conferida contra o HiGHS nas três etapas.
- **Capítulo 07 reescrito** sobre a montadora, e `etapa-01` refeita para montar o modelo a partir
  da **lista de materiais** — MRP ao contrário — com as duas regras de bolso refutadas por número.

**Os números, e de onde vêm.** Sem restrição, ilimitado. Com 10 CPUs, dez do Tipo 2 e R$ 1.500.
Com 12 pentes de 16 GB, o ótimo anterior deixa de existir (faltavam 8 pentes) e o novo é 8 do
Tipo 1 mais 2 do Tipo 2, R$ 1.100 — a única combinação que esgota os dois recursos. As duas
regras de bolso perdem R$ 200 e R$ 100 por mês. Tudo de `po-zero/etapa-01` e `etapa-02`.

**Portões alterados:**

- A bateria deixa de ser limitada a **quatro** variantes (A–D) e passa a aceitar até 26. O limite
  vinha do livro de origem, onde uma bateria era o mesmo exercício em quatro versões; aqui uma
  bateria é banco de treino.
- A regra "a variante D é a do leitor" virou o campo **`contexto`** (`livro` | `leitor`). A regra
  antiga confundia **posição** na bateria com **natureza** do exercício, e um banco de dez itens
  expôs isso.

**Dívida declarada.** As mesmas duas, agora nos dois capítulos: vídeo sem autoria e duração
conferidas, e ausência de artigos científicos na seção de fundamentos.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.5 — 2026-08-07 · Vídeo provisório, e o estado que ele exigiu criar

Os capítulos 07 e 08 passam a ter vídeo. **Provisório**, e dizendo por quê.

**O problema.** A política da Videoteca exige autor, duração e justificativa declarados — e o
ambiente em que este handbook é produzido **não alcança o YouTube nem as páginas de curso das
universidades**: o proxy de rede bloqueia os dois. Foi tentado, e falhou nos dois caminhos.

Restavam três saídas: publicar capítulo sem vídeo, violando o Princípio I; **inventar** autor e
duração, violando o Princípio III e a regra de atribuição da própria Videoteca; ou publicar o
que se sabe e marcar o que não se sabe.

**A decisão.** A terceira, formalizada como um **estado** e não como exceção. A Videoteca passa
a ter dois: *definitivo*, com a ficha conferida na fonte, e *provisório*, em que os campos não
conferidos aparecem `⏳` — **nunca preenchidos por estimativa**. Todo vídeo provisório carrega,
ao lado, a condição da sua promoção.

**Entrou:**

- Capítulo 07: *Aula 1 — Programação Linear: introdução*.
- Capítulo 08: *Aula 2 — Programação Linear: método gráfico*.

São da mesma série, e a divisão dela — introdução, depois método gráfico — coincide com a dos
dois capítulos. Título e endereço foram verificados por busca; **autoria e duração, não**, e a
Videoteca diz isso numa tabela campo a campo.

**Como fecha.** Preferencialmente pela troca pelos vídeos equivalentes do canal do João Sarubbi,
cujo uso está autorizado — aí a ficha nasce completa. Alternativamente, o autor assiste aos
provisórios e completa a ficha.

**O que não mudou:** a fachada. Sem bloco de vídeo no motor, o "Assista" é link puro — e link
puro é a fachada mais forte que existe, porque nenhuma requisição sai do navegador do leitor
antes do clique.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.6 — 2026-08-07 · O que a revisão independente encontrou

Um agente em contexto fresco revisou os capítulos 07 e 08 contra as especificações e a
constituição — o gate que a metodologia exige e que quem escreve não pode cumprir. Ele **não
aprovou o merge**, e tinha razão.

**O achado que justifica o gate inteiro.** O exercício `cap07.exC` apresentava uma saída de
solver **impossível**: para o modelo escrito, o ótimo era (137,5; 125) com 103.500, e o
enunciado afirmava (200, 0). Não era erro de digitação — era um exercício de *diagnóstico* que
mandava o leitor ler um sintoma inexistente, com critérios de correção falsos. Um aluno que
raciocinasse bem seria reprovado pela rubrica.

**A causa raiz, registrada para não se repetir:** as dez respostas do capítulo 08 foram
conferidas com código; as quatro do 07, não. **O único banco sem verificação executável foi o
único com erro de fato.**

**Também corrigido:**

- A ilha interativa dizia "a reta encosta" ao passar por um vértice **não-ótimo** — contradizendo
  a definição do próprio capítulo no ponto exato em que o leitor a está formando. E abria com a
  memória ligada, invertendo a ordem da narrativa.
- Quatro exercícios apontavam para objetivos que não testavam. O capítulo não tinha objetivo para
  "formular a partir de enunciado", embora a prática o cobrasse: entrou o **O5**.
- Duas rubricas com erro: uma trocava gradiente por reta de iso-lucro, outra citava um número
  que não decorre do erro que ela descreve.
- O capítulo afirmava "o último contato é sempre um vértice", desmentido por um exercício dele
  mesmo. Vale a formulação precisa: **se existe ótimo, existe um vértice ótimo**.
- Siglas nuas (CPU, GB, JSON), glossário intocado, mapa ainda marcando os dois capítulos como não
  escritos, e uma "saída colada" que tinha sido reescrita à mão.
- A edição 0.3 deste histórico propagava os números do exemplo descartado — e está indexada no
  corpus do tutor. Ganhou nota de superação, sem apagar o registro.

**O que fica como trabalho:** construir o portão que teria pego o `cap07.exC` sozinho — verificar
que todo exercício cujo enunciado afirme uma solução ótima seja consistente com o modelo que ele
mesmo apresenta. Está em `specs/003-cap08-geometria/tasks.md`.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), revisado por
agente independente em contexto fresco, sob curadoria e responsabilidade editorial humanas.

### Edição 0.7 — 2026-08-09 · Capítulo 09: o método Simplex

Rodada 004. Diferente das duas anteriores, **o conteúdo não veio de uma narrativa de sala** —
o autor respondeu ao *clarify* que não havia uma, e aprovou a proposta da especificação. Fica
registrado: a sequência didática deste capítulo é proposta editorial, não sequência já testada
com alunos.

Duas decisões do autor no gate: o veículo é o **quadro** (*tableau*), e a **Fase I / *big-M***
entra neste capítulo em vez de virar capítulo próprio.

**Entrou:**

- **[Capítulo 09 — O método Simplex](capitulos/09-simplex.md)**, encadeado na promessa que o 08
  deixou aberta. O algoritmo chega a (8, 2) e R$ 1.100 em duas iterações, **pisando exatamente
  nos vértices que o desenho do capítulo anterior mostrou**.
- A ponte central do capítulo: **vértice = solução básica viável**. A tabela de bases da
  montadora é, linha por linha, a mesma tabela de pares de retas do capítulo 08.
- ***Big-M* com uma segunda instância da mesma história**: cinco unidades do Tipo 2 já vendidas
  tiram a origem da região viável. O plano vira (2, 5) e R$ 950 — o compromisso custou R$ 150.
- A resposta à dívida do capítulo 07: **por que a ganância do Simplex não engana**, se duas
  regras gulosas foram refutadas lá. Porque ela escolhe só a direção do próximo passo, e o teste
  da razão escolhe o tamanho.
- **[Etapa 03 do `po-zero`](../po-zero/etapa-03-simplex/)** — Simplex de quadro em aritmética
  exata, com *big-M* simbólico e todos os quadros guardados.
- **Oito exercícios** (`cap09`, A–H), com três dedicados ao erro de conclusão sobre conta certa.
- Capacidade `simplex` no tutor, nos dois lados do espelho.
- Doze verbetes novos no [glossário](glossario.md): forma padrão, base, solução básica viável,
  custo reduzido, pivoteamento, teste da razão, convexidade, entre outros.

**O portão que faltava, construído.** A edição 0.6 deixou como trabalho o portão que teria pego
sozinho o defeito do `cap07.exC`. Ele existe: `publicar/verifica-otimos.mjs` resolve, em
aritmética exata sobre racionais, **todo modelo declarado numa rubrica** e confere o ótimo
afirmado. Foram anexados modelos verificáveis aos onze exercícios anteriores que afirmavam um
ótimo; hoje são dezenove modelos conferidos a cada build. O portão foi provado quebrando: com o
defeito histórico reintroduzido, ele acusa e nomeia o ótimo verdadeiro (103.500).

O portão tem duas metades, e a segunda importa tanto quanto a primeira: se a rubrica afirma um
ótimo e **não** há modelo declarado, o build falha. Sem isso, bastaria omitir o campo para o
exercício voltar ao estado em que o defeito nasceu.

**O pior caso, medido em vez de citado.** A afirmação de que o Simplex tem pior caso exponencial
costuma vir emprestada da literatura. Aqui o cubo de Klee–Minty é **construído** pelo
experimento, e os pivôs são contados: 3, 7, 15, 31, 63 e 127 para $n$ de 2 a 7 — sempre
$2^n - 1$. A troca foi deliberada, e nasceu de uma limitação: como as fontes acadêmicas não são
alcançáveis deste ambiente, uma afirmação que pudesse ser medida foi medida.

**Um erro meu, pego antes de publicar.** O rascunho do capítulo trazia um endereço de vídeo do
YouTube que eu **inventei** — exatamente o que o Princípio III proíbe. Foi substituído por um
localizado em busca real. Registrar isso aqui é o ponto: o defeito não chegou ao leitor, mas o
mecanismo que o produziu é o mesmo que produz os que chegam.

**Dívidas declaradas:**

- **O vídeo do capítulo 09 tem uma ressalva a mais** que os anteriores: não é da mesma série, e
  a atribuição da série ao curso indicado pela busca **não foi confirmada na fonte**. Está dito
  na [Videoteca](videoteca.md).
- **A seção de fundamentos científicos declara a lacuna.** arXiv, Crossref, OpenAlex e os sites
  das editoras respondem `403` ao proxy de saída deste ambiente. História do método,
  complexidade em média e comparação entre regras de pivoteamento seguem sem literatura
  primária.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.8 — 2026-08-09 · O método tem história (constituição 1.1.0)

Emenda constitucional pedida pelo autor, ao ler o capítulo 09:

> *"Importante trazer um racional do porquê, algo histórico, filosófico, do problema que motivou
> ter que buscar uma alternativa e solução para alguma decisão. Por exemplo: de onde veio big-M?
> Por quê, qual a ideia. Não quero passar decoreba, o livro deve ser uma inspiração motivacional,
> ter história."*

O diagnóstico era certeiro. O capítulo 09 explicava **como** o *big-M* funciona e por que a
mecânica é segura, e não dizia de onde a ideia veio nem qual padrão de raciocínio ela carrega.
Assim o leitor sai capaz de executar e incapaz de reconhecer o mesmo tipo de aperto noutro
contexto — que é a definição operacional de decoreba.

**Entrou:**

- **Princípio XII — Nenhum método cai do céu**, não-negociável. Constituição vai a **1.1.0**,
  com [ADR 0006](../adr/0006-o-metodo-tem-historia.md). Cinco consequências verificáveis, entre
  elas: **nome com origem é nome explicado**, e **todo artifício declara a ideia reaproveitável**
  por trás dele.
- **Seção "De onde isto veio"** no esqueleto obrigatório de capítulo, com §2.2 no
  [Guia Editorial](GUIA-EDITORIAL.md) dizendo o que ela precisa entregar: o aperto, o que se
  fazia antes, a virada, a ideia reaproveitável, o nome.
- **A seção no capítulo 09.** O Simplex nasceu de um problema de logística — planejar a Força
  Aérea dos Estados Unidos em 1947, no projeto SCOOP — e não de um problema de matemática. Com
  o desfazimento de um mal-entendido que quase todo aluno carrega: **"programação", em
  Programação Linear, quer dizer plano, não código.**
- **A resposta ao pedido do autor**, sobre o *big-M*: o aperto do ovo e da galinha (o método
  precisa de um vértice para começar, e achar o primeiro é tão difícil quanto o problema todo), e
  a ideia que fica — *quando não há ponto de partida, invente um e cobre caro por ele* —, com os
  lugares fora da PO onde o mesmo padrão aparece.
- **Portão para o princípio**: `verifica-capitulos.mjs` passa a exigir a seção. Duas listas com
  significados distintos, para não disfarçar escopo de dívida: o que **não é capítulo de método**
  (a introdução) e o que **é dívida de verdade**.
- Seção **História dos métodos** na [bibliografia](bibliografia.md), com as fontes e o estado de
  cada uma.

**Dívida retroativa, assumida.** Os capítulos **07 e 08 estão publicados sem a seção** e entram
na lista de dívida declarada do portão. Fazer o princípio valer só do 09 em diante seria
conveniente e desonesto.

**A honestidade que o princípio exige de si mesmo.** História é o terreno mais fácil do livro
para inventar, porque data errada e atribuição plausível soam bem e passam por revisão apressada.
Por isso a seção do capítulo 09 termina com uma tabela que separa **o que é documentado**, **o
que é atribuição corrente** e **o que é leitura deste livro** — e admite, numa linha, que não
encontrei fonte para a pergunta mais simples de todas: **por que a letra M**. A leitura óbvia é
*muito grande*; leitura óbvia não é documento.

Todas as fontes de história nascem `⏳`: localizadas em busca, **não abertas**, porque este
ambiente não alcança arquivo acadêmico. É dívida de acesso, não de pesquisa.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.9 — 2026-08-09 · A dívida retroativa do Princípio XII, quitada

A edição anterior criou o Princípio XII e deixou os capítulos 07 e 08 na lista de dívida
declarada do portão. Esta edição quita a dívida **no mesmo dia em que ela nasceu**, e a lista
volta a ficar vazia.

**Capítulo 07 — a formulação que valeu a pena sem método.** Em 1945 o economista George Stigler
escreveu o problema da dieta — a combinação mais barata de alimentos que atende às exigências
nutricionais — e **não tinha como resolvê-lo**. Chutou, por tentativa e eliminação: US$ 39,93 por
ano, a preços de 1939, sem prova de que fosse o melhor.

Dois anos depois o método existia. Nove escriturários, com calculadoras de mesa manuais, gastaram
**120 dias-de-escriturário** para chegar a US$ 39,69. O chute do Stigler errou por **24 centavos
por ano**.

É a história certa para um capítulo de formulação, porque o que ela ensina é onde está o
trabalho: **o custo de calcular despencou; o de formular, não.** O modelo de 1945 roda hoje em
milissegundos sem uma vírgula alterada. E a dieta ótima da época era impecável e intragável —
farinha, repolho, feijão seco —, o que diz a coisa mais importante do capítulo: **o modelo
responde exatamente a pergunta que você fez.**

Ideia reaproveitável: *escrever o problema com precisão é ganho por si só, mesmo sem meio de
resolvê-lo.* O que está escrito pode ser criticado, comparado e corrigido — e é essa a vantagem.

**Capítulo 08 — o desenho não é muleta didática.** A assimetria histórica: no século XIX a teoria
dos sistemas de **equações** lineares estava dominada, e a das **desigualdades** mal saía do
lugar. A razão é a que o leitor sente na primeira restrição `≤`: uma equação fixa um ponto; uma
desigualdade descreve uma **região**, e não havia álgebra para regiões.

Em **1826**, Joseph Fourier — o das séries — publicou dois métodos para o problema: um algébrico,
de eliminação de variáveis, e um **geométrico**, para achar a região das soluções. Em vez de
inventar a álgebra que faltava, mudou de representação para uma em que "região" já era natural.
**Cento e vinte anos antes do Simplex, a região viável já estava desenhada.**

O método algébrico foi esquecido e redescoberto em 1936 por **Theodore Motzkin** — hoje
eliminação de Fourier–Motzkin. E aqui um fio que liga os dois capítulos: **é o mesmo Motzkin**
que sugeriu a Dantzig o nome *simplex*. A mesma pessoa nas duas pontas.

Ideia reaproveitável: *quando a álgebra não dá alça, troque de representação.* Nada do problema
muda; muda o que você consegue ver dele.

**A lista de dívida do portão está vazia** — e o comentário no código defende esse estado: uma
entrada nova ali é sempre aceitável; o que não é aceitável é ela ficar.

**Procedência.** Todas as afirmações históricas destas duas seções são `⏳`: localizadas em busca,
**não abertas na fonte**. Cada seção termina com a tabela que separa documentado, atribuição
corrente e leitura deste livro — inclusive marcando o que é interpretação editorial e não
história. As fontes entraram na [bibliografia](bibliografia.md).

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.10 — 2026-08-09 · As fontes de história, abertas

O acesso à literatura foi liberado no ambiente de trabalho, e as afirmações históricas das três
seções *De onde isto veio* — que nasceram todas `⏳`, localizadas em busca e **não abertas** —
foram lidas na fonte. A maioria virou `✓`.

**O que a leitura mudou, e a lição de método.** Três coisas aconteceram, e as três valem registro:

1. **Um fato que parecia errado estava certo.** Um resumo secundário abreviava o relato original
   de tal forma que os "nove escriturários" do capítulo 07 pareciam ser um erro de leitura — o
   resumo só mencionava "nove equações". A fonte primária confirma as duas coisas: **9 equações e
   77 incógnitas**, repartidas entre **nove escriturários**. A correção que eu ia fazer teria
   introduzido o erro.
2. **Nomes e números ganharam precisão.** Foi **Jack Laderman**, do *Mathematical Tables Project*
   do National Bureau of Standards, no **outono de 1947**, resolvendo a dieta de Stigler como
   **teste** do método recém-proposto.
3. **Apareceu a melhor parte da história, que resumo nenhum trazia.**

**O vinagre.** No início dos anos 1950, na RAND, Dantzig modelou a **própria dieta** como um
programa linear. A primeira solução ótima pedia **500 galões de vinagre** — porque a base de dados
listava vinagre com teor de água zero, e o objetivo era maximizar saciedade medida por peso menos
água. Na rodada seguinte, **200 tabletes de caldo por dia**; ele tentou beber quatro dissolvidos e
cuspiu, era salmoura. Perguntou ao médico por que a tabela de exigências não limitava o sal, e
ouviu: *"não era necessário — a maioria das pessoas tem bom senso o bastante para não consumir
demais"*.

**A restrição existia e era óbvia demais para alguém escrevê-la.** Dantzig pôs um limite superior
de três tabletes por dia e registrou: *"foi assim que os limitantes superiores em variáveis, na
programação linear, começaram"*.

É a melhor ilustração possível do que o capítulo 07 ensina, contada pelo inventor do método contra
si mesmo: **o modelo responde exatamente a pergunta que você fez** — e as duas causas de erro são
dado ruim e restrição não escrita.

**Também entrou:** o batismo do termo "programação linear" por **T. J. Koopmans**, na RAND, em
1948 — a expressão de Dantzig era *programming in a linear structure*. O capítulo 09 agora conta
que **as duas metades do nome do campo vieram de conversa de corredor**, e nenhuma foi escolhida
por quem inventou o método.

**O que continua em aberto**, dito item a item nas tabelas de procedência dos capítulos:

- **O nome *simplex* atribuído a Motzkin** — atribuição corrente, sem fonte primária. O texto que
  fecharia isso é *Origins of the Simplex Method*, do próprio Dantzig, e a editora responde `403`
  a acesso automatizado.
- **O *big-M* atribuído a Charnes** — os metadados do artigo de 1952 na *Econometrica* estão
  conferidos, mas o **conteúdo não foi lido**, então a atribuição segue corrente.
- **A origem da letra M** — sem fonte, e continua assim. A leitura óbvia é *muito grande*; leitura
  óbvia não é documento.

**Um item saiu da coluna errada.** O crescimento exponencial das desigualdades na eliminação de
Fourier–Motzkin estava marcado no capítulo 08 como "afirmação corrente, não medida". Está agora
sustentado por fonte aberta.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.11 — 2026-08-09 · A sessão de história

Rodada 005. Pesquisa concentrada, **sem publicar nada no livro** — o produto é
[`estudos/002-historia-dos-metodos.md`](../estudos/002-historia-dos-metodos.md), insumo das
seções "De onde isto veio" das rodadas que vêm.

**A decisão de processo.** O Princípio XII passou a exigir história em todo capítulo de método.
Pesquisar por capítulo, dentro de cada rodada, sai mais caro e sai pior — e há prova disso no
próprio livro: a ligação entre **Motzkin** no capítulo 08 e **Motzkin** no capítulo 09 só apareceu
porque as duas pesquisas foram feitas juntas. Em rodadas separadas, os dois capítulos teriam
saído sem a conexão.

**O que a pesquisa achou de melhor**, e que muda o encaminhamento de dois capítulos futuros:

- **O fluxo máximo nasceu de um problema de bombardeio.** Ford e Fulkerson citam como motivação um
  relatório da RAND de Harris e Ross, de 1955, **secreto por décadas**, sobre a rede ferroviária
  soviética. E o interesse dos autores **não era o fluxo máximo: era o corte mínimo** —
  *interdiction*, quais trechos destruir. O teorema que a sala aprende como coincidência elegante
  tinha, na origem, **dois donos com objetivos opostos**. A dualidade deixa de ser elegância e
  vira conflito formalizado.
- **O problema de transporte é dez anos mais velho do que se atribui.** Tolstoĭ publicou em 1930,
  num livro do Comissariado de Transportes soviético, com critério de ciclo negativo e uma
  instância 10 × 68 resolvida à otimalidade. A lição não é de precedência: é que **o que entra no
  cânone é o que é lido**, e isso depende de língua e de circulação.
- **O método elipsoidal foi manchete de primeira página do *New York Times*** em 7 de novembro de
  1979 — e um mês antes um jornal britânico anunciara que o caixeiro-viajante tinha sido resolvido,
  o que é falso. É o exemplo mais antigo do handbook para a Parte XI, que ensina a ler artigo
  aplicado. E ensina que **polinomial não quer dizer rápido**: o elipsoidal perde do Simplex na
  prática.

**O padrão de selos**, decidido pelo autor: `✓` fonte aberta e lida, `✓ᵐ` só metadados conferidos,
`⏳` atribuição corrente não confirmada, `❌` sem fonte, `📖` leitura editorial. A distinção entre
`✓` e `✓ᵐ` é o que impede confundir "existe e é este artigo" com "eu li e diz isso" — e é
exatamente onde a atribuição do *big-M* a Charnes continua parada.

**A fila de verificação** está no estudo, ordenada por dívida fechada por esforço. O item 1 é o
relato de Dantzig em *Origins of the Simplex Method*: fecharia o nome *simplex* por Motzkin **e**
a história de von Neumann e a dualidade. Está atrás de um `403` **da editora**, não da política de
rede.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.12 — 2026-08-09 · As três dívidas antigas, fechadas

Com o acesso ao YouTube e à literatura liberado no ambiente, três pendências que vinham sendo
declaradas edição após edição foram encerradas.

**1. Os vídeos saíram de `⏳` e viraram definitivos.** As três fichas nasceram provisórias porque
o ambiente não alcançava o YouTube. Agora estão conferidas na fonte:

- Capítulos 07 e 08 — **André Brochi**, canal *Matemática e Estatística*, 18min04s e 24min20s,
  publicados em 21 de maio de 2020.
- Capítulo 09 — **UNIVESP**, 18min48s, publicado em 10 de agosto de 2016.

A Videoteca dizia, na própria política, que *curadoria sem atribuição é apropriação* — e estava
em dívida com a própria regra enquanto o autor era um `⏳`. A ressalva extra que a ficha do
capítulo 09 carregava também caiu: a atribuição da série à UNIVESP, que aparecia só em resultado
de busca, **estava certa**.

O que **não** foi conferido continua dito: a frase "o que ele resolve" é leitura do editor a
partir do título e da posição na série. Ninguém assistiu.

**2. A ilha interativa foi operada num navegador — e ganhou portão.** Ela era o **único artefato
publicado do livro sem verificação executável**: a lógica tinha sido corrigida na edição 0.6 e
conferida por leitura, e ninguém a havia usado. Agora `publicar/verifica-ilha.mjs` abre o
capítulo 08 num Chromium e opera os controles, conferindo **as afirmações do capítulo**: que a
ilha abre com uma restrição só, que abaixo do ótimo a reta corta, no ótimo encosta e acima passa
por cima, e que ligar a memória mata o ótimo anterior — R$ 1.500 deixa de existir e o teto cai
para R$ 1.100, com (0, 10) saindo da tabela de vértices.

Quinze verificações, todas verdes. O portão foi provado quebrando: com a ilha abrindo com a
memória ligada — o defeito exato que a revisão da edição 0.6 encontrou à mão —, ele acusa quatro
falhas.

> **A lição de método desta edição.** A primeira versão do teste procurava a palavra "encosta" no
> texto inteiro da ilha e acusou três falhas. **A ilha estava certa**: o rótulo do controle é
> "Subir até encostar", e a busca casava com a legenda em vez do estado. Diagnosticar antes de
> corrigir evitou "consertar" código correto — é a segunda vez nesta série que isso acontece, e
> nas duas o erro estava no verificador, não no verificado.

**3. Os fundamentos científicos dos capítulos 07 e 09 deixaram de declarar lacuna.**

No **capítulo 09**, a contradição que o texto abria e não fechava — pior caso exponencial medido
versus desempenho prático — agora tem resposta com fonte lida: a **análise suavizada** de
Spielman e Teng, que mede o desempenho esperado sob pequenas perturbações da entrada e prova
complexidade polinomial nessa medida. A leitura que fica é acionável: **o pior caso do Simplex é
frágil** — exige coeficientes ajustados com precisão e não sobrevive a ruído.

No **capítulo 07**, os dois modos de falha da formulação — dado com significado errado e
restrição óbvia demais para ser escrita — passam a ser apresentados como **evidência de primeira
mão**, do relato de Dantzig sobre a própria dieta, com o teste prático de cada um.

**O que continua em dívida**, e agora por motivo de acesso da editora, não de política de rede:
a comparação sistemática entre regras de pivoteamento; o conteúdo de Bixby (2002), que fica só
como ponteiro; e a varredura sobre **qualidade de formulação**, cuja escassez é impressão
declarada e não resultado verificado.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), sob curadoria e
responsabilidade editorial humanas.

### Edição 0.13 — 2026-08-09 · Capítulo 10: casos especiais e degenerescência

Rodada 006, executada em **long run autorizado pelo autor**, com a instrução de consultar
especialistas nas decisões, registrar em ADR e prosseguir. Foi a primeira rodada em que o
**gate de plano aconteceu antes da implementação** desde que ele foi pulado na rodada 004.

**O que o capítulo entrega.** Quatro vereditos que não são um plano — inviável, ilimitado, mais
de um ótimo, vértice degenerado — e um quinto caso em que o método não termina. Para cada um, a
**conduta**: o que investigar, o que renegociar, o que dizer na reunião.

**A tese, medida em vez de afirmada:**

> **O que é do modelo sobrevive à troca do método. O que some quando você troca o método era do
> método.**

Ela sai de um experimento controlado na [etapa 04 do `po-zero`](../po-zero/etapa-04-casos-especiais/):
a mesma instância, com o modelo intacto, resolvida com duas regras de pivoteamento. Com a regra
de Dantzig — a que o capítulo 09 ensina — o Simplex **cicla**, com período 6, sem sair do ponto
$(0,0,0,0)$. Com a de Bland, **termina em 6 pivôs**. E no modelo degenerado os empates no teste
da razão **continuam existindo sob as duas regras**. A ciclagem some: era da regra. A
degenerescência fica: é do modelo.

**Duas fontes primárias abertas e lidas**, e uma delas dá a tese do capítulo escrita pelos
próprios autores do método, em 1955: *"embora a maioria dos problemas que surgem de fontes
práticas tenha sido degenerada, nenhum jamais ciclou"* (Dantzig, Orden e Wolfe). A segunda, de
2004, corrige um mal-entendido comum — o problema prático não é o ciclo, é o ***stalling***, a
estagnação finita — e registra que o procedimento anticiclagem dos solvers reais **não tem
garantia**.

**Três decisões editoriais foram a especialista e viraram ADR**, porque o autor estava ausente:

- [ADR 0007](../adr/0007-fronteira-entre-modelo-e-metodo.md) — a fronteira entre os capítulos 09
  e 10 (detecção já ensinada vira linha de tabela; detecção inédita vira seção) e o lugar da
  degenerescência no discurso do livro.
- [ADR 0008](../adr/0008-atribuicao-da-instancia-que-cicla.md) — a atribuição da instância que
  cicla, em três camadas, e a instância condutora do capítulo.

**A atribuição merece nota,** porque contraria o que quase todo material didático faz. A
instância de ciclagem costuma ser creditada a Beale (1955) sem ressalva. A fonte de 1955 lida
aqui credita os **primeiros** exemplos a **Hoffman** e a **Wolfe**; e o artigo de Beale se chama
*"Cycling in the **dual** simplex algorithm"*, enquanto a instância que circula é **primal**. O
handbook diz as três camadas e não afirma o que não conferiu.

**O que o guardião de processo barrou, e que estava certo.** O plano foi submetido antes de
qualquer linha de capítulo e voltou com cinco ressalvas. Quatro eram defeitos reais e foram
corrigidos: uma afirmação de que a regra de Bland "prova terminação" e "é mais lenta", escrita
por mim no código **sem fonte e sem medição**; uma frase falsa no README da etapa 03, dizendo que
o desempate por menor índice "evita os casos conhecidos"; uma decisão tomada e não registrada em
ADR; e a ausência do arquivo de verificação. O "mais lenta" virou **medição**: Bland nunca muda a
resposta e gasta mais pivôs em duas das quatro instâncias testadas.

**Correção em capítulo publicado.** A seção "quando não serve" do capítulo 09 dizia que o código
"usa a mais simples (menor índice)" para desempatar, o que sugeria cobertura parcial contra
ciclagem. **A cobertura é zero**, e o capítulo 10 exibe a instância em que aquele mesmo código
gira para sempre. A frase foi reescrita.

**Dívida declarada:** o vídeo do capítulo 10 é o único **provisório** do handbook, e por um campo
só — título, endereço e autoria conferidos na fonte; a duração não saiu da página em nenhuma
tentativa.

**Pendente de ratificação do autor**, e dito aqui porque o guardião apontou com razão: a tese
fixada no ADR 0007 governa a Parte II inteira, e a alteração do capítulo 09 mexe em texto já
publicado. Ambas vão ao gate de merge como itens explícitos.

**Produção:** conteúdo redigido com apoio de agente de IA (Claude, Anthropic), com decisões
submetidas a agentes especialistas e registradas em ADR, sob curadoria e responsabilidade
editorial humanas.

### Edição 0.14 — 2026-08-12 · O selo vira medição

Rodada de **motor**, não de capítulo: nada foi escrito no livro. O que mudou é o que o livro
consegue provar sobre si mesmo.

**O problema.** O handbook tinha um sistema de selos de procedência honesto — `✓`, `✓ᵐ`, `⏳`,
`❌` — e **nenhum deles verificado por máquina**. O `✓` ao lado de um identificador de objeto
digital (DOI, *Digital Object Identifier*) era palavra de quem escreveu. Um dígito trocado
passava; um DOI inventado passava. Não é hipótese: na edição 0.9 uma URL de vídeo **foi
inventada** e só apareceu por acidente, ao tentar abri-la.

**Entrou:**

- **`publicar/verifica-fontes.mjs`** — portão do `npm run build`, antes da geração do site.
  Roda **offline**, comparando a bibliografia com `livro/fontes.lock.json`, versionado.
- **`publicar/atualiza-fontes.mjs`** (`npm run fontes`) — o gerador, com rede, sob demanda.
  **Recusa rodar em integração contínua (CI)**, para que o reparo diante de um build vermelho
  nunca seja "regerar até ficar verde".
- **Legenda de selos completa** nesta bibliografia: cinco selos, com o que cada um **prova** e
  o que **não** prova.
- **Reconferência mensal agendada** (`.github/workflows/reconfere-fontes.yml`), que compara o
  travamento contra os registros e abre issue se divergir.
- **[ADR 0009](../adr/0009-portao-de-fontes-doi-inexistente.md)** e
  **[ADR 0010](../adr/0010-a-semantica-do-selo.md)**.

**A virada de enquadramento.** A pergunta "este DOI existe?" não é para o Crossref nem para o
OpenAlex — são índices de **metadados**, com cobertura parcial por construção. Existência é
decidida pelo *Handle System*. Com isso, "obra real não indexada" deixou de ser exceção a
negociar e virou estado **normal e aprovável**, e o caso restante — o registro nega o DOI —
não tem instância legítima, porque o reparo é apagar o identificador. **Não há lista de
exceções.**

**O que a rodada derrubou de si mesma.** O limiar de comparação de títulos entrou no plano como
"0,70, o mesmo que um guia externo documenta" — citação sem fonte nomeável. Medido, caiu duas
vezes: primeiro o extrator (o *regex* casava o **nome do autor em negrito** antes do título),
depois a própria ideia de limiar único (o pior par legítimo ficou **abaixo** do melhor
impostor). A correção foi de critério — contenção antes de bigramas — e o limiar medido é
**0,78**, com janela de 0,440.

**O portão apanhou o próprio defeito.** Na primeira execução, o parser leu 11 entradas onde havia
12, e a contagem independente reprovou. Causa: `\z` **não existe em regex de JavaScript** — é a
letra `z` literal, e o corpo da entrada terminava no primeiro `z` minúsculo. A entrada perdida
era a de Gill et al., cujo título contém "optimi**z**ation".

**A dívida que esta edição NÃO paga, dita em voz alta:** o portão cobre **12 das 31 obras** da
bibliografia — 39%. Livro impresso, página institucional, curso gravado e identificador do arXiv
continuam sendo afirmação humana — e **o incidente que motivou esta rodada, a URL de vídeo
inventada, continuaria passando por ela**. O item "Portão de URL externa" segue aberto no
[ROADMAP](../ROADMAP.md) e subiu de prioridade. Portão que cria confiança maior do que sua
cobertura é pior do que portão nenhum.

**Verificação:** build verde nos dois caminhos (`npm run build` e `SEM_PDF=1`), 24 testes do
tutor verdes, e **20 verificações destrutivas** — cada reprovação que o portão promete foi provada
quebrando-o de propósito.

**A revisão independente reprovou a primeira versão**, e cinco achados viraram correção mais
teste. O mais grave era o portão ficar verde tendo verificado nada quando os índices de metadados
caíssem: o canário só exercitava o registro. O mais simples, e o mais constrangedor: o portão
conferia o **texto** do link e não o **endereço** — trocar só o destino passava. E o número de
cobertura publicado estava errado: são 12 de **31 obras**, 39%, não "cerca de 25".

### Edição 0.15 — 2026-08-12 · As fórmulas nunca tinham sido renderizadas

**Defeito encontrado pelo autor, na página publicada.** O motor não tinha renderizador de
matemática **nenhum**. As fórmulas em `$...$` e `$$...$$` iam para o HTML como texto cru, e o
leitor via, literalmente:

```
$$ \begin{cases} x_1 + x_2 = 10 \ x_1 + 2x_2 = 12 \end{cases} $$
```

Não era configuração errada: a capacidade **nunca existiu**. Medido antes de corrigir — 17 blocos
e mais de 550 expressões em linha, em quatro capítulos no ar. O capítulo 09 era o mais atingido,
por ser o que mais usa notação.

**Entrou:** KaTeX no motor, com a folha de estilo e as fontes copiadas para `docs/`; e o portão
`verifica-matematica.mjs`, encadeado no `npm run build`.

**A lição, e ela vale além deste portão.** Os oito portões deste livro nasceram todos olhando
para o que se extrai do **Markdown** — seções, links, exercícios, ótimos, fontes. Nenhum olhava
para o **HTML gerado**, que é o artefato que chega ao leitor. Este é o primeiro. Foi preciso o
autor abrir a página e apontar, o que é a definição de portão que faltava.

**E uma segunda armadilha, encontrada porque o autor olhou a página de novo.** A primeira
correção usou o `markdown-it-katex`, de 2017, que carrega um **KaTeX 0.6.0 aninhado** no próprio
`node_modules`. A folha de estilo era copiada do KaTeX do topo, **0.18**. Marcação de 2016 servida
com estilo de 2024: os índices caíam abaixo da linha e o alinhamento colapsava. A fórmula
**renderizava, e renderizava errado** — pior do que não renderizar, porque parece conteúdo.

E o portão passou **verde** sobre isso, porque conferia que o arquivo CSS *existe*, não que ele
*corresponde* a quem renderizou.

Corrigido em três camadas:

1. plugin mantido (`@vscode/markdown-it-katex`), com **um KaTeX só** no projeto;
2. a folha de estilo é resolvida **do mesmo módulo que renderiza**, não de caminho fixo;
3. o portão passou a exigir que **toda classe estrutural emitida pelo renderizador esteja
   definida na folha publicada** — teste que pega divergência de versão sem comparar números.

> Nota de método: a primeira lista de classes do portão incluía `mord`, que o KaTeX emite e
> **não estiliza**. Falso vermelho. Cada classe foi conferida contra a folha antes de entrar —
> falso vermelho crônico é o que ensina a desligar portão.

**Verificação:** `✓ matemática OK: 1124 expressão(ões) renderizada(s) em 16 páginas, 0
delimitador cru`, com o portão provado quebrando-o de propósito **duas vezes** (delimitador cru e
folha de estilo de outra versão), e a página conferida **em navegador**: fonte `KaTeX_Main`
carregada, 0 erro de console, 0 requisição falha.

### Edição 0.16 — 2026-08-13 · Capítulo 12: dualidade, e o selo de maturidade

Primeiro capítulo do **lote 1 da v0** ([spec 009](https://github.com/GHDaru/operationalresearchaibook/blob/main/specs/009-lote1-parte2/spec.md)),
e a estreia da escada de maturidade decidida na [ADR 0013](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0013-o-que-e-a-v0.md).

**Entrou:**

- **[Capítulo 12 — Dualidade](capitulos/12-dualidade.md)**, em 🟡 **v0**. O problema irmão, os dois
  teoremas, as folgas complementares e a leitura do preço-sombra no quadro que o leitor já sabe
  montar. Três objetivos, três exercícios, um para um.
- **[Etapa 05 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-05-parte2)** —
  uma etapa por **Parte**, não por capítulo (ADR 0013, D3). Ela ancora o capítulo 12 e já ancora
  o 13.
- **Selo de maturidade** 🟡 v0 / 🔵 medido / ✅ verificado, no alto de cada capítulo e no
  [mapa](mapa-do-handbook.md), **verificado por máquina**.
- **Capacidade `dualidade`** no tutor, liberada no capítulo 12, com o espelho de exibição em
  sincronia.

**A verificação que sustenta o capítulo, e por que ela é chata de propósito.** Ler o preço-sombra
no quadro do primal é conveniente e **circular**: usa o mesmo cálculo para produzir e para
conferir. A etapa 05 monta o **dual como problema separado** e o resolve do zero. Os dois caminhos
chegam a **R$ 1.100**, e o script **encerra com erro** se não chegarem — o capítulo não pode ser
escrito com o experimento vermelho.

**O número que o capítulo existe para impedir.** Um preço-sombra citado sem a **faixa de
validade** custa, na instância do livro, **R$ 350 de prejuízo** numa compra em que *nenhuma conta
está errada*. É o erro caro da Parte II, e agora está medido, não advertido.

**O que este capítulo NÃO afirma.** A cena mais contada da área — von Neumann apontando a
dualidade a Dantzig em 1947 — foi procurada por identificador e **não localizada**. Fica `⏳`, dita
como atribuição corrente e não como história. A origem do nome "dual" neste campo fica `❌`.
Nenhuma das duas foi preenchida com invenção.

**Quitado:** o último `⏳` de vídeo do handbook. A duração do vídeo do capítulo 10 é **19min04s** —
e a leitura foi conferida contra um caso conhecido (o vídeo do capítulo 09, que devolve os mesmos
18min48s já registrados por outra via) antes de ser aceita.

**Verificação:** nove portões verdes — `✓ template verificado [pt]: 6 capítulos … maturidade 🟡1
🔵0 ✅4`, `✓ registro de exercícios OK: 30 exercícios em 5 baterias`, `✓ consistência de ótimo OK:
30 modelo(s) resolvido(s) em aritmética exata`. O portão de maturidade foi **provado quebrando**
nos quatro modos que ele promete pegar, incluindo o falso verde que importa: o sumário passar a
declarar um selo e a página continuar exibindo outro.

### Edição 0.17 — 2026-08-13 · A faixa estava errada, e o portão que faltava

Registro *append-only*: a edição 0.16 publicou o capítulo 12 com **duas faixas de validade
erradas**. Esta edição as corrige e, mais importante, constrói o portão que teria impedido.

**O que estava errado.** A faixa em que o preço-sombra vale saía de uma varredura do estoque de
meio em meio. O defeito não é de precisão, é de definição: a varredura mede **em que base o
Simplex aterrissa**, não **para que estoque a base continua ótima**. Na fronteira o vértice fica
degenerado, o método aterrissa em outra base equivalente, e a varredura lê "mudou" um passo antes
da hora.

| Recurso | Publicado na 0.16 | Correto |
|---|---|---|
| CPUs | de 6,5 a 12 | **de 6 a 12** |
| pentes de 16 GB | de 10 a 19,5 | **de 10 a 20** |

O que torna o defeito pior do que dois números: **o teto 12 saiu certo, por sorte de desempate**.
Um método que erra um lado e acerta o outro sem avisar não é medição.

**O que mudou na medição.** A faixa passa a sair de **álgebra exata** sobre o quadro final — com
todas as restrições `<=`, as colunas de folga são $B^{-1}$ — e é **conferida por um segundo
caminho**, que põe o estoque na fronteira e um pouco além e exige que o preço acerte na fronteira e
**erre** além dela. Faixa curta demais escapa de qualquer teste que só confira o valor certo.

**O portão que nasceu disto.** Era a **segunda vez** que um número entrava no livro sem portão — a
primeira foi o ótimo errado do `cap07.exC`, que produziu o `verifica-otimos.mjs`. Defeito de mesma
classe pela segunda vez é defeito do pipeline: a etapa 05 ganhou uma suíte que **lê o capítulo
publicado** e exige que cada número medido apareça no texto na forma exata — **e que as versões
antigas não apareçam**, porque um teste que só confere o valor certo passa verde num capítulo que
publica o certo e o errado em lugares diferentes.

**Entrou junto:** a **faixa dos coeficientes do objetivo** (`[75, 150]` para o Tipo 1 e
`[100, 200]` para o Tipo 2), que é a metade do relatório de sensibilidade que ainda não tinha
artefato e que o capítulo 13 vai precisar.

**Corrigido também:** o capítulo 12 afirmava em prosa que o *minimax* foi "publicado por von
Neumann em 1928" enquanto a sua própria tabela de Procedência marcava a afirmação `⏳`. Corpo
afirmando o que a tabela nega é o modo mais silencioso de um sistema de selos deixar de valer.

**O exercício C do capítulo 12 foi reescrito** e ficou melhor: com a faixa certa terminando em 20,
comprar 20 ou 24 pentes dá **o mesmo lucro** de R$ 1.500 — as 4 unidades finais valem exatamente
zero e são custo puro. A faixa de validade aparece como dinheiro, que é o que o exercício existe
para ensinar.

**A decisão está registrada** na [ADR 0014](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0014-relatorio-de-sensibilidade-e-a-faixa-medida.md),
com o comitê de três especialistas que a instruiu — e com o registro de que nenhuma recomendação
foi aceita sem reconferência própria.

**Verificação:** `8 passed` na etapa 05, nove portões verdes, `✓ consistência de ótimo OK: 30
modelo(s) resolvido(s) em aritmética exata`.

### Edição 0.18 — 2026-08-13 · Capítulo 77: como ler um artigo, antecipado de propósito

Segundo capítulo do lote 1, e o único fora da Parte II. **A antecipação é a decisão**: o capítulo
77 é barato de escrever, não tem método a medir, e dá a todo o resto do livro o direito de
**citar em vez de explicar**. Enquanto ele não existisse, cada capítulo que dissesse "as fontes
lidas mostram que X" estaria pedindo confiança; agora está apontando para um protocolo que o
leitor pode aplicar à mesma fonte.

**Entrou:** [capítulo 77](capitulos/77-ler-artigo.md), em 🟡 **v0**. Três passadas de custo
crescente com critério explícito de desistência, e — o que o torna de Pesquisa Operacional e não
um guia genérico — a **checklist da comparação computacional**: instâncias, *baseline* com versão,
critério de parada, máquina, semente e número de execuções, forma de medir qualidade,
disponibilidade de código e dados.

**Este capítulo não publica número nenhum**, e isso é declarado no corpo. Ele é protocolo.

**O que ele não afirma, e é o ponto mais delicado.** A ideia de organizar a leitura em passadas é
creditada a Keshav (2007), com selo `✓ᵐ`: **o identificador foi conferido e o texto não foi
aberto** — nenhuma via de acesso aberto o devolveu. Consequência assumida no desenho: o protocolo
publicado é **autoral**, escrito para artigos de PO, e o capítulo diz isso em vez de atribuir a
Keshav detalhes que não leu. A dívida fecha quando alguém com acesso institucional conferir o que
é dele e o que é adaptação — e o resultado pode ser **encolher** a seção.

**Cláusula de expiração**, porque o capítulo está na camada de fronteira: as três passadas não
expiram por conta própria; a checklist de comparação computacional e a afirmação sobre variação de
desempenho entre versões de solver são reverificadas **até 2028-08**.

**Portão ajustado, com medição antes.** O portão de consistência de ótimo usava a régua `[óo]tim`,
que num livro sobre **otimização** é falso vermelho esperando a hora: "código otimizado" disparava
o portão num exercício sem modelo. A régua foi estreitada para o substantivo (`ótimo/ótima/
ótimos/ótimas`). Medido sobre o registro inteiro **antes** de trocar: exatamente **um** exercício
sai da vigilância — o falso positivo — e nenhum outro é solto. Falso vermelho crônico é o que
ensina a desligar portão.

**Verificação:** nove portões verdes — `✓ registro de exercícios OK: 33 exercícios em 6 baterias`,
`✓ template verificado [pt]: 7 capítulos … maturidade 🟡2 🔵0 ✅4` —, `8 passed` na etapa 05 e
`24 passed` no backend.

### Edição 0.19 — 2026-08-13 · Capítulo 13: sensibilidade, e o preço que não é um número

Terceiro capítulo do lote 1, e o que paga a dívida que o capítulo 12 deixou por escrito: *"como
usar a faixa é o capítulo 13"*.

**Entrou:** [capítulo 13](capitulos/13-sensibilidade.md), em 🟡 **v0**, e a segunda metade da
etapa 05 do `po-zero`.

**O relatório de sensibilidade é de formato próprio**, por decisão registrada na
[ADR 0014](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0014-relatorio-de-sensibilidade-e-a-faixa-medida.md)
(D1). O relatório de um solver de mercado empilha **duas famílias de faixa com os mesmos rótulos** —
uma diz até onde o **plano** aguenta, a outra até onde o **preço** vale — e é essa fusão visual que
produz o erro caro. Aqui os dois blocos têm títulos que dizem o que cada faixa protege. Não há
imitação de layout de fornecedor: o Princípio IV proíbe que um objetivo declarado dependa de
produto licenciado.

**O preço ambíguo deixou de ser advertência e virou demonstração.** O capítulo 10 disse que em
vértice degenerado a leitura de preço-sombra fica ambígua e parou aí. Agora o handbook **exibe**:
a montadora mais uma restrição que não muda nada (a bancada de teste, que comporta os 8 do Tipo 1
que o plano já produz), a **mesma implementação**, e só a **ordem em que as restrições foram
digitadas** mudando:

| | CPUs | pentes | bancada |
|---|---:|---:|---:|
| ordem CPU, pente, bancada | 50 | 50 | 0 |
| ordem bancada, pente, CPU | 0 | 75 | 25 |

Os dois foram conferidos como **soluções viáveis do dual, de mesmo custo** — e o ponto médio
também. O dual não tem um ótimo: tem um **segmento** de ótimos. Medindo direto, `z(9) = 1050`,
`z(10) = 1100`, `z(11) = 1100`: perder uma CPU custa R$ 50 e ganhar uma CPU rende R$ 0. Não é que
um relatório esteja errado — é a pergunta "qual é *o* preço" que está mal feita.

**Achado do próprio teste, e ele virou uma frase no capítulo.** A faixa do lucro tem **três**
regimes, e o do meio quase nunca é escrito: estritamente dentro, o plano é o mesmo e é único;
**exatamente na fronteira**, ele continua ótimo mas **empata** com outro — em $c_1 = 75$, os planos
$(8,2)$ e $(0,6)$ rendem os dois R$ 900 —; fora, deixa de ser ótimo. O teste tinha sido escrito
exigindo igualdade de ponto na fronteira, e falhou. Estava errado o teste, e a correção rendeu
conteúdo.

**Verificação:** nove portões verdes — `✓ consistência de ótimo OK: 41 modelo(s) resolvido(s) em
aritmética exata`, `✓ registro de exercícios OK: 36 exercícios em 7 baterias`, `maturidade 🟡3 🔵0
✅4` —, `13 passed` na etapa 05 e `24 passed` no backend.

### Edição 0.20 — 2026-08-13 · Capítulo 38: convexidade, e a dívida do capítulo 09 paga

Quarto capítulo do lote 1, antecipado da Parte VI por dois motivos declarados: o
[capítulo 09](capitulos/09-simplex.md) usou a convexidade **a crédito** ao afirmar que "parar no
primeiro topo é seguro", e ~40 capítulos do mapa vão poder **apontar** para cá em vez de
reexplicar.

**Entrou:** [capítulo 38](capitulos/38-convexidade.md), em 🟡 **v0** e curto por desenho, mais a
[etapa 06 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-06-convexidade).

**A assimetria do teste, medida.** O teste do ponto médio percorreu **12.561** pares na região da
montadora sem achar contraexemplo — e isso **não prova** convexidade, porque nenhuma amostragem
prova. Na região com "fornecedor A **ou** B", **15** pares bastaram para provar a **não**
convexidade, porque um contraexemplo é uma prova completa. O capítulo publica os dois vereditos
com palavras diferentes de propósito.

**O ótimo local, exibido em vez de advertido.** Mesma região não convexa, mesmo objetivo, duas
partidas: a busca local para em $(2,8)$ com margem **22** e em $(10,0)$ com margem **30**. A busca
é honesta — só aceita vizinho viável e melhor —, e em $(2,8)$ **nenhum vizinho é melhor**. Não
houve erro, nem aviso, nem bandeira: o que estava errado era supor que aquilo bastava.

**A não convexidade entrou pela porta da frente.** A regra que a produz é banal e está escrita em
português: *compre pelo menos 6 de A **ou** pelo menos 8 de B*. Todo "ou" é uma união de regiões, e
união de convexos quase nunca é convexa.

**Um portão declarou o que não alcança.** O portão de consistência de ótimo enumera vértices de
interseções de semiespaços — é, por construção, uma máquina de conjuntos **convexos**. Um exercício
sobre região não convexa é exatamente o que ele não consegue conferir. Os três exercícios do
capítulo 38 entraram na lista de isenção **com justificativa**, e a isenção **aponta para onde a
conferência acontece**; um teste da etapa 06 verifica que a isenção e o apontamento continuam lá.
Nenhum número do handbook fica sem dono.

**Armadilha de idioma, consertada na configuração.** O padrão do pytest coleta como teste qualquer
função cujo nome comece com `test` — **sem** o sublinhado. Num repositório em português isso
significa que `teste_do_ponto_medio` era coletada e falhava com "fixture não encontrada": falso
vermelho vindo do nome, não do código. Exigir o sublinhado resolve a classe inteira, e proteger as
próximas funções vale mais do que renomear esta.

**Verificação:** nove portões verdes — `maturidade 🟡4 🔵0 ✅4`, `39 exercícios em 8 baterias`,
`41 modelo(s) resolvido(s) em aritmética exata` —, `19 passed` no `po-zero` e `24 passed` no
backend.

### Edição 0.21 — 2026-08-13 · Capítulo 14: atravessar em vez de contornar

Quinto capítulo do lote 1. Fecha a família de métodos da Parte II e resolve um incômodo que os
capítulos 08 a 13 deixaram no ar: se o ótimo está numa quina, por que um método que **evita** as
quinas é competitivo — e por que a resposta que ele entrega **não é uma quina**?

**Entrou:** [capítulo 14](capitulos/14-pontos-interiores.md), em 🟡 **v0**, e a
[etapa 07 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-07-pontos-interiores),
com escalonamento afim.

**A reconciliação com o capítulo 08**, que é o ponto conceitual: o teorema afirma que **existe** um
ótimo num vértice. Ele **não** afirma que o método precisa andar pelos vértices para achá-lo — um
é um fato sobre onde a resposta mora, o outro seria um fato sobre como chegar lá, e não está no
teorema.

**Ponto flutuante, declarado.** É a primeira etapa do handbook que **não pode** usar aritmética
exata, e o motivo é de natureza: método interior é iterativo e converge a um **limite**. Isso vira
conteúdo em vez de rodapé:

```
Simplex (fração exata):     ponto (8, 2)                 valor 1100        2 pivôs
interior (ponto flutuante): ponto [7.999996, 2.000002]   valor 1099.99982  11 iterações
distância ao vértice: 4.472e-06 · erro no valor: 1.800e-04
```

**O Simplex chega; este se aproxima.** A distância de $4{,}5 \times 10^{-6}$ não é defeito de
implementação — apertar a tolerância a diminui, e zerá-la é impossível.

**Onde os dois métodos discordam, e ambos acertam.** Na marcenaria do capítulo 10, cujo ótimo é um
**segmento** entre $(4,0)$ e $(2,3)$, o Simplex devolve uma das quinas e o método interior devolve
$(2{,}928;\ 1{,}608)$ — **no meio da face ótima**, valendo os mesmos 24. Há teste que verifica que
o ponto está sobre o segmento e **estritamente entre as pontas**: parar colado numa ponta não teria
lição a extrair.

**O que o capítulo recusa afirmar.** Nenhuma comparação de desempenho do tipo "ponto interior ganha
acima de $N$ variáveis" — seria exatamente a comparação sem instância, *baseline* e máquina que o
[capítulo 77](capitulos/77-ler-artigo.md) ensina a recusar. A afirmação corrente de que o método do
elipsoide "perdia na prática" entra como `⏳` **do campo**, não como resultado próprio.

**Defeito encontrado e corrigido durante a construção**, do tipo que vale registrar: a primeira
versão do critério de parada declarava `ilimitado` quando nenhuma componente da direção era
negativa — raciocínio correto em teoria e errado na prática, porque é exatamente o que acontece
**perto do ótimo**. O método convergia e a função dizia "ilimitado". O critério certo é o resíduo
reescalado; detectar ilimitado não é trabalho desta etapa.

**Verificação:** nove portões verdes — `maturidade 🟡5 🔵0 ✅4`, `42 exercícios em 9 baterias`,
`42 modelo(s) resolvido(s) em aritmética exata` —, `26 passed` no `po-zero` e `24 passed` no
backend.

### Edição 0.22 — 2026-08-13 · Capítulo 15: os quatro padrões, e o erro que não avisa

Último capítulo 🟡 do lote 1, e o que **fecha a Parte II** — resta o capítulo 11, que tem spec e
medição próprias.

**Entrou:** [capítulo 15](capitulos/15-modelagem-aplicada.md), em 🟡 **v0**, e a
[etapa 08 do `po-zero`](https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero/etapa-08-modelagem),
que resolve mistura, transporte e cobertura com o **mesmo Simplex da etapa 03** — sem uma linha de
método novo, porque a tese do capítulo é que o repertório é de **formulação**. Há teste que
verifica isso: se a etapa passar a importar solver externo, ele quebra.

**O erro mais silencioso do livro.** Todos os anteriores tinham sintoma — `Infeasible` avisa,
`Unbounded` avisa, ciclagem trava, preço fora da faixa dá prejuízo. **Padrão errado não avisa
nada.** Medido: a mesma situação de distribuição custa **R$ 365** modelada como transporte e
**R$ 403,33** modelada como mix de produção com custo médio de frete — `Optimal` nos dois.

E o dano maior não é a diferença de 10,5%: o modelo errado tem **duas variáveis**, uma por fábrica,
e portanto **não diz quanto vai para cada centro**. A informação não está imprecisa — ela não
existe. A perda aconteceu na escolha da variável de decisão, e o custo médio foi consequência, não
causa.

**A porta de entrada da programação inteira, medida.** A cobertura relaxada para contínua devolve
`['1/2','1/2','1/2','1/2']` ao custo **9**; a decisão executável mais barata, obtida por
**enumeração dos 16 subconjuntos**, é abrir as estações 2 e 3 ao custo **10**. A relaxação é um
limitante inferior que **não se alcança**, e o buraco de 1 é exatamente o que a Parte de
programação inteira existe para fechar.

**Um alcance de portão, declarado em vez de descoberto depois.** O `verifica-otimos.mjs` não pegou
os números deste capítulo, e não por estarem certos: ele só resolve modelos de **duas** variáveis
(o transporte tem seis) e só inspeciona rubricas que contenham a palavra "ótimo" (as deste capítulo
afirmam custos sem usá-la). Isso não é defeito — é o alcance dele. O controle compensatório é o
teste da etapa 08, que confere o capítulo **e** a rubrica, e que declara no próprio cabeçalho qual
buraco está fechando.

**Verificação:** nove portões verdes — `maturidade 🟡6 🔵0 ✅4`, `45 exercícios em 10 baterias` —,
`32 passed` no `po-zero` e `24 passed` no backend.

### Edição 0.23 — 2026-08-13 · Capítulo 11: a medição que contraria o folclore

**Fecha a Parte II** e fecha o lote 1 da v0. É o único capítulo 🔵 **medido** do lote — todo número
dele se regenera por experimento; falta a revisão independente para ✅.

**Entrou:** [capítulo 11](capitulos/11-simplex-revisado.md) e a segunda metade da etapa 05, com o
desenho da [ADR 0012](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0012-o-desenho-da-medicao-do-capitulo-11.md)
marcado no código decisão por decisão (D1…D8).

**O resultado contraria o que se costuma dizer, e entra assim.** A forma revisada ganha nas
instâncias densas, com vantagem crescente em $n/m$ — **1,27× · 1,87× · 2,96×** — e **perde** em duas
das três esparsas (**0,94×** e **0,75×**). A spec da rodada tinha se comprometido com isso antes de
medir: *o livro não afirma ganho que o experimento não mostrar*.

**E a explicação foi medida, não contada:** o **preenchimento**. Na "média esparsa" o quadro salta
de 0,27 para 0,41 de densidade ao pivotear, fica caro de manter, e a revisada ganha; na "magra
esparsa" ele quase não preenche (0,13 → 0,20), continua barato, e a revisada perde. A troca real é
*manter tudo para poder ler* contra *não manter nada e recalcular*, e qual sai mais barato depende
da instância.

**Três garantias tornam o resultado inesperado acreditável**, e sem elas ele seria só suspeita de
bug: concordância com a etapa 03 (publicada e **intocada**) como árbitro; **mesma trajetória de
pivô** nas duas formas, provada em toda instância; e seis instâncias **congeladas antes** da
primeira execução, com todas publicadas.

**Dois resultados negativos, publicados como resultado.**

1. **Nenhuma instância estagna** pelo limiar pré-declarado de 3 iterações consecutivas sem melhora
   — nem a aleatória (veredito: *lentidão*), nem uma deliberadamente degenerada com cinco
   restrições sobre o mesmo vértice. **O limiar não foi baixado** para o exemplo caber: baixá-lo
   depois de ver o resultado é ajustar até ficar verde.
2. **O ponto flutuante não mudou o veredito**: erro relativo de $1{,}1 \times 10^{-16}$, mesma base,
   mesmas 30 iterações. E a lição está em **por que a base foi comparada separada do valor** — erro
   pequeno no número não garante o mesmo plano.

Os três negativos estão **asseverados em teste**. Se um dia a implementação mudar e a revisada
passar a ganhar sempre, a suíte fica vermelha — o capítulo teria de ser reescrito, não
silenciosamente corrigido.

**Critérios da spec 008 medidos:** `wc -l` = **362** linhas contra o teto de 722 (A12); blocos de
mecânica em **28,2%** das linhas contra o teto de 50% (A13); **cinco** exercícios, um por objetivo
(A18); a caixa que fecha a ponte — *"solver nenhum faz isso"* — publicada (A16); e o verbete
**custo reduzido** do glossário ganhou a leitura por preço, $c_j - y^{\top}a_j$ (A17).

**Verificação:** nove portões verdes — `maturidade 🟡6 🔵1 ✅4`, `50 exercícios em 11 baterias` —,
`40 passed` no `po-zero` e `24 passed` no backend.

### Edição 0.24 — 2026-08-13 · A revisão do lote reprovou, e o que ela pegou

A revisão em contexto fresco do lote 1 — feita por quem não escreveu nada dele, lendo **seguindo o
fio** e não capítulo a capítulo — **reprovou**. Não pelo conteúdo: as sete medições se regeneram
exatamente como publicadas. Reprovou a **costura**, e num padrão que vale registrar.

**O defeito que voltou dentro do mesmo lote.** A edição 0.17 corrigiu, no capítulo 12, o corpo
afirmando o que a tabela de Procedência marcava `⏳` — e escreveu que *"corpo afirmando o que a
tabela nega é o modo mais silencioso de um sistema de selos deixar de valer"*. O capítulo 14, do
mesmo lote, fazia exatamente isso três vezes: afirmava que o método do elipsoide "perdia feio", que
Karmarkar "mudou o mercado" e que a família interior "é a escolha usual do mercado" — tudo com a
Procedência marcando `⏳` ou sem linha nenhuma. **Corrigido**: as três viraram atribuição explícita,
e a tabela de viradas ganhou uma coluna `⏳` que separa o que foi medido do que se repete.

**Junto, uma data ganhou honestidade.** O capítulo ensinava "1979" cinco vezes para Khachiyan,
enquanto o único identificador conferido é o da publicação de **1980**. O capítulo agora publica as
duas e **não reconcilia** — diz o que tem conferido e marca o resto.

**O capítulo 11 exagerava o próprio resultado negativo.** Escrevia *"nas esparsas ela perde, ou
quase: 0,94×, 1,34× e 0,75×"* — e 1,34× é **vitória**, a segunda maior de todas. Num capítulo cujo
argumento é "não suavizamos resultado negativo", inflar um negativo é a mesma falha espelhada.
Corrigido para **duas das três**, com a régua certa dita em seguida: não existe regra por
esparsidade, a régua é o **preenchimento**.

**Três elos do fio não existiam.** O 12 mandava o leitor ao **mapa** para o capítulo 13, publicado
no mesmo lote; o 14 dizia que o 11 "**fará** caber em memória", no futuro, sobre o capítulo mais
maduro do lote; e o 38 pagava a dívida de convexidade do 09 sem que o 09 soubesse — o leitor que
segue a ordem nunca era avisado. Os três foram ligados.

**O README da etapa 05 ainda publicava as faixas erradas.** A correção da edição 0.17 tocou o
script, o capítulo, os resultados e os testes — e não o README, que é a primeira tela de quem segue
o link dos capítulos 12 e 13. Corrigido, com o defeito registrado nele.

**Oito fichas de vídeo, uma registrada.** A Videoteca declara ser mantida à mão, *"quem adiciona um
vídeo atualiza os dois lugares"* — e o lote registrou uma das oito. As sete faltantes entraram, com
o registro de **por qual via** título, autoria e duração foram lidos.

**Dois portões novos, porque as duas falhas eram invisíveis aos nove existentes.** Um barra
capítulo publicado que aponte para o mapa quando o capítulo-alvo **já existe** — legítimo enquanto
a vaga é vaga, defeito no instante em que ela é preenchida, e ninguém volta para trocar o link. O
outro exige que toda ficha `## Assista` esteja no índice da Videoteca. **Os dois foram provados
quebrando** antes de entrar.

**Fica para o autor**, porque não é trabalho de agente: a revisão apontou que o ✅ do capítulo 09
não tem registro da revisão em contexto fresco que a ADR 0013 usa para definir o selo — o
`specs/004-cap09-simplex/verificacao.md` marca `⏳ pendente`. Ou o 09 recebe a revisão, ou o selo
cai para 🔵. Importa duplamente porque o teto do portão de razão é `3 × ✅`.

**Verificação:** nove portões verdes com os dois novos incluídos, `40 passed` no `po-zero`,
`24 passed` no backend.

### Edição 0.25 — 2026-08-13 · O capítulo 09 perde o ✅, e o que a revisão achou junto

A revisão em contexto fresco que faltava ao capítulo 09 foi feita — e **rebaixou o selo para 🔵**.
O capítulo é genuinamente medido: todo número publicado sai da etapa 03, reproduz com o mesmo
`md5` e concorda com o HiGHS por **veredito**, não só por ponto. O que ele não tinha era a revisão
que o ✅ promete, e ela achou defeitos em conteúdo **publicado**.

**Duas afirmações que o próprio livro desmente com medição.** A caixa da garantia dizia que trocar
a regra de pivoteamento *"muda quantas iterações o método gasta — nunca **onde** ele termina"*, e o
[capítulo 10](capitulos/10-casos-especiais.md) mede o contrário: com múltiplos ótimos, Dantzig para
num plano e Bland em outro. Dizia também que *"enquanto houver custo reduzido negativo, existe
vértice melhor"* — falso sob degenerescência, e se fosse verdade a ciclagem de período 6 que o
capítulo 10 exibe não poderia existir. **Corrigido**: a garantia agora afirma o que sobrevive — o
**valor** ótimo não muda — e as duas qualificações apontam para onde foram medidas.

**Uma fórmula errada na primeira tabela do capítulo.** *"Um modelo em forma padrão com $n$
variáveis e $m$ restrições tem $\binom{n+m}{m}$ bases"* — em forma padrão com $n$ variáveis são
$\binom{n}{m}$. O enunciado agora diz o que o script calcula e o que o exercício A já cobrava
corretamente: $n$ variáveis de decisão **mais** $m$ folgas.

**A terceira reincidência do mesmo defeito.** O corpo afirmava como fato a cena de Motzkin
batizando o método, enquanto a tabela de procedência do mesmo capítulo marcava `⏳`. É o defeito
que apareceu no 12, voltou no 14 e agora aparece no 09 — em conteúdo publicado há mais tempo.
Corrigido, e com a lição preservada de um jeito que **não depende da atribuição**: o método não
manipula simplex nenhum, e isso se verifica lendo o algoritmo.

**Dois erros menores de história, em afirmações seladas `✓`:** o economista é **T. C.** Koopmans, e
a inicial errada veio da própria fonte consultada, propagada sem conferência; e a frase *"um mês
antes de a Força Aérea existir"* estava mais forte do que a fonte, que ancora o mês ao *National
Security Act* de 26/07/1947 — a Força Aérea só existe como ramo em 18/09. **A fonte estava `✓` e a
paráfrase excedia o que ela cobria**, o que é um modo de errar que o selo não pega.

**Dívida declarada, junto:** o capítulo maximiza do início ao fim e nunca instalava a convenção de
minimização — que o exercício H cobrava. A convenção entrou; o tratamento próprio de minimização,
inclusive o que muda no *big-M*, fica declarado como dívida.

**Efeito no freio, e ele é o ponto.** O handbook fica em **🟡7 · 🔵2 · ✅3**, e o teto do portão de
razão cai de 12 para **9**. Restam **duas** vagas 🟡 antes de o build ficar vermelho — o lote da
Parte I, planejado com seis capítulos, **não cabe mais**. É exatamente o que a ADR 0013 D2 queria
que acontecesse: um ✅ que não se sustentava estava afrouxando o freio com dado próprio.

### Edição 0.26 — 2026-08-13 · O selo passa a exigir evidência, e cinco capítulos sobem

A revisão do capítulo 09 mostrou o que acontece quando um selo não tem evidência atrás: ele
afrouxa o freio com dado próprio. A resposta não foi rebaixar aquele capítulo e seguir — foi tirar
do humano a decisão sobre o selo, do mesmo jeito que o `verifica-otimos.mjs` tirou do humano a
conferência de aritmética.

**O que o portão passou a exigir.** A ADR 0013 D2 define 🔵 como *"🟡 mais experimento no `po-zero`
que regenera cada número"*. A evidência mais forte que este repositório sabe produzir disso é o
**teste que lê o arquivo do capítulo** — o vínculo criado na rodada 009, depois de duas faixas
erradas terem sido publicadas. Ele quebra quando a medição muda e o texto não, **e vice-versa**.

Agora: capítulo declarado 🔵 ou ✅ **sem** teste que o leia falha o build; e capítulo declarado 🟡
**com** teste que o leia também falha, porque o selo está abaixo do que a evidência sustenta.

**Cinco capítulos subiram, e quem decidiu foi o portão.** Ao instalar a regra, o build acusou
`12-dualidade`, `13-sensibilidade`, `14-pontos-interiores`, `15-modelagem-aplicada` e
`38-convexidade` como declarados 🟡 tendo evidência de 🔵. Não houve auto-avaliação: a lista saiu da
medição.

**Dívida declarada, retroativa de propósito.** Os capítulos 07 a 10 foram medidos **antes** de o
vínculo automático existir — têm `experimento.py`, `resultados.json` e reprodutibilidade por `md5`
conferida à mão. Fingir que o vínculo existe seria mentir; rebaixá-los por uma prática que não
existia quando foram escritos apagaria medição real. Entram em `SEM_VINCULO_AUTOMATICO`, em código,
e **cada entrada é trabalho pendente, não isenção permanente** — o portão avisa quando uma delas
for quitada e alguém esquecer de tirá-la da lista.

**Estado:** 🟡2 · 🔵7 · ✅3. O teto do portão de razão é 9 e há 2 capítulos em 🟡 — o lote da Parte I
volta a caber, com folga de cinco vagas.

**Provado quebrando** nos dois sentidos antes de entrar.

### Edição 0.27 — 2026-08-13 · O portão da procedência, e o que ele não pega

O defeito "o corpo afirma o que a tabela nega" apareceu **quatro** vezes, em quatro capítulos —
12, 14, 09 e agora **08**, encontrado por este portão. Prometer atenção não conserta padrão que
reincide, então ele virou código.

**O que ele mede.** Para cada linha `⏳`/`❌` da tabela de Procedência, extrai os termos que carregam
a afirmação — nomes próprios e anos. Se um deles aparece no corpo, exige **ressalva por perto**.

**A calibração mudou a regra, e a mudança importa.** A primeira versão exigia o glifo `⏳` e acusou
o capítulo 10 por dizer *"costuma ser atribuída a Beale (1955)"* — que é exatamente a ressalva que a
constituição pede, escrita em português em vez de em símbolo. Exigir o glifo seria exigir
formatação, e portão que persegue formatação treina quem escreve a satisfazê-lo em vez de a pensar.
O portão passou a procurar a **marca de atribuição**, no glifo ou na prosa.

**Uma limitação declarada, e ela é do parser, não do texto.** Linha de estado **misto** —
`✓ᵐ metadados; ⏳ enunciado exato` — fica fora do alcance: o portão não sabe a que metade da célula
cada termo pertence, e chutar produziria o falso vermelho que ele existe para não produzir. Duas
linhas do handbook estão nesse caso, e elas continuam sendo leitura humana.

**O defeito real que ele achou:** o capítulo 08 — que carrega selo ✅ — afirmava como fato a
redescoberta de Fourier–Motzkin em 1936 e a cena da conversa com Dantzig, com as duas marcadas `⏳`
na própria tabela. Corrigido, e com a lição preservada de um jeito que não depende da atribuição.

**O QUE ELE NÃO PEGA, medido e dito.** Ele cobre a forma **grosseira** — termo sem ressalva
nenhuma por perto. Não cobre o termo ressalvado num lugar e afirmado em outro, que é o caso
original do capítulo 12: removendo a ressalva de lá, o portão continua verde. A régua estrita foi
medida e acusou "Karmarkar" num capítulo que trata de Karmarkar do início ao fim — troca um buraco
por falso vermelho crônico. **Proximidade não decide se uma frase afirma**, e o resto continua
sendo leitura humana. O ganho real é outro: o padrão tem nome, tem quatro ocorrências documentadas,
e entra na instrução de toda revisão em contexto fresco.

### Edição 0.28 — 2026-08-13 · Os cadernos entram, e entram sem poder derivar

O autor acrescentou os **cadernos Colab** ao escopo da v0. Decisão de médio impacto pela régua da
skill `longrun`: foi a comitê de três lentes, cada recomendação foi reconferida por medição
própria, e o resultado está na
[ADR 0016](https://github.com/GHDaru/operationalresearchaibook/blob/main/adr/0016-cadernos-colab-sem-deriva.md).

**A decisão central:** o caderno é **invólucro que importa o script**, nunca cópia. O `.py` é a
fonte única; o caderno clona o repositório, importa o módulo e chama funções — e **`def` e `class`
são proibidos nas células**. Uma cópia em caderno da função que publicou `13/2` ainda estaria
exibindo o número errado hoje, com ar de autoridade.

**A alternativa que parecia melhor foi testada e quebra.** Gerar o caderno a partir do `.py` por
conversor falha em `NameError: name '__file__' is not defined` — os módulos resolvem caminho por
`Path(__file__)`, que não existe num caderno. Consertar exigiria refatorar seis módulos, contra o
pedido explícito de simplicidade.

**Saída gravada no `.ipynb` é defeito, não conveniência.** Uma célula com saída salva é número
publicado **fora de qualquer portão** — a classe de defeito das duas faixas erradas, ressuscitada
num artefato que o build não olha. O caderno é commitado limpo, e o teste falha se não estiver.

**O caderno faz o que a página não faz**, ou não vale existir: uma célula **"mexa aqui"** e **o
erro rodado antes da correção**. No livro, o certo e o errado aparecem lado a lado e o leitor nunca
chega a errar; no caderno ele roda o telefonema, se compromete com uma conclusão, e **só então** vê
o prejuízo de R$ 350 aparecer. É o exercício `diagnosticar` encenado.

**Sete testes por caderno**, sem Jupyter e sem rede: `.ipynb` é JSON, e o clone vira um atalho para
a árvore de trabalho — então o caderno roda contra o código de **hoje**, não o publicado. O
sétimo é o que eu ia esquecer: **caderno órfão falha**. Ele pegou este na primeira execução.

**E o comitê achou um buraco maior que a decisão:** o CI **nunca rodou** os testes do `po-zero`. O
filtro `paths:` não incluía o diretório e não havia passo que os executasse — as seis suítes que
sustentam o selo 🔵 nunca tinham rodado lá. Consertado **antes** do primeiro caderno, porque
acrescentar artefato novo a um pipeline que não cobre o antigo é multiplicar o buraco.

**Dívida quitada de quebra:** o `po-zero/README.md` ainda dizia "Uma etapa por capítulo de
método", contradizendo a ADR 0013 D3, que mudou a unidade para a **Parte**.

> **Nota de método, porque o episódio é instrutivo.** A primeira tentativa de corrigir usou a
> frase que o parecer citou, em minúscula, e substituiu **zero** ocorrências — o texto real começa
> com maiúscula. O `replace` silencioso teria passado despercebido se o script não imprimisse a
> contagem, e esta edição já estaria publicando "dívida quitada" com a dívida intacta. **Toda
> substituição deste repositório imprime quantas casou**, e é por isso.

### Edição 0.29 — 2026-08-13 · A Parte I começa: o que é PO, e o ciclo que a sustenta

Com a Programação Linear (PL) publicada, a Parte I passa a ser escrita — **nesta ordem de
propósito**, que é a inversão declarada no [Roadmap](../ROADMAP.md). O capítulo 01 não promete o
que o campo entrega: ele **presta contas** do que já foi medido nas etapas do `po-zero` e
publicado nos capítulos 07 a 15. Um capítulo de abertura escrito antes teria feito a promessa
sem ter como cumpri-la.

**Entrou:**

- **[Capítulo 01 — O que é Pesquisa Operacional](capitulos/01-o-que-e-po.md)**, 🟡 v0. As quatro
  perguntas que decidem se um problema é de PO — há alavanca? há medida única? há restrição? dá
  para dizer o que a resposta **não** autoriza? — e o exercício de julgar um caso publicado por
  elas.
- **[Capítulo 02 — O ciclo de modelagem](capitulos/02-ciclo-de-modelagem.md)**, 🟡 v0. As cinco
  etapas e o entregável de cada uma, com a etapa 4 — validação — tratada como a mais pulada. O
  sintoma que o capítulo ensina a reconhecer é sempre o mesmo: **o modelo nunca errou**, não por
  ser bom, mas porque ninguém deu a ele a chance de errar.
- **Seis exercícios** e **dois vídeos**, um por capítulo. O do capítulo 01 estreia — enfim — o
  canal de **João Sarubbi** (CEFET-MG), que é a fonte curada primária desta Videoteca desde a
  rodada de fundação e que nunca tinha sido usada.
- **Duas capacidades no tutor**, `o_que_e_po` (libera 1) e `ciclo_modelagem` (libera 2). A
  segunda cobra sempre a mesma pergunta antes de ajudar a formular qualquer coisa: **quem vai
  decidir diferente por causa disto?**

**O que o portão pegou, e vale registrar.** O capítulo 02 nasceu com a seção intitulada *"Quando
não modelar"*. Está substantivamente certa — cinco casos em que modelar é a resposta errada —, e
mesmo assim **o build falhou**: o Princípio II é não-negociável e o portão procura a seção pelo
nome. Renomear para *"Quando não serve — quando não modelar"* não é burocracia satisfeita: é o
capítulo assumindo que **o ciclo também é um método**, e que a régua que ele aplica ao Simplex se
aplica a ele mesmo.

**A dívida que os dois capítulos declaram, e não disfarçam:** a origem do ciclo em cinco etapas,
`❌` procurada e não localizada em fonte primária; e a afirmação corrente de que projetos de PO
fracassam mais por definição e adoção do que por método — `⏳`, **não medida aqui e não citada de
memória**. Os dois capítulos nascem 🟡 porque nenhum dos dois produz número próprio: os que
aparecem são citação dos capítulos que os mediram, com teste que compara o texto publicado à
medição.

### Edição 0.30 — 2026-08-13 · Capítulo 03: três das quatro peças erram em silêncio

**Entrou:** o [capítulo 03 — Anatomia de um modelo de otimização](capitulos/03-anatomia-do-modelo.md),
🟡 v0, com três exercícios, vídeo curado e a capacidade `anatomia_modelo` (libera 3) no tutor.

**O recorte, que não é o usual.** Um capítulo de anatomia costuma ser vocabulário: aqui está a
variável, aqui está o objetivo, aqui está a restrição. Este organiza as quatro peças **pelo erro
que cada uma produz**, porque a assimetria entre elas é o que vale ensinar:

> Três das quatro peças, quando erradas, produzem um modelo que roda e devolve `Optimal`. Só a
> restrição tem chance de gritar — e mesmo ela grita em apenas metade dos casos.

**O instrumento do capítulo é o teste da unidade**, que custa um minuto e pega o que o solver não
pega: unidade incoerente, coeficiente na escala errada, e a variável que virou parâmetro sem
ninguém notar.

**O exercício C ensina o limite do próprio instrumento.** Ele traz um modelo de transportadora que
**passa** no teste da unidade — todos os termos fecham em reais, todas as restrições fecham em
quilômetros — e ainda assim está errado: o quilometrado entrou como variável de decisão, e
quilometrado não é algo que alguém decide. Quem procurar o defeito na unidade não vai achar, e é
esse o ponto.

**E a rubrica desse exercício não ficou solta.** Ela afirma que o Simplex cola o quilometrado no
piso da malha, e o portão de ótimo não alcança a afirmação — ele só resolve modelos de duas
variáveis, e esse tem três. Em vez de isentar e seguir, a conferência foi para
`po-zero/etapa-01-formulacao/test_anatomia.py`, em aritmética exata, pelo mesmo Simplex da etapa 03
que sustenta os selos 🔵 da Parte II. **Um número novo não entra no handbook por um caminho novo.**

A medição trouxe um achado que a rubrica não tinha: com a variável errada, o modelo recomenda
**zero caminhões próprios** e 200 terceirizações. O dano do defeito, visível.

**O que o portão pegou desta vez:** o capítulo 01 apontava *"capítulo 03"* para o mapa do handbook,
e o capítulo 03 passou a existir. O portão de costura barrou o link obsoleto no mesmo build em que
a página nasceu — que é exatamente quando um link desses costuma passar despercebido.

**A dívida declarada:** o aperto histórico que produziu a forma comum de escrever modelos entra
`⏳`. A narrativa é estrutural e verificável no que existe hoje; **o que falta é a citação primária
que a date e a atribua**, e enquanto ela faltar a linha não muda de estado.

### Edição 0.31 — 2026-08-13 · Capítulo 04: a classe decide o que você pode prometer

**Entrou:** o [capítulo 04 — Classificação de problemas e escolha de método](capitulos/04-classificacao-e-escolha.md),
🟡 v0, com três exercícios, vídeo curado e a capacidade `classificacao` (libera 4) no tutor.

**O recorte.** Uma tabela de classes é a parte do assunto que se decora e não se usa. Este
capítulo troca o eixo da tabela: cada travessia é apresentada pela **garantia que ela destrói**, e
não pela técnica que ela exige.

> Sair do linear elimina a certeza de que o ótimo está numa quina. Exigir integralidade invalida o
> teorema do vértice. Admitir incerteza faz desaparecer *"a"* solução ótima. E sair da convexidade
> reduz `Optimal` a *"não achei nada melhor por aqui"* — a distância entre **22 e 30** que o
> capítulo 38 mediu.

**O capítulo fecha numa decisão de três, e não numa taxonomia:** o ótimo provado, o ótimo com
*gap* declarado, e "a melhor que encontrei". A do meio é a mais subestimada, e o exercício C
insiste nela: um *gap* de 1,8% é **teto**, não estimativa — o ganho real de continuar pode ser
zero, porque a solução em mãos pode já ser a ótima e faltar apenas a prova.

**Duas fontes novas, e as duas entram `✓ᵐ`.** Gomory (1958) e Land & Doig (1960) tiveram autor,
veículo, ano e página conferidos no Crossref; **o conteúdo não foi lido**. A atribuição do
*branch-and-bound* e a do método dos cortes ficam declaradas como **correntes** — na bibliografia
e no corpo do capítulo. O que é `✓` **lido** é o outro fio: o sentido militar de *programming*, a
expressão original de Dantzig e o batismo por Koopmans em 1948, todos do MacTutor.

> **O parser da bibliografia tinha um defeito, e foi o sobrenome Doig que o revelou.** A entrada de
> **LAND, A. H.; DOIG, A. G.** falhava com *"ano não extraível"* — com o ano no lugar de sempre. O
> extrator procurava o ano antes do link de DOI cortando o texto na primeira ocorrência das três
> letras `DOI`, e elas aparecem **dentro do sobrenome DOIG**. A correção não foi reescrever a
> entrada para agradar o portão: foi o portão parar de confundir nome próprio com marcador de
> campo. Um parser que falha por causa de um sobrenome falharia de novo, em silêncio, na próxima
> bibliografia.

### Edição 0.32 — 2026-08-13 · Capítulo 05: o pior caso existe, e não é frágil como se diz

**Entrou:** o [capítulo 05 — Complexidade computacional para quem modela](capitulos/05-complexidade.md),
🔵 **medido** — o primeiro capítulo da Parte I a nascer com experimento próprio —, com três
exercícios, vídeo curado e a capacidade `complexidade` (libera 5) no tutor. E, com ele, a etapa
`po-zero/parte-I-fundamentos`, a primeira criada já sob a regra de **uma etapa por Parte**
(ADR 0013, D3).

**A frase que o capítulo existe para desmontar** é dita por gente competente todo dia: *"esse
problema é NP-difícil, então vamos direto para uma heurística."* Ela parece rigor e é o contrário
— uma decisão de projeto tomada sem medir nada, com autoridade emprestada de um teorema que fala
de outra coisa. E o prejuízo é invisível: quem descarta o método exato descarta junto o
**limitante**, que era a única coisa capaz de dizer depois se a heurística ficou boa.

**Três medições, em aritmética exata.**

1. **O pior caso existe e é construído.** O cubo de Klee–Minty custa exatamente $2^n-1$ pivôs, de
   $n=2$ a $n=7$. Não é tendência: é o valor exato em todos os tamanhos medidos.
2. **A instância aleatória fica longe dele.** Mesmo tamanho, sem malícia: mediana de **2 a 7
   pivôs**, contra pior caso teórico de 31 a mais de um milhão.
3. **E o pior caso não é frágil** — que é o resultado desta edição.

**Sobre o terceiro, com todas as letras.** Circula junto com Klee–Minty a frase *"tudo bem, o pior
caso é frágil; qualquer perturbaçãozinha desmancha"*. Testar custa minutos, e a medição **não
sustenta a frase**: com $n=6$, perturbar a matriz de restrições em **0,1%, 1% ou 10% deixa os 63
pivôs absolutamente intactos**. Só em 25% (57 pivôs) e 50% (22) o caminho encurta — e aí a
instância já é honestamente outra instância.

> **O que a medição não autoriza concluir, e o capítulo diz isso em prosa:** ela **não** refuta a
> análise suavizada de Spielman & Teng (2004). Aquele teorema é assintótico, vale **em esperança**,
> supõe perturbação **gaussiana** e uma regra de pivoteamento específica — nenhuma das três
> condições vale na tabela. O que a medição refuta é a **leitura popular** do teorema. Há teste que
> falha se essa ressalva desaparecer numa revisão de estilo, porque sem ela o capítulo passaria a
> afirmar algo que a medição não sustenta, e nenhum outro portão pegaria.

**Três fontes novas, todas `✓ᵐ`:** Edmonds (1965), Cook (1971) e Karp (1972), com metadados
conferidos no Crossref e **conteúdo não lido**. As atribuições — critério polinomial, NP-completude,
lista de reduções — entram declaradas como **correntes**. O artigo original de Klee e Minty (1972)
**não tem DOI localizado** e fica como ponteiro: o handbook não depende dele, porque constrói e
mede o cubo.

**O que a nova etapa não reimplementa:** nem o Simplex nem o cubo. Os dois vêm da `etapa-03`, por
`sys.path`. Reimplementar criaria uma segunda fonte da verdade para números que o livro já
publicou no capítulo 09 — a classe de defeito que a ADR 0016 proíbe nos cadernos, e que não tem por
que ser tolerada entre etapas.

### Edição 0.33 — 2026-08-13 · Capítulo 06, e a Parte I fecha

**Entrou:** o [capítulo 06 — Ferramentas de trabalho](capitulos/06-ferramentas.md), 🔵 **medido**,
com três exercícios, vídeo curado e a capacidade `ferramentas` (libera 6). **Com ele a Parte I
fecha**: seis vagas declaradas na rodada de fundação, seis publicadas.

**Um capítulo de ferramenta é o mais fácil de escrever mal**, porque a tentação é entregar um
folheto — *instale isto, escreva assim*. O que impede aqui são três medições, e as três mudam o
modo de ler uma saída de solver.

1. **Com múltiplos ótimos, a ferramenta escolhe o seu plano.** Mesmo modelo, valor **10** nos
   três; o Simplex exato devolve **(6, 4)** e os dois solvers devolvem **(2, 8)**. Nenhum está
   errado — e é o **plano**, não o valor, que a fábrica executa na segunda-feira.
2. **Nenhum solver devolve a fração.** O ótimo da ração é **780/17**. O HiGHS reporta
   `45.88235294117647` (erro de 4,18 × 10⁻¹⁶) e o CBC reporta `45.882352` (erro de 9,41 × 10⁻⁷).
   Os dois estão certos e **discordam entre si** — o que não muda decisão nenhuma até alguém
   comparar duas saídas com `==`.
3. **Os vereditos concordam**, e isso também é resultado: `Unbounded` e `Infeasible` saem iguais
   nas três implementações. **`Infeasible` não se conserta trocando de solver.**

**E o capítulo encontrou um defeito ao ser escrito — o segundo do mesmo passo de CI.** A edição
0.28 registrou que os testes do `po-zero` nunca haviam rodado na integração contínua. O passo foi
criado, e **instalava `pytest` e `numpy` e mais nada** — enquanto `etapa-08-modelagem` importa
`pulp` direto e vários módulos de etapa o importam no topo. Ou seja: o passo criado para proteger
os selos 🔵 **também não podia passar**. A correção não foi remover a dependência, e sim declará-la
em `po-zero/requirements.txt` — **o mesmo arquivo que o capítulo 06 manda o leitor instalar**.

> **A regra que sai daí, e ela vale além deste repositório:** instrução de instalação que ninguém
> executa envelhece em silêncio. A do capítulo 06 é executada a cada envio, e quando quebrar o
> build fica vermelho. Há teste que falha se a CI deixar de instalar o arquivo que o capítulo cita.

**Duas fontes novas, ambas `✓ᵐ`:** Fourer, Gay & Kernighan (1990), a que se atribui a separação
entre modelo algébrico e dados; e Huangfu & Hall (2017), na origem do HiGHS. Metadados conferidos,
**conteúdo não lido**, atribuições declaradas correntes. A data do segundo é a da publicação
eletrônica — o fascículo impresso é de 2018, e a divergência é do registro: o portão de fontes
compara com o Crossref e barraria a outra escolha.

**Uma dependência de versão, assumida de propósito.** Os dígitos da tabela de ponto flutuante
mudam se o solver mudar, e o teste fica vermelho quando isso acontecer. É o comportamento certo —
o capítulo publica dígitos e diz a versão ao lado. O PuLP 3.3 já marca `PULP_CBC_CMD` como
descontinuado, com remoção anunciada para a 4.0: quando chegar, o teste avisa antes do leitor.

### Edição 0.34 — 2026-08-13 · O caderno da Parte I

**Entrou:** [`po-zero/cadernos/parte-I.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-I.ipynb),
o segundo caderno do handbook, sob as mesmas sete regras da ADR 0016 — invólucro que importa o
código publicado, sem `def`, sem saída gravada, sem magia do IPython, com célula "mexa aqui", com
erro rodado antes da correção, exibindo a fonte de uma função, e **executado de verdade** pelo
`pytest` contra o código de hoje.

**O erro que o leitor roda antes de ver o certo** é o melhor desta Parte. O caderno pergunta:
*"o cubo com $n=6$ custa 63 pivôs; perturbando a matriz em 1%, quantos sobram?"* O palpite quase
universal é "bem menos" — e a célula seguinte mostra **63**. No livro, o resultado aparece pronto
numa tabela e o leitor nunca chega a errar; no caderno ele se compromete com uma resposta e vê o
próprio palpite não acontecer.

**O caderno declara o que não tem.** Os capítulos 01 a 04 não aparecem, porque não produzem número
próprio — e dizer isso na primeira célula é mais honesto do que inventar código para eles.

Com isto, **a Parte I fecha inteira**: seis capítulos, dezoito exercícios, seis vídeos, duas
etapas de medição e um caderno.

### Edição 0.35 — 2026-08-13 · A revisão da Parte I reprovou, e o que ela pegou

A revisão em contexto fresco — três lentes independentes, nenhuma delas de quem escreveu — devolveu
a rodada. **Isto é o processo funcionando**, e o registro existe para que fique claro o que passou
despercebido a quem escreveu.

**O achado mais grave é meu, e saiu da reconferência por medição própria** que a skill `longrun`
exige antes de aceitar qualquer parecer. A revisão apontou que a tabela de perturbação do capítulo
05 não declarava quantas amostras usava, enquanto a tabela vizinha declarava "20 amostras por
tamanho". Ao medir, a assimetria virou defeito:

> A tabela era **um sorteio por magnitude**. Medida sobre 20 sementes, a linha de 10% deixou de ser
> **63 pivôs** e virou **14 de 20** — o caminho às vezes encurta. O resultado central sobreviveu
> intacto (0,1% e 1% não mexem em nada, em **20 de 20**), mas a linha que o exagerava, não.

A correção troca o sorteio pela distribuição: a tabela publica mínimo, mediana, máximo e **em
quantas amostras o caminho ficou intacto**, e o teste passou a asserir a distribuição, não o
sorteio. **Um teste que confere um sorteio herda a fragilidade do sorteio.**

**O segundo achado é de firmeza, e é o defeito reincidente deste repositório.** Em três lugares o
corpo do texto afirmava com mais convicção do que a tabela de procedência autoriza: Gomory e Land &
Doig no capítulo 04, Cook e Karp no capítulo 05, a AMPL no capítulo 06 — todos `✓ᵐ`, com **conteúdo
não lido**. A tabela dizia certo; o corpo, não. E a prova de que era lapso e não convenção estava
no mesmo capítulo 05, que hedgeia Edmonds corretamente três parágrafos antes. **O hedge tem de
estar na frase, e não vinte linhas adiante**, porque é na frase que o leitor forma a crença.

**O terceiro é um erro conceitual que eu repeti em quatro superfícies.** O capítulo 04 dizia que
`Optimal` num modelo não convexo significa *"não achei nada melhor por aqui"*. **Está errado**, e o
próprio capítulo o desmente no corpo: um modelo inteiro é não convexo e o `Optimal` de um
*branch-and-bound* é **prova**, porque o método fecha a distância por limitante. A regra correta é
mais curta e não tem exceção:

> **`Optimal` só é prova quando vem com limitante.**

**O quarto: um `Optimal` que a medição nunca produziu.** Os capítulos 01, 02 e 04 contavam o 22
contra 30 do capítulo 38 como um solver que escreveu `Optimal`. O experimento é uma **busca local
em aritmética exata** — não há status, não há solver, e o próprio capítulo 38 diz que *"nenhum
erro, nenhum aviso, nenhuma bandeira"* aconteceu. Era moldura acrescentada a um número verdadeiro,
que é a deriva mais convincente e por isso a pior.

**Também entraram:** o capítulo 06 descrevia como erro caro uma divergência **entre solvers** que a
medição não produz (os dois concordaram; quem divergiu foi o Simplex exato); a diferença de casas
decimais era de **oito**, não nove; a citação de Huangfu & Hall trazia 2018 contra os 2017 do
registro; o capítulo 01 dizia "quatro formas" para uma tabela de cinco linhas; o capítulo 02
afirmava que os nove capítulos da Parte II estão "todos na etapa 3" enquanto a sua própria tabela
classificava um deles como etapa 1 e 2; e o objetivo O3 do capítulo 01 tinha exercício e não tinha
conteúdo que o sustentasse — ganhou a seção *"Três perguntas antes de citar um caso"*.

**Seis termos deixaram de ser órfãos:** `NP`, `AMPL`, `CBC` e `HiGHS` entraram no glossário e no
mapa de siglas do motor; **limitante**, ***gap***, **face ótima** e **análise suavizada** ganharam
verbete. E o capítulo 04 deixou de cunhar `PIM`, que concorria com `PI` e `MILP` já registradas.

**Uma duplicação de exercício foi desfeita:** o `cap03.exA` era a mesma padaria, com a mesma tarefa,
do `cap07.exA`. Ganhou cenário próprio — uma gráfica com duas máquinas, em que a variável é **hora
de máquina** e não unidade produzida, o que faz o teste da unidade trabalhar de verdade.

> **O que continua em dívida, declarado:** o campo de **âncora** que o Guia Editorial promete em
> cada exercício ("aponte a seção que resolve a dúvida") não existe em nenhum dos 68. Não é
> regressão desta rodada — é promessa editorial sem implementação, e fica registrada como tal.

### Edição 0.36 — 2026-08-13 · A terceira lente atacou a medição, e ganhou

A revisão da medição fez o que nenhuma leitura de texto faria: **rodou 46 mutações de um dígito**
nos capítulos 05 e 06 e contou quantas a suíte deixava passar. Dezenove passavam. O relatório é o
mais útil que este handbook já recebeu, e o que ele achou muda o desenho, não só os números.

**Primeiro, a boa notícia, e ela é grande.** A afirmação central do capítulo 05 foi atacada por
três ângulos independentes — 200 sementes, sete tamanhos de cubo, e três modelos diferentes de
perturbação — e **sobreviveu aos três**. Ela é mais forte do que o capítulo dizia.

**A tabela de perturbação estava publicando ruído.** Vinte sementes bastavam para a mediana e para
a fração de caminhos intactos, e **não** para mínimo e máximo: o máximo da linha de 50% vai de 47
para 63 só por passar de 20 para 200 sementes. Extremo de amostra pequena é estatística de ordem,
não medição. A tabela agora roda **200 sementes** e publica **só o que estabiliza** — mediana e
caminhos intactos.

**E o teste que corrigi na edição anterior repetia o defeito que ele existia para pegar.** Ele
assertava `intactas == 0` para a perturbação de 50%: verdade nas 20 sementes escolhidas, **falso na
família** — com 200, dois caminhos sobrevivem. Assertar o extremo de uma amostra, dentro do teste
criado para impedir que se publique um sorteio.

**Entrou o eixo que faltava.** A tabela olhava um tamanho só, e o teorema de Spielman & Teng vive
no crescimento em $n$. Medido: a **1%**, o caminho fica intacto em **25/25 de $n=4$ a $n=8$** — o
que sustenta o capítulo; a **10%**, a fração cai de 25/25 para 7/25 conforme o cubo cresce, que é
**a direção que o teorema prevê**. A medição passou a honrar o resultado que ela ressalva.

**O modelo de perturbação era indeclarado e é load-bearing.** Ele é multiplicativo, relativo,
entrada a entrada, e **preserva o padrão de zeros** do cubo. Quem reproduzir com ruído aditivo
denso obtém mediana 9 em vez de 63 e concluirá que o livro errou — e não terá errado: preencher os
zeros não é perturbação pequena, porque as variáveis do cubo chegam a $10^n$. Calibrado para 1% no
vértice ótimo, o resultado volta. A declaração está no capítulo e há teste que exige que ela fique.

**Um rótulo escorregava, e justamente neste capítulo.** A coluna dizia *"pior caso teórico"* para
$2^n-1$, que é o custo do cubo — um pior caso **construído** para uma regra de pivoteamento. Um
poliedro de dimensão 20 com 40 facetas admite mais de **40 milhões** de vértices. Num capítulo cujo
primeiro objetivo é dizer sobre o que exatamente uma afirmação fala, o rótulo virou *"o cubo do
mesmo tamanho"*.

**Três bloqueios no capítulo 06, todos reais:**

1. **A linha do CBC não tinha dono.** O teste procurava `45.882352` no documento inteiro, e o
   número também aparece na Síntese — então **apagar a linha da tabela deixava a suíte verde**. Era
   o único número que o próprio teste chamava de "dependente de versão".
2. **A Síntese e a Leitura executiva de ambos os capítulos não tinham teste nenhum.** Treze das
   dezenove mutações que passaram estavam ali. E o risco não era teórico: cada correção desta
   rodada teve de atualizar a mesma medição **em três lugares à mão**.
3. **O capítulo enunciava a regra da versão e a violava.** Ele manda *"diga a ferramenta e a versão
   que produziu o número"*, e `resultados-ferramentas.json` gravava os **nomes** dos solvers no
   campo `versoes`. As versões que produzem `45.88235294117647` e `45.882352` não estavam em lugar
   nenhum. Agora estão — HiGHS 1.15.1, e o CBC declarado como *embutido no PuLP 3.3.2*, que é mais
   honesto do que inventar um número de versão para o binário.

**E o `test_anatomia.py` criou a segunda fonte da verdade que o seu próprio cabeçalho dizia estar
evitando:** ele transcrevia os sete coeficientes do enunciado do `cap03.exC` e nenhum teste lia o
enunciado. Agora lê.

> **A lição que fica, e é sobre testes, não sobre números.** Um teste pode herdar exatamente o
> defeito que ele existe para impedir. O que separou os dois casos aqui foi **variar o que o teste
> supõe fixo** — a semente, o tamanho, o modelo de ruído. Foi assim que a afirmação central
> sobreviveu com mais força, e foi assim que as duas asserções frágeis caíram.

### Edição 0.37 — 2026-08-13 · A Parte III abre: grafos, e o método que se contradiz

**Entrou:** a etapa de medição `po-zero/parte-III-redes` — com sete resultados — e os dois
primeiros capítulos da Parte III: [16 — Grafos e redes](capitulos/16-grafos-e-redes.md) 🟡 e
[17 — Caminho mínimo](capitulos/17-caminho-minimo.md) 🔵.

**O achado do capítulo 17 é o mais desconfortável do livro até aqui.** Diante de um peso negativo,
Dijkstra não devolve um número errado — ele devolve **um número e um caminho que não fecham entre
si**. Medido: distância **6** até o destino, e caminho `A → C → B → D`, que custa **4**. Sem erro,
sem aviso, sem exceção.

> O defeito não foi o método errar. Foi o método **não ter como saber** que errou: a hipótese de
> peso não negativo está na cabeça de quem escolheu Dijkstra, não no código. Há teste que fica
> vermelho se alguém "consertar" a implementação — porque aí o capítulo passaria a descrever algo
> que não acontece mais.

**Os outros seis resultados**, medidos e ainda esperando os capítulos que os publicam: max-fluxo
igual a corte mínimo (**15**, com o corte exibido); a relaxação linear do transporte devolvendo
**todos inteiros** sem restrição de integralidade, e **uma** restrição transversal quebrando isso;
a designação saindo **0/1** sem variável binária; o mesmo gesto guloso sendo **ótimo na árvore** e
**14,3% pior no roteiro**; e o PERT publicando **21 dias** para um projeto que leva **24,48** e
**estoura a estimativa em 82,3%** das amostras.

**Três erros meus pelo caminho, todos registrados no README da etapa**, e o terceiro é o que mais
ensina:

1. O experimento da estrutura quebrada **não quebrava nada** — a restrição escolhida deixava o
   modelo inviável, e passou porque a função devolvia o plano sem ninguém olhar o `status`.
2. A comparação do PERT misturava duas causas. Isolando **nas mesmas amostras** — duração do
   projeto contra duração do caminho declarado antes de sortear —, o viés honesto é **0,49 dia**,
   e não os ~4,7 que a comparação ingênua daria. Com controle: um ramo só dá **exatamente zero**.
3. **O grafo das cinco cidades não sustentava a tese que ele existia para sustentar.** Eu escolhi
   os pesos à mão para o guloso errar o roteiro, e **ele acertou** — 17 contra 17. A instância
   publicada saiu de uma busca com semente declarada sobre 4.000 grafos aleatórios, tomando a de
   maior perda. **Procurar um contraexemplo é mais honesto do que arranjar um.**

**E o portão da procedência pegou, antes de publicar, o defeito que a revisão da Parte I tinha
pegado depois:** o capítulo 16 afirmava "Euler mostrou, em 1736" no corpo enquanto a tabela marcava
a atribuição como `⏳`. O hedge foi para a frase. É a diferença entre uma regra que alguém lembra e
uma regra que a máquina cobra.

### Edição 0.38 — 2026-08-13 · Capítulos 18 e 19: o mesmo gesto, e o gargalo que não é aresta

**Entrou:** [18 — Árvore geradora mínima](capitulos/18-arvore-geradora.md) 🔵 e
[19 — Fluxo máximo e corte mínimo](capitulos/19-fluxo-maximo.md) 🔵, com seis exercícios e dois
vídeos.

**O capítulo 18 existe por causa de uma pergunta que quase todo mundo faz errado:** *"se pegar
sempre o mais barato agora funciona aqui, por que não funciona no roteiro?"* A resposta não é
"porque o roteiro é maior" — e o capítulo mede a diferença **na mesma instância, com o mesmo
gesto**: o guloso é ótimo na árvore (**17**, conferido por dois caminhos) e **14,3% pior** no
roteiro (**32** contra **28**).

> A diferença é estrutural: na árvore existe um argumento **local** — a aresta mais barata de
> qualquer corte pertence a alguma árvore ótima — que sustenta a conclusão **global**. No roteiro
> esse argumento não existe, e a decisão local **compromete o futuro**.

**O capítulo 19 entrega o resultado mais bonito do campo, e ele é bonito por ser útil:** o quanto
se escoa é **exatamente** a capacidade do corte mínimo. Medido: **15** e **15**, com o corte
exibido — três arestas, e elas **não estão no mesmo nível da rede**.

Daí saem três decisões que o método dá de graça: investir numa aresta **do** corte aumenta o
fluxo; investir numa aresta **fora** dele não muda nada, por mais importante que ela pareça; e
depois de investir é preciso **recalcular**, porque o corte se move.

> **A confusão mais cara desta Parte é tratar aresta estreita como gargalo.** Na rede medida, a
> aresta de menor capacidade (`centro_sul → loja_b`, com 3) **não** está no corte — o fluxo a
> contorna. E a de maior capacidade também não está, porque sobra folga nela. O exercício B do
> capítulo 19 é inteiro sobre isso, com três propostas de investimento das quais **duas não
> aumentam nada**.

**O que o capítulo 19 declara não fazer:** demonstrar o teorema. Ele o **exibe** numa instância,
com o corte nomeado, e diz que é isso que está fazendo. Um livro que mede um caso e chama isso de
demonstração estaria mentindo; um que cita o teorema e nunca mostra o corte estaria pedindo fé.

### Edição 0.39 — 2026-08-13 · A Parte III fecha: a integralidade de graça, e o prazo que estoura

**Entrou:** os três últimos capítulos da Parte III — [20 — Fluxo de custo mínimo](capitulos/20-fluxo-custo-minimo.md),
[21 — Transporte, designação e transbordo](capitulos/21-transporte-designacao.md) e
[22 — PERT e CPM](capitulos/22-pert-cpm.md), os três 🔵 —, com nove exercícios e três vídeos.
**A Parte III está completa**: sete capítulos, vinte e um exercícios, uma etapa de medição com
sete resultados.

**O capítulo 20 publica o resultado mais útil da Parte**, e ele muda decisão de projeto: a
relaxação linear de um problema de rede **já vem inteira**. Medido: custo **220**, todos os
embarques em unidades exatas, num modelo sem uma única variável declarada inteira ou binária. Não é
sorte nem arredondamento — é a estrutura, e ela também mantém preço-sombra e faixa de validade, que
um modelo inteiro não tem.

E o outro lado está medido na mesma página: **uma** restrição banal — rotas ocupam espaço diferente
no pátio — tira a matriz da família, e o ótimo vai a **223,33** com **quatro** embarques
fracionários. `Optimal` nos dois casos, e nenhum aviso.

**O capítulo 21 mede o caso em que isso mais surpreende.** A designação é combinatória em cada
palavra do enunciado — *cada pessoa faz exatamente uma tarefa* — e resolvida como Programação
Linear **contínua** devolve **0/1**: custo 9, três atribuições. Declarar `Binary` por precaução
paga o custo do *branch-and-bound* e **perde a análise de sensibilidade junto**.

> Há teste que lê o **código-fonte** do modelo, e não a saída: se alguém acrescentar `cat="Binary"`,
> a resposta continua 0/1 e o capítulo passa a mentir — porque a lição não é que a saída é binária,
> é que ela é binária **sem ter sido pedida**.

**O capítulo 22 fecha a Parte com o resultado mais incômodo dela.** A fórmula do PERT publica
**21 dias**; o projeto leva **24,48** em média e **estoura a estimativa em 82,3% das amostras**.

E a parte que custou a manchete: **duas causas produzem esse desvio, e só uma é defeito do método**.
Separando **nas mesmas amostras** — duração do projeto contra duração do caminho declarado crítico
antes de sortear —, o viés próprio do PERT é **0,49 dia**, e não os ~3,5 que a comparação ingênua
daria. Seria mais impressionante publicar o número grande; seria também falso.

A varredura de ramos paralelos vem com **controle**: um ramo só dá **exatamente 0,0**, que é o que
prova a isolação. Depois 1,71 · 2,55 · 3,64 · 4,45. E mesmo com um ramo só a estimativa estoura em
**76,5%** das amostras — essa parte não é viés de convergência, é **média não ser promessa**.

### Edição 0.40 — 2026-08-13 · O caderno da Parte III

**Entrou:** [`po-zero/cadernos/parte-III.ipynb`](https://github.com/GHDaru/operationalresearchaibook/blob/main/po-zero/cadernos/parte-III.ipynb),
o terceiro caderno do handbook, sob as mesmas sete regras da ADR 0016.

**O erro que o leitor roda antes de ver o certo, desta vez, tem duas camadas.** O caderno pergunta,
diante da rede com peso negativo: *"você espera que Dijkstra devolva o número errado, o caminho
errado, ou os dois?"* — e a resposta é **nenhuma das três**. Ele devolve um número e um caminho que
**não fecham entre si**, e é preciso olhar as duas linhas juntas para ver.

**E há um segundo palpite**, no capítulo 22: *"a fórmula diz 21 dias, a simulação diz 24,48; desses
~3,5 dias de diferença, quanto é culpa do método?"* O palpite comum é "tudo". A célula seguinte
separa as duas causas nas mesmas amostras e mostra **0,49**.

**A célula "mexa aqui" começa pelo controle.** O leitor é instruído a rodar primeiro com **um**
ramo paralelo — que tem de dar viés exatamente zero — antes de aumentar. É a primeira vez que um
caderno deste handbook pede que o leitor rode o **controle** do experimento antes do experimento, e
a razão está escrita ao lado: sem paralelismo o viés não pode existir, e ver o zero é o que
autoriza confiar nos outros números.

Três capítulos apontam para ele — 17, 20 e 22 —, e o teste de caderno órfão barrou o commit até que
o primeiro link existisse.

### Edição 0.41 — 2026-08-13 · A Parte III revisada por quem não a escreveu

Revisão independente em contexto fresco dos capítulos 16 a 22 e das sete baterias. Quem
escreveu não revisou, e cada achado foi **reconferido por medição própria** antes de virar
correção. A medição desmentiu o revisor em nenhum dos três erros de fato e o confirmou nos três
— mas mudou o desenho de duas correções.

**Três erros de fato, e o padrão que eles revelam.**

O gabarito de `cap18.exA` publicava **19** para a árvore geradora sem a aresta `a–c`; o correto é
**21**. O número errado não era o pior: dele saía a moral *"a perda é de 2, e não de 3 — o custo de
proibir uma aresta não é o custo dela"*, que está **invertida**. A aresta vale 3 e a perda é **4** —
maior, não menor, porque a substituta não é a próxima aresta da lista, é a melhor reconexão
disponível **depois que a topologia mudou**. Era o único número da Parte III sem medição, e o único
errado. Agora existe `custo_de_proibir()`, o capítulo 18 publica a tabela, e dois testes prendem o
valor: um lê o capítulo, o outro lê o gabarito.

`cap22.exB` e `cap22.exC` afirmavam, em quatro trechos, que *"por definição, metade das realizações
fica acima da média"*. Isso é a definição de **mediana**. Medido nas mesmas 20 mil amostras: a média
simulada (24,48) é estourada em **48,1%** das amostras, e a mediana (24,30) em **50,0%** exatos —
prazo de projeto é assimétrico à direita, então a média fica acima da mediana. O veredito prático
não muda (nenhuma das duas é compromisso), mas o argumento estava trocado, e num capítulo cuja tese
inteira é *"média não é promessa"*.

O diagrama do capítulo 19 trazia `centro_sul --6--> loja_b`, aresta que **não existe** na rede
medida — o 6 é de `centro_norte`. Nenhum teste pegava, porque o fluxo máximo dá 15 nas duas
leituras; só um leitor conferindo à mão veria. Agora um teste compara **todo** desenho da rede —
capítulo e enunciados — com a instância, aresta por aresta.

**O padrão:** os três estavam onde não havia vínculo texto↔medição. A correção que interessa não é o
número, é o vínculo.

**Onde a garantia de integralidade para.** A Parte afirmava, sem qualificação, que *"a resposta não
tem como sair fracionária"* — e o capítulo 21 transformava isso em conselho operacional (*não
declare `Binary`*). O teorema garante que **existe vértice ótimo inteiro**; quem entrega o inteiro é
o Simplex, porque para em vértice. Medido, com controle:

| Instância | Método | Objetivo | Saída |
|---|---|---|---|
| Empate no ótimo | pontos interiores, *crossover* desligado | 3 | **1/3 em toda variável** |
| Empate no ótimo | pontos interiores, *crossover* ligado | 3 | 0/1 |
| Ótimo único | pontos interiores, *crossover* desligado | 9 | 0/1 |

O `1/3` é um ponto **ótimo**, não erro numérico. As duas últimas linhas são o controle, e sem elas o
resultado de cima poderia ser lido como solver ruim em vez de método diferente. Virou a quinta
entrada de *"quando não serve"* do capítulo 20, uma ressalva no 21, e um teste que falha se qualquer
um dos dois voltar a garantir integralidade sem dizer onde a garantia acaba.

**Uma armadilha de projeto de experimento, registrada porque custou uma tentativa.** A primeira
instância de "ótimo único" usava custo da forma $a_i + b_j$. Toda designação soma $\sum a + \sum b$,
então **tudo empata** — o controle media o mesmo que o caso, e teria "confirmado" a hipótese por
construção. A instância de ótimo único passou a ser a equipe do capítulo 21, cujo ótimo (custo 9) é
único de fato.

**Correção de um número desta página.** A **edição 0.39** registra *"e não os ~4,7 que a comparação
ingênua daria"*, e a **edição 0.40** registra *"~3,5"* para a mesma comparação. Os dois estavam
certos quando foram escritos: o 4,7 era da rede de projeto anterior, e o 3,5 é da rede publicada. O
registro é *append-only* e as duas linhas ficam — **o valor corrente é 3,5**, e o viés próprio do
método, isolado nas mesmas amostras, é **0,49**.

**O resto.** O capítulo 04 produzia, como conselho, o erro caro do capítulo 21: o mapa de decisão
mandava classificar como Programação Inteira Mista diante de qualquer decisão indivisível, sem
ressalva. O link entre os dois era de mão única — quem para na Parte I saía com uma regra falsa para
uma família inteira de problemas. `cap19.exC` avaliava o aluno por conteúdo do capítulo 20, que ele
ainda não leu. `cap16.exA` fixava uma leitura de enfermeiro/turno que o próprio livro contradiz três
capítulos adiante. Números de desempenho sem medição (*"resolvem em segundos"*) saíram do capítulo
16, que na mesma página declarava não ter número novo. O capítulo 22 passou a declarar a
distribuição amostrada — **triangular**, de média $(o+m+p)/3$ contra os $(o+4m+p)/6$ da fórmula —,
que responde por quase todo o desvio e era cobrada num critério sem estar no texto. **"Restrição
transversal"**, que carrega a tese da Parte, só estava definida em gabarito, que por arquitetura
nunca é publicado; agora está no corpo do 20 e no glossário. O capítulo 17 ganhou *"os problemas que
não parecem caminho"*, que o mapa prometia e a página não entregava — com a arbitragem de câmbio,
onde o veredito *"ciclo negativo"* deixa de ser aviso de erro e vira **a resposta procurada**.

**O que foi apontado e não acatado.** A revisão pediu para cortar as repetições do mecanismo da
restrição transversal no capítulo 21. Duas das três estão na **Síntese** e na **Leitura executiva**,
que o guia editorial existe para exigir que restatem o capítulo. Repetição ali é função, não ruído.

**Baterias.** Os capítulos 19 e 20 eram as únicas séries da Parte sem exercício `facil`, e o 20 é o
capítulo mais importante dela. Ganharam porta de entrada — o do 19 provoca de propósito o erro de
somar só o que sai da fábrica; o do 20 escreve a equação de conservação de um nó e descobre, ao
somar as cinco, por que oferta e demanda têm de fechar. A Parte III passa a ter **23 exercícios**.

### Edição 0.42 — 2026-08-13 · A Parte III ganha literatura, e um portão novo

**A Parte III era a única do handbook sem ancoragem em literatura.** Nenhum dos sete capítulos
tinha a seção **Fundamentos científicos** que o esqueleto obrigatório exige, nem um link para a
bibliografia, nem um identificador. Apontado pela revisão independente, e é violação de princípio,
não questão de estilo.

**A dívida foi paga: 30 referências novas, todas com identificador conferido.** As seções entraram
nos sete capítulos, a bibliografia ganhou a seção da Parte III, e o Radar ganhou oito linhas — desta
vez **na ordem certa**, junto com a bibliografia e não depois, ao contrário do que aconteceu na
rodada 006 e está registrado no próprio Radar.

**Todas são `✓ᵐ` e nenhuma é `✓`, e a diferença importa.** O ambiente desta rodada bloqueia o
acesso às páginas das editoras. O que foi conferido, por identificador em Crossref, é autor,
título, periódico e ano — **nenhum texto foi aberto**. Onde o conteúdo mudaria uma afirmação do
livro, a afirmação **não foi feita**, e o selo `⏳` do capítulo permanece:

- a origem do nome **"húngaro"** (capítulo 21) continua `⏳`, mesmo agora que existe a reimpressão
  de 2004 em que, pelos registros, o próprio Kuhn explica a homenagem;
- o enunciado de **Hoffman & Kruskal** (capítulo 20) continua `⏳`, mesmo sendo o resultado que
  sustenta o capítulo inteiro. **Confirmar um DOI não é confirmar um teorema**;
- **Klingel (1966)** entrou como bloqueante declarado: há indício de que a direção do viés que ele
  relata não seja a que o capítulo 22 mede, e por isso o capítulo **não faz nenhuma afirmação
  comparativa com a literatura**.

**A referência de maior retorno da Parte é Megiddo (1991)**, e ela chegou por acaso feliz: trata de
recuperar base ótima a partir de um ponto interior, que é exatamente o mecanismo do *crossover* —
o mesmo que esta rodada mediu ao encontrar `1/3` numa designação totalmente unimodular. A literatura
e a medição própria se encontraram no mesmo parágrafo.

**Uma lição de método, e ela é sobre não aceitar o relatório de ninguém.** O levantamento foi feito
por um agente em contexto próprio, que reportou **zero DOIs resolvidos** — todo acesso bloqueado — e
marcou sete identificadores como "candidatos não conferidos". Reconferido por medição própria:
**os 31 identificadores resolvem**, inclusive os sete. A diferença era de ferramenta, não de
ambiente — `fetch` nativo leva 403 do proxy e `curl` passa, coisa que uma rodada anterior deste
repositório já havia diagnosticado e registrado no próprio código. Sem a reconferência, a Parte III
teria ficado sem literatura por um obstáculo que não existia. **Duas datas do relatório também
estavam erradas** (2005 onde o registro diz 2004).

**E entrou o décimo portão: `verifica-desempenho.mjs`.** O guia proíbe comparação de velocidade sem
cronômetro — *"nem 'cerca de 10× mais rápido'"* — e numa única rodada o defeito apareceu três vezes,
a terceira delas escrita **por quem tinha acabado de corrigir as duas primeiras**. É o que separa
lapso de tentação de escrita, e tentação de escrita não se resolve com disciplina.

O portão só ficou útil na quarta versão, e as três primeiras **falharam no teste que importa** —
reintroduzir os defeitos documentados e exigir vermelho:

1. aceitar a **renúncia** como autorização deixou os três passarem, porque os defeitos moravam ao
   lado das renúncias que os corrigiram. Renúncia é o que se escreve **no lugar** da afirmação, não
   ao lado dela — agora ela é falha própria;
2. a janela de 900 caracteres deixou dois passarem: um "Medido nesta página: custo 9" a setecentos
   caracteres autorizava "de minutos para horas". O escopo virou **a frase**;
3. a palavra solta "medido" deixou um passar, por algo que nenhuma expressão regular resolve —
   *"garantias que o modelo genérico não oferece, a principal delas **medida** no capítulo 20"*. O
   portão passou a exigir o que a constituição já exige: **procedência é lugar**, um ponteiro que o
   leitor possa abrir.

Ele encontrou, de saída, dois defeitos fora da Parte III: o capítulo 07 e o gabarito de `cap17.exC`.

### Edição 0.43 — 2026-08-13 · A segunda revisão derruba duas afirmações centrais

Revisão independente com **lente de medição** — campanha de mutação, implementações de referência,
reprodução da busca declarada. Dois bloqueantes, e os dois do tipo pior: **afirmação conferível que
não sobrevive à conferência**. Os dois reconferidos por medição própria antes de virar correção.

**A contradição do Dijkstra era artefato da implementação.** O capítulo 17 afirmava que o método
*"devolve uma resposta que contradiz a si mesma"* e que *"não há erro, não há aviso, não há exceção
lançada"*. Medido na mesma instância:

| | Distância | Caminho devolvido custa | |
|---|---|---|---|
| com a guarda do nó fechado | 6 | 6 | erra, **coerente** |
| sem a guarda (a que estava no repositório) | 6 | 4 | **contradiz a si mesma** |
| com fila de prioridade | 4 | 4 | **acerta**, por acidente |
| `networkx` 3.6.1 | — | — | **levanta exceção** |

A contradição vinha de um `if` que faltava: a relaxação escrevia em nó já fechado e corrompia a
árvore de predecessores. E o "silêncio" era falso — biblioteca consagrada avisa.

**O agravante é sobre teste, e é a lição da rodada.** O teste
`test_a_saida_de_dijkstra_contradiz_a_si_mesma` existia para impedir que o contraexemplo morresse —
e por isso **trancava o artefato**, obrigando o capítulo a descrever um defeito como propriedade do
método. Um teste preserva um erro com o mesmo zelo com que preservaria um acerto: **o que ele
garante é estabilidade, não verdade.** Está registrado no cabeçalho da suíte, para quem vier depois.

A correção não enfraqueceu o capítulo. A lição publicada agora é melhor e é verdadeira: **três
coisas chamadas "Dijkstra" dão três respostas** assim que a hipótese cai, e *"usei Dijkstra"* não
descreve o que foi executado. A `networkx` entrou em `requirements.txt` — é a única dependência
deste handbook que existe para **contradizer** o handbook.

**A procedência da instância do roteiro era falsa.** O capítulo 18 dizia que a instância veio de
*"uma busca sobre 4.000 grafos, tomando a de maior perda relativa"* — numa caixa que se gabava de
honestidade. O código da busca **não existia**; só a prosa. Reconstruído e medido: a instância
publicada é o **sorteio nº 3**, com perda de 14,3%, enquanto a de maior perda é o 1867, com 150%, e
**848 das 4.000** perdem tanto quanto ou mais. A regra de seleção narrada nunca foi aplicada.

Afirmação de procedência que é conferível e falha na conferência é **pior que número sem fonte** —
porque convida à conferência e a decepciona.

A busca agora existe, e trouxe o que o capítulo devia ao leitor: a **distribuição**. Mediana da
perda **0%**; o guloso é **ótimo em 55,93%** das instâncias. Publicar só o caso em que ele perde
14,3% distorcia — e a lição foi deslocada para onde é verdadeira: **o problema do guloso não é
errar muito, é não ter como avisar**.

**Duas asserções não conseguiam falhar.** O custo 223,33 tinha um `or "223,33"` literal, que passava
mesmo se a medição mudasse; e os fracionários comparavam só o nome da rota, descartando o valor — é
por isso que 1,67 · 3,33 · 23,33 · 6,67 estavam sem dono **apesar de parecerem cobertos**.

**Os dados de entrada ganharam dono.** Todo teste conferia *resultado*; nenhum conferia a
**definição** da instância — que é o que o leitor usa para refazer a conta à mão, e onde o defeito
do diagrama do capítulo 19 nasceu. As seis instâncias passam a ser conferidas célula por célula.
Campanha de mutação: **6 de 6 pegas**.

**Três refinamentos que não bloqueavam e melhoram o livro.**

*Ser transversal não basta.* Três restrições igualmente transversais: coeficientes 2 e 3 quebram a
integralidade, coeficiente 1 não quebra, e um percentual do total não quebra. O que separa não é a
transversalidade — é o **coeficiente**. Um exercício de Verificação pedia ao leitor que previsse a
quebra justamente no caso em que ela não acontece.

*Até onde o dígito carrega.* Entre seis sementes, a duração média varia de 24,43 a 24,51 e a
probabilidade de estouro de 81,83% a 83,06%. **O segundo dígito carrega e o terceiro não** — e agora
a página diz isso.

*O controle que não podia falhar.* O controle de um ramo dá zero **por construção**, então prova
menos do que o capítulo afirmava. Foi acrescentado um que pode falhar: dois ramos desiguais com
faixas sobrepostas, viés **0,0618** — positivo e pequeno.

E aqui a rodada repetiu o próprio defeito que estava corrigindo, o que vale mais registrado do que
escondido: **a primeira versão desse novo controle também não podia falhar.** As faixas escolhidas
foram (30, 40, 55) e (2, 5, 9) — que não se cruzam. O ramo curto nunca vencia, o viés dava 0,0 por
construção, e o controle escrito para substituir um controle tautológico era tautológico pelo mesmo
motivo. Só a medição pegou. **Quem escreve controle precisa perguntar, antes de rodar, o que
exatamente o faria dar diferente de zero** — e essa pergunta agora está escrita no capítulo 22.
