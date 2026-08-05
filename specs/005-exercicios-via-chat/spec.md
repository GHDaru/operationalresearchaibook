# Spec 005 — Exercícios via chat

> **Raia:** plena · **Rodada:** 7 · **Branch:** `007-exercicios-via-chat`
> **Decisor:** Gilsiley Darú · **Status:** aguardando gate humano
> **Fundamentação:** `estudos/003-protocolo-aph-para-exercicios.md`

## Intenção

Fechar a maior lacuna do livro: o **Princípio I** exige que todo capítulo tenha prática
com devolutiva, e hoje há **um objeto interativo em onze capítulos** — e o tutor não
propõe, não corrige e não registra exercício nenhum.

O fluxo pedido pelo autor:

> O livro injeta a pergunta no chat → o leitor responde → o chat dá feedback → o
> exercício é registrado.

## Por quê

O tutor já sabe conversar sobre o livro, mas o leitor precisa **decidir** conversar. O
exercício inverte a iniciativa: a página oferece a prática, e o chat vira o lugar onde ela
acontece — com o guardrail socrático já em produção garantindo que a devolutiva não vire
resposta pronta.

E há a diferença que o estudo do protocolo tornou explícita: sem registro, não há
progresso. Com registro, o livro passa a saber o que o leitor domina — insumo do
monitoramento por IA (Fase 5 do roadmap original).

## Escopo

### Entra

1. **Registro de exercícios no servidor** (`exercicios.json`, gerado a partir dos
   capítulos): `{exercicio_id, capitulo, titulo, enunciado, criterios[], capacidade}`.
   **O enunciado nunca viaja do cliente** — a página manda só o identificador; o servidor
   resolve. O leitor não forja exercício inexistente, e o enunciado não paga tokens.
2. **Snapshot de contexto** no `/chat`, conforme o padrão APH: a página declara
   `screen`, `selected_entity = {type: "exercicio", id: "cap02.ex03"}` e `fields`.
   Substitui os campos `chapter`/`mode` achatados.
3. **Camadas de prompt separadas** — persona, exercício em foco, contexto de tela e
   trechos do RAG entram como mensagens de sistema **distintas e rotuladas**, nunca
   concatenadas ao texto do leitor. Fecha a camada 1 de segurança do padrão.
4. **Catálogo de ações** com duas entradas, projetadas como ferramentas do modelo pelo
   mecanismo que já existe:
   - `exercicio.registrar_tentativa` (risco `write`, reversível) — executa direto e deixa
     traço;
   - `capitulo.marcar_concluido` (risco `confirm`) — para no gate humano.
5. **Traço persistido** — tabela de tentativas no Postgres + `GET /progresso`.
   Neste produto, traço e dado de domínio coincidem: o registro da tentativa **é** o
   traço de execução.
6. **Botão "Praticar no tutor"** nos exercícios do livro, que abre o chat com o exercício
   em foco declarado.
7. **Selo de progresso** no exercício da página, alimentado por `GET /progresso`.

### Não entra (registrado como fase 2)

`ui_command` e executor no host (nenhum passo pede que o agente mude a tela);
`context_hash` (comparar `exercicio_id` entrega quase todo o valor); `idempotency_key`
(chave natural com `ON CONFLICT` resolve); estados `stale`, `expired`, `denied`,
`executing`; replay `?after=N`; cancelamento cooperativo; slot filling estruturado —
para um tutor socrático, **perguntar em prosa é o produto**, não defeito.

## Critérios de aceite (verificáveis)

| # | Critério | Como verificar |
|---|---|---|
| CA-1 | O enunciado não vem do cliente | `POST /chat` com `exercicio_id` inexistente → 400, sem chamar o modelo |
| CA-2 | O enunciado chega ao modelo como mensagem de sistema própria | teste inspeciona as mensagens montadas: ≥ 2 `role: system`, uma delas com o enunciado |
| CA-3 | A ação só existe com exercício em foco | sem `selected_entity`, `exercicio.registrar_tentativa` fora das tools |
| CA-4 | A tentativa é persistida | `POST /chat` que registra → `GET /progresso` devolve a tentativa |
| CA-5 | Dedup de clique duplo | duas tentativas com a mesma chave natural → um registro |
| CA-6 | `marcar_concluido` não executa sem confirmação | proposta fica `awaiting_approval`; sem confirmar, nada muda |
| CA-7 | Esquecimento | `DELETE /session/{id}` apaga também as tentativas |
| CA-8 | Guardrail preservado | pedido de resposta pronta segue recusado |
| CA-9 | Sem JS, a página continua legível | exercício visível sem o botão |
| CA-10 | Nada regride | build verde, portão verde, testes verdes |

## Dívida a registrar em ADR

O capítulo vem do **cliente** e é ele que decide o gating. No padrão APH isso é nível
*domínio*, que deveria ser composto no servidor. Num livro público anônimo, o leitor pode
enviar `capitulo: 99` e destravar o modo avançado — o dano é ele estragar a própria
pedagogia, sem identidade nem dado sensível em risco. **Dívida visível é desenho; dívida
silenciosa é bug.** Revisar quando houver conta de leitor.
