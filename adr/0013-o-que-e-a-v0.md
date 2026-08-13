# ADR 0013 — O que é a v0, e como ela é construída

**Data:** 2026-08-12 · **Status:** decidido pelo agente sob delegação explícita do autor
("acione um comitê de 3 especialistas, verifique a recomendação, registre em ADR, tome a decisão
e prossiga"), com **quatro itens devolvidos ao autor** por serem gates não delegáveis
· **Comitê:** arquitetura, didática, processo — os três pareceres sintetizados em
[`estudos/003-comite-v0.md`](../estudos/003-comite-v0.md), com o que foi verificado marcado como tal

## Contexto

O autor mandou construir a **v0 do livro completo** — 3 exercícios por tópico, prova ao final,
*long run*, um ciclo Maestro por capítulo, sem parar até terminar — justificando: *"como é um
livro, tudo é reversível e de baixo impacto"*.

**Aritmética conferida:** o mapa declara **77 vagas**; publicadas são **4 numeradas** (07–10) mais
a introdução; o capítulo 11 está em curso na rodada 008. Restam **72**.

## O que o comitê achou, e eu verifiquei antes de aceitar

### A premissa "tudo é reversível" é verdadeira sobre arquivo e falsa sobre leitura

Reversível é o `git`. Não voltam: o `HISTORICO.md`, que é *append-only* por princípio — a edição
0.3 carrega até hoje a nota "⚠️ Registro superado pela edição 0.4" porque **não pôde ser
reescrita**; o corpus do tutor, que indexa o livro e passa a responder com autoridade por texto
que ninguém verificou; e a correção de um aluno — o `cap07.exC` da edição 0.6 tinha critérios
falsos, e o histórico registra que *"um aluno que raciocinasse bem seria reprovado pela rubrica"*.

E há uma classe pior que irreversível: **invisível**. Um livro com 72 capítulos plausíveis e sem
procedência não parece quebrado — **parece pronto**.

### ACHADO VERIFICADO: dois princípios não-negociáveis não têm portão

Conferido por mim, não aceito do parecer:

```
verifica-capitulos.mjs exige "quando não serve"?   NÃO   (0 ocorrências)
verifica-capitulos.mjs exige vídeo?                NÃO   (0 ocorrências)
verifica-exercicios.mjs exige mínimo de 3?         NÃO
os 4 capítulos publicados têm os três — por DISCIPLINA
```

Com 5 capítulos e atenção, passa. **Com 72 em série, deriva — é aritmética, não pessimismo.**

### CORREÇÃO FACTUAL: a constituição não promete anonimato

Conferido: **zero** ocorrências de "anônimo", "privacidade", "LGPD" ou "dado pessoal" nos 12
princípios. Quem promete são `chat-companion/backend/store.py` (*"Identidade é anônima… nenhum
dado pessoal é exigido"*), o README do backend e **`publicar/tema/uso.js`, que exibe ao leitor**:
*"Contagens agregadas e anônimas, registradas apenas com consentimento."*

Eu havia afirmado o contrário, ao autor e no `chat-companion/DEPLOY.md`. Estava errado, e o erro
**piora** o enquadramento: a promessa não está num documento interno emendável — está publicada.

## Decisão

### D1 — A unidade da rodada passa a ser a PARTE, não o capítulo

Os três membros convergiram nisto de forma independente, e o argumento decisivo é do próprio
`ROADMAP`, virado do avesso: ele fixou um capítulo por rodada porque *"uma Parte inteira num
único gate vira carimbo"*. Em 72 rodadas a mesma lógica se inverte — **72 gates que ninguém
consegue ler também viram carimbo, e um pior, porque cada um parece pequeno.**

Carga medida no padrão atual: spec (127) + plano (125) + capítulo (478) + verificação (225) ≈
**950 linhas por gate** × 72 ≈ 144 horas só de leitura do autor.

**Passa a ser:** ~11 lotes de núcleo + módulos aplicados + 1 fronteira ≈ **14 rodadas**. Uma
branch por Parte, **um commit por capítulo** — para o autor poder rejeitar o capítulo 19 sem
rejeitar 16–18, com um `git revert`.

Isto **emenda a decisão de cadência de 2026-08-06** registrada no `ROADMAP`.

### D2 — Capítulo v0 tem selo de maturidade, visível e verificado por máquina

Condição de parecer favorável dos três. Sem selo, o resultado não é "77 capítulos": é **o
apagamento dos 4 capítulos exemplares na média de 77** — e o leitor julga pela média.

| Selo | Estado | O que o leitor recebe | O que ainda não tem |
|---|---|---|---|
| 🟡 | **v0** | Texto no esqueleto; 3 objetivos ↔ 3 exercícios; "quando não serve"; "De onde isto veio" com selos de procedência; 1 vídeo com ficha conferida | Nenhum número medido próprio |
| 🔵 | **medido** | + experimento no `po-zero` que regenera cada número | Ainda sem revisão independente |
| ✅ | **verificado** | + revisão em contexto fresco + portões provados quebrando | — (é o padrão dos capítulos 07–10) |

**O selo é campo em `sumario.json` e verificado por portão, nunca prosa** — senão é exatamente o
defeito que a edição 0.14 existiu para corrigir: um sistema de selos honesto e nenhum verificado
por máquina é a palavra de quem escreveu.

**Capítulo v0 não recebe ✅ no mapa.** O mapa é a promessa institucional; ✅ mentiroso seria o
pior artefato do repositório.

### D3 — A regra que substitui "uma etapa `po-zero` por capítulo"

O Princípio IV não diz "toda etapa tem script". Diz que **resultado publicado tem artefato que o
regenera**. Logo:

> **Capítulo v0 não publica número que não saiba regenerar.** Capítulo sem medição alguma é
> legítimo; capítulo com desempenho afirmado sem script é violação.

Uma etapa `po-zero` **por Parte**. Isso libera ~50 dos 72 capítulos de escrever código, e é o
maior corte de custo disponível **sem tocar em princípio**.

### D4 — A história vem em lote, antes da Parte, e dívida declarada vence invenção

O Princípio XII exige a seção; o III proíbe afirmar sem fonte. Em v0 o III vence:

> Nenhum capítulo é escrito antes de a sua entrada existir no estudo de história da Parte. Sem
> fonte aberta, o capítulo publica **"De onde isto veio — em dívida"**, nomeando o que falta.
> **Omitir com dívida declarada é conforme; inventar não é.**

Precedente que prova que lote é melhor, não só mais barato: a sessão concentrada da rodada 005
achou a ligação Motzkin entre os capítulos 08 e 09 — **pesquisa capítulo a capítulo teria
perdido**.

**Alarme contraintuitivo, e é o que mais vigio:** lote que fechar com **zero `⏳`** para de
imediato e três capítulos são auditados contra a fonte primária. Num *long run*, 100% verificado
não é sinal de boa pesquisa — é sinal de fabricação.

### D5 — Três objetivos, três exercícios, um para um

Com 3 exercícios e a regra de que todo exercício rastreia a um objetivo, **5 objetivos deixam 2
sem evidência** — e o portão não pega, porque confere `exercício → objetivo` e nunca o inverso.

O trio é uma **progressão**, não três itens soltos:

| | Tipo | Objetivo |
|---|---|---|
| A | `formular` ou `resolver` — reconhecimento e mecânica | O1 |
| B | **`diagnosticar`** — um modelo errado que rodou e devolveu ótimo | O2 |
| C | `interpretar`, `escolher` ou `julgar` — *a conta está certa e a conclusão está errada* | O3 |

**O item B nunca pode ser cortado.** É o único que treina o erro que o Princípio II diz ser o caro
em Pesquisa Operacional — o de formulação. Um banco de 216 sem `diagnosticar` é um banco de
aritmética.

**Uma instância-fio por Parte**, não por capítulo — a montadora atravessa 07/08/09/10 e é metade
da razão de aqueles capítulos funcionarem.

### D6 — A prova sai do *long run*. É produto separado.

Os três disseram, independentemente. É o **único artefato genuinamente irreversível do plano
inteiro**: capítulo errado leva um `revert` e uma nota no histórico; nota errada leva um recurso
de aluno.

**Decidido agora (é grátis decidir cedo; caro decidir implicitamente):**

- A prova é **contexto separado** — registro próprio, endpoints próprios, retenção própria. Item
  de prova **nunca** entra em `livro/exercicios.json`, que é empacotado para o tutor e publicado.
- **Prova por Parte**, 12 questões (8 de cobertura + 4 integradoras valendo 50%), 90 minutos.
- **O código do aluno é opaco, entregue pelo professor** — não matrícula institucional, não CPF,
  não nome. O mapeamento mora na lista do professor, fora do sistema. Assim a nota existe e o
  anonimato do handbook sobrevive.
- Nenhum capítulo da v0 escreve item de prova; `capabilities.py` **não** ganha capacidade `prova`.

**Implementação em rodada própria, raia infra**, depois da v0 do núcleo.

### D7 — Escopo da v0

**Entra:** Partes I a IX (58 capítulos) + 2 módulos aplicados.
**Fica fora, declarado na página que o leitor lê:** Parte XI inteira (fronteira exige cláusula de
expiração e literatura viva — *"fronteira sem base é hype"* é frase do próprio `ROADMAP`), os
outros 11 módulos aplicados (a Parte X **cresce por adição por desenho**: um livro cuja camada
aplicada é infinita não tem v0 completa por definição), o par em inglês, e comparação de
desempenho onde não houver script.

### D8 — Ordem

```
Parte II (11–15) → 38 Convexidade → 77 Como ler um artigo → Parte I (01–06)
→ Parte III → Parte IV → 37 + Parte V → Parte VIII → Parte VII → Parte VI
→ Parte IX → 2 módulos da Parte X
```

Duas antecipações fora do mapa, ambas defendidas pela didática e aceitas:

- **38 (Convexidade) junto com a Parte II** — já está sendo usada a crédito: o capítulo 09 apoia
  a garantia de parada do Simplex inteiramente em convexidade. Tê-la escrita cedo permite que ~40
  capítulos **apontem** em vez de reexplicar. Maior economia de repetição do plano.
- **77 (Como ler um artigo) cedo** — é barato, não tem método, e dá ao resto do livro o direito
  de **citar em vez de explicar**. É o antídoto direto do risco de fabricação.

### D9 — Os dez sinais de parada obrigatória

Valem **mesmo sob a instrução "não pare"**. Ausência do autor não é autorização — é a condição
que torna a parada obrigatória.

1. Qualquer ato de **publicação** — merge na `main`, e **editar texto já publicado**.
2. **Conflito com a constituição** — o `CLAUDE.md` manda explicitar ao autor **antes de agir**.
3. Decisão de alcance maior que a rodada.
4. **Evidência que não vem** e a afirmação é objetivo declarado.
5. Build ou teste vermelho — **nunca "ajustar até ficar verde"**.
6. **Defeito de mesma classe pela segunda vez** — aí o defeito é do pipeline, não do artefato.
7. Revisão em contexto fresco **reprova**.
8. Risco de direito autoral ou de dado pessoal.
9. **Dívida crescendo mais do que encolhe** num lote.
10. Executor e revisor no mesmo contexto — o Princípio XI deixou de ser cumprível.

## Alternativas avaliadas

**Executar o pedido literal — 72 rodadas, padrão atual.** *Rejeitada.* O histórico mede a razão
real: 15 edições em 6 dias, das quais **4 são capítulos** — 1 rodada de capítulo puxa ~2,75 de
não-capítulo. Extrapolando: ~270 rodadas e ~324 mil palavras. E quebraria necessariamente III,
IV, VI, XI e XII, entregando um livro que **parece** completo — o resultado que o Princípio XII
classifica como pior do que a omissão.

**Publicar esqueleto vazio como quarto estado.** *Rejeitada.* A vaga ⬜ do mapa já é o esqueleto,
e já é honesta. Publicar esqueleto acrescenta um estado que não significa nada e **dilui a
honestidade do mapa**.

**Reduzir o piso de 3 exercícios ou dispensar o vídeo.** *Rejeitada.* É o Princípio I, não
negociável, e é a diferença entre handbook e apostila. O que se reduz é **ambição**, não padrão.

## Consequências

**Boas** — 14 rodadas em vez de 72; ~45 gates em vez de 216; o leitor sabe o que está lendo; a
Parte vira unidade com fio pedagógico; a história em lote acha ligação que a pesquisa isolada
perde.

**Custosas, e assumidas** — a v0 não é o livro inteiro (58 de 77 vagas); a maioria dos capítulos
nasce 🟡 e a promoção a ✅ é trabalho futuro; **o sinal de que a v0 está apodrecendo é `verificado`
parar de crescer enquanto `v0` cresce** — mais de 3 🟡 por ✅ obriga a próxima rodada a ser de
**promoção**, não de Parte nova.

## O que volta ao autor — quatro itens, e nenhum é delegável

1. **Ratificar o que está pendente.** ADRs 0007, 0009, 0010, 0011, 0012 e as specs 007 e 008
   estão "aguardando ratificação". Começar 14 lotes sobre fundação não assinada é o defeito de
   processo mais caro disponível.
2. **D1 emenda decisão fechada** — a cadência de um capítulo por rodada, de 2026-08-06.
3. **A promessa de anonimato publicada** ao leitor precisa ser reescrita antes de existir prova
   identificada. Não é emenda constitucional (a constituição é silente); é mudança de promessa
   **na cara do leitor**, o que é mais sério.
4. **O gate de merge continua não delegável.** Eu rascunho sem parar, em branch. Publicar é seu.
