# Materiais de terceiros — política

> **Conteúdo revisado em 2026-08.** O que pode e o que não pode entrar no repositório.

Este diretório existe para deixar a regra visível no lugar onde a tentação aparece. Ele
**não contém material de terceiros** — e não vai conter.

## A regra

O texto do handbook é **autoral**. Livros-texto, apostilas, listas de exercícios e slides de
terceiros **não são reproduzidos neste repositório** — nem como arquivo, nem como imagem, nem
como trecho longo transcrito (constituição, Princípio X).

Isso vale inclusive para obras que o autor comprou. Ter a licença de **ler** um livro não é ter
a licença de **redistribuí-lo** — e um repositório público é redistribuição.

## O que pode ser versionado

| Pode | Exemplo |
|---|---|
| **Metadados bibliográficos** | Autor, título, edição, editora, ano, ISBN, DOI |
| **Mapa de correspondência** | "A vaga *Dualidade* do handbook corresponde à unidade X da obra Y" |
| **Citação curta com atribuição** | Uma frase ou definição, entre aspas, com fonte e localização |
| **Referência a exercício** | "Exercício 4.12 da obra Y" — a referência, não o enunciado |
| **Nota de leitura autoral** | O que *você* concluiu lendo, escrito com suas palavras |

## O que não pode, em nenhuma hipótese

| Não pode | Por quê |
|---|---|
| O arquivo da obra (PDF, EPUB, digitalização) | Redistribuição |
| Capítulos ou seções transcritos | Redistribuição |
| Figuras, tabelas e gráficos extraídos | Obra derivada sem licença |
| Enunciados de exercícios copiados | Redistribuição |
| Texto "parafraseado" que segue a obra frase a frase | Obra derivada; trocar palavras não cria autoria |

## Onde os materiais ficam, então

**Fora do versionamento.** Duas opções, nesta ordem de preferência:

1. **Fora do repositório** — na máquina do autor ou em armazenamento privado. É o padrão.
2. **Neste diretório, ignorado pelo Git** — `materiais/` está no `.gitignore` (exceto este
   `README.md`). Serve para trabalhar com os arquivos localmente sem risco de commit acidental.

Um repositório privado separado para materiais de estudo **já é a decisão vigente** — mesmo
padrão do livro *Teoria das Restrições*, que mantém os seus fora do repositório publicado. Ele
é **outro repositório**, privado, e nada dele é espelhado aqui.

> **Precedente registrado.** Em 2026-08-06 dois livros-texto em PDF chegaram a ser commitados
> na branch padrão deste repositório, que é público. Foram purgados do histórico, e a decisão
> — com o que se perde e o que não se desfaz — está no
> [ADR 0005](../adr/0005-materiais-em-repositorio-privado.md). A reescrita mudou os
> identificadores de todos os commits: clones anteriores àquela data divergem e precisam ser
> refeitos.

## Como anexar um livro-base ao projeto, na prática

Quando o autor quiser registrar um livro didático como base do curso:

1. **Anexe a obra na conversa** com o agente, ou deixe o arquivo em `materiais/` localmente.
2. O agente **lê** e extrai: metadados bibliográficos completos e a estrutura de unidades.
3. Entram no repositório, em `livro/bibliografia.md`: a ficha da obra e a **tabela de
   correspondência** com as vagas do [Mapa do handbook](../livro/mapa-do-handbook.md).
4. **Não entra:** o arquivo, o texto, as figuras, os enunciados.
5. Se um conceito da obra for usado no handbook, ele é **reescrito com autoria própria** e
   citado na primeira ocorrência.

O resultado é o que o autor precisa — um handbook alinhado ao livro que os alunos têm em mãos —
sem que o repositório vire uma cópia dele.

## Se houver dúvida

A regra prática: **se um advogado da editora abrir este repositório, ele encontra referências
ao livro dela ou pedaços do livro dela?** Se a resposta for a segunda, não commite.

Na dúvida, o conflito é explicitado ao autor antes de agir — nunca resolvido pelo agente por
conta própria.
