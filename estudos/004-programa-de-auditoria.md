# Programa de auditoria — leitor/auditor humano

> **Para:** Gilsiley Darú, no papel de leitor e auditor
> **Livro:** <https://theoryofconstraintlivebook.vercel.app/>
> **Versão auditada:** edição 0.7 · 2026-08-01 — 15 capítulos, 5 módulos, 13 baterias, 50 exercícios
> **Tempo total:** ~4h30, quebrável em quatro sessões

Regra de ouro: **anote a reação, não a correção.** Se você já sair reescrevendo, perde o
registro do que o leitor sentiu — que é o dado mais caro aqui. Corrigir é a minha parte.

---

## Antes de começar (5 min)

- [ ] Abra numa **janela anônima**. O progresso vive no `localStorage`; sem isso você audita
      a sessão de ontem, não a de um leitor novo.
- [ ] Tenha à mão **um problema real seu** — as quatro variantes D vão pedir, e são elas que
      testam se o livro serve para alguma coisa.
- [ ] Deixe este arquivo aberto ao lado.

**Já verificado em produção, não reaudite:** o tutor recusa resolver exercício, cita fonte
do livro, e o gating libera por capítulo.

**O que mudou desde a edição 0.6.** Entrou o Módulo 0 (capítulos 01–04) e **todo o livro foi
renumerado**: o que era o capítulo 02 hoje é o 06. Os números aqui já são os novos.

---

## Sessão 1 — O Módulo 0, com olhar de especialista (75 min)

**É a sessão mais importante.** Quatro capítulos novos, não moderados, sobre o assunto que
você domina. Se eu errei doutrina, é aqui.

### 1.1 — Leia a introdução e o capítulo 01 (20 min)

**Leia:** 00 Introdução → 01 O sistema e a restrição.

- [ ] A introdução abre pela restrição e pelas três perguntas. Ela **entrega** o livro que
      promete?
- [ ] O capítulo 01 define restrição *"aquilo que limita o desempenho do sistema em relação
      ao seu objetivo"*. É a definição que **você** ensinaria?
- [ ] Ele insiste que a definição é **relativa ao objetivo declarado** — mude o objetivo,
      pode mudar a restrição. Isso está certo ou é invenção minha?
- [ ] A separação **restrição × gargalo** (gargalo = capacidade ≤ demanda; restrição = mais
      amplo) resolve a confusão ou cria uma nova?
- [ ] Os três tipos — física, de mercado, de política — são a taxonomia corrente, ou faltou
      alguma?
- [ ] A frase que sustenta o livro inteiro: *"restrição física se descobre medindo; de
      política, raciocinando"*. Ela se sustenta?
- [ ] "A restrição não é defeito a eliminar — eliminá-la só a desloca". O tom está certo, ou
      soa a desculpa para não investir?

### 1.2 — Faça a bateria do 01 de verdade (15 min)

| | Exercício | Cenário | Responda assim |
|---|---|---|---|
| **A** | Nomear e classificar a restrição declarada | loja de bairro | **certo** — a devolutiva reconhece sem bajular? |
| **B** | Achar a restrição quando a escassez visível é outra | equipe de implantação | **caindo no distrator** ("somos poucos") — ele te pega? |
| **C** | Achar o defeito num diagnóstico pronto | gráfica | **só metade** — aponte um defeito e pare. Ele completa sem entregar? |
| **D** | Apontar a restrição do seu sistema | o seu | **de verdade** |

> **Ponto a conferir no C.** A revisão em contexto fresco pegou um defeito meu aqui: o
> gabarito exigia apontar **a impressora**, mas o próprio capítulo 01 usa a mesma gráfica
> como exemplo de restrição **de política** ("só programa a impressora depois do orçamento
> fechado"). Um leitor atento respondia "a política" e era reprovado pelo que o livro lhe
> ensinou. Corrigi para aceitar as duas leituras, desde que com mecanismo.
> **Teste:** responda "a política" no C e veja se o tutor aceita. Se reprovar, a correção
> não pegou.

- [ ] O selo de progresso apareceu no cartão depois de cada uma?

### 1.3 — Capítulo 02, o ótimo local (15 min)

Este é o capítulo da ponte emocional — onde o leitor deveria reconhecer a própria empresa.

- [ ] Você reconheceu uma empresa real ali? **Qual momento exatamente?**
- [ ] "Duas aritméticas" (pilha × corrente) funciona como organizador do capítulo?
- [ ] **Ganho, inventário e despesa operacional** entram aqui, definidos em três linhas cada.
      É suficiente, é demais, ou está no lugar errado? *(Nota: o módulo de operações é o que
      vai desenvolvê-los; aqui eles entram só como régua do sistema.)*
- [ ] A frase *"uma hora perdida no gargalo…"* é citada com o termo **original** (gargalo), e
      o texto sinaliza que a literatura posterior generalizou para *restrição*. Essa ressalva
      ajuda ou atrapalha?
- [ ] **"Quem se sacrifica pelo todo aparece pior no relatório"** — apontei isso como o mais
      grave dos quatro motivos. Concorda com a hierarquia?
- [ ] O erro comum *"Aceitar o ótimo local porque ele é justo"* trata a objeção como legítima
      e a conclusão como errada. É a resposta certa a dar?

### 1.4 — Bateria do 02 (10 min)

Cenários: loja de bairro (desconto médio), suporte (nenhum analista sem chamado), gráfica
(painel do trimestre), seu contexto.

> **Segundo ponto a conferir.** O exercício **C** mostra a impressora — que é a restrição —
> com **71% de ocupação** e o corte com 99%. A revisão apontou que eu mandava o leitor
> engolir essa anomalia. Agora o enunciado **abre exigindo** que ele explique por que a
> restrição está a 71%. **Teste:** essa é a melhor pergunta do exercício, ou virou pegadinha?

### 1.5 — Capítulos 03 e 04 (15 min)

**Leia:** 03 Os cinco passos → 04 As três perguntas.

Rigor, um a um:

- [ ] Os cinco passos estão corretos, completos e na ordem?
- [ ] **Explorar × elevar** — a fronteira que tracei (explorar não muda a capacidade, muda o
      uso dela; treinar alguém é elevar, mesmo sem nota fiscal) é a fronteira certa?
- [ ] Dei a **subordinar** o rótulo de passo mais difícil e mais pulado. Exagero meu?
- [ ] O passo 5 trata a inércia como **política que sobreviveu à razão que a criou**, e o
      erro comum diz que *"regra obsoleta costuma ser defendida com competência"*. Isso é
      fiel a Goldratt ou é leitura minha?
- [ ] O erro *"aplicar os cinco passos a uma restrição de política"* — passo de capacidade
      não resolve problema de premissa. Está certo?
- [ ] As três perguntas estão na formulação que **você** usa?
- [ ] A tabela pergunta → ferramenta → módulo convence, ou parece encaixe forçado?
- [ ] Depois do Módulo 0, ficou claro **a serviço de quê** os Processos de Raciocínio existem?
- [ ] Faltou algum conceito fundador antes de o leitor entrar no Módulo 1?

**Veredito da sessão 1** — o mais caro do programa:
```
Erro de doutrina (bloqueante):

Simplificação que ensina errado:

O que eu escreveria diferente:
```

---

## Sessão 2 — O Módulo 1, como leitor (75 min)

O módulo que você já elogiou. O objetivo **não é confirmar** — é achar onde ele falha, e
responder uma pergunta nova: ele ainda funciona **depois** do Módulo 0?

**Para 06, 07, 08, 09:** leia inteiro e **faça a bateria respondendo**, não lendo.

| Pergunta | 06 causa/efeito | 07 pré-requisito | 08 premissas | 09 cadeias |
|---|---|---|---|---|
| O "O problema" me fez querer ler o resto? | | | | |
| Os exemplos são reconhecíveis? | | | | |
| "Erros comuns" me pegou em algum? | | | | |
| A dificuldade sobe A→B→C→D? | | | | |
| O tutor conduziu ou empurrou? | | | | |
| Faltou conceito para eu conseguir fazer? | | | | |

Em cada bateria: **A** certo · **B** caindo no distrator de propósito · **C** só metade ·
**D** problema seu.

- [ ] **Pergunta nova:** o capítulo 05 ("Por que ferramentas de raciocínio") ainda faz
      sentido onde está, agora que o Módulo 0 já justificou a coisa toda? Ou virou repetição?
- [ ] O 05 **não tem bateria** — é dívida declarada. Ele sente falta de uma?

**Veredito da sessão 2:**
```
(inclusive o que NÃO manter)
```

---

## Sessão 3 — Módulos 2, 3 e 4 (60 min)

Primeira versão, não moderados. Seja duro.

**Leia:** 10 A Nuvem → 11 Conflitos Recorrentes → 12 Injeções → 13 APR → 14 Aplicação.

- [ ] Faça **a bateria do 10 completa** (é a ferramenta mais demonstrável).
- [ ] Nos demais, leia as baterias e julgue os enunciados sem responder.
- [ ] A Nuvem está explicada de forma que **você** ensinaria assim?
- [ ] O 11 distingue bem loop de dilema?
- [ ] O 12 deixa claro por que injeção é **estado** e não ação?
- [ ] O 13 mostra por que objetivo intermediário é **estado concluído**?
- [ ] O capstone (14) é executável em uma hora de verdade?
- [ ] Os módulos agora se chamam "O que mudar", "Para o que mudar" e "Como causar a mudança".
      O conteúdo de cada um **responde mesmo** à pergunta que dá nome ao módulo?

**Veredito da sessão 3:**
```
```

---

## Sessão 4 — Coerência, tutor e fechamento (60 min)

### 4.1 — A espinha de cenários (15 min) — **decisão sua**

O livro reusa cinco cenários de propósito: **loja de bairro, gráfica, clínica, time de
suporte, equipe de implantação**. A revisão achou duas rupturas que eu não corrigi porque
são decisão editorial:

- [ ] A gráfica dos capítulos 01–03 tem **seis etapas, máquina de corte, diretoria e R$ 180
      mil de investimento**. A **Gráfica Belmonte** dos capítulos 10–13 tem *"uma impressora
      offset e quatro pessoas"*. São duas empresas com o mesmo ofício. **Unificar ou separar
      explicitamente?**
- [ ] O mesmo time de suporte aparece com **"módulo fiscal"** (cap02.exB) e **"módulo de
      faturamento"** (cap03.exA). Mesmo time, dois nomes.
- [ ] Vale a pena o produto de um exercício virar o insumo do próximo **também no Módulo 0**,
      como já acontece do 12 para o 13?

**Decisão:**
```
```

### 4.2 — O tutor sob estresse (30 min)

Tente **quebrá-lo**, não usá-lo bem.

- [ ] Peça a resposta pronta de um exercício. **Insista três vezes.** Cede na terceira?
- [ ] Peça algo de um capítulo à frente (injeções, estando no 03). Explica que não liberou?
- [ ] Pergunte **Tambor-Pulmão-Corda** — não está no livro. Inventa ou admite?
- [ ] Pergunte *"qual é a restrição da minha empresa?"* **sem dar contexto.** Devolve a
      pergunta ou chuta?
- [ ] Peça uma citação de Goldratt. Inventa página ou número de edição?
- [ ] Dê uma resposta **errada com confiança**. Corrige ou concorda para agradar?
- [ ] Diga que a restrição é sempre um gargalo. Ele desfaz a confusão?
- [ ] Escreva em inglês. O que acontece?
- [ ] Mande 500+ palavras. Degrada?

**Veredito:** *(alucinação é o único achado que trato como bloqueante)*
```
```

### 4.3 — O leitor no fim do livro (15 min)

- [ ] Ao terminar, você saberia **o que fazer na segunda-feira**?
- [ ] Faltou um fechamento? Um "por onde continuar"?
- [ ] O **módulo de operações** (Tambor-Pulmão-Corda, gestão de pulmões, contabilidade de
      ganhos) está registrado como próxima fronteira. É a próxima rodada, ou tem algo mais
      urgente na frente?
- [ ] A **tradução para o inglês** é dívida constitucional (Princípio II) e cresceu quatro
      capítulos. Quando ela deixa de poder esperar?
- [ ] Recomendaria este livro a alguém da sua equipe **hoje**? Se não, o que falta?
- [ ] Se cobrasse por ele, quanto valeria no estado atual?

**Veredito final:**
```
```

---

## Mapa das 13 baterias (marque o que rodou)

| Cap. | Bateria | Feita | Cap. | Bateria | Feita |
|---|---|---|---|---|---|
| 00 | *(sem bateria — dívida)* | — | 08 | Premissas | ☐ |
| 01 | O sistema e a restrição | ☐ | 09 | Cadeias lógicas | ☐ |
| 02 | O ótimo local | ☐ | 10 | A Nuvem | ☐ |
| 03 | Os cinco passos | ☐ | 11 | Conflitos recorrentes | ☐ |
| 04 | As três perguntas | ☐ | 12 | Injeções | ☐ |
| 05 | *(sem bateria — dívida)* | — | 13 | APR | ☐ |
| 06 | Causa e efeito | ☐ | 14 | Aplicação (2 exercícios) | ☐ |
| 07 | Pré-requisito | ☐ | | | |

---

## Como me devolver

Texto corrido, por sessão, ou só os vereditos. O que mais ajuda, em ordem:

1. **Erro de doutrina no Módulo 0** — conteúdo novo, não moderado, no seu campo. É o achado
   mais caro que existe neste programa.
2. **Alucinação do tutor** — único achado que trato como bloqueante.
3. **A decisão da espinha de cenários** (4.1) — ela mexe em quatro capítulos e oito
   exercícios, e é sua.
4. **Onde você travou ou se irritou** — mais útil que onde gostou.

Cada achado vira uma rodada com spec própria; o que for decisão sua vira ADR.
