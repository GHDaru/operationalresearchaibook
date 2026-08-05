# 13 — Análise de Pré-Requisitos

> **Conteúdo revisado em 2026-08** · edição inaugural · [histórico](../HISTORICO.md)
>
> Capítulo em primeira versão — a ser aprofundado com o material do autor.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve conseguir:

1. **Levantar** os obstáculos entre a situação atual e um objetivo;
2. **Converter** cada obstáculo em um **objetivo intermediário** formulado como estado concluído;
3. **Sequenciar** os objetivos intermediários por dependência, não por ordem de lembrança;
4. **Delegar** um objetivo intermediário sem transferir a ambiguidade junto.

## O problema

Você tem uma injeção — um estado que resolveria o problema. Falta transformá-la em algo que comece amanhã.

O caminho usual é fazer uma lista de tarefas. O problema da lista de tarefas é que ela nasce da ordem em que as coisas ocorreram a você, não da ordem em que precisam acontecer. E ela ignora justamente o que faz planos falharem: os obstáculos.

A Análise de Pré-Requisitos inverte isso. Em vez de perguntar "o que fazer?", pergunta:

> **O que impede** que isto já seja verdade hoje?

Os obstáculos deixam de ser motivo de desânimo e viram a matéria-prima do plano. Como escreveu Marco Aurélio, o que fica no caminho torna-se o caminho.

## O processo

### 1. Enunciar o objetivo

Uma frase, estado no presente. Geralmente é a injeção do capítulo 12 — mas serve para qualquer objetivo que hoje não se realiza.

### 2. Levantar obstáculos

Liste o que impede o objetivo de ser verdade **agora**. Escreva livremente: falta de recurso, resistência de pessoas, ausência de informação, restrição contratual.

Uma calibragem prática: **entre cinco e dez obstáculos**. Menos que cinco costuma significar que você pensou pouco. Mais que dez costuma significar que o objetivo é grande demais e deveria ser quebrado em planos menores, aninhados.

Não julgue a viabilidade agora — obstáculo intransponível também é informação, e às vezes é o próprio achado do exercício.

### 3. Converter obstáculos em objetivos intermediários

Para cada obstáculo, escreva o **estado** que o supera. Esse estado é um **objetivo intermediário** (OI).

A formulação é a mesma exigência do capítulo 07: OI é **estado concluído**, não tarefa.

| Obstáculo | ❌ Tarefa | ✅ Objetivo intermediário |
|---|---|---|
| Vendas não enxerga a fila | "Fazer reunião com TI" | "Vendas consulta a fila atualizada antes de prometer data" |
| Ninguém mantém a fila | "Definir responsável" | "A fila tem um responsável que a atualiza diariamente" |
| Regra atual proíbe | "Falar com o jurídico" | "A norma permite consulta direta à fila pela equipe comercial" |

A diferença é verificável na prática: você consegue olhar para um estado e dizer se ele já é verdade. Uma tarefa apenas foi feita ou não — e "foi feita" não garante que o obstáculo caiu.

Um teste útil: o OI é **suficiente** para superar aquele obstáculo? Se não for, ou ele está incompleto, ou aquele obstáculo esconde dois.

### 4. Sequenciar

Para cada par de objetivos intermediários, pergunte: **um precisa existir antes do outro?**

Três respostas possíveis: antes, depois ou paralelo. A maior parte é paralela — e é isso que revela quanto do plano pode andar ao mesmo tempo, informação que a lista de tarefas nunca dá.

O resultado é uma sequência com dependências explícitas: o plano.

## Delegação

Cada objetivo intermediário pode ser entregue a alguém — e, se for grande, a pessoa que o recebeu pode aplicar a mesma análise dentro dele, produzindo um plano aninhado.

É aqui que a formulação como estado paga o investimento. Delegar uma tarefa transfere a execução; delegar um **estado** transfere o resultado, e deixa a quem executa a liberdade de escolher o meio. A pergunta "isto já é verdade?" tem resposta objetiva — e, portanto, a delegação não devolve ambiguidade para você.

## Erros comuns

**Obstáculos que são desculpas.** "Falta cultura", "a diretoria não apoia". Formulados assim, não geram OI. Especifique: que comportamento, de quem, em que momento?

**OI que é tarefa.** O erro mais comum, e o mais caro — porque o plano parece pronto e não é.

**Sequenciar pela ordem em que se lembrou.** A ordem de lembrança quase nunca é a ordem de dependência.

**Ignorar o obstáculo intransponível.** Se um obstáculo realmente não cai, o objetivo precisa mudar. Descobrir isso na análise custa uma hora; descobrir na execução custa o projeto.

**Plano grande demais.** Acima de dez OIs, quebre em planos menores. Um plano que ninguém consegue ler inteiro não será executado inteiro.

## Mão na massa

<div data-bateria="cap13"></div>

### Leitura executiva

A Análise de Pré-Requisitos transforma um objetivo em plano perguntando **o que impede** que ele já seja verdade. Levante de cinco a dez obstáculos (menos indica pouca reflexão; mais indica objetivo grande demais), converta cada um em um **objetivo intermediário formulado como estado concluído** — nunca tarefa — e sequencie por dependência, o que revela o que pode andar em paralelo. A formulação como estado é o que torna a delegação limpa: transfere-se o resultado, não a execução, e a pergunta "isto já é verdade?" tem resposta objetiva. Obstáculo intransponível descoberto aqui custa uma hora; descoberto na execução, custa o projeto.
