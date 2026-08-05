# Guia Editorial

> **Conteúdo revisado em 2026-08** · como este livro é escrito — método e regras.

Este documento é a regra de escrita do livro. Vale para o autor humano e para os agentes de IA que o apoiam.

## 1. O que este livro é

Um **treinamento** em forma de livro vivo. A unidade de valor não é o capítulo lido, é a habilidade exercitada. Toda decisão editorial se subordina a isso.

Consequência prática: um capítulo que explica bem mas não faz o leitor praticar está incompleto, por melhor que esteja escrito.

## 2. Método pedagógico

Quatro referenciais se combinam, cada um respondendo a uma pergunta diferente.

**Desenho retroativo (*backward design*)** — define **o que medir**. Escreve-se primeiro a evidência de domínio (o que o leitor deve conseguir fazer), depois a prática que produz essa evidência, e só então o texto. Por isso todo capítulo abre com objetivos de aprendizagem formulados com verbos verificáveis.

**Tarefas-íntegras com apoio decrescente (4C/ID)** — define **a sequência**. O leitor trabalha problemas completos desde cedo, com apoio que diminui: no capítulo 01 o exercício vem com alternativas e devolutiva; no capítulo 14 ele traz o próprio problema e se autoavalia.

**Arquitetura de conteúdo (Diátaxis)** — separa os quatro modos: tutorial (as lições), receita (o "mão na massa"), referência (glossário e bibliografia) e explicação (o "porquê" de cada seção). Não misturar modos na mesma seção é o que mantém os capítulos legíveis.

**Carga cognitiva** — governa o tamanho. Um assunto por seção; exemplo antes da abstração; nada de nota de rodapé que exija manter duas ideias na cabeça ao mesmo tempo.

A evidência que sustenta a escolha por prática intercalada (em vez de leitura ou vídeo contínuos) está documentada no estudo que originou o projeto, em `estudos/`.

## 3. Estrutura obrigatória de capítulo

Todo capítulo numerado segue este esqueleto:

1. **Título** e linha de datação (`> **Conteúdo revisado em AAAA-MM** · [histórico]`).
2. **Objetivos de aprendizagem** — 3 a 4 itens, verbo verificável em negrito.
3. **O problema** — a dor concreta que justifica o capítulo. Nunca começar pela definição.
4. **O conceito** — a exposição, com exemplo antes da abstração.
5. **Prática** — exercício, preferencialmente interativo.
6. **Erros comuns** — os modos de falha observados, cada um com o sinal que o denuncia.
7. **Mão na massa** — aplicação ao contexto do próprio leitor, encadeada com os capítulos vizinhos.
8. **Leitura executiva** — parágrafo final que resume o capítulo para quem já sabe.

Páginas de aparato (glossário, bibliografia, histórico, este guia) não seguem o esqueleto.

## 4. Regras de escrita

**Português com termos técnicos consagrados.** Não se traduz à força o que a área usa em outra língua (*Evaporating Cloud*); traduz-se o que já tem forma corrente em português (Nuvem, injeção, objetivo intermediário). Na primeira ocorrência, os dois.

**Frase curta, voz ativa, exemplo concreto.** Exemplos vêm de situações de trabalho reconhecíveis — prazo, fila, cliente, equipe — e não de abstrações genéricas.

**Sem promessa de resultado.** O livro descreve o que a ferramenta faz e em que condições. Não promete transformação.

**Sem jargão órfão.** Todo termo do método aparece no glossário. Um termo usado sem definição prévia é defeito.

**Uma ideia por parágrafo.** Se o parágrafo tem dois assuntos, são dois parágrafos.

## 5. Regras de conteúdo e fontes

**Toda afirmação sobre um conceito da TOC é rastreável.** A fonte primária vai na [Bibliografia](bibliografia.md) e é citada no texto na primeira ocorrência do conceito. Formulação autoral é sinalizada como tal.

**Materiais de terceiros não são reproduzidos.** Materiais de estudo do autor ficam em repositório privado; o livro publicado é texto autoral que os referencia por fonte oficial.

**Nenhum segredo em arquivo ou commit.** Credenciais apenas em `.env` fora do versionamento.

**Datação obrigatória.** Todo capítulo carrega a data da última revisão, e toda mudança relevante entra no [Histórico](HISTORICO.md).

## 6. Objetos interativos

Objetos interativos são o mecanismo central da prática. Regras:

- **Progressive enhancement.** Sem JavaScript, a página mostra o mesmo conteúdo em forma estática. Um objeto que deixa a página vazia quando falha é defeito.
- **Devolutiva imediata e explicativa.** Não basta dizer "errado" — o objeto explica por quê, na linguagem do capítulo.
- **Erro barato.** O leitor deve poder errar sem custo e repetir à vontade.
- **Um objetivo por objeto.** Objeto que exercita duas coisas ao mesmo tempo não ensina nenhuma.

Implementação: ilhas React em `publicar/viz/`, montadas em `<div data-viz="...">`.

## 7. Processo

O livro segue a metodologia **Maestro**: a especificação é a fonte de verdade, os agentes executam, o humano decide, aprova e verifica.

- Uma **spec por rodada**, cada rodada em sua **própria branch** (`NNN-nome`), com registro em `specs/NNN-nome/`.
- Decisões relevantes viram **ADR** em `adr/`.
- Portões verificáveis antes de concluir: build do site verde, verificação por página verde, testes do chat verdes. Vale a regra "prove, não declare" — a evidência é anexada, não afirmada.
- O merge na `main` é o que publica.
