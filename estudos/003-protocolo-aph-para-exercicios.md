# Protocolo APH aplicado ao fluxo de exercício

> **Data da captura:** 2026-08-01 · **Fonte:** `GHDaru/protocolos` (livro vivo
> "Protocolo de Comunicação Aplicação ↔ Harness", padrão APH v0.2)
> **Motivação:** desenhar o fluxo *"o livro injeta a pergunta no chat → o leitor
> responde → o chat dá feedback → o exercício é registrado"* sobre um contrato já
> existente, em vez de inventar um.

---

## 0. Mapa do que existe no repositório-fonte

| Artefato | Path em `protocolos` | Natureza |
|---|---|---|
| Padrão normativo APH v0.2 | `livro/padrao-aph.md` | requisitos DEVE/DEVERIA/PODE, 3 níveis de conformidade |
| Anexo A — wire format | `livro/padrao/anexo-a-wire-format.md` | formato exato das mensagens + superfície HTTP de referência |
| Schemas validáveis | `livro/padrao/schemas/{evento,snapshot,acao-catalogo,confirmacao,erro}.schema.json` | JSON Schema draft 2020-12, `additionalProperties: false` |
| Exemplos verificados por CI | `livro/padrao/schemas/exemplos.json` | válidos + contraexemplos, gate `publicar/valida-wire.mjs` |
| Capítulos-fonte | `livro/capitulos/02` (transporte), `03` (eventos), `04` (contexto), `05` (ações), `06` (UI), `07` (segurança), `09` (federação) | prosa + evidência por path |
| Handoffs executáveis | `handoffs/ghdaru-spec-integridade-confirmacao.md`, `handoffs/ghdaru-roteiro-conformidade-aph-nivel2.md` | o segundo é auditoria requisito-a-requisito com esforço estimado |

Ponto de partida conceitual: **duas direções assimétricas.** `app→IA` é *descrição*
(snapshot + catálogo); `IA→app` é *ação mediada* (eventos tipados; toda intenção passa
por um interpretador soberano da aplicação). **"O modelo propõe; a aplicação dispõe."**

---

## 1. Snapshot de Contexto — como a aplicação descreve seu estado

Normativo §4.3 (APH-3.1 a 3.5) · Capítulo `04-contexto-de-tela.md` · Schema `snapshot.schema.json`

### Estrutura canônica (schema fechado)

```
{screen{id, route, title?}, fields[]?, selected_entity?, domain?,
 conversation?, context_hash?, captured_at?}
```

Só `screen` é obrigatório, e dentro dele `id` + `route`. `fields[].type` é enum fechado:
`text | number | boolean | date | select | entity | other`. `selected_entity` exige
`type` + `id`. Todos os níveis fechados têm `additionalProperties: false` — há um
contraexemplo (`senha_vazada`) no repositório justamente para provar que campo
desconhecido é rejeitado na borda.

### Os três níveis — e a *fonte* de cada um

| Nível | Pergunta | Autoridade | Conteúdo |
|---|---|---|---|
| 1 — Domínio | quem / onde / com que permissão | **servidor** | tenant, papel, módulos habilitados |
| 2 — Interface | o que o usuário está vendo | **cliente**, derivado do catálogo semântico | `screen.id`, `screen.route`, campos e estados |
| 3 — Conversa | o que já foi dito / o que falta | **servidor** | intenção detectada, proposta pendente, campos faltantes |

A formulação da fonte: *"o cliente informa a tela, o servidor sabe quem é"*. **O cliente
nunca é perguntado sobre permissões.** É a linha que mais nos afeta — ver a dívida em §8.

### `context_hash` e sanitização

`context_hash` é maturidade **desenhada**, não comprovada (APH-3.4 é DEVERIA): SHA-256 do
JSON canônico sanitizado, `sort_keys=True`, truncado a 16 hex, **calculado no servidor**.
O repositório documenta uma divergência tripla real (cliente com 8 hex por hash 31-based,
schema exigindo 16, backend com SHA-256 truncado) — as três definições nunca casariam. A
lição registrada: *"hash de contexto calculado no cliente é promessa, não garantia"*.

Sanitização (APH-3.3) é obrigatória e no servidor, por duas estratégias compostas:
denylist recursiva por substring (`password`, `senha`, `secret`, `token`, `credential` —
pega `accessToken` sem tê-lo previsto) e default-deny (passa só o que existe na definição
da tela e não está marcado como sensível). Teto de tamanho: **< 32 KB**.

### Como diria "o leitor está no exercício X do capítulo 02"

O padrão já tem o campo certo — `selected_entity`:

```json
{
  "screen": {
    "id": "capitulo.exercicio",
    "route": "/02-causa-e-efeito#ex-03",
    "title": "Capítulo 02 — Exercício 3"
  },
  "fields": [
    {"name": "capitulo", "type": "number", "value": 2},
    {"name": "modo", "type": "select", "value": "progressivo"},
    {"name": "tentativa_n", "type": "number", "value": 1}
  ],
  "selected_entity": {
    "type": "exercicio",
    "id": "cap02.ex03",
    "label": "Testar uma conexão 'se… então…'"
  },
  "captured_at": "2026-08-01T14:03:00Z"
}
```

**O que não está aí: o enunciado.** A página envia o identificador; o servidor resolve o
enunciado num registro próprio. O leitor não consegue forjar um exercício inexistente, e o
enunciado não paga tokens de ida e volta.

---

## 2. Catálogo de Ações — o que o agente pode fazer

Normativo §4.4 (APH-4.1 a 4.4) · Capítulo `05-acoes-governadas.md`

```
{action_id, title, description?, risk, input_schema, ui_route?, intent_keywords?, reversible?}
```

`action_id` segue `^[a-z][a-z0-9_.]*$`. `risk` é string aberta — **cada aplicação declara
sua taxonomia**.

- **APH-4.1** (DEVE): o catálogo é a **única superfície executável**. "O que não está
  declarado, a IA não faz."
- **APH-4.2** (DEVE): id, título, `input_schema` (JSON Schema) e classe de risco.
- **APH-4.3** (DEVE): **derivado das permissões reais na composição** — a IA nunca enxerga
  o que está desabilitado. A governança começa na composição do inventário, não numa
  checagem posterior.
- **APH-4.4** (DEVERIA): o mesmo `input_schema` vira a *tool* do modelo. O Anexo A chama
  isso de **"uma fonte, três projeções"**: valida os argumentos, vira tool de function
  calling e, no Nível 3, vira tool MCP.

> **Nota que nos favorece:** as duas bases-laboratório do livro pararam na mesma linha —
> catálogo pronto, nenhum caminho de código que o entregue ao modelo (lacuna L4, "a
> alavanca das demais"). **Nosso `chat-companion` já atravessou essa ponte**
> (`tools.py` → `schemas_para()`, com gating por capítulo). É vantagem real sobre os dois
> laboratórios.

---

## 3. Eventos tipados e SSE — o vocabulário IA→app

Normativo §4.1 e §4.2 · Capítulos `02` e `03` · Schema `evento.schema.json`

Envelope: `{seq, kind, payload}` — `seq` inteiro ≥ 1, monotônico por sessão, **atribuído
no servidor antes da emissão**; `kind` de enum fechado. Frame SSE de linha única:

```
data: {"seq":1,"kind":"content","payload":{"text":"Olá"}}\n\n
```

### Vocabulário completo da v0.2

| `kind` | Payload mínimo | Semântica |
|---|---|---|
| `content` | `{text}` | pedaço do texto da resposta |
| `thinking` | `{text}` | pedaço do raciocínio exibível |
| `action_proposal` | `{proposal_id, action_id, risk, requires_confirmation}` | a IA propõe uma ação do catálogo |
| `action_result` | `{proposal_id, status}` | `executed \| failed \| denied \| cancelled \| expired \| stale` |
| `ui_command` | `{command}` + `args` | comando declarativo executado pelo host |
| `citation` | `{source_id}` + `title`, `url`, `excerpt` | fonte de uma afirmação (quando há RAG) |
| `error` | `{code, message, details?}` | falha com código estável |
| `done` | `{}` + `usage` | terminador; alimenta o metering |

### Regras que protegem o vocabulário

- **APH-2.1**: vocabulário **fechado**, versionado. `citation` é DEVERIA quando houver RAG.
- **APH-2.2**: evolução assimétrica — **"o consumidor ignora tipos desconhecidos; o
  produtor documenta antes de emitir"**.
- **APH-2.3**: o domínio nunca vê formato bruto de provedor; um normalizador converte.
- **APH-2.5**: **apresentação é função do vocabulário, nunca parte dele.**

### Transporte

- **APH-1.1**: SSE sobre POST (`EventSource` só faz GET, e o protocolo precisa mandar
  corpo com mensagem + snapshot).
- **APH-1.2/1.3**: `seq` no servidor + replay `?after=N` + dedup no cliente. Racional: *no
  chat, o que trafega é a conversa — perder eventos é perder o produto*.
- **APH-1.4**: cancelamento **cooperativo**, nunca silêncio.
- **APH-1.5**: erros são protocolo, com códigos estáveis em `MAIUSCULAS_COM_SUBLINHADO`.
  **"A mensagem é para o humano; o código é para o programa."**

### Superfície HTTP de referência

Os *corpos* são normativos; os *paths*, referência.

| Operação | Path | Corpo → Resposta |
|---|---|---|
| Criar sessão | `POST /aph/sessions` | `{}` → `{"session_id"}` |
| Enviar mensagem | `POST /aph/sessions/{id}/messages` | `{"text","snapshot"}` → stream SSE |
| Replay | `GET /aph/sessions/{id}/events?after=N` | → array JSON |
| Decidir proposta | `POST /aph/sessions/{id}/proposals/{pid}` | Confirmação → `{"proposal_id","status"}` |
| Cancelar stream | `DELETE /aph/sessions/{id}/stream` | → 204 |
| Catálogo | `GET /aph/catalog` | → array já filtrado por permissão |

---

## 4. Proposta de ação e a FSM

Normativo §4.5 (APH-5.1 a 5.5) · Capítulo `05-acoes-governadas.md`

### FSM de referência

```
proposed → awaiting_approval → confirmed → executing
        → executed | failed | cancelled | denied | expired | stale
```

**"Subconjuntos PODEM ser usados; transições fora da tabela DEVEM falhar."**

### Os quatro momentos da ação governada

1. **Proposta** — nada executa quando o modelo menciona. Nasce objeto de domínio com
   identidade e transições validadas em código.
2. **Confirmação proporcional ao risco (APH-5.2)** — decidida **fora do modelo e antes da
   conversa**. *"O modelo escolhe qual ação propor; nunca escolhe quanto de governança ela
   recebe."*
3. **Execução** — sempre pela aplicação.
4. **Resultado / traço (APH-5.5)** — 100% das ações executadas *e das recusadas por
   política* deixam traço. **"Sem traço, a ação é considerada não-governada e é
   rejeitada"** — o traço é pré-condição, não subproduto.

### Mecanismos desenhados (ainda não comprovados)

- **APH-5.3** `idempotency_key` com dedup real. Contraexemplo instrutivo: num laboratório
  a chave viaja no contrato mas é apenas armazenada; a dedup efetiva continua sendo a FSM.
- **APH-5.4** comparação de `context_hash` → estado `stale`, sem execução.

O handoff `ghdaru-spec-integridade-confirmacao.md` é a spec pronta dos dois acidentes
clássicos do gate humano: **o clique duplo** e **a tela que mudou**.

### Insight sobre traço adaptativo

*"O traço é o que permite **relaxar** os gates com o tempo. Uma ação hoje `confirm` pode,
com histórico de execuções corretas, ser rebaixada a execução direta — decisão impossível
sem o registro. Governança sem traço é chute; com traço, é política ajustável por
evidência."*

---

## 5. Comandos de UI declarativos

Normativo §4.6 · Capítulo `06-comandos-de-ui.md`

- **APH-6.1**: vocabulário fechado — `navigate`, `fill_fields`, `focus_field`, `submit`,
  `open_resource`, `clarify`. **Nunca cliques simulados, coordenadas ou DOM.**
- **APH-6.2**: **todo comando exige um executor no host.** O executor de referência tem
  oito linhas. *"Comando sem executor é cartão morto e não conta para conformidade."* Um
  dos laboratórios é a prova por ausência: taxonomia rica, política, FSM, botões — e o
  usuário confirma e nada acontece na tela.
- **APH-6.3**: a linha executa-direto × propõe-e-confirma é traçada pela
  **reversibilidade**, por política server-side **por tipo de ação** — não é função
  mecânica do risco.
- **APH-6.4** (desenhado): **slot filling estruturado** — pedido com JSON Schema,
  formulário renderizado pela aplicação. O livro define como *"um comando de UI ao
  contrário"*.
- **APH-6.5**: **sem UI serializada gerada pelo modelo em produção.** A forma madura de
  generative UI é *"dados estruturados para componentes que o app já possui"*.

---

## 6. Manifesto de Aplicação (Nível 3)

Normativo §4.9 · Capítulo `09-federacao-composicao.md`

Documento com que uma aplicação de terceiro se apresenta antes de ser embutida. Decisão
estruturante *negativa*: descartar um protocolo de integração separado — **o contrato da
federação é o mesmo contrato da IA.**

Cinco elementos: identidade, marca, camada semântica (snapshot + catálogo), design system
e **auditoria** (traço para 100% das ações — sem traço, ação rejeitada). Regra
unidirecional: todo terceiro começa no Nível 3 (headless) e sobe ao Nível 2 (federado) com
manifesto revisado e iframe sandbox.

> Detalhe relevante: o capítulo 09 nomeia o **TOC Builder** como candidato de estreia da
> federação. Se um dia ele for embutido, é este manifesto que se preenche. Hoje, não.

---

## 7. Injeção de contexto a partir da página

Não há capítulo com esse nome; o mecanismo está em três lugares:

1. **O snapshot viaja com cada mensagem** (APH-3.2). O corpo é literalmente
   `{"text": "...", "snapshot": {...}}`.
2. **A página empurra pelo registro, não pelo texto.** Só o nível interface vem do
   cliente, derivado do catálogo semântico — nunca do DOM cru. O sanitizador consulta a
   definição da tela e descarta campo que o registro não conhece.
3. **A regra de segurança que governa a injeção (APH-7.1):** o snapshot entra como
   **mensagem de sistema separada e rotulada**, nunca misturado ao texto do usuário.
   > *"Concatenar tudo num prompt gigante não é só deselegante — é destruir a estrutura da
   > qual toda defesa posterior depende."* Só dá para sanitizar "o snapshot" se ele é um
   > objeto identificável; só dá para auditar "que contexto originou esta proposta" se o
   > contexto tem identidade.

---

## 8. Recomendação para este livro

### O que já temos (e é mais do que os laboratórios do livro-fonte)

| Peça do APH | Estado no `chat-companion` | Path |
|---|---|---|
| SSE sobre POST (APH-1.1) | **conforme** | `app.py` `chat_stream()` |
| Catálogo → tools do modelo (APH-4.4) | **conforme** — a lacuna que nenhum laboratório atravessou | `tools.py` `schemas_para()` + `loop.py` |
| Catálogo derivado de permissões (APH-4.3) | **conforme** — o gating por capítulo é exatamente isso | `capabilities.py` `tools_ativas()` |
| Separação de camadas (APH-7.1) | **parcial** — persona, capacidades e RAG concatenados num prompt só | `app.py` `_system_prompt()` |
| Porta única de LLM (APH-8.1) | **conforme** | `llm.py` `make_llm()` |
| Traço | **parcial** — `trace` volta na resposta, não é persistido | `app.py` |
| Vocabulário de eventos (APH-2.1) | **ausente** — hoje `{delta}`/`{trace}`/`{done}`/`{erro}`, sem `kind` nem `seq` | `app.py` |
| Snapshot estruturado (APH-3.2) | **ausente** — `chapter` e `mode` achatados no `ChatIn` | `app.py` |
| Proposta / FSM / traço persistido | **ausente** | — |

### O subconjunto mínimo — seis entregas

**E1 — Snapshot mínimo + registro de exercícios no servidor.** Trocar `chapter`/`mode`
achatados por um `snapshot` conforme o schema. Um `exercicios.json` gerado pelo
`build_corpus.py` a partir dos capítulos, com `{exercicio_id, capitulo, titulo, enunciado,
criterios[], capacidade_requerida}`. O enunciado nunca viaja do cliente; o servidor o
resolve pelo id e o injeta como mensagem system separada:

```python
history = [
    {"role": "system", "content": PERSONA + capacidades + modo},
    {"role": "system", "content": f"Exercício em foco (declarado pela página): {json.dumps(ex)}"},
    {"role": "system", "content": f"Contexto de tela (sanitizado): {json.dumps(safe_snapshot)}"},
    {"role": "system", "content": f"Trechos do livro (RAG): …"},
    *historico,
]
```

Isso resolve dois problemas de uma vez: *"o livro injeta a pergunta"* deixa de ser uma
mensagem falsa no transcript e vira declaração de foco; e a camada 1 de segurança passa de
parcial a conforme.

**E2 — Catálogo com duas ações**, projetado como tool (reusa `tools.py` inteiro):

```json
[
  {"action_id": "exercicio.registrar_tentativa", "risk": "write", "reversible": true,
   "input_schema": {"type":"object","required":["exercicio_id","veredito"],
     "properties":{"exercicio_id":{"type":"string"},
                   "veredito":{"enum":["aprovado","parcial","refazer"]},
                   "criterios_atendidos":{"type":"array","items":{"type":"string"}},
                   "resumo_feedback":{"type":"string","maxLength":600}}}},
  {"action_id": "capitulo.marcar_concluido", "risk": "confirm", "reversible": false,
   "input_schema": {"type":"object","required":["capitulo"],
     "properties":{"capitulo":{"type":"integer","minimum":0}}}}
]
```

Taxonomia de risco recomendada: **`read | write | confirm`** — `read` (busca no livro)
executa direto; `write` (registrar tentativa: dado da própria sessão, reversível) executa
direto **e deixa traço**; `confirm` (marcar capítulo concluído: muda a progressão e o
gating) para no gate humano. Derivação por permissão: `exercicio.registrar_tentativa` só
entra no catálogo se `snapshot.selected_entity.type == "exercicio"`.

**E3 — Envelope `{seq, kind, payload}` com 6 dos 8 `kind`:** `content`, `citation`,
`action_proposal`, `action_result`, `error`, `done`. Fora: `thinking` (não expomos
raciocínio) e `ui_command` (ver abaixo).

> **`citation` é o ganho imediato.** Já computamos `achados` com fonte, título e trecho — e
> jogamos fora. Emitir o evento custa cinco linhas e é exatamente a capacidade que a
> persona exige ("citando o trecho do livro entre colchetes"). Nenhum dos dois laboratórios
> do livro-fonte tem `citation` com fonte real.

**E4 — FSM reduzida a 5 estados** (subconjunto explicitamente permitido):

```
proposed → executed | failed                                    (read | write)
proposed → awaiting_approval → confirmed → executed | cancelled (confirm)
```

Substitutos baratos dos dois mecanismos desenhados: em vez de `context_hash`, comparar
`args.exercicio_id` com `snapshot.selected_entity.id` no momento da execução; em vez de
`idempotency_key`, chave natural `(session_id, exercicio_id, tentativa_n)` com
`ON CONFLICT DO NOTHING`.

**E5 — O traço como tabela de progresso.** Nova porta no `StorePort`
(`registrar_tentativa`, `progresso`) + `GET /progresso?session_id=`. Neste produto, **traço
e dado de domínio coincidem** — o registro da tentativa *é* o traço. `delete_session` tem
que apagar as tentativas junto.

**E6 — A página reage.** Ao receber `action_result` com `status: "executed"`, o widget
refaz `GET /progresso` e atualiza o selo do exercício. **Sem `ui_command`.**

### O que é over-engineering nesta fase

| Peça | Por quê |
|---|---|
| `ui_command` + executor | Nenhum passo do fluxo pede que o agente mude a tela. *"Comando sem executor é cartão morto."* Não declarar no vocabulário enquanto não houver executor |
| `context_hash` | Desenhado, com divergência tripla documentada na fonte. Comparar `exercicio_id` entrega quase todo o valor |
| `idempotency_key` | Desenhado. Chave natural com `ON CONFLICT` resolve |
| Estados `stale`, `expired`, `denied`, `executing` | Subconjuntos são autorizados; `expired` só faz sentido com TTL de proposta pendente |
| Replay `?after=N` | Nada no fluxo depende dele. Fazer o `seq` agora (um inteiro), o endpoint depois |
| Cancelamento cooperativo | Feature de UX ("botão parar"), não do fluxo de exercício |
| Slot filling estruturado | Desenhado, e para um tutor socrático **perguntar em prosa é o produto**, não defeito |
| Manifesto, handshake, iframe | Nível 3, para plataformas que embutem apps de terceiros |
| Projeção MCP / protocolo externo | A ordem do roadmap da fonte é *tool calling → slot filling → MCP → externo*; já estamos no passo 1 |

### Ordem de execução

1. **E1** (snapshot + registro + system messages separadas) — destrava tudo.
2. **E3** (envelope tipado + `citation` + códigos de erro) — independente, ganho imediato.
3. **E2** (catálogo com duas ações) — reusa `tools.py`/`capabilities.py`.
4. **E5** (tabela de tentativas + `GET /progresso`) — a persistência.
5. **E4** (FSM reduzida + endpoint de confirmação).
6. **E6** (widget reage).

Fase 2, se e quando doer: `seq` + replay completo, cancelamento cooperativo, `ui.navigate`
com executor, `context_hash` canônico no servidor.

---

## 9. Dívida a registrar em ADR

O `capitulo` vem do **cliente**, e é ele que decide o gating. No APH isso é o nível
*domínio*, que **DEVERIA ser composto no servidor** — *"o cliente informa a tela, o
servidor sabe quem é"*. Num livro público anônimo, um leitor pode enviar `capitulo: 99` e
destravar o modo avançado.

Não é falha grave — o dano é ele estragar a própria pedagogia, e não há identidade nem
dado sensível envolvido. Mas é a mesma categoria do contraexemplo instrutivo que o
capítulo 07 da fonte usa. **Dívida visível é desenho; dívida silenciosa é bug.** Registrar:
*"gating derivado do cliente — aceito porque não há identidade nem dado sensível; revisar
se houver conta de leitor"*.

---

## 10. Modelos de método a reaproveitar

Dois documentos da fonte servem de gabarito para o nosso processo:

- `handoffs/ghdaru-roteiro-conformidade-aph-nivel2.md` — auditoria requisito-a-requisito
  com placar, esforço P/M/G e uma seção **"O que NÃO fazer (economia de esforço)"**.
- `padrao-aph.md` §7 — checklist de autoavaliação com evidência por path.
