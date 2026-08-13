---
name: longrun
description: O que "longrun" autoriza e o que continua fora dele. Use SEMPRE que o autor disser "longrun", "prossiga", "não pare" ou equivalente, e SEMPRE que uma decisão de médio ou alto impacto aparecer durante uma rodada autônoma. Define o rito do comitê de três especialistas cuja recomendação consolidada já nasce aprovada.
---

# Longrun — autonomia com rito, não autonomia sem freio

## Iron Law

```
EM LONGRUN, DECISÃO NÃO ESPERA O AUTOR — ELA PASSA PELO COMITÊ E VIRA ADR.
NENHUMA DECISÃO SEGUE SEM PARECER DE 3 ESPECIALISTAS E ADR REGISTRADO.
```

**Violar a letra desta regra é violar o espírito dela.** Isso NÃO é desculpa:

- *"É óbvio o que decidir"* — se fosse, não seria decisão de médio impacto. Convoque.
- *"O comitê ia concordar comigo"* — então o parecer sai barato. Convoque assim mesmo.
- *"Perguntar ao autor é mais seguro"* — em longrun, parar é o custo. O autor delegou o
  **julgamento**, não a **disciplina**: seguir sem comitê é desobedecer nos dois sentidos.

## O que "longrun" significa

O autor declarou, e está registrado: **toda decisão deste repositório é reversível e de baixo
impacto**, porque o trabalho vive em *branch* e voltar é `git checkout`. Em longrun, portanto, o
agente **não para para pedir permissão** — ele decide, registra e segue.

O que muda não é o rigor. É **quem** decide, e **como isso fica auditável**.

## O rito, quando aparece decisão de médio ou alto impacto

1. **Nomeie a decisão em uma frase**, com as opções concretas. Se você não consegue enunciá-la
   como escolha entre alternativas nomeadas, ainda não é uma decisão — é uma dúvida, e dúvida se
   resolve medindo.
2. **Convoque no mínimo três especialistas**, em contexto fresco, com **lentes diferentes**. A
   escolha das lentes é sua e deve caber ao caso. As que este repositório já usou com resultado:
   didática/editorial, conformidade constitucional, rigor técnico/medição, segurança, processo.
   **Três pareceres da mesma lente não são um comitê** — são um eco.
3. **Reconfira cada recomendação por medição própria antes de aceitar.** Especialista erra, e já
   errou aqui: um afirmou que um termo faltava no glossário e ele estava na linha 123. O parecer
   é insumo, não veredito.
4. **Consolide numa recomendação única**, dizendo o que sobreviveu à reconferência e **o que foi
   descartado, com o motivo**. Divergência entre pareceres é informação: registre-a.
5. **A recomendação consolidada já está aprovada.** Não espere confirmação.
6. **Registre em ADR** — contexto, alternativas, decisão, consequências boas **e ruins**, e o
   sinal que faria a decisão ser revista. Marque o estado como *decidida sob delegação de
   longrun; aguardando ratificação do autor*.
7. **Siga o desenvolvimento com a decisão registrada.**

## O que continua fora do longrun

A delegação é de **julgamento**, e não dissolve o que não é questão de permissão.

| Continua valendo | Por quê |
|---|---|
| **Build ou teste vermelho nunca vira verde por ajuste** (ADR 0013, D9.5) | Não é decisão a tomar: é integridade. Baixar limiar depois de ver o resultado é fraude, com ou sem delegação |
| **Quem executa não verifica** (Princípio XI) | Revisão em contexto fresco é o instrumento que pega o que o autor do texto não vê. Delegar a decisão não delega o ponto cego |
| **Direito autoral e dado pessoal** (D9.8) | Não é reversível por *branch*: a distribuição é que causa o dano. Foi o caso do Sci-Hub, recusado |
| **Fonte não confirmada não sustenta afirmação** (Princípio III) | Delegação não cria evidência |

> **O merge saiu desta lista em 2026-08-13, por decisão do autor** — constituição 1.2.0,
> [ADR 0015](../../../adr/0015-longrun-inclui-o-merge-ate-a-v0.md). **Enquanto a v0 não fechar**,
> o agente mergeia e publica sem esperar aprovação. A exceção **expira sozinha** ao fim da v0: não
> é preciso revogá-la, é preciso estendê-la.
>
> **O que isso cobra do resto.** Com o gate humano fora do caminho, a **revisão em contexto
> fresco** deixa de ser boa prática e passa a ser o **último olho independente antes de
> publicar** — nenhum lote vai à `main` sem ela, e nenhum vai com achado dela em aberto. É a
> troca que torna a delegação aceitável, e ela já provou que funciona: a revisão do lote 1
> reprovou, e o lote foi corrigido antes de publicar.

## O que é "médio ou alto impacto", na prática

Não é o tamanho do diff. É se a decisão **cria precedente** ou **muda o que o leitor recebe**.

| Convoca comitê | Decide sozinho |
|---|---|
| Mudar o que um selo significa, ou a régua de um portão | Escolher o nome de uma variável, a ordem de duas seções |
| Reproduzir formato de terceiro; escolher entre neutralidade e familiaridade | Corrigir erro de digitação, link quebrado, número que o script desmente |
| Antecipar um capítulo fora da ordem declarada | Escrever o capítulo que a ordem já mandava |
| Emendar spec ou ADR já registrada | Cumprir spec já registrada |
| Aceitar dívida nova que não tem prazo | Quitar dívida que já estava declarada |

**Na dúvida, convoque.** O parecer custa minutos; o precedente errado custa rodadas.

## O sinal de que o longrun está apodrecendo

Um só, e ele é aritmético: **rodada que fecha sem nenhum `⏳`, sem nenhum resultado negativo e
sem nenhuma dívida nova é suspeita**, não exemplar. Trabalho honesto em escala produz lacunas.
Ausência total delas costuma significar que alguém parou de procurar.
