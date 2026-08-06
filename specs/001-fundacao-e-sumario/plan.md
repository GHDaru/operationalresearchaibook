# Plan 001 — Fundação do handbook e primeira versão do sumário

**Especificação:** [`spec.md`](spec.md) · **Data:** 2026-08-06

## Constitution Check

Portão obrigatório antes da implementação. A constituição avaliada é a **ratificada nesta
rodada** (versão 1.0.0) — situação peculiar, e por isso cada princípio é avaliado contra o
estado em que a rodada **termina**.

| # | Princípio | Situação | Veredito |
|---|---|---|---|
| I | É um treino, não uma leitura | Nenhum capítulo de método é publicado; logo, nenhum exercício é devido | ✅ não se aplica, **dívida declarada** no histórico |
| II | Modelar antes de resolver | Regra codificada no esqueleto obrigatório do Guia Editorial | ✅ |
| III | Evidência acima de retórica | O estudo cita fontes verificadas e **declara três lacunas** em vez de escondê-las | ✅ |
| IV | Fonte-base é o experimento executável | `po-zero` entrega contrato e decisão de pilha, sem etapas | ⚠️ **dívida declarada**, fecha na rodada de Programação Linear (PL) |
| V | Arquitetura em três camadas | É o próprio objeto da rodada; formalizada no ADR 0004 | ✅ |
| VI | Atualização por Radar | `radar/RADAR.md` criado com vereditos, cadência e registro inicial honesto | ✅ |
| VII | Livro vivo | Todo documento datado; `HISTORICO.md` com a edição 0.1 e as dívidas | ✅ |
| VIII | Português canônico | Emendado nesta rodada via ADR 0002, com a dívida registrada por capítulo | ✅ |
| IX | Comunicação inteligível | Siglas abertas na primeira ocorrência de cada documento; glossário criado | ✅ |
| X | Direitos autorais | `materiais/README.md` + `.gitignore`; nenhum material de terceiros versionado | ✅ |
| XI | DoD verificável | Build e testes rodados, com saída colada na verificação | ✅ |

**Violações que impediriam a rodada:** nenhuma. As duas marcas ⚠️ são **dívidas declaradas**,
não violações silenciosas: ambas estão registradas no `HISTORICO.md` com a rodada em que fecham,
como o Princípio VII exige.

**Nota de processo (Maestro, Princípio II).** Quem executou não verifica. A revisão em contexto
fresco é gate desta rodada e cabe ao autor acioná-la antes do merge.

## Estratégia

Cinco blocos, nesta ordem — a ordem importa porque o motor precisa apontar para conteúdo que já
existe:

1. **Remover** o conteúdo herdado. Feito primeiro para que nada novo seja escrito ao lado do
   antigo.
2. **Pesquisar e decidir** — o estudo do corpo de conhecimento produz o recorte; as decisões do
   autor viram ADR.
3. **Escrever o mapa e o aparato** — o entregável central e o que o sustenta.
4. **Religar o motor** — sumário, siglas, capacidades do tutor, nomes dos artefatos, portões.
5. **Verificar** — build e testes, com a saída anexada.

## Decisões arquiteturais

Quatro, todas registradas como Architecture Decision Record (ADR):

- [ADR 0001](../../adr/0001-reuso-motor-livro-vivo.md) — reúso do motor de livro vivo.
- [ADR 0002](../../adr/0002-portugues-primeiro.md) — português canônico, inglês como dívida.
- [ADR 0003](../../adr/0003-stack-po-zero.md) — Python + PuLP/Pyomo + HiGHS.
- [ADR 0004](../../adr/0004-arquitetura-do-sumario.md) — arquitetura do sumário em três camadas.

## Mudanças de motor previstas

O motor foi herdado acoplado ao conteúdo anterior. Os acoplamentos conhecidos, e o que se faz
com cada um:

| Acoplamento | Tratamento |
|---|---|
| `sumario.json` aponta para os capítulos do livro anterior | Reescrito para a abertura + aparato do handbook |
| Nome do livro nos artefatos de download (`.md` e `.pdf` consolidados) | Renomeado; o portão que os confere passa a usar o novo nome |
| Mapa de siglas voltado a outro domínio | Substituído pelas siglas de Pesquisa Operacional (PO), espelhando o glossário |
| Registro de capacidades do tutor, específico do livro anterior | Reduzido ao que o handbook oferece hoje; cresce com os capítulos |
| Portão do grafo com contagem **fixa** de capítulos | Passa a derivar a contagem do sumário — a constante era dívida do motor, não regra |
| Portão de exercícios exige registro não vazio | Passa a aceitar vazio **apenas** enquanto não houver capítulo numerado além da abertura |
| Ilha interativa do livro anterior | Removida; o registro de componentes fica vazio até a primeira ilha de PO |

**Princípio que guia essas mudanças:** substituir constante por derivação sempre que possível.
Um portão que conta "15 capítulos" não estava medindo um invariante — estava registrando um
estado. Derivar do sumário é o que faz o portão continuar valendo quando o livro crescer.

## Riscos de implementação

| Risco | Mitigação |
|---|---|
| Enfraquecer um portão para fazer o build passar | Nenhuma condição é removida: as duas alteradas ficam **mais precisas** e se auto-restauram quando o livro crescer |
| Referência de capítulo em prosa apontando para vaga não publicada | O portão de referências cobre isso; o aparato refere-se a **partes**, não a números, enquanto não houver capítulo publicado |
| Link quebrado para página não incluída no sumário | O aparato novo entra no `sumario.json`; o build faz a verificação de links internos |
