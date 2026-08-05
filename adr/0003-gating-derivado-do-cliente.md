# ADR 0003 — Gating derivado do cliente (dívida aceita)

- **Status:** aceito com prazo de revisão
- **Data:** 2026-08-01
- **Rodada:** 7 (`specs/005-exercicios-via-chat`)

## Contexto

O tutor libera capacidades conforme o capítulo em que o leitor está. Esse capítulo
chega no corpo da requisição, declarado pela página — e a página roda no navegador do
leitor.

O padrão APH, estudado em `estudos/003-protocolo-aph-para-exercicios.md`, classifica
isso como o nível **domínio** do contexto, e é explícito: *"o cliente informa a tela, o
servidor sabe quem é"*. Nível domínio deveria ser composto no servidor, nunca aceito do
cliente.

## Decisão

**Aceitar a dívida**, declarando-a, enquanto o livro for anônimo.

Um leitor pode enviar `capitulo: 99` e destravar capacidades que o livro ainda não
ensinou. As consequências:

- **Não há escalada de privilégio**: não existe conta, papel nem dado de outro leitor a
  alcançar. As tools liberadas são busca no próprio livro, cálculo aritmético em sandbox
  e registro de tentativa na própria sessão.
- **O dano é pedagógico e recai sobre quem o causa**: o leitor recebe a ferramenta antes
  de aprender o conceito, e estraga a própria progressão.

## O que **não** ficou no cliente

A distinção importa, e é o que torna a dívida aceitável:

| Decisão | Onde mora | Por quê |
|---|---|---|
| Qual capítulo | **cliente** (esta dívida) | anônimo, sem dado a proteger |
| Qual exercício está em foco | cliente declara o **id**; o servidor resolve o resto | o leitor não forja exercício inexistente |
| Enunciado e **critérios de avaliação** | **servidor** | o leitor não deve poder ler nem alterar a rubrica pela qual é avaliado |
| Em qual exercício a tentativa é registrada | **servidor**, pelo foco declarado | o modelo não registra tentativa de outra página |
| Sessão do registro | **servidor**, do contexto do turno | nunca dos argumentos do modelo |

Ou seja: o que o cliente decide é o **ritmo**; o que o servidor decide é **a verdade**.

## Revisão obrigatória

Esta decisão **expira** quando qualquer uma destas condições aparecer:

1. houver conta de leitor (identidade real);
2. o progresso valer certificado, nota ou qualquer consequência externa;
3. houver dado de terceiro alcançável a partir da sessão.

Nesse momento, o capítulo passa a ser derivado no servidor a partir da identidade e do
progresso registrado — que, a partir desta rodada, já existe na tabela de tentativas.

## Consequência aceita

Enquanto valer, as métricas de progresso incluem leitores que pularam capítulos. Ao
analisar mastery por conceito, considerar isso — a série não é de leitores que
necessariamente passaram pela trilha.
