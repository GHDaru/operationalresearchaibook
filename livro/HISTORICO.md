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
